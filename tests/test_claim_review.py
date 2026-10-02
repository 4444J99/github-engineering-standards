"""Unstructured claim provenance must fail closed as well as structured receipts."""
import gzip
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from ges.claim_review import validate_provenance


class ClaimProvenance(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.text = 'Review access.\nCheck scope.\n'
        self.source = 'owner/repo'
        self.commit = 'a'*40
        self.artifact = {'artifact_id': 'artifact', 'source': self.source,
                         'commit': self.commit, 'path': 'guide.md',
                         'sha256': hashlib.sha256(self.text.encode()).hexdigest()}
        self.claim = {'claim_id': 'REF-1', 'statement': 'Review actual access.',
                      'source': self.source, 'commit': self.commit, 'path': 'guide.md',
                      'start_line': 1, 'end_line': 2, 'accepted_policy': False}
        self.doc = {'reviewer': 'reviewer', 'reviewed_at': '2026-01-01T00:00:00Z',
                    'claims': [self.claim]}

    def check(self, text=None, control_ids=None):
        artifacts = self.root / 'artifacts.jsonl'
        artifacts.write_text(json.dumps(self.artifact)+'\n')
        (self.root / 'reference-claims.json').write_text(json.dumps(self.doc))
        with gzip.open(self.root / 'owner__repo.text.jsonl.gz', 'wt') as stream:
            stream.write(json.dumps({'source': self.source, 'commit': self.commit,
                                     'path': 'guide.md', 'content': self.text if text is None else text})+'\n')
        return validate_provenance(artifacts, self.root, self.root, ['reviewer'],
                                   {self.source: self.commit}, control_ids)

    def test_valid_reference_provenance_is_not_semantic_certification(self):
        result = self.check()
        self.assertEqual(result['reference_claims'], 1)
        self.assertFalse(result['semantic_truth_certified'])
        self.assertFalse(result['rights_cleared'])

    def test_claim_beyond_end_of_file_rejected(self):
        self.claim['end_line'] = 3
        with self.assertRaisesRegex(ValueError, 'exceeds source span'):
            self.check()

    def test_blank_source_span_rejected_even_with_matching_digest(self):
        for blank in ('', ' \t '):
            with self.subTest(blank=blank):
                self.text = f'Review access.\n{blank}\nCheck scope.\n'
                self.artifact['sha256'] = hashlib.sha256(self.text.encode()).hexdigest()
                self.claim.update(start_line=2, end_line=2,
                                  span_sha256=hashlib.sha256(blank.encode()).hexdigest())
                with self.assertRaisesRegex(ValueError, 'Blank claim source span'):
                    self.check()

    def test_unpinned_commit_rejected(self):
        self.claim['commit'] = 'b'*40
        with self.assertRaisesRegex(ValueError, 'locked source pin'):
            self.check()

    def test_changed_source_text_rejected(self):
        with self.assertRaisesRegex(ValueError, 'artifact digest'):
            self.check('Altered.\nCheck scope.\n')

    def test_wrong_claim_content_digest_rejected(self):
        self.claim['content_sha256'] = 'b'*64
        with self.assertRaisesRegex(ValueError, 'content digest mismatch'):
            self.check()

    def test_wrong_claim_span_digest_rejected(self):
        self.claim['span_sha256'] = 'b'*64
        with self.assertRaisesRegex(ValueError, 'span digest mismatch'):
            self.check()

    def test_duplicate_claim_rejected(self):
        self.doc['claims'].append(dict(self.claim))
        with self.assertRaisesRegex(ValueError, 'duplicate claim'):
            self.check()

    def test_no_claims_is_not_success(self):
        self.doc['claims'] = []
        with self.assertRaisesRegex(ValueError, 'Missing claims'):
            self.check()

    def test_foreign_reviewer_rejected(self):
        self.doc['reviewer'] = 'stranger'
        with self.assertRaisesRegex(ValueError, 'Unauthorized reviewer'):
            self.check()

    def test_reference_adoption_claim_rejected(self):
        self.claim['accepted_policy'] = True
        with self.assertRaisesRegex(ValueError, 'asserts adoption'):
            self.check()

    def test_unknown_duplicate_target_rejected(self):
        self.claim['duplicate_of'] = 'missing'
        with self.assertRaisesRegex(ValueError, 'Unknown duplicate'):
            self.check()

    def test_self_duplicate_rejected(self):
        self.claim['duplicate_of'] = 'REF-1'
        with self.assertRaisesRegex(ValueError, 'Cyclic duplicate'):
            self.check()

    def test_duplicate_cycle_rejected(self):
        self.claim['duplicate_of'] = 'REF-2'
        other = dict(self.claim, claim_id='REF-2', duplicate_of='REF-1')
        self.doc['claims'].append(other)
        with self.assertRaisesRegex(ValueError, 'Cyclic duplicate'):
            self.check()

    def test_valid_duplicate_is_not_semantic_equivalence_certificate(self):
        other = dict(self.claim, claim_id='REF-2', duplicate_of='REF-1')
        self.doc['claims'].append(other)
        result = self.check()
        self.assertEqual(result['duplicate_relationships_validated'], 1)
        self.assertFalse(result['semantic_truth_certified'])

    def test_unknown_proposed_control_rejected(self):
        self.claim['proposed_control_ids'] = ['NONEXISTENT']
        with self.assertRaisesRegex(ValueError, 'Unknown proposed control'):
            self.check(control_ids={'GES-ACT-001'})

    def test_malformed_proposed_controls_rejected(self):
        for value in ('GES-ACT-001', [None], ['GES-ACT-001', 'GES-ACT-001']):
            self.claim['proposed_control_ids'] = value
            with self.subTest(value=value), self.assertRaisesRegex(ValueError, 'Invalid proposed control'):
                self.check()

    def test_valid_proposal_identity_is_not_equivalence(self):
        self.claim['proposed_control_ids'] = ['GES-ACT-001']
        report = self.check(control_ids={'GES-ACT-001'})
        self.assertTrue(report['proposed_control_identities_verified'])
        self.assertFalse(report['proposed_mapping_equivalence_certified'])


if __name__ == '__main__':
    unittest.main()
