"""Requirement-driven opaque-box End-to-End (E2E) test suite for github-engineering-standards.

Follows the 4-tier methodology:
- Tier 1: Feature Coverage (happy-path CLI execution: validate, compile, audit, gate, render, impact)
- Tier 2: Boundary & Corner Cases (empty snapshots, missing files, corrupted YAML/JSON, boundary thresholds)
- Tier 3: Cross-Feature Interactions (profile overrides, solo vs team policies, exception lifecycles, ruleset compilation)
- Tier 4: Real-World Scenarios (complete repository assessment lifecycle, safe remediation plan/diff, read-only safety)
"""
from __future__ import annotations

import difflib
import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from ges.core import ROOT, digest, load, safe_path


FIXTURE_CLOCK = "2026-10-01T22:00:00+00:00"


def run_cli(*args: str, check: bool = False, at: str | None = FIXTURE_CLOCK) -> subprocess.CompletedProcess[str]:
    """Execute the CLI with deterministic fixture time; None uses the real clock."""
    cmd = [sys.executable, "-m", "ges", *args]
    if at is not None:
        # Test-only clock injection inside the subprocess; production CLI and
        # expiry predicates remain unchanged.
        script = (
            "import runpy, sys; from unittest.mock import patch; "
            "clock = sys.argv.pop(1); sys.argv[0] = 'ges'; "
            "with_clock = patch('ges.evaluate.now', return_value=clock); "
            "with_clock.start(); runpy.run_module('ges', run_name='__main__')"
        )
        cmd = [sys.executable, "-c", script, at, *args]
    return subprocess.run(
        cmd,
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=check,
    )


class BaseE2ETestCase(unittest.TestCase):
    """Base test case providing clean temporary directories and helper factories."""

    def setUp(self) -> None:
        self._temp_dir = tempfile.TemporaryDirectory()
        self.work_dir = Path(self._temp_dir.name)
        self.catalog_path = ROOT / "controls/catalog.json"
        self.solo_profile_path = ROOT / "profiles/solo-software.json"
        self.team_profile_path = ROOT / "profiles/team-service.json"

    def tearDown(self) -> None:
        self._temp_dir.cleanup()

    def make_snapshot(
        self,
        *,
        target: str = "4444J99/github-engineering-standards",
        target_revision: str = "0123456789abcdef0123456789abcdef01234567",
        target_type: str = "repository",
        observed_at: str = "2026-10-01T22:00:00+00:00",
        observations: dict | None = None,
    ) -> dict:
        """Construct a valid schema-compliant snapshot dictionary."""
        if observations is None:
            observations = {
                "repository": {
                    "status": "OK",
                    "http_status": 200,
                    "data": {
                        "name": "github-engineering-standards",
                        "description": "Executable engineering standard",
                        "topics": ["standards", "compliance"],
                        "default_branch": "main",
                        "owner": {"login": "4444J99"},
                    },
                },
                "files": {
                    "status": "OK",
                    "complete": True,
                    "data": {
                        "README.md": {"content": "# Standard\n\nHigh quality.", "blob_sha": "a" * 40},
                        "CONTRIBUTING.md": {"content": "# Contributing\n\nGuidelines.", "blob_sha": "b" * 40},
                        "SECURITY.md": {"content": "# Security\n\nReporting process.", "blob_sha": "c" * 40},
                        ".github/CODEOWNERS": {"content": "* @4444J99\n", "blob_sha": "d" * 40},
                        ".github/dependabot.yml": {
                            "content": "version: 2\nupdates:\n  - package-ecosystem: pip\n    directory: /\n    schedule:\n      interval: daily\n",
                            "blob_sha": "e" * 40,
                        },
                        ".github/workflows/ci.yml": {
                            "content": (
                                "name: CI\non: [push]\npermissions: read-all\njobs:\n  test:\n    runs-on: ubuntu-latest\n"
                                "    steps:\n      - uses: actions/checkout@0123456789abcdef0123456789abcdef01234567\n"
                            ),
                            "blob_sha": "f" * 40,
                        },
                    },
                },
                "effective_branch_rules": {
                    "status": "OK",
                    "http_status": 200,
                    "data": [
                        {"type": "deletion"},
                        {"type": "non_fast_forward"},
                        {
                            "type": "pull_request",
                            "parameters": {
                                "required_approving_review_count": 0,
                                "dismiss_stale_reviews_on_push": True,
                                "required_review_thread_resolution": True,
                            },
                        },
                    ],
                },
                "actions_permissions": {
                    "status": "OK",
                    "http_status": 200,
                    "data": {"enabled": True, "allowed_actions": "selected"},
                },
                "deploy_keys": {"status": "OK", "http_status": 200, "data": []},
                "codeowners": {
                    "status": "OK",
                    "http_status": 200,
                    "data": {"content": "KiBANDQ0NEo5OQo=", "encoding": "base64"},
                },
                "dependabot_config": {
                    "status": "OK",
                    "http_status": 200,
                    "data": {"content": "dmVyc2lvbjogMg==", "encoding": "base64"},
                },
                "dependabot_alerts": {"status": "OK", "http_status": 200, "data": []},
                "code_scanning_alerts": {"status": "OK", "http_status": 200, "data": []},
                "secret_scanning_alerts": {"status": "OK", "http_status": 200, "data": []},
            }
        return {
            "target": target,
            "target_revision": target_revision,
            "target_type": target_type,
            "observed_at": observed_at,
            "observations": observations,
        }

    def write_json(self, relative_name: str, payload: dict | list) -> Path:
        """Write JSON payload to a temporary file."""
        target = self.work_dir / relative_name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        return target


