import copy
import hashlib
import json
import unittest

from ges import reconciliation_envelopes
from ges.claim_reconciliation import SUBJECT_FIELDS


class EnvelopeComparison(unittest.TestCase):
    def setUp(self):
        self.row = {
            'schema': 'ges.claim-reconciliation-receipt.draft.v1',
            'claim': {key: key for key in SUBJECT_FIELDS},
            'claim_input_digest': 'a' * 64, 'catalog_digest': 'b' * 64,
            'proposal_digest': 'c' * 64, 'disposition': 'REFERENCE',
            'control_references': [], 'details': {'reference_reason': 'Context'},
            'rationale': 'Retain context', 'reconciler': None,
            'independent_reviewer': None, 'reconciled_at': None,
            'reviewed_at': None, 'accepted_policy': False, 'adopted_obligation': None,
        }
        self.raw = (json.dumps([self.row]) + '\n').encode()
        self.sha = hashlib.sha256(self.raw).hexdigest()
        self.receipt = {**copy.deepcopy(self.row),
            'schema': 'ges.claim-reconciliation-receipt.v1',
            'reconciler': 'actual-reconciler', 'independent_reviewer': 'actual-reviewer',
            'reconciled_at': '2026-01-02T00:00:00Z', 'reviewed_at': '2026-01-03T00:00:00Z'}
        self.policy = {'schema': 'ges.claim-reconciliation-policy.v1',
            'approval_reference': 'SYNTHETIC TEST ONLY',
            **{key: self.row[key] for key in ('claim_input_digest', 'catalog_digest', 'proposal_digest')},
            'authorized_reconcilers': ['actual-reconciler'],
            'authorized_independent_reviewers': ['actual-reviewer']}

    def compare(self, receipts=None):
        return reconciliation_envelopes.compare_envelopes(
            self.raw, self.sha, [self.receipt] if receipts is None else receipts, self.policy)

    def test_comparison_does_not_claim_authorization_or_accounting(self):
        result = self.compare()
        self.assertEqual(result['compared_decisions'], 1)
        self.assertFalse(result['authority_authenticated'])
        self.assertFalse(result['source_provenance_replayed'])
        self.assertFalse(result['accounting_performed'])
        self.assertNotIn('validated_count', result)

    def test_every_substantive_field_is_preserved(self):
        for key in set(self.row) - reconciliation_envelopes.ENVELOPE_FIELDS:
            with self.subTest(key=key):
                original = copy.deepcopy(self.receipt)
                self.receipt[key] = 'changed'
                with self.assertRaises(ValueError):
                    self.compare()
                self.receipt = original

    def test_rejects_missing_extra_duplicate_and_nonissued_receipts(self):
        for rows in ([], [self.receipt, self.receipt], [self.row]):
            with self.subTest(rows=len(rows)), self.assertRaises(ValueError):
                self.compare(rows)

    def test_rejects_wrong_draft_digest_or_nonnull_draft_roles(self):
        self.sha = '0' * 64
        with self.assertRaises(ValueError):
            self.compare()
        self.row['reconciler'] = 'invented'
        self.raw = json.dumps([self.row]).encode()
        self.sha = hashlib.sha256(self.raw).hexdigest()
        with self.assertRaises(ValueError):
            self.compare()

    def test_rejects_unauthorized_same_actor_and_invalid_times(self):
        for changes in ({'reconciler': 'other'},
                        {'independent_reviewer': 'actual-reconciler'},
                        {'reconciled_at': '2026-01-04T00:00:00Z'},
                        {'reviewed_at': '2099-01-01T00:00:00Z'},
                        {'reviewed_at': '2026-01-03T00:00:00'}):
            original = copy.deepcopy(self.receipt)
            self.receipt.update(changes)
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                self.compare()
            self.receipt = original

    def test_rejects_same_actor_even_when_both_roles_authorize_it(self):
        self.policy['authorized_independent_reviewers'].append('actual-reconciler')
        self.receipt['independent_reviewer'] = 'actual-reconciler'
        with self.assertRaises(ValueError):
            self.compare()

    def test_rejects_wrong_policy_binding(self):
        self.policy['claim_input_digest'] = 'd' * 64
        with self.assertRaises(ValueError):
            self.compare()
