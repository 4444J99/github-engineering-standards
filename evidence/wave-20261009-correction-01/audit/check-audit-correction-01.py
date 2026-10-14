#!/usr/bin/env python3
"""Bounded re-derivation checker for wave-20261009-correction-01 (worker E audit).

Read-only: runs git read commands and hashes against committed bytes in the five
pre-existing checkouts. Writes nothing. Emits a JSON verdict block on stdout.

Scope (deliberately bounded): head equality, stage exclusivity, additions-only
stats, identity/session binding, disposition honesty, planning-freeze selected
counts, gate-retention strings, freeze hash binding. Heavy/Governance suite is
NOT run (deferred to A-integrate by the execution freeze).
"""

import hashlib
import json
import subprocess
import sys

ROOT = "/Users/4jp/Workspace/4444J99/.worktrees"
CHECKOUTS = {
    "E": f"{ROOT}/ges-wave-e-20261009",
    "A": f"{ROOT}/ges-wave-20261009",
    "B": f"{ROOT}/ges-wave-b-20261009",
    "C": f"{ROOT}/ges-wave-c-20261009",
    "D": f"{ROOT}/ges-wave-d-20261009",
}
EXPECTED_HEADS = {
    "E": "509f4a4f3268d1d91c97d898f1c90e48a6946a52",
    "A": "21e9719af490740b7807bf4fa5ce3931d120ed5d",
    "B": "c034c82d6e15b29e30711f3cb77b53d5a61e206c",
    "C": "a29214dc5ff55dd5df6176a80d1f4478789a9beb",
    "D": "4e137f69448ac10fe20002838941369b72d255b1",
}
STAGES = {  # role -> (start, end, exclusive root prefix)
    "B": ("2ad83ba6a3029eebadfd9c97e80cf6def8e98234", EXPECTED_HEADS["B"],
          "evidence/wave-20261009-correction-01/source/"),
    "C": ("a2b81ff848d0c4137f0df03baf09e9685473a016", EXPECTED_HEADS["C"],
          "evidence/wave-20261009-correction-01/publication/"),
    "D": ("4768db8929420538e3b828467de9dbe314fd4b74", EXPECTED_HEADS["D"],
          "evidence/wave-20261009-correction-01/omission/"),
}
FREEZE_PATH = "evidence/wave-20261009-correction-01/serialized-admission-03/execution-freeze-20261010.json"
ASSIGN_PATH = "evidence/wave-20261009-correction-01/assignment.json"
RECON_PATH = "evidence/wave-20261009-correction-01/reconciliation-CORRECTION-01.json"
EXPECTED_FREEZE_SHA = "b1b8fd0f7389369f9a1cfd02513d07794239be0072ddfa7a1b2e4d9b4c1dd573"
EXPECTED_ASSIGN_SHA = "dc9854e6740a1c1c122f3d292a4f53b9a349e89f72fca568d430acf54f31a3a4"

checks = []


def check(name, ok, detail=""):
    checks.append({"name": name, "ok": bool(ok), "detail": detail})
    return bool(ok)


def git(role, *args):
    out = subprocess.run(["git", "-C", CHECKOUTS[role], *args],
                         capture_output=True, text=True)
    if out.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {out.stderr.strip()}")
    return out.stdout


def show(role, rev, path):
    return git(role, "show", f"{rev}:{path}")


def load(role, rev, path):
    return json.loads(show(role, rev, path))


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


# 1. input heads ------------------------------------------------------------
for role, want in EXPECTED_HEADS.items():
    got = git(role, "rev-parse", "HEAD").strip()
    check(f"heads.{role}", got == want, f"expected {want} observed {got}")
    status = git(role, "status", "--porcelain", "-uno").strip()
    check(f"clean.{role}", status == "", f"status='{status}'")

# 2/3. exclusivity + additions-only ----------------------------------------
for role, (start, end, prefix) in STAGES.items():
    names = [n for n in git(role, "diff", "--name-only", f"{start}..{end}").splitlines() if n]
    stray = [n for n in names if not n.startswith(prefix)]
    check(f"exclusivity.{role}", not stray,
          f"{len(names)} files, stray={stray}")
    numstat = [l.split("\t") for l in
               git(role, "diff", "--numstat", f"{start}..{end}").splitlines() if l]
    added = sum(int(a) for a, d, _ in numstat)
    deleted = sum(int(d) for a, d, _ in numstat if d != "-")
    renamed = sum(1 for a, d, _ in numstat if a == "-" or d == "-")
    check(f"additions_only.{role}", deleted == 0 and renamed == 0,
          f"{added} insertions, {deleted} deletions, {renamed} renames, "
          f"{len(numstat)} files")

