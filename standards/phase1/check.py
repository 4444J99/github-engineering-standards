#!/usr/bin/env python3
"""Phase 1 (secrets & supply chain) warn-only workflow checks.

Thin by design: inspects .github/workflows and .github/dependabot.yml of a
checked-out repository and reports findings. Exit code is always 0 unless
--enforce is passed (warn-only everywhere first).
"""
from __future__ import annotations
import argparse, json, os, re, sys
from pathlib import Path
import yaml

SHA = re.compile(r"@[0-9a-f]{40}$")
MASK = re.compile(r"\|\|\s*true\b|(^|[;&\s])exit 0\b")
LOCKS = {
    "package.json": ["package-lock.json", "pnpm-lock.yaml", "yarn.lock", "bun.lock", "bun.lockb"],
    "pyproject.toml": ["uv.lock", "poetry.lock", "pdm.lock", "requirements.txt", "requirements.lock"],
    "Cargo.toml": ["Cargo.lock"],
    "go.mod": ["go.sum"],
}


def _load(p: Path):
    try:
        res = yaml.safe_load(p.read_text())
        return {} if res is None else res
    except Exception as exc:  # report, never crash the warn-only run
        return {"__error__": str(exc)}


def check_repo(root: Path) -> list[dict]:
    f: list[dict] = []
    add = lambda rule, where, msg: f.append({"rule": rule, "where": where, "message": msg})
    wfdir = root / ".github" / "workflows"
    files = sorted(list(wfdir.glob("*.yml")) + list(wfdir.glob("*.yaml"))) if wfdir.is_dir() else []
    for p in files:
        n = f".github/workflows/{p.name}"
        y = _load(p)
        if not isinstance(y, dict):
            add("yaml-parse", n, "top-level YAML document must be a mapping"); continue
        if "__error__" in y:
            add("yaml-parse", n, str(y["__error__"])[:200]); continue
        jobs = y.get("jobs") if isinstance(y.get("jobs"), dict) else {}
        if "permissions" not in y and not all(isinstance(j, dict) and "permissions" in j for j in jobs.values()):
            add("least-privilege-permissions", n, "no top-level or per-job `permissions:`")
        top_conc = "concurrency" in y
        for jn, j in jobs.items():
            if not isinstance(j, dict):
                continue
            where = f"{n}#{jn}"
            if "uses" in j:  # reusable workflow call
                u = str(j["uses"])
                if not u.startswith("./") and not SHA.search(u):
                    add("pin-by-sha", where, f"reusable workflow not pinned by SHA: {u}")
                continue
            ro = json.dumps(j.get("runs-on", ""))
            if "-latest" in ro:
                add("pin-runner-image", where, f"runs-on uses a moving image: {ro}")
            if "timeout-minutes" not in j:
                add("job-timeout", where, "missing timeout-minutes")
            if not top_conc and "concurrency" not in j:
                add("concurrency", where, "no workflow- or job-level concurrency group")
            if j.get("continue-on-error") is True:
                add("no-masked-failures", where, "job continue-on-error: true")
            steps = j.get("steps") if isinstance(j.get("steps"), list) else []
            for i, s in enumerate(steps):
                if not isinstance(s, dict):
                    continue
                u = s.get("uses")
                if u and not str(u).startswith(("./", "docker://")) and not SHA.search(str(u)):
                    add("pin-by-sha", f"{where} step {i+1}", f"action not pinned by SHA: {u}")
                if s.get("continue-on-error") is True:
                    add("no-masked-failures", f"{where} step {i+1}", "step continue-on-error: true")
                if MASK.search(str(s.get("run", ""))):
                    add("no-masked-failures", f"{where} step {i+1}", "`|| true` or `exit 0` in run")
    db = [root / ".github" / x for x in ("dependabot.yml", "dependabot.yaml")]
    db = [x for x in db if x.exists()]
    if not db:
        add("dependabot-configured", ".github/dependabot.yml", "missing")
    else:
        y = _load(db[0])
        n_db = f".github/{db[0].name}"
        if not isinstance(y, dict):
            add("yaml-parse", n_db, "top-level YAML document must be a mapping")
        elif "__error__" in y:
            add("yaml-parse", n_db, str(y["__error__"])[:200])
        else:
            updates = y.get("updates") if isinstance(y.get("updates"), list) else []
            for u in updates:
                if not isinstance(u, dict):
                    continue
                eco = u.get("package-ecosystem")
                sched = u.get("schedule") if isinstance(u.get("schedule"), dict) else {}
                if sched.get("interval") != "weekly" or not u.get("groups"):
                    add("dependabot-grouped-weekly", n_db, f"{eco}: needs weekly schedule + groups")
    for man, locks in LOCKS.items():
        if (root / man).exists() and not any((root / l).exists() for l in locks):
            add("lockfile-committed", man, "manifest at root without a committed lockfile")
    return f


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("path", nargs="?", default=".")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--enforce", action="store_true", help="exit 1 on findings (not used in warn-only rollout)")
    a = ap.parse_args(argv)
    findings = check_repo(Path(a.path))
    if a.json:
        print(json.dumps(findings, indent=1))
    else:
        for x in findings:
            print(f"::warning title=phase1/{x['rule']}::{x['where']}: {x['message']}")
        print(f"phase1: {len(findings)} finding(s)")
    return 1 if (a.enforce and findings) else 0


if __name__ == "__main__":
    sys.exit(main())
