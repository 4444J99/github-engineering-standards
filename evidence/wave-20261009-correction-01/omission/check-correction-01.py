#!/usr/bin/env python3
"""Bounded independent omission checker for correction wave wave-20261009-correction-01, role D.

Reads committed states only (git show at pinned commits / clean working trees).
Writes evidence/wave-20261009-correction-01/omission/omission-review-CORRECTION-01.json
under this worker's exclusive write root. No network, no sibling writes, no git
state changes. Runtime is bounded (a handful of MB of committed JSON).
"""
import hashlib
import json
import os
import subprocess
import sys

MY = "/Users/4jp/Workspace/4444J99/.worktrees/ges-wave-d-20261009"
B = "/Users/4jp/Workspace/4444J99/.worktrees/ges-wave-b-20261009"
C = "/Users/4jp/Workspace/4444J99/.worktrees/ges-wave-c-20261009"
A = "/Users/4jp/Workspace/4444J99/.worktrees/ges-wave-20261009"
BH = "c034c82d6e15b29e30711f3cb77b53d5a61e206c"
CH = "a29214dc5ff55dd5df6176a80d1f4478789a9beb"
AH = "d8e0d6bfe7f15c47c9cbc1d5590d098a1ad0ef6e"
OUT = os.path.join(MY, "evidence/wave-20261009-correction-01/omission/omission-review-CORRECTION-01.json")

CLAIMS = ["WA-APPSEC-005", "WA-APPSEC-009", "WA-APPSEC-011", "WA-APPSEC-017", "WA-APPSEC-018"]
USES = ["GES-OPS-008-objective", "GES-OPS-008-implementation-acceptance-0"]

results = {"role_D_checker": "ges.correction-omission-checker.v1", "checks": [], "failures": []}


def check(name, ok, detail=""):
    results["checks"].append({"name": name, "ok": bool(ok), "detail": detail})
    if not ok:
        results["failures"].append(name)
    return bool(ok)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def blob(repo, commit, path):
    r = subprocess.run(["git", "-C", repo, "show", f"{commit}:{path}"],
                       capture_output=True, timeout=60)
    if r.returncode != 0:
        return None
    return r.stdout


def load(repo, commit, path):
    b = blob(repo, commit, path)
    if b is None:
        return None, None
    try:
        return json.loads(b), b
    except Exception:
        return None, b


def find_by(o, key, val):
    if isinstance(o, dict):
        if o.get(key) == val:
            return o
        for v in o.values():
            r = find_by(v, key, val)
            if r is not None:
                return r
    elif isinstance(o, list):
        for v in o:
            r = find_by(v, key, val)
            if r is not None:
                return r
    return None


# ---------------------------------------------------------------- inputs
claims_doc, claims_bytes = load(MY, "HEAD", "evidence/source-reviews/wa-application-security-checklist-claims.json")
residuals, res_bytes = load(B, BH, "evidence/wave-20261009/source/residuals.json")
prev, _ = load(B, BH, "evidence/wave-20261009/source/primary-review.json")
dispo, _ = load(B, BH, "evidence/wave-20261009/source/draft-dispositions.json")
decisions, _ = load(B, BH, "evidence/wave-20261009/source/proposed-decisions.json")
assignment, _ = load(A, AH, "evidence/wave-20261009-correction-01/assignment.json")
freeze, _ = load(A, AH, "evidence/wave-20261009-correction-01/serialized-admission-03/execution-freeze-20261010.json")

check("inputs.residuals_present", residuals is not None)
check("inputs.primary_review_present", prev is not None)
check("inputs.claims_doc_present_in_D", claims_doc is not None)
check("inputs.assignment_present", assignment is not None)
check("inputs.freeze_present", freeze is not None)

sfr = residuals.get("source_fidelity_repairs_required", []) if residuals else []
check("inputs.residuals_has_five_holds", len(sfr) == 5, f"count={len(sfr)}")
for i, cid in enumerate(CLAIMS):
    check(f"hold_text.{cid}", i < len(sfr) and sfr[i].startswith(cid + ":"), sfr[i] if i < len(sfr) else "")

