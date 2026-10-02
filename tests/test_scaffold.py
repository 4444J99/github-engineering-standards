import copy
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from ges.core import ROOT, digest, load
from ges.render import render_template_text
from ges.scaffold import plan_scaffold, write_scaffold

CONTROLS = load(ROOT / "controls/catalog.json")
ARTIFACT_CATALOG = load(ROOT / "factory/artifacts.json")
REPOSITORY_SPEC = load(ROOT / "examples/repository-spec.json")


def plan(profile_name="solo-software", *, controls=None, spec=None, artifacts=None):
    selected_spec = copy.deepcopy(REPOSITORY_SPEC if spec is None else spec)
    selected_spec["standard"]["profile"] = profile_name
    if profile_name == "archive":
        selected_spec["template_parameters"]["SUPPORT_AND_CONTRIBUTION"] = (
            "See GOVERNANCE.md and SECURITY.md. This archived repository does not "
            "accept contributions or community participation."
        )
    return plan_scaffold(
        ROOT,
        copy.deepcopy(CONTROLS if controls is None else controls),
        selected_spec,
        load(ROOT / f"profiles/{profile_name}.json"),
        copy.deepcopy(ARTIFACT_CATALOG if artifacts is None else artifacts),
    )


def tree_bytes(root):
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in root.rglob("*")
        if path.is_file()
    }


