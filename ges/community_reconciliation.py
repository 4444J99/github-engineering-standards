"""Compile authored C0 relationships; never infer semantics or approve reviews."""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import tempfile
import os

from .reconciliation import AST_FIELDS, fingerprint, read_records, require
from .semantics import canonical_bytes, stable_id, validate_record

BASE = Path('evidence/semantics/c0')
B0 = Path('evidence/semantics/b0')
MANIFEST = BASE / 'input-manifest.v3.json'
ANNOTATIONS = BASE / 'annotations.v3.json'
CLASSES = {'DISTINCT', 'SPECIALIZED', 'REFERENTIAL', 'CONFLICTING'}
PROPOSED = {'status': 'PROPOSED', 'reviewer': None, 'evidence_reference': None}
INPUT_FILES = {str(B0 / name) for name in (
    'input-manifest.v3.json', 'annotations.v3.json', 'revision-v3.json', 'ledger/propositions.jsonl',
    'ledger/occurrences.jsonl', 'ledger/receipt.json')}


def validate_specialization(identity: str, relation: dict, indexed: dict) -> None:
    """Check declared direction and predicate-preserving narrowing, not semantic truth."""
    direction = relation['specialization']
    require(isinstance(direction, dict) and set(direction) == {'base_id', 'refinement_id'},
            'Specialization requires an explicit base and refinement')
    base_id, refinement_id = direction['base_id'], direction['refinement_id']
    require(base_id != refinement_id and {base_id, refinement_id} ==
            {identity, *relation['counterpart_ids']}, 'Specialization direction does not bind peers')
    base, refinement = indexed[base_id], indexed[refinement_id]
    require(base['applicability'] == refinement['applicability'], 'Specialization changes unaccounted applicability')
    fields = AST_FIELDS - {'preconditions', 'qualifiers'}
    require(all(base['semantic_ast'][field] == refinement['semantic_ast'][field] for field in fields),
            'Related/complementary actions are not predicate-preserving specialization')
    differences = False
    for field in ('preconditions', 'qualifiers'):
        broad, narrow = set(base['semantic_ast'][field]), set(refinement['semantic_ast'][field])
        require(broad <= narrow, 'Specialization loses a condition or qualifier')
        differences |= broad != narrow
    require(differences, 'Specialization requires an explicit narrowing difference')


