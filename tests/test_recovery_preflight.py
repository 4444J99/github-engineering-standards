"""Incomplete recovery caches fail before expensive review/source accounting."""
import json
import os
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from ges.recovery import preflight_recovery_inputs, status


class RecoveryPreflight(unittest.TestCase):
    def setUp(self):
        temporary = TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve()
        self.sources = self.root / 'sources'
        self.corpus = self.root / 'corpus'
        self.sources.mkdir()
        self.corpus.mkdir()
        self.pins = [{'repository': 'example/docs', 'commit': 'a' * 40}]
        (self.sources / 'sources.lock.json').write_text(json.dumps({'sources': self.pins}))

    def complete_metadata(self):
        # Contents are not interpreted by the preflight; downstream validators
        # remain responsible for provenance and accounting.
        for name in ('artifacts.jsonl', 'candidates.jsonl', 'ledger-summary.json',
                     'structured-source-requirements.json', 'published-page-ledger.json'):
            (self.corpus / name).write_text('')
        for suffix in ('inventory.json', 'tree-reconciliation.json'):
            (self.sources / ('example__docs.' + suffix)).write_text('{}')

    def test_source_only_cache_lists_all_missing_corpus_inputs_before_catalog_load(self):
        for suffix in ('inventory.json', 'tree-reconciliation.json', 'text.jsonl.gz'):
            (self.sources / ('example__docs.' + suffix)).write_text('{}')
        # No catalog exists. The useful cache error must precede catalog access
        # and candidate/review processing, rather than fail one file at a time.
        with patch('ges.recovery.ROOT', self.root), self.assertRaises(ValueError) as caught:
            status(self.sources, self.corpus)
        message = str(caught.exception)
        for name in ('artifacts.jsonl', 'candidates.jsonl', 'ledger-summary.json',
                     'structured-source-requirements.json', 'published-page-ledger.json'):
            self.assertIn('corpus/' + name, message)
        self.assertIn('source-only claim-provenance cache is insufficient', message)
        self.assertEqual(list(self.corpus.iterdir()), [])

    def test_missing_candidate_and_directory_in_place_of_page_ledger_are_aggregated(self):
        self.complete_metadata()
        (self.corpus / 'candidates.jsonl').unlink()
        pages = self.corpus / 'published-page-ledger.json'
        pages.unlink()
        pages.mkdir()
        with self.assertRaises(ValueError) as caught:
            preflight_recovery_inputs(self.sources, self.corpus, self.pins)
        self.assertIn('corpus/candidates.jsonl', str(caught.exception))
        self.assertIn('corpus/published-page-ledger.json', str(caught.exception))

    def test_candidate_symlink_and_symlinked_corpus_directory_are_rejected(self):
        self.complete_metadata()
        candidate = self.corpus / 'candidates.jsonl'
        target = self.root / 'candidate-target.jsonl'
        target.write_text('')
        candidate.unlink()
        candidate.symlink_to(target)
        with self.assertRaisesRegex(ValueError, r'corpus/candidates.jsonl \(symlink\)'):
            preflight_recovery_inputs(self.sources, self.corpus, self.pins)
        candidate.unlink()
        candidate.write_text('')
        alias = self.root / 'corpus-alias'
        alias.symlink_to(self.corpus, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, r'corpus/artifacts.jsonl \(symlink\)'):
            preflight_recovery_inputs(self.sources, alias, self.pins)

    def test_metadata_only_recovery_does_not_require_snapshots_or_nonempty_candidates(self):
        self.complete_metadata()
        preflight_recovery_inputs(self.sources, self.corpus, self.pins)
        self.assertFalse((self.sources / 'example__docs.text.jsonl.gz').exists())

    def test_trusted_darwin_directory_alias_uses_existing_exact_target_policy(self):
        self.complete_metadata()
        alias = self.root / 'system-var'
        alias.symlink_to(self.root, target_is_directory=True)
        real_lstat = Path.lstat

        def root_owned_alias(path, *args, **kwargs):
            result = real_lstat(path, *args, **kwargs)
            if path == alias:
                fields = list(result)
                fields[4] = 0
                return os.stat_result(fields)
            return result

        with (patch('ges.evidence_paths.sys.platform', 'darwin'),
              patch('ges.evidence_paths._DARWIN_SYSTEM_ALIASES', {alias: self.root}),
              patch.object(Path, 'lstat', root_owned_alias)):
            preflight_recovery_inputs(alias / 'sources', alias / 'corpus', self.pins)
            # Trust for the system directory never extends to caller symlinks
            # beneath it, or to the same alias with an unexpected target.
            caller_alias = self.root / 'caller-corpus'
            caller_alias.symlink_to(self.corpus, target_is_directory=True)
            with self.assertRaisesRegex(ValueError, r'corpus/artifacts.jsonl \(symlink\)'):
                preflight_recovery_inputs(alias / 'sources', alias / 'caller-corpus', self.pins)
            with patch('ges.evidence_paths._DARWIN_SYSTEM_ALIASES', {alias: self.sources}):
                with self.assertRaisesRegex(ValueError, r'corpus/artifacts.jsonl \(symlink\)'):
                    preflight_recovery_inputs(alias / 'sources', alias / 'corpus', self.pins)

    def test_claim_documents_require_snapshot_before_review_or_catalog_processing(self):
        self.complete_metadata()
        reviews = self.root / 'reviews'
        reviews.mkdir()
        (reviews / 'source-claims.json').write_text('{}')
        policy = self.root / 'review-policy.json'
        policy.write_text('{}')
        with (patch('ges.recovery.ROOT', self.root),
              self.assertRaisesRegex(ValueError, r'sources/example__docs.text.jsonl.gz')):
            status(self.sources, self.corpus, reviews=reviews, review_policy=policy)

    def test_optional_argument_pair_errors_still_precede_cache_access(self):
        with self.assertRaisesRegex(ValueError, 'both receipts and authority policy'):
            status(self.sources, self.corpus, reviews=self.root / 'absent-reviews')


if __name__ == '__main__':
    unittest.main()