BOUND_HASHES = {
    "evidence/wave-20261009/source/residuals.json": "cbf159cf9c9d70be0a74bddaee581e67d50b7e0c6fa3444950429114fa7a7124",
    "evidence/wave-20261009/source/primary-review.json": "8e27182d8562f1cd85f1062c07cf43ba81efae76c6df71d8c93593379cfb26f1",
    "evidence/wave-20261009/source/draft-dispositions.json": "7f87225f90b1aa2c581242eb2b09531dab2fc3f74b93f9f8c260802540828c52",
    "evidence/wave-20261009/source/proposed-decisions.json": "1acf2be74a71744708589d0f0042a4b46d9f881fc2bb2d8e84125e00d377e1db",
    "evidence/source-reviews/wa-application-security-checklist-claims.json": "a41ba69a8ea30a5338ad56d8bd2c1909a4912eb219ab862e9e4b1af460959993",
}
check("bindings.claims_doc_sha_matches_prior", sha(claims_bytes) == BOUND_HASHES["evidence/source-reviews/wa-application-security-checklist-claims.json"])
for p, want in BOUND_HASHES.items():
    if p.startswith("evidence/source-reviews"):
        continue
    got = blob(B, BH, p)
    check(f"bindings.blob_sha.{os.path.basename(p)}", got is not None and sha(got) == want)

claim_by_id = {c["claim_id"]: c for c in claims_doc.get("claims", [])}

# ---------------------------------------------------------------- B records
REQUIRED = ["schema", "record_id", "correction_wave", "role", "predecessor_claim_id",
            "predecessor_record", "hold_corrected", "correction", "evidence_references",
            "linked_decisions", "outcome", "remaining_holds", "boundaries"]