class ScaffoldPlanning(unittest.TestCase):
    def test_generation_is_byte_identical(self):
        first = plan()
        second = plan()
        self.assertEqual(first.files, second.files)
        self.assertEqual(first.manifest, second.manifest)

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            first_output = root / "first"
            second_output = root / "second"
            write_scaffold(first, first_output)
            write_scaffold(second, second_output)
            self.assertEqual(tree_bytes(first_output), tree_bytes(second_output))

    def test_solo_profile_selects_and_omits_expected_artifacts(self):
        scaffold = plan()
        materialized = {
            item["destination"]
            for item in scaffold.manifest["artifacts"]["materialized"]
        }
        omitted = {
            item["destination"] for item in scaffold.manifest["artifacts"]["omitted"]
        }

        self.assertEqual(
            materialized,
            {
                "README.md",
                "CONTRIBUTING.md",
                "GOVERNANCE.md",
                "SECURITY.md",
                "CODE_OF_CONDUCT.md",
                ".github/CODEOWNERS",
                ".github/pull_request_template.md",
                ".github/ISSUE_TEMPLATE/bug_report.yml",
                ".github/ISSUE_TEMPLATE/feature_request.yml",
                ".github/dependabot.yml",
            },
        )
        self.assertEqual(omitted, {"CITATION.cff", ".github/FUNDING.yml"})
        self.assertTrue(materialized.issubset(scaffold.files))
        self.assertTrue(omitted.isdisjoint(scaffold.files))

    def test_archive_profile_does_not_generate_contributing(self):
        scaffold = plan("archive")
        omitted = {
            item["destination"]: item
            for item in scaffold.manifest["artifacts"]["omitted"]
        }

        self.assertNotIn("CONTRIBUTING.md", scaffold.files)
        self.assertIn("CONTRIBUTING.md", omitted)
        self.assertEqual(
            omitted["CONTRIBUTING.md"]["selection_control"]["applicability"],
            "NOT_APPLICABLE_WITH_REASON",
        )
        self.assertIn(
            "accepts_contributions=False",
            omitted["CONTRIBUTING.md"]["selection_control"]["reason"],
        )

        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "archive"
            write_scaffold(scaffold, output)
            self.assertFalse((output / "CONTRIBUTING.md").exists())

    def test_manifest_hashes_and_status_boundaries_match_outputs(self):
        scaffold = plan()
        manifest = scaffold.manifest
        manifest_path = ".ges/generation-manifest.json"
        expected_outputs = sorted(set(scaffold.files) - {manifest_path})

        self.assertEqual(
            [item["path"] for item in manifest["outputs"]],
            expected_outputs,
        )
        for item in manifest["outputs"]:
            self.assertEqual(
                item["sha256"],
                hashlib.sha256(
                    scaffold.files[item["path"]].encode("utf-8")
                ).hexdigest(),
            )
        self.assertEqual(
            manifest["standard_lock_sha256"],
            hashlib.sha256(
                scaffold.files[".ges/standard.lock.json"].encode("utf-8")
            ).hexdigest(),
        )
        standard_lock = json.loads(scaffold.files[".ges/standard.lock.json"])
        generator_sources = standard_lock["generator"]["sources"]
        self.assertEqual(
            {source["path"] for source in generator_sources},
            {
                "ges/__init__.py",
                "ges/__main__.py",
                "ges/core.py",
                "ges/render.py",
                "ges/scaffold.py",
                "ges/yamlutil.py",
                "requirements.txt",
            },
        )
        for source in generator_sources:
            self.assertEqual(
                source["sha256"],
                hashlib.sha256((ROOT / source["path"]).read_bytes()).hexdigest(),
            )
        self.assertEqual(
            standard_lock["generator"]["sources_sha256"],
            digest(generator_sources),
        )
        for artifact in manifest["artifacts"]["materialized"]:
            self.assertEqual(
                artifact["template_sha256"],
                hashlib.sha256((ROOT / artifact["template"]).read_bytes()).hexdigest(),
            )
            self.assertEqual(
                artifact["output_sha256"],
                hashlib.sha256(
                    scaffold.files[artifact["destination"]].encode("utf-8")
                ).hexdigest(),
            )
        self.assertEqual(
            manifest["status_boundary"],
            {
                "policy_adoption": "NOT_RECORDED",
                "compliance": "NOT_ASSESSED",
                "semantic_review": "NOT_ESTABLISHED",
                "native_changes_applied": False,
                "git_repository_initialized": False,
                "remote_repository_created": False,
            },
        )
        self.assertEqual(json.loads(scaffold.files[manifest_path]), manifest)
        self.assertNotIn("ACCEPTED", {item["status"] for item in manifest["controls"]})

    def test_existing_output_and_dangling_symlink_are_not_overwritten(self):
        scaffold = plan()
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            existing = root / "existing"
            existing.mkdir()
            sentinel = existing / "sentinel.txt"
            sentinel.write_text("preserve me", encoding="utf-8")

            with self.assertRaisesRegex(FileExistsError, "Refusing to overwrite"):
                write_scaffold(scaffold, existing)
            self.assertEqual(sentinel.read_text(encoding="utf-8"), "preserve me")

            dangling = root / "dangling"
            dangling.symlink_to(root / "missing-target")
            self.assertFalse(dangling.exists())
            self.assertTrue(os.path.lexists(dangling))
            with self.assertRaisesRegex(FileExistsError, "Refusing to overwrite"):
                write_scaffold(scaffold, dangling)
            self.assertTrue(dangling.is_symlink())
            self.assertEqual(os.readlink(dangling), str(root / "missing-target"))

    def test_interrupt_during_publication_removes_partial_tree(self):
        scaffold = plan()
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            output = root / "generated"
            original_rename = Path.rename
            moves = 0

            def interrupt_after_first_move(source, target):
                nonlocal moves
                result = original_rename(source, target)
                moves += 1
                if moves == 1:
                    raise KeyboardInterrupt
                return result

            with (
                mock.patch.object(Path, "rename", interrupt_after_first_move),
                self.assertRaises(KeyboardInterrupt),
            ):
                write_scaffold(scaffold, output)

            self.assertFalse(os.path.lexists(output))
            self.assertEqual(list(root.iterdir()), [])

    def test_unknown_applicability_is_a_planning_error(self):
        profile = load(ROOT / "profiles/solo-software.json")
        profile["context"].pop("accepts_contributions")

        with self.assertRaisesRegex(
            ValueError,
            r"Profile leaves applicability UNKNOWN.*GES-DOC-002",
        ):
            plan_scaffold(
                ROOT,
                copy.deepcopy(CONTROLS),
                copy.deepcopy(REPOSITORY_SPEC),
                profile,
                copy.deepcopy(ARTIFACT_CATALOG),
            )

    def test_profile_types_and_spec_binding_fail_closed(self):
        malformed = load(ROOT / "profiles/solo-software.json")
        malformed["context"]["software"] = "true"
        with self.assertRaisesRegex(
            ValueError, "profile.context.software must have type bool"
        ):
            plan_scaffold(
                ROOT,
                copy.deepcopy(CONTROLS),
                copy.deepcopy(REPOSITORY_SPEC),
                malformed,
                copy.deepcopy(ARTIFACT_CATALOG),
            )

        promoted = load(ROOT / "profiles/solo-software.json")
        promoted["policy_status"] = "ACCEPTED"
        with self.assertRaisesRegex(
            ValueError,
            "profile.policy_status must be DRAFT_REQUIRES_TARGET_ADOPTION",
        ):
            plan_scaffold(
                ROOT,
                copy.deepcopy(CONTROLS),
                copy.deepcopy(REPOSITORY_SPEC),
                promoted,
                copy.deepcopy(ARTIFACT_CATALOG),
            )

        missing_parameter = load(ROOT / "profiles/solo-software.json")
        missing_parameter["context"].pop("required_reviews")
        with self.assertRaisesRegex(
            ValueError,
            "profile.context missing required parameter: required_reviews",
        ):
            plan_scaffold(
                ROOT,
                copy.deepcopy(CONTROLS),
                copy.deepcopy(REPOSITORY_SPEC),
                missing_parameter,
                copy.deepcopy(ARTIFACT_CATALOG),
            )

        archive = load(ROOT / "profiles/archive.json")
        with self.assertRaisesRegex(
            ValueError,
            "Repository spec requires profile solo-software; received archive",
        ):
            plan_scaffold(
                ROOT,
                copy.deepcopy(CONTROLS),
                copy.deepcopy(REPOSITORY_SPEC),
                archive,
                copy.deepcopy(ARTIFACT_CATALOG),
            )

    def test_rendered_output_cannot_reference_an_omitted_artifact(self):
        archive_spec = copy.deepcopy(REPOSITORY_SPEC)
        archive_spec["standard"]["profile"] = "archive"
        with self.assertRaisesRegex(
            ValueError,
            "Rendered output references omitted artifact CONTRIBUTING.md: README.md",
        ):
            plan_scaffold(
                ROOT,
                copy.deepcopy(CONTROLS),
                archive_spec,
                load(ROOT / "profiles/archive.json"),
                copy.deepcopy(ARTIFACT_CATALOG),
            )

    def test_stale_artifact_control_revision_is_rejected(self):
        artifacts = copy.deepcopy(ARTIFACT_CATALOG)
        artifacts["artifacts"][0]["control_revision"] += 1
        with self.assertRaisesRegex(
            ValueError,
            r"Stale artifact control revision: GES-DOC-001 expected 1",
        ):
            plan(artifacts=artifacts)

    def test_required_unsupported_capabilities_cannot_be_erased(self):
        artifacts = copy.deepcopy(ARTIFACT_CATALOG)
        artifacts["unsupported"] = []
        with self.assertRaisesRegex(
            ValueError,
            "Artifact catalog missing required unsupported capabilities",
        ):
            plan(artifacts=artifacts)

    def test_template_output_and_digest_use_the_same_byte_snapshot(self):
        readme = (ROOT / "templates/README.md").resolve()
        original_read_bytes = Path.read_bytes
        sentinel = b"\nSnapshot sentinel.\n"

        def read_snapshot(path):
            source = original_read_bytes(path)
            if path.resolve() == readme:
                return source + sentinel
            return source

        with mock.patch.object(Path, "read_bytes", read_snapshot):
            scaffold = plan()

        readme_artifact = next(
            item
            for item in scaffold.manifest["artifacts"]["materialized"]
            if item["destination"] == "README.md"
        )
        expected_source = original_read_bytes(readme) + sentinel
        self.assertIn("Snapshot sentinel.", scaffold.files["README.md"])
        self.assertEqual(
            readme_artifact["template_sha256"],
            hashlib.sha256(expected_source).hexdigest(),
        )

    def test_unsafe_and_duplicate_artifact_destinations_are_rejected(self):
        unsafe = copy.deepcopy(ARTIFACT_CATALOG)
        unsafe["artifacts"][0]["destination"] = "../README.md"
        with self.assertRaisesRegex(ValueError, "Unsafe artifact destination"):
            plan(artifacts=unsafe)

        reserved = copy.deepcopy(ARTIFACT_CATALOG)
        reserved["artifacts"][0]["destination"] = ".ges/custom.json"
        controls_for_reserved = copy.deepcopy(CONTROLS)
        readme_control = next(
            control
            for control in controls_for_reserved
            if control["id"] == "GES-DOC-001"
        )
        readme_control["verification"]["paths"].append(".ges/custom.json")
        with self.assertRaisesRegex(ValueError, "Unsafe artifact destination"):
            plan(controls=controls_for_reserved, artifacts=reserved)

        nested_git = copy.deepcopy(ARTIFACT_CATALOG)
        nested_git["artifacts"][0]["destination"] = "docs/.git/config"
        controls_for_git = copy.deepcopy(CONTROLS)
        readme_control = next(
            control for control in controls_for_git if control["id"] == "GES-DOC-001"
        )
        readme_control["verification"]["paths"].append("docs/.git/config")
        with self.assertRaisesRegex(ValueError, "Unsafe artifact destination"):
            plan(controls=controls_for_git, artifacts=nested_git)

        controls = copy.deepcopy(CONTROLS)
        artifacts = copy.deepcopy(ARTIFACT_CATALOG)
        duplicate = artifacts["artifacts"][0]["destination"]
        second_control_id = artifacts["artifacts"][1]["control_id"]
        second_control = next(
            control for control in controls if control["id"] == second_control_id
        )
        second_control["verification"]["paths"].append(duplicate)
        artifacts["artifacts"][1]["destination"] = duplicate
        with self.assertRaisesRegex(ValueError, "Duplicate artifact destination"):
            plan(controls=controls, artifacts=artifacts)

    def test_pure_render_rejects_parameter_marker_injection(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            template = root / "template.md"
            template.write_text("Value: {{VALUE}}\n", encoding="utf-8")

            self.assertEqual(
                render_template_text(root, "template.md", {"VALUE": "safe"}),
                "Value: safe\n",
            )
            with self.assertRaisesRegex(
                ValueError,
                "Template markers are not allowed in parameter values",
            ):
                render_template_text(
                    root,
                    "template.md",
                    {"VALUE": "unsafe {{INJECTED}}"},
                )
            self.assertEqual([path.name for path in root.iterdir()], ["template.md"])


class ScaffoldCLI(unittest.TestCase):
    def run_cli(self, *arguments):
        return subprocess.run(
            [sys.executable, "-m", "ges", *map(str, arguments)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_missing_parameter_fails_preflight_without_output(self):
        spec = copy.deepcopy(REPOSITORY_SPEC)
        spec["template_parameters"].pop("STATUS_AND_SCOPE")
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            spec_path = root / "spec.json"
            output = root / "generated"
            spec_path.write_text(json.dumps(spec), encoding="utf-8")

            result = self.run_cli(
                "scaffold",
                "--spec",
                spec_path,
                "--profile",
                ROOT / "profiles/solo-software.json",
                "--output",
                output,
            )

            self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
            self.assertEqual(result.stdout, "")
            error = json.loads(result.stderr)
            self.assertEqual(error["type"], "ValueError")
            self.assertIn("Missing parameters: STATUS_AND_SCOPE", error["error"])
            self.assertFalse(os.path.lexists(output))

    def test_scaffold_command_creates_local_tree_and_summary(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "generated"
            result = self.run_cli(
                "scaffold",
                "--spec",
                ROOT / "examples/repository-spec.json",
                "--profile",
                ROOT / "profiles/solo-software.json",
                "--output",
                output,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(result.stderr, "")
            report = json.loads(result.stdout)
            self.assertEqual(report["created"], str(output))
            self.assertEqual(report["files"], 14)
            self.assertEqual(report["materialized_artifacts"], 10)
            self.assertFalse(report["native_changes_applied"])
            self.assertTrue((output / ".ges/generation-manifest.json").is_file())
            self.assertFalse((output / ".ges-scaffold-incomplete").exists())
            self.assertFalse((output / ".git").exists())

    def test_dry_run_prints_manifest_without_output(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "generated"
            result = self.run_cli(
                "scaffold",
                "--spec",
                ROOT / "examples/repository-spec.json",
                "--profile",
                ROOT / "profiles/solo-software.json",
                "--output",
                output,
                "--dry-run",
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(result.stderr, "")
            report = json.loads(result.stdout)
            self.assertTrue(report["dry_run"])
            self.assertEqual(report["would_create"], str(output))
            self.assertEqual(
                report["manifest"]["status_boundary"]["native_changes_applied"],
                False,
            )
            self.assertFalse(os.path.lexists(output))

    def test_scaffold_help_has_no_output_side_effect(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            output = root / "generated"
            result = self.run_cli("scaffold", "--output", output, "--help")

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("--dry-run", result.stdout)
            self.assertIn("--spec", result.stdout)
            self.assertEqual(result.stderr, "")
            self.assertFalse(os.path.lexists(output))
            self.assertEqual(list(root.iterdir()), [])


if __name__ == "__main__":
    unittest.main()
