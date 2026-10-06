"""Validate and record the frozen A3 inputs without retrieving live sources."""
import argparse
import fcntl
import hashlib
import json
import re
from pathlib import Path

from ges.core import digest, dump, load
from ges.frozen_inputs import validate_capsule
from ges.pages import cached_pages
from ges.pinned_sources import inventory_digest, verify_snapshot
from ges.yamlutil import parse


def fingerprint(path):
    raw = path.read_bytes()
    return {'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)}


def validate_structured(rows, artifacts, texts):
    if not isinstance(rows, list):
        raise ValueError('Structured ledger must be an array')
    seen = set()
    for row in rows:
        if not isinstance(row, dict) or not isinstance(row.get('requirement_id'), str):
            raise ValueError('Invalid structured occurrence')
        identity = row['requirement_id']
        artifact = artifacts.get(row.get('artifact_id'))
        if identity in seen or artifact is None or any(
                row.get(k) != artifact[k] for k in ('source', 'commit', 'path')):
            raise ValueError('Duplicate or unbound structured occurrence')
        text = texts[(row['source'], row['path'])]
        lines = text.splitlines()
        start, end = row.get('start_line'), row.get('end_line')
        if (type(start) is not int or type(end) is not int or
                not 1 <= start <= end <= len(lines) or row.get('line') != start):
            raise ValueError('Invalid structured occurrence span')
        span = '\n'.join(lines[start - 1:end])
        if (row.get('content_sha256') != artifact['sha256'] or
                row.get('span_sha256') != hashlib.sha256(span.encode()).hexdigest()):
            raise ValueError('Structured occurrence digest mismatch')
        if row['source'] == 'microsoft/ghqr':
            definition = row.get('source_definition')
            if (not isinstance(definition, dict) or
                    identity != 'SRC-GHQR-' + definition.get('id', '') or
                    parse(span) != [definition]):
                raise ValueError('Structured GHQR definition differs from source')
        elif row['source'] == 'github/github-well-architected':
            statement = row.get('source_statement')
            if (start != end or not isinstance(statement, str) or
                    span.strip() != '- ' + statement or
                    identity != 'SRC-WA-' + digest([row['path'], start, statement])[:16]):
                raise ValueError('Structured checklist identity differs from source')
        else:
            raise ValueError('Unsupported structured source')
        seen.add(identity)


def receipt(capsule, expected, sources, corpus, rendered, *, expected_structured_count,
            tree_evidence):
    if type(expected_structured_count) is not int or expected_structured_count < 1:
        raise ValueError('Expected structured occurrence count must be positive')
    accounting = validate_capsule(capsule, expected)
    supplements_before = {name: fingerprint(corpus / name) for name in
                          ('structured-source-requirements.json', 'ledger-summary.json')}
    tree_evidence_before = fingerprint(tree_evidence)
    lock = load(capsule / 'sources.lock.json')
    trees = {}
    snapshots = {}
    inventories = {}
    texts = {}
    structured = load(corpus / 'structured-source-requirements.json')
    if not isinstance(structured, list):
        raise ValueError('Structured ledger must be an array')
    tree_records = load(tree_evidence)
    if not isinstance(tree_records, dict) or set(tree_records) != {
            source['repository'] for source in lock['sources']}:
        raise ValueError('Tree evidence source set differs from pinned capsule')
    for source in lock['sources']:
        repository = source['repository']
        slug = repository.replace('/', '__')
        tree = load(capsule / 'sources' / (slug + '.tree-reconciliation.json'))
        if (tree['status'] != 'MATCH' or tree['git_tree_artifacts'] != source['artifacts']
                or tree['archive_artifacts'] != source['artifacts']
                or any(tree[key] for key in
                       ('missing_from_archive', 'extra_in_archive', 'blob_mismatches'))):
            raise ValueError('Source tree reconciliation failed: ' + repository)
        inventory = load(capsule / 'sources' / (slug + '.inventory.json'))
        bound_tree = tree_records.get(repository)
        if (not isinstance(bound_tree, dict) or bound_tree.get('repository') != repository or
                bound_tree.get('commit') != source['commit'] or
                bound_tree.get('inventory_digest') != inventory_digest(inventory) or
                bound_tree.get('status') != 'MATCH' or
                type(bound_tree.get('artifacts')) is not int or
                bound_tree['artifacts'] != source['artifacts'] or
                not isinstance(bound_tree.get('tree_sha'), str) or
                not re.fullmatch('[a-f0-9]{40}', bound_tree['tree_sha']) or
                bound_tree.get('method') != 'GitHub pinned commit and recursive tree API'):
            raise ValueError('Tree evidence differs from pinned revision or inventory')
        trees[repository] = bound_tree
        inventories[repository] = inventory_digest(inventory)
        snapshot = sources / (slug + '.text.jsonl.gz')
        snapshot_before = fingerprint(snapshot)
        retained = verify_snapshot(snapshot, inventory,
                                   repository, source['commit'], retain={
                                       row['path'] for row in structured
                                       if row.get('source') == repository})
        texts.update({(repository, path): text for path, text in retained.items()})
        snapshots[slug + '.text.jsonl.gz'] = fingerprint(snapshot)
        if snapshots[slug + '.text.jsonl.gz'] != snapshot_before:
            raise ValueError('Pinned snapshot changed during validation')
    for name in ('artifacts.jsonl', 'candidates.jsonl', 'dependencies.jsonl',
                 'published-page-ledger.json'):
        if fingerprint(corpus / name) != fingerprint(capsule / 'corpus' / name):
            raise ValueError('Supplement corpus differs from frozen capsule: ' + name)
    dependencies = [json.loads(line) for line in
                    (corpus / 'dependencies.jsonl').read_text().splitlines() if line]
    artifacts = {row['artifact_id']: row for row in
                 (json.loads(line) for line in (corpus / 'artifacts.jsonl').read_text().splitlines())}
    validate_structured(structured, artifacts, texts)
    summary = load(corpus / 'ledger-summary.json')
    if len(structured) != expected_structured_count:
        raise ValueError('Structured occurrence count differs from trusted expected count')
    if len(dependencies) != summary['dependency_references']:
        raise ValueError('Dependency count differs from ledger summary')
    if len(structured) != summary['structured_source_requirements']:
        raise ValueError('Structured occurrence count differs from ledger summary')
    pages = load(capsule / 'corpus/published-page-ledger.json')
    for page in pages:
        matches = page['source_matches']
        if not isinstance(matches, list) or len(set(matches)) != len(matches):
            raise ValueError('Invalid page source-match list')
        bits = page['path'].strip('/').split('/')
        tail = bits[2:] if len(bits) > 1 and '@' in bits[1] else bits[1:]
        stem = '/'.join(tail)
        paths = {'content/' + stem + '.md', 'content/' + stem + '/index.md'} if stem else {'content/index.md'}
        if any(key not in artifacts or artifacts[key]['source'] != 'github/docs' or
               artifacts[key]['path'] not in paths for key in matches):
            raise ValueError('Page references unknown or inappropriate source artifact')
    with (rendered / '.writer.lock').open('a') as writer_lock:
        fcntl.flock(writer_lock, fcntl.LOCK_SH | fcntl.LOCK_NB)
        index_before = fingerprint(rendered / 'index.jsonl')
        bodies = cached_pages(rendered, pages, accounting['published_ledger_sha256'])
        index_after = fingerprint(rendered / 'index.jsonl')
        if index_before != index_after:
            raise ValueError('Rendered index changed during validation')
    applications = [bodies[key] for key in sorted(bodies)]
    if len(applications) != len(pages):
        raise ValueError('Rendered body acquisition is incomplete')
    if (fingerprint(tree_evidence) != tree_evidence_before or
            any(fingerprint(corpus / name) != value for name, value in supplements_before.items()) or
            any(fingerprint(sources / name) != value for name, value in snapshots.items())):
        raise ValueError('Receipt input changed during validation')
    return {
        'schema': 'ges.a3-capsule-receipt.v2',
        'supersedes': 'evidence/a3-six-source-capsule.json',
        'capsule_sha256': expected,
        'capsule_manifest': load(capsule / 'manifest.json'),
        'source_trees': trees,
        'tree_evidence': tree_evidence_before,
        'inventory_identity_digests': inventories,
        'pinned_text_snapshots': snapshots,
        'supplement_files': supplements_before,
        'dependency_references': len(dependencies),
        'structured_occurrences': len(structured),
        'rendered_applications': len(applications),
        'rendered_application_digest': digest(applications),
        'rendered_index': index_after,
        'unresolved_page_source_mappings': sum(not page['source_matches'] for page in pages),
        'semantic_review_performed': False,
        'rendered_source_commit_assured': False,
        'remote_capsule_custody_verified': False,
        'checkout_retained': None,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('capsule', 'sources', 'corpus', 'rendered', 'output'):
        parser.add_argument('--' + name, type=Path, required=True)
    parser.add_argument('--capsule-sha256', required=True)
    parser.add_argument('--expected-structured-count', type=int, required=True)
    parser.add_argument('--tree-evidence', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError('Receipt output already exists')
    result = receipt(args.capsule, args.capsule_sha256, args.sources,
                     args.corpus, args.rendered,
                     expected_structured_count=args.expected_structured_count,
                     tree_evidence=args.tree_evidence)
    dump(args.output, result)
    print(json.dumps({key: result[key] for key in
                      ('capsule_sha256', 'dependency_references',
                       'structured_occurrences', 'rendered_applications',
                       'unresolved_page_source_mappings')}))


if __name__ == '__main__':
    main()
