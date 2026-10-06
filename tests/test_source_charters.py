"""Charter evidence contracts without requiring private source caches in CI."""
import gzip
import hashlib
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from ges.source_charters import validate_manifest
from ges.pinned_sources import inventory_digest


ROOT = Path(__file__).resolve().parents[1]


class SourceCharters(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        for directory in ('evidence', 'sources', 'docs/source-charters'):
            (self.root / directory).mkdir(parents=True)
        shutil.copy(ROOT / 'sources/sources.lock.json', self.root / 'sources')
        for doc in (ROOT / 'docs/source-charters').glob('*.md'):
            shutil.copy(doc, self.root / 'docs/source-charters')
        self.manifest = json.loads((ROOT / 'evidence/a4-source-charters.json').read_text())
        self.sources = self.root / 'cache'
        self.sources.mkdir()
        # Synthetic sources exercise all real locator shapes without copying upstream text.
        text = ''.join(f'Synthetic line {i}\n' for i in range(1, 201))
        self.text = text
        artifacts = {}
        for row in self.manifest['citations']:
            row['content_sha256'] = hashlib.sha256(text.encode()).hexdigest()
            span = '\n'.join(text.splitlines()[row['start_line']-1:row['end_line']])
            row['span_sha256'] = hashlib.sha256(span.encode()).hexdigest()
            artifacts.setdefault(row['repository'], {})[row['path']] = {
                'source': row['repository'], 'commit': row['commit'],
                'path': row['path'], 'content': text, 'kind': 'text',
                'size': len(text.encode()), 'sha256': hashlib.sha256(text.encode()).hexdigest(),
                'git_blob_sha': hashlib.sha1(b'blob '+str(len(text.encode())).encode()+b'\0'+text.encode()).hexdigest()}
        inventories = {}
        for repo, files in artifacts.items():
            inventory = [{k:v for k,v in artifact.items() if k != 'content'}
                         for artifact in files.values()]
            (self.sources / (repo.replace('/', '__')+'.inventory.json')).write_text(json.dumps(inventory))
            inventories[repo] = inventory_digest(inventory)
            with gzip.open(self.sources / (repo.replace('/', '__')+'.text.jsonl.gz'), 'wt') as stream:
                for artifact in files.values():
                    stream.write(json.dumps(artifact)+'\n')
        manifest = {'source_lock_sha256': hashlib.sha256(
            (self.root / 'sources/sources.lock.json').read_bytes()).hexdigest()}
        self.capsule_sha = hashlib.sha256(
            (json.dumps(manifest, indent=2, sort_keys=True)+'\n').encode()).hexdigest()
        self.manifest['a3_capsule_sha256'] = self.capsule_sha
        self.baseline = self.root / 'baseline.json'
        self.baseline.write_text(json.dumps({'schema': 'ges.a3-capsule-receipt.v2',
                                            'capsule_sha256': self.capsule_sha,
                                            'capsule_manifest': manifest,
                                            'inventory_identity_digests': inventories}))
        self.receipt_sha = hashlib.sha256(self.baseline.read_bytes()).hexdigest()
        self.manifest['a3_receipt_sha256'] = self.receipt_sha

    def check(self):
        (self.root / 'evidence/a4-source-charters.json').write_text(json.dumps(self.manifest))
        return validate_manifest(self.root, self.sources, capsule_receipt=self.baseline,
                                 capsule_sha256=self.capsule_sha, receipt_sha256=self.receipt_sha)

    def test_committed_manifest_matches_pins_and_document_locators(self):
        result = validate_manifest(ROOT)
        self.assertTrue(result['valid'])
        self.assertFalse(result['source_bytes_replayed'])
        self.assertFalse(result['owner_approved'])

    def test_all_locator_shapes_replay_through_canonical_verifier(self):
        self.assertTrue(self.check()['source_bytes_replayed'])

    def test_trailing_newline_span_is_rejected(self):
        row = self.manifest['citations'][0]
        span = '\n'.join(self.text.splitlines()[row['start_line']-1:row['end_line']])+'\n'
        row['span_sha256'] = hashlib.sha256(span.encode()).hexdigest()
        with self.assertRaisesRegex(ValueError, 'Pinned source span digest mismatch'):
            self.check()

    def test_changed_content_digest_is_rejected(self):
        self.manifest['citations'][0]['content_sha256'] = '0'*64
        with self.assertRaisesRegex(ValueError, 'Pinned source content digest mismatch'):
            self.check()

    def test_missing_citation_is_rejected(self):
        self.manifest['citations'].pop()
        with self.assertRaisesRegex(ValueError, 'locator set mismatch'):
            self.check()

    def test_old_field_name_is_rejected(self):
        self.manifest['citations'][0]['file_sha256'] = '0'*64
        with self.assertRaisesRegex(ValueError, 'canonical content_sha256'):
            self.check()

    def test_missing_cache_fails_instead_of_skipping(self):
        self.check()
        with self.assertRaises(FileNotFoundError):
            validate_manifest(self.root, self.root / 'absent-cache',
                              capsule_receipt=self.baseline, capsule_sha256=self.capsule_sha,
                              receipt_sha256=self.receipt_sha)

    def test_changed_visible_charter_link_rejected(self):
        doc = self.root / self.manifest['citations'][0]['charter']
        doc.write_text(doc.read_text().replace('#L32-L33', '#L32-L34'))
        with self.assertRaisesRegex(ValueError, 'locator set mismatch'):
            self.check()

    def test_missing_or_changed_capsule_trust_rejected(self):
        self.check()
        with self.assertRaisesRegex(ValueError, 'Independently trusted'):
            validate_manifest(self.root, self.sources)
        with self.assertRaisesRegex(ValueError, 'trusted baseline'):
            validate_manifest(self.root, self.sources, capsule_receipt=self.baseline,
                              capsule_sha256='0'*64, receipt_sha256=self.receipt_sha)

    def test_receipt_inventory_digest_substitution_rejected(self):
        baseline = json.loads(self.baseline.read_text())
        baseline['inventory_identity_digests']['github/docs'] = '0'*64
        self.baseline.write_text(json.dumps(baseline))
        with self.assertRaisesRegex(ValueError, 'receipt bytes'):
            self.check()

    def test_alternative_inventory_with_same_cited_spans_rejected(self):
        path = next(self.sources.glob('*.inventory.json'))
        rows = json.loads(path.read_text())
        rows.append({**rows[0], 'path': 'uncited-new-file'})
        path.write_text(json.dumps(rows))
        with self.assertRaisesRegex(ValueError, 'trusted A3 capsule'):
            self.check()
