import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

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
            'sources': [{'repository': 'example/source', 'artifacts': 1}]})
        self.tree = self.capsule / 'sources/example__source.tree-reconciliation.json'
        self.write(self.tree, {'status': 'MATCH', 'git_tree_artifacts': 1,
                              'archive_artifacts': 1, 'missing_from_archive': [],
                              'extra_in_archive': [], 'blob_mismatches': []})
        (self.sources / 'example__source.text.jsonl.gz').write_bytes(b'fixture')
        self.write(self.capsule / 'manifest.json', {})
        for name in ('artifacts.jsonl', 'candidates.jsonl', 'dependencies.jsonl'):
            for directory in (self.corpus, self.capsule / 'corpus'):
                (directory / name).write_text('')
        for directory in (self.corpus, self.capsule / 'corpus'):
            self.write(directory / 'published-page-ledger.json',
                       [{'page_id': 'page', 'source_matches': []}])
        self.write(self.corpus / 'structured-source-requirements.json', [])
        self.write(self.corpus / 'ledger-summary.json',
                   {'dependency_references': 0, 'structured_source_requirements': 0})
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
        return receipt(self.capsule, 'fixture', self.sources, self.corpus, self.rendered)

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