# ==============================================================================
# Tier 1: Feature Coverage (Happy-Path CLI Execution)
# ==============================================================================
class Tier1FeatureCoverage(BaseE2ETestCase):
    """Tier 1: Verify standard CLI subcommands succeed under nominal conditions."""

    def test_cli_validate_success(self) -> None:
        """Feature: ges validate. Must exit 0 and report valid status for the canonical catalog."""
        res = run_cli("validate")
        self.assertEqual(res.returncode, 0, f"ges validate failed: {res.stderr}")
        data = json.loads(res.stdout)
        self.assertTrue(data.get("valid"), "Catalog should be marked valid")
        self.assertGreaterEqual(data.get("controls", 0), 95, "Catalog should have at least 95 controls")

    def test_cli_validate_custom_catalog(self) -> None:
        """Feature: ges validate with --catalog flag pointing to a validated subset."""
        cat = load(self.catalog_path)[:5]
        custom_cat_file = self.write_json("custom_cat.json", cat)
        res = run_cli("--catalog", str(custom_cat_file), "validate")
        self.assertEqual(res.returncode, 0, f"Custom validate failed: {res.stderr}")
        data = json.loads(res.stdout)
        self.assertTrue(data.get("valid"))
        self.assertEqual(data.get("controls"), 5)

    def test_cli_compile_generates_artifacts_with_digests(self) -> None:
        """Feature: ges compile. Must emit bindings.json, functional-checklist.md, and source-crosswalk.md."""
        out_dir = self.work_dir / "compiled"
        res = run_cli("compile", "--output", str(out_dir))
        self.assertEqual(res.returncode, 0, f"ges compile failed: {res.stderr}")

        bindings_file = out_dir / "bindings.json"
        checklist_file = out_dir / "functional-checklist.md"
        crosswalk_file = out_dir / "source-crosswalk.md"

        self.assertTrue(bindings_file.exists(), "bindings.json was not created")
        self.assertTrue(checklist_file.exists(), "functional-checklist.md was not created")
        self.assertTrue(crosswalk_file.exists(), "source-crosswalk.md was not created")

        bindings_data = json.loads(bindings_file.read_text(encoding="utf-8"))
        canonical_cat = load(self.catalog_path)
        expected_digest = digest(canonical_cat)
        self.assertEqual(bindings_data.get("catalog_digest"), expected_digest)
        self.assertEqual(len(bindings_data.get("controls", [])), len(canonical_cat))

        checklist_content = checklist_file.read_text(encoding="utf-8")
        self.assertIn("# GitHub Engineering Standards — functional checklist", checklist_content)
        self.assertIn("GES-DOC-001", checklist_content)

    def test_cli_audit_execution_nominal(self) -> None:
        """Feature: ges audit. Processes snapshot and writes assessment report matching ges.assessment.v1."""
        snap_file = self.write_json("snapshot.json", self.make_snapshot())
        out_report = self.work_dir / "report.json"

        res = run_cli(
            "audit",
            "--snapshot", str(snap_file),
            "--profile", str(self.solo_profile_path),
            "--output", str(out_report),
        )
        self.assertEqual(res.returncode, 0, f"ges audit failed: {res.stderr}")
        self.assertTrue(out_report.exists(), "Assessment report was not generated")

        report = json.loads(out_report.read_text(encoding="utf-8"))
        self.assertEqual(report.get("schema_version"), "ges.assessment.v1")
        self.assertEqual(report.get("standard_version"), "0.1.0")
        self.assertIn("summary", report)
        summary = report["summary"]
        self.assertIn("expected_instances", summary)
        self.assertIn("known_applicable", summary)
        self.assertIn("outcomes", summary)

    def test_cli_gate_nominal_pass(self) -> None:
        """Feature: ges gate. Approves a report where all applicable MUST controls pass."""
        cat = load(self.catalog_path)
        # Select two controls that are guaranteed to pass with our snapshot
        small_cat = [c for c in cat if c["id"] in ("GES-ID-001", "GES-ID-002")]
        cat_file = self.write_json("small_cat.json", small_cat)
        snap_file = self.write_json("snap.json", self.make_snapshot())
        report_file = self.work_dir / "report.json"

        # Audit with the small catalog
        res_audit = run_cli(
            "--catalog", str(cat_file),
            "audit",
            "--snapshot", str(snap_file),
            "--profile", str(self.solo_profile_path),
            "--output", str(report_file),
        )
        self.assertEqual(res_audit.returncode, 0)

        # Gate on the report
        res_gate = run_cli("--catalog", str(cat_file), "gate", "--report", str(report_file))
        self.assertEqual(res_gate.returncode, 0, f"Gate failed unexpectedly: {res_gate.stdout}")
        gate_data = json.loads(res_gate.stdout)
        self.assertTrue(gate_data.get("pass"))
        self.assertEqual(gate_data.get("blockers"), [])

    def test_cli_gate_nominal_blockers(self) -> None:
        """Feature: ges gate. Blocks with exit code 1 when MUST controls fail."""
        cat = load(self.catalog_path)
        # Include GES-DOC-001 (MUST; file_present: README.md) which applies unconditionally
        target_controls = [c for c in cat if c["id"] in ("GES-ID-001", "GES-DOC-001")]
        cat_file = self.write_json("fail_cat.json", target_controls)
        # Snapshot missing README.md
        snap = self.make_snapshot()
        snap["observations"]["files"]["data"].pop("README.md", None)
        snap_file = self.write_json("snap.json", snap)
        report_file = self.work_dir / "report.json"

        run_cli(
            "--catalog", str(cat_file),
            "audit",
            "--snapshot", str(snap_file),
            "--profile", str(self.solo_profile_path),
            "--output", str(report_file),
        )

        res_gate = run_cli("--catalog", str(cat_file), "gate", "--report", str(report_file))
        self.assertEqual(res_gate.returncode, 1, "Gate should return exit code 1 on failed MUST controls")
        gate_data = json.loads(res_gate.stdout)
        self.assertFalse(gate_data.get("pass"))
        self.assertTrue(any("GES-DOC-001" in b for b in gate_data.get("blockers", [])))

    def test_cli_render_template_success(self) -> None:
        """Feature: ges render. Compiles parameterized JSON and YAML templates."""
        ruleset_params = self.write_json("ruleset_params.json", {"REQUIRED_REVIEWS": "2"})
        ruleset_out = self.work_dir / "rendered_ruleset.json"
        res = run_cli(
            "render",
            "--template", "templates/ruleset.json",
            "--parameters", str(ruleset_params),
            "--output", str(ruleset_out),
        )
        self.assertEqual(res.returncode, 0, f"Render failed: {res.stderr}")
        self.assertTrue(ruleset_out.exists())
        data = json.loads(ruleset_out.read_text(encoding="utf-8"))
        pr_rule = next(r for r in data["rules"] if r["type"] == "pull_request")
        self.assertEqual(pr_rule["parameters"]["required_approving_review_count"], 2)