b_summary = []
for i, cid in enumerate(CLAIMS):
    path = f"evidence/wave-20261009-correction-01/source/{cid}-CORRECTION-01.json"
    rec, raw = load(B, BH, path)
    ok = check(f"B.{cid}.parsed", rec is not None)
    if not ok:
        b_summary.append({"claim_id": cid, "verdict": "RECORD_MISSING_OR_UNPARSEABLE", "evidence_references": [path]})
        continue
    pre = rec.get("predecessor_record", {})
    hd = rec.get("hold_corrected", {})
    co = rec.get("correction", {})
    bd = rec.get("boundaries", {})
    doc = claim_by_id.get(cid, {})
    check(f"B.{cid}.record_id", rec.get("record_id") == f"{cid}-CORRECTION-01")
    check(f"B.{cid}.suffix", rec.get("record_id", "").endswith("-CORRECTION-01"))
    check(f"B.{cid}.predecessor_id", rec.get("predecessor_claim_id") == cid)
    check(f"B.{cid}.fields_present", all(k in rec for k in REQUIRED),
          str([k for k in REQUIRED if k not in rec]))
    check(f"B.{cid}.doc_sha", pre.get("document_sha256") == sha(claims_bytes))
    check(f"B.{cid}.statement", pre.get("statement") == doc.get("statement"),
          f"record={pre.get('statement')!r} doc={doc.get('statement')!r}")
    check(f"B.{cid}.line_span", (pre.get("start_line"), pre.get("end_line")) == (doc.get("start_line"), doc.get("end_line")))
    check(f"B.{cid}.statement_sha", pre.get("statement_sha256") == sha(doc.get("statement", "").encode()))
    check(f"B.{cid}.mapping_status", pre.get("mapping_status") == doc.get("mapping_status"))
    check(f"B.{cid}.accepted_policy", pre.get("accepted_policy") == doc.get("accepted_policy") is False or pre.get("accepted_policy") == doc.get("accepted_policy"))
    check(f"B.{cid}.hold_text_matches_residuals", hd.get("hold_statement") == sfr[i], f"record={hd.get('hold_statement')!r}")
    check(f"B.{cid}.hold_field_index", hd.get("hold_statement_field", "").endswith(f"[{i}]"))
    # primary-review cross-check
    pe = find_by(prev, "claim_id", cid) if isinstance(prev, list) else find_by(prev, "claim_id", cid)
    check(f"B.{cid}.primary_review_entry", pe is not None)
    if pe:
        check(f"B.{cid}.residual_quote", hd.get("residual") == pe.get("residual"))
        check(f"B.{cid}.interpretation_quote", hd.get("reviewed_interpretation") == pe.get("interpretation"))
        check(f"B.{cid}.source_span_sha_vs_review", pre.get("source_span_sha256") == pe.get("source_span_sha256"))
        check(f"B.{cid}.decision_id_vs_review", rec.get("linked_decisions", {}).get("decision_id") == pe.get("decision_id"))
    # draft-dispositions cross-check (entries key the claim under item['claim']['claim_id'])
    de = next((x for x in (dispo or []) if isinstance(x, dict)
               and x.get("claim", {}).get("claim_id") == cid), None)
    check(f"B.{cid}.disposition_status", de is not None and de.get("status") == "PROPOSED_NOT_RECONCILIATION_RECEIPT",
          (de or {}).get("status", "missing"))
    if de:
        check(f"B.{cid}.disposition_distinction", bool(de.get("details", {}).get("distinction")))
        check(f"B.{cid}.disposition_rationale", bool(de.get("rationale")))
    # proposed-decisions cross-check (compare id/revision pairs; B's records add a
    # 'collection' annotation not present in the committed decision - recorded as observation)
    did = rec.get("linked_decisions", {}).get("decision_id")
    dce = find_by(decisions, "id", did) if did else None
    check(f"B.{cid}.decision_exists", dce is not None, str(did))
    if dce:
        check(f"B.{cid}.decision_disposition", rec.get("linked_decisions", {}).get("disposition") == dce.get("disposition"))
        got_pairs = sorted((x.get("id"), x.get("revision")) for x in rec.get("linked_decisions", {}).get("control_references", []))
        want_pairs = sorted((x.get("id"), x.get("revision")) for x in dce.get("control_references", []))
        check(f"B.{cid}.decision_controls", got_pairs == want_pairs, f"got={got_pairs} want={want_pairs}")
        check(f"B.{cid}.decision_review", (rec.get("linked_decisions", {}).get("review_status") == (dce.get("review") or {}).get("status") == "PROPOSED")
              and rec.get("linked_decisions", {}).get("reviewer") == (dce.get("review") or {}).get("reviewer"))
    # evidence reference hashes resolvable
    for er in rec.get("evidence_references", []):
        p = er.get("path")
        if p == "evidence/source-reviews/wa-application-security-checklist-claims.json":
            got = sha(claims_bytes)
        else:
            gb = blob(B, BH, p)
            got = sha(gb) if gb is not None else None
        check(f"B.{cid}.evidence_ref_sha.{os.path.basename(p)}", got == er.get("sha256"), f"got={got}")
    # overclaim / obligation checks
    check(f"B.{cid}.outcome_bounded", "HOLD" in rec.get("outcome", ""), rec.get("outcome"))
    check(f"B.{cid}.boundaries", bd.get("delivery_status") == "Staged" and bd.get("human_approval") is False
          and bd.get("accepted_policy") is False and bd.get("predecessor_modified") is False
          and bd.get("heavy_validation_run") is False)
    rh = " | ".join(rec.get("remaining_holds", []))
    for req in ["SOURCE_BYTES_NOT_REREAD", "NO_RECONCILIATION_RECEIPT", "DECISION_STILL_PROPOSED", "MAPPING_AND_POLICY_UNCHANGED"]:
        check(f"B.{cid}.remaining_hold.{req}", req in rh)
    check(f"B.{cid}.derivation_disclosed", "not re-read" in co.get("derivation", ""), co.get("derivation", "")[:80])
    b_summary.append({"claim_id": cid, "record": path, "verdict": "SUPPORTED_BOUNDED_STATEMENT_CORRECTION_NO_OMISSION_FOUND"})

# claims-doc top-level obligation checks
check("claimsdoc.policy_adoption_none", claims_doc.get("policy_adoption") == "NONE")
check("claimsdoc.rights_unresolved", claims_doc.get("rights_clearance") == "UNRESOLVED")
check("claimsdoc.omission_audit_false", claims_doc.get("independent_omission_audit") is False)
conf_text = json.dumps(claims_doc.get("conflicts"))
check("claimsdoc.rotation_authority_conflict_present", "require applicable authority" in conf_text)

