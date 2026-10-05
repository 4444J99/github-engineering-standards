"""Frozen inputs are transport integrity, never review or remote custody."""
import copy
import gzip
import hashlib
import io
import json
from pathlib import Path
import tarfile
import tempfile
import unittest
from unittest.mock import patch

from ges.core import digest, dump
from ges.frozen_inputs import freeze, hydrate, validate_capsule


class FrozenInputs(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name).resolve()
        self.sources = self.root / 'sources'
        self.corpus = self.root / 'corpus'
        self.sources.mkdir()
        self.corpus.mkdir()
        self.content = b'First clause.\nSecond clause.\n'
        stream = io.BytesIO()
        with tarfile.open(fileobj=stream, mode='w:gz') as archive:
            member = tarfile.TarInfo('repo-pin/content/example.md')
            member.size = len(self.content)
            archive.addfile(member, io.BytesIO(self.content))
        self.archive = stream.getvalue()
        self.spec = {'repository': 'owner/repo', 'commit': 'a' * 40,
                     'archive_sha256': hashlib.sha256(self.archive).hexdigest(),
                     'archive_bytes': len(self.archive), 'artifacts': 1}
        self.lock = self.root / 'lock.json'
        dump(self.lock, {'sources': [self.spec]})
        row = {'source': 'owner/repo', 'commit': 'a' * 40,
               'path': 'content/example.md', 'sha256': hashlib.sha256(self.content).hexdigest(),
               'git_blob_sha': hashlib.sha1(b'blob ' + str(len(self.content)).encode() + b'\0' + self.content).hexdigest(),
               'size': len(self.content), 'kind': 'text', 'retrieval_status': 'RETRIEVED',
               'retrieved_at': '2026-10-01T00:00:00+00:00', 'review_status': 'UNREVIEWED',
               'url': 'https://github.com/owner/repo/blob/' + 'a' * 40 + '/content/example.md'}
        dump(self.sources / 'owner__repo.inventory.json', [row])
        dump(self.sources / 'owner__repo.tree-reconciliation.json', {
            'status': 'MATCH', 'missing_from_archive': [], 'extra_in_archive': [], 'blob_mismatches': []})
        self.artifact = {**row, 'artifact_id': digest(['owner/repo', 'a' * 40, row['path']])[:24],
                         'candidate_count': 0, 'proposed_disposition': 'documentation'}
        (self.corpus / 'artifacts.jsonl').write_text(json.dumps(self.artifact) + '\n')
        (self.corpus / 'candidates.jsonl').write_text('')
        (self.corpus / 'dependencies.jsonl').write_text('')
        dump(self.corpus / 'published-page-ledger.json', [{'page_id': 'page-one',
             'path': '/en/example', 'version': 'free-pro-team@latest', 'source_matches': []}])
        self.capsule = self.root / 'capsule'
        self.report = freeze(self.sources, self.corpus, self.capsule, manifest=self.lock)
        self.sha = self.report['capsule_sha256']
        self.partition = {'schema_version': 'ges.review-partition.v1', 'capsule_sha256': self.sha,
                          'artifact_ids': [self.artifact['artifact_id']]}

    def validate(self, sha=None):
        return validate_capsule(self.capsule, sha or self.sha, manifest=self.lock)

    def test_frozen_inventory_and_page_bytes_are_unchanged(self):
        report = self.validate()
        self.assertEqual(report['inventory_artifacts'], 1)
        self.assertEqual(report['published_pages'], 1)
        self.assertFalse(report['semantic_review_performed'])
        self.assertFalse(report['remote_custody_verified'])
        self.assertEqual((self.capsule / 'corpus/published-page-ledger.json').read_bytes(),
                         (self.corpus / 'published-page-ledger.json').read_bytes())

    def test_mismatched_trusted_fingerprint_rejected(self):
        with self.assertRaises(ValueError):
            self.validate('0' * 64)

    def test_changed_payload_rejected(self):
        (self.capsule / 'corpus/candidates.jsonl').write_text('{}\n')
        with self.assertRaises(ValueError):
            self.validate()

    def test_extra_file_rejected(self):
        (self.capsule / 'secret.txt').write_text('not a metadata input')
        with self.assertRaises(ValueError):
            self.validate()

    def test_symlink_payload_rejected(self):
        target = self.capsule / 'corpus/candidates.jsonl'
        target.unlink()
        target.symlink_to(self.corpus / 'candidates.jsonl')
        with self.assertRaises(ValueError):
            self.validate()

    def test_cannot_overwrite_capsule_or_worker_output(self):
        with self.assertRaises(FileExistsError):
            freeze(self.sources, self.corpus, self.capsule, manifest=self.lock)
        output = self.root / 'worker'
        output.mkdir()
        with self.assertRaises(FileExistsError):
            hydrate(self.capsule, self.sha, self.partition, output, manifest=self.lock)

    def test_source_only_hydration_does_not_fetch_page_lists(self):
        output = self.root / 'worker'
        with patch('ges.frozen_inputs.fetch', return_value=self.archive) as fetch:
            report = hydrate(self.capsule, self.sha, self.partition, output, manifest=self.lock)
        self.assertEqual(fetch.call_count, 1)
        self.assertEqual(fetch.call_args.args[0], 'https://codeload.github.com/owner/repo/tar.gz/' + 'a' * 40)
        self.assertEqual(report['assigned_artifacts'], 1)
        self.assertFalse(report['provider_dispatched'])
        self.assertEqual((output / 'sources/owner__repo.inventory.json').read_bytes(),
                         (self.sources / 'owner__repo.inventory.json').read_bytes())
        with gzip.open(output / 'sources/owner__repo.text.jsonl.gz', 'rt') as stream:
            row = json.loads(stream.readline())
        self.assertEqual(row['retrieved_at'], self.artifact['retrieved_at'])
        self.assertEqual(row['content'], self.content.decode())

    def test_bad_archive_rejected_without_publishing_output(self):
        output = self.root / 'worker'
        with patch('ges.frozen_inputs.fetch', return_value=b'changed'):
            with self.assertRaises(ValueError):
                hydrate(self.capsule, self.sha, self.partition, output, manifest=self.lock)
        self.assertFalse(output.exists())

    def test_duplicate_or_unknown_partition_rejected_before_network(self):
        for ids in [[self.artifact['artifact_id']] * 2, ['unknown'], []]:
            with self.subTest(ids=ids), patch('ges.frozen_inputs.fetch') as fetch:
                partition = {**self.partition, 'artifact_ids': ids}
                with self.assertRaises(ValueError):
                    hydrate(self.capsule, self.sha, partition, self.root / 'worker', manifest=self.lock)
                fetch.assert_not_called()

    def test_partition_cannot_switch_capsule(self):
        with self.assertRaises(ValueError):
            hydrate(self.capsule, self.sha, {**self.partition, 'capsule_sha256': '0' * 64},
                    self.root / 'worker', manifest=self.lock)

    def test_lock_change_rejected(self):
        lock = copy.deepcopy({'sources': [self.spec]})
        lock['sources'][0]['commit'] = 'b' * 40
        dump(self.lock, lock)
        with self.assertRaises(ValueError):
            self.validate()

    def test_restricted_text_cannot_enter_metadata_capsule(self):
        record = {'artifact_id': self.artifact['artifact_id'], 'candidate_id': 'example',
                  'text': 'Upstream expression must remain outside the transport metadata.'}
        (self.corpus / 'candidates.jsonl').write_text(json.dumps(record) + '\n')
        with self.assertRaises(ValueError):
            freeze(self.sources, self.corpus, self.root / 'restricted', manifest=self.lock)

    def test_nested_rendered_body_cannot_enter_metadata_capsule(self):
        dump(self.corpus / 'published-page-ledger.json', [{'page_id': 'page-one',
             'path': '/en/example', 'version': 'free-pro-team@latest',
             'source_matches': [{'body': 'restricted upstream body'}]}])
        with self.assertRaises(ValueError):
            freeze(self.sources, self.corpus, self.root / 'nested', manifest=self.lock)

    def test_tree_payload_cannot_transport_restricted_text(self):
        dump(self.sources / 'owner__repo.tree-reconciliation.json', {'status': 'MATCH',
             'text': 'restricted upstream text'})
        with self.assertRaises(ValueError):
            freeze(self.sources, self.corpus, self.root / 'tree', manifest=self.lock)

    def test_reduced_inventory_cannot_be_frozen(self):
        (self.corpus / 'artifacts.jsonl').write_text('')
        with self.assertRaises(ValueError):
            freeze(self.sources, self.corpus, self.root / 'reduced', manifest=self.lock)


if __name__ == '__main__':
    unittest.main()
