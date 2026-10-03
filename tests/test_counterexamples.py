"""
Negative Regression Counterexample Test Suite (TDD Gate).

Author: Explorer M1.1 (Negative Regression Test Suite Designer)
Target File: tests/test_counterexamples.py
Reference: ORIGINAL_REQUEST.md §R1, Recovery Addendum, Explorer Survey 2 handoff

This test suite establishes the negative regression baseline for all 20 counterexample
scenarios across 11 evaluator/binding defect clusters and 5 data contract flaws identified
in commit 30b1f83.

Each test is designed according to TDD principles:
- Against the current unpatched codebase (commit 30b1f83), ALL 20 TESTS FAIL (raising AssertionError),
  conclusively proving the existence of the false-pass and false-fail defects.
- After evaluator repairs in `ges/checks.py`, schema validations in `ges/core.py`, and
  catalog binding corrections in `controls/catalog.json`, ALL 20 TESTS WILL PASS.

Test Matrix:
1.  test_rule_015_force_push_pr_rule_only       -> Fails when only PR rule is present without non_fast_forward.
2.  test_rule_016_deletion_pr_rule_only         -> Fails when only PR rule is present without deletion.
3.  test_rule_010_zero_reviews_fails            -> Fails when required_approving_review_count == 0.
4.  test_rule_011_stale_reviews_not_dismissed   -> Fails when dismiss_stale_reviews_on_push == False.
5.  test_rule_012_codeowners_not_required       -> Fails when require_code_owner_review == False.
6.  test_rule_014_no_status_checks_rule         -> Fails when required_status_checks rule is missing.
7.  test_com_006_discussions_disabled           -> Fails when repo metadata has_discussions == False even if CODE_OF_CONDUCT.md exists.
8.  test_com_007_empty_description              -> Fails when repo metadata description == "" even if CODE_OF_CONDUCT.md exists.
9.  test_com_008_empty_topics                   -> Fails when repo metadata topics == [] even if CODE_OF_CONDUCT.md exists.
10. test_act_010_token_write_permission         -> Fails when default_workflow_permissions == 'write'.
11. test_sec_046_alerts_disabled_empty_list     -> Fails or NOT_VERIFIABLE when dependabot alerts are disabled (empty list without enablement proof).
12. test_sec_047_critical_alerts_only_medium    -> Passes when only medium alerts are present (0 critical).
13. test_sec_048_high_alerts_only_medium        -> Passes when only medium alerts are present (0 high).
14. test_sec_052_code_scanning_unconfigured     -> Fails when CodeQL is not configured (empty alerts list without analysis/workflow evidence).
15. test_sec_043_deploy_key_missing_read_only   -> Fails when read_only is missing (not boolean True).
16. test_sec_044_deploy_key_missing_verified    -> Fails when verified is missing (not boolean True).
17. test_sec_050_dependabot_config_empty_dict   -> Fails when dependabot config is empty dict or invalid YAML.
18. test_alerts_untyped_payload_null            -> Returns ERROR on None payload.
19. test_alerts_untyped_payload_dict            -> Returns ERROR on dict payload for list endpoint.
20. test_composite_action_unpinned_remote       -> Detects unpinned action inside local composite action.
"""

from __future__ import annotations
import copy
import sys
import unittest
from pathlib import Path

# Ensure project root is in sys.path when executed directly
_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from ges.core import ROOT, load
from ges.checks import execute


def load_catalog_index() -> dict[str, dict]:
    """Index controls by id from catalog.json and review_queue.json."""
    index: dict[str, dict] = {}
    cat_path = ROOT / 'controls' / 'catalog.json'
    if cat_path.is_file():
        try:
            for c in load(cat_path):
                if 'id' in c:
                    index[c['id']] = c
        except Exception:
            pass
    rq_path = ROOT / 'controls' / 'review_queue.json'
    if rq_path.is_file():
        try:
            for c in load(rq_path):
                if 'id' in c and c['id'] not in index:
                    index[c['id']] = c
        except Exception:
            pass
    return index


CAT_INDEX = load_catalog_index()