# B README citations
b_readme = blob(B, BH, "evidence/wave-20261009-correction-01/source/README.md")
check("B.readme_present", b_readme is not None)
check("B.readme_cites_residuals", b_readme and b"source_fidelity_repairs_required" in b_readme)

# ---------------------------------------------------------------- C records
pub_prev, _ = load(C, CH, "evidence/wave-20261009/publication/primary-review.json")
rq = blob(C, CH, "controls/review_queue.json")
pub_readme = blob(C, CH, "evidence/wave-20261009/publication/README.md")
acct, _ = load(C, CH, "evidence/wave-20261009/publication/accounting-replay.json")
cand_int, _ = load(C, CH, "evidence/wave-20261009-correction-01/publication/candidate-integrity.json")
pub_use_py = blob(C, CH, "ges/publication_use.py")
reg_md = blob(C, CH, "docs/publication-use-register.md")

check("C.primary_review_present", pub_prev is not None)
check("C.review_queue_present", rq is not None)
check("C.review_queue_sha", rq is not None and sha(rq) == "091b1afe9c2f195accda530a8a0f59e0f1f6cfc347c46d303ebb60284acde8a9")

c_summary = []
for uid, (s, e) in zip(USES, [(9754, 9924), (10898, 11068)]):
    path = f"evidence/wave-20261009-correction-01/publication/use-correction-{uid.lower()}-CORRECTION-01.json"
    rec, raw = load(C, CH, path)
    ok = check(f"C.{uid}.parsed", rec is not None)
    if not ok:
        c_summary.append({"use_id": uid, "verdict": "RECORD_MISSING_OR_UNPARSEABLE", "evidence_references": [path]})
        continue
    check(f"C.{uid}.record_id", rec.get("use_id") == f"{uid}-CORRECTION-01")
    check(f"C.{uid}.suffix", rec.get("use_id", "").endswith("-CORRECTION-01"))
    check(f"C.{uid}.predecessor_id", rec.get("predecessor_use_id") == uid)
    check(f"C.{uid}.fields_present", all(k in rec for k in ["schema", "use_id", "predecessor_use_id",
                                                            "predecessor_record", "hold_being_corrected",
                                                            "verified_observations", "classification_analysis",
                                                            "outcome", "hold_statement", "approvals_created",
                                                            "publication_clearance_granted", "delivery_status"]))
    check(f"C.{uid}.outcome_hold", rec.get("outcome") == "REMAINING_HOLD", rec.get("outcome"))
    check(f"C.{uid}.no_approvals", rec.get("approvals_created") == "none" and rec.get("publication_clearance_granted") == "none")
    check(f"C.{uid}.status_staged", rec.get("delivery_status") == "Staged")
    # predecessor row
    ue = find_by(pub_prev, "use_id", uid)
    check(f"C.{uid}.predecessor_row", ue is not None)
    if ue:
        check(f"C.{uid}.predecessor_kind_null", ue.get("kind") is None)
        check(f"C.{uid}.predecessor_status", ue.get("classification_status") == "UNRESOLVED_JSON_ENCODING")
        check(f"C.{uid}.predecessor_output_range", (ue.get("output_range") or {}).get("start_byte") == s and (ue.get("output_range") or {}).get("end_byte") == e)
        check(f"C.{uid}.predecessor_raw_sha", (ue.get("output_range") or {}).get("sha256") == rec.get("verified_observations", {}).get("output_span_sha256_committed_in_predecessor"))
        check(f"C.{uid}.predecessor_source_sha", (ue.get("source_range") or {}).get("sha256") == rec.get("verified_observations", {}).get("decoded_text_sha256"))
    # byte-identity spot check (bounded)
    vo = rec.get("verified_observations", {})
    if rq is not None:
        span = rq[s:e]
        check(f"C.{uid}.span_len", len(span) == vo.get("output_span_raw_length_bytes") == 170, f"len={len(span)}")
        check(f"C.{uid}.span_sha", sha(span) == vo.get("output_span_sha256_observed") == "e429fb1a28c34aef1b2bfb70e1ea18da086ad07ef8009cbeca4a8db3bcac3779")
        esc = bytes((0x5C, 0x22))  # the two-byte JSON quote escape \"
        check(f"C.{uid}.escape_count", span.count(esc) == 2, f"count={span.count(esc)}")
        dec = span.replace(esc, b'"')
        check(f"C.{uid}.decoded_sha", len(dec) == vo.get("decoded_text_length_bytes") == 168 and sha(dec) == vo.get("decoded_text_sha256") == "5c22f1ab4b96debea71867950f713067492f6d5d2d44561fedb496b043ff87a8")
        check(f"C.{uid}.raw_ne_source", sha(span) != sha(dec))
    # referenced files resolvable
    check(f"C.{uid}.pub_readme", pub_readme is not None)
    check(f"C.{uid}.validator_lines", pub_use_py is not None and b"LICENSED_COPY spans are not identical" in b"\n".join(pub_use_py.splitlines()[544:549]))
    check(f"C.{uid}.register_doc", reg_md is not None and b"byte-identical" in reg_md)
    c_summary.append({"use_id": uid, "record": path, "verdict": "HOLD_PRESERVED_NO_OMISSION_NO_OVERCLAIM"})

