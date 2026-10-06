"""Propose semantic comparisons and validate externally authorized decisions."""
from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from pathlib import Path

from .semantics import canonical_bytes, validate_record

ROLES = ('primary_reviewers', 'omission_reviewers', 'reconcilers', 'auditors')
AST_FIELDS = {'subject', 'action', 'object', 'modality', 'polarity', 'scope',
              'preconditions', 'qualifiers', 'exceptions', 'consequences', 'parameters'}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def fingerprint(value: object) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def read_records(path: Path, kind: str) -> list[dict]:
    records = []
    for number, line in enumerate(path.read_text(encoding='utf-8').splitlines(), 1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
            validate_record(record)
            require(record['schema'] == 'ges.' + kind + '.v1', 'Wrong record kind')
        except (ValueError, KeyError, TypeError) as exc:
            raise ValueError(f'{path.name} line {number}: {exc}') from exc
        records.append(record)
    return records


def _index(records: list[dict], kind: str) -> dict[str, dict]:
    require(isinstance(records, list), 'Records must be an array')
    indexed = {}
    for record in records:
        validate_record(record)
        require(record['schema'] == 'ges.' + kind + '.v1', 'Wrong record kind')
        require(record['id'] not in indexed, 'Duplicate record identity')
        indexed[record['id']] = record
    return indexed


def inputs(propositions: list[dict], catalog: list[dict]) -> tuple[dict, dict, str]:
    """Bind the whole proposition records, including reviews and applicability."""
    indexed = _index(propositions, 'semantic-proposition')
    require(bool(indexed), 'No propositions to reconcile')
    require(isinstance(catalog, list), 'Catalog must be an array')
    controls = {}
    for control in catalog:
        require(isinstance(control, dict) and isinstance(control.get('id'), str)
                and bool(control['id'].strip()) and type(control.get('revision')) is int
                and control['revision'] > 0, 'Malformed control identity')
        require(control['id'] not in controls, 'Duplicate control identity')
        controls[control['id']] = control
    bound = {'propositions': [indexed[key] for key in sorted(indexed)],
             'catalog': [controls[key] for key in sorted(controls)]}
    return indexed, controls, fingerprint(bound)


def propose(propositions: list[dict], catalog: list[dict]) -> dict:
    """Group exact predicate strings; every comparison remains a proposal."""
    indexed, _, input_digest = inputs(propositions, catalog)
    groups = defaultdict(list)
    for identity, record in indexed.items():
        ast = record['semantic_ast']
        groups[canonical_bytes([ast[key] for key in ('subject', 'action', 'object')])].append(identity)
    comparisons = []
    for key in sorted(groups):
        members = sorted(groups[key])
        if len(members) < 2:
            continue
        records = [indexed[identity] for identity in members]
        differing = sorted(field for field in AST_FIELDS
                           if len({canonical_bytes(r['semantic_ast'][field])
                                   for r in records}) > 1)
        applicability_differs = len({canonical_bytes(r['applicability'])
                                    for r in records}) > 1
        possible_conflict = bool({'polarity', 'modality'} & set(differing))
        comparison = {
            'proposition_ids': members,
            'relation': 'POSSIBLE_CONFLICT' if possible_conflict else 'RELATED',
            'differing_fields': differing,
            'applicability_differs': applicability_differs,
            'status': 'PROPOSED',
        }
        comparison['id'] = 'comparison:' + fingerprint(comparison)
        comparisons.append(comparison)
    return {'schema': 'ges.reconciliation-proposals.v1',
            'input_digest': input_digest, 'comparisons': comparisons,
            'proposition_ids': sorted(indexed),
            'semantic_truth_certified': False, 'policy_adopted': False}


def _authority(policy: dict, input_digest: str) -> None:
    require(isinstance(policy, dict) and set(policy) == {
        'schema', 'approval_reference', 'input_digest', *ROLES}, 'Malformed authority policy')
    require(policy['schema'] == 'ges.reconciliation-authority.v1', 'Wrong authority schema')
    require(isinstance(policy['approval_reference'], str)
            and bool(policy['approval_reference'].strip()), 'Missing authority approval reference')
    require(policy['input_digest'] == input_digest, 'Stale authority input digest')
    for role in ROLES:
        values = policy[role]
        require(isinstance(values, list) and bool(values)
                and all(isinstance(v, str) and bool(v.strip()) for v in values)
                and len(set(values)) == len(values), 'Invalid authority role: ' + role)


def _review(review: dict, allowed: list[str]) -> str:
    require(review['status'] == 'REVIEWED', 'Proposal cannot satisfy a review gate')
    require(review['reviewer'] in allowed, 'Unauthorized reviewer')
    return review['reviewer']


def _evidence(reference: str, root: Path, kind: str, identity: str,
              subject_digest: str, input_digest: str) -> str:
    """Resolve bounded evidence without trusting symlinks or self-asserted digests."""
    require(isinstance(reference, str) and bool(reference.strip()), 'Missing evidence reference')
    relative = Path(reference)
    require(not relative.is_absolute() and '..' not in relative.parts
            and relative.parts and relative.parts[0] == 'evidence'
            and relative.suffix == '.json' and '\\' not in reference,
            'Unsafe evidence reference')
    for length in range(1, len(relative.parts) + 1):
        require(not (root / Path(*relative.parts[:length])).is_symlink(),
                'Symlinked evidence reference')
    path = root / relative
    require(path.is_file() and path.stat().st_size <= 1_000_000,
            'Evidence is missing or exceeds size bound')
    raw = path.read_bytes()
    require(len(raw) <= 1_000_000, 'Evidence exceeds size bound')
    document = json.loads(raw)
    require(isinstance(document, dict) and set(document) == {
        'schema', 'kind', 'reviewer', 'subject_digest', 'input_digest', 'outcome'},
        'Malformed reconciliation evidence')
    require(document == {
        'schema': 'ges.reconciliation-evidence.v1', 'kind': kind,
        'reviewer': identity, 'subject_digest': subject_digest,
        'input_digest': input_digest, 'outcome': 'PASS'},
        'Evidence does not bind reviewed subject and inputs')
    return hashlib.sha256(raw).hexdigest()


def _proposition_subject(record: dict) -> str:
    return fingerprint({key: value for key, value in record.items()
                        if key not in ('primary_review', 'omission_review')})


def _disposition(decision: dict, indexed: dict, controls: dict) -> None:
    ids = decision['proposition_ids']
    require(all(identity in indexed for identity in ids), 'Unknown proposition reference')
    fields = set(decision['preserved_fields']) | set(decision['lost_fields'])
    require(fields == AST_FIELDS and not (set(decision['preserved_fields'])
                & set(decision['lost_fields'])), 'Semantic field accounting is incomplete or overlapping')
    conflicts = decision['conflicts']
    require(all(identity in indexed for identity in conflicts), 'Unknown conflict reference')
    references = decision['control_references']
    require(len({r['id'] for r in references}) == len(references), 'Duplicate control reference')
    for reference in references:
        require(reference['id'] in controls and
                controls[reference['id']]['revision'] == reference['revision'],
                'Unknown or stale control revision')
    disposition = decision['disposition']
    if disposition in ('EXISTING_CONTROL', 'NEW_CONTROL', 'SPECIALIZATION'):
        require(bool(references), 'Control disposition requires control references')
        require(not conflicts, 'Control disposition cannot erase a conflict')
    else:
        require(not references, 'Non-control disposition cannot map controls')
    if disposition == 'CONFLICT':
        require(len(set(ids) | set(conflicts)) >= 2 and bool(conflicts)
                and decision['source_treatment'] == 'CONFLICTING',
                'CONFLICT requires counterpart identities and conflicting treatment')
    else:
        require(not conflicts and decision['source_treatment'] != 'CONFLICTING',
                'Conflict must retain an explicit CONFLICT disposition')
    if disposition == 'DUPLICATE':
        records = [indexed[identity] for identity in ids]
        require(len({canonical_bytes([r['semantic_ast'], r['applicability']])
                     for r in records}) == 1 and
                all(not r['preserved_differences'] and not r['ambiguities'] for r in records)
                and sum(len(r['occurrence_ids']) for r in records) >= 2
                and not decision['lost_fields'], 'False equivalence or unsubstantiated duplicate')
    if disposition == 'SUPERSEDED':
        require(len(ids) >= 2, 'SUPERSEDED requires predecessor and successor identities')
    if disposition == 'EXCLUDED_WITH_REASON':
        require(decision['source_treatment'] == 'OMITTED', 'Exclusion requires omitted treatment')


def audit(propositions: list[dict], catalog: list[dict], decisions: list[dict],
          policy: dict, evidence_root: Path, audits: list[dict]) -> dict:
    """Validate receipts and coverage; conflict records always remain open."""
    indexed, controls, input_digest = inputs(propositions, catalog)
    require(len(indexed) <= 250, 'Audit tranche exceeds 250 propositions')
    _authority(policy, input_digest)
    decision_index = _index(decisions, 'reconciliation-decision')
    require(isinstance(audits, list), 'Audit receipts must be an array')
    audit_index = {}
    for receipt in audits:
        require(isinstance(receipt, dict) and set(receipt) == {
            'decision_id', 'auditor', 'evidence_reference'}, 'Malformed audit receipt')
        identity = receipt['decision_id']
        require(isinstance(identity, str) and identity in decision_index
                and identity not in audit_index, 'Unknown or duplicate audited decision')
        audit_index[identity] = receipt
    require(set(audit_index) == set(decision_index), 'Every decision requires independent audit')
    covered = set()
    conflicted = set()
    evidence_digests = {}
    for identity in sorted(decision_index):
        decision = decision_index[identity]
        _disposition(decision, indexed, controls)
        require(not covered.intersection(decision['proposition_ids']), 'Proposition disposition duplicated')
        reconciler = _review(decision['review'], policy['reconcilers'])
        receipt = audit_index[identity]
        auditor = receipt['auditor']
        require(auditor in policy['auditors'] and auditor != reconciler,
                'Unauthorized or non-independent auditor')
        for prop_id in sorted(set(decision['proposition_ids']) | set(decision['conflicts'])):
            record = indexed[prop_id]
            primary = _review(record['primary_review'], policy['primary_reviewers'])
            omission = _review(record['omission_review'], policy['omission_reviewers'])
            require(len({primary, omission, reconciler, auditor}) == 4,
                    'Review roles must be independent for each proposition')
            for field, kind, reviewer in (
                    ('primary_review', 'PRIMARY', primary),
                    ('omission_review', 'OMISSION', omission)):
                reference = record[field]['evidence_reference']
                evidence_digests[reference] = _evidence(
                    reference, evidence_root, kind, reviewer,
                    _proposition_subject(record), input_digest)
        reference = decision['review']['evidence_reference']
        evidence_digests[reference] = _evidence(
            reference, evidence_root, 'RECONCILIATION', reconciler,
            fingerprint(decision), input_digest)
        reference = receipt['evidence_reference']
        evidence_digests[reference] = _evidence(
            reference, evidence_root, 'INDEPENDENT_AUDIT', auditor,
            fingerprint(decision), input_digest)
        covered.update(decision['proposition_ids'])
        if decision['disposition'] == 'CONFLICT':
            conflicted.update(decision['proposition_ids'])
            conflicted.update(decision['conflicts'])
    comparison = propose(propositions, catalog)
    candidate_conflicts = {identity for group in comparison['comparisons']
                          if group['relation'] == 'POSSIBLE_CONFLICT'
                          for identity in group['proposition_ids']}
    # The detector is deliberately conservative: its findings need an explicit
    # conflict disposition before they may be reported as reviewed.
    require(not (candidate_conflicts & covered) - conflicted,
            'Potential conflict would be erased by a non-conflict disposition')
    missing = set(indexed) - covered
    unresolved = missing | conflicted | {
        identity for identity, record in indexed.items() if record['ambiguities']}
    return {'schema': 'ges.reconciliation-audit.v1', 'input_digest': input_digest,
            'decisions_digest': fingerprint([decision_index[k] for k in sorted(decision_index)]),
            'authority_digest': fingerprint(policy),
            'audit_receipts_digest': fingerprint(sorted(audits, key=lambda r: r['decision_id'])),
            'evidence_sha256': dict(sorted(evidence_digests.items())),
            'known_proposition_count': len(indexed), 'validated_decision_count': len(decisions),
            'covered_proposition_ids': sorted(covered), 'unmapped_proposition_ids': sorted(missing),
            'conflict_proposition_ids': sorted(conflicted),
            'unresolved_proposition_ids': sorted(unresolved),
            'decision_accounting_complete': not unresolved,
            'semantic_truth_certified': False, 'policy_adopted': False}
