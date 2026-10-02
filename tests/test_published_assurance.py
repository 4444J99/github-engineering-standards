import copy
import hashlib
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from ges.core import digest
from ges.pages import acquire
from ges.published_assurance import assurance_accounting
from ges.published_claim_review import validate_published_claims
from ges.recovery import status


class PublishedAssurance(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.evidence = self.root / 'evidence'
        self.evidence.mkdir()
        self.ledger = self.root / 'ledger.json'
        self.cache = self.root / 'cache'
        self.page = {'version': 'free-pro-team@latest', 'path': '/en/test',
                     'page_id': digest(['free-pro-team@latest', '/en/test'])[:24],
                     'source_matches': ['artifact']}
        self.ledger.write_text(json.dumps([self.page]))
        self.ledger_sha = hashlib.sha256(self.ledger.read_bytes()).hexdigest()
        acquire(self.ledger, self.cache, fetcher=lambda *_: b'# Test\nContent\n')
        self.row = json.loads((self.cache / 'index.jsonl').read_text())
        self.artifact = {'artifact_id': 'artifact', 'source': 'github/docs',
                         'commit': 'a' * 40, 'path': 'content/test.md',
                         'sha256': 'b' * 64}
        self.artifacts = self.root / 'artifacts.jsonl'
        self.artifacts.write_text(json.dumps(self.artifact) + '\n')
        self.pins = {'github/docs': 'a' * 40}
        self.policy = {'schema': 'ges.published-assurance-policy.v1',
                       'approval_reference': 'synthetic approval, not real authority',
                       'authorized_claim_authors': ['author'],
                       'authorized_certifiers': ['reviewer'],
                       'authorized_omission_auditors': ['auditor']}
        self.receipt = {'schema': 'ges.published-assurance-receipt.v1',
                        **{k: self.page[k] for k in ('page_id', 'path', 'version')},
                        'ledger_sha256': self.ledger_sha,
                        'body_sha256': self.row['sha256'],
                        'source_identity': self.artifact,
                        'claim_author': 'author', 'reviewer': 'reviewer',
                        'independent_auditor': 'auditor',
                        'reviewed_at': '2026-01-02T00:00:00Z',
                        'claims': [],
                        'evidence': {}}
        # Fixed historical acquisition/review times avoid microsecond ordering.
        self.row['retrieved_at'] = '2026-01-01T00:00:00Z'
        (self.cache / 'index.jsonl').write_text(json.dumps(self.row) + '\n')
        for kind in ('source_identity', 'version_rendering', 'dependency_resolution',
                     'claim_mapping', 'independent_omission_audit'):
            doc = {'schema': 'ges.published-assurance-evidence.v1', 'kind': kind,
                   'page_id': self.page['page_id'], 'ledger_sha256': self.ledger_sha,
                   'body_sha256': self.row['sha256'], 'source_identity': self.artifact,
                   'reviewer': 'auditor' if kind == 'independent_omission_audit' else 'reviewer',
                   'reviewed_at': '2026-01-01T12:00:00Z', 'outcome': 'PASS',
                   'method': 'Synthetic scoped manual review',
                   'observations': ['Synthetic positive evidence'], 'unresolved': []}
            path = self.evidence / (kind + '.json')
            path.write_text(json.dumps(doc))
            self.receipt['evidence'][kind] = {
                'path': 'evidence/' + path.name,
                'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
        self.claim_doc = {'schema': 'ges.published-reference-claims.v1',
                          'reviewer': 'author', 'reviewed_at': '2026-01-01T12:00:00Z',
                          'ledger_sha256': self.ledger_sha, 'disposition': 'REFERENCE_ONLY',
                          'instances': [{k: self.receipt[k] for k in
                                         ('page_id', 'path', 'version', 'body_sha256')}],
                          'spans': {'body': {'lines': [1, 2],
                                             'sha256': hashlib.sha256(b'# Test\nContent').hexdigest()}},
                          'claims': [{'id': 'claim1', 'span': 'body',
                                      'statement': 'Synthetic source reference.'}],
                          'page_instance_denominator': 1, 'claim_statements': 1}
        for flag in ('accepted_policy', 'rights_accepted', 'source_revision_verified',
                     'native_behavior_verified', 'independent_omission_audit_passed',
                     'automated_provenance_validation_passed'):
            self.claim_doc[flag] = False
        self.write_claim_doc()

    def write_claim_doc(self):
        path = self.evidence / 'claims.json'
        path.write_text(json.dumps(self.claim_doc))
        self.receipt['claims'] = [{'path': 'evidence/claims.json',
                                  'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}]
        for kind in self.receipt['evidence']:
            self.mutate_evidence(kind, {'claims': self.receipt['claims']})

    def account(self, receipts=None, policy=None):
        return assurance_accounting(self.ledger, self.cache, self.artifacts,
                                    [self.receipt] if receipts is None else receipts,
                                    self.policy if policy is None else policy,
                                    self.pins, evidence_root=self.root)

    def mutate_evidence(self, kind, changes):
        path = self.root / self.receipt['evidence'][kind]['path']
        doc = json.loads(path.read_text())
        doc.update(changes)
        path.write_text(json.dumps(doc))
        self.receipt['evidence'][kind]['sha256'] = hashlib.sha256(path.read_bytes()).hexdigest()

    def test_complete_scoped_receipt_counts_not_runtime_or_rights(self):
        result = self.account()
        self.assertEqual(result['completed'], 1)
        self.assertEqual(result['denominator'], 1)
        self.assertTrue(result['version_include_and_render_assurance'])
        self.assertFalse(result['rights_cleared'])
        self.assertFalse(result['native_behavior_verified'])

    def test_missing_inputs_remain_unknown_not_pass(self):
        result = self.account(receipts=[], policy={})
        self.assertEqual(result['completed'], 0)
        self.assertIsNone(result['version_include_and_render_assurance'])

    def test_source_disposition_policy_has_no_certification_authority(self):
        with self.assertRaises(ValueError):
            self.account(policy={'authorized_reviewers': ['reviewer']})

    def test_unknown_policy_role_never_counts(self):
        for key in ('claim_author', 'reviewer', 'independent_auditor'):
            with self.subTest(key=key), self.assertRaises(ValueError):
                receipt = copy.deepcopy(self.receipt)
                receipt[key] = 'intruder'
                self.account([receipt])

    def test_self_audit_is_rejected_even_if_both_roles_authorized(self):
        self.policy['authorized_omission_auditors'] = ['reviewer']
        self.receipt['independent_auditor'] = 'reviewer'
        with self.assertRaises(ValueError):
            self.account()

    def test_duplicate_or_unknown_page_rejected(self):
        with self.assertRaises(ValueError):
            self.account([self.receipt, self.receipt])
        self.receipt['page_id'] = 'unknown'
        with self.assertRaises(ValueError):
            self.account()

    def test_wrong_ledger_body_or_route_identity_rejected(self):
        for key in ('ledger_sha256', 'body_sha256', 'path', 'version'):
            with self.subTest(key=key), self.assertRaises(ValueError):
                receipt = copy.deepcopy(self.receipt)
                receipt[key] = 'wrong'
                self.account([receipt])

    def test_nonempty_source_match_is_not_source_identity_proof(self):
        for key in ('source', 'commit', 'path', 'sha256', 'artifact_id'):
            with self.subTest(key=key), self.assertRaises(ValueError):
                receipt = copy.deepcopy(self.receipt)
                receipt['source_identity'][key] = 'wrong'
                self.account([receipt])

    def test_unmatched_page_cannot_inherit_basename_mapping(self):
        self.page['source_matches'] = []
        self.ledger.write_text(json.dumps([self.page]))
        with self.assertRaises(ValueError):
            self.account()

    def test_future_or_preacquisition_review_rejected(self):
        for time in ('2999-01-01T00:00:00Z', '2025-12-31T00:00:00Z', '2026-01-02T00:00:00'):
            with self.subTest(time=time), self.assertRaises(ValueError):
                self.receipt['reviewed_at'] = time
                self.account()

    def test_missing_evidence_or_unresolved_observations_rejected(self):
        self.mutate_evidence('dependency_resolution', {'unresolved': ['missing include']})
        with self.assertRaises(ValueError):
            self.account()
        self.receipt['evidence'].pop('dependency_resolution')
        with self.assertRaises(ValueError):
            self.account()

    def test_false_or_string_true_cannot_replace_pass_evidence(self):
        for outcome in (False, True, 'true', 'UNVERIFIED'):
            with self.subTest(outcome=outcome), self.assertRaises(ValueError):
                self.mutate_evidence('version_rendering', {'outcome': outcome})
                self.account()

    def test_digest_tampering_rejected(self):
        path = self.root / self.receipt['evidence']['claim_mapping']['path']
        path.write_text('{}')
        with self.assertRaises(ValueError):
            self.account()

    def test_claim_documents_required_and_provenance_validated(self):
        self.receipt['claims'] = []
        with self.assertRaises(ValueError):
            self.account()
        self.claim_doc['spans']['body']['sha256'] = '0' * 64
        self.write_claim_doc()
        with self.assertRaises(ValueError):
            self.account()

    def test_foreign_claim_author_cannot_support_receipt(self):
        self.claim_doc['reviewer'] = 'different-author'
        self.write_claim_doc()
        with self.assertRaises(ValueError):
            self.account()

    def test_claim_replacement_between_digest_and_provenance_reads_rejected(self):
        def replaced(*args):
            path = self.evidence / 'claims.json'
            doc = json.loads(path.read_text())
            doc['claims'][0]['statement'] = 'Different unaudited statement.'
            path.write_text(json.dumps(doc))
            return validate_published_claims(*args)

        with patch('ges.published_assurance.validate_published_claims', side_effect=replaced):
            with self.assertRaises(ValueError):
                self.account()

    def test_evidence_target_or_kind_mismatch_rejected(self):
        path = self.root / self.receipt['evidence']['claim_mapping']['path']
        original = json.loads(path.read_text())
        for key in ('page_id', 'ledger_sha256', 'body_sha256', 'kind', 'reviewer'):
            with self.subTest(key=key), self.assertRaises(ValueError):
                self.mutate_evidence('claim_mapping', {**original, key: 'wrong'})
                self.account()

    def test_evidence_path_escape_or_symlink_rejected(self):
        self.receipt['evidence']['claim_mapping']['path'] = '../escape.json'
        with self.assertRaises(ValueError):
            self.account()
        target = self.evidence / 'claim_mapping.json'
        link = self.evidence / 'alias.json'
        link.symlink_to(target)
        self.receipt['evidence']['claim_mapping']['path'] = 'evidence/alias.json'
        with self.assertRaises(ValueError):
            self.account()

    def test_empty_path_parts_rejected_as_value_error(self):
        for path in ('.', './'):
            with self.subTest(path=path), self.assertRaises(ValueError):
                self.receipt['evidence']['claim_mapping']['path'] = path
                self.account()

    def test_audit_bound_to_exact_claim_documents(self):
        self.mutate_evidence('independent_omission_audit', {'claims': []})
        with self.assertRaises(ValueError):
            self.account()

    def recovery_fixture(self):
        sources, corpus = self.root / 'sources', self.root / 'corpus'
        for path in (sources, corpus, self.root / 'controls',
                     self.root / 'templates', self.root / 'profiles'):
            path.mkdir()
        for name in ('catalog', 'review_queue'):
            (self.root / 'controls' / (name + '.json')).write_text('[]')
        (sources / 'sources.lock.json').write_text(json.dumps({'sources': [
            {'repository': 'github/docs', 'commit': 'a' * 40}]}))
        (sources / 'github__docs.inventory.json').write_text(json.dumps([self.artifact]))
        (sources / 'github__docs.tree-reconciliation.json').write_text('{"status":"MATCH"}')
        (corpus / 'artifacts.jsonl').write_bytes(self.artifacts.read_bytes())
        (corpus / 'candidates.jsonl').write_text('')
        (corpus / 'published-page-ledger.json').write_bytes(self.ledger.read_bytes())
        (corpus / 'ledger-summary.json').write_text('{}')
        (corpus / 'structured-source-requirements.json').write_text('[]')
        receipts, policy = self.root / 'receipts.json', self.root / 'policy.json'
        receipts.write_text(json.dumps([self.receipt]))
        policy.write_text(json.dumps(self.policy))
        return sources, corpus, receipts, policy

    def test_recovery_uses_validated_receipts_and_preserves_other_gates(self):
        sources, corpus, receipts, policy = self.recovery_fixture()
        with patch('ges.recovery.ROOT', self.root):
            result = status(sources, corpus, rendered_directory=self.cache,
                            published_assurance=receipts, published_assurance_policy=policy)
        gate = next(g for g in result['gates'] if g['gate'] == 'published_content_assurance')
        self.assertEqual(gate['completed'], 1)
        self.assertEqual(gate['status'], 'CLOSED')
        self.assertFalse(result['project_complete'])
        self.assertEqual(sum(g['status'] == 'OPEN' for g in result['gates']), 8)

    def test_recovery_missing_receipts_keeps_assurance_unknown(self):
        sources, corpus, _, _ = self.recovery_fixture()
        with patch('ges.recovery.ROOT', self.root):
            result = status(sources, corpus, rendered_directory=self.cache)
        gate = next(g for g in result['gates'] if g['gate'] == 'published_content_assurance')
        self.assertEqual(gate['completed'], 0)
        self.assertEqual(gate['status'], 'OPEN')
        self.assertIsNone(gate['conditions']['version_include_and_render_assurance'])

    def test_recovery_one_sided_authority_input_rejected(self):
        sources, corpus, receipts, _ = self.recovery_fixture()
        with patch('ges.recovery.ROOT', self.root), self.assertRaises(ValueError):
            status(sources, corpus, rendered_directory=self.cache,
                   published_assurance=receipts)

    def test_partial_receipts_preserve_complete_ledger_denominator(self):
        other = dict(self.page, path='/en/other')
        other['page_id'] = digest([other['version'], other['path']])[:24]
        self.ledger.write_text(json.dumps([self.page, other]))
        ledger_sha = hashlib.sha256(self.ledger.read_bytes()).hexdigest()
        self.row['ledger_sha256'] = ledger_sha
        (self.cache / 'index.jsonl').write_text(json.dumps(self.row) + '\n')
        self.receipt['ledger_sha256'] = ledger_sha
        self.claim_doc['ledger_sha256'] = ledger_sha
        self.write_claim_doc()
        for kind in self.receipt['evidence']:
            self.mutate_evidence(kind, {'ledger_sha256': ledger_sha})
        result = self.account()
        self.assertEqual(result['completed'], 1)
        self.assertEqual(result['denominator'], 2)
        self.assertFalse(result['version_include_and_render_assurance'])