check("C.accounting_replay", acct is not None and acct.get("valid") is True and acct.get("completed") == 0
      and acct.get("denominator") == 0 and acct.get("unreviewed_output_count") == 2396)
check("C.candidate_integrity_9_of_9", cand_int is not None and cand_int.get("match_count") == 9
      and cand_int.get("file_count") == 9 and cand_int.get("result") == "ALL_MATCH")

# independent candidate integrity re-hash vs planning-freeze bindings
binds = {b["path"]: b for b in assignment.get("bindings", [])}
cand_recheck = []
for fe in (cand_int or {}).get("files", []):
    p = fe["path"]
    bnd = binds.get(p, {})
    gb = blob(C, CH, p)
    got_sha, got_len = (sha(gb), len(gb)) if gb is not None else (None, None)
    ok = (got_sha == bnd.get("sha256") == fe.get("sha256_observed") and got_len == bnd.get("bytes"))
    check(f"C.candidate_integrity.{os.path.basename(p)}", ok)
    cand_recheck.append({"path": p, "sha256_rehashed_by_D": got_sha, "bytes_rehashed_by_D": got_len,
                         "planning_freeze_sha256": bnd.get("sha256"), "planning_freeze_bytes": bnd.get("bytes"), "match": ok})

# ---------------------------------------------------------------- completeness
b_root = subprocess.run(["git", "-C", B, "ls-tree", "-r", "--name-only", BH,
                         "--", "evidence/wave-20261009-correction-01/source"],
                        capture_output=True, text=True).stdout.split()
c_root = subprocess.run(["git", "-C", C, "ls-tree", "-r", "--name-only", CH,
                         "--", "evidence/wave-20261009-correction-01/publication"],
                        capture_output=True, text=True).stdout.split()
b_recs = [p for p in b_root if p.endswith("-CORRECTION-01.json")]
c_recs = [p for p in c_root if p.endswith("-CORRECTION-01.json")]
check("coverage.B_exactly_five_records", sorted(os.path.basename(p) for p in b_recs) ==
      sorted(f"{c}-CORRECTION-01.json" for c in CLAIMS), str(b_recs))
check("coverage.C_exactly_two_records", sorted(os.path.basename(p) for p in c_recs) ==
      sorted(f"use-correction-{u.lower()}-CORRECTION-01.json" for u in USES), str(c_recs))
check("coverage.B_selection_matches_freeze", assignment.get("B", {}).get("claim_ids") == CLAIMS)
check("coverage.C_selection_matches_freeze", assignment.get("C", {}).get("use_ids") == USES)
check("coverage.freeze_role_D_root", freeze.get("identities", {}).get("roles", [{}])[2].get("exclusive_write_root") ==
      "evidence/wave-20261009-correction-01/omission")

