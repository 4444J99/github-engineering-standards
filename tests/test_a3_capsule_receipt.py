import hashlib
import gzip
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from ges.core import ROOT, digest
from ges.pinned_sources import inventory_digest
from scripts.a3_capsule_receipt import receipt


class CapsuleReceipt(unittest.TestCase):
    def setUp(self):
        temporary = TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.capsule = self.root / 'capsule'
        self.sources = self.root / 'sources'
        self.corpus = self.root / 'corpus'
        self.rendered = self.root / 'rendered'
        for directory in (self.capsule / 'sources', self.capsule / 'corpus',
                          self.sources, self.corpus, self.rendered):
            directory.mkdir(parents=True)
        self.write(self.capsule / 'sources.lock.json', {
            'sources': [{'repository': 'microsoft/ghqr', 'commit': 'a'*40, 'artifacts': 1}]})
        self.tree = self.capsule / 'sources/microsoft__ghqr.tree-reconciliation.json'
        self.write(self.tree, {'status': 'MATCH', 'git_tree_artifacts': 1,
                              'archive_artifacts': 1, 'missing_from_archive': [],
                              'extra_in_archive': [], 'blob_mismatches': []})
        text = '- id: example\n  title: Example\n'
        raw = text.encode()
        self.artifact = {'source': 'microsoft/ghqr', 'commit': 'a'*40,
                         'path': 'README.yaml', 'kind': 'text', 'size': len(raw),
                         'sha256': hashlib.sha256(raw).hexdigest(),
                         'git_blob_sha': hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()}
        self.artifact['artifact_id'] = digest(['microsoft/ghqr', 'a'*40, 'README.yaml'])[:24]
        self.write(self.capsule / 'sources/microsoft__ghqr.inventory.json', [self.artifact])
        self.snapshot = self.sources / 'microsoft__ghqr.text.jsonl.gz'
        with gzip.open(self.snapshot, 'wt') as stream:
            stream.write(json.dumps({**self.artifact, 'content': text})+'\n')
        self.tree_evidence = self.root / 'trees.json'
        self.write(self.tree_evidence, {'microsoft/ghqr': {
            'repository': 'microsoft/ghqr', 'commit': 'a'*40, 'status': 'MATCH',
            'tree_sha': 'c'*40, 'artifacts': 1,
            'method': 'GitHub pinned commit and recursive tree API',
            'inventory_digest': inventory_digest([self.artifact])}})
        self.write(self.capsule / 'manifest.json', {})
        for name in ('artifacts.jsonl', 'candidates.jsonl', 'dependencies.jsonl'):
            for directory in (self.corpus, self.capsule / 'corpus'):
                (directory / name).write_text('')
        for directory in (self.corpus, self.capsule / 'corpus'):
            (directory / 'artifacts.jsonl').write_text(json.dumps(self.artifact)+'\n')
        for directory in (self.corpus, self.capsule / 'corpus'):
            self.write(directory / 'published-page-ledger.json',
                       [{'page_id': 'page', 'path': '/en/example', 'source_matches': []}])
        self.structured = [{**{k: self.artifact[k] for k in ('source', 'commit', 'path', 'artifact_id')},
                            'requirement_id': 'SRC-GHQR-example', 'line': 1,
                            'start_line': 1, 'end_line': 2,
                            'content_sha256': self.artifact['sha256'],
                            'span_sha256': hashlib.sha256(text.rstrip('\n').encode()).hexdigest(),
                            'source_definition': {'id': 'example', 'title': 'Example'}}]
        self.write(self.corpus / 'structured-source-requirements.json', self.structured)
        self.write(self.corpus / 'ledger-summary.json',
                   {'dependency_references': 0, 'structured_source_requirements': 1})
        (self.rendered / 'index.jsonl').write_text('')
        self.validation = patch('scripts.a3_capsule_receipt.validate_capsule',
                                return_value={'published_ledger_sha256': 'fixture'})
        self.bodies = patch('scripts.a3_capsule_receipt.cached_pages',
                            return_value={'page': {'page_id': 'page'}})
        self.validation.start()
        self.bodies.start()
        self.addCleanup(self.validation.stop)
        self.addCleanup(self.bodies.stop)

    def write(self, path, value):
        path.write_text(json.dumps(value))

    def account(self):
        return receipt(self.capsule, 'fixture', self.sources, self.corpus, self.rendered,
                       expected_structured_count=1, tree_evidence=self.tree_evidence)

    def test_non_gzip_and_truncated_snapshots_rejected(self):
        original = self.snapshot.read_bytes()
        for invalid in (b'fixture', original[:-8]):
            self.snapshot.write_bytes(invalid)
            with self.assertRaises(ValueError):
                self.account()

    def test_missing_duplicate_or_substituted_snapshot_rows_rejected(self):
        for rows in ([], [{**self.artifact, 'content': 'changed'}],
                     [{**self.artifact, 'content': '- id: example\n  title: Example\n'}]*2):
            with gzip.open(self.snapshot, 'wt') as stream:
                for row in rows:
                    stream.write(json.dumps(row)+'\n')
            with self.assertRaises(ValueError):
                self.account()

    def test_object_structured_ledger_rejected(self):
        self.write(self.corpus / 'structured-source-requirements.json', {'fake': 1})
        with self.assertRaisesRegex(ValueError, 'must be an array'):
            self.account()

    def test_structured_provenance_and_identity_rejected(self):
        for field, value in (('commit', 'b'*40), ('span_sha256', '0'*64),
                             ('requirement_id', 'SRC-GHQR-forged'), ('start_line', True)):
            bad = [{**self.structured[0], field: value}]
            self.write(self.corpus / 'structured-source-requirements.json', bad)
            with self.subTest(field=field), self.assertRaises(ValueError):
                self.account()

    def test_stale_tree_revision_rejected(self):
        records = json.loads(self.tree_evidence.read_text())
        records['microsoft/ghqr']['commit'] = 'b'*40
        self.write(self.tree_evidence, records)
        with self.assertRaisesRegex(ValueError, 'pinned revision'):
            self.account()

    def test_unknown_page_mapping_rejected(self):
        self.write(self.capsule / 'corpus/published-page-ledger.json',
                   [{'page_id': 'page', 'path': '/en/example', 'source_matches': ['unknown']}])
        self.write(self.corpus / 'published-page-ledger.json',
                   [{'page_id': 'page', 'path': '/en/example', 'source_matches': ['unknown']}])
        with self.assertRaisesRegex(ValueError, 'unknown or inappropriate'):
            self.account()

    def test_busy_rendered_writer_rejected(self):
        import fcntl
        with (self.rendered / '.writer.lock').open('a') as stream:
            fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
            with self.assertRaises(BlockingIOError):
                self.account()

    def test_rendered_index_change_during_read_rejected(self):
        def mutate_index(*args, **kwargs):
            (self.rendered / 'index.jsonl').write_text('{}\n')
            return {'page': {'page_id': 'page'}}
        with patch('scripts.a3_capsule_receipt.cached_pages', mutate_index):
            with self.assertRaisesRegex(ValueError, 'index changed'):
                self.account()

    def test_receipt_does_not_assert_checkout_retention(self):
        self.assertIsNone(self.account()['checkout_retained'])

    def test_consistent_structured_row_and_summary_removal_is_rejected(self):
        self.write(self.corpus / 'structured-source-requirements.json', [])
        self.write(self.corpus / 'ledger-summary.json',
                   {'dependency_references': 0, 'structured_source_requirements': 0})
        with self.assertRaisesRegex(ValueError, 'trusted expected count'):
            self.account()

    def test_receipt_is_deterministic_and_preserves_unresolved_mappings(self):
        self.assertEqual(self.account(), self.account())
        self.assertEqual(self.account()['unresolved_page_source_mappings'], 1)
        self.assertFalse(self.account()['remote_capsule_custody_verified'])

    def test_tree_mismatch_is_rejected(self):
        tree = json.loads(self.tree.read_text())
        tree['blob_mismatches'] = ['README.md']
        self.write(self.tree, tree)
        with self.assertRaisesRegex(ValueError, 'tree reconciliation'):
            self.account()

    def test_supplement_substitution_is_rejected(self):
        (self.corpus / 'dependencies.jsonl').write_text('{}\n')
        with self.assertRaisesRegex(ValueError, 'differs from frozen capsule'):
            self.account()

    def test_incomplete_rendered_acquisition_is_rejected(self):
        with patch('scripts.a3_capsule_receipt.cached_pages', return_value={}):
            with self.assertRaisesRegex(ValueError, 'acquisition is incomplete'):
                self.account()


