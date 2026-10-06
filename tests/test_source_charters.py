import copy
import gzip
import hashlib
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from ges.core import ROOT
from ges.source_charters import validate_citations


class SourceCharters(unittest.TestCase):
    def test_manifest_uses_canonical_fields_and_retains_approval_gate(self):
        manifest = json.loads((ROOT / 'evidence/a4-source-charters.json').read_text())
        self.assertEqual(manifest['status'], 'PROPOSED_REQUIRES_OWNER_APPROVAL')
        self.assertEqual(len(manifest['citations']), 23)
        for citation in manifest['citations']:
            self.assertIn('content_sha256', citation)
            self.assertNotIn('file_sha256', citation)
            self.assertTrue((ROOT / citation['charter']).is_file())

    def test_replay_rejects_trailing_newline_and_changed_content(self):
        content = 'First line\nSecond line\n'
        citation = {'repository': 'test/source', 'commit': 'a' * 40,
                    'path': 'README.md', 'start_line': 1, 'end_line': 1,
                    'content_sha256': hashlib.sha256(content.encode()).hexdigest(),
                    'span_sha256': hashlib.sha256(b'First line').hexdigest()}
        manifest = {'citations': [citation]}
        with TemporaryDirectory() as directory:
            sources = Path(directory)
            with gzip.open(sources / 'test__source.text.jsonl.gz', 'wt') as stream:
                stream.write(json.dumps({'source': 'test/source', 'commit': 'a' * 40,
                                         'path': 'README.md', 'content': content}) + '\n')
            pins = {'test/source': 'a' * 40}
            self.assertTrue(validate_citations(manifest, sources, pins)['valid'])
            bad = copy.deepcopy(manifest)
            bad['citations'][0]['span_sha256'] = hashlib.sha256(b'First line\n').hexdigest()
            with self.assertRaisesRegex(ValueError, 'span digest mismatch'):
                validate_citations(bad, sources, pins)
            bad = copy.deepcopy(manifest)
            bad['citations'][0]['content_sha256'] = '0' * 64
            with self.assertRaisesRegex(ValueError, 'content digest mismatch'):
                validate_citations(bad, sources, pins)
