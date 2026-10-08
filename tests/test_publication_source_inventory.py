"""Adversarial publication provenance checks; all approvals here are synthetic."""
import contextlib
import copy
import gzip
import hashlib
import io
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from ges.core import ROOT, digest
from ges.pinned_sources import inventory_digest
from ges.publication_use import main, prepare_draft, publication_accounting
from test_publication_use import bind_approvals, create_fixture


REFERENCE = ROOT / 'evidence/a3-six-source-capsule-repair.json'
REFERENCE_SHA256 = '05dab95bfbc88c2401a97da702339f4f1be89545c8f8c9f48198194aac07bb15'
REPOSITORY = 'tmcw/github-best-practices'
COMMIT = '801411757531a8880cb315148160fde3079d7227'


def relink_source(fixture, row):
    """Keep attack data internally consistent without altering source authority."""
    previous = fixture['register']['uses'][0]['source']['artifact_id']
    row['artifact_id'] = digest([row['source'], row['commit'], row['path']])[:24]
    for use in fixture['register']['uses']:
        if use['source']['artifact_id'] == previous:
            use['source'] = {key: row[key] for key in
                             ('artifact_id', 'source', 'commit', 'path', 'sha256')}
    for reference in fixture['register']['source_evidence']:
        if reference['artifact_id'] == previous:
            reference['artifact_id'] = row['artifact_id']


def set_source_bytes(fixture, row, raw, source_format):
    row.update(sha256=hashlib.sha256(raw).hexdigest(), kind='text', size=len(raw),
               git_blob_sha=hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest())
    relink_source(fixture, row)
    reference = fixture['register']['source_evidence'][0]
    if source_format == 'RAW':
        path = fixture['source_root'] / 'source.txt'
        path.write_bytes(raw)
    else:
        path = fixture['source_root'] / (row['source'].replace('/', '__') + '.text.jsonl.gz')
        with gzip.open(path, 'wt', encoding='utf-8') as stream:
            stream.write(json.dumps({**row, 'content': raw.decode('utf-8')}) + '\n')
    reference.update(format=source_format, path=path.name,
                     sha256=hashlib.sha256(path.read_bytes()).hexdigest())


