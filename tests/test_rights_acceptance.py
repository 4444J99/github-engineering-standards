import copy
import hashlib
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from ges.core import digest
from ges.rights_acceptance import rights_accounting
from ges.recovery import evaluate_gate, status


class RightsAcceptance(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'evidence').mkdir()
        self.artifact = {'artifact_id': 'one', 'source': 'owner/repo',
                         'commit': 'a' * 40, 'path': 'README.md',
                         'sha256': 'b' * 64, 'url': 'reference',
                         'retrieved_at': '2026-01-01T00:00:00Z'}
        self.artifacts = [self.artifact]
        self.pins = {'owner/repo': 'a' * 40}
        self.policy = {'schema': 'ges.rights-authority-policy.v1',
                       'approval_reference': 'Synthetic externally approved fixture',
                       'inventory_digest': digest(self.artifacts),
                       'intended_use': 'REFERENCES_ONLY',
                       'distribution_scope': 'Synthetic private reference bundle v1',
                       'authorized_reviewers': ['reviewer'],
                       'authorized_auditors': ['auditor'],
                       'authorized_human_acceptors': ['human'],
                       'authorized_distribution_approvers': ['publisher']}
        self.receipt = {'schema': 'ges.rights-acceptance-receipt.v1',
                        'artifact': {k: self.artifact[k] for k in
                                     ('artifact_id', 'source', 'commit', 'path', 'sha256')},
                        'inventory_digest': digest(self.artifacts),
                        'findings_digest': digest([]),
                        'intended_use': 'REFERENCES_ONLY',
                        'distribution_scope': 'Synthetic private reference bundle v1',
                        'valid_until': '2030-01-01T00:00:00Z',
                        'obligations': ['Exclude raw source expression', 'Preserve provenance'],
                        'reviewer': 'reviewer', 'independent_auditor': 'auditor',
                        'human_acceptor': 'human', 'distribution_approver': 'publisher',
                        'evidence': {}}
        for kind, identity in [('file_rights_review', 'reviewer'),
                               ('independent_exception_audit', 'auditor'),
                               ('human_acceptance', 'human'),
                               ('distribution_approval', 'publisher')]:
            doc = {'schema': 'ges.rights-attestation.v1', 'kind': kind,
                   'identity': identity, 'reviewed_at': '2026-01-02T00:00:00Z',
                   'subject': {k: copy.deepcopy(self.receipt[k]) for k in
                               ('artifact', 'inventory_digest', 'findings_digest',
                                'intended_use', 'distribution_scope', 'obligations', 'valid_until')},
                   'decision': 'APPROVED_FOR_SPECIFIED_USE',
                   'file_specific_grant_and_components_reviewed': True,
                   'exceptions_and_restrictions_accounted_for': True,
                   'rationale': 'Synthetic fixture only, not a real rights decision'}
            self.write(kind, doc)

    def write(self, kind, doc):
        path = self.root / 'evidence' / (kind + '.json')
        path.write_text(json.dumps(doc))
        self.receipt['evidence'][kind] = {
            'path': 'evidence/' + path.name,
            'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}

    def run_accounting(self, receipts=None, policy=None):
        return rights_accounting(self.artifacts, self.pins, [],
                                 [self.receipt] if receipts is None else receipts,
                                 self.policy if policy is None else policy,
                                 evidence_root=self.root)

    def test_no_receipts_remains_unknown(self):
        result = self.run_accounting([], {})
        self.assertEqual(result['completed'], 0)
        self.assertIsNone(result['per_file_rights_acceptance'])
        self.assertIsNone(result['authorized_distribution_decision'])

    def test_synthetic_approved_scope_counts_not_legal_truth(self):
        result = self.run_accounting()
        self.assertEqual(result['completed'], 1)
        self.assertTrue(result['per_file_rights_acceptance'])
        self.assertTrue(result['authorized_distribution_decision'])
        self.assertFalse(result['legal_truth_automatically_certified'])
        self.assertFalse(result['publication_performed'])

    def test_partial_keeps_full_inventory(self):
        self.artifacts.append({**self.artifact, 'artifact_id': 'two', 'path': 'other.md'})
        self.receipt['inventory_digest'] = digest(self.artifacts)
        self.policy['inventory_digest'] = digest(self.artifacts)
        for kind, ref in list(self.receipt['evidence'].items()):
            doc = json.loads((self.root / ref['path']).read_text())
            doc['subject']['inventory_digest'] = self.receipt['inventory_digest']
            self.write(kind, doc)
        result = self.run_accounting()
        self.assertEqual((result['completed'], result['denominator']), (1, 2))
        self.assertFalse(result['per_file_rights_acceptance'])
        self.assertFalse(result['authorized_distribution_decision'])

    def test_no_policy_rejected(self):
        with self.assertRaises(ValueError):
            self.run_accounting(policy={})

    def test_triage_record_not_acceptance(self):
        with self.assertRaises(ValueError):
            self.run_accounting([{'status': 'PENDING_RIGHTS_ACCEPTANCE'}])

    def test_duplicate_receipt_rejected(self):
        with self.assertRaises(ValueError):
            self.run_accounting([self.receipt, self.receipt])

    def test_changed_artifact_rejected(self):
        self.receipt['artifact']['sha256'] = 'c' * 64
        with self.assertRaises(ValueError):
            self.run_accounting()

    def test_changed_inventory_rejected(self):
        self.receipt['inventory_digest'] = 'c' * 64
        with self.assertRaises(ValueError):
            self.run_accounting()

    def test_unauthorized_human_rejected(self):
        self.receipt['human_acceptor'] = 'agent'
        with self.assertRaises(ValueError):
            self.run_accounting()

    def test_self_audit_rejected(self):
        self.policy['authorized_auditors'].append('reviewer')
        self.receipt['independent_auditor'] = 'reviewer'
        with self.assertRaises(ValueError):
            self.run_accounting()

    def test_missing_evidence_rejected(self):
        self.receipt['evidence'].pop('human_acceptance')
        with self.assertRaises(ValueError):
            self.run_accounting()

    def test_changed_evidence_rejected(self):
        (self.root / self.receipt['evidence']['file_rights_review']['path']).write_text('{}')
        with self.assertRaises(ValueError):
            self.run_accounting()

    def test_future_or_preacquisition_evidence_rejected(self):
        kind = 'human_acceptance'
        for value in ['2999-01-01T00:00:00Z', '2025-01-01T00:00:00Z']:
            doc = json.loads((self.root / self.receipt['evidence'][kind]['path']).read_text())
            doc['reviewed_at'] = value
            self.write(kind, doc)
            with self.assertRaises(ValueError):
                self.run_accounting()

    def test_wrong_use_or_obligations_rejected(self):
        self.receipt['intended_use'] = 'LICENSED_COPY'
        with self.assertRaises(ValueError):
            self.run_accounting()

    def test_unresolved_exception_rejected(self):
        kind = 'independent_exception_audit'
        doc = json.loads((self.root / self.receipt['evidence'][kind]['path']).read_text())
        doc['exceptions_and_restrictions_accounted_for'] = False
        self.write(kind, doc)
        with self.assertRaises(ValueError):
            self.run_accounting()

    def test_path_escape_or_symlink_rejected(self):
        ref = self.receipt['evidence']['human_acceptance']
        ref['path'] = '../outside.json'
        with self.assertRaises(ValueError):
            self.run_accounting()
        ref['path'] = 'evidence/human_acceptance.json'
        target = self.root / ref['path']
        original = target.read_bytes()
        target.unlink()
        other = self.root / 'other.json'
        other.write_bytes(original)
        target.symlink_to(other)
        with self.assertRaises(ValueError):
            self.run_accounting()

    def test_wrong_pin_rejected_even_without_receipts(self):
        self.pins.clear()
        with self.assertRaises(ValueError):
            self.run_accounting([], {})

    def test_stale_findings_digest_rejected(self):
        self.receipt['findings_digest'] = 'c' * 64
        with self.assertRaises(ValueError):
            self.run_accounting()

    def test_approved_policy_cannot_change_project_target(self):
        for field, value in [('inventory_digest', 'c' * 64),
                             ('intended_use', 'LICENSED_COPY'),
                             ('distribution_scope', 'Different public release')]:
            with self.subTest(field=field):
                policy = {**self.policy, field: value}
                with self.assertRaises(ValueError):
                    self.run_accounting(policy=policy)

    def test_expired_or_unbound_validity_rejected(self):
        for value in [None, '2026-01-01T00:00:00Z', '2031-01-01T00:00:00Z']:
            with self.subTest(value=value):
                self.receipt['valid_until'] = value
                with self.assertRaises(ValueError):
                    self.run_accounting()

    def test_nonboolean_attestation_flags_rejected(self):
        kind = 'independent_exception_audit'
        original = json.loads((self.root / self.receipt['evidence'][kind]['path']).read_text())
        for value in [1, 'true', None]:
            doc = {**original, 'exceptions_and_restrictions_accounted_for': value}
            self.write(kind, doc)
            with self.assertRaises(ValueError):
                self.run_accounting()

    def test_naive_timestamp_and_decision_order_rejected(self):
        kind = 'human_acceptance'
        original = json.loads((self.root / self.receipt['evidence'][kind]['path']).read_text())
        for value in ['2026-01-02T00:00:00', '2026-01-01T12:00:00Z']:
            self.write(kind, {**original, 'reviewed_at': value})
            with self.assertRaises(ValueError):
                self.run_accounting()

    def test_changed_distribution_or_obligations_rejected(self):
        self.receipt['obligations'] = ['Different obligations']
        with self.assertRaises(ValueError):
            self.run_accounting()

    def test_duplicate_inventory_and_preapproved_finding_rejected(self):
        with self.assertRaises(ValueError):
            rights_accounting(self.artifacts * 2, self.pins, [], [], {}, evidence_root=self.root)
        finding = {k: self.artifact[k] for k in ('source', 'commit', 'path')}
        finding.update(content_sha256=self.artifact['sha256'], redistribution_approved=True)
        with self.assertRaises(ValueError):
            rights_accounting(self.artifacts, self.pins, [finding], [], {}, evidence_root=self.root)

    def test_untyped_policy_and_findings_rejected(self):
        for field, value in [('intended_use', []), ('authorized_human_acceptors', 'human'),
                             ('authorized_reviewers', [None])]:
            with self.assertRaises(ValueError):
                self.run_accounting(policy={**self.policy, field: value})
        with self.assertRaises(ValueError):
            rights_accounting(self.artifacts, self.pins, [None], [], {}, evidence_root=self.root)

    def test_recovery_requires_paired_inputs_before_acquisition(self):
        for kwargs in [
                {'reviews': Path('unused')},
                {'review_policy': Path('unused')},
                {'published_assurance': Path('unused')},
                {'published_assurance_policy': Path('unused')},
                {'rights_acceptance': Path('unused')},
                {'rights_acceptance_policy': Path('unused')},
                {'source_fidelity': Path('unused')},
                {'source_fidelity_policy': Path('unused')},
                {'claim_reconciliation': Path('unused')},
                {'claim_reconciliation_policy': Path('unused')}]:
            with self.assertRaisesRegex(ValueError, 'both receipts and authority policy'):
                status(Path('absent'), Path('absent'), **kwargs)

        with self.assertRaisesRegex(ValueError, 'requires source reviews'):
            status(Path('absent'), Path('absent'),
                   source_fidelity=Path('unused'),
                   source_fidelity_policy=Path('unused'))

    def test_synthetic_rights_gate_closes_only_complete_scoped_attestations(self):
        result = self.run_accounting()
        gate = evaluate_gate('rights_and_publication', result['completed'], result['denominator'],
                             'Synthetic scoped receipt test',
                             {k: result[k] for k in ('per_file_rights_acceptance',
                                                    'authorized_distribution_decision')})
        self.assertEqual(gate['status'], 'CLOSED')
        result = self.run_accounting([], {})
        gate = evaluate_gate('rights_and_publication', result['completed'], result['denominator'],
                             'No real approval',
                             {k: result[k] for k in ('per_file_rights_acceptance',
                                                    'authorized_distribution_decision')})
        self.assertEqual(gate['status'], 'OPEN')

    def test_replacement_before_final_reread_rejected(self):
        from ges.rights_acceptance import _evidence
        calls = []

        def replace_after_initial_validation(root, reference):
            doc = _evidence(root, reference)
            calls.append(reference)
            if len(calls) == 4:
                (root / calls[0]['path']).write_text('{}')
            return doc

        with patch('ges.rights_acceptance._evidence', side_effect=replace_after_initial_validation):
            with self.assertRaises(ValueError):
                self.run_accounting()
