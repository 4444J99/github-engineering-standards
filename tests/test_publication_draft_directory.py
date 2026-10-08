"""Draft metadata must never change the candidate it has just inventoried."""
from contextlib import redirect_stdout
from io import StringIO
import json
import os
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from ges.publication_use import main, output_inventory, prepare_draft


class PublicationDraftDirectory(unittest.TestCase):
    def setUp(self):
        temporary = TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.candidate = self.root / 'candidate'
        self.candidate.mkdir()
        (self.candidate / 'release.txt').write_text('Original synthetic output.\n', encoding='utf-8')

    def run_draft(self, destination, *, candidate=None):
        args = ['prepare-draft', '--output-root', str(candidate or self.candidate),
                '--draft-directory', str(destination), '--candidate-id', 'synthetic-path-test',
                '--candidate-revision', 'b' * 40, '--distribution-scope', 'Synthetic path test only']
        stdout = StringIO()
        with redirect_stdout(stdout):
            result = main(args)
        return result, json.loads(stdout.getvalue())

    def assert_rejected_before_inventory(self, destination, *, candidate=None, error):
        before = output_inventory(self.candidate)
        before_paths = sorted(path.relative_to(self.root).as_posix() for path in self.root.rglob('*'))
        with patch('ges.publication_use.output_inventory',
                   side_effect=AssertionError('Candidate must not be inventoried for an invalid destination')) as observe:
            result, report = self.run_draft(destination, candidate=candidate)
        observe.assert_not_called()
        self.assertEqual(result, 2)
        self.assertFalse(report['valid'])
        self.assertIn(error, report['error'])
        self.assertEqual(output_inventory(self.candidate), before)
        self.assertEqual(sorted(path.relative_to(self.root).as_posix() for path in self.root.rglob('*')),
                         before_paths)

    def test_equal_or_descendant_destination_rejected_before_inventory_or_writes(self):
        for destination in [self.candidate, self.candidate / 'draft',
                            self.candidate / 'new-parent' / 'draft']:
            with self.subTest(destination=destination):
                self.assert_rejected_before_inventory(destination, error='outside the candidate output root')
        self.assertFalse((self.candidate / 'new-parent').exists())

    def test_relative_and_normalized_descendants_rejected_before_inventory_or_writes(self):
        for destination in [Path(os.path.relpath(self.candidate / 'draft')),
                            self.candidate / '..' / 'candidate' / 'new-parent' / 'draft']:
            with self.subTest(destination=destination):
                self.assert_rejected_before_inventory(
                    destination, candidate=Path(os.path.relpath(self.candidate)),
                    error='outside the candidate output root')
        self.assertFalse((self.candidate / 'new-parent').exists())

    def test_symlink_alias_to_candidate_rejected_before_inventory_or_writes(self):
        alias = self.root / 'candidate-alias'
        alias.symlink_to(self.candidate, target_is_directory=True)
        self.assert_rejected_before_inventory(alias / 'new-parent' / 'draft',
                                              error='Symlink draft directory')
        self.assertFalse((self.candidate / 'new-parent').exists())

    def test_symlink_alias_as_output_root_rejected_before_inventory_or_writes(self):
        alias = self.root / 'candidate-alias'
        alias.symlink_to(self.candidate, target_is_directory=True)
        self.assert_rejected_before_inventory(self.root / 'draft', candidate=alias,
                                              error='Symlink output root')
        self.assertFalse((self.root / 'draft').exists())

    def test_dangling_symlink_destination_rejected_before_inventory_or_writes(self):
        destination = self.root / 'draft'
        destination.symlink_to(self.candidate / 'new-parent', target_is_directory=True)
        self.assert_rejected_before_inventory(destination, error='Symlink draft directory')
        self.assertTrue(destination.is_symlink())
        self.assertFalse((self.candidate / 'new-parent').exists())

    def test_disjoint_sibling_metadata_preserves_exact_candidate_inventory(self):
        before = output_inventory(self.candidate)
        destination = self.root / 'review' / 'draft'
        result, report = self.run_draft(Path(os.path.relpath(destination)),
                                        candidate=Path(os.path.relpath(self.candidate)))
        self.assertEqual(result, 0)
        self.assertTrue(report['draft_prepared'])
        self.assertEqual(report['output_count'], 1)
        self.assertIsNone(report['clearance'])
        manifest = json.loads((destination / 'manifest.json').read_text())
        self.assertEqual(manifest['outputs'], before)
        self.assertEqual(output_inventory(self.candidate), before)
        self.assertEqual(sorted(path.name for path in destination.iterdir()),
                         ['manifest.json', 'policy.json', 'receipts.json', 'register.json'])
        self.assertEqual(json.loads((destination / 'receipts.json').read_text()), [])
        self.assertEqual(json.loads((destination / 'policy.json').read_text()), {})
        register = json.loads((destination / 'register.json').read_text())
        self.assertEqual([row['disposition'] for row in register['outputs']], ['UNREVIEWED'])

    def test_destination_parent_change_during_inventory_rejected_before_writes(self):
        parent = self.root / 'review'
        parent.mkdir()
        destination = parent / 'draft'

        def change_parent(*args, **kwargs):
            draft = prepare_draft(*args, **kwargs)
            parent.rmdir()
            parent.symlink_to(self.candidate, target_is_directory=True)
            return draft

        with patch('ges.publication_use.prepare_draft', side_effect=change_parent):
            result, report = self.run_draft(destination)
        self.assertEqual(result, 2)
        self.assertIn('Symlink draft directory', report['error'])
        self.assertFalse((self.candidate / 'draft').exists())
        self.assertEqual([row['path'] for row in output_inventory(self.candidate)], ['release.txt'])


if __name__ == '__main__':
    unittest.main()
