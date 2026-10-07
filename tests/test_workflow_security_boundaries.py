"""Adversarial boundaries for observed workflow files; no execution certification."""
import unittest

import yaml

from ges.checks import execute


class WorkflowSecurityBoundaries(unittest.TestCase):
    def check(self, workflow, kind="workflow_permissions", extra=None, entry_kind="file"):
        files = {".github/workflows/ci.yml": {"kind": entry_kind, "content": yaml.safe_dump(workflow)}}
        files.update(extra or {})
        snapshot = {"observations": {"files": {"status": "OK", "complete": True, "data": files}}}
        return execute({"verification": {"kind": kind}}, snapshot, {})[0]

    def workflow(self, permissions=None):
        return {"on": "push", "permissions": {"contents": "read"} if permissions is None else permissions,
                "jobs": {"ci": {"runs-on": "ubuntu-latest", "steps": [{"run": "true"}]}}}

    def test_missing_and_empty_jobs_never_pass(self):
        for jobs in (None, {}, {"ci": {}}):
            for kind in ("workflow_permissions", "workflow_pinning"):
                with self.subTest(jobs=jobs, kind=kind):
                    wf = self.workflow(); wf["jobs"] = jobs
                    self.assertEqual(self.check(wf, kind), "FAIL")

    def test_unresolved_workflow_symlink_requires_review(self):
        for kind in ("workflow_permissions", "workflow_pinning"):
            self.assertEqual(self.check(self.workflow(), kind, entry_kind="symlink"), "MANUAL_REVIEW")

    def test_ambiguous_or_empty_step_never_passes(self):
        for step in ({"run": "true", "uses": "a/b@" + "a"*40}, {"run": ""}, {"uses": 123}, {}):
            for kind in ("workflow_permissions", "workflow_pinning"):
                wf = self.workflow(); wf["jobs"]["ci"]["steps"] = [step]
                self.assertEqual(self.check(wf, kind), "FAIL")

    def test_reusable_job_cannot_mix_execution_forms(self):
        wf = self.workflow(); wf["jobs"]["ci"]["uses"] = "a/b/.github/workflows/c.yml@" + "a"*40
        for kind in ("workflow_permissions", "workflow_pinning"):
            self.assertEqual(self.check(wf, kind), "FAIL")

    def test_unsupported_scope_is_not_green(self):
        self.assertEqual(self.check(self.workflow({"future-scope": "read"})), "MANUAL_REVIEW")

    def test_invalid_scope_levels_fail(self):
        for permissions in ({"id-token": "read"}, {"vulnerability-alerts": "write"}, {"contents": True}):
            self.assertEqual(self.check(self.workflow(permissions)), "FAIL")

    def test_root_write_still_fails(self):
        self.assertEqual(self.check(self.workflow({"contents": "write"})), "FAIL")

    def test_job_scoped_oidc_requires_justification(self):
        wf = self.workflow(); wf["jobs"]["ci"]["permissions"] = {"contents": "read", "id-token": "write"}
        self.assertEqual(self.check(wf), "MANUAL_REVIEW")

    def test_job_scoped_repository_write_requires_justification(self):
        wf = self.workflow(); wf["jobs"]["ci"]["permissions"] = {"contents": "write"}
        self.assertEqual(self.check(wf), "MANUAL_REVIEW")

    def test_readonly_and_none_remain_valid(self):
        for permissions in ({}, {"contents": "read"}, "read-all"):
            self.assertEqual(self.check(self.workflow(permissions)), "PASS")

    def test_local_action_symlink_not_pinning_proof(self):
        wf = self.workflow(); wf["jobs"]["ci"]["steps"] = [{"uses": "./action"}]
        entry = {"kind": "symlink", "content": "runs: {using: composite, steps: [{run: true}]}"}
        self.assertEqual(self.check(wf, "workflow_pinning", {"action/action.yml": entry}), "MANUAL_REVIEW")

    def test_nested_reusable_ambiguous_step_fails(self):
        wf = self.workflow(); wf["jobs"] = {"call": {"uses": "./.github/workflows/nested.yml"}}
        nested = self.workflow(); nested["jobs"]["ci"]["steps"] = [{"run": "true", "uses": "a/b@" + "a"*40}]
        self.assertEqual(self.check(wf, "workflow_pinning", {".github/workflows/nested.yml": yaml.safe_dump(nested)}), "FAIL")

    def test_new_known_read_scopes_supported(self):
        self.assertEqual(self.check(self.workflow({"artifact-metadata": "read", "code-quality": "read", "vulnerability-alerts": "read"})), "PASS")