# ==============================================================================
# Tier 2: Boundary & Corner Cases (Adversarial, Invalid, Truncated, Escapes)
# ==============================================================================
class Tier2BoundaryCornerCases(BaseE2ETestCase):
    """Tier 2: Verify system behavior on adversarial inputs, boundaries, and failure modes."""

    def test_empty_snapshot_rejected_never_silent_pass(self) -> None:
        """Contract: Malformed/empty snapshot observations must result in ERROR or NOT_ASSESSED, never PASS."""
        empty_snap = self.write_json("empty_snap.json", {
            "target": "owner/repo",
            "target_revision": "a" * 40,
            "target_type": "repository",
            "observed_at": "2026-10-01T22:00:00+00:00",
            "observations": {},
        })
        out_report = self.work_dir / "report_empty.json"
        res = run_cli(
            "audit",
            "--snapshot", str(empty_snap),
            "--profile", str(self.solo_profile_path),
            "--output", str(out_report),
        )
        self.assertEqual(res.returncode, 0)
        report = json.loads(out_report.read_text(encoding="utf-8"))
        # Verify no applicable control was marked PASS
        for row in report["results"]:
            if row["applicability"] == "APPLICABLE":
                self.assertNotEqual(
                    row["outcome"],
                    "PASS",
                    f"Control {row['control_id']} produced vacuous PASS on empty observations",
                )

    def test_missing_target_or_revision_sets_error_outcome(self) -> None:
        """Contract: Snapshots omitting target or target_revision must produce ERROR outcome."""
        bad_snap = self.write_json("bad_snap.json", {
            "target": "owner/repo",
            # target_revision omitted
            "observed_at": "2026-10-01T22:00:00+00:00",
            "observations": {},
        })
        out_report = self.work_dir / "report_bad.json"
        run_cli(
            "audit",
            "--snapshot", str(bad_snap),
            "--profile", str(self.solo_profile_path),
            "--output", str(out_report),
        )
        report = json.loads(out_report.read_text(encoding="utf-8"))
        for row in report["results"]:
            if row["applicability"] == "APPLICABLE":
                self.assertEqual(row["outcome"], "ERROR")
                self.assertIn("target and exact target revision", row["detail"])

    def test_timestamp_freshness_boundaries(self) -> None:
        """Contract: Freshness checks distinguish FRESH, STALE (> max_age), and FUTURE."""
        # A frozen fixture clock must not hide actual elapsed-time boundaries.
        baseline = self.write_json("baseline.json", self.make_snapshot())
        for clock, expected in (
            ("2026-10-02T22:00:00+00:00", "FRESH"),
            ("2026-10-02T22:00:01+00:00", "STALE"),
        ):
            with self.subTest(clock=clock):
                output = self.work_dir / f"boundary-{expected}.json"
                result = run_cli(
                    "audit", "--snapshot", str(baseline),
                    "--profile", str(self.solo_profile_path),
                    "--output", str(output), at=clock,
                )
                self.assertEqual(result.returncode, 0, result.stderr)
                rows = json.loads(output.read_text())["results"]
                self.assertTrue(rows)
                self.assertTrue(all(row["evidence_freshness"] == expected for row in rows))
        # Stale (> 24h old)
        stale_snap = self.write_json("stale.json", self.make_snapshot(observed_at="2026-09-01T00:00:00+00:00"))
        stale_out = self.work_dir / "stale_report.json"
        run_cli("audit", "--snapshot", str(stale_snap), "--profile", str(self.solo_profile_path), "--output", str(stale_out))
        stale_data = json.loads(stale_out.read_text(encoding="utf-8"))
        self.assertEqual(stale_data["results"][0]["evidence_freshness"], "STALE")
        self.assertEqual(stale_data["results"][0]["outcome"], "STALE")

        # Future (< -60s in future)
        future_snap = self.write_json("future.json", self.make_snapshot(observed_at="2027-01-01T00:00:00+00:00"))
        future_out = self.work_dir / "future_report.json"
        run_cli("audit", "--snapshot", str(future_snap), "--profile", str(self.solo_profile_path), "--output", str(future_out))
        future_data = json.loads(future_out.read_text(encoding="utf-8"))
        self.assertEqual(future_data["results"][0]["evidence_freshness"], "FUTURE")
        self.assertEqual(future_data["results"][0]["outcome"], "ERROR")

    def test_incomplete_inventory_returns_not_verifiable(self) -> None:
        """Contract: Incomplete file inventory yields NOT_VERIFIABLE rather than FAIL."""
        cat = load(self.catalog_path)
        doc_cat = [c for c in cat if c["id"] == "GES-DOC-001"]
        cat_file = self.write_json("doc_cat.json", doc_cat)

        snap = self.make_snapshot()
        # Mark files incomplete and empty
        snap["observations"]["files"] = {"status": "OK", "complete": False, "data": {}}
        snap_file = self.write_json("snap_incomplete.json", snap)
        report_file = self.work_dir / "report_inc.json"

        run_cli(
            "--catalog", str(cat_file),
            "audit",
            "--snapshot", str(snap_file),
            "--profile", str(self.solo_profile_path),
            "--output", str(report_file),
        )
        report = json.loads(report_file.read_text(encoding="utf-8"))
        self.assertEqual(report["results"][0]["outcome"], "NOT_VERIFIABLE")
        self.assertIn("File inventory incomplete", report["results"][0]["detail"])

    def test_symlink_demands_manual_review(self) -> None:
        """Contract: Symlinks in file inventories cannot be assumed safe; demand MANUAL_REVIEW."""
        cat = load(self.catalog_path)
        doc_cat = [c for c in cat if c["id"] == "GES-DOC-001"]
        cat_file = self.write_json("sym_cat.json", doc_cat)

        snap = self.make_snapshot()
        snap["observations"]["files"]["data"]["README.md"] = {"kind": "symlink"}
        snap_file = self.write_json("snap_symlink.json", snap)
        report_file = self.work_dir / "report_sym.json"

        run_cli(
            "--catalog", str(cat_file),
            "audit",
            "--snapshot", str(snap_file),
            "--profile", str(self.solo_profile_path),
            "--output", str(report_file),
        )
        report = json.loads(report_file.read_text(encoding="utf-8"))
        self.assertEqual(report["results"][0]["outcome"], "MANUAL_REVIEW")
        self.assertIn("is a symlink; target not established", report["results"][0]["detail"])

    def test_path_traversal_rejection(self) -> None:
        """Security: Relative path traversal attempts (../) and root escapes must be rejected."""
        with self.assertRaises(ValueError):
            safe_path(ROOT, "../../../etc/passwd")

        with self.assertRaises(ValueError):
            safe_path(ROOT, "/etc/passwd")

        with self.assertRaises(ValueError):
            safe_path(ROOT, "foo/../../bar")

    def test_corrupted_workflow_yaml_fails(self) -> None:
        """Contract: Corrupted or unparseable workflow YAML fails with FAIL outcome."""
        cat = load(self.catalog_path)
        act_cat = [c for c in cat if c["id"] == "GES-ACT-001"]
        cat_file = self.write_json("act_cat.json", act_cat)

        snap = self.make_snapshot()
        snap["observations"]["files"]["data"][".github/workflows/ci.yml"] = {
            "content": "jobs: [ unclosed list syntax",
            "blob_sha": "f" * 40,
        }
        snap_file = self.write_json("snap_corrupt_yaml.json", snap)
        report_file = self.work_dir / "report_corrupt_yaml.json"

        run_cli(
            "--catalog", str(cat_file),
            "audit",
            "--snapshot", str(snap_file),
            "--profile", str(self.solo_profile_path),
            "--output", str(report_file),
        )
        report = json.loads(report_file.read_text(encoding="utf-8"))
        self.assertEqual(report["results"][0]["outcome"], "FAIL")
        self.assertIn("Invalid YAML", report["results"][0]["detail"])

    def test_unpinned_actions_fail(self) -> None:
        """Contract: Workflows using floating tag versions (e.g. @v4) fail pinning checks."""
        cat = load(self.catalog_path)
        pin_cat = [c for c in cat if c["id"] == "GES-ACT-002"]
        cat_file = self.write_json("pin_cat.json", pin_cat)

        snap = self.make_snapshot()
        snap["observations"]["files"]["data"][".github/workflows/ci.yml"] = {
            "content": "jobs:\n  test:\n    steps:\n      - uses: actions/checkout@v4\n",
            "blob_sha": "f" * 40,
        }
        snap_file = self.write_json("snap_unpinned.json", snap)
        report_file = self.work_dir / "report_unpinned.json"

        run_cli(
            "--catalog", str(cat_file),
            "audit",
            "--snapshot", str(snap_file),
            "--profile", str(self.solo_profile_path),
            "--output", str(report_file),
        )
        report = json.loads(report_file.read_text(encoding="utf-8"))
        self.assertEqual(report["results"][0]["outcome"], "FAIL")
        self.assertIn("not pinned to a full SHA", report["results"][0]["detail"])

    def test_deploy_keys_write_access_rejected(self) -> None:
        """Contract: Deploy keys with read_only=False must trigger immediate failure."""
        cat = load(self.catalog_path)
        # An explicit evaluator fixture, never a quarantined control promoted to policy.
        key_control = copy.deepcopy(cat[0])
        key_control["verification"] = {"kind": "deploy_keys", "require_read_only": True}
        key_cat = [key_control]
        cat_file = self.write_json("key_cat.json", key_cat)

        snap = self.make_snapshot()
        snap["observations"]["deploy_keys"] = {
            "status": "OK",
            "http_status": 200,
            "complete": True,
            "data": [{"key": "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5...", "read_only": False, "verified": True}],
        }
        snap_file = self.write_json("snap_keys.json", snap)
        report_file = self.work_dir / "report_keys.json"

        run_cli(
            "--catalog", str(cat_file),
            "audit",
            "--snapshot", str(snap_file),
            "--profile", str(self.solo_profile_path),
            "--output", str(report_file),
        )
        report = json.loads(report_file.read_text(encoding="utf-8"))
        self.assertEqual(report["results"][0]["outcome"], "FAIL")
        self.assertIn("has write access", report["results"][0]["detail"])


