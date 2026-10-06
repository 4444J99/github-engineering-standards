"""Invalidated identities must be rejected before authority is exercised."""
import json
import tempfile
import unittest
from pathlib import Path

from ges.core import digest, load
from ges.evaluate import audit
from ges.evidence_integrity import validate_authority


class AuthorityBoundary(unittest.TestCase):
    def test_all_authority_roles_reject_invalidated_identity(self):
        roles = ('reviewers', 'auditors', 'certifiers', 'claim_authors',
                 'omission_auditors', 'fidelity_auditors',
                 'independent_omission_auditors', 'reconcilers',
                 'independent_reviewers', 'human_acceptors',
                 'distribution_approvers')
        for role in roles:
            policy = {'authorized_' + role: ['automated:semantic-review-v0.2.0']}
            with self.subTest(role=role):
                for boundary in (validate_authority, digest):
                    with self.assertRaisesRegex(ValueError, 'Invalidated heuristic'):
                        boundary(policy)
                with tempfile.TemporaryDirectory() as directory:
                    path = Path(directory) / 'policy.json'
                    path.write_text(json.dumps(policy))
                    with self.assertRaisesRegex(ValueError, 'Invalidated heuristic'):
                        load(path)

    def test_manual_control_cannot_pass_with_invalidated_authority(self):
        with self.assertRaisesRegex(ValueError, 'Invalidated heuristic'):
            audit([], {}, {'authorized_reviewers': ['automated:semantic-review-v0.2.0']})

    def test_nested_authority_rejected_but_historical_identity_allowed(self):
        with self.assertRaises(ValueError):
            validate_authority({'profile': {'authorized_reviewers':
                ['automated:semantic-review-v0.2.0']}})
        self.assertEqual(validate_authority({'reviewer':
            'automated:semantic-review-v0.2.0'}), {'reviewer':
            'automated:semantic-review-v0.2.0'})
