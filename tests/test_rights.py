import unittest
from ges.rights import triage


class RightsTriage(unittest.TestCase):
    def setUp(self):
        self.artifact = {'artifact_id': 'one', 'source': 'owner/repo', 'commit': 'pin',
                         'path': 'README.md', 'sha256': 'digest', 'url': 'reference'}
        self.pins = {'owner/repo': 'pin'}
        self.finding = {k: self.artifact[k] for k in ('source', 'commit', 'path')}
        self.finding.update(content_sha256='digest', redistribution_approved=False)

    def test_inventory_is_not_clearance(self):
        report = triage([self.artifact], self.pins, [])
        self.assertEqual(report['denominator'], 1)
        self.assertEqual(report['rights_accepted'], 0)
        self.assertFalse(report['records'][0]['file_specific_review_performed'])
        self.assertFalse(report['rights_clearance_certified'])

    def test_existing_findings_remain_pending(self):
        report = triage([self.artifact], self.pins, [self.finding])
        self.assertTrue(report['records'][0]['file_specific_review_performed'])
        self.assertEqual(report['rights_accepted'], 0)

    def test_mismatched_pin_rejected(self):
        with self.assertRaises(ValueError):
            triage([self.artifact], {}, [])

    def test_mismatched_digest_rejected(self):
        self.finding['content_sha256'] = 'changed'
        with self.assertRaises(ValueError):
            triage([self.artifact], self.pins, [self.finding])

    def test_approval_cannot_be_inferred(self):
        self.finding['redistribution_approved'] = True
        with self.assertRaises(ValueError):
            triage([self.artifact], self.pins, [self.finding])

    def test_duplicate_inventory_rejected(self):
        with self.assertRaises(ValueError):
            triage([self.artifact, self.artifact], self.pins, [])
