import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from ges.warning_pilot import inspect, execution_result, load, validate_plan


class WarningPilotTests(unittest.TestCase):
    def setUp(self):
        self.plan = {"repository_id": 1, "revision": "a" * 40, "plan_digest": "b" * 64, "checks": ["test"]}
        self.receipt = {**self.plan, "checks": [{"name": "test", "revision": "a" * 40,
                        "status": "completed", "conclusion": "success", "runner_id": 1,
                        "steps": [{"status": "completed", "conclusion": "success"}]}]}
        self.snapshot = {"repository_id": 1, "revision": "a" * 40, "observations": {"files": {
            "status": "OK", "complete": True, "data": {".github/workflows/ci.yml":
                "on: push\npermissions: {contents: read}\njobs: {test: {runs-on: ubuntu-24.04, steps: [{run: 'true'}]}}"}}}}

    def test_positive_is_observation_never_certification(self):
        r = inspect(self.snapshot, self.plan, self.receipt)
        self.assertTrue(all(f["status"] == "OBSERVED" for f in r["findings"]))
        self.assertFalse(r["compliance_certified"])
        self.assertFalse(r["native_enforcement_verified"])
        self.assertIn("evidence_authenticity", r["not_evaluated"])

    def test_missing_receipt_never_observed(self):
        self.assertEqual("NOT_VERIFIABLE", execution_result(self.plan, None)[0])

    def test_changed_identity_or_plan_never_observed(self):
        for key, value in (("revision", "c" * 40), ("repository_id", True), ("repository_id", 2), ("plan_digest", "d" * 64)):
            with self.subTest(key=key):
                r = copy.deepcopy(self.receipt); r[key] = value
                self.assertEqual("NOT_VERIFIABLE", execution_result(self.plan, r)[0])

    def test_check_inventory_and_revision_cannot_self_waive(self):
        for checks in ([], self.receipt["checks"] * 2, [{**self.receipt["checks"][0], "name": "other"}],
                       [{**self.receipt["checks"][0], "revision": "d" * 40}]):
            r = {**self.receipt, "checks": checks}
            self.assertEqual("NOT_VERIFIABLE", execution_result(self.plan, r)[0])

    def test_failed_cancelled_skipped_pending_checks(self):
        for outcome in ("failure", "cancelled", "skipped", "neutral", None):
            r = copy.deepcopy(self.receipt); r["checks"][0]["conclusion"] = outcome
            self.assertEqual("WARN", execution_result(self.plan, r)[0])

    def test_zero_step_or_zero_runner_not_execution(self):
        for key, value in (("runner_id", 0), ("runner_id", True), ("steps", []), ("steps", None)):
            r = copy.deepcopy(self.receipt); r["checks"][0][key] = value
            self.assertEqual("NOT_VERIFIABLE", execution_result(self.plan, r)[0])

    def test_failed_skipped_malformed_steps_never_observed(self):
        for step in ({"status": "completed", "conclusion": "failure"},
                     {"status": "completed", "conclusion": "skipped"}, {}, None):
            r = copy.deepcopy(self.receipt); r["checks"][0]["steps"] = [step]
            self.assertEqual("WARN", execution_result(self.plan, r)[0])

    def test_workflow_incomplete_permission_denied_symlink_and_duplicate_yaml(self):
        for mutate in (lambda s: s["observations"]["files"].update(complete=False),
                       lambda s: s["observations"]["files"].update(status="FORBIDDEN"),
                       lambda s: s.update(revision="c" * 40),
                       lambda s: s["observations"]["files"]["data"].update({".github/workflows/ci.yml": {"kind": "symlink"}}),
                       lambda s: s["observations"]["files"]["data"].update({".github/workflows/ci.yml": "jobs: {}\njobs: {}"})):
            s = copy.deepcopy(self.snapshot); mutate(s)
            self.assertTrue(all(f["status"] != "OBSERVED" for f in inspect(s, self.plan)["findings"][:2]))

    def test_write_permissions_and_mutable_actions_warn(self):
        s = copy.deepcopy(self.snapshot)
        s["observations"]["files"]["data"][".github/workflows/ci.yml"] = "on: push\npermissions: write-all\njobs: {test: {runs-on: ubuntu-24.04, steps: [{uses: 'actions/checkout@main'}]}}"
        self.assertTrue(all(f["status"] == "WARN" for f in inspect(s, self.plan)["findings"][:2]))

    def test_empty_or_duplicate_trusted_plan_rejected(self):
        for checks in ([], ["test", "test"], [True]):
            with self.assertRaises(ValueError): validate_plan({**self.plan, "checks": checks})

    def test_duplicate_json_keys_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "x.json"; p.write_text('{"x":1,"x":2}')
            with self.assertRaises(ValueError): load(str(p))

    def test_warning_exit_zero_but_bad_input_exit_two_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)
            for name, data in (("snapshot", self.snapshot), ("plan", self.plan)):
                (p / (name + ".json")).write_text(json.dumps(data))
            args = [sys.executable, "-m", "ges.warning_pilot", "--snapshot", str(p / "snapshot.json"),
                    "--plan", str(p / "plan.json"), "--output", str(p / "report.json")]
            self.assertEqual(0, subprocess.run(args, capture_output=True).returncode)
            self.assertEqual("NOT_VERIFIABLE", json.loads((p / "report.json").read_text())["findings"][2]["status"])
            self.assertEqual(2, subprocess.run(args, capture_output=True).returncode)
            (p / "plan.json").write_text("{}")
            self.assertEqual(2, subprocess.run(args, capture_output=True).returncode)
