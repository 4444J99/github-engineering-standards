"""Synthetic receipt fixtures, never real authority or source-completion evidence."""
import copy
import gzip
import hashlib
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from ges.core import digest
from ges import structured_reconciliation


class StructuredReconciliation(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.sources = self.root / 'sources'
        self.reviews = self.root / 'reviews'
        self.sources.mkdir()
        self.reviews.mkdir()
        self.source = 'github/github-well-architected'
        self.pin = 'a' * 40
        self.path = 'content/library/test/checklist.md'
        self.content = '- Alpha\n- Beta\n'
        self.sha = hashlib.sha256(self.content.encode()).hexdigest()
        self.artifact = dict(artifact_id='artifact', source=self.source,
                             commit=self.pin, path=self.path, sha256=self.sha)
        self.artifacts = self.root / 'artifacts.jsonl'
        self.artifacts.write_text(json.dumps(self.artifact) + '\n')
        self.snapshot = self.sources / 'github__github-well-architected.text.jsonl.gz'
        self.write_source()
        with gzip.open(self.sources / 'microsoft__ghqr.text.jsonl.gz', 'wt') as stream:
            stream.write('')
        self.rows = []
        for line, statement in ((1, 'Alpha'), (2, 'Beta')):
            self.rows.append({
                'requirement_id': 'SRC-WA-' + digest([self.path, line, statement])[:16],
                'artifact_id': 'artifact', 'source': self.source, 'commit': self.pin,
                'path': self.path, 'line': line, 'function': '',
                'source_statement': statement, 'review_status': 'UNREVIEWED',
                'adopted_obligation': None, 'canonical_control_ids': [],
                'verification_binding': 'manual_source_disposition', 'license': 'MIT',
                'start_line': line, 'end_line': line, 'content_sha256': self.sha,
                'span_sha256': hashlib.sha256(('- ' + statement).encode()).hexdigest()})
        self.document = dict(
            source=self.source, commit=self.pin, path=self.path,
            content_sha256=self.sha, reviewer='source-reviewer',
            reviewed_at='2026-01-01T00:00:00Z', claims=[
                dict(claim_id='one', start_line=1, end_line=1, statement='Alpha',
                     structured_requirement_ids=[self.rows[0]['requirement_id']],
                     accepted_policy=False),
                dict(claim_id='two', start_line=1, end_line=1, statement='Alpha caveat',
                     structured_requirement_ids=[self.rows[0]['requirement_id']],
                     accepted_policy=False)])
        self.review_file = self.reviews / 'review-claims.json'
        self.review_file.write_text(json.dumps(self.document))
        from ges.claim_reconciliation import reconciliation_accounting
        self.kwargs = dict(requirements=self.rows, artifacts=self.artifacts,
                           sources=self.sources, reviews=self.reviews,
                           review_policy={'authorized_reviewers': ['source-reviewer']},
                           pins={self.source: self.pin, 'microsoft/ghqr': 'b' * 40},
                           catalog=[], proposals=[])
        base = reconciliation_accounting(
            self.artifacts, self.sources, self.reviews, self.kwargs['review_policy'],
            self.kwargs['pins'], [], [], None, None)
        self.claim_policy = {
            'schema': 'ges.claim-reconciliation-policy.v1',
            'approval_reference': 'SYNTHETIC ONLY',
            **{key: base[key] for key in ('claim_input_digest', 'catalog_digest', 'proposal_digest')},
            'authorized_reconcilers': ['reconciler'],
            'authorized_independent_reviewers': ['claim-auditor']}
        self.claim_receipts = []
        for claim in self.document['claims']:
            subject = dict(claim_id=claim['claim_id'], source=self.source,
                           commit=self.pin, path=self.path, artifact_id='artifact',
                           content_sha256=self.sha, start_line=1, end_line=1,
                           statement_sha256=hashlib.sha256(claim['statement'].encode()).hexdigest(),
                           claim_document=self.review_file.name,
                           claim_document_sha256=hashlib.sha256(self.review_file.read_bytes()).hexdigest())
            self.claim_receipts.append({
                'schema': 'ges.claim-reconciliation-receipt.v1', 'claim': subject,
                **{key: base[key] for key in ('claim_input_digest', 'catalog_digest', 'proposal_digest')},
                'disposition': 'REFERENCE', 'control_references': [],
                'details': {'reference_reason': 'Synthetic context'},
                'rationale': 'Synthetic fixture, not a semantic approval',
                'reconciler': 'reconciler', 'independent_reviewer': 'claim-auditor',
                'reconciled_at': '2026-01-02T00:00:00Z',
                'reviewed_at': '2026-01-03T00:00:00Z',
                'accepted_policy': False, 'adopted_obligation': None})

    def write_source(self):
        with gzip.open(self.snapshot, 'wt') as stream:
            stream.write(json.dumps({**self.artifact, 'content': self.content}) + '\n')

    def account(self, receipts=None, policy=None):
        function = getattr(structured_reconciliation, 'reconciliation_accounting', None)
        self.assertTrue(callable(function), 'Missing structured-occurrence reconciliation adapter')
        return function(**self.kwargs, claim_receipts=self.claim_receipts,
                        claim_policy=self.claim_policy, receipts=receipts, policy=policy,
                        evidence_root=self.root)

    def package(self):
        initial = self.account()
        policy = {'schema': 'ges.structured-reconciliation-policy.v1',
                  'approval_reference': 'SYNTHETIC ONLY', 'subject': initial['subject'],
                  'authorized_reviewers': ['occurrence-reviewer'],
                  'authorized_independent_reviewers': ['occurrence-auditor']}
        receipts = []
        for index, row in enumerate(self.rows):
            subject = {'occurrence': row, 'claim_ids': ['one', 'two'] if index == 0 else [],
                       'inputs': initial['subject']}
            receipt = {'schema': 'ges.structured-reconciliation-receipt.v1',
                       'subject': subject,
                       'disposition': 'CLAIMS_RECONCILED' if index == 0 else 'NONOPERATIVE',
                       'rationale': 'Synthetic reviewed mapping or explicit nonoperative reason',
                       'reviewer': 'occurrence-reviewer',
                       'independent_reviewer': 'occurrence-auditor',
                       'reviewed_at': '2026-01-04T00:00:00Z',
                       'audited_at': '2026-01-05T00:00:00Z', 'evidence': {}}
            for kind, identity, stamp in (
                    ('review', 'occurrence-reviewer', receipt['reviewed_at']),
                    ('independent_audit', 'occurrence-auditor', receipt['audited_at'])):
                doc = {'schema': 'ges.structured-reconciliation-evidence.v1',
                       'kind': kind, 'identity': identity, 'subject': subject,
                       'disposition': receipt['disposition'], 'reviewed_at': stamp,
                       'outcome': 'PASS', 'unresolved': [],
                       'observations': ['Synthetic exact occurrence and full associated claim set reviewed']}
                path = self.root / 'evidence' / f'{index}-{kind}.json'
                path.parent.mkdir(exist_ok=True)
                path.write_text(json.dumps(doc))
                receipt['evidence'][kind] = {'path': path.relative_to(self.root).as_posix(),
                                             'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
            receipts.append(receipt)
        return receipts, policy

    def test_missing_evidence_stays_unknown(self):
        result = self.account()
        self.assertEqual(result['denominator'], 2)
        self.assertEqual(result['completed'], 0)
        self.assertIsNone(result['all_structured_occurrences_reconciled'])

    def test_recovery_requires_paired_structured_inputs_before_reading_files(self):
        from ges.recovery import status
        for kwargs in ({'structured_reconciliation': Path('absent')},
                       {'structured_reconciliation_policy': Path('absent')}):
            with self.subTest(kwargs=kwargs), self.assertRaisesRegex(ValueError, 'Structured reconciliation'):
                status(Path('absent'), Path('absent'), **kwargs)

    def test_recovery_requires_claim_receipts_for_structured_certification(self):
        from ges.recovery import status
        with self.assertRaisesRegex(ValueError, 'Structured reconciliation requires'):
            status(Path('absent'), Path('absent'),
                   structured_reconciliation=Path('receipts'),
                   structured_reconciliation_policy=Path('policy'))

    def test_full_and_partial_coverage_retain_the_denominator(self):
        receipts, policy = self.package()
        result = self.account(receipts[:1], policy)
        self.assertEqual((result['completed'], result['denominator']), (1, 2))
        self.assertFalse(result['all_structured_occurrences_reconciled'])
        self.assertTrue(self.account(receipts, policy)['all_structured_occurrences_reconciled'])
        self.assertFalse(self.account([], policy)['all_structured_occurrences_reconciled'])

    def test_omitting_one_associated_claim_cannot_close_occurrence(self):
        receipts, policy = self.package()
        receipts[0]['subject']['claim_ids'] = ['one']
        with self.assertRaises(ValueError):
            self.account(receipts, policy)

    def test_unresolved_associated_claim_and_false_nonoperative_rejected(self):
        receipts, policy = self.package()
        self.claim_receipts.pop()
        with self.assertRaises(ValueError):
            self.account(receipts, policy)
        receipts, policy = self.package()
        with self.assertRaisesRegex(ValueError, 'unresolved'):
            self.account(receipts, policy)
        receipts[0]['disposition'] = 'NONOPERATIVE'
        with self.assertRaises(ValueError):
            self.account(receipts, policy)

    def test_missing_or_duplicate_denominator_subject_is_rejected(self):
        receipts, policy = self.package()
        for rows in (self.rows[:1], [*self.rows, self.rows[0]]):
            self.kwargs['requirements'] = rows
            with self.assertRaises(ValueError):
                self.account(receipts, policy)

    def test_entire_source_omission_and_missing_pin_are_rejected(self):
        self.artifacts.write_text('')
        self.kwargs['requirements'] = []
        with self.assertRaisesRegex(ValueError, 'structured source artifact'):
            structured_reconciliation._inventory([], self.artifacts, self.sources,
                                                  self.kwargs['pins'])
        self.kwargs['pins'].pop('microsoft/ghqr')
        with self.assertRaisesRegex(ValueError, 'structured source pins'):
            structured_reconciliation._inventory([], self.artifacts, self.sources,
                                                  self.kwargs['pins'])

    def test_changed_source_and_foreign_claim_association_rejected(self):
        receipts, policy = self.package()
        self.content = '- Altered\n- Beta\n'
        self.write_source()
        with self.assertRaises(ValueError):
            self.account(receipts, policy)

    def test_duplicate_foreign_receipts_and_stale_policy_rejected(self):
        receipts, policy = self.package()
        with self.assertRaises(ValueError):
            self.account([*receipts, receipts[0]], policy)
        receipts[0]['subject']['occurrence']['requirement_id'] = 'foreign'
        with self.assertRaises(ValueError):
            self.account(receipts, policy)
        policy['subject']['structured_ledger_digest'] = '0' * 64
        with self.assertRaises(ValueError):
            self.account([], policy)

    def test_unauthorized_nonindependent_and_quarantined_roles_rejected(self):
        receipts, policy = self.package()
        for identity in ('impostor', 'source-reviewer', 'reconciler', 'occurrence-reviewer'):
            candidate = copy.deepcopy(receipts)
            candidate[0]['independent_reviewer'] = identity
            authority = copy.deepcopy(policy)
            authority['authorized_independent_reviewers'] = [identity]
            with self.assertRaises(ValueError):
                self.account(candidate, authority)
        policy['authorized_reviewers'] = ['automated:semantic-review-v0.2.0']
        with self.assertRaises(ValueError):
            self.account([], policy)

    def test_future_and_out_of_order_reviews_rejected(self):
        receipts, policy = self.package()
        for field, stamp in (('reviewed_at', '2025-01-01T00:00:00Z'),
                             ('audited_at', '2099-01-01T00:00:00Z'),
                             ('audited_at', '2026-01-03T00:00:00Z')):
            changed = copy.deepcopy(receipts)
            changed[0][field] = stamp
            with self.assertRaises(ValueError):
                self.account(changed, policy)

    def test_actual_executor_cannot_independently_audit_own_claim(self):
        self.document['executor'] = 'occurrence-auditor'
        self.review_file.write_text(json.dumps(self.document))
        from ges.claim_reconciliation import _known_claims
        provenance = {'reference_claims': 2, 'review_documents': [
            {'path': str(self.review_file),
             'sha256': hashlib.sha256(self.review_file.read_bytes()).hexdigest()}]}
        subjects, _ = _known_claims(self.artifacts, self.reviews, provenance)
        for receipt, subject in zip(self.claim_receipts, subjects):
            receipt['claim'] = subject
            receipt['claim_input_digest'] = digest(subjects)
        self.claim_policy['claim_input_digest'] = digest(subjects)
        receipts, policy = self.package()
        with self.assertRaisesRegex(ValueError, 'independent'):
            self.account(receipts, policy)

    def test_forged_nested_span_digest_is_rejected(self):
        self.document['claims'][0]['source_occurrence_spans'] = [{
            'requirement_id': self.rows[0]['requirement_id'],
            'start_line': 1, 'end_line': 1, 'span_sha256': 'f' * 64}]
        self.review_file.write_text(json.dumps(self.document))
        with self.assertRaisesRegex(ValueError, 'digest'):
            structured_reconciliation.reconciliation_accounting(**self.kwargs)

    def test_altered_unsafe_missing_evidence_and_unpaired_inputs_rejected(self):
        receipts, policy = self.package()
        reference = receipts[0]['evidence']['review']
        (self.root / reference['path']).write_text('{}')
        with self.assertRaises(ValueError):
            self.account(receipts, policy)
        reference['path'] = '../outside.json'
        with self.assertRaises(ValueError):
            self.account(receipts, policy)
        with self.assertRaises(ValueError):
            self.account([], None)
        with self.assertRaises(ValueError):
            self.account(None, policy)
