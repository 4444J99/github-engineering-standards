"""Regression guards for independently reviewed GHQR source mappings."""

import json
from pathlib import Path
import unittest

from ges.checks import execute


ROOT = Path(__file__).resolve().parents[1]


class BranchSourceReconciliation(unittest.TestCase):
    def setUp(self):
        self.controls = {
            c["id"]: c for c in json.loads((ROOT / "controls/catalog.json").read_text())
        }
        self.review = json.loads(
            (ROOT / "evidence/source-reviews/ghqr-branch-protection-claims.json").read_text()
        )

    def test_specific_objectives_have_matching_definitions(self):
        expected = {
            "GES-RULE-001": {"repo-bp-011"},
            "GES-RULE-002": {"repo-bp-010"},
            "GES-RULE-003": {"repo-bp-006"},
            "GES-RULE-004": {"repo-bp-002", "repo-bp-003"},
            "GES-RULE-005": {"repo-bp-004"},
        }
        claims = {c["source_id"]: c for c in self.review["claims"]}
        for control_id, definition_ids in expected.items():
            control = self.controls[control_id]
            self.assertGreaterEqual(control["revision"], 2)
            sources = [s for s in control["sources"] if s["repository"] == "microsoft/ghqr"]
            self.assertEqual({s["section"] for s in sources}, definition_ids)
            for source in sources:
                claim = claims[source["section"]]
                self.assertEqual(source["start_line"], claim["start_line"])
                self.assertEqual(source["end_line"], claim["end_line"])
                self.assertIn(control_id, claim["proposed_control_ids"])
                self.assertFalse(claim["accepted_policy"])

    def test_information_is_not_thread_resolution_evidence(self):
        sources = self.controls["GES-RULE-006"]["sources"]
        ghqr = next(s for s in sources if s["repository"] == "microsoft/ghqr")
        self.assertEqual(ghqr["support_role"], "BACKGROUND_ONLY_NOT_EVIDENCE_FOR_THREAD_RESOLUTION")
        self.assertFalse(self.review["independent_omission_audit"])

    def test_review_quorum_remains_profile_parameterized(self):
        binding = self.controls["GES-RULE-004"]["verification"]
        self.assertEqual(binding["profile_parameter"], "required_reviews")
        self.assertEqual(binding["operator"], "at_least")
        self.assertEqual(self.review["policy_adoption"], "NONE")

    def test_thread_resolution_has_objective_specific_manual_source(self):
        control = self.controls["GES-RULE-006"]
        source = next(s for s in control["sources"] if s["path"].endswith("MANUAL_CHECKS.md"))
        review = json.loads((ROOT / "evidence/source-reviews/ghqr-manual-checks-claims.json").read_text())
        claim = next(c for c in review["claims"] if c["start_line"] == source["start_line"])
        self.assertIn(control["id"], claim["proposed_control_ids"])
        self.assertFalse(claim["accepted_policy"])
        self.assertEqual(source["start_line"], 136)
        self.assertEqual(control["status"], "REVIEWED_DRAFT")
        self.assertFalse(control["enforcement"]["native_deployed"])

    def test_malformed_required_check_parameters_do_not_crash(self):
        control = {"verification": {"kind": "effective_rule", "rule_type": "required_status_checks"}}
        snapshot = {"observations": {"effective_branch_rules": {"status": "OK", "data": [
            {"type": "required_status_checks", "parameters": []}
        ]}}}
        self.assertEqual(execute(control, snapshot, {})[0], "ERROR")

    def test_empty_required_check_context_does_not_pass(self):
        control = {"verification": {"kind": "effective_rule", "rule_type": "required_status_checks"}}
        snapshot = {"observations": {"effective_branch_rules": {"status": "OK", "data": [
            {"type": "required_status_checks", "parameters": {"required_status_checks": [{"context": ""}]}}
        ]}}}
        self.assertEqual(execute(control, snapshot, {})[0], "FAIL")

    def test_named_required_check_is_configuration_pass_only(self):
        control = {"verification": {"kind": "effective_rule", "rule_type": "required_status_checks"}}
        snapshot = {"observations": {"effective_branch_rules": {"status": "OK", "data": [
            {"type": "required_status_checks", "parameters": {"required_status_checks": [{"context": "build"}]}}
        ]}}}
        self.assertEqual(execute(control, snapshot, {})[0], "PASS")
        self.assertNotIn("enforcement_verified", snapshot)

    def test_null_required_check_list_is_error(self):
        control = {"verification": {"kind": "effective_rule", "rule_type": "required_status_checks"}}
        snapshot = {"observations": {"effective_branch_rules": {"status": "OK", "data": [
            {"type": "required_status_checks", "parameters": {"required_status_checks": None}}
        ]}}}
        self.assertEqual(execute(control, snapshot, {})[0], "ERROR")

    def test_negative_review_threshold_is_invalid_policy(self):
        control = self.controls["GES-RULE-004"]
        snapshot = {"observations": {"effective_branch_rules": {"status": "OK", "data": [
            {"type": "pull_request", "parameters": {"required_approving_review_count": 0}}
        ]}}}
        self.assertEqual(execute(control, snapshot, {"required_reviews": -1})[0], "ERROR")


if __name__ == "__main__":
    unittest.main()
