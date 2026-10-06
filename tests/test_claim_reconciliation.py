import copy
import gzip
import hashlib
import json
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from ges.claim_reconciliation import reconciliation_accounting


class ClaimReconciliation(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.sources = self.root / 'sources'
        self.reviews = self.root / 'reviews'
        self.sources.mkdir()
        self.reviews.mkdir()
        self.source = 'owner/repo'
        self.commit = 'a' * 40
        self.source_path = 'guide.md'
        self.content = 'Must alpha.\nShould beta.\n'
        self.content_sha = hashlib.sha256(self.content.encode()).hexdigest()
        self.artifact = {'artifact_id': 'artifact-1', 'source': self.source,
                         'commit': self.commit, 'path': self.source_path,
                         'sha256': self.content_sha}
        self.artifacts = self.root / 'artifacts.jsonl'
        self.artifacts.write_text(json.dumps(self.artifact) + '\n')
        self.source_archive = self.sources / 'owner__repo.text.jsonl.gz'
        with gzip.open(self.source_archive, 'wt') as stream:
            stream.write(json.dumps({**self.artifact, 'content': self.content}) + '\n')
        self.review_doc = {
            'reviewer': 'source-reviewer',
            'reviewed_at': '2026-01-01T00:00:00Z',
            'source': self.source,
            'commit': self.commit,
            'path': self.source_path,
            'content_sha256': self.content_sha,
            'claims': [
                {'claim_id': 'CLAIM-001', 'statement': 'Must alpha.',
                 'start_line': 1, 'end_line': 1,
                 'proposed_control_ids': ['GES-CP-001'],
                 'accepted_policy': False},
                {'claim_id': 'CLAIM-002', 'statement': 'Should beta.',
                 'start_line': 2, 'end_line': 2,
                 'proposed_control_ids': ['GES-CP-002'],
                 'accepted_policy': False},
            ],
        }
        self.review_file = self.reviews / 'claims-claims.json'
        self.write_review()
        self.review_policy = {'authorized_reviewers': ['source-reviewer']}
        self.pins = {self.source: self.commit}
        self.catalog = [{'id': 'GES-CP-001', 'revision': 2}]
        self.proposals = [{'id': 'GES-CP-002', 'revision': 3}]
        empty = self.account(None, None)
        self.policy = {
            'schema': 'ges.claim-reconciliation-policy.v1',
            'approval_reference': 'synthetic approval; not real authority',
            'claim_input_digest': empty['claim_input_digest'],
            'catalog_digest': empty['catalog_digest'],
            'proposal_digest': empty['proposal_digest'],
            'authorized_reconcilers': ['reconciler'],
            'authorized_independent_reviewers': ['auditor'],
        }
        self.receipt = self.make_receipt(0)

    def write_review(self):
        self.review_file.write_text(json.dumps(self.review_doc))

    def subject(self, index):
        claim = self.review_doc['claims'][index]
        return {
            'claim_id': claim['claim_id'],
            'source': self.source,
            'commit': self.commit,
            'path': self.source_path,
            'artifact_id': self.artifact['artifact_id'],
            'content_sha256': self.content_sha,
            'start_line': claim['start_line'],
            'end_line': claim['end_line'],
            'statement_sha256': hashlib.sha256(claim['statement'].encode()).hexdigest(),
            'claim_document': self.review_file.name,
            'claim_document_sha256': hashlib.sha256(
                self.review_file.read_bytes()).hexdigest(),
        }

    def make_receipt(self, index, disposition='MAP'):
        if disposition == 'MAP':
            references = [{'id': 'GES-CP-001' if index == 0 else 'GES-CP-002',
                           'revision': 2 if index == 0 else 3,
                           'collection': 'CATALOG' if index == 0 else 'PROPOSAL'}]
            details = {}
        elif disposition == 'REFERENCE':
            references = []
            details = {'reference_reason': 'Preserved as contextual guidance.'}
        else:
            references = []
            details = {}
        return {
            'schema': 'ges.claim-reconciliation-receipt.v1',
            'claim': self.subject(index),
            'claim_input_digest': self.policy['claim_input_digest'],
            'catalog_digest': self.policy['catalog_digest'],
            'proposal_digest': self.policy['proposal_digest'],
            'disposition': disposition,
            'control_references': references,
            'details': details,
            'rationale': 'Synthetic exact-scope reconciliation for contract testing.',
            'reconciler': 'reconciler',
            'independent_reviewer': 'auditor',
            'reconciled_at': '2026-02-01T00:00:00Z',
            'reviewed_at': '2026-02-02T00:00:00Z',
            'accepted_policy': False,
            'adopted_obligation': None,
        }

    def account(self, receipts=None, policy=None):
        return reconciliation_accounting(
            self.artifacts, self.sources, self.reviews, self.review_policy,
            self.pins, self.catalog, self.proposals, receipts, policy)

    def test_valid_partial_receipt_preserves_denominator_and_boundaries(self):
        result = self.account([self.receipt], self.policy)
        self.assertEqual(result['known_claim_denominator'], 2)
        self.assertEqual(result['validated_count'], 1)
        self.assertEqual(result['unresolved_count'], 1)
        self.assertEqual(result['disposition_counts']['MAP'], 1)
        self.assertFalse(result['mapping_complete'])
        for field in ('semantic_truth_automatically_certified',
                      'source_to_claim_omission_denominator_certified',
                      'rights_cleared', 'policy_adopted'):
            self.assertFalse(result[field])

    def test_valid_full_receipts_are_complete_and_deterministic(self):
        second = self.make_receipt(1, 'REFERENCE')
        first = self.account([second, self.receipt], self.policy)
        again = self.account([second, self.receipt], self.policy)
        self.assertEqual(first, again)
        self.assertEqual(first['validated_count'], 2)
        self.assertEqual(first['unresolved_count'], 0)
        self.assertTrue(first['mapping_complete'])
        self.assertEqual(first['validated_claim_ids'], ['CLAIM-001', 'CLAIM-002'])

    def test_multiple_control_references_are_supported(self):
        self.receipt['disposition'] = 'SPECIALIZE'
        self.receipt['details'] = {
            'scope': 'team services',
            'distinction': 'The proposal records the profile-specific threshold.',
        }
        self.receipt['control_references'].append(
            {'id': 'GES-CP-002', 'revision': 3, 'collection': 'PROPOSAL'})
        result = self.account([self.receipt], self.policy)
        self.assertEqual(result['validated_count'], 1)

    def test_map_rejects_proposal_and_specialize_requires_one(self):
        proposal_map = self.make_receipt(0)
        proposal_map['control_references'] = [
            {'id': 'GES-CP-002', 'revision': 3, 'collection': 'PROPOSAL'}]
        with self.assertRaisesRegex(ValueError, 'canonical catalog'):
            self.account([proposal_map], self.policy)

        specialize = self.make_receipt(0)
        specialize['disposition'] = 'SPECIALIZE'
        specialize['details'] = {'scope': 'team services',
                                 'distinction': 'A narrower local threshold.'}
        with self.assertRaisesRegex(ValueError, 'requires a proposal'):
            self.account([specialize], self.policy)

    def test_empty_receipts_still_validate_a_supplied_policy(self):
        with self.assertRaisesRegex(ValueError, 'authority policy'):
            self.account([], {})

    def test_unknown_ges_cp_identity_is_rejected(self):
        self.receipt['control_references'][0]['id'] = 'GES-CP-999'
        with self.assertRaisesRegex(ValueError, 'Unknown control identity'):
            self.account([self.receipt], self.policy)

    def test_unapproved_or_identical_automated_roles_are_rejected(self):
        self.receipt['independent_reviewer'] = 'automation:heuristic'
        with self.assertRaisesRegex(ValueError, 'Unauthorized'):
            self.account([self.receipt], self.policy)
        self.receipt['independent_reviewer'] = 'reconciler'
        self.policy['authorized_independent_reviewers'] = ['reconciler']
        with self.assertRaisesRegex(ValueError, 'independent'):
            self.account([self.receipt], self.policy)

    def test_substring_schema_or_heuristic_output_is_rejected(self):
        self.receipt['schema'] = 'result: ges.claim-reconciliation-receipt.v1 MAP'
        with self.assertRaisesRegex(ValueError, 'Malformed'):
            self.account([self.receipt], self.policy)
        with self.assertRaisesRegex(ValueError, 'array'):
            self.account({'result': 'MAP CLAIM-001 to GES-CP-001'}, self.policy)

    def test_changed_claim_or_control_revision_is_rejected(self):
        changed = copy.deepcopy(self.receipt)
        changed['claim']['statement_sha256'] = '0' * 64
        with self.assertRaisesRegex(ValueError, 'Known claim changed'):
            self.account([changed], self.policy)
        changed = copy.deepcopy(self.receipt)
        changed['control_references'][0]['revision'] = 1
        with self.assertRaisesRegex(ValueError, 'revision changed'):
            self.account([changed], self.policy)

    def test_duplicate_receipt_and_defer_are_rejected(self):
        with self.assertRaisesRegex(ValueError, 'duplicate'):
            self.account([self.receipt, copy.deepcopy(self.receipt)], self.policy)
        self.receipt['disposition'] = 'DEFER'
        with self.assertRaisesRegex(ValueError, 'Unsupported claim disposition'):
            self.account([self.receipt], self.policy)

    def test_specialization_requires_scope_distinction_and_controls(self):
        receipt = self.make_receipt(0)
        receipt['disposition'] = 'SPECIALIZE'
        receipt['control_references'].append(
            {'id': 'GES-CP-002', 'revision': 3, 'collection': 'PROPOSAL'})
        receipt['details'] = {'scope': 'team services',
                              'distinction': 'Threshold remains profile-specific.'}
        self.assertEqual(self.account([receipt], self.policy)['validated_count'], 1)
        receipt['details'].pop('distinction')
        with self.assertRaisesRegex(ValueError, 'SPECIALIZE'):
            self.account([receipt], self.policy)

    def test_conflict_reference_and_exclusion_invariants(self):
        conflict = self.make_receipt(0)
        conflict['disposition'] = 'CONFLICT'
        conflict['details'] = {'conflicting_claim_ids': ['CLAIM-002'],
                               'resolution': 'Preserve both and document scoped precedence.'}
        self.assertEqual(self.account([conflict], self.policy)['validated_count'], 1)
        conflict['details']['conflicting_claim_ids'] = ['CLAIM-001']
        with self.assertRaisesRegex(ValueError, 'self-referential'):
            self.account([conflict], self.policy)

        reference = self.make_receipt(1, 'REFERENCE')
        reference['control_references'] = [
            {'id': 'GES-CP-002', 'revision': 3, 'collection': 'PROPOSAL'}]
        with self.assertRaisesRegex(ValueError, 'REFERENCE'):
            self.account([reference], self.policy)

        excluded = self.make_receipt(0)
        excluded['disposition'] = 'EXCLUDED_WITH_REASON'
        excluded['control_references'] = []
        excluded['details'] = {'basis': 'DUPLICATE',
                               'exclusion_reason': 'Exact duplicate intent.',
                               'related_claim_ids': ['CLAIM-002']}
        self.assertEqual(self.account([excluded], self.policy)['validated_count'], 1)
        excluded['details']['related_claim_ids'] = []
        with self.assertRaisesRegex(ValueError, 'requires a related claim'):
            self.account([excluded], self.policy)

    def test_policy_and_receipt_must_bind_exact_input_digests(self):
        for target, key in ((self.policy, 'claim_input_digest'),
                            (self.receipt, 'catalog_digest'),
                            (self.receipt, 'proposal_digest')):
            with self.subTest(key=key):
                changed_policy = copy.deepcopy(self.policy)
                changed_receipt = copy.deepcopy(self.receipt)
                if target is self.policy:
                    changed_policy[key] = '0' * 64
                else:
                    changed_receipt[key] = '0' * 64
                with self.assertRaisesRegex(ValueError, 'exact reconciliation inputs'):
                    self.account([changed_receipt], changed_policy)

    def test_naive_future_and_out_of_order_timestamps_are_rejected(self):
        for key, value in (('reviewed_at', '2026-02-02T00:00:00'),
                           ('reviewed_at', '2999-01-01T00:00:00Z'),
                           ('reconciled_at', '2025-12-31T00:00:00Z')):
            with self.subTest(key=key, value=value):
                receipt = copy.deepcopy(self.receipt)
                receipt[key] = value
                with self.assertRaises(ValueError):
                    self.account([receipt], self.policy)

    def test_unsupported_fields_and_types_are_rejected(self):
        receipt = copy.deepcopy(self.receipt)
        receipt['heuristic_match'] = 'GES-CP-001'
        with self.assertRaisesRegex(ValueError, 'unsupported'):
            self.account([receipt], self.policy)
        receipt = copy.deepcopy(self.receipt)
        receipt['control_references'] = 'GES-CP-001'
        with self.assertRaisesRegex(ValueError, 'array'):
            self.account([receipt], self.policy)
        policy = copy.deepcopy(self.policy)
        policy['unsupported_grant'] = True
        with self.assertRaisesRegex(ValueError, 'unsupported'):
            self.account([self.receipt], policy)

    def test_reconciliation_cannot_assert_adoption(self):
        for key, value in (('accepted_policy', True),
                           ('adopted_obligation', 'MUST')):
            with self.subTest(key=key):
                receipt = copy.deepcopy(self.receipt)
                receipt[key] = value
                with self.assertRaisesRegex(ValueError, 'policy adoption'):
                    self.account([receipt], self.policy)

    def test_source_claim_provenance_is_validated_before_accounting(self):
        with gzip.open(self.source_archive, 'wt') as stream:
            stream.write(json.dumps({**self.artifact, 'content': 'Changed.\n'}) + '\n')
        with self.assertRaisesRegex(ValueError, 'Pinned text differs'):
            self.account([], {})

    def test_cli_returns_exit_two_for_invalid_receipt(self):
        paths = {}
        values = {
            'review-policy': self.review_policy,
            'receipts': [{**self.receipt, 'disposition': 'DEFER'}],
            'policy': self.policy,
            'pins': {'sources': [{'repository': self.source, 'commit': self.commit}]},
            'catalog': self.catalog,
            'proposals': self.proposals,
        }
        for name, value in values.items():
            path = self.root / (name + '.json')
            path.write_text(json.dumps(value))
            paths[name] = path
        base_command = [sys.executable, '-m', 'ges.claim_reconciliation',
                        '--artifacts', str(self.artifacts), '--sources', str(self.sources),
                        '--reviews', str(self.reviews),
                        '--review-policy', str(paths['review-policy']),
                        '--pins', str(paths['pins']), '--catalog', str(paths['catalog']),
                        '--proposals', str(paths['proposals'])]
        command = [*base_command, '--receipts', str(paths['receipts']),
                   '--policy', str(paths['policy'])]
        completed = subprocess.run(command, cwd=Path(__file__).resolve().parents[1],
                                   capture_output=True, text=True, check=False)
        self.assertEqual(completed.returncode, 2)

        accounting = subprocess.run(
            base_command, cwd=Path(__file__).resolve().parents[1],
            capture_output=True, text=True, check=False)
        self.assertEqual(accounting.returncode, 0)
        self.assertEqual(json.loads(accounting.stdout)['validated_count'], 0)
        self.assertFalse(json.loads(completed.stdout)['valid'])


if __name__ == '__main__':
    unittest.main()