class CommittedCapsuleReceipt(unittest.TestCase):
    def test_committed_receipt_binds_current_source_lock_and_manifest(self):
        record = json.loads((ROOT / 'evidence/a3-six-source-capsule.json').read_text())
        lock_path = ROOT / 'sources/sources.lock.json'
        lock_sha = hashlib.sha256(lock_path.read_bytes()).hexdigest()
        manifest = record['capsule_manifest']
        self.assertEqual(manifest['source_lock_sha256'], lock_sha)
        self.assertEqual(manifest['files']['sources.lock.json'],
                         {'sha256': lock_sha, 'bytes': lock_path.stat().st_size})
        manifest_bytes = (json.dumps(manifest, indent=2, sort_keys=True) + '\n').encode()
        self.assertEqual(record['capsule_sha256'],
                         hashlib.sha256(manifest_bytes).hexdigest())
        lock = json.loads(lock_path.read_text())
        self.assertEqual(set(record['source_trees']),
                         {source['repository'] for source in lock['sources']})
        self.assertEqual(manifest['accounting']['inventory_artifacts'],
                         sum(source['artifacts'] for source in lock['sources']))
        for source in lock['sources']:
            tree = record['source_trees'][source['repository']]
            self.assertEqual(tree['status'], 'MATCH')
            self.assertEqual(tree['git_tree_artifacts'], source['artifacts'])
            self.assertEqual(tree['archive_artifacts'], source['artifacts'])
        self.assertEqual(record['structured_occurrences'], 605)
