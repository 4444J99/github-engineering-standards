"""Account for completed source reviews without granting control or project acceptance."""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

from .reconciliation import read_records, require
from .semantics import canonical_bytes, stable_id, validate_record

BASE = Path('evidence/semantics')
OWNER = BASE / 'owner-approval-2026-10-06.json'


def build(root: Path) -> dict[str, bytes]:
    """Replay exact accountable attestations; machine checks do not prove their truth."""
    bindings = {}

    def bound(name: str | Path) -> object:
        path = Path(name)
        require(not path.is_absolute() and '..' not in path.parts, 'Unsafe evidence path')
        require(not any((root / Path(*path.parts[:i])).is_symlink()
                        for i in range(1, len(path.parts) + 1)), 'Symlinked evidence')
        raw = (root / path).read_bytes()
        bindings[str(path)] = hashlib.sha256(raw).hexdigest()
        return json.loads(raw) if path.suffix != '.jsonl' else None

    owner = bound(OWNER)
    require(owner['schema'] == 'ges.native-owner-authorization.v1' and
            owner['repository'] == '4444J99/github-engineering-standards' and
            owner['authority_source'] == 'Direct human user instruction in this native conversation',
            'Missing scoped native authorization')
    require(all(owner[key] is False for key in (
        'human_github_review_performed', 'target_policy_adoption_authorized',
        'rights_clearance_authorized', 'native_rollout_authorized', 'whole_project_accepted')),
        'Bounded source review cannot expand authority')
    require(owner['source_review_scope'] ==
            'B0/C0 bounded community batch and the previously agreed five Actions source artifacts' and
            all(pr in owner['integration_scope'] for pr in (479, 480)),
            'Native grant does not cover this source batch')
    b0_names = {str(BASE / 'b0' / name) for name in (
        'input-manifest.v3.json', 'annotations.v3.json', 'revision-v3.json',
        'ledger/occurrences.jsonl', 'ledger/propositions.jsonl', 'ledger/residual.json',
        'independent-review-v2-full.json')}
    c0_names = {str(BASE / 'c0' / name) for name in (
        'input-manifest.v3.json', 'annotations.v3.json',
        'ledger/decisions.jsonl', 'ledger/relationships.json')} | {
        str(BASE / 'b0' / name) for name in (
            'input-manifest.v3.json', 'annotations.v3.json', 'revision-v3.json',
            'ledger/propositions.jsonl', 'ledger/occurrences.jsonl')}
    reports = {}
    for lane in ('b0', 'c0'):
        for role in ('primary', 'independent'):
            path = BASE / lane / f'{role}-review-v3.json'
            report = bound(path)
            schema = (f'ges.{lane}-primary-source-review.v1' if role == 'primary'
                      else f'ges.{lane}-independent-correction-review.v1')
            require(report['schema'] == schema, 'Wrong review schema')
            require(report['status'] == 'PASS', 'Review did not pass')
            reviewer = report['reviewer']
            identity = reviewer.get('identity', reviewer.get('agent_task'))
            require(isinstance(identity, str) and bool(identity) and identity == identity.strip(),
                    'Missing or noncanonical actual reviewer')
            require(reviewer['human_review'] is False, 'Do not impersonate human review')
            if role == 'primary':
                require(identity == owner['recorded_by'], 'Primary not bound to native grant')
            else:
                require(identity != owner['recorded_by'], 'Independent review requires distinct worker')
            paths = [item['path'] for item in report['input_bindings']]
            expected_paths = b0_names if lane == 'b0' else c0_names
            require(len(paths) == len(set(paths)) and set(paths) == expected_paths,
                    'Incomplete reviewed input membership')
            for item in report['input_bindings']:
                bound(item['path'])
                require(bindings[item['path']] == item['sha256'], 'Changed reviewed input')
            key = 'open_source_fidelity_findings' if lane == 'b0' else 'open_semantic_findings'
            require(report[key] == [], 'Unresolved or undeclared review findings')
            reports[lane, role] = (identity, str(path), report)
    require(reports['b0', 'primary'][0] == reports['c0', 'primary'][0] and
            reports['b0', 'independent'][0] == reports['c0', 'independent'][0],
            'Inconsistent review identities')
    b0_scope = reports['b0', 'primary'][2]['scope']
    require(b0_scope == {'artifacts': 22, 'source_lines': 1550, 'occurrences': 178,
                         'propositions': 227, 'nonclaim_spans': 160},
            'Incomplete primary source denominator')
    delta = reports['b0', 'independent'][2]['delta_scope']
    require(all(type(delta[key]) is int and delta[key] == value for key, value in (
        ('source_artifacts_denominator', 22), ('source_lines_denominator', 1550),
        ('occurrences', 178), ('v3_propositions', 227), ('nonclaim_spans', 160))),
        'Incomplete independent source denominator')
    require(reports['c0', 'primary'][2]['scope']['source_artifacts'] == 22 and
            reports['c0', 'independent'][2]['prior_full_source_review']['source_artifacts'] == 22 and
            reports['c0', 'independent'][2]['prior_full_source_review']['source_lines'] == 1550,
            'Incomplete reconciliation source denominator')
    propositions = read_records(root / BASE / 'b0/ledger/propositions.jsonl', 'semantic-proposition')
    occurrences = read_records(root / BASE / 'b0/ledger/occurrences.jsonl', 'semantic-occurrence')
    decisions = read_records(root / BASE / 'c0/ledger/decisions.jsonl', 'reconciliation-decision')
    expected = {p['id'] for p in propositions}
    require(len(expected) == 227 and len(decisions) == 227 and len(occurrences) == 178 and
            {p for d in decisions for p in d['proposition_ids']} == expected,
            'Incomplete bounded denominator')
    require(all(not d['control_references'] and not d['lost_fields'] and
                d['disposition'] in {'REFERENCE', 'CONFLICT'} for d in decisions),
            'Source review cannot silently adopt, exclude or lose meaning')
    require(sum(bool(d['conflicts']) for d in decisions) == 4, 'Source tensions must remain')
    require(reports['b0', 'primary'][2]['scope']['propositions'] == 227 and
            reports['b0', 'independent'][2]['delta_scope']['v3_propositions'] == 227 and
            reports['c0', 'primary'][2]['scope']['propositions_and_decisions'] == 227 and
            reports['c0', 'independent'][2]['scope']['propositions_and_decisions'] == 227,
            'Review scope is incomplete')

    def review(lane: str, role: str) -> dict:
        identity, path, _ = reports[lane, role]
        return {'status': 'REVIEWED', 'reviewer': identity, 'evidence_reference': path}

    reviewed_props = copy.deepcopy(propositions)
    for p in reviewed_props:
        p['primary_review'] = review('b0', 'primary')
        p['omission_review'] = review('b0', 'independent')
        validate_record(p)
    reviewed_decisions = copy.deepcopy(decisions)
    for d in reviewed_decisions:
        d['review'] = review('c0', 'primary')
        d['id'] = stable_id(d)
        validate_record(d)
    pilot = BASE / 'actions-five-file-pilot'
    primary = bound(pilot / 'primary-review.json')
    independent = bound(pilot / 'independent-review.json')
    require(primary['primary_reviewer'] == owner['recorded_by'] and
            independent['reviewer']['agent_task'] == reports['b0', 'independent'][0] and
            independent['status'] == 'PASS' and not independent['open_findings'],
            'Pilot requires complete independent review')
    require(set(independent['input_file_sha256']) ==
            {str(pilot / 'primary-review.json'), *primary['files']},
            'Incomplete pilot reviewed input membership')
    for name, expected_digest in independent['input_file_sha256'].items():
        bound(name)
        require(bindings[name] == expected_digest, 'Changed pilot reviewed input')
    claims, artifacts = set(), set()
    for name in primary['files']:
        document = bound(name)
        if name.endswith('-claims.json'):
            for claim in document['claims']:
                require(claim['claim_id'] not in claims and claim['accepted_policy'] is False,
                        'Duplicate or adopted pilot claim')
                claims.add(claim['claim_id'])
        else:
            require(len(document) == 1 and document[0]['all_claims_accounted_for'] is True,
                    'Incomplete pilot artifact receipt')
            artifacts.add(document[0]['artifact_id'])
    require(len(claims) == 35 and set(independent['scope']['claim_ids_reviewed']) == claims and
            len(artifacts) == 5 and artifacts ==
            {a['artifact_id'] for a in independent['scope']['artifacts']},
            'Incomplete pilot review denominator')
    report = {
        'schema': 'ges.bounded-source-review-accounting.v1',
        'status': 'SOURCE_REVIEW_ACCEPTED', 'input_bindings': bindings,
        'artifacts_reviewed': 22, 'new_artifact_coverage': 0,
        'propositions_reviewed': 227, 'proposition_denominator': 227,
        'source_classifications_reviewed': 227, 'classification_denominator': 227,
        'conflicting_propositions_retained': 4, 'unresolved_source_tension_pairs': 2,
        'accepted_controls': 0, 'policy_adopted': False, 'rights_cleared': False,
        'human_github_review_performed': False, 'whole_project_accepted': False,
        'machine_certified_semantic_truth': False,
        'pilot_source_review_accepted': True, 'pilot_new_artifacts_reviewed': 5,
        'pilot_authored_reference_claims': 35,
        'scope': 'Primary and independent automated source review under native owner authorization. '
                 'No control-adoption audit, rights decision, merge proof or project-gate closure.',
    }
    outputs = {
        'propositions.jsonl': b''.join(canonical_bytes(p) + b'\n' for p in reviewed_props),
        'decisions.jsonl': b''.join(canonical_bytes(d) + b'\n' for d in reviewed_decisions),
    }
    report['output_digests'] = {name: hashlib.sha256(raw).hexdigest() for name, raw in outputs.items()}
    outputs['accounting.json'] = json.dumps(report, indent=2, sort_keys=True).encode() + b'\n'
    return outputs


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path.cwd())
    parser.add_argument('--output', type=Path, default=BASE / 'bounded-reviewed')
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    try:
        outputs = build(args.root)
        if args.check:
            require({p.name for p in args.output.iterdir()} == set(outputs), 'Changed output membership')
            require(all(not (args.output / name).is_symlink() and
                        (args.output / name).read_bytes() == raw for name, raw in outputs.items()),
                    'Changed reviewed accounting')
        else:
            require(not args.output.exists(), 'Output already exists')
            args.output.mkdir(parents=True)
            for name, raw in outputs.items():
                (args.output / name).write_bytes(raw)
        print('227/227 source propositions and classifications reviewed; 0 adopted controls')
        return 0
    except (ValueError, KeyError, TypeError, OSError) as exc:
        print(f'Bounded source review ERROR: {exc}')
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
