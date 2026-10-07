import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from ges.claim_workload import inventory


class ClaimWorkload(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.reviews = self.root / 'reviews'
        self.reviews.mkdir()
        self.artifacts = self.root / 'artifacts.jsonl'
        self.receipts = self.root / 'receipts.json'
        self.receipts.write_text('[]')
        self.records = []

    def add(self, path, claims):
        self.records.append({'source': 'owner/source', 'commit': 'a' * 40,
                             'path': path, 'artifact_id': path,
                             'sha256': 'b' * 64})
        self.artifacts.write_text(''.join(json.dumps(r) + '\n' for r in self.records))
        doc = {'source': 'owner/source', 'commit': 'a' * 40,
               'path': path, 'claims': claims}
        (self.reviews / (path.replace('/', '-') + '-claims.json')).write_text(json.dumps(doc))

    def claim(self, cid, **extra):
        return {'claim_id': cid, 'start_line': 4, 'end_line': 4,
                'statement': 'Same words can have different context.', **extra}

    def provider(self, cid, ordinal=1, identifier='raw-id'):
        return self.claim(cid, context={
            'provider': 'provider', 'credential_identifier': identifier,
            'raw_credential_identifier': identifier, 'source_field': 'isPublic',
            'entry_ordinal': ordinal, 'definition_start_line': 1,
            'definition_end_line': 10})

    def run_inventory(self):
        return inventory(self.reviews, self.artifacts, self.receipts)

    def test_provider_versions_and_duplicate_rows_remain_members(self):
        self.add('v1.yml', [self.provider('a'), self.provider('b', ordinal=2)])
        self.add('v2.yml', [self.provider('c')])
        result = self.run_inventory()
        self.assertEqual(result['counts']['provider_dataset_rows'], 3)
        self.assertEqual(result['families'][0]['claim_ids'], ['a', 'b', 'c'])
        self.assertFalse(result['families'][0]['semantic_equivalence_verified'])
        self.assertEqual(result['counts']['new_reconciliation_credit'], 0)

    def test_raw_identity_variants_are_not_normalized_away(self):
        self.add('v1.yml', [self.provider('a', identifier='a<br>b'),
                            self.provider('b', identifier='ab')])
        self.assertEqual(len(self.run_inventory()['families']), 2)

    def test_equal_text_in_different_files_does_not_collapse_context(self):
        self.add('first.md', [self.claim('a')])
        self.add('second.md', [self.claim('b')])
        result = self.run_inventory()
        self.assertEqual(result['counts']['repeated_statement_occurrences'], 1)
        self.assertEqual(len(result['families']), 2)
        self.assertIsNone(result['counts']['unique_actionable_obligations'])

    def test_query_help_identity_and_language_context_preserved(self):
        self.add('first.md', [self.claim('a', query_occurrence='first.md#L4',
                                        query_help_identity='help/first')])
        self.add('second.md', [self.claim('b', query_occurrence='second.md#L4',
                                         query_help_identity='help/second')])
        self.assertEqual(self.run_inventory()['counts']['query_row_occurrences'], 2)

    def test_duplicate_claim_id_rejected(self):
        self.add('first.md', [self.claim('a'), self.claim('a')])
        with self.assertRaises(ValueError):
            self.run_inventory()

    def test_incomplete_provider_or_false_boolean_span_rejected(self):
        c = self.provider('a')
        del c['context']['raw_credential_identifier']
        self.add('first.md', [c])
        with self.assertRaises(ValueError):
            self.run_inventory()
        c = self.claim('a')
        c['start_line'] = True
        p = self.reviews / 'first.md-claims.json'
        d = json.loads(p.read_text())
        d['claims'] = [c]
        p.write_text(json.dumps(d))
        with self.assertRaises(ValueError):
            self.run_inventory()

    def test_unknown_reconciliation_claim_rejected(self):
        self.add('first.md', [self.claim('a')])
        self.receipts.write_text(json.dumps([{'claim': {'claim_id': 'absent'}}]))
        with self.assertRaises(ValueError):
            self.run_inventory()

    def test_supplied_artifact_binding_cannot_be_silently_overridden(self):
        self.add('first.md', [self.claim('a', artifact_id='wrong')])
        with self.assertRaises(ValueError):
            self.run_inventory()

    def test_incomplete_provider_without_display_identifier_rejected(self):
        c = self.provider('a')
        del c['context']['credential_identifier']
        del c['context']['definition_end_line']
        self.add('first.md', [c])
        with self.assertRaises(ValueError):
            self.run_inventory()

    def test_document_artifact_binding_cannot_be_silently_overridden(self):
        self.add('first.md', [self.claim('a')])
        p = self.reviews / 'first.md-claims.json'
        d = json.loads(p.read_text())
        d['artifact_id'] = 'wrong'
        p.write_text(json.dumps(d))
        with self.assertRaises(ValueError):
            self.run_inventory()

    def test_changed_statement_cannot_keep_old_receipt_binding(self):
        self.add('first.md', [self.claim('a')])
        doc = self.reviews / 'first.md-claims.json'
        subject = {**self.records[0], 'claim_id': 'a', 'start_line': 4, 'end_line': 4,
                   'content_sha256': 'b' * 64, 'claim_document': doc.name,
                   'claim_document_sha256': hashlib.sha256(doc.read_bytes()).hexdigest(),
                   'statement_sha256': 'c' * 64}
        self.receipts.write_text(json.dumps([{'claim': subject}]))
        with self.assertRaises(ValueError):
            self.run_inventory()

    def test_mid_read_mutation_rejected(self):
        self.add('first.md', [self.claim('a')])
        original = Path.read_bytes
        calls = 0

        def changed(path):
            nonlocal calls
            raw = original(path)
            if path.name == 'first.md-claims.json':
                calls += 1
                if calls > 1:
                    return raw + b' '
            return raw

        with patch.object(Path, 'read_bytes', changed), self.assertRaises(ValueError):
            self.run_inventory()

    def test_added_document_during_read_rejected(self):
        self.add('first.md', [self.claim('a')])
        original = Path.read_bytes

        def added(path):
            raw = original(path)
            if path.name == 'first.md-claims.json':
                (self.reviews / 'added-claims.json').write_text(json.dumps({
                    'claims': [self.claim('b')]}))
            return raw

        with patch.object(Path, 'read_bytes', added), self.assertRaises(ValueError):
            self.run_inventory()


if __name__ == '__main__':
    unittest.main()