# Fallback definitions conforming to canonical control structures in case controls
# are quarantined or evaluated in isolation.
CANONICAL_FALLBACKS: dict[str, dict] = {
    'GES-RULE-015': {
        'id': 'GES-RULE-015',
        'revision': 1,
        'title': 'Force pushes allowed on protected branch',
        'objective': 'CRITICAL: Disable force pushes on all protected branches to prevent history rewriting.',
        'verification': {'kind': 'effective_rule', 'rule_type': 'non_fast_forward'},
        'obligation': 'MUST',
        'status': 'REVIEWED_DRAFT'
    },
    'GES-RULE-016': {
        'id': 'GES-RULE-016',
        'revision': 1,
        'title': 'Branch deletion allowed on protected branch',
        'objective': 'Disable branch deletion for all protected branches.',
        'verification': {'kind': 'effective_rule', 'rule_type': 'deletion'},
        'obligation': 'MUST',
        'status': 'REVIEWED_DRAFT'
    },
    'GES-RULE-010': {
        'id': 'GES-RULE-010',
        'revision': 1,
        'title': 'No approving reviews required before merge',
        'objective': 'CRITICAL: Require at least 1 approving review before merge to enforce code review and catch errors or malicious changes.',
        'verification': {
            'kind': 'effective_rule',
            'rule_type': 'pull_request',
            'parameter': 'required_approving_review_count',
            'operator': 'at_least',
            'profile_parameter': 'required_reviews',
            'value': 1
        },
        'obligation': 'MUST',
        'status': 'REVIEWED_DRAFT'
    },
    'GES-RULE-011': {
        'id': 'GES-RULE-011',
        'revision': 1,
        'title': 'Stale reviews not dismissed on new commits',
        'objective': 'Enable stale review dismissal so that existing approvals are invalidated when new commits are pushed.',
        'verification': {
            'kind': 'effective_rule',
            'rule_type': 'pull_request',
            'parameter': 'dismiss_stale_reviews_on_push',
            'value': True
        },
        'obligation': 'MUST',
        'status': 'REVIEWED_DRAFT'
    },
    'GES-RULE-012': {
        'id': 'GES-RULE-012',
        'revision': 1,
        'title': 'Code owner review not required',
        'objective': 'Enable the code owner review requirement so changes to paths defined in CODEOWNERS must be approved by the designated owner.',
        'verification': {
            'kind': 'effective_rule',
            'rule_type': 'pull_request',
            'parameter': 'require_code_owner_review',
            'value': True
        },
        'obligation': 'SHOULD',
        'status': 'REVIEWED_DRAFT'
    },
    'GES-RULE-014': {
        'id': 'GES-RULE-014',
        'revision': 1,
        'title': 'No required status checks configured',
        'objective': 'Configure CI/CD checks that must pass before any pull request can be merged.',
        'verification': {'kind': 'effective_rule', 'rule_type': 'required_status_checks'},
        'obligation': 'MUST',
        'status': 'REVIEWED_DRAFT'
    },
    'GES-COM-006': {
        'id': 'GES-COM-006',
        'revision': 1,
        'title': 'GitHub Discussions not enabled',
        'objective': 'Consider enabling GitHub Discussions to provide a dedicated channel for community Q&A.',
        'verification': {'kind': 'metadata_nonempty', 'field': 'has_discussions'},
        'obligation': 'MAY',
        'status': 'REVIEWED_DRAFT'
    },
    'GES-COM-007': {
        'id': 'GES-COM-007',
        'revision': 1,
        'title': 'Repository has no description',
        'objective': 'Add a concise description to every repository.',
        'verification': {'kind': 'metadata_nonempty', 'field': 'description'},
        'obligation': 'SHOULD',
        'status': 'REVIEWED_DRAFT'
    },
    'GES-COM-008': {
        'id': 'GES-COM-008',
        'revision': 1,
        'title': 'Repository has no topics',
        'objective': 'Add relevant GitHub topics to this repository.',
        'verification': {'kind': 'metadata_nonempty', 'field': 'topics'},
        'obligation': 'MAY',
        'status': 'REVIEWED_DRAFT'
    },
    'GES-ACT-010': {
        'id': 'GES-ACT-010',
        'revision': 1,
        'title': 'Default GITHUB_TOKEN permission is write',
        'objective': 'Change the default workflow permission to read in Organization/Repository Settings.',
        'verification': {'kind': 'actions_permissions', 'require_read_permissions': True},
        'obligation': 'MUST',
        'status': 'REVIEWED_DRAFT'
    },
    'GES-SEC-046': {
        'id': 'GES-SEC-046',
        'revision': 1,
        'title': 'Dependabot alerts not enabled',
        'objective': 'Enable Dependabot alerts in repository settings.',
        'verification': {'kind': 'dependabot_alerts', 'check_enablement': True},
        'obligation': 'MUST',
        'status': 'REVIEWED_DRAFT'
    },
    'GES-SEC-047': {
        'id': 'GES-SEC-047',
        'revision': 1,
        'title': 'Critical Dependabot alerts open',
        'objective': 'Immediately address critical security vulnerabilities by updating affected dependencies.',
        'verification': {'kind': 'dependabot_alerts', 'severity': 'critical'},
        'obligation': 'MUST',
        'status': 'REVIEWED_DRAFT'
    },
    'GES-SEC-048': {
        'id': 'GES-SEC-048',
        'revision': 1,
        'title': 'High-severity Dependabot alerts open',
        'objective': 'Prioritize fixing high-severity dependency vulnerabilities.',
        'verification': {'kind': 'dependabot_alerts', 'severity': 'high'},
        'obligation': 'MUST',
        'status': 'REVIEWED_DRAFT'
    },
    'GES-SEC-052': {
        'id': 'GES-SEC-052',
        'revision': 1,
        'title': 'Code scanning (CodeQL) not configured',
        'objective': 'Enable GitHub code scanning with CodeQL to automatically detect security vulnerabilities.',
        'verification': {'kind': 'code_scanning_alerts', 'require_configured': True},
        'obligation': 'MUST',
        'status': 'REVIEWED_DRAFT'
    },
    'GES-SEC-043': {
        'id': 'GES-SEC-043',
        'revision': 1,
        'title': 'Deploy keys with write access',
        'objective': 'Use read-only deploy keys where possible.',
        'verification': {'kind': 'deploy_keys'},
        'obligation': 'MUST',
        'status': 'REVIEWED_DRAFT'
    },
    'GES-SEC-044': {
        'id': 'GES-SEC-044',
        'revision': 1,
        'title': 'Unverified deploy keys',
        'objective': 'Verify all deploy keys to ensure they are associated with authorized systems.',
        'verification': {'kind': 'deploy_keys'},
        'obligation': 'SHOULD',
        'status': 'REVIEWED_DRAFT'
    },
    'GES-SEC-050': {
        'id': 'GES-SEC-050',
        'revision': 1,
        'title': 'Dependabot alerts enabled but no dependabot.yml found',
        'objective': 'Create a .github/dependabot.yml file to enable automated dependency version updates.',
        'verification': {'kind': 'dependabot_config'},
        'obligation': 'SHOULD',
        'status': 'REVIEWED_DRAFT'
    }
}


