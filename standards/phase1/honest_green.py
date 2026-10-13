#!/usr/bin/env python3
"""Honest-green aggregate: green only if every depended-on job succeeded.

Input: the caller's `toJSON(needs)` (env NEEDS_JSON) and optionally the jobs of
the current run (env RUN_JOBS_JSON, from the Actions API) to catch jobs that
"succeeded" with zero steps. skipped, cancelled, failure, missing and zero-step
are all NOT green. Warn-only unless --enforce.
"""
from __future__ import annotations
import argparse, json, os, sys


def evaluate(needs: dict, run_jobs: list | None = None) -> list[str]:
    problems = []
    if not needs:
        problems.append("no depended-on jobs: nothing proves green")
    for name, v in sorted(needs.items()):
        r = (v or {}).get("result")
        if r != "success":
            problems.append(f"{name}: result={r}")
    for j in run_jobs or []:
        if j.get("conclusion") == "success" and not j.get("steps"):
            problems.append(f"{j.get('name')}: success with 0 steps")
    return problems


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--enforce", action="store_true")
    a = ap.parse_args(argv)
    needs = json.loads(os.environ.get("NEEDS_JSON") or "{}")
    rj = os.environ.get("RUN_JOBS_JSON")
    run_jobs = json.loads(rj).get("jobs", []) if rj else None
    p = evaluate(needs, run_jobs)
    for x in p:
        print(f"::warning title=phase1/honest-green::{x}")
    print("honest-green: " + ("NOT green" if p else "green"))
    return 1 if (a.enforce and p) else 0


if __name__ == "__main__":
    sys.exit(main())
