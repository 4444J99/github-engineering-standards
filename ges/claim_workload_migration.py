"""Reproduce frozen and expanded workload inventories for the five WA successors.

This metadata check grants no semantic, reconciliation, or acceptance credit.
Historical accounting equivalence remains unchanged; full current membership is
always checked separately. A later migration requires its own reviewed scope.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from .claim_workload import check_inventory
from .core import digest
from .evidence_paths import canonical_path


# These already reviewed bytes are independent of the new, mutable report.
# Do not repin historical evidence to accommodate a changed current inventory.
FROZEN_SHA256 = {
    'historical': '6151dcc71dda756610f371337bebe9981c0f9656cc6f7b252ad60e007701f5ec',
    'baseline': '2e718486119b29cf286f4b21f067d67dc3bea17f2559a45fbc01105931a22658',
    'provenance': '239fc3e89643202c9a7935749249eb4a0ca14e67a32c6e2a0517166a81e9bbf8',
    'approval': '9c17a1fcbfee8a38e5d7dc49e95e4df108f96b43dc8e51ad744342c4d0ba4e04',
}
SUCCESSOR_DOCUMENT = 'wa-application-security-correction-01-claims.json'


def _sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _fingerprints(paths: list[Path]) -> dict[Path, str]:
    result = {}
    for path in paths:
        canonical_path(path, symlink_error='Symlink workload migration input is not permitted')
        result[path] = _sha(path.read_bytes())
    return result


def check_migration(reviews: Path, artifacts: Path, reconciliation: Path,
                    baseline: Path, current: Path, historical: Path,
                    provenance: Path, approval: Path) -> dict:
    """Verify both complete states and only the previously reviewed addition."""
    reviews = canonical_path(reviews, symlink_error='Symlink review directory is not permitted')
    inputs = dict(artifacts=artifacts, reconciliation=reconciliation,
                  baseline=baseline, current=current, historical=historical,
                  provenance=provenance, approval=approval)
    inputs = {key: canonical_path(path, symlink_error='Symlink migration input is not permitted')
              for key, path in inputs.items()}
    raw = {key: path.read_bytes() for key, path in inputs.items()}
    for key, expected in FROZEN_SHA256.items():
        if _sha(raw[key]) != expected:
            raise ValueError('Migration input differs from independently pinned ' + key)
    baseline_doc = json.loads(raw['baseline'])
    provenance_doc = json.loads(raw['provenance'])
    approval_doc = json.loads(raw['approval'])
    if (_sha(raw['artifacts']) !=
            provenance_doc['bindings']['compressed_artifact_inventory_sha256']):
        raise ValueError('Migration compressed artifact fingerprint differs before replay')
    reference = inputs['provenance'].parent / provenance_doc['source_identity_reference']['path']
    paths = sorted(reviews.glob('*-claims.json'))
    before = _fingerprints([*inputs.values(), reference, *paths])
    if any(before[inputs[key]] != _sha(value) for key, value in raw.items()):
        raise ValueError('Workload migration inputs changed before check')
    baseline_membership = baseline_doc['inputs']['claim_documents']
    expected_names = {item['path'] for item in baseline_membership}
    if (SUCCESSOR_DOCUMENT in expected_names or
            {path.name for path in paths} != expected_names | {SUCCESSOR_DOCUMENT}):
        raise ValueError('Current membership is not exactly the baseline plus approved document')
    successor_path = reviews / SUCCESSOR_DOCUMENT
    successor_raw = successor_path.read_bytes()
    if _sha(successor_raw) != approval_doc['successor_document_sha256']:
        raise ValueError('Successor document differs from independently reviewed bytes')
    approved_pairs = {(row['predecessor'], row['successor'])
                      for row in approval_doc['proposed_decisions']}
    successors = json.loads(successor_raw)['claims']
    observed_pairs = {(claim.get('supersedes_claim_id'), claim.get('claim_id'))
                      for claim in successors}
    if (len(approved_pairs) != 5 or len(successors) != 5 or
            observed_pairs != approved_pairs or
            len({new for _, new in observed_pairs}) != 5 or
            len({old for old, _ in observed_pairs}) != 5):
        raise ValueError('Successor identities or predecessor relationships differ')

    old = check_inventory(reviews, inputs['artifacts'], inputs['reconciliation'],
                          inputs['baseline'], historical=inputs['historical'],
                          provenance=inputs['provenance'], preserved_membership=True)
    new = check_inventory(reviews, inputs['artifacts'], inputs['reconciliation'], inputs['current'])
    old_ids = {cid for family in old['families'] for cid in family['claim_ids']}
    new_ids = {cid for family in new['families'] for cid in family['claim_ids']}
    added_ids = {new_id for _, new_id in approved_pairs}
    if (new_ids - old_ids != added_ids or old_ids - new_ids or
            not {old_id for old_id, _ in approved_pairs}.issubset(old_ids)):
        raise ValueError('Migration changes claims beyond the five approved successors')
    new_documents = {item['path']: item for item in new['inputs']['claim_documents']}
    if any(digest(new_documents.get(item['path'])) != digest(item)
           for item in old['inputs']['claim_documents']):
        raise ValueError('Historical document changed across workload reproductions')
    if (new['inputs']['artifacts_sha256'] != old['inputs']['artifacts_sha256'] or
            new['inputs']['reconciliation_sha256'] != old['inputs']['reconciliation_sha256']):
        raise ValueError('Migration changed artifact or reconciliation input')
    projected_families = []
    for family in new['families']:
        members = [cid for cid in family['claim_ids'] if cid not in added_ids]
        if members:
            projected_families.append({**family, 'claim_ids': members})
    if digest(projected_families) != digest(old['families']):
        raise ValueError('Migration changes preserved family or reconciliation membership')
    if (sorted(reviews.glob('*-claims.json')) != paths or
            _fingerprints(list(before)) != before):
        raise ValueError('Workload migration inputs changed during combined check')
    return {
        'schema': 'ges.claim-workload-migration-check.v1', 'status': 'MATCH',
        'baseline_recorded_claims': old['counts']['recorded_claims'],
        'current_recorded_claims': new['counts']['recorded_claims'],
        'baseline_claim_documents': old['counts']['claim_documents'],
        'current_claim_documents': new['counts']['claim_documents'],
        'added_claims': len(added_ids), 'added_claim_ids': sorted(added_ids),
        'families': len(new['families']),
        'reconciliation_records_present': new['counts']['reconciliation_records_present'],
        'recorded_claims_without_reconciliation': new['counts']['recorded_claims_without_reconciliation'],
        'new_review_credit': 0, 'new_reconciliation_credit': 0,
        'input_sha256': {key: _sha(value) for key, value in raw.items()},
        'scope': 'Metadata workload reproduction; not authenticated source replay or disposition validation.',
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('reviews', 'artifacts', 'reconciliation', 'baseline', 'current',
                 'historical', 'provenance', 'approval'):
        parser.add_argument('--' + name, type=Path, required=True)
    args = parser.parse_args()
    try:
        result = check_migration(**vars(args))
    except (OSError, EOFError, ValueError, KeyError, TypeError) as exc:
        parser.exit(1, 'Workload migration failed: ' + str(exc) + '\n')
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
