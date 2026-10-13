"""Check a pinned, additive workload transition without awarding semantic credit."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from .claim_workload import _recorded_claim_paths, _sha, check_inventory
from .core import digest
from .evidence_paths import canonical_path


# Independent metadata/code review binds the approved addition and both reports.
# Candidate data cannot select a different membership or repin its own authority.
DEFAULT_TRANSITION_SHA256 = 'f92cbe31c618e793b9bdc07f51b609d0b464fa5f8698fe715efc6bb542089dd8'


def check_transition(reviews: Path, artifacts: Path, reconciliation: Path,
                     baseline: Path, historical: Path, provenance: Path,
                     transition: Path, current: Path) -> dict:
    """Reproduce both snapshots and require exactly the independently pinned delta."""
    transition_path = canonical_path(
        transition, symlink_error='Symlink workload transition is not permitted')
    transition_raw = transition_path.read_bytes()
    if _sha(transition_raw) != DEFAULT_TRANSITION_SHA256:
        raise ValueError('Workload transition differs from independently pinned contract')
    contract = json.loads(transition_raw)
    if not isinstance(contract, dict) or contract.get('schema') != 'ges.claim-workload-transition.v1':
        raise ValueError('Invalid workload transition contract')
    paths = {'historical': historical, 'baseline': baseline, 'provenance': provenance,
             'artifacts': artifacts, 'reconciliation': reconciliation, 'current': current}
    if not isinstance(contract.get('bindings'), dict) or set(contract['bindings']) != set(paths):
        raise ValueError('Incomplete workload transition bindings')
    before = {}
    for label, path in paths.items():
        canonical_path(path, symlink_error='Symlink workload transition input is not permitted')
        raw = path.read_bytes()
        if _sha(raw) != contract['bindings'][label]:
            raise ValueError('Pinned workload transition input differs: ' + label)
        before[label] = raw
    added = contract.get('added_document')
    added_path = _recorded_claim_paths(reviews, [added])[0]
    pairs = contract.get('successor_pairs')
    if (not isinstance(pairs, list) or not pairs or
            any(not isinstance(pair, dict) or set(pair) != {'predecessor', 'successor'} or
                any(not isinstance(value, str) or not value.strip() for value in pair.values())
                for pair in pairs)):
        raise ValueError('Invalid workload successor pairs')
    predecessors = [pair['predecessor'] for pair in pairs]
    successors = [pair['successor'] for pair in pairs]
    if (len(set(predecessors)) != len(pairs) or len(set(successors)) != len(pairs) or
            set(predecessors) & set(successors) or added['claims'] != len(pairs) or
            not isinstance(contract.get('family_id'), str) or
            not re.fullmatch('[a-f0-9]{64}', contract['family_id'])):
        raise ValueError('Invalid workload successor identities or family')
    for key in ('new_review_credit', 'new_reconciliation_credit'):
        if type(contract.get(key)) is not int or contract[key] != 0:
            raise ValueError('Workload migration cannot award review or reconciliation credit')

    # This preserves the original equivalence/provenance checks. Its explicit
    # membership selection is never used for the full-current check below.
    old = check_inventory(reviews, artifacts, reconciliation, baseline,
                          historical=historical, provenance=provenance,
                          recorded_membership=True)
    # The old replay validates this pinned sibling reference. Keep that same
    # authority stable through the current replay and the outer final checks.
    reference = json.loads(before['provenance'])['source_identity_reference']
    reference_input = provenance.parent / reference['path']
    reference_path = canonical_path(
        reference_input, symlink_error='Symlink source identity reference is not permitted')
    reference_raw = reference_path.read_bytes()
    if _sha(reference_raw) != reference['sha256']:
        raise ValueError('Source identity reference changed during transition check')
    new = check_inventory(reviews, artifacts, reconciliation, current)
    old_documents = old['inputs']['claim_documents']
    if added['path'] in {item['path'] for item in old_documents}:
        raise ValueError('Successor document replaces a preserved document')
    expected_documents = sorted([*old_documents, added], key=lambda item: item['path'])
    if digest(new['inputs']['claim_documents']) != digest(expected_documents):
        raise ValueError('Current document membership is not exactly the approved addition')
    for field in ('artifacts_sha256', 'reconciliation_sha256'):
        if new['inputs'][field] != old['inputs'][field]:
            raise ValueError('Workload transition changed a frozen input: ' + field)

    old_ids = {cid for family in old['families'] for cid in family['claim_ids']}
    new_ids = {cid for family in new['families'] for cid in family['claim_ids']}
    if (not set(predecessors) <= old_ids or set(successors) & old_ids or
            new_ids != old_ids | set(successors)):
        raise ValueError('Workload claim membership is not the exact successor transition')
    added_raw = added_path.read_bytes()
    if _sha(added_raw) != added['sha256']:
        raise ValueError('Successor bytes differ from reviewed correction')
    actual_pairs = [{'predecessor': claim.get('supersedes_claim_id'),
                     'successor': claim.get('claim_id')}
                    for claim in json.loads(added_raw)['claims']]
    if digest(sorted(actual_pairs, key=lambda pair: pair['successor'])) != digest(
            sorted(pairs, key=lambda pair: pair['successor'])):
        raise ValueError('Successor predecessor links differ from reviewed correction')
    old_family_ids = {family['family_id'] for family in old['families']}
    if contract['family_id'] not in old_family_ids:
        raise ValueError('Approved successor family is missing from the baseline')
    stripped = []
    for family in new['families']:
        additions = set(family['claim_ids']) & set(successors)
        if additions and family['family_id'] != contract['family_id']:
            raise ValueError('Successor moved to a different workload family')
        stripped.append({**family, 'claim_ids': [cid for cid in family['claim_ids']
                                               if cid not in successors]})
    if digest(stripped) != digest(old['families']):
        raise ValueError('Preserved workload families or receipt members changed')
    deltas = {'recorded_claims': len(successors), 'claim_documents': 1,
              'recorded_claims_without_reconciliation': len(successors),
              'reconciliation_records_present': 0,
              'new_review_credit': 0, 'new_reconciliation_credit': 0}
    for field, delta in deltas.items():
        if (type(old['counts'][field]) is not int or type(new['counts'][field]) is not int or
                new['counts'][field] != old['counts'][field] + delta):
            raise ValueError('Unexpected workload accounting transition: ' + field)

    # The outer transaction also observes inputs after both independent replays.
    # An ignored historical extra must still be present in the full current set.
    expected_paths = _recorded_claim_paths(reviews, new['inputs']['claim_documents'])
    if sorted(reviews.glob('*-claims.json')) != expected_paths:
        raise ValueError('Current document membership changed during transition check')
    for path, item in zip(expected_paths, new['inputs']['claim_documents']):
        if _sha(path.read_bytes()) != item['sha256']:
            raise ValueError('Claim document changed during transition check')
    for label, path in paths.items():
        canonical_path(path, symlink_error='Symlink workload transition input is not permitted')
        if path.read_bytes() != before[label]:
            raise ValueError('Workload transition input changed during check: ' + label)
    if (canonical_path(reference_input,
                       symlink_error='Symlink source identity reference is not permitted') !=
            reference_path or reference_path.read_bytes() != reference_raw):
        raise ValueError('Source identity reference changed during transition check')
    if (canonical_path(transition, symlink_error='Symlink workload transition is not permitted') !=
            transition_path or transition_path.read_bytes() != transition_raw):
        raise ValueError('Workload transition contract changed during check')
    return {'status': 'MATCH', 'scope': 'METADATA_WORKLOAD_TRANSITION_ONLY',
            'transition_id': contract['transition_id'],
            'historical_recorded_claims': old['counts']['recorded_claims'],
            'current_recorded_claims': new['counts']['recorded_claims'],
            'current_claim_documents': new['counts']['claim_documents'],
            'added_claims': len(successors), 'preserved_families': len(old['families']),
            'workload_receipt_subjects': new['counts']['reconciliation_records_present'],
            'recorded_claims_without_workload_receipt':
                new['counts']['recorded_claims_without_reconciliation'],
            'new_review_credit': 0, 'new_reconciliation_credit': 0,
            'full_source_provenance_replayed': False,
            'replacement_receipt_envelopes_issued': False}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('reviews', 'artifacts', 'reconciliation', 'baseline', 'historical',
                 'provenance', 'transition', 'check'):
        parser.add_argument('--' + name, type=Path, required=True)
    args = parser.parse_args()
    try:
        result = check_transition(args.reviews, args.artifacts, args.reconciliation,
                                  args.baseline, args.historical, args.provenance,
                                  args.transition, args.check)
    except (OSError, EOFError, ValueError, KeyError, TypeError) as exc:
        parser.exit(1, 'Claim workload transition failed: ' + str(exc) + '\n')
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