def get_control(control_id: str) -> dict:
    """Retrieve control by ID from current catalog/review queue or canonical fallback."""
    if control_id in CAT_INDEX:
        return copy.deepcopy(CAT_INDEX[control_id])
    if control_id in CANONICAL_FALLBACKS:
        return copy.deepcopy(CANONICAL_FALLBACKS[control_id])
    raise KeyError(f"Control {control_id} not found in catalog, review_queue, or fallbacks")


def make_snapshot(files: dict | None = None, extra: dict | None = None, complete: bool = True) -> dict:
    """Construct a clean, valid snapshot fixture with optional file inventory and endpoint observations."""
    snap = {
        'target': 'test-owner/test-repo',
        'target_revision': 'a' * 40,
        'target_type': 'repository',
        'observed_at': '2026-10-01T20:00:00+00:00',
        'observations': {
            'repository': {
                'status': 'OK',
                'data': {
                    'name': 'test-repo',
                    'description': 'A valid repository description',
                    'topics': ['python', 'standards'],
                    'has_discussions': True
                }
            },
            'files': {
                'status': 'OK',
                'complete': complete,
                'data': files or {}
            }
        }
    }
    if extra:
        for observation in extra.values():
            if isinstance(observation,dict) and isinstance(observation.get('data'),list):
                observation.setdefault('complete',True)
        snap['observations'].update(extra)
    return snap