class PublicationSourceInventory(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with gzip.open(ROOT / 'evidence/claim-workload-inputs/artifacts.jsonl.gz',
                       'rt', encoding='utf-8') as stream:
            cls.current_artifacts = [json.loads(line) for line in stream if line.strip()]
        cls.current_pins = {row['repository']: row['commit'] for row in
                            json.loads((ROOT / 'sources/sources.lock.json').read_text())['sources']}

    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def official_forgery(self, directory, source_format='RAW', *, existing_path=False):
        fixture = create_fixture(directory)
        row = fixture['artifacts'][0]
        if existing_path:
            row.clear()
            row.update(copy.deepcopy(next(item for item in self.current_artifacts
                                           if item['source'] == REPOSITORY)))
        else:
            row.update(source=REPOSITORY, commit=COMMIT,
                       path='fabricated-file-not-in-locked-inventory.md')
        # Synthetic approval dates are intentionally independent of real acquisition dates.
        row['retrieved_at'] = '2026-01-01T00:00:00Z'
        fixture['pins'] = {REPOSITORY: COMMIT}
        raw = (fixture['source_root'] / 'source.txt').read_bytes()
        set_source_bytes(fixture, row, raw, source_format)
        fixture.update(source_inventory_reference=REFERENCE,
                       source_inventory_sha256=REFERENCE_SHA256)
        return bind_approvals(fixture)

    def default_accounting(self, fixture):
        arguments = dict(fixture)
        arguments.pop('source_inventory_reference', None)
        arguments.pop('source_inventory_sha256', None)
        return publication_accounting(**arguments)

    def current_draft(self):
        fixture = create_fixture(self.root)
        draft = prepare_draft(fixture['output_root'], 'current-metadata-check', 'b' * 40,
                              'Synthetic unreviewed output; no publication authorized',
                              prepared_at='2026-01-02T00:00:00Z')
        return {**fixture, **draft, 'artifacts': copy.deepcopy(self.current_artifacts),
                'pins': dict(self.current_pins)}

    def test_default_anchor_rejects_canonical_fabricated_raw_and_snapshot_rows(self):
        for source_format in ('RAW', 'SNAPSHOT_TEXT'):
            with self.subTest(source_format=source_format):
                fixture = self.official_forgery(self.root / source_format, source_format)
                row = fixture['artifacts'][0]
                self.assertEqual(row['artifact_id'],
                                 digest([REPOSITORY, COMMIT, row['path']])[:24])
                with self.assertRaises(ValueError):
                    self.default_accounting(fixture)

    def test_default_anchor_rejects_changed_bytes_at_an_existing_real_path(self):
        for source_format in ('RAW', 'SNAPSHOT_TEXT'):
            with self.subTest(source_format=source_format):
                fixture = self.official_forgery(self.root / source_format, source_format,
                                                existing_path=True)
                original = next(row for row in self.current_artifacts
                                if row['source'] == REPOSITORY)
                self.assertEqual(fixture['artifacts'][0]['artifact_id'], original['artifact_id'])
                self.assertEqual(fixture['artifacts'][0]['path'], original['path'])
                self.assertNotEqual(fixture['artifacts'][0]['sha256'], original['sha256'])
                with self.assertRaises(ValueError):
                    self.default_accounting(fixture)

    def test_standalone_cli_rejects_fabrication_using_its_default_anchor(self):
        fixture = self.official_forgery(self.root)
        arguments = []
        for name in ('manifest', 'register', 'receipts', 'policy'):
            path = self.root / (name + '.json')
            path.write_text(json.dumps(fixture[name]), encoding='utf-8')
            arguments.extend(['--' + name, str(path)])
        artifacts = self.root / 'artifacts.jsonl'
        artifacts.write_text(json.dumps(fixture['artifacts'][0]) + '\n', encoding='utf-8')
        pins = self.root / 'pins.json'
        pins.write_text(json.dumps({'sources': [{'repository': REPOSITORY, 'commit': COMMIT}]}),
                        encoding='utf-8')
        arguments.extend(['--artifacts', str(artifacts), '--pins', str(pins),
                          '--output-root', str(fixture['output_root']),
                          '--source-root', str(fixture['source_root']),
                          '--evidence-root', str(fixture['evidence_root'])])
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = main(arguments)
        self.assertEqual(code, 2)
        report = json.loads(output.getvalue())
        self.assertIs(report['valid'], False)
        self.assertIsNot(report.get('exact_use_clearance'), True)

    def test_alternate_cli_authority_requires_reference_and_independent_fingerprint_together(self):
        fixture = create_fixture(self.root)
        arguments = []
        for name in ('manifest', 'register', 'receipts', 'policy'):
            path = self.root / (name + '.json')
            path.write_text(json.dumps(fixture[name]), encoding='utf-8')
            arguments.extend(['--' + name, str(path)])
        artifacts = self.root / 'artifacts.jsonl'
        artifacts.write_text(json.dumps(fixture['artifacts'][0]) + '\n', encoding='utf-8')
        pins = self.root / 'pins.json'
        pins.write_text(json.dumps({'sources': [
            {'repository': repository, 'commit': commit}
            for repository, commit in fixture['pins'].items()]}), encoding='utf-8')
        arguments.extend(['--artifacts', str(artifacts), '--pins', str(pins),
                          '--output-root', str(fixture['output_root']),
                          '--source-root', str(fixture['source_root']),
                          '--evidence-root', str(fixture['evidence_root'])])
        expected_fingerprint = fixture['source_inventory_sha256']
        reference = ['--source-inventory-reference', str(fixture['source_inventory_reference'])]
        fingerprint = ['--source-inventory-sha256', expected_fingerprint]
        for supplied, extra in [('both', reference + fingerprint),
                                ('reference_only', reference),
                                ('fingerprint_only', fingerprint)]:
            with self.subTest(supplied=supplied):
                output = io.StringIO()
                with contextlib.redirect_stdout(output):
                    code = main(arguments + extra)
                report = json.loads(output.getvalue())
                if supplied == 'both':
                    self.assertEqual(code, 0)
                    self.assertIs(report['valid'], True)
                    self.assertIs(report['exact_use_clearance'], True)
                    self.assertEqual(report['source_inventory_reference_digest'], expected_fingerprint)
                else:
                    self.assertEqual(code, 2)
                    self.assertIs(report['valid'], False)
                    self.assertIn('supplied together', report['error'])
                    self.assertIsNot(report.get('exact_use_clearance'), True)

    def test_current_complete_metadata_matches_default_anchor_without_clearance(self):
        fixture = self.current_draft()
        self.assertEqual(len(fixture['artifacts']), 13657)
        result = self.default_accounting(fixture)
        self.assertEqual(result['source_inventory_reference_digest'], REFERENCE_SHA256)
        self.assertIs(result['complete_output_inventory'], True)
        self.assertEqual(result['unreviewed_output_count'], 1)
        self.assertIsNone(result['exact_use_clearance'])
        self.assertIs(result['zero_use_clearance'], False)

    def test_missing_artifact_or_whole_declared_source_does_not_shrink_inventory(self):
        fixture = self.current_draft()
        for removed in ('one_artifact', 'whole_source'):
            with self.subTest(removed=removed):
                artifacts = copy.deepcopy(self.current_artifacts)
                if removed == 'one_artifact':
                    artifacts.pop(next(index for index, row in enumerate(artifacts)
                                       if row['source'] == 'github/docs'))
                else:
                    artifacts = [row for row in artifacts if row['source'] != REPOSITORY]
                with self.assertRaises(ValueError):
                    self.default_accounting({**fixture, 'artifacts': artifacts})

    def test_changed_pin_or_unrecognized_source_cannot_rebind_approval(self):
        for changed in ('pin', 'source'):
            with self.subTest(changed=changed):
                fixture = create_fixture(self.root / changed)
                row = fixture['artifacts'][0]
                if changed == 'pin':
                    row['commit'] = 'c' * 40
                else:
                    row['source'] = 'test/unrecognized-source'
                fixture['pins'] = {row['source']: row['commit']}
                relink_source(fixture, row)
                bind_approvals(fixture)
                with self.assertRaises(ValueError):
                    publication_accounting(**fixture)

    def test_artifact_id_must_be_canonical_even_when_content_projection_matches(self):
        fixture = create_fixture(self.root)
        fixture['artifacts'][0]['artifact_id'] = '0' * 24
        fixture['register']['uses'][0]['source']['artifact_id'] = '0' * 24
        fixture['register']['source_evidence'][0]['artifact_id'] = '0' * 24
        bind_approvals(fixture)
        with self.assertRaises(ValueError):
            publication_accounting(**fixture)

    def test_forged_anchor_cannot_replace_the_independent_expected_fingerprint(self):
        fixture = create_fixture(self.root)
        expected = fixture['source_inventory_sha256']
        row = fixture['artifacts'][0]
        row['path'] = 'fabricated.md'
        relink_source(fixture, row)
        path = fixture['source_inventory_reference']
        anchor = json.loads(path.read_text())
        forged_digest = inventory_digest(fixture['artifacts'])
        anchor['inventory_identity_digests'][row['source']] = forged_digest
        anchor['source_trees'][row['source']]['inventory_digest'] = forged_digest
        path.write_text(json.dumps(anchor), encoding='utf-8')
        self.assertNotEqual(hashlib.sha256(path.read_bytes()).hexdigest(), expected)
        bind_approvals(fixture)
        self.assertEqual(fixture['source_inventory_sha256'], expected)
        with self.assertRaises(ValueError):
            publication_accounting(**fixture)

    def test_changed_valid_anchor_fingerprint_requires_new_approval_scope(self):
        fixture = create_fixture(self.root)
        self.assertIs(publication_accounting(**fixture)['exact_use_clearance'], True)
        path = fixture['source_inventory_reference']
        path.write_bytes(path.read_bytes() + b'\n')
        fixture['source_inventory_sha256'] = hashlib.sha256(path.read_bytes()).hexdigest()
        with self.assertRaises(ValueError):
            publication_accounting(**fixture)
        bind_approvals(fixture)
        self.assertIs(publication_accounting(**fixture)['exact_use_clearance'], True)

    def test_anchor_symlink_and_change_during_validation_are_rejected(self):
        fixture = create_fixture(self.root)
        original_path = fixture['source_inventory_reference']
        link = self.root / 'anchor-link.json'
        link.symlink_to(original_path)
        with self.assertRaises(ValueError):
            publication_accounting(**{**fixture, 'source_inventory_reference': link})
        from ges.publication_use import _evidence
        changed = False

        def mutate_anchor_after_read(root, reference):
            nonlocal changed
            document = _evidence(root, reference)
            if not changed:
                original_path.write_bytes(original_path.read_bytes() + b'\n')
                changed = True
            return document

        with patch('ges.publication_use._evidence', side_effect=mutate_anchor_after_read):
            with self.assertRaises(ValueError):
                publication_accounting(**fixture)
        self.assertTrue(changed)

    def test_new_acquisition_time_preserves_anchored_content_identity(self):
        fixture = create_fixture(self.root)
        expected = fixture['source_inventory_sha256']
        fixture['artifacts'][0]['retrieved_at'] = '2026-01-02T00:00:00Z'
        bind_approvals(fixture)
        result = publication_accounting(**fixture)
        self.assertEqual(result['source_inventory_reference_digest'], expected)
        self.assertIs(result['exact_use_clearance'], True)


if __name__ == '__main__':
    unittest.main()
