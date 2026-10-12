"""Compare supplied receipt envelopes to a hash-pinned nonissued decision draft.

This read-only comparison neither issues receipts nor authenticates authority.
Full source-bound claim_reconciliation accounting remains separately required.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from .claim_reconciliation import (RECEIPT_FIELDS, SUBJECT_FIELDS, _require,
                                   _sha, _text, _time, _validate_policy)
from .core import digest, now

ENVELOPE_FIELDS = {'schema', 'reconciler', 'independent_reviewer',
                   'reconciled_at', 'reviewed_at'}
ROLE_TIME_FIELDS = ENVELOPE_FIELDS - {'schema'}
BINDINGS = ('claim_input_digest', 'catalog_digest', 'proposal_digest')


def compare_envelopes(draft_bytes: bytes, expected_sha256: str,
                      receipts: list[dict], policy: dict) -> dict:
    """Prove decision equality under supplied policy, without reconciliation credit."""
    _require(_sha(expected_sha256) and
             hashlib.sha256(draft_bytes).hexdigest() == expected_sha256,
             'Reviewed draft byte digest mismatch')
    draft = json.loads(draft_bytes)
    _require(isinstance(draft, list) and bool(draft), 'Draft must be a nonempty array')
    indexed = {}
    bindings = None
    for row in draft:
        _require(isinstance(row, dict) and set(row) == RECEIPT_FIELDS and
                 row['schema'] == 'ges.claim-reconciliation-receipt.draft.v1',
                 'Malformed or issued draft')
        _require(all(row[key] is None for key in ROLE_TIME_FIELDS),
                 'Draft role and time fields must remain null')
        subject = row['claim']
        _require(isinstance(subject, dict) and set(subject) == set(SUBJECT_FIELDS),
                 'Malformed draft subject')
        cid = subject['claim_id']
        _require(_text(cid) and cid not in indexed, 'Duplicate or missing draft claim ID')
        current_bindings = tuple(row[key] for key in BINDINGS)
        _require(all(_sha(value) for value in current_bindings), 'Malformed draft bindings')
        if bindings is None:
            bindings = current_bindings
        _require(current_bindings == bindings, 'Inconsistent draft bindings')
        _require(row['accepted_policy'] is False and row['adopted_obligation'] is None,
                 'Draft cannot assert adoption')
        indexed[cid] = row
    policy = _validate_policy(policy, *bindings)
    _require(isinstance(receipts, list) and len(receipts) == len(draft),
             'Receipt membership differs from reviewed draft')
    seen = set()
    current_time = _time(now())
    for receipt in receipts:
        _require(isinstance(receipt, dict) and set(receipt) == RECEIPT_FIELDS and
                 receipt['schema'] == 'ges.claim-reconciliation-receipt.v1',
                 'Malformed or nonissued receipt')
        subject = receipt['claim']
        _require(isinstance(subject, dict) and _text(subject.get('claim_id')),
                 'Malformed receipt subject')
        cid = subject['claim_id']
        _require(cid in indexed and cid not in seen, 'Foreign or duplicate receipt')
        for key in RECEIPT_FIELDS - ENVELOPE_FIELDS:
            _require(digest(receipt[key]) == digest(indexed[cid][key]),
                     'Reviewed decision changed: ' + cid + ':' + key)
        reconciler, reviewer = receipt['reconciler'], receipt['independent_reviewer']
        _require(reconciler in policy['authorized_reconcilers'] and
                 reviewer in policy['authorized_independent_reviewers'] and
                 reconciler != reviewer, 'Unauthorized or nonindependent receipt role')
        _require(_time(receipt['reconciled_at']) <= _time(receipt['reviewed_at']) <= current_time,
                 'Receipt timestamps future or out of order')
        seen.add(cid)
    return {
        'schema': 'ges.reconciliation-envelope-comparison.v1',
        'status': 'MATCH_UNDER_SUPPLIED_POLICY', 'compared_decisions': len(seen),
        'draft_sha256': expected_sha256, 'draft_canonical_digest': digest(draft),
        'receipts_digest': digest(receipts), 'policy_digest': digest(policy),
        **dict(zip(BINDINGS, bindings)),
        'authority_authenticated': False, 'source_provenance_replayed': False,
        'accounting_performed': False,
        'scope': 'Mechanical comparison only. Authenticate the external role grant and '
                 'actual issuance/review evidence, then run full source-bound accounting. '
                 'Matching JSON role strings are not identity or issuance evidence.',
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--draft', type=Path, required=True)
    parser.add_argument('--draft-sha256', required=True)
    parser.add_argument('--receipts', type=Path, required=True)
    parser.add_argument('--policy', type=Path, required=True)
    args = parser.parse_args()
    try:
        report = compare_envelopes(args.draft.read_bytes(), args.draft_sha256,
                                   json.loads(args.receipts.read_bytes()),
                                   json.loads(args.policy.read_bytes()))
    except (ValueError, KeyError, TypeError, OSError, UnicodeError) as exc:
        print(json.dumps({'valid': False, 'error': str(exc)}))
        return 2
    print(json.dumps({'valid': True, **report}))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
