import json
import shutil
import tempfile
import unittest
from pathlib import Path

from ges.bounded_review import BASE, build
from ges.core import ROOT


class BoundedReviewTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        shutil.copytree(ROOT / BASE, self.root / BASE)
        source = self.root / 'evidence/source-reviews'
        source.mkdir(parents=True)
        for path in (ROOT / 'evidence/source-reviews').glob('docs-actions-pilot*.json'):
            shutil.copyfile(path, source / path.name)

    def alter(self, path, change):
        target = self.root / BASE / path
        data = json.loads(target.read_text())
        change(data)
        target.write_text(json.dumps(data))

    def test_complete_source_reviews_preserve_conflicts_without_adoption(self):
        result = build(self.root)
        report = json.loads(result['accounting.json'])
        self.assertEqual(report['propositions_reviewed'], 227)
        self.assertEqual(report['new_artifact_coverage'], 0)
        self.assertEqual(report['conflicting_propositions_retained'], 4)
        self.assertFalse(report['whole_project_accepted'])
        self.assertEqual(report['accepted_controls'], 0)
        decisions = [json.loads(line) for line in result['decisions.jsonl'].splitlines()]
        self.assertEqual(sum(d['disposition'] == 'CONFLICT' for d in decisions), 4)
        self.assertTrue(all(d['review']['status'] == 'REVIEWED' for d in decisions))

    def test_changed_source_interpretation_invalidates_review(self):
        self.alter('b0/annotations.v3.json', lambda d: d['artifacts'].pop())
        with self.assertRaisesRegex(ValueError, 'Changed reviewed input'):
            build(self.root)

    def test_unresolved_review_cannot_be_promoted(self):
        self.alter('c0/independent-review-v3.json', lambda d: d.update(status='HOLD'))
        with self.assertRaisesRegex(ValueError, 'did not pass'):
            build(self.root)

    def test_same_worker_is_not_independent(self):
        identity = 'codex:01a11342-68e2-7851-9636-9af99289c0d7'
        self.alter('b0/independent-review-v3.json',
                   lambda d: d['reviewer'].update(agent_task=identity))
        with self.assertRaisesRegex(ValueError, 'distinct worker'):
            build(self.root)

    def test_source_grant_cannot_be_used_for_policy_adoption(self):
        self.alter('owner-approval-2026-10-06.json',
                   lambda d: d.update(target_policy_adoption_authorized=True))
        with self.assertRaisesRegex(ValueError, 'expand authority'):
            build(self.root)

    def test_missing_bindings_and_wrong_scope_fail_closed(self):
        self.alter('b0/primary-review-v3.json', lambda d: d.update(input_bindings=[]))
        with self.assertRaisesRegex(ValueError, 'input membership'):
            build(self.root)

    def test_incomplete_review_denominator_is_rejected(self):
        self.alter('b0/primary-review-v3.json', lambda d: d['scope'].update(artifacts=1))
        with self.assertRaisesRegex(ValueError, 'source denominator'):
            build(self.root)

    def test_unrelated_owner_scope_is_not_authority(self):
        self.alter('owner-approval-2026-10-06.json', lambda d: d.update(source_review_scope='Other work'))
        with self.assertRaisesRegex(ValueError, 'does not cover'):
            build(self.root)

    def test_noncanonical_worker_cannot_evade_independence(self):
        self.alter('b0/independent-review-v3.json',
                   lambda d: d['reviewer'].update(agent_task='codex:01a11342-68e2-7851-9636-9af99289c0d7 '))
        with self.assertRaisesRegex(ValueError, 'noncanonical'):
            build(self.root)