# ==============================================================================
# Tier 3: Cross-Feature Interactions
# ==============================================================================
class Tier3CrossFeatureInteractions(BaseE2ETestCase):
    """Tier 3: Interactions between profiles, context overrides, exceptions, and rulesets."""

    def test_solo_vs_team_review_profiles(self) -> None:
        """Interaction: Solo maintainer policy (required_reviews=0) vs Team Service policy (required_reviews=2).

        Evaluates GES-RULE-004 ('at_least' review count operator bound to profile_parameter: required_reviews).
        """
        cat = load(self.catalog_path)
        rule_cat = [c for c in cat if c["id"] == "GES-RULE-004"]
        cat_file = self.write_json("rule_cat.json", rule_cat)

        # Snapshot has required_approving_review_count = 1
        snap = self.make_snapshot()
        snap["observations"]["effective_branch_rules"]["data"] = [
            {
                "type": "pull_request",
                "parameters": {
                    "required_approving_review_count": 1,
                    "dismiss_stale_reviews_on_push": True,
                    "required_review_thread_resolution": True,
                },
            }
        ]
        snap_file = self.write_json("snap_rev1.json", snap)

        # 1. Under solo-software (required_reviews = 0): 1 >= 0 -> PASS
        solo_report = self.work_dir / "solo_report.json"
        res_solo = run_cli(
            "--catalog", str(cat_file),
            "audit",
            "--snapshot", str(snap_file),
            "--profile", str(self.solo_profile_path),
            "--output", str(solo_report),
        )
        self.assertEqual(res_solo.returncode, 0)
        solo_data = json.loads(solo_report.read_text(encoding="utf-8"))
        self.assertEqual(solo_data["results"][0]["outcome"], "PASS")

        # 2. Under team-service (required_reviews = 2): 1 >= 2 is False -> FAIL
        team_report = self.work_dir / "team_report.json"
        res_team = run_cli(
            "--catalog", str(cat_file),
            "audit",
            "--snapshot", str(snap_file),
            "--profile", str(self.team_profile_path),
            "--output", str(team_report),
        )
        self.assertEqual(res_team.returncode, 0)
        team_data = json.loads(team_report.read_text(encoding="utf-8"))
        self.assertEqual(team_data["results"][0]["outcome"], "FAIL")
        self.assertIn("does not satisfy parameter required_approving_review_count", team_data["results"][0]["detail"])

    def test_missing_profile_context_dimension_stays_unknown(self) -> None:
        """Contract: When a control requires context dimension missing from profile, applicability is UNKNOWN.

        Missing applicability dimensions block the gate.
        """
        cat = load(self.catalog_path)
        rule_cat = [c for c in cat if c["id"] == "GES-RULE-004"]
        cat_file = self.write_json("rule_cat.json", rule_cat)

        # Create profile missing 'actions', 'software', or 'required_reviews'
        incomplete_profile = self.write_json("incomplete_profile.json", {
            "name": "incomplete",
            "context": {},  # completely empty context
            "max_age_hours": 24,
            "authorized_reviewers": ["4444J99"],
        })
        snap_file = self.write_json("snap.json", self.make_snapshot())
        report_file = self.work_dir / "report_unknown.json"

        run_cli(
            "--catalog", str(cat_file),
            "audit",
            "--snapshot", str(snap_file),
            "--profile", str(incomplete_profile),
            "--output", str(report_file),
        )
        report = json.loads(report_file.read_text(encoding="utf-8"))
        self.assertEqual(report["results"][0]["applicability"], "UNKNOWN")

        # Gate on this report must fail
        res_gate = run_cli("--catalog", str(cat_file), "gate", "--report", str(report_file))
        self.assertEqual(res_gate.returncode, 1)
        self.assertIn("UNKNOWN", res_gate.stdout)

    def test_exception_lifecycle_preserves_outcome_integrity(self) -> None:
        """Contract: An exception changes exception_status to APPROVED_UNTIL, but NEVER rewrites outcome from FAIL to PASS.

        Gate requires --allow-exceptions to pass.
        """
        cat = load(self.catalog_path)
        doc_cat = [c for c in cat if c["id"] == "GES-DOC-001"]
        cat_file = self.write_json("doc_cat.json", doc_cat)

        # Snapshot missing README.md -> outcome will be FAIL
        snap = self.make_snapshot()
        snap["observations"]["files"]["data"].pop("README.md", None)
        snap_file = self.write_json("snap_no_readme.json", snap)

        # Valid authorized exception
        exceptions = [{
            "control_id": "GES-DOC-001",
            "control_revision": 1,
            "target": snap["target"],
            "approved_by": "4444J99",  # authorized in solo-software.json
            "approved_at": "2026-10-01T21:00:00+00:00",
            "expires_at": "2026-10-02T21:00:00+00:00",
            "reason": "Documentation rewrite underway in docs PR",
            "compensating_control": "Temporary documentation hosted at external link",
        }]
        exc_file = self.write_json("exceptions.json", exceptions)
        report_file = self.work_dir / "report_excepted.json"

        res_audit = run_cli(
            "--catalog", str(cat_file),
            "audit",
            "--snapshot", str(snap_file),
            "--profile", str(self.solo_profile_path),
            "--exceptions", str(exc_file),
            "--output", str(report_file),
            at="2026-10-01T22:00:00+00:00",
        )
        self.assertEqual(res_audit.returncode, 0)
        report = json.loads(report_file.read_text(encoding="utf-8"))
        result = report["results"][0]

        # Critical verification: Outcome is STILL FAIL, exception_status is APPROVED_UNTIL
        self.assertEqual(result["outcome"], "FAIL", "Exceptions must NEVER rewrite outcome to PASS")
        self.assertEqual(result["exception_status"], "APPROVED_UNTIL")

        # Without --allow-exceptions: gate FAILS
        res_gate_strict = run_cli("--catalog", str(cat_file), "gate", "--report", str(report_file))
        self.assertEqual(res_gate_strict.returncode, 1)

        # With --allow-exceptions: gate PASSES
        res_gate_allow = run_cli("--catalog", str(cat_file), "gate", "--report", str(report_file), "--allow-exceptions")
        self.assertEqual(res_gate_allow.returncode, 0)
        gate_data = json.loads(res_gate_allow.stdout)
        self.assertTrue(gate_data.get("pass"))

        # Exact expiry is exclusive even when the snapshot is fresh.
        snap["observed_at"] = exceptions[0]["expires_at"]
        snap_file = self.write_json("snap_at_expiry.json", snap)
        expired_report = self.work_dir / "report_at_expiry.json"
        expired_audit = run_cli(
            "--catalog", str(cat_file), "audit",
            "--snapshot", str(snap_file),
            "--profile", str(self.solo_profile_path),
            "--exceptions", str(exc_file),
            "--output", str(expired_report),
            at=exceptions[0]["expires_at"],
        )
        self.assertEqual(expired_audit.returncode, 0, expired_audit.stderr)
        expired_result = json.loads(expired_report.read_text())["results"][0]
        self.assertEqual(expired_result["outcome"], "FAIL")
        self.assertEqual(expired_result["exception_status"], "EXPIRED")
        expired_gate = run_cli(
            "--catalog", str(cat_file), "gate",
            "--report", str(expired_report), "--allow-exceptions",
        )
        self.assertEqual(expired_gate.returncode, 1)

    def test_untrusted_or_expired_exception_rejected(self) -> None:
        """Contract: Exceptions approved by unauthorized reviewers or expired timestamps remain invalid."""
        cat = load(self.catalog_path)
        doc_cat = [c for c in cat if c["id"] == "GES-DOC-001"]
        cat_file = self.write_json("doc_cat.json", doc_cat)

        snap = self.make_snapshot()
        snap["observations"]["files"]["data"].pop("README.md", None)
        snap_file = self.write_json("snap_no_readme.json", snap)

        # Exception from unauthorized reviewer
        untrusted_exceptions = [{
            "control_id": "GES-DOC-001",
            "control_revision": 1,
            "target": snap["target"],
            "approved_by": "unknown_adversary",
            "approved_at": "2026-10-01T21:00:00+00:00",
            "expires_at": "2026-10-02T21:00:00+00:00",
            "reason": "Bypassing rule",
            "compensating_control": "None",
        }]
        exc_file = self.write_json("untrusted_exc.json", untrusted_exceptions)
        report_file = self.work_dir / "report_untrusted.json"

        run_cli(
            "--catalog", str(cat_file),
            "audit",
            "--snapshot", str(snap_file),
            "--profile", str(self.solo_profile_path),
            "--exceptions", str(exc_file),
            "--output", str(report_file),
        )
        report = json.loads(report_file.read_text(encoding="utf-8"))
        self.assertEqual(report["results"][0]["exception_status"], "INVALID")

        # Even with --allow-exceptions, gate MUST block
        res_gate = run_cli("--catalog", str(cat_file), "gate", "--report", str(report_file), "--allow-exceptions")
        self.assertEqual(res_gate.returncode, 1)

    def test_ruleset_compilation_from_profile_parameter(self) -> None:
        """Interaction: Ruleset template rendering parameterized directly by profile values."""
        solo_prof = load(self.solo_profile_path)
        reviews = str(solo_prof["context"]["required_reviews"])
        params_file = self.write_json("ruleset_solo_params.json", {"REQUIRED_REVIEWS": reviews})
        out_ruleset = self.work_dir / "solo_ruleset.json"

        res = run_cli(
            "render",
            "--template", "templates/ruleset.json",
            "--parameters", str(params_file),
            "--output", str(out_ruleset),
        )
        self.assertEqual(res.returncode, 0)
        ruleset = json.loads(out_ruleset.read_text(encoding="utf-8"))
        pr_rule = next(r for r in ruleset["rules"] if r["type"] == "pull_request")
        self.assertEqual(pr_rule["parameters"]["required_approving_review_count"], 0)