# 1b. role binding / session distinctness ----------------------------------
ident = {}
paths = {
    "B": ("B", EXPECTED_HEADS["B"],
          "evidence/wave-20261009-correction-01/source/identity.json"),
    "B_cancelled": ("B", EXPECTED_HEADS["B"],
                    "evidence/wave-20261009-correction-01/source/"
                    "identity-cancelled-ses_edbeebdceffe8CrNpIv5HJMXtW.json"),
    "C": ("C", EXPECTED_HEADS["C"],
          "evidence/wave-20261009-correction-01/publication/identity.json"),
    "D": ("D", EXPECTED_HEADS["D"],
          "evidence/wave-20261009-correction-01/omission/identity.json"),
}
for key, (role, rev, path) in paths.items():
    ident[key] = load(role, rev, path)
    check(f"identity_present.{key}", True, path)

recon = load("A", EXPECTED_HEADS["A"], RECON_PATH)
freeze = load("A", EXPECTED_HEADS["A"], FREEZE_PATH)
sessions = {
    "B": ident["B"]["session_id"]["value"],
    "B_cancelled": ident["B_cancelled"]["session_id"]["value"],
    "C": ident["C"]["session"]["session_id"],
    "D": ident["D"]["session_id"]["value"],
    "A": recon["A_identity"]["surface"].split(":", 1)[1],
}
with open(f"{CHECKOUTS['E']}/evidence/wave-20261009-correction-01/audit/identity.json",
          encoding="utf-8") as fh:
    sessions["E"] = json.load(fh)["session"]["session_id"]
check("sessions.distinct", len(set(sessions.values())) == len(sessions),
      json.dumps(sessions))
freeze_roles = {r["role"] for r in freeze["identities"]["roles"]}
check("freeze.roles_complete", {"A-reconcile", "E", "A-integrate"} <= freeze_roles,
      f"roles={sorted(freeze_roles)}")
check("A_identity_in_freeze_and_recon",
      freeze["identities"]["A_conductor"]["surface"] == recon["A_identity"]["surface"],
      recon["A_identity"]["surface"])

# 5a. B dispositions --------------------------------------------------------
B_CLAIMS = ["005", "009", "011", "017", "018"]
for cid in B_CLAIMS:
    d = load("B", EXPECTED_HEADS["B"],
             f"evidence/wave-20261009-correction-01/source/"
             f"WA-APPSEC-{cid}-CORRECTION-01.json")
    holds = d.get("remaining_holds") or []
    b = d.get("boundaries", {})
    check(f"B_{cid}.remaining_holds", len(holds) >= 4, f"count={len(holds)}")
    check(f"B_{cid}.honest_boundaries",
          b.get("human_approval") is False and b.get("accepted_policy") is False
          and b.get("delivery_status") == "Staged"
          and b.get("predecessor_modified") is False,
          json.dumps(b))
    check(f"B_{cid}.suffix", d["record_id"] == f"WA-APPSEC-{cid}-CORRECTION-01",
          d["record_id"])

# 5b. C dispositions --------------------------------------------------------
for use in ["objective", "implementation-acceptance-0"]:
    d = load("C", EXPECTED_HEADS["C"],
             f"evidence/wave-20261009-correction-01/publication/"
             f"use-correction-ges-ops-008-{use}-CORRECTION-01.json")
    tag = f"C_{use}"
    check(f"{tag}.remaining_hold", d["outcome"] == "REMAINING_HOLD", d["outcome"])
    check(f"{tag}.no_clearance",
          d["publication_clearance_granted"] == "none"
          and d["approvals_created"] == "none"
          and d["delivery_status"] == "Staged",
          f"clearance={d['publication_clearance_granted']}, "
          f"approvals={d['approvals_created']}, status={d['delivery_status']}")

# 5c. D coverage matrix + planning-freeze counts ---------------------------
d = load("D", EXPECTED_HEADS["D"],
         "evidence/wave-20261009-correction-01/omission/"
         "omission-review-CORRECTION-01.json")
m = d["scope_coverage_matrix"]
assign = load("A", EXPECTED_HEADS["A"], ASSIGN_PATH)
acct = assign["accounting"]
check("D.matrix_5_claims",
      len(m["claims"]) == acct["selected_unresolved_claims"] == 5
      and all(c["covered"] for c in m["claims"]),
      f"matrix={len(m['claims'])} assignment={acct['selected_unresolved_claims']}")
check("D.matrix_2_fields",
      len(m["use_fields"]) == acct["selected_unresolved_publication_fields"] == 2
      and all(f["covered"] for f in m["use_fields"]),
      f"matrix={len(m['use_fields'])} assignment={acct['selected_unresolved_publication_fields']}")
sel = m["selected_by_planning_freeze"]
check("D.matrix_selected_ids",
      sel["claims"] == [f"WA-APPSEC-{c}" for c in B_CLAIMS]
      and sel["use_fields"] == ["GES-OPS-008-objective",
                                "GES-OPS-008-implementation-acceptance-0"],
      json.dumps(sel))