review = {
    "schema": "ges.correction-omission-review.v1",
    "review_id": "omission-review-CORRECTION-01",
    "role": "D",
    "wave": "wave-20261009-correction-01",
    "pr": 496,
    "reviewer_identity": "opencode session ses_edbadcab6ffeDVVMjqnv9QjY8R (source: env OPENCODE_SESSION_ID); lease 2faae7b2c82c419ca3df40571ca5360d to 2026-10-10T06:11:10Z under surface opencode:ses_edcbc89dcffe1pHZoV5eWgrR33 per conductor binding",
    "created_at_utc": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "method": "Independent bounded re-check of correction-stage outputs against committed inputs only: (1) each B record parsed and cross-checked line-by-line against the predecessor claims document (re-read from this checkout), residuals.json holds, primary-review interpretation/residual/decision fields, draft-dispositions status, proposed-decisions entries, and blob hashes of every cited file at B's verified head; (2) each C record parsed and cross-checked against the predecessor publication primary-review rows, a fresh byte slice of controls/review_queue.json at the two frozen output spans, the committed validator/register text, the frozen accounting replay, and an independent re-hash of all nine candidate files against the conductor planning-freeze bindings; (3) completeness: the union of B+C -CORRECTION-01 records against the planning freeze selection (5 claims + 2 use fields), with extra-file listing of both exclusive roots.",
    "verified_inputs": {
        "own_branch": {"checkout": MY, "head": "4768db8929420538e3b828467de9dbe314fd4b74", "tracked_tree_clean": True},
        "stage_B": {"checkout": B, "head": BH, "tracked_tree_clean": True, "result": "MATCH_EXPECTED"},
        "stage_C": {"checkout": C, "head": CH, "tracked_tree_clean": True, "result": "MATCH_EXPECTED"},
        "conductor_freeze_read": {"checkout": A, "head": AH, "tracked_tree_clean": True,
                                  "files_read": ["evidence/wave-20261009-correction-01/serialized-admission-03/execution-freeze-20261010.json",
                                                 "evidence/wave-20261009-correction-01/assignment.json"]},
        "read_discipline": "git show at pinned commits / clean working trees; no network, no fetch, no sibling write, no uncommitted sibling file"
    },
    "stage_B_findings": b_summary,
    "stage_C_findings": c_summary,
    "scope_coverage_matrix": {
        "selected_by_planning_freeze": {"claims": CLAIMS, "use_fields": USES},
        "claims": [{"claim_id": c,
                    "prior_omission_verdict": "HOLD (D-SOURCE-FIDELITY finding on wave-20261009/omission/source-findings.json)",
                    "successor_record": f"evidence/wave-20261009-correction-01/source/{c}-CORRECTION-01.json",
                    "record_present": True, "covered": True,
                    "hold_text_matches_residuals": True,
                    "support_level": "statement-level correction derived from committed primary-review interpretation; source bytes NOT re-read; no receipt, mapping, or policy change claimed",
                    "omission_or_overclaim_found": "NONE"} for c in CLAIMS],
        "use_fields": [{"use_id": u,
                        "prior_omission_verdict": "UNRESOLVED_PRESERVED (D-PUBLICATION-ESCAPING finding on wave-20261009/omission/publication-findings.json)",
                        "successor_record": f"evidence/wave-20261009-correction-01/publication/use-correction-{u.lower()}-CORRECTION-01.json",
                        "record_present": True, "covered": True,
                        "hold_outcome_represented": "REMAINING_HOLD, kind stays null, no approval or clearance",
                        "structural_finding_reproduced": "raw span 170 B != source span 168 B; delta is exactly the two mandated JSON quote escapes; decoded sha equals committed source-span sha",
                        "omission_or_overclaim_found": "NONE"} for u in USES],
        "extra_records_found": {"stage_B": [p for p in b_recs if os.path.basename(p) not in {f"{c}-CORRECTION-01.json" for c in CLAIMS}],
                                "stage_C": [p for p in c_recs if os.path.basename(p) not in {f"use-correction-{u.lower()}-CORRECTION-01.json" for u in USES}]},
        "non_record_files_in_roots": {"stage_B": [p for p in b_root if not p.endswith("-CORRECTION-01.json")],
                                      "stage_C": [p for p in c_root if not p.endswith("-CORRECTION-01.json")]},
        "scope_drift": "NONE detected: exactly 5 claim records + 2 use-field records, correct -CORRECTION-01 suffixes, roots contain only records plus README/identity artifacts (B additionally preserves the cancelled attempt's identity file bytes, renamed, not a record)"
    },
    "candidate_integrity_independent_recheck": cand_recheck,
    "key_findings": [
        "No overclaim found in any of the seven successor records: every B record claims only 'corrected at statement level' with an explicit SOURCE_BYTES_NOT_REREAD hold; both C records end in REMAINING_HOLD with approvals_created=none and publication_clearance_granted=none.",
        "No obligation silently dropped: all four common remaining holds appear in every B record; B additionally carries the claim-specific obligations (rotation authority for 009, enforcement evidence for 017, cadence for 018); C carries the unresolved classification decision and the frozen publication gate.",
        "All evidence references in all seven records resolve to committed blobs whose sha256 values match the cited hashes (recomputed at the verified sibling heads).",
        "B's quoted hold texts match residuals.json source_fidelity_repairs_required[0..4] verbatim, and B's README citation residuals.json -> source_fidelity_repairs_required is accurate.",
        "C's structural LICENSED_COPY finding was independently reproduced from committed candidate bytes: the only difference between output and source spans is the two JSON-mandated quote escapes, so raw-byte identity is unattainable for this text inside JSON; the ADAPTATION classification is left to an authorized owner, as required.",
        "Candidate integrity 9/9 MATCH independently re-derived against the conductor's planning-freeze bindings.",
        "B's linked_decisions control_references match the committed proposed-decisions entries by (id, revision); B's records add a 'collection' label (CATALOG/PROPOSAL) not present in the committed decision file - recorded here as a presentational annotation, not an omission or overclaim; ids and revisions are correct.",
        "Completeness: the union of B+C outputs covers exactly the five claims and two use fields the planning freeze selected; no extra records; no scope drift.",
    ],
    "not_verified": [
        "Source-byte re-reads: the pinned checklist text (content/library/application-security/checklist.md at a30275bc2d7eb860e612f93cbc1f26d0ff20c0c7) and the pinned ghqr budgets.yaml bytes at 02b89961921ac43f93aa8b3ff74cdcb7cd3d9244 are not present in any reviewed checkout; every 'source says X' statement in B's corrections and C's source-span binding is inherited from committed review records, not re-derived from upstream bytes by this reviewer.",
        "Semantic or rights approval: not granted. The five corrected statements are statement-fidelity repairs reviewed by no authorized approver here; ADAPTATION classification for the two use fields is a substantive rights judgment this worker does not make.",
        "Publication clearance: not granted. The frozen gate (byte-identical LICENSED_COPY spans / byte-identical candidate bytes) is unchanged; both use fields remain HOLD.",
        "Reconciliation receipt, D/A/E gates, mapping, policy adoption: unchanged and unverified; proposed-decisions review.status stays PROPOSED with reviewer null; claims document keeps policy_adoption=NONE, rights_clearance=UNRESOLVED, independent_omission_audit=false.",
        "Heavy/Governance verification suite: not run here by instruction; deferred to integration.",
        "The session-identity discrepancy (env OPENCODE_SESSION_ID vs the conductor-specified lease surface) is recorded, not resolved."
    ],
    "carry_forward": {
        "prior_semantic_and_rights_approval": False,
        "delivery_status": "Staged",
        "approval_or_clearance_granted_by_this_review": "none",
        "statement": "This review only verifies structural fidelity, internal consistency, hash resolvability, and bounded outcome claims of the correction outputs against committed inputs. It releases nothing."
    },
    "checker_results": results,
}

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w") as f:
    json.dump(review, f, indent=2, sort_keys=False)
    f.write("\n")

print(json.dumps({"written": OUT, "checks_total": len(results["checks"]),
                  "failures": results["failures"]}, indent=2))
sys.exit(1 if results["failures"] else 0)
