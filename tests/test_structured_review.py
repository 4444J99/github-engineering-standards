"""Public reference-accounting contracts, including counterexamples."""
import copy
import hashlib
import gzip
import json
import tempfile
import unittest
from pathlib import Path

from ges.structured_review import validate_accounting


class StructuredReview(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.ledger = self.root / 'ledger.json'
        self.doc = self.root / 'claims.json'
        self.accounting = self.root / 'accounting.json'
        self.row = {'requirement_id': 'SRC-1', 'source': 'owner/repo',
                    'commit': 'a'*40, 'path': 'checklist.md', 'start_line': 2,
                    'end_line': 3, 'content_sha256': 'b'*64, 'span_sha256': 'c'*64}
        self.document = {'reviewer': 'reviewer', 'reviewed_at': '2026-01-01T00:00:00Z',
                         'source': self.row['source'], 'commit': self.row['commit'],
                         'path': self.row['path'], 'claims': [
                             {'claim_id': 'REF-1', 'statement': 'Review access.',
                              'structured_requirement_ids': ['SRC-1'],
                              'start_line': 2, 'end_line': 3, 'accepted_policy': False}]}
        self.receipt = {'structured_occurrences': 1, 'accounted_occurrence_ids': ['SRC-1'],
                        'nonoperative_labels': [], 'reviewed_reference_statements': 1,
                        'missing_ids': [], 'extra_ids': []}
        for key in ('consolidation_complete', 'generalization_complete',
                    'operational_completeness', 'policy_accepted', 'independent_omission_certified'):
            self.receipt[key] = False

    def write_inputs(self):
        self.ledger.write_text(json.dumps([self.row]))
        self.doc.write_text(json.dumps(self.document))
        self.receipt['structured_ledger_sha256'] = hashlib.sha256(self.ledger.read_bytes()).hexdigest()
        self.receipt['review_documents'] = [{'path': 'claims.json',
                                           'sha256': hashlib.sha256(self.doc.read_bytes()).hexdigest()}]
        self.accounting.write_text(json.dumps(self.receipt))

    def check(self):
        self.write_inputs()
        return validate_accounting(self.root, self.ledger, self.accounting, ['reviewer'])

    def test_valid_reference_is_not_completion(self):
        result = self.check()
        self.assertTrue(result['valid'])
        self.assertFalse(result['consolidation_complete'])
        self.assertFalse(result['independent_omission_certified'])

    def test_narrow_atomic_span_within_definition_is_valid(self):
        self.document['claims'][0]['end_line'] = 2
        self.assertTrue(self.check()['valid'])

    def test_changed_claim_document_fails_digest(self):
        self.write_inputs()
        self.doc.write_text(self.doc.read_text()+' ')
        with self.assertRaisesRegex(ValueError, 'digest mismatch'):
            validate_accounting(self.root, self.ledger, self.accounting, ['reviewer'])

    def test_changed_ledger_fails_digest(self):
        self.write_inputs()
        self.ledger.write_text(self.ledger.read_text()+' ')
        with self.assertRaisesRegex(ValueError, 'ledger digest'):
            validate_accounting(self.root, self.ledger, self.accounting, ['reviewer'])

    def test_missing_reference_cannot_hide_behind_advertised_id(self):
        self.document['claims'][0]['structured_requirement_ids'] = ['SRC-OTHER']
        with self.assertRaises(ValueError):
            self.check()

    def test_duplicate_advertised_id_rejected(self):
        self.receipt['accounted_occurrence_ids'].append('SRC-1')
        with self.assertRaises(ValueError):
            self.check()

    def test_duplicate_claim_id_rejected(self):
        self.document['claims'].append(copy.deepcopy(self.document['claims'][0]))
        with self.assertRaisesRegex(ValueError, 'duplicate reference'):
            self.check()

    def test_out_of_definition_span_rejected(self):
        self.document['claims'][0]['end_line'] = 4
        with self.assertRaisesRegex(ValueError, 'outside occurrence'):
            self.check()

    def test_boolean_span_is_not_line_number(self):
        self.document['claims'][0]['start_line'] = True
        with self.assertRaises(ValueError):
            self.check()

    def test_wrong_source_commit_rejected(self):
        self.document['commit'] = 'd'*40
        with self.assertRaisesRegex(ValueError, 'provenance mismatch'):
            self.check()

    def test_unauthorized_reviewer_rejected(self):
        self.document['reviewer'] = 'stranger'
        with self.assertRaisesRegex(ValueError, 'Unauthorized'):
            self.check()

    def test_future_timestamp_rejected(self):
        self.document['reviewed_at'] = '2999-01-01T00:00:00Z'
        with self.assertRaises(ValueError):
            self.check()

    def test_naive_timestamp_rejected(self):
        self.document['reviewed_at'] = '2026-01-01T00:00:00'
        with self.assertRaises(ValueError):
            self.check()

    def test_empty_statement_rejected(self):
        self.document['claims'][0]['statement'] = ' '
        with self.assertRaises(ValueError):
            self.check()

    def test_reference_cannot_assert_adoption(self):
        self.document['claims'][0]['accepted_policy'] = True
        with self.assertRaisesRegex(ValueError, 'adopted policy'):
            self.check()

    def test_reference_cannot_close_gate(self):
        self.receipt['independent_omission_certified'] = True
        with self.assertRaisesRegex(ValueError, 'cannot certify'):
            self.check()

    def test_false_statement_count_rejected(self):
        self.receipt['reviewed_reference_statements'] = 100
        with self.assertRaisesRegex(ValueError, 'statement count'):
            self.check()

    def test_label_reference_conflict_rejected(self):
        self.document['non_actionable_structured_occurrences'] = [
            {'structured_requirement_id': 'SRC-1', 'line': 2,
             'rationale': 'Section label, not a requirement.'}]
        with self.assertRaisesRegex(ValueError, 'both a label'):
            self.check()

    def test_unsubstantiated_label_rejected(self):
        self.receipt['nonoperative_labels'] = ['SRC-1']
        with self.assertRaisesRegex(ValueError, 'Advertised labels'):
            self.check()

    def test_parent_path_is_not_allowed(self):
        self.write_inputs()
        self.receipt['review_documents'][0]['path'] = '../claims.json'
        self.accounting.write_text(json.dumps(self.receipt))
        with self.assertRaisesRegex(ValueError, 'Unsafe'):
            validate_accounting(self.root, self.ledger, self.accounting, ['reviewer'])

    def source_fixture(self):
        text = 'Title\nReview access.\nCheck inherited grants.\n'
        self.row['content_sha256'] = hashlib.sha256(text.encode()).hexdigest()
        self.row['span_sha256'] = hashlib.sha256('Review access.\nCheck inherited grants.'.encode()).hexdigest()
        with gzip.open(self.root / 'owner__repo.text.jsonl.gz', 'wt') as stream:
            stream.write(json.dumps({'source': self.row['source'], 'commit': self.row['commit'],
                                     'path': self.row['path'], 'content': text})+'\n')
        self.write_inputs()

    def test_actual_pinned_source_spans_validate(self):
        self.source_fixture()
        result = validate_accounting(self.root, self.ledger, self.accounting, ['reviewer'], self.root)
        self.assertTrue(result['pinned_source_spans_verified'])

    def test_source_tamper_rejected_even_with_unchanged_ledger(self):
        self.source_fixture()
        with gzip.open(self.root / 'owner__repo.text.jsonl.gz', 'wt') as stream:
            stream.write(json.dumps({'source': self.row['source'], 'commit': self.row['commit'],
                                     'path': self.row['path'], 'content': 'Title\nAltered.\nAltered.\n'})+'\n')
        with self.assertRaisesRegex(ValueError, 'content digest mismatch'):
            validate_accounting(self.root, self.ledger, self.accounting, ['reviewer'], self.root)

    def test_forged_ledger_span_digest_rejected(self):
        self.source_fixture()
        self.row['span_sha256'] = 'f'*64
        self.write_inputs()
        with self.assertRaisesRegex(ValueError, 'span digest mismatch'):
            validate_accounting(self.root, self.ledger, self.accounting, ['reviewer'], self.root)

    def test_string_reviewer_policy_is_not_authorization(self):
        self.write_inputs()
        with self.assertRaisesRegex(ValueError, 'list of identities'):
            validate_accounting(self.root, self.ledger, self.accounting, 'reviewer')

    def test_forged_nested_occurrence_span_rejected(self):
        self.document['claims'][0]['source_occurrence_spans'] = [
            {'requirement_id': 'SRC-1', 'start_line': 2, 'end_line': 3, 'span_sha256': 'f'*64}]
        with self.assertRaisesRegex(ValueError, 'digest mismatch'):
            self.check()


if __name__ == '__main__':
    unittest.main()
