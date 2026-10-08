"""Exercise platform alias policy without changing real system directories."""
from contextlib import ExitStack, redirect_stdout
from io import StringIO
import json
import os
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from ges.evidence_paths import canonical_path
from ges.publication_use import main, output_inventory


class EvidencePaths(unittest.TestCase):
    def setUp(self):
        temporary = TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve()
        self.target = self.root / 'private' / 'var'
        self.target.mkdir(parents=True)
        self.alias = self.root / 'var'
        self.alias.symlink_to(Path('private/var'), target_is_directory=True)
        self.candidate = self.target / 'candidate'
        self.candidate.mkdir()
        (self.candidate / 'output.txt').write_text('Synthetic output.\n', encoding='utf-8')

    def policy(self, *, platform='darwin', owner=0, expected=None):
        stack = ExitStack()
        real_lstat = Path.lstat

        def ownership(path, *args, **kwargs):
            result = real_lstat(path, *args, **kwargs)
            if path == self.alias:
                fields = list(result)
                fields[4] = owner
                return os.stat_result(fields)
            return result

        stack.enter_context(patch('ges.evidence_paths.sys.platform', platform))
        stack.enter_context(patch('ges.evidence_paths._DARWIN_SYSTEM_ALIASES',
                                  {self.alias: expected or self.target}))
        stack.enter_context(patch.object(Path, 'lstat', ownership))
        return stack

    def run_draft(self, destination):
        stdout = StringIO()
        with redirect_stdout(stdout):
            result = main(['prepare-draft', '--output-root', str(self.alias / 'candidate'),
                           '--draft-directory', str(destination), '--candidate-id', 'alias-policy-test',
                           '--candidate-revision', 'b' * 40,
                           '--distribution-scope', 'Synthetic alias policy test only'])
        return result, json.loads(stdout.getvalue())

    def test_trusted_system_alias_supports_real_candidate_and_sibling_draft(self):
        before = output_inventory(self.candidate)
        with self.policy():
            result, report = self.run_draft(self.alias / 'review' / 'draft')
        self.assertEqual(result, 0)
        self.assertTrue(report['draft_prepared'])
        self.assertIsNone(report['clearance'])
        manifest = json.loads((self.target / 'review' / 'draft' / 'manifest.json').read_text())
        self.assertEqual(manifest['outputs'], before)
        self.assertEqual(output_inventory(self.candidate), before)

    def test_absolute_or_relative_exact_system_link_targets_resolve(self):
        for target in (Path('private/var'), self.target):
            with self.subTest(target=target):
                self.alias.unlink()
                self.alias.symlink_to(target, target_is_directory=True)
                with self.policy():
                    self.assertEqual(canonical_path(self.alias / 'new', symlink_error='blocked'),
                                     self.target / 'new')

    def test_equal_or_nested_draft_through_system_alias_still_rejected_before_inventory(self):
        for destination in (self.alias / 'candidate', self.alias / 'candidate' / 'draft'):
            with self.subTest(destination=destination), self.policy():
                with patch('ges.publication_use.output_inventory') as observe:
                    result, report = self.run_draft(destination)
                observe.assert_not_called()
                self.assertEqual(result, 2)
                self.assertIn('outside the candidate output root', report['error'])
        self.assertFalse((self.candidate / 'draft').exists())

    def test_non_darwin_system_alias_is_not_exempted(self):
        with self.policy(platform='linux'), self.assertRaisesRegex(ValueError, 'blocked'):
            canonical_path(self.alias / 'candidate', symlink_error='blocked')

    def test_nonroot_owned_system_alias_is_not_exempted(self):
        with self.policy(owner=501), self.assertRaisesRegex(ValueError, 'blocked'):
            canonical_path(self.alias / 'candidate', symlink_error='blocked')

    def test_system_alias_with_changed_target_is_not_exempted(self):
        other = self.root / 'other'
        other.mkdir()
        with self.policy(expected=other), self.assertRaisesRegex(ValueError, 'blocked'):
            canonical_path(self.alias / 'candidate', symlink_error='blocked')

    def test_caller_alias_below_trusted_system_directory_is_rejected(self):
        caller_alias = self.target / 'caller-alias'
        caller_alias.symlink_to(self.candidate, target_is_directory=True)
        with self.policy(), self.assertRaisesRegex(ValueError, 'blocked'):
            canonical_path(self.alias / 'caller-alias' / 'output.txt', symlink_error='blocked')

    def test_trusted_alias_target_cannot_have_another_symlink_ancestor(self):
        redirect = self.root / 'redirect'
        redirect.symlink_to(self.target.parent, target_is_directory=True)
        expected = redirect / 'var'
        self.alias.unlink()
        self.alias.symlink_to(expected, target_is_directory=True)
        with self.policy(expected=expected), self.assertRaisesRegex(ValueError, 'blocked'):
            canonical_path(self.alias / 'candidate', symlink_error='blocked')


if __name__ == '__main__':
    unittest.main()
