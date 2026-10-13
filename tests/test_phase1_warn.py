import json, os, subprocess, sys, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "standards" / "phase1"))
import check  # noqa: E402
import honest_green  # noqa: E402

FX = ROOT / "tests" / "fixtures" / "phase1"


class Phase1Checks(unittest.TestCase):
    def test_pass_fixture_has_no_findings(self):
        self.assertEqual(check.check_repo(FX / "pass"), [])

    def test_fail_fixture_trips_each_rule(self):
        rules = {f["rule"] for f in check.check_repo(FX / "fail")}
        self.assertEqual(rules, {
            "least-privilege-permissions", "pin-runner-image", "job-timeout", "concurrency",
            "no-masked-failures", "pin-by-sha", "dependabot-configured", "lockfile-committed",
        })

    def test_warn_only_exit_zero_and_enforce_exit_one(self):
        self.assertEqual(check.main([str(FX / "fail")]), 0)
        self.assertEqual(check.main([str(FX / "fail"), "--enforce"]), 1)


class HonestGreen(unittest.TestCase):
    def test_all_success_is_green(self):
        self.assertEqual(honest_green.evaluate({"a": {"result": "success"}}), [])

    def test_skipped_cancelled_failure_are_not_green(self):
        for r in ("skipped", "cancelled", "failure", None):
            self.assertTrue(honest_green.evaluate({"a": {"result": r}}), r)

    def test_zero_step_success_is_not_green(self):
        p = honest_green.evaluate({"a": {"result": "success"}}, [{"name": "a", "conclusion": "success", "steps": []}])
        self.assertTrue(p)

    def test_empty_needs_is_not_green(self):
        self.assertTrue(honest_green.evaluate({}))


if __name__ == "__main__":
    unittest.main()