class NegativeCounterexampleTests(unittest.TestCase):
    """20 Negative Counterexample Regression Test Cases proving evaluator defects before repair."""

    # -------------------------------------------------------------------------
    # Cluster 1: Branch Protection Ruleset Bindings (Defects 1 & 2)
    # -------------------------------------------------------------------------

    def test_rule_015_force_push_pr_rule_only(self):
        """
        Scenario 1: GES-RULE-015 must fail when only PR rule is present without non_fast_forward.

        Defect in commit 30b1f83:
            catalog.json line 9997 binds GES-RULE-015 to rule_type: 'pull_request'.
            When ruleset contains only pull_request, checks.py line 77 unconditionally returns PASS,
            falsely asserting that force pushes are blocked even though force pushes are unrestricted!
        Expected post-repair:
            Evaluator checks rule_type: 'non_fast_forward'. When absent, returns FAIL or NOT_VERIFIABLE.
        """
        ctrl = get_control('GES-RULE-015')
        snap = make_snapshot(extra={
            'effective_branch_rules': {
                'status': 'OK',
                'data': [
                    {'type': 'pull_request', 'parameters': {'required_approving_review_count': 1}}
                ]
            }
        })
        verdict, detail = execute(ctrl, snap, {})
        self.assertIn(
            verdict, ('FAIL', 'NOT_VERIFIABLE'),
            f"GES-RULE-015 must reject branch protection lacking non_fast_forward rule. Got: {verdict} ({detail})"
        )
        self.assertNotEqual(verdict, 'PASS', "False PASS: Force push protection passed without non_fast_forward rule!")

    def test_rule_016_deletion_pr_rule_only(self):
        """
        Scenario 2: GES-RULE-016 must fail when only PR rule is present without deletion.

        Defect in commit 30b1f83:
            catalog.json line 10044 binds GES-RULE-016 to rule_type: 'pull_request'.
            Returns PASS even though branch deletion is unrestricted.
        Expected post-repair:
            Evaluator checks rule_type: 'deletion'. When absent, returns FAIL or NOT_VERIFIABLE.
        """
        ctrl = get_control('GES-RULE-016')
        snap = make_snapshot(extra={
            'effective_branch_rules': {
                'status': 'OK',
                'data': [
                    {'type': 'pull_request', 'parameters': {'required_approving_review_count': 1}}
                ]
            }
        })
        verdict, detail = execute(ctrl, snap, {})
        self.assertIn(
            verdict, ('FAIL', 'NOT_VERIFIABLE'),
            f"GES-RULE-016 must reject branch protection lacking deletion rule. Got: {verdict} ({detail})"
        )
        self.assertNotEqual(verdict, 'PASS', "False PASS: Branch deletion prevention passed without deletion rule!")

    def test_rule_010_zero_reviews_fails(self):
        """
        Scenario 3: GES-RULE-010 must fail when required_approving_review_count == 0.

        Defect in commit 30b1f83:
            GES-RULE-010 checks rule_type: 'pull_request' with parameter=None.
            Because parameter is None, checks.py line 77 returns PASS when review count is 0.
        Expected post-repair:
            Checks parameter required_approving_review_count >= 1 (or against profile). Returns FAIL on 0.
        """
        ctrl = get_control('GES-RULE-010')
        snap = make_snapshot(extra={
            'effective_branch_rules': {
                'status': 'OK',
                'data': [
                    {
                        'type': 'pull_request',
                        'parameters': {
                            'required_approving_review_count': 0,
                            'dismiss_stale_reviews_on_push': True,
                            'require_code_owner_review': True
                        }
                    }
                ]
            }
        })
        verdict, detail = execute(ctrl, snap, {'required_reviews': 1})
        self.assertEqual(
            verdict, 'FAIL',
            f"GES-RULE-010 must fail when required_approving_review_count is 0. Got: {verdict} ({detail})"
        )

    def test_rule_011_stale_reviews_not_dismissed(self):
        """
        Scenario 4: GES-RULE-011 must fail when dismiss_stale_reviews_on_push == False.

        Defect in commit 30b1f83:
            GES-RULE-011 checks rule_type: 'pull_request' without validating dismiss_stale_reviews_on_push.
            Returns PASS when dismiss_stale_reviews_on_push is False.
        Expected post-repair:
            Checks dismiss_stale_reviews_on_push is True. Returns FAIL when False.
        """
        ctrl = get_control('GES-RULE-011')
        snap = make_snapshot(extra={
            'effective_branch_rules': {
                'status': 'OK',
                'data': [
                    {
                        'type': 'pull_request',
                        'parameters': {
                            'required_approving_review_count': 1,
                            'dismiss_stale_reviews_on_push': False,
                            'require_code_owner_review': True
                        }
                    }
                ]
            }
        })
        verdict, detail = execute(ctrl, snap, {})
        self.assertEqual(
            verdict, 'FAIL',
            f"GES-RULE-011 must fail when dismiss_stale_reviews_on_push is False. Got: {verdict} ({detail})"
        )

    def test_rule_012_codeowners_not_required(self):
        """
        Scenario 5: GES-RULE-012 must fail when require_code_owner_review == False.

        Defect in commit 30b1f83:
            GES-RULE-012 checks rule_type: 'pull_request' without validating require_code_owner_review.
            Returns PASS when require_code_owner_review is False.
        Expected post-repair:
            Checks require_code_owner_review is True. Returns FAIL when False.
        """
        ctrl = get_control('GES-RULE-012')
        snap = make_snapshot(extra={
            'effective_branch_rules': {
                'status': 'OK',
                'data': [
                    {
                        'type': 'pull_request',
                        'parameters': {
                            'required_approving_review_count': 1,
                            'dismiss_stale_reviews_on_push': True,
                            'require_code_owner_review': False
                        }
                    }
                ]
            }
        })
        verdict, detail = execute(ctrl, snap, {})
        self.assertEqual(
            verdict, 'FAIL',
            f"GES-RULE-012 must fail when require_code_owner_review is False. Got: {verdict} ({detail})"
        )

    def test_rule_014_no_status_checks_rule(self):
        """
        Scenario 6: GES-RULE-014 must fail or return NOT_VERIFIABLE when required_status_checks rule is missing.

        Defect in commit 30b1f83:
            GES-RULE-014 (CI status checks) binds to rule_type: 'pull_request' instead of 'required_status_checks'.
            Returns PASS even when zero CI status checks are required for merge.
        Expected post-repair:
            Evaluator checks rule_type: 'required_status_checks'. When absent, returns FAIL or NOT_VERIFIABLE.
        """
        ctrl = get_control('GES-RULE-014')
        snap = make_snapshot(extra={
            'effective_branch_rules': {
                'status': 'OK',
                'data': [
                    {
                        'type': 'pull_request',
                        'parameters': {'required_approving_review_count': 1}
                    }
                ]
            }
        })
        verdict, detail = execute(ctrl, snap, {})
        self.assertIn(
            verdict, ('FAIL', 'NOT_VERIFIABLE'),
            f"GES-RULE-014 must fail or return NOT_VERIFIABLE when required_status_checks rule is absent. Got: {verdict} ({detail})"
        )
        self.assertNotEqual(verdict, 'PASS', "False PASS: Status check rule passed without required_status_checks rule!")

    # -------------------------------------------------------------------------
    # Cluster 2: Community Metadata vs Code of Conduct File Bindings (Defect 3)
    # -------------------------------------------------------------------------

    def test_com_006_discussions_disabled(self):
        """
        Scenario 7: GES-COM-006 must fail when repository has_discussions == False even if CODE_OF_CONDUCT.md exists.

        Defect in commit 30b1f83:
            generate_ghqr_controls.py lines 126-127 mapped category 'community' to file_present of CODE_OF_CONDUCT.md.
            Because CODE_OF_CONDUCT.md exists, file_exists() returns PASS, ignoring repo metadata has_discussions=False!
        Expected post-repair:
            Evaluator checks repository metadata has_discussions is True. Returns FAIL when False.
        """
        ctrl = get_control('GES-COM-006')
        snap = make_snapshot(
            files={'CODE_OF_CONDUCT.md': '# Code of Conduct\nBe respectful and inclusive.\n'},
            extra={
                'repository': {
                    'status': 'OK',
                    'data': {
                        'name': 'test-repo',
                        'description': 'A valid repository description',
                        'topics': ['python', 'standards'],
                        'has_discussions': False
                    }
                }
            }
        )
        verdict, detail = execute(ctrl, snap, {})
        self.assertEqual(
            verdict, 'FAIL',
            f"GES-COM-006 must fail when has_discussions is False even if CODE_OF_CONDUCT.md exists. Got: {verdict} ({detail})"
        )

    def test_com_007_empty_description(self):
        """
        Scenario 8: GES-COM-007 must fail when repository description == "" even if CODE_OF_CONDUCT.md exists.

        Defect in commit 30b1f83:
            Bound to CODE_OF_CONDUCT.md presence. Returns PASS when repository description is completely empty!
        Expected post-repair:
            Evaluator checks repository description is nonempty string. Returns FAIL when empty.
        """
        ctrl = get_control('GES-COM-007')
        snap = make_snapshot(
            files={'CODE_OF_CONDUCT.md': '# Code of Conduct\nBe respectful and inclusive.\n'},
            extra={
                'repository': {
                    'status': 'OK',
                    'data': {
                        'name': 'test-repo',
                        'description': '',
                        'topics': ['python', 'standards'],
                        'has_discussions': True
                    }
                }
            }
        )
        verdict, detail = execute(ctrl, snap, {})
        self.assertEqual(
            verdict, 'FAIL',
            f"GES-COM-007 must fail when description is empty even if CODE_OF_CONDUCT.md exists. Got: {verdict} ({detail})"
        )

    def test_com_008_empty_topics(self):
        """
        Scenario 9: GES-COM-008 must fail when repository topics == [] even if CODE_OF_CONDUCT.md exists.

        Defect in commit 30b1f83:
            Bound to CODE_OF_CONDUCT.md presence. Returns PASS when repository topics list is empty!
        Expected post-repair:
            Evaluator checks repository topics has at least one topic. Returns FAIL when empty list.
        """
        ctrl = get_control('GES-COM-008')
        snap = make_snapshot(
            files={'CODE_OF_CONDUCT.md': '# Code of Conduct\nBe respectful and inclusive.\n'},
            extra={
                'repository': {
                    'status': 'OK',
                    'data': {
                        'name': 'test-repo',
                        'description': 'A valid repository description',
                        'topics': [],
                        'has_discussions': True
                    }
                }
            }
        )
        verdict, detail = execute(ctrl, snap, {})
        self.assertEqual(
            verdict, 'FAIL',
            f"GES-COM-008 must fail when topics is empty even if CODE_OF_CONDUCT.md exists. Got: {verdict} ({detail})"
        )

    # -------------------------------------------------------------------------
    # Cluster 3: GitHub Actions Token Permissions (Defect 4)
    # -------------------------------------------------------------------------

    def test_act_010_token_write_permission(self):
        """
        Scenario 10: GES-ACT-010 must fail when default_workflow_permissions == 'write'.

        Defect in commit 30b1f83:
            checks.py actions_permissions() reads allowed_actions from /actions/permissions,
            completely ignoring default_workflow_permissions.
            When allowed_actions is 'selected', it returns PASS even if token default permission is 'write'!
        Expected post-repair:
            Evaluator inspects actions_permissions_workflow and requires default_workflow_permissions == 'read'.
            Returns FAIL when permissions are 'write'.
        """
        ctrl = get_control('GES-ACT-010')
        snap = make_snapshot(extra={
            'actions_permissions': {
                'status': 'OK',
                'data': {
                    'enabled': True,
                    'allowed_actions': 'selected'
                }
            },
            'actions_permissions_workflow': {
                'status': 'OK',
                'data': {
                    'default_workflow_permissions': 'write',
                    'can_approve_pull_request_reviews': False
                }
            }
        })
        verdict, detail = execute(ctrl, snap, {})
        self.assertEqual(
            verdict, 'FAIL',
            f"GES-ACT-010 must fail when default_workflow_permissions is 'write'. Got: {verdict} ({detail})"
        )

    # -------------------------------------------------------------------------
    # Cluster 4: Alert Enablement, Severity Separation & Configuration (Defects 6 & 7)
    # -------------------------------------------------------------------------

    def test_sec_046_alerts_disabled_empty_list(self):
        """
        Scenario 11: GES-SEC-046 must fail or return NOT_VERIFIABLE when dependabot alerts are disabled.

        Defect in commit 30b1f83:
            checks.py line 257 executes: if not alerts: return 'PASS', 'No open Dependabot alerts'.
            When alerts are disabled, the endpoint returns [], which returns PASS, falsely claiming enablement!
        Expected post-repair:
            Evaluator distinguishes empty alert list from verified enablement evidence.
            Returns FAIL or NOT_VERIFIABLE when enablement is unverified.
        """
        ctrl = get_control('GES-SEC-046')
        snap = make_snapshot(extra={
            'dependabot_alerts': {
                'status': 'OK',
                'data': []
            }
        })
        verdict, detail = execute(ctrl, snap, {})
        self.assertIn(
            verdict, ('FAIL', 'NOT_VERIFIABLE'),
            f"GES-SEC-046 must return FAIL or NOT_VERIFIABLE on empty alerts list without enablement proof. Got: {verdict} ({detail})"
        )
        self.assertNotEqual(verdict, 'PASS', "False PASS: Dependabot alerts marked enabled based on empty alerts list!")

    def test_sec_047_critical_alerts_only_medium(self):
        """
        Scenario 12: GES-SEC-047 must PASS when only medium alerts are present (0 critical alerts).

        Defect in commit 30b1f83:
            checks.py line 261 returns FAIL whenever len(alerts) > 0, regardless of severity!
            A repository with 1 medium alert and 0 critical alerts fails GES-SEC-047 ('Critical Dependabot alerts open').
        Expected post-repair:
            GES-SEC-047 filters alerts by severity == 'critical'.
            When critical alerts count is 0, returns PASS.
        """
        ctrl = get_control('GES-SEC-047')
        snap = make_snapshot(extra={
            'dependabot_alerts': {
                'status': 'OK',
                'data': [
                    {
                        'number': 101,
                        'state': 'open',
                        'security_advisory': {
                            'severity': 'moderate',
                            'ghsa_id': 'GHSA-med-0001',
                            'summary': 'Moderate vulnerability'
                        }
                    }
                ]
            }
        })
        verdict, detail = execute(ctrl, snap, {})
        self.assertEqual(
            verdict, 'PASS',
            f"GES-SEC-047 must PASS when there are 0 critical alerts even if medium alerts exist. Got: {verdict} ({detail})"
        )

    def test_sec_048_high_alerts_only_medium(self):
        """
        Scenario 13: GES-SEC-048 must PASS when only medium alerts are present (0 high alerts).

        Defect in commit 30b1f83:
            checks.py line 261 returns FAIL whenever len(alerts) > 0, regardless of severity!
            A repository with 1 medium alert and 0 high alerts fails GES-SEC-048 ('High-severity alerts open').
        Expected post-repair:
            GES-SEC-048 filters alerts by severity == 'high'.
            When high alerts count is 0, returns PASS.
        """
        ctrl = get_control('GES-SEC-048')
        snap = make_snapshot(extra={
            'dependabot_alerts': {
                'status': 'OK',
                'data': [
                    {
                        'number': 102,
                        'state': 'open',
                        'security_advisory': {
                            'severity': 'moderate',
                            'ghsa_id': 'GHSA-med-0002',
                            'summary': 'Moderate vulnerability'
                        }
                    }
                ]
            }
        })
        verdict, detail = execute(ctrl, snap, {})
        self.assertEqual(
            verdict, 'PASS',
            f"GES-SEC-048 must PASS when there are 0 high alerts even if medium alerts exist. Got: {verdict} ({detail})"
        )

    def test_sec_052_code_scanning_unconfigured(self):
        """
        Scenario 14: GES-SEC-052 must fail when CodeQL is not configured (empty alerts list without analysis/workflow evidence).

        Defect in commit 30b1f83:
            checks.py line 231 executes: if not alerts: return 'PASS', 'No open code scanning alerts'.
            An unconfigured repository returns [] for /code-scanning/alerts and passes GES-SEC-052 ('CodeQL not configured')!
        Expected post-repair:
            Requires evidence of CodeQL configuration (workflow file or recent analysis).
            When unconfigured, returns FAIL or NOT_VERIFIABLE.
        """
        ctrl = get_control('GES-SEC-052')
        snap = make_snapshot(
            files={'README.md': '# Unconfigured Repo\n'},
            extra={
                'code_scanning_alerts': {
                    'status': 'OK',
                    'data': []
                },
                'code_scanning_analyses': {
                    'status': 'OK',
                    'data': []
                }
            }
        )
        verdict, detail = execute(ctrl, snap, {})
        self.assertIn(
            verdict, ('FAIL', 'NOT_VERIFIABLE'),
            f"GES-SEC-052 must fail or return NOT_VERIFIABLE when CodeQL is not configured. Got: {verdict} ({detail})"
        )
        self.assertNotEqual(verdict, 'PASS', "False PASS: CodeQL marked configured based on empty alert list!")

    # -------------------------------------------------------------------------
    # Cluster 5: Deploy Key Boolean Validation (Defect 8)
    # -------------------------------------------------------------------------

    def test_sec_043_deploy_key_missing_read_only(self):
        """
        Scenario 15: GES-SEC-043 must fail or return ERROR when read_only is missing (not boolean True).

        Defect in commit 30b1f83:
            checks.py line 186 executes: if key.get('read_only') is False: issues.append(...).
            When read_only is omitted or None, None is False evaluates to False, so missing read_only passes!
            Violates contract: 'Unknown is not true; require positive evidence of read_only is True'.
        Expected post-repair:
            Evaluator checks: key.get('read_only') is True. Missing or non-True returns FAIL/ERROR.
        """
        ctrl = get_control('GES-SEC-043')
        snap = make_snapshot(extra={
            'deploy_keys': {
                'status': 'OK',
                'data': [
                    {
                        'id': 101,
                        'key': 'ssh-rsa AAAA1234EXAMPLE==',
                        'title': 'Production Deployment Key',
                        'verified': True
                        # 'read_only' is omitted / missing!
                    }
                ]
            }
        })
        verdict, detail = execute(ctrl, snap, {})
        self.assertIn(
            verdict, ('FAIL', 'ERROR'),
            f"GES-SEC-043 must fail or return ERROR when deploy key read_only is missing. Got: {verdict} ({detail})"
        )
        self.assertNotEqual(verdict, 'PASS', "False PASS: Deploy key with missing read_only passed as read-only!")

    def test_sec_044_deploy_key_missing_verified(self):
        """
        Scenario 16: GES-SEC-044 must fail or return ERROR when verified is missing (not boolean True).

        Defect in commit 30b1f83:
            checks.py line 188 executes: if not key.get('verified', True): issues.append(...).
            When verified is omitted or None, key.get('verified', True) defaults to True!
            Missing verification passes as verified.
        Expected post-repair:
            Evaluator checks: key.get('verified') is True. Missing or non-True returns FAIL/ERROR.
        """
        ctrl = get_control('GES-SEC-044')
        snap = make_snapshot(extra={
            'deploy_keys': {
                'status': 'OK',
                'data': [
                    {
                        'id': 102,
                        'key': 'ssh-rsa AAAA5678EXAMPLE==',
                        'title': 'Staging Deployment Key',
                        'read_only': True
                        # 'verified' is omitted / missing!
                    }
                ]
            }
        })
        verdict, detail = execute(ctrl, snap, {})
        self.assertIn(
            verdict, ('FAIL', 'ERROR'),
            f"GES-SEC-044 must fail or return ERROR when deploy key verified is missing. Got: {verdict} ({detail})"
        )
        self.assertNotEqual(verdict, 'PASS', "False PASS: Deploy key with missing verified passed as verified!")

    # -------------------------------------------------------------------------
    # Cluster 6: Dependabot YAML Validation (Defect 9)
    # -------------------------------------------------------------------------

    def test_sec_050_dependabot_config_empty_dict(self):
        """
        Scenario 17: GES-SEC-050 must fail when dependabot config is empty dict or invalid YAML.

        Defect in commit 30b1f83:
            checks.py lines 158-163 checks only whether status == 'OK', returning PASS without
            inspecting content, base64 decoding, YAML syntax, or required version/updates keys.
            An empty dictionary {} passes dependabot_config check.
        Expected post-repair:
            Evaluator decodes base64 content, parses YAML, and validates version: 2 and updates list.
            Empty dictionary returns FAIL.
        """
        ctrl = get_control('GES-SEC-050')
        snap = make_snapshot(extra={
            'dependabot_config': {
                'status': 'OK',
                'data': {}
            }
        })
        verdict, detail = execute(ctrl, snap, {})
        self.assertEqual(
            verdict, 'FAIL',
            f"GES-SEC-050 must fail when dependabot_config is empty dict. Got: {verdict} ({detail})"
        )

    # -------------------------------------------------------------------------
    # Cluster 7: Untyped Payloads Data Contracts (Defect 11)
    # -------------------------------------------------------------------------

    def test_alerts_untyped_payload_null(self):
        """
        Scenario 18: Alert evaluator must return ERROR on None payload.

        Defect in commit 30b1f83:
            checks.py alert checkers do: alerts=data; if not alerts: return 'PASS'.
            When data is None, not None is True, causing malformed null observation to return PASS!
        Expected post-repair:
            Evaluator asserts isinstance(data, list). If data is None, returns ERROR.
        """
        ctrl = {'verification': {'kind': 'code_scanning_alerts'}}
        snap = make_snapshot(extra={
            'code_scanning_alerts': {
                'status': 'OK',
                'data': None
            }
        })
        verdict, detail = execute(ctrl, snap, {})
        self.assertEqual(
            verdict, 'ERROR',
            f"code_scanning_alerts must return ERROR on None data payload. Got: {verdict} ({detail})"
        )

    def test_alerts_untyped_payload_dict(self):
        """
        Scenario 19: Alert evaluator must return ERROR on dict payload for list endpoint.

        Defect in commit 30b1f83:
            When data is {} (dict instead of list of alerts), if not alerts evaluates to True,
            returning PASS instead of flagging the malformed data contract.
        Expected post-repair:
            Evaluator asserts isinstance(data, list). If data is a dict {}, returns ERROR.
        """
        ctrl = {'verification': {'kind': 'dependabot_alerts'}}
        snap = make_snapshot(extra={
            'dependabot_alerts': {
                'status': 'OK',
                'data': {}
            }
        })
        verdict, detail = execute(ctrl, snap, {})
        self.assertEqual(
            verdict, 'ERROR',
            f"dependabot_alerts must return ERROR on dict data payload. Got: {verdict} ({detail})"
        )

    # -------------------------------------------------------------------------
    # Cluster 8: Local Composite Action Recursive Pinning (Defect 12)
    # -------------------------------------------------------------------------

    def test_composite_action_unpinned_remote(self):
        """
        Scenario 20: workflow_pinning must detect unpinned action inside local composite action.

        Defect in commit 30b1f83:
            checks.py line 112 unconditionally executes continue immediately after detecting ./ prefix,
            making lines 113-133 DEAD CODE. Local composite action steps are NEVER scanned.
            Furthermore, line 114 contains an unbound variable bug ('files').
            An unpinned remote action (e.g. actions/setup-node@v3) inside a local composite action is ignored and passes!
        Expected post-repair:
            Evaluator resolves local composite action path, scans runs.steps, detects unpinned remote action,
            and returns FAIL.
        """
        workflow_yaml = (
            "name: CI\n"
            "on: [push]\n"
            "jobs:\n"
            "  build:\n"
            "    runs-on: ubuntu-latest\n"
            "    steps:\n"
            "      - uses: ./.github/actions/setup\n"
        )
        composite_action_yaml = (
            "name: Setup Environment\n"
            "description: Composite action to setup Node\n"
            "runs:\n"
            "  using: composite\n"
            "  steps:\n"
            "    - uses: actions/setup-node@v3\n"
        )
        snap = make_snapshot(files={
            '.github/workflows/ci.yml': workflow_yaml,
            '.github/actions/setup/action.yml': composite_action_yaml
        })
        ctrl = {'verification': {'kind': 'workflow_pinning'}}
        verdict, detail = execute(ctrl, snap, {})
        self.assertEqual(
            verdict, 'FAIL',
            f"workflow_pinning must fail on unpinned remote action inside local composite action. Got: {verdict} ({detail})"
        )
        self.assertIn(
            'setup-node@v3', detail,
            f"Failure detail must identify the unpinned action 'setup-node@v3'. Got: {detail}"
        )


if __name__ == '__main__':
    unittest.main()
