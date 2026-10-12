"""Bounded advisory inspection; never a native required-check or adoption claim."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

from .checks import execute

SHA = re.compile(r"[0-9a-f]{40}")


def execution_result(plan: dict, receipt: dict | None) -> tuple[str, str]:
    """Compare an observation to a separately supplied trusted execution plan.

    This validates reported structure and outcomes, not producer authentication.
    A caller must retrieve both inputs through the authorized evidence surface.
    """
    if receipt is None:
        return "NOT_VERIFIABLE", "Execution receipt absent"
    if not isinstance(receipt, dict) or type(receipt.get("repository_id")) is not int:
        return "NOT_VERIFIABLE", "Execution receipt is not an object"
    for key in ("repository_id", "revision", "plan_digest"):
        if receipt.get(key) != plan.get(key):
            return "NOT_VERIFIABLE", "Receipt does not match trusted " + key
    observations = receipt.get("checks")
    if not isinstance(observations, list) or not all(isinstance(c, dict) for c in observations):
        return "NOT_VERIFIABLE", "Malformed check observations"
    names = [c.get("name") for c in observations]
    if names != plan["checks"]:
        return "NOT_VERIFIABLE", "Missing, duplicate, extra or reordered planned checks"
    for check in observations:
        if check.get("revision") != plan["revision"]:
            return "NOT_VERIFIABLE", "Check revision differs from trusted plan"
        if check.get("status") != "completed" or check.get("conclusion") != "success":
            return "WARN", "A planned check did not complete successfully"
        if (type(check.get("runner_id")) is not int or check["runner_id"] <= 0
                or not isinstance(check.get("steps"), list) or not check["steps"]):
            return "NOT_VERIFIABLE", "No positive runner and executed-step evidence"
        for step in check["steps"]:
            if not isinstance(step, dict) or step.get("status") != "completed" or step.get("conclusion") != "success":
                return "WARN", "A reported step failed, skipped, or did not complete"
    return "OBSERVED", "Reported execution matches the plan; provenance and authenticity still require review"


def validate_plan(plan: dict) -> None:
    if (not isinstance(plan, dict) or type(plan.get("repository_id")) is not int
            or plan["repository_id"] <= 0 or not SHA.fullmatch(str(plan.get("revision", "")))
            or not re.fullmatch(r"[0-9a-f]{64}", str(plan.get("plan_digest", "")))
            or not isinstance(plan.get("checks"), list) or not plan["checks"]
            or not all(isinstance(n, str) and n.strip() for n in plan["checks"])
            or len(set(plan["checks"])) != len(plan["checks"])):
        raise ValueError("Trusted plan requires stable repository ID, exact revision, digest and unique nonempty checks")


def inspect(snapshot: dict, plan: dict, receipt: dict | None = None) -> dict:
    validate_plan(plan)
    if not isinstance(snapshot, dict):
        raise ValueError("Snapshot must be an object")
    bound = (type(snapshot.get("repository_id")) is int and snapshot.get("repository_id") == plan["repository_id"]
             and snapshot.get("revision") == plan["revision"])
    findings = []
    for control in ("workflow_permissions", "workflow_pinning"):
        if bound:
            status, reason = execute({"verification": {"kind": control}}, snapshot, {})
            status = "OBSERVED" if status == "PASS" else "WARN" if status == "FAIL" else status
        else:
            status, reason = "NOT_VERIFIABLE", "Snapshot repository/revision does not match trusted plan"
        findings.append({"control": control, "status": status, "reason": reason})
    status, reason = execution_result(plan, receipt)
    findings.append({"control": "execution_receipt", "status": status, "reason": reason})
    return {"schema": "ges.warning-pilot.v1", "mode": "warning-only",
            "repository_id": plan["repository_id"], "revision": plan["revision"],
            "plan_digest": plan["plan_digest"], "findings": findings,
            "compliance_certified": False, "native_enforcement_verified": False,
            "not_evaluated": ["publication_artifacts", "checker_protection", "retention_and_restoration",
                              "complete_workflow_schema", "privileged_trigger_dataflow", "evidence_authenticity"]}


def load(path: str) -> dict:
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("Duplicate JSON key: " + key)
            result[key] = value
        return result
    return json.loads(Path(path).read_text(), object_pairs_hook=unique)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--snapshot", required=True)
    parser.add_argument("--plan", required=True, help="Trusted plan, retrieved independently of candidate changes")
    parser.add_argument("--receipt")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    try:
        result = inspect(load(args.snapshot), load(args.plan), load(args.receipt) if args.receipt else None)
        result["input_digests"] = {name: hashlib.sha256(Path(path).read_bytes()).hexdigest()
                                  for name, path in (("snapshot", args.snapshot), ("plan", args.plan), ("receipt", args.receipt)) if path}
        with Path(args.output).open("x") as output:
            json.dump(result, output, indent=2)
            output.write("\n")
    except (ValueError, TypeError, KeyError, OSError) as exc:
        parser.exit(2, "Pilot inspection error: " + str(exc) + "\n")
    print("Advisory report written; exit 0 means inspection completed, not compliance.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
