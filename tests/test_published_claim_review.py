"""Synthetic contract fixtures are not published-content acceptance receipts."""
import copy
import gzip
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from ges.core import digest
from ges.published_claim_review import validate_published_claims


class PublishedClaimReview(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        self.body = b'# Guide\n\nCheck actual scope.\n'
        self.page = {'path': '/en/guide', 'version': 'free-pro-team@latest'}
        self.page['page_id'] = digest([self.page['version'], self.page['path']])[:24]
        self.ledger = self.root / 'pages.json'
        self.ledger.write_text(json.dumps([self.page]))
        self.ledger_sha = hashlib.sha256(self.ledger.read_bytes()).hexdigest()
        self.sha = hashlib.sha256(self.body).hexdigest()
        self.row = dict(self.page, ledger_sha256=self.ledger_sha, status='RETRIEVED',
                        sha256=self.sha, bytes=len(self.body),
                        body_file=self.page['page_id']+'.'+self.sha+'.md.gz',
                        retrieved_at='2026-01-01T00:00:00Z')
        self.doc = {'schema': 'ges.published-reference-claims.v1',
                    'reviewer': 'reviewer', 'reviewed_at': '2026-01-02T00:00:00Z',
                    'disposition': 'REFERENCE_ONLY', 'ledger_sha256': self.ledger_sha,
                    'instances': [dict(self.page, body_sha256=self.sha)],
                    'spans': {'scope': {'lines': [3, 3], 'sha256': hashlib.sha256(b'Check actual scope.').hexdigest()}},
                    'claims': [{'id': 'PD-1', 'span': 'scope', 'statement': 'Check real scope.'}],
                    'claim_statements': 1, 'page_instance_denominator': 1,
                    'accepted_policy': False, 'rights_accepted': False,
                    'source_revision_verified': False, 'native_behavior_verified': False,
                    'independent_omission_audit_passed': False,
                    'automated_provenance_validation_passed': False}

    def check(self, body=None, docs=None):
        self.root.joinpath('index.jsonl').write_text(json.dumps(self.row)+'\n')
        with gzip.open(self.root / self.row['body_file'], 'wb') as stream:
            stream.write(self.body if body is None else body)
        paths = []
        for i, doc in enumerate([self.doc] if docs is None else docs):
            path = self.root / f'claims-{i}.json'
            path.write_text(json.dumps(doc))
            paths.append(path)
        return validate_published_claims(self.ledger, self.root, paths, ['reviewer'])

    def test_valid_receipt_does_not_certify_semantics_or_deployment(self):
        result = self.check()
        self.assertEqual(result['reference_claims'], 1)
        self.assertEqual(result['page_instances'], 1)
        self.assertFalse(result['semantic_truth_certified'])
        self.assertFalse(result['source_revision_verified'])

    def test_corrupted_cached_body_rejected(self):
        with self.assertRaises(ValueError): self.check(body=b'changed')

    def test_wrong_ledger_rejected(self):
        self.doc['ledger_sha256'] = 'a'*64
        with self.assertRaises(ValueError): self.check()

    def test_wrong_instance_digest_rejected(self):
        self.doc['instances'][0]['body_sha256'] = 'a'*64
        with self.assertRaises(ValueError): self.check()

    def test_wrong_version_rejected(self):
        self.doc['instances'][0]['version'] = 'enterprise-cloud@latest'
        with self.assertRaises(ValueError): self.check()

    def test_wrong_path_rejected(self):
        self.doc['instances'][0]['path'] = '/en/other'
        with self.assertRaises(ValueError): self.check()

    def test_wrong_span_digest_rejected(self):
        self.doc['spans']['scope']['sha256'] = 'a'*64
        with self.assertRaises(ValueError): self.check()

    def test_out_of_range_and_boolean_spans_rejected(self):
        for lines in ([0, 3], [3, 4], [True, 3], [3, 2]):
            with self.subTest(lines=lines):
                self.doc['spans']['scope']['lines'] = lines
                with self.assertRaises(ValueError): self.check()

    def test_unknown_claim_span_rejected(self):
        self.doc['claims'][0]['span'] = 'missing'
        with self.assertRaises(ValueError): self.check()

    def test_duplicate_claim_across_documents_rejected(self):
        with self.assertRaises(ValueError): self.check(docs=[self.doc, copy.deepcopy(self.doc)])

    def test_duplicate_page_instance_rejected(self):
        self.doc['instances'].append(dict(self.doc['instances'][0]))
        self.doc['page_instance_denominator'] = 2
        with self.assertRaises(ValueError): self.check()

    def test_blank_claim_rejected(self):
        self.doc['claims'][0]['statement'] = '  '
        with self.assertRaises(ValueError): self.check()

    def test_empty_claims_and_count_mismatch_rejected(self):
        self.doc['claims'] = []
        self.doc['claim_statements'] = 0
        with self.assertRaises(ValueError): self.check()

    def test_foreign_reviewer_rejected(self):
        self.doc['reviewer'] = 'stranger'
        with self.assertRaises(ValueError): self.check()

    def test_false_completion_assertions_rejected(self):
        for key in ('accepted_policy', 'rights_accepted', 'source_revision_verified',
                    'native_behavior_verified', 'independent_omission_audit_passed'):
            with self.subTest(key=key):
                doc = copy.deepcopy(self.doc)
                doc[key] = True
                with self.assertRaises(ValueError): self.check(docs=[doc])

    def test_future_review_and_naive_timestamp_rejected(self):
        for value in ('2999-01-01T00:00:00Z', '2026-01-02T00:00:00'):
            self.doc['reviewed_at'] = value
            with self.assertRaises(ValueError): self.check()

    def test_review_before_acquisition_rejected(self):
        self.doc['reviewed_at'] = '2025-12-31T00:00:00Z'
        with self.assertRaises(ValueError): self.check()

    def test_missing_review_documents_rejected(self):
        with self.assertRaises(ValueError): self.check(docs=[])