failed = [c for c in d["checker_results"]["checks"] if not c["ok"]]
check("D.checker_270_clean",
      len(d["checker_results"]["checks"]) == 270 and not failed,
      f"{len(d['checker_results']['checks'])} checks, {len(failed)} failed")

# 4. lease narrative --------------------------------------------------------
lease_ids = {
    "B": ident["B"]["lease"]["lease_id"],
    "C": ident["C"]["lease"]["lease_id"],
    "D": ident["D"]["lease"]["lease_id"],
}
check("lease.single_wave_lease_BCD", len(set(lease_ids.values())) == 1
      == len(set(recon["stages"][i]["lease"].split(" ")[0] for i in range(3))),
      json.dumps(lease_ids))
a_leases = recon["A_identity"]["lease"]
check("lease.release_before_A_reconcile",
      a_leases["preceded_by"].startswith("released lease 2faae7b2"),
      a_leases["preceded_by"])
# C's recorded expiry must be derivable from its recorded acquire + ttl
c_l = ident["C"]["lease"]
import datetime as _dt
acq = _dt.datetime.fromisoformat(c_l["acquired_at_utc"].replace("Z", "+00:00"))
exp = _dt.datetime.fromisoformat(c_l["expires_at_utc"].replace("Z", "+00:00"))
derived = acq + _dt.timedelta(seconds=c_l.get("ttl_seconds", 1800) if isinstance(c_l.get("ttl_seconds"), int) else 1800)
check("lease.C_expiry_derivable_from_acquire_plus_ttl", derived == exp,
      f"acquired={c_l['acquired_at_utc']} ttl=1800 -> {derived.isoformat()} "
      f"recorded={c_l['expires_at_utc']} (unrecorded refresh implied)")

# 6. gate retention ---------------------------------------------------------
g = freeze["gates_retained"]
check("gate.storage_closed", "CLOSED" in g["storage"], g["storage"])
check("gate.broker_closed_not_bypassed", "not bypassed" in g["broker"]
      and "no run or capacity claimed" in g["broker"], g["broker"])
check("gate.deadline_30min", "30 minutes" in g["deadline"], g["deadline"])
check("gate.review_deferred_to_heavy", "final heavy tranche" in g["review"],
      g["review"])
check("gate.publication_hold_retained", "retain HOLD" in g["publication"]
      and "no publication clearance" in g["publication"], g["publication"])
check("gate.status_staged", freeze["delivery_status_retained"] == "Staged"
      and recon["status"] == "Staged",
      f"freeze={freeze['delivery_status_retained']} recon={recon['status']}")

# admission receipts --------------------------------------------------------
host = load("A", EXPECTED_HEADS["A"],
            "evidence/wave-20261009-correction-01/serialized-admission-03/"
            "host-admission-20261010.json")
broker = load("A", EXPECTED_HEADS["A"],
              "evidence/wave-20261009-correction-01/serialized-admission-03/"
              "broker-status-20261010.json")
check("receipt.host_heavy_deferred_gate_intact",
      host["heavy"]["gate_intact"] is True
      and "final verification tranche" in host["heavy"]["deferred_to"],
      json.dumps(host["heavy"]["deferred_to"]))
check("receipt.ttl_policy_30min", "30-minute" in host["ttl_policy"],
      host["ttl_policy"])
ra = broker["reservation_attempt"]
check("receipt.broker_closed_0_runs", ra["run_created"] is False
      and ra["retained_runs"] == 0
      and ra["result"].endswith("execution_priority_not_approved"),
      json.dumps({"result": ra["result"], "run_created": ra["run_created"],
                  "retained_runs": ra["retained_runs"]}))

# hash bindings -------------------------------------------------------------
freeze_sha = sha256_bytes(show("A", EXPECTED_HEADS["A"], FREEZE_PATH).encode())
assign_sha = sha256_bytes(show("A", EXPECTED_HEADS["A"], ASSIGN_PATH).encode())
check("hash.freeze_matches_reconciliation_binding",
      freeze_sha == recon["freeze_binding"]["sha256"] == EXPECTED_FREEZE_SHA,
      freeze_sha)
check("hash.planning_freeze_unmodified",
      assign_sha == EXPECTED_ASSIGN_SHA
      and EXPECTED_ASSIGN_SHA in freeze["freeze_relationship"]["planning_freeze"],
      assign_sha)

# adjudicate ----------------------------------------------------------------
verdict = "PASS" if all(c["ok"] for c in checks) else "FAIL"
print(json.dumps({"checker": "ges.correction-wave-audit-check.v1",
                  "verdict": verdict,
                  "checks_total": len(checks),
                  "checks_failed": sum(1 for c in checks if not c["ok"]),
                  "checks": checks}, indent=2))
sys.exit(0 if verdict == "PASS" else 1)
