"""Validate and record the frozen A3 inputs without retrieving live sources."""
import argparse
import hashlib
import json
from pathlib import Path

from ges.core import digest, dump, load
from ges.frozen_inputs import validate_capsule
from ges.pages import cached_pages


def fingerprint(path):
    return {'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'bytes': path.stat().st_size}


def receipt(capsule, expected, sources, corpus, rendered, *, expected_structured_count):
    if type(expected_structured_count) is not int or expected_structured_count < 1:
        raise ValueError('Expected structured occurrence count must be positive')
    accounting = validate_capsule(capsule, expected)
    lock = load(capsule / 'sources.lock.json')
    trees = {}
    snapshots = {}
    for source in lock['sources']:
        repository = source['repository']
        slug = repository.replace('/', '__')
        tree = load(capsule / 'sources' / (slug + '.tree-reconciliation.json'))
        if (tree['status'] != 'MATCH' or tree['git_tree_artifacts'] != source['artifacts']
                or tree['archive_artifacts'] != source['artifacts']
                or any(tree[key] for key in
                       ('missing_from_archive', 'extra_in_archive', 'blob_mismatches'))):
            raise ValueError('Source tree reconciliation failed: ' + repository)
        trees[repository] = tree
        snapshots[slug + '.text.jsonl.gz'] = fingerprint(
            sources / (slug + '.text.jsonl.gz'))
    for name in ('artifacts.jsonl', 'candidates.jsonl', 'dependencies.jsonl',
                 'published-page-ledger.json'):
        if fingerprint(corpus / name) != fingerprint(capsule / 'corpus' / name):
            raise ValueError('Supplement corpus differs from frozen capsule: ' + name)
    dependencies = [json.loads(line) for line in
                    (corpus / 'dependencies.jsonl').read_text().splitlines() if line]
    structured = load(corpus / 'structured-source-requirements.json')
    summary = load(corpus / 'ledger-summary.json')
    if len(structured) != expected_structured_count:
        raise ValueError('Structured occurrence count differs from trusted expected count')
    if len(dependencies) != summary['dependency_references']:
        raise ValueError('Dependency count differs from ledger summary')
    if len(structured) != summary['structured_source_requirements']:
        raise ValueError('Structured occurrence count differs from ledger summary')
    pages = load(capsule / 'corpus/published-page-ledger.json')
    bodies = cached_pages(rendered, pages, accounting['published_ledger_sha256'])
    applications = [bodies[key] for key in sorted(bodies)]
    if len(applications) != len(pages):
        raise ValueError('Rendered body acquisition is incomplete')
    return {
        'schema': 'ges.a3-capsule-receipt.v1',
        'capsule_sha256': expected,
        'capsule_manifest': load(capsule / 'manifest.json'),
        'source_trees': trees,
        'pinned_text_snapshots': snapshots,
        'supplement_files': {name: fingerprint(corpus / name) for name in
                            ('structured-source-requirements.json', 'ledger-summary.json')},
        'dependency_references': len(dependencies),
        'structured_occurrences': len(structured),
        'rendered_applications': len(applications),
        'rendered_application_digest': digest(applications),
        'rendered_index': fingerprint(rendered / 'index.jsonl'),
        'unresolved_page_source_mappings': sum(not page['source_matches'] for page in pages),
        'semantic_review_performed': False,
        'rendered_source_commit_assured': False,
        'remote_capsule_custody_verified': False,
        'checkout_retained': True,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('capsule', 'sources', 'corpus', 'rendered', 'output'):
        parser.add_argument('--' + name, type=Path, required=True)
    parser.add_argument('--capsule-sha256', required=True)
    parser.add_argument('--expected-structured-count', type=int, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError('Receipt output already exists')
    result = receipt(args.capsule, args.capsule_sha256, args.sources,
                     args.corpus, args.rendered,
                     expected_structured_count=args.expected_structured_count)
    dump(args.output, result)
    print(json.dumps({key: result[key] for key in
                      ('capsule_sha256', 'dependency_references',
                       'structured_occurrences', 'rendered_applications',
                       'unresolved_page_source_mappings')}))


if __name__ == '__main__':
    main()
