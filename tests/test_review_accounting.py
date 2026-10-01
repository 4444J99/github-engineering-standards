"""Regression contracts for truthful review and source-change accounting."""
import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from ges.core import ROOT, load, validate_controls
from ges.corpus import coverage_with_reviews, impact
from ges.__main__ import main


class ReviewAccounting(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.control = copy.deepcopy(load(ROOT/'controls/catalog.json')[0])
        self.source = self.control['sources'][0]
        self.artifact = {'artifact_id': 'artifact', 'source': self.source['repository'],
                         'commit': self.source['commit'], 'path': self.source['path'],
                         'sha256': self.source['content_sha256']}
        self.candidate = {'candidate_id': 'candidate', 'artifact_id': 'artifact', 'text_sha256': 'a'*64}
        self.review = {'artifact_id': 'artifact', 'commit': self.source['commit'],
                       'content_sha256': self.source['content_sha256'], 'reviewer': 'reviewer',
                       'reviewed_at': '2026-10-01T00:00:00Z', 'rationale': 'Reviewed full artifact',
                       'disposition': 'CONTROL_SOURCE', 'all_claims_accounted_for': True,
                       'claim_mappings': [{'candidate_id': 'candidate', 'text_sha256': 'a'*64,
                                           'disposition': 'CONTROL', 'control_id': self.control['id'],
                                           'control_revision': self.control['revision']}]}

    def coverage(self, reviews):
        artifacts = self.root/'artifacts.jsonl'
        artifacts.write_text(json.dumps(self.artifact)+'\n')
        receipts = self.root/'reviews.json'
        receipts.write_text(json.dumps(reviews))
        return coverage_with_reviews(artifacts, receipts, candidates=[self.candidate],
                                     controls=[self.control], authorized_reviewers=['reviewer'])

    def test_valid_full_accounting(self):
        self.assertEqual(self.coverage([self.review])['reviewed'], 1)

    def test_invalid_mapping_never_counts(self):
        self.review['claim_mappings'] = ['GES-BOGUS-001']
        self.assertEqual(self.coverage([self.review])['reviewed'], 0)

    def test_unaccounted_candidate_never_counts(self):
        self.review['disposition'] = 'REFERENCE_ONLY'
        self.review['claim_mappings'] = []
        self.assertEqual(self.coverage([self.review])['reviewed'], 0)

    def test_foreign_reviewer_never_counts(self):
        self.review['reviewer'] = 'stranger'
        self.assertEqual(self.coverage([self.review])['reviewed'], 0)

    def test_invalid_timestamp_never_counts(self):
        self.review['reviewed_at'] = 'not a timestamp'
        self.assertEqual(self.coverage([self.review])['reviewed'], 0)

    def test_duplicate_receipt_never_counts(self):
        self.assertEqual(self.coverage([self.review, self.review])['reviewed'], 0)

    def test_wrong_control_revision_never_counts(self):
        self.review['claim_mappings'][0]['control_revision'] += 1
        self.assertEqual(self.coverage([self.review])['reviewed'], 0)

    def test_changed_commit_without_changed_content_is_not_modification(self):
        old, new = self.root/'old.jsonl', self.root/'new.jsonl'
        old.write_text(json.dumps(self.artifact)+'\n')
        newer = dict(self.artifact, commit='b'*40)
        new.write_text(json.dumps(newer)+'\n')
        self.assertEqual(impact(old,new,[self.control])['changes'], [])
        newer['sha256'] = 'c'*64
        new.write_text(json.dumps(newer)+'\n')
        self.assertEqual(impact(old,new,[self.control])['changes'][0]['reopen_controls'], [self.control['id']])

    def test_provenance_requires_hash_and_ordered_span(self):
        for key, value in [('content_sha256', ''), ('start_line', 0), ('end_line', 1)]:
            c = copy.deepcopy(self.control)
            c['sources'][0][key] = value
            self.assertTrue(validate_controls([c]))

    def test_page_acquisition_failure_is_nonzero(self):
        report = {'sources': [{'status': 'SNAPSHOT_RETRIEVED', 'git_tree_reconciliation': {'status': 'MATCH'}}],
                  'published_docs': {'status': 'ERROR'}}
        with patch('ges.sources.sync',return_value=report):
            self.assertEqual(main(['sync','--output',str(self.root)]), 2)

    def test_changed_fragment_reopens_transitive_parent_control(self):
        old,new,deps=self.root/'old.jsonl',self.root/'new.jsonl',self.root/'dependencies.jsonl'
        rows=[dict(self.artifact),dict(self.artifact,artifact_id='fragment',path='fragment.md'),
              dict(self.artifact,artifact_id='nested',path='nested.md')]
        old.write_text(''.join(json.dumps(r)+'\n' for r in rows))
        rows[-1]['sha256']='c'*64
        new.write_text(''.join(json.dumps(r)+'\n' for r in rows))
        deps.write_text('\n'.join(json.dumps(r) for r in [
            {'artifact_id':'artifact','resolved_artifact_ids':['fragment']},
            {'artifact_id':'fragment','resolved_artifact_ids':['nested']},
            {'artifact_id':'nested','resolved_artifact_ids':['fragment']}]))
        report=impact(old,new,[self.control],deps)
        self.assertEqual(report['changes'][0]['reopen_controls'],[self.control['id']])
        self.assertEqual(len(report['changes'][0]['dependent_artifacts']),2)

    def test_unknown_dependency_target_fails_closed(self):
        old,new,deps=self.root/'old.jsonl',self.root/'new.jsonl',self.root/'dependencies.jsonl'
        old.write_text(json.dumps(self.artifact)+'\n');new.write_text(old.read_text())
        deps.write_text(json.dumps({'artifact_id':'artifact','resolved_artifact_ids':['unknown']}))
        with self.assertRaises(ValueError): impact(old,new,[self.control],deps)


if __name__ == '__main__':
    unittest.main()