def build(root: Path) -> dict[str, bytes]:
    manifest = json.loads((root / MANIFEST).read_text())
    require(set(manifest) == {'schema', 'b0_commit', 'files', 'proposition_ids',
                             'annotations_digest'}, 'Malformed C0 manifest')
    require(manifest['schema'] == 'ges.c0-input.v1', 'Wrong C0 input schema')
    require(manifest['b0_commit'] == 'b2f73d3df70dcd08a72de6e0d7d7a0ca28278b9f',
            'Unexpected B0 revision')
    require(set(manifest['files']) == INPUT_FILES, 'Incomplete B0 input membership')
    for name, digest in manifest['files'].items():
        path = root / name
        require(not any((root / Path(*path.relative_to(root).parts[:i])).is_symlink()
                        for i in range(1, len(path.relative_to(root).parts) + 1)),
                'Symlinked input')
        require(hashlib.sha256(path.read_bytes()).hexdigest() == digest,
                'Changed frozen input: ' + name)
    propositions = read_records(root / B0 / 'ledger/propositions.jsonl',
                                'semantic-proposition')
    indexed = {p['id']: p for p in propositions}
    require(0 < len(propositions) <= 250 and len(indexed) == len(propositions),
            'Invalid proposition denominator')
    require(sorted(indexed) == manifest['proposition_ids'], 'Changed denominator')
    occurrences = read_records(root / B0 / 'ledger/occurrences.jsonl',
                               'semantic-occurrence')
    occurrence_index = {o['id']: o for o in occurrences}
    require(len(occurrence_index) == len(occurrences), 'Duplicate occurrence')
    annotations = json.loads((root / ANNOTATIONS).read_text())
    require(fingerprint(annotations) == manifest['annotations_digest'],
            'Changed authored annotations')
    require(isinstance(annotations, list), 'Annotations must be an array')
    authored = {}
    for row in annotations:
        require(set(row) == {'proposition_id', 'classification', 'rationale',
                             'relationships', 'review'}, 'Malformed annotation')
        identity = row['proposition_id']
        require(identity in indexed and identity not in authored,
                'Unknown or duplicate proposition disposition')
        require(row['classification'] in CLASSES and row['review'] == PROPOSED,
                'C0 staging cannot confer review approval')
        require(isinstance(row['rationale'], str) and bool(row['rationale'].strip()),
                'Missing authored rationale')
        require(isinstance(row['relationships'], list), 'Malformed relationships')
        seen = set()
        for relation in row['relationships']:
            fields = {'classification', 'counterpart_ids', 'rationale'}
            if relation.get('classification') == 'SPECIALIZED':
                fields.add('specialization')
            require(set(relation) == fields,
                    'Malformed relationship')
            require(relation['classification'] in {'SPECIALIZED', 'CONFLICTING', 'RELATED', 'COMPLEMENTARY'},
                    'Unsupported source relationship')
            peers = relation['counterpart_ids']
            require(isinstance(peers, list) and bool(peers) and
                    len(peers) == len(set(peers)) and identity not in peers and
                    all(peer in indexed for peer in peers), 'Invalid counterparts')
            require(isinstance(relation['rationale'], str) and
                    bool(relation['rationale'].strip()), 'Missing relationship rationale')
            if relation['classification'] == 'SPECIALIZED':
                validate_specialization(identity, relation, indexed)
            signature = fingerprint(relation)
            require(signature not in seen, 'Duplicate relationship')
            seen.add(signature)
        classes = {r['classification'] for r in row['relationships']}
        expected = 'CONFLICTING' if 'CONFLICTING' in classes else (
            'SPECIALIZED' if 'SPECIALIZED' in classes else row['classification'])
        require(row['classification'] == expected and
                (bool(classes & {'SPECIALIZED', 'CONFLICTING'}) ==
                 (row['classification'] in {'SPECIALIZED', 'CONFLICTING'})),
                'Classification does not match relationships')
        authored[identity] = row
    require(set(authored) == set(indexed), 'Missing proposition disposition')
    for identity, row in authored.items():
        for relation in row['relationships']:
            for peer in relation['counterpart_ids']:
                reciprocal = {'classification': relation['classification'],
                              'counterpart_ids': sorted((set(relation['counterpart_ids']) |
                                                        {identity}) - {peer}),
                              'rationale': relation['rationale']}
                if 'specialization' in relation:
                    reciprocal['specialization'] = relation['specialization']
                require(reciprocal in authored[peer]['relationships'],
                        'Asymmetric authored relationship')
    decisions, rows, conflicts = [], [], []
    for identity in sorted(indexed):
        p, annotation = indexed[identity], authored[identity]
        counterparts = sorted({peer for relation in annotation['relationships']
                               if relation['classification'] == 'CONFLICTING'
                               for peer in relation['counterpart_ids']})
        decision = {
            'schema': 'ges.reconciliation-decision.v1',
            'proposition_ids': [identity],
            'disposition': 'CONFLICT' if counterparts else 'REFERENCE',
            'source_treatment': 'CONFLICTING' if counterparts else 'RETAINED',
            'control_references': [], 'rationale': annotation['rationale'],
            'preserved_fields': sorted(AST_FIELDS), 'lost_fields': [],
            'conflicts': counterparts, 'review': dict(PROPOSED),
        }
        decision['id'] = stable_id(decision)
        validate_record(decision)
        decisions.append(decision)
        locators = []
        for occurrence in p['occurrence_ids']:
            require(occurrence in occurrence_index, 'Missing source occurrence')
            locators.append(occurrence_index[occurrence]['source'])
        rows.append({**annotation, 'decision_id': decision['id'],
                     'proposition': p, 'source_locators': locators})
        if counterparts:
            conflicts.append({'proposition_id': identity, 'counterpart_ids': counterparts,
                              'rationale': annotation['rationale']})
    receipt = {
        'schema': 'ges.c0-staging-receipt.v1', 'status': 'HOLD',
        'input_digest': fingerprint(manifest), 'annotations_digest': fingerprint(annotations),
        'propositions': len(indexed), 'decisions': len(decisions),
        'classifications': dict(sorted(Counter(a['classification'] for a in annotations).items())),
        'approved_decisions': 0, 'semantic_truth_certified': False, 'policy_adopted': False,
        'b0_review_status': 'PROPOSED', 'output_digests': {},
    }
    residual = {
        'schema': 'ges.c0-residual.v1', 'status': 'HOLD',
        'pending_decision_reviews': sorted(d['id'] for d in decisions),
        'conflicts': conflicts,
        'inherited_b0_hold': 'B0 primary/omission and artifact reviews, foundation acceptance remain B0 obligations.',
        'pending_gates': ['B0 and foundation acceptance', 'Authorized reconciliation reviews',
                          'Independent audit', 'Reviewed source-conflict classifications (resolution owned downstream)',
                          'Exact-head human approval and remote CI',
                          'Merge and merged-main verification', 'Owner scope acceptance'],
    }
    review = ['# C0 source-only reconciliation review', '',
              'HOLD — all decisions PROPOSED; zero approvals or policy adoption.', '',
              'RELATED/COMPLEMENTARY links do not change a DISTINCT or REFERENTIAL disposition. SPECIALIZED requires an explicit base-to-refinement direction.',
              'REFERENCE in A5 retains a proposition as source evidence; it does not exclude actionable guidance.',
              'No duplicates or supersessions are asserted across differing scope/applicability.', '']
    for row in rows:
        ast = row['proposition']['semantic_ast']
        review.extend([f"## {row['proposition_id']}", '',
                       f"{row['classification']}: {ast['modality']} {ast['subject']} — {ast['action']} {ast['object']}", '',
                       row['rationale'], '', 'Source locators: `' +
                       json.dumps(row['source_locators'], sort_keys=True) + '`', '',
                       'Preserved AST/applicability: `' + json.dumps({
                           'semantic_ast': ast, 'applicability': row['proposition']['applicability'],
                           'ambiguities': row['proposition']['ambiguities']}, sort_keys=True) + '`', '',
                       'Relationships: `' + json.dumps(row['relationships'], sort_keys=True) + '`', ''])
    encode = lambda obj: json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False).encode() + b'\n'
    outputs = {'decisions.jsonl': b''.join(canonical_bytes(d) + b'\n' for d in decisions),
               'relationships.json': encode(rows), 'residual.json': encode(residual),
               'review.md': ('\n'.join(review).rstrip() + '\n').encode()}
    receipt['output_digests'] = {name: hashlib.sha256(raw).hexdigest()
                                 for name, raw in sorted(outputs.items())}
    outputs['receipt.json'] = encode(receipt)
    return outputs


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path.cwd())
    parser.add_argument('--output', type=Path, default=BASE / 'ledger')
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    try:
        outputs = build(args.root)
        if args.check:
            require(args.output.is_dir() and not args.output.is_symlink(), 'Missing/unsafe output')
            require({p.name for p in args.output.iterdir()} == set(outputs), 'Changed output membership')
            for name, raw in outputs.items():
                target = args.output / name
                require(not target.is_symlink() and target.read_bytes() == raw,
                        'Changed generated output: ' + name)
        else:
            require(not args.output.exists() and not args.output.is_symlink(), 'Output already exists')
            args.output.parent.mkdir(parents=True, exist_ok=True)
            with tempfile.TemporaryDirectory(dir=args.output.parent) as staging:
                directory = Path(staging) / 'ledger'
                directory.mkdir()
                for name, raw in outputs.items():
                    (directory / name).write_bytes(raw)
                os.rename(directory, args.output)
        count = json.loads(outputs['receipt.json'])['decisions']
        print(f'C0 structural staging valid: {count} proposals; HOLD; zero approved decisions')
        return 0
    except (ValueError, KeyError, TypeError, OSError) as exc:
        print(f'C0 ERROR: {exc}')
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
