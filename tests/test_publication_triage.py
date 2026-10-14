"""Publication triage observations never become semantic or rights approval."""
import copy
import gzip
import hashlib
import json
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory
import unittest

from ges.core import digest
from ges.pinned_sources import inventory_digest
from ges.publication_triage import triage


class PublicationTriage(unittest.TestCase):
    def setUp(self):
        temporary = TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.repository = self.root / 'repository'
        self.repository.mkdir()
        self.source = 'synthetic/source'
        self.pin = 'a' * 40
        self.expression = 'A synthetic "quoted" clause preserves café accents and exact source punctuation.'
        self.raw_source = (self.expression + '\n\nAnother synthetic source paragraph.\n').encode('utf-8')
        artifact = {'source': self.source, 'commit': self.pin, 'path': 'README.md',
                    'artifact_id': digest([self.source, self.pin, 'README.md'])[:24],
                    'sha256': hashlib.sha256(self.raw_source).hexdigest(),
                    'git_blob_sha': hashlib.sha1(b'blob ' + str(len(self.raw_source)).encode() + b'\0' + self.raw_source).hexdigest(),
                    'size': len(self.raw_source), 'kind': 'text', 'retrieved_at': '2026-01-01T00:00:00Z'}
        self.artifacts, self.pins = [artifact], {self.source: self.pin}
        identity = inventory_digest(self.artifacts)
        reference = {'schema': 'SYNTHETIC_TEST_ONLY',
                     'inventory_identity_digests': {self.source: identity},
                     'source_trees': {self.source: {'repository': self.source, 'commit': self.pin,
                       'status': 'MATCH', 'artifacts': 1, 'inventory_digest': identity, 'tree_sha': 'c' * 40}}}
        self.reference = self.root / 'synthetic-reference.json'
        self.reference.write_text(json.dumps(reference))
        self.reference_sha = hashlib.sha256(self.reference.read_bytes()).hexdigest()
        self.source_root = self.root / 'sources'
        self.source_root.mkdir()
        self.snapshot = self.source_root / 'synthetic__source.text.jsonl.gz'
        self.write_snapshot()
        proposal = {'source': self.source, 'commit': self.pin, 'claims': [
            {'path': 'README.md', 'statement': self.expression},
            {'path': 'README.md', 'statement': 'A different project observation with sufficient words requires human comparison.'}]}
        (self.repository / 'proposals.json').write_text(json.dumps(proposal, indent=2), encoding='utf-8')
        (self.repository / 'README.md').write_text(
            f'https://github.com/{self.source}/blob/{self.pin}/README.md\n\n{self.expression}\n', encoding='utf-8')
        (self.repository / 'support.txt').write_text('No source locator appears in this synthetic project file.\n')
        (self.repository / '.included').write_text('Tracked support file must be inventoried.\n')
        self.git('init', '-q')
        self.commit()

    def git(self, *args):
        return subprocess.check_output(['git', '-C', str(self.repository), *args], stderr=subprocess.PIPE)

    def commit(self):
        self.git('add', '.')
        self.git('-c', 'user.name=Synthetic Test', '-c', 'user.email=test@example.invalid',
                 'commit', '-qm', 'Synthetic publication candidate')
        self.revision = self.git('rev-parse', 'HEAD').decode().strip()

    def write_snapshot(self, *, rows=None):
        rows = rows if rows is not None else [{**self.artifacts[0], 'content': self.raw_source.decode('utf-8')}]
        with gzip.open(self.snapshot, 'wt', encoding='utf-8') as stream:
            for row in rows:
                stream.write(json.dumps(row) + '\n')

    def report(self, *, compare=False, artifacts=None):
        return triage(self.repository, self.revision, artifacts or self.artifacts, self.pins,
                      source_inventory_reference=self.reference, source_inventory_sha256=self.reference_sha,
                      source_root=self.source_root if compare else None)

    def test_complete_immutable_tree_ignores_worktree_drift_and_untracked_files(self):
        original = self.report()
        (self.repository / 'support.txt').write_text('Changed after candidate commit.')
        (self.repository / 'untracked.txt').write_text('Outside immutable candidate.')
        actual = self.report()
        self.assertEqual(actual, original)
        self.assertEqual(actual['summary']['output_count'], 4)
        self.assertIn('.included', [row['path'] for row in actual['outputs']])
        for row in actual['outputs']:
            raw = self.git('cat-file', 'blob', self.revision + ':' + row['path'])
            self.assertEqual(row['sha256'], hashlib.sha256(raw).hexdigest())
            self.assertEqual(row['size_bytes'], len(raw))

    def test_without_bodies_candidates_and_absent_locators_remain_unreviewed(self):
        result = self.report()
        self.assertEqual(result['summary']['unreviewed_output_count'], 4)
        self.assertEqual(result['summary']['exact_match_candidate_count'], 0)
        self.assertEqual(result['source_body_observations'], [])
        for row in result['outputs']:
            self.assertEqual(row['disposition'], 'UNREVIEWED')
            for candidate in row['expression_candidates']:
                self.assertEqual(candidate['body_comparison'], 'NOT_SUPPLIED')
        support = next(row for row in result['outputs'] if row['path'] == 'support.txt')
        self.assertEqual(support['triage_category'], 'NO_SOURCE_LOCATOR_DETECTED')
        self.assertIn('AUTHORSHIP_AND_AUTHORITY', support['review_requirements'])
        self.assertFalse(any(result['authority'].values()))

    def test_exact_matches_bind_original_encoded_output_and_pinned_source_bytes(self):
        result = self.report(compare=True)
        proposals = next(row for row in result['outputs'] if row['path'] == 'proposals.json')
        candidate = proposals['expression_candidates'][0]
        self.assertEqual(candidate['locator'], '/claims/0/statement')
        self.assertEqual(candidate['body_comparison'], 'EXACT_MATCH_FOUND')
        self.assertEqual(candidate['exact_matches'][0]['match_kind'], 'EXACT_DECODED_JSON_STRING')
        self.assertEqual(proposals['expression_candidates'][1]['body_comparison'], 'NO_EXACT_MATCH_FOUND')
        raw = self.git('cat-file', 'blob', self.revision + ':proposals.json')
        span = candidate['output_range']
        self.assertEqual(hashlib.sha256(raw[span['start_byte']:span['end_byte']]).hexdigest(), span['sha256'])
        self.assertEqual(json.loads(b'"' + raw[span['start_byte']:span['end_byte']] + b'"'), self.expression)
        source_span = candidate['exact_matches'][0]['source_range']
        self.assertEqual(hashlib.sha256(self.raw_source[source_span['start_byte']:source_span['end_byte']]).hexdigest(),
                         source_span['sha256'])
        self.assertEqual(proposals['disposition'], 'UNREVIEWED')
        self.assertFalse(result['authority']['rights_clearance_granted'])

    def test_canonical_fabricated_source_row_cannot_supply_its_own_inventory_authority(self):
        changed = copy.deepcopy(self.artifacts)
        changed[0]['path'] = 'fabricated.md'
        changed[0]['artifact_id'] = digest([self.source, self.pin, 'fabricated.md'])[:24]
        with self.assertRaisesRegex(ValueError, 'complete trusted pinned inventory'):
            self.report(artifacts=changed)

    def test_changed_and_incomplete_snapshot_bytes_are_rejected(self):
        self.write_snapshot(rows=[{**self.artifacts[0], 'content': self.raw_source.decode() + ' changed'}])
        with self.assertRaisesRegex(ValueError, 'pinned inventory digest'):
            self.report(compare=True)
        self.write_snapshot(rows=[])
        with self.assertRaisesRegex(ValueError, 'Incomplete pinned text-artifact coverage'):
            self.report(compare=True)

    def test_unresolved_locator_is_recorded_without_fabricating_a_source_identity(self):
        (self.repository / 'missing.json').write_text(json.dumps({
            'source': self.source, 'commit': self.pin, 'path': 'not-in-source.md',
            'statement': 'This uncertain proposed expression has no matching source artifact.'}))
        self.commit()
        result = self.report()
        row = next(row for row in result['outputs'] if row['path'] == 'missing.json')
        self.assertEqual(row['source_artifact_ids'], [])
        self.assertEqual(row['unresolved_locators'][0]['path'], 'not-in-source.md')
        self.assertIn('LOCATOR_REPAIR', row['review_requirements'])
        self.assertEqual(len(result['source_artifacts']), 1)

    def test_compressed_payload_ranges_are_explicitly_not_raw_output_spans(self):
        payload = json.dumps({'source': self.source, 'commit': self.pin, 'path': 'README.md',
                              'statement': self.expression}).encode() + b'\n'
        with gzip.open(self.repository / 'claims.jsonl.gz', 'wb') as stream:
            stream.write(payload)
        self.commit()
        result = self.report(compare=True)
        row = next(row for row in result['outputs'] if row['path'] == 'claims.jsonl.gz')
        candidate = row['expression_candidates'][0]
        self.assertEqual(row['content_format'], 'GZIP_JSONL')
        self.assertEqual(candidate['range_encoding'], 'DECODED_GZIP_JSON_STRING')
        self.assertEqual(candidate['exact_matches'][0]['match_kind'], 'EXACT_DECODED_CONTAINER_STRING')
        span = candidate['output_range']
        self.assertEqual(hashlib.sha256(payload[span['start_byte']:span['end_byte']]).hexdigest(), span['sha256'])
        self.assertIn('CONTAINER_CONTENTS', row['review_requirements'])
        self.assertEqual(row['disposition'], 'UNREVIEWED')

    def test_symlink_git_entry_is_rejected_instead_of_omitted(self):
        (self.repository / 'alias').symlink_to('support.txt')
        self.commit()
        with self.assertRaisesRegex(ValueError, 'Nonregular candidate Git entry'):
            self.report()

    def test_malformed_json_retains_output_identity_and_explicit_unfinished_review(self):
        raw = b'{"statement": "Invalid JSON with trailing comma",}\n'
        (self.repository / 'malformed.json').write_bytes(raw)
        self.commit()
        result = self.report()
        row = next(row for row in result['outputs'] if row['path'] == 'malformed.json')
        self.assertEqual(result['summary']['output_count'], 5)
        self.assertEqual(result['summary']['scan_incomplete_output_count'], 1)
        self.assertEqual(row['sha256'], hashlib.sha256(raw).hexdigest())
        self.assertEqual(row['scan_status'], 'INCOMPLETE')
        self.assertEqual(row['disposition'], 'UNREVIEWED')
        self.assertIn('MANUAL_FORMAT_REVIEW', row['review_requirements'])

    def test_generated_view_inherits_only_observed_exact_canonical_field_associations(self):
        (self.repository / 'controls').mkdir()
        (self.repository / 'generated').mkdir()
        control = {'id': 'GES-TEST-001', 'objective': self.expression,
                   'sources': [{'repository': self.source, 'commit': self.pin, 'path': 'README.md'}]}
        (self.repository / 'controls' / 'catalog.json').write_text(json.dumps([control]))
        (self.repository / 'generated' / 'functional-checklist.md').write_text(
            '# Generated synthetic view\n\n- ' + self.expression + '\n', encoding='utf-8')
        self.commit()
        result = self.report(compare=True)
        row = next(row for row in result['outputs'] if row['path'] == 'generated/functional-checklist.md')
        candidates = [candidate for candidate in row['expression_candidates'] if 'derived_from' in candidate]
        self.assertEqual(len(candidates), 1)
        self.assertEqual(candidates[0]['derived_from'], {'path': 'controls/catalog.json', 'locator': '/0/objective'})
        self.assertEqual(candidates[0]['body_comparison'], 'EXACT_MATCH_FOUND')
        self.assertEqual(row['disposition'], 'UNREVIEWED')
        self.assertNotIn(self.expression, json.dumps(result, ensure_ascii=False))

    def test_external_pinned_locator_is_preserved_without_expanding_source_authority(self):
        (self.repository / 'external.md').write_text(
            'External component provenance: https://github.com/external/component/blob/' + 'd' * 40 + '/NOTICE.md\n')
        self.commit()
        result = self.report()
        row = next(row for row in result['outputs'] if row['path'] == 'external.md')
        self.assertEqual(row['unresolved_locators'][0]['source'], 'external/component')
        self.assertEqual(row['unresolved_locators'][0]['status'], 'OUTSIDE_AUTHENTICATED_SOURCE_INVENTORY')
        self.assertEqual(row['source_artifact_ids'], [])
        self.assertEqual(len(result['source_artifacts']), 1)
        self.assertEqual(row['disposition'], 'UNREVIEWED')


if __name__ == '__main__':
    unittest.main()
