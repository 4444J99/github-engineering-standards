import gzip
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from urllib.parse import quote

from ges.claim_workload import check_historical_equivalence, check_inventory, inventory
from ges.core import digest
from ges.pinned_sources import inventory_digest


class ClaimWorkload(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.reviews = self.root / 'reviews'
        self.reviews.mkdir()
        self.artifacts = self.root / 'artifacts.jsonl'
        self.receipts = self.root / 'receipts.json'
        self.receipts.write_text('[]')
        self.records = []

    def add(self, path, claims):
        self.records.append({'source': 'owner/source', 'commit': 'a' * 40,
                             'path': path, 'artifact_id': digest(['owner/source', 'a' * 40, path])[:24],
                             'sha256': 'b' * 64, 'git_blob_sha': 'c' * 40,
                             'kind': 'text', 'size': 128, 'candidate_count': 0,
                             'retrieval_status': 'RETRIEVED', 'review_status': 'UNREVIEWED',
                             'proposed_disposition': 'documentation',
                             'retrieved_at': '2026-01-01T00:00:00+00:00',
                             'url': 'https://github.com/owner/source/blob/' + 'a' * 40 + '/' + quote(path)})
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

    def committed_inventory(self):
        path = self.root / 'committed.json'
        path.write_text(json.dumps(self.run_inventory(), indent=2) + '\n')
        return path

    def check_command(self, committed, artifacts=None):
        return subprocess.run([
            sys.executable, '-m', 'ges.claim_workload',
            '--reviews', str(self.reviews),
            '--artifacts', str(artifacts or self.artifacts),
            '--reconciliation', str(self.receipts), '--check', str(committed),
        ], capture_output=True, text=True, check=False)

    def forward_baseline(self):
        historical = self.committed_inventory()
        self.artifacts.write_bytes(self.artifacts.read_bytes() + b'\n')
        current = self.root / 'current.json'
        current.write_text(json.dumps(self.run_inventory(), indent=2) + '\n')
        compressed = self.root / 'artifacts.jsonl.gz'
        compressed.write_bytes(gzip.compress(self.artifacts.read_bytes(), mtime=0))
        identities = {'owner/source': inventory_digest(self.records)}
        reference = self.root / 'pinned-identities.json'
        reference.write_text(json.dumps({'inventory_identity_digests': identities,
                                         'source_trees': {'owner/source': {
                                             'repository': 'owner/source', 'commit': 'a' * 40,
                                             'artifacts': len(self.records), 'status': 'MATCH',
                                             'inventory_digest': identities['owner/source'],
                                             'tree_sha': 'd' * 40}}}))
        # Synthetic authority is fixed independently before any attack rewrites inputs.
        authority = patch('ges.claim_workload.DEFAULT_SOURCE_INVENTORY_SHA256',
                          hashlib.sha256(reference.read_bytes()).hexdigest())
        authority.start()
        self.addCleanup(authority.stop)
        provenance = self.root / 'provenance.json'
        provenance.write_text(json.dumps({
            'schema': 'ges.claim-workload-current-provenance.v1',
            'acquisition_kind': 'NEW_OBSERVED_WORKFLOW_METADATA',
            'is_historical_cache_restoration': False,
            'credits': {
                'new_review_credit': 0, 'new_reconciliation_credit': 0,
                'source_body_validation': 'NOT_ASSERTED_BY_THIS_METADATA_OBSERVATION',
                'rights_clearance': 'NOT_GRANTED', 'policy_adoption': 'NOT_GRANTED',
                'native_acceptance': 'NOT_GRANTED', 'human_review': 'NOT_ASSERTED',
            },
            'bindings': {
                'historical_report_sha256': hashlib.sha256(historical.read_bytes()).hexdigest(),
                'current_report_sha256': hashlib.sha256(current.read_bytes()).hexdigest(),
                'artifact_inventory_sha256': hashlib.sha256(self.artifacts.read_bytes()).hexdigest(),
                'compressed_artifact_inventory_sha256': hashlib.sha256(compressed.read_bytes()).hexdigest(),
            },
            'historical_original_input_replay': {
                'status': 'UNAVAILABLE',
                'artifact_inventory_sha256': json.loads(historical.read_text())['inputs']['artifacts_sha256'],
            },
            'allowed_report_difference': ['inputs.artifacts_sha256'],
            'source_identity_reference': {
                'path': reference.name, 'sha256': hashlib.sha256(reference.read_bytes()).hexdigest(),
            },
            'source_identity_digests': identities,
            'metadata_projection': {
                'artifact_rows': len(self.records),
                'uncompressed_bytes': self.artifacts.stat().st_size,
                'compressed_bytes': compressed.stat().st_size,
                'fields': sorted({key for row in self.records for key in row}),
                'raw_source_bodies_included': False, 'source_archives_included': False,
                'credentials_included': False,
            },
        }))
        return historical, current, compressed, provenance

    def test_historical_equivalence_allows_only_artifact_input_hash_change(self):
        self.add('first.md', [self.claim('a')])
        historical = self.committed_inventory()
        original = historical.read_bytes()
        result = self.run_inventory()
        result['inputs']['artifacts_sha256'] = 'c' * 64
        self.assertEqual(check_historical_equivalence(result, historical), original)
        self.assertEqual(historical.read_bytes(), original)
        self.assertEqual(result['inputs']['artifacts_sha256'], 'c' * 64)

    def test_historical_equivalence_rejects_other_accounting_changes(self):
        self.add('first.md', [self.claim('a')])
        historical = self.committed_inventory()
        for mutation in ('denominator', 'membership', 'claim_digest', 'receipt_digest',
                         'credit', 'json_type'):
            with self.subTest(mutation=mutation):
                result = json.loads(historical.read_text())
                result['inputs']['artifacts_sha256'] = 'c' * 64
                if mutation == 'denominator':
                    result['counts']['recorded_claims'] += 1
                elif mutation == 'membership':
                    result['families'][0]['claim_ids'] = ['different']
                elif mutation == 'claim_digest':
                    result['claim_membership_digest'] = 'd' * 64
                elif mutation == 'receipt_digest':
                    result['inputs']['reconciliation_sha256'] = 'd' * 64
                elif mutation == 'credit':
                    result['counts']['new_review_credit'] = 1
                else:
                    result['counts']['new_review_credit'] = False
                with self.assertRaisesRegex(ValueError, 'accounting differs beyond'):
                    check_historical_equivalence(result, historical)

    def test_forward_baseline_provenance_passes_without_restoring_old_input(self):
        self.add('first.md', [self.claim('a')])
        historical, current, compressed, provenance = self.forward_baseline()
        before = {p: p.read_bytes() for p in (historical, current, compressed, provenance)}
        result = check_inventory(self.reviews, compressed, self.receipts, current,
                                 historical=historical, provenance=provenance)
        self.assertEqual(result, json.loads(current.read_text()))
        self.assertNotEqual(result['inputs']['artifacts_sha256'],
                            json.loads(historical.read_text())['inputs']['artifacts_sha256'])
        self.assertEqual(before, {p: p.read_bytes() for p in before})

    def test_forward_provenance_rejects_changed_hashes_identities_and_scope(self):
        self.add('first.md', [self.claim('a')])
        historical, current, compressed, provenance = self.forward_baseline()
        original = provenance.read_bytes()
        for mutation in ('historical_hash', 'current_hash', 'source_identities',
                         'replay_status', 'comparison_scope', 'restoration',
                         'credit', 'raw_bodies', 'review_assertion'):
            with self.subTest(mutation=mutation):
                record = json.loads(original)
                if mutation == 'historical_hash':
                    record['bindings']['historical_report_sha256'] = 'c' * 64
                elif mutation == 'current_hash':
                    record['bindings']['current_report_sha256'] = 'c' * 64
                elif mutation == 'source_identities':
                    record['source_identity_digests']['owner/source'] = 'c' * 64
                elif mutation == 'replay_status':
                    record['historical_original_input_replay']['status'] = 'RESTORED'
                elif mutation == 'comparison_scope':
                    record['allowed_report_difference'].append('counts')
                elif mutation == 'restoration':
                    record['is_historical_cache_restoration'] = True
                elif mutation == 'credit':
                    record['credits']['new_review_credit'] = 1
                elif mutation == 'raw_bodies':
                    record['metadata_projection']['raw_source_bodies_included'] = True
                else:
                    record['credits']['human_review'] = 'APPROVED'
                provenance.write_text(json.dumps(record))
                with self.assertRaises(ValueError):
                    check_inventory(self.reviews, compressed, self.receipts, current,
                                    historical=historical, provenance=provenance)

    def test_forward_provenance_rejects_raw_source_content_even_with_updated_hashes(self):
        self.add('first.md', [self.claim('a')])
        historical, current, compressed, provenance = self.forward_baseline()
        record = json.loads(provenance.read_text())
        changed = {**self.records[0], 'content': 'Upstream expression must stay out of metadata.'}
        self.artifacts.write_text(json.dumps(changed) + '\n')
        compressed.write_bytes(gzip.compress(self.artifacts.read_bytes(), mtime=0))
        current.write_text(json.dumps(self.run_inventory(), indent=2) + '\n')
        record['bindings'].update({
            'current_report_sha256': hashlib.sha256(current.read_bytes()).hexdigest(),
            'artifact_inventory_sha256': hashlib.sha256(self.artifacts.read_bytes()).hexdigest(),
            'compressed_artifact_inventory_sha256': hashlib.sha256(compressed.read_bytes()).hexdigest(),
        })
        provenance.write_text(json.dumps(record))
        with self.assertRaisesRegex(ValueError, 'non-metadata fields'):
            check_inventory(self.reviews, compressed, self.receipts, current,
                            historical=historical, provenance=provenance)

    def test_committed_inventory_reproduces_without_writing(self):
        self.add('first.md', [self.claim('a')])
        committed = self.committed_inventory()
        before = {p: p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        command = self.check_command(committed)
        self.assertEqual(command.returncode, 0, command.stderr)
        self.assertEqual(json.loads(command.stdout)['status'], 'MATCH')
        self.assertEqual(before,
                         {p: p.read_bytes() for p in self.root.rglob('*') if p.is_file()})

    def test_compressed_artifact_input_reproduces_original_byte_binding(self):
        self.add('first.md', [self.claim('a')])
        committed = self.committed_inventory()
        original = self.artifacts.read_bytes()
        compressed = self.root / 'artifacts.jsonl.gz'
        compressed.write_bytes(gzip.compress(original, mtime=0))
        self.artifacts.unlink()
        result = check_inventory(self.reviews, compressed, self.receipts, committed)
        self.assertEqual(result['inputs']['artifacts_sha256'],
                         hashlib.sha256(original).hexdigest())
        self.assertEqual(result, json.loads(committed.read_text()))
        compressed.write_bytes(compressed.read_bytes()[:-8])
        command = self.check_command(committed, artifacts=compressed)
        self.assertEqual(command.returncode, 1)
        self.assertNotIn('MATCH', command.stdout)

    def test_committed_inventory_rejects_changed_input_bytes(self):
        self.add('first.md', [self.claim('a')])
        committed = self.committed_inventory()
        for path in (self.artifacts, self.receipts, self.reviews / 'first.md-claims.json'):
            with self.subTest(path=path.name):
                original = path.read_bytes()
                path.write_bytes(original + b'\n')
                try:
                    with self.assertRaises(ValueError):
                        check_inventory(self.reviews, self.artifacts, self.receipts, committed)
                finally:
                    path.write_bytes(original)

    def test_committed_inventory_rejects_tampered_counts_and_membership(self):
        self.add('first.md', [self.claim('a')])
        committed = self.committed_inventory()
        original = committed.read_bytes()
        for mutation in ('count', 'credit', 'membership'):
            with self.subTest(mutation=mutation):
                report = json.loads(original)
                if mutation == 'count':
                    report['counts']['recorded_claims'] = 0
                elif mutation == 'credit':
                    report['counts']['new_review_credit'] = 1
                else:
                    report['families'][0]['claim_ids'] = ['different']
                committed.write_text(json.dumps(report, indent=2) + '\n')
                with self.assertRaisesRegex(ValueError, 'Committed workload inventory differs'):
                    check_inventory(self.reviews, self.artifacts, self.receipts, committed)

    def test_committed_inventory_cli_fails_missing_or_stale_input_without_repair(self):
        self.add('first.md', [self.claim('a')])
        committed = self.committed_inventory()
        expected = committed.read_bytes()
        original = self.artifacts.read_bytes()
        for payload in (None, original + b'\n'):
            with self.subTest(missing=payload is None):
                if payload is None:
                    self.artifacts.unlink()
                else:
                    self.artifacts.write_bytes(payload)
                command = self.check_command(committed)
                self.assertEqual(command.returncode, 1)
                self.assertNotIn('MATCH', command.stdout)
                self.assertEqual(committed.read_bytes(), expected)
                if payload is None:
                    self.assertFalse(self.artifacts.exists())
                else:
                    self.assertEqual(self.artifacts.read_bytes(), payload)

    def test_committed_inventory_change_during_check_rejected(self):
        self.add('first.md', [self.claim('a')])
        committed = self.committed_inventory()
        original = Path.read_bytes
        calls = 0

        def changed(path):
            nonlocal calls
            raw = original(path)
            if path == committed:
                calls += 1
                if calls > 1:
                    return raw + b' '
            return raw

        with patch.object(Path, 'read_bytes', changed):
            with self.assertRaisesRegex(ValueError, 'Committed workload inventory changed'):
                check_inventory(self.reviews, self.artifacts, self.receipts, committed)

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
                            self.provider('b', ordinal=2, identifier='ab')])
        result = self.run_inventory()
        self.assertEqual(result['counts']['provider_dataset_rows'], 2)
        self.assertEqual({family['key'][-1] for family in result['families']},
                         {'a<br>b', 'ab'})

    def test_conflicting_provider_row_identity_rejected(self):
        self.add('v1.yml', [self.provider('a'), self.provider('b')])
        path = self.reviews / 'v1.yml-claims.json'
        for field, value in (
                ('provider', 'different provider'),
                ('raw_credential_identifier', 'different-identifier'),
                ('definition_start_line', 2),
                ('definition_end_line', 11)):
            with self.subTest(field=field):
                document = json.loads(path.read_text())
                second = self.provider('b')
                second['context'][field] = value
                document['claims'][1] = second
                path.write_text(json.dumps(document))
                with self.assertRaisesRegex(ValueError, 'Conflicting provider row identity: b'):
                    self.run_inventory()

    def test_consistent_fields_share_one_provider_row_without_losing_claims(self):
        second = self.provider('b')
        second['context']['source_field'] = 'hasPushProtection'
        self.add('v1.yml', [self.provider('a'), second])
        result = self.run_inventory()
        self.assertEqual(result['counts']['provider_dataset_rows'], 1)
        self.assertEqual(result['counts']['provider_field_occurrences'],
                         {'hasPushProtection': 1, 'isPublic': 1})
        self.assertEqual(result['families'][0]['claim_ids'], ['a', 'b'])

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

    def test_query_metadata_missing_either_key_rejected(self):
        self.add('first.md', [self.claim('a')])
        path = self.reviews / 'first.md-claims.json'
        for key, value in (('query_occurrence', 'first.md#L4'),
                           ('query_help_identity', 'help/first')):
            with self.subTest(present=key):
                document = json.loads(path.read_text())
                document['claims'] = [self.claim('a', **{key: value})]
                path.write_text(json.dumps(document))
                with self.assertRaisesRegex(ValueError, 'Incomplete query row: a'):
                    self.run_inventory()

    def test_malformed_query_values_rejected(self):
        self.add('first.md', [self.claim('a')])
        path = self.reviews / 'first.md-claims.json'
        for field, value in (
                ('query_occurrence', None), ('query_occurrence', 4),
                ('query_occurrence', 'first.md#L5'),
                ('query_occurrence', 'second.md#L4'),
                ('query_help_identity', None), ('query_help_identity', True),
                ('query_help_identity', '')):
            with self.subTest(field=field, value=value):
                claim = self.claim('a', query_occurrence='first.md#L4',
                                   query_help_identity='help/first')
                claim[field] = value
                document = json.loads(path.read_text())
                document['claims'] = [claim]
                path.write_text(json.dumps(document))
                with self.assertRaisesRegex(ValueError, 'Malformed query row: a'):
                    self.run_inventory()

    def test_provider_context_cannot_hide_query_metadata(self):
        self.add('first.md', [self.provider('a')])
        path = self.reviews / 'first.md-claims.json'
        for metadata, message in (
                ({'query_occurrence': 'first.md#L4'}, 'Incomplete query row'),
                ({'query_help_identity': 'help/first'}, 'Incomplete query row'),
                ({'query_occurrence': 'first.md#L4',
                  'query_help_identity': 'help/first'}, 'Ambiguous provider and query context')):
            with self.subTest(metadata=metadata):
                document = json.loads(path.read_text())
                document['claims'] = [{**self.provider('a'), **metadata}]
                path.write_text(json.dumps(document))
                with self.assertRaisesRegex(ValueError, message):
                    self.run_inventory()

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