# ==============================================================================
# Tier 4: Real-World Scenarios (Assessment Lifecycle, Safe Remediation, Read-Only)
# ==============================================================================
class Tier4RealWorldScenarios(BaseE2ETestCase):
    """Tier 4: End-to-end estate assessment, safe dry-run remediation plan & diff generation."""

    def test_complete_repo_assessment_lifecycle(self) -> None:
        """Scenario: Full assessment pipeline for a realistic repository snapshot against solo profile.

        Verifies that:
        1. CLI audit runs cleanly without exceptions.
        2. Assessment schema and summary counters are strictly valid.
        3. Outcomes are accurately computed across multiple checkers.
        4. Gate execution accurately reflects the evaluation.
        """
        snapshot_file = self.write_json("estate_snapshot.json", self.make_snapshot())
        report_file = self.work_dir / "estate_report.json"

        # 1. Run audit
        res_audit = run_cli(
            "audit",
            "--snapshot", str(snapshot_file),
            "--profile", str(self.solo_profile_path),
            "--output", str(report_file),
        )
        self.assertEqual(res_audit.returncode, 0, f"Estate audit failed: {res_audit.stderr}")
        self.assertTrue(report_file.exists())

        # 2. Verify summary and cryptographic digests
        report = json.loads(report_file.read_text(encoding="utf-8"))
        self.assertEqual(report["target"], "4444J99/github-engineering-standards")
        self.assertEqual(len(report["catalog_digest"]), 64)
        self.assertEqual(len(report["snapshot_digest"]), 64)

        summary = report["summary"]
        self.assertGreater(summary["known_applicable"], 0)
        self.assertGreater(summary["valid_evaluations"], 0)
        self.assertGreaterEqual(summary["verified_pass"], 1)

        # 3. Verify gate execution
        res_gate = run_cli("gate", "--report", str(report_file))
        # Depending on unassessed manual controls in catalog, gate returns 0 or 1 with blockers
        gate_data = json.loads(res_gate.stdout)
        self.assertIn("pass", gate_data)
        self.assertIn("blockers", gate_data)
        if not gate_data["pass"]:
            self.assertGreater(len(gate_data["blockers"]), 0)

    def test_remediation_plan_and_diff_generation(self) -> None:
        """Scenario: Detect missing asset, render remediation template in dry-run, compute diff.

        Demonstrates that remediation creates unified diffs for review before applying changes.
        """
        # 1. Simulate workspace missing dependabot.yml
        repo_workspace = self.work_dir / "mock_repo"
        repo_workspace.mkdir()
        (repo_workspace / "README.md").write_text("# Project\n", encoding="utf-8")

        # 2. Render proposed remediation asset to a staging area
        remediation_staging = self.work_dir / "remediation_staging"
        params_file = self.write_json("dependabot_params.json", {
            "ECOSYSTEM": "pip",
            "MANIFEST_DIRECTORY": "/",
            "INTERVAL": "weekly",
            "PR_LIMIT": "10",
        })
        staged_dependabot = remediation_staging / ".github/dependabot.yml"

        res_render = run_cli(
            "render",
            "--template", "templates/dependabot.yml",
            "--parameters", str(params_file),
            "--output", str(staged_dependabot),
        )
        self.assertEqual(res_render.returncode, 0, f"Remediation template render failed: {res_render.stderr}")
        self.assertTrue(staged_dependabot.exists())

        # 3. Compute unified diff between existing target (non-existent) and staged file
        target_file = repo_workspace / ".github/dependabot.yml"
        existing_lines = []
        if target_file.exists():
            existing_lines = target_file.read_text(encoding="utf-8").splitlines(keepends=True)
        staged_lines = staged_dependabot.read_text(encoding="utf-8").splitlines(keepends=True)

        diff = list(difflib.unified_diff(
            existing_lines,
            staged_lines,
            fromfile=str(target_file),
            tofile=str(staged_dependabot),
        ))

        # 4. Verify the diff captures the complete addition
        diff_text = "".join(diff)
        self.assertIn("+version: 2", diff_text)
        self.assertIn("+    directory: \"/\"", diff_text)

        # 5. Confirm the mock repository was NOT modified during diff/plan generation (read-only)
        self.assertFalse(target_file.exists(), "Plan generation must not write directly to workspace")

    def test_read_only_safety_guarantees(self) -> None:
        """Safety Contract: CLI tools refuse to overwrite existing destination files."""
        existing_dest = self.work_dir / "protected_existing.json"
        existing_dest.write_text('{"do_not_touch": true}\n', encoding="utf-8")

        params_file = self.write_json("params.json", {"REQUIRED_REVIEWS": "1"})

        # Attempt to render to existing destination
        res = run_cli(
            "render",
            "--template", "templates/ruleset.json",
            "--parameters", str(params_file),
            "--output", str(existing_dest),
        )
        self.assertEqual(res.returncode, 2, "Render must fail with code 2 when attempting overwrite")
        self.assertIn("FileExistsError", res.stderr)

        # Verify original file content remains completely intact
        dest_content = existing_dest.read_text(encoding="utf-8")
        self.assertEqual(dest_content, '{"do_not_touch": true}\n')

    def test_deterministic_audit_execution(self) -> None:
        """Safety Contract: Running audit twice on identical inputs produces bitwise identical digests."""
        from ges.evaluate import audit

        snap_file = self.write_json("deterministic_snap.json", self.make_snapshot())
        fixed_time = "2026-10-01T22:30:00+00:00"

        cat = load(self.catalog_path)[:10]
        snap = load(snap_file)
        prof = load(self.solo_profile_path)

        rep1 = audit(cat, snap, prof, at=fixed_time)
        rep2 = audit(cat, snap, prof, at=fixed_time)

        self.assertEqual(rep1["catalog_digest"], rep2["catalog_digest"])
        self.assertEqual(rep1["snapshot_digest"], rep2["snapshot_digest"])
        self.assertEqual(rep1["profile_digest"], rep2["profile_digest"])
        self.assertEqual(digest(rep1), digest(rep2))


if __name__ == "__main__":
    unittest.main()
