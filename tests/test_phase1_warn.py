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

    def test_non_mapping_yaml_top_level_emits_finding_without_crash(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            wfdir = tmppath / ".github" / "workflows"
            wfdir.mkdir(parents=True)

            # Non-empty sequence top level
            (wfdir / "list.yml").write_text("- one\n- two\n")
            # Scalar top level
            (wfdir / "scalar.yml").write_text("just_a_string\n")
            # Valid mapping control
            (wfdir / "valid.yml").write_text("name: valid\non: push\njobs: {}\npermissions: {}\nconcurrency: c\n")

            findings = check.check_repo(tmppath)
            yaml_parse_findings = [f for f in findings if f["rule"] == "yaml-parse"]
            self.assertEqual(len(yaml_parse_findings), 2)
            self.assertEqual(yaml_parse_findings[0]["where"], ".github/workflows/list.yml")
            self.assertEqual(yaml_parse_findings[0]["message"], "top-level YAML document must be a mapping")
            self.assertEqual(yaml_parse_findings[1]["where"], ".github/workflows/scalar.yml")
            self.assertEqual(yaml_parse_findings[1]["message"], "top-level YAML document must be a mapping")

            # In warn-only mode (default), main exits 0
            self.assertEqual(check.main([str(tmppath)]), 0)
            # Under --enforce, main exits 1 without a traceback
            self.assertEqual(check.main([str(tmppath), "--enforce"]), 1)


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
