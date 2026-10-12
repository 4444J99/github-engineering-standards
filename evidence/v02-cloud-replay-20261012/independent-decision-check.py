"""Independent exact comparison of a nonissued draft; no GES imports or issuance.

The semantic findings below are the current reviewer's authored observations after
reading the ten draft rows, their source context, and ten control records. Running
this script reproduces their byte bindings and exhaustive mechanical comparisons;
it does not turn a future execution into a new semantic review or receipt grant.
"""
from __future__ import annotations
from collections import Counter
from datetime import datetime, timezone
import gzip
import hashlib
import io
import json
from pathlib import Path
import stat
import subprocess
import sys
import time

if not __debug__:
    raise SystemExit("Independent review requires assertions enabled")

ROOT = Path("/workspace/scratch/9f3cdabec13b/ges")
WORK = ROOT / ".cache/cloud-replay-20261012/fresh-pinned"
DRAFT = ROOT / ".cache/cloud-replay-20261012/replacement-draft"
OUTPUT = Path("/workspace/scratch/9f3cdabec13b/migration_review_replacement_draft_review.json")
ACTOR = "chatgpt-cloud:20261012:9f3cdabec13b:/root/migration_review"
HEAD = "6c37fe5eb98039341cb49444305703dc43048685"
CURRENT = "4c9c65b1c59f656d0a8bc423ee84c26e835754f7fca02ac4cc8df8e27f5bd20b"
HISTORICAL = "9e4116b7a70772c94f59e1f5b1a27b1a736c15a8cae78341586a12bf8f80bd0d"
CATALOG = "125555b58ee9cfc66af0fb335429911005f1f9ad1da555ea4f0acd51602ec24c"
PROPOSAL = "e16b506ada35741ea1d61f93bcf11b846893b643eb6e25eaed4a6edb70cf59d4"
SOURCE = "github/github-well-architected"
COMMIT = "a30275bc2d7eb860e612f93cbc1f26d0ff20c0c7"
SOURCE_PATH = "content/library/application-security/checklist.md"
SOURCE_SHA = "d460c2c2daf45d6914cc15b908f1e487d0e4afe8e28632706b58ccddaab27773"
SOURCE_BLOB = "defd8205c96f51216141ce047dc9f91971bd47a7"
PAIRS = [
    ("WA-APPSEC-005", 21, "GES-SEC-003", "GES-OPS-041", "SRC-WA-f2588aac5b8db563"),
    ("WA-APPSEC-009", 27, "GES-SEC-004", "GES-OPS-045", "SRC-WA-21ba8f727520fdc5"),
    ("WA-APPSEC-011", 31, "GES-GOV-010", "GES-OPS-047", "SRC-WA-a441e3f909b1c6a3"),
    ("WA-APPSEC-017", 41, "GES-GOV-003", "GES-OPS-053", "SRC-WA-07b58ba8ebb9ab92"),
    ("WA-APPSEC-018", 42, "GES-GOV-008", "GES-OPS-054", "SRC-WA-7fa32a56e702a377"),
]
SEMANTIC = {
    "WA-APPSEC-005": "Source context recommends code scanning in CI/CD generally. The original static-analysis wording narrows that recommendation. Supersession preserves the original record, while the successor SPECIALIZE scope retains general code scanning and avoids claiming completed analysis under the broader catalog control.",
    "WA-APPSEC-009": "Source context recommends actual recurring rotation of both secrets and credentials. A reviewed rotation practice alone is weaker; exposure-triggered response in the catalog is a separate condition. The successor preserves rotation without an exposure prerequisite and adds neither a numerical schedule nor operating authority.",
    "WA-APPSEC-011": "The Security Policies section makes policies accessible to all team members. The predecessor's relevant-contributor restriction loses that scope. The successor decision explicitly preserves security-policy accessibility for the whole team, independently of the catalog's training and governance-feedback duties.",
    "WA-APPSEC-017": "Source context calls for actual role-based access control limiting access to GitHub and other business systems. Role assignment documentation alone does not establish that limitation. The successor retains both system classes and enforcement meaning without claiming deployment or effective operation.",
    "WA-APPSEC-018": "Source context calls for recurring examination of access logs for suspicious activity across GitHub and other business systems. Investigation of already detected suspicious activity alone loses the recurring examination. The successor preserves both systems and recurrence without inventing cadence, retention or incident-response duties.",
}

started = datetime.now(timezone.utc).isoformat()
tick = time.monotonic()
checks = 0
fingerprints = {}

def require(name, condition):
    global checks
    checks += 1
    if not condition:
        raise ValueError(name)
    if time.monotonic() - tick > 55:
        raise TimeoutError("Independent review internal 55-second deadline")

def norm(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)

def digest(value):
    return hashlib.sha256(norm(value).encode()).hexdigest()

def strict_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate JSON object key: " + key)
        result[key] = value
    return result

def parse(raw):
    return json.loads(raw, object_pairs_hook=strict_object,
                      parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))

def state(path):
    for component in (path, *path.parents):
        require("no_symlink:" + str(component), not component.is_symlink())
    s = path.lstat()
    require("regular_file:" + str(path), stat.S_ISREG(s.st_mode))
    return (s.st_dev, s.st_ino, s.st_size, s.st_mtime_ns, s.st_ctime_ns)

def read(path, expected=None):
    before = state(path)
    raw = path.read_bytes()
    after = state(path)
    sha = hashlib.sha256(raw).hexdigest()
    require("stable_read:" + str(path), before == after)
    if expected:
        require("pinned_raw_sha:" + str(path), sha == expected)
    value = {"sha256": sha, "stat": list(after)}
    if str(path) in fingerprints:
        require("stable_repeated_read:" + str(path), value == fingerprints[str(path)])
    fingerprints[str(path)] = value
    return raw

def load(path, expected=None):
    return parse(read(path, expected))

draft_path = DRAFT / "replacement-decisions.draft.json"
old_path = ROOT / "evidence/wave-20261009/integration/combined-reconciliation.json"
draft = load(draft_path, "a8b9065b0a5a43e950451683badcbeaa335cc344bbce78940dac4420fb6d7185")
old = load(old_path, "63d1b79fe2b9d58207050abdb593adbe1ebd009bbc327643e599dd4515d6ac5c")
origins_path = DRAFT / "decision-origins.json"
origins = load(origins_path, "91822aac4169bffaec4bc47520c05322717049958598f7ed33cc848aee1923e0")
preparation = load(DRAFT / "preparation.json")
audit = load(ROOT / "evidence/v02-finish-20261010/claim-migration-audit.json", "9c17a1fcbfee8a38e5d7dc49e95e4df108f96b43dc8e51ad744342c4d0ba4e04")
inventory = load(ROOT / "evidence/claim-workload-v02-inventory.json", "ed4ee7e8be9a5369d4651769dc8717456473063d2db21010544349a9848b8a00")
provenance = load(WORK / "claim-provenance.log", "c174b9b941667bdbbcc5a35b548ac403e7763112e3926f31704242c33b76fcd6")
accounting = load(WORK / "current-reconciliation-without-envelopes.log", "f928b74702aba91bf3ac74746fc473a3de1b5637378b4c71d7210c568187a7a6")
execution = load(WORK / "execution.json", "da51b1279a8a7bd6b671193774180e2eab406049b9b6af1729b9f2ef83840937")
read(ROOT / ".cache/cloud-replay-20261012/prepare_replacement_draft.py", "3546278e187db572071acc296963480be6a0f485e069f7eebef2e8043e597cd1")
require("head", subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip() == HEAD)
require("old_canonical_digest", digest(old) == "6dbc2f4ddee55e1dfae40c4a3acb121cb1d57a86c6ed9e7ed77a36644a96a9ee")
require("draft_canonical_digest", digest(draft) == "010aa6e9003301d96825cb1f34b317bafb401783e9f7462c40ac1c7d05bbb8e6")

artifacts = {}
for rawline in read(WORK / "artifacts.oct7.jsonl", "86225491fb70197b893a0bfb1fa96ebfc1f5a6e33c21c86ab874d9d34f5db9a2").splitlines():
    row = parse(rawline)
    key = tuple(row[k] for k in ("source", "commit", "path"))
    require("unique_artifact", key not in artifacts)
    artifacts[key] = row
require("artifact_denominator", len(artifacts) == 13657)
expected_docs = {x["path"]: x for x in inventory["inputs"]["claim_documents"]}
paths = sorted((ROOT / "evidence/source-reviews").glob("*-claims.json"))
require("complete_document_membership", len(paths) == len(expected_docs) == len(inventory["inputs"]["claim_documents"]) == 655 and {p.name for p in paths} == set(expected_docs))
require("replay_consumed_exact_documents", len(provenance["review_documents"]) == 655 and {Path(x["path"]).name: x["sha256"] for x in provenance["review_documents"]} == {name: x["sha256"] for name, x in expected_docs.items()})
subjects = {}
claims = {}
for path in paths:
    document = load(path, expected_docs[path.name]["sha256"])
    require("document_claim_count", len(document["claims"]) == expected_docs[path.name]["claims"])
    for claim in document["claims"]:
        cid = claim["claim_id"]
        require("unique_claim", cid not in subjects)
        source, commit, source_path = (claim.get(k, document.get(k)) for k in ("source", "commit", "path"))
        art = artifacts[(source, commit, source_path)]
        subjects[cid] = {
            "claim_id": cid, "source": source, "commit": commit, "path": source_path,
            "artifact_id": art["artifact_id"], "content_sha256": art["sha256"],
            "start_line": claim["start_line"], "end_line": claim["end_line"],
            "statement_sha256": hashlib.sha256(claim["statement"].encode()).hexdigest(),
            "claim_document": path.name, "claim_document_sha256": expected_docs[path.name]["sha256"],
        }
        claims[cid] = claim
successors = {p[0] + "-CORRECTION-01" for p in PAIRS}
new_ids = successors | {p[0] for p in PAIRS}
require("current_subject_universe", len(subjects) == 61941 and digest([subjects[c] for c in sorted(subjects)]) == CURRENT)
require("historical_subject_universe", len(set(subjects) - successors) == 61936 and digest([subjects[c] for c in sorted(set(subjects) - successors)]) == HISTORICAL)
catalog = load(ROOT / "controls/catalog.json")
proposals = load(ROOT / "controls/review_queue.json")
require("catalog_binding", digest(catalog) == CATALOG)
require("proposal_binding", digest(proposals) == PROPOSAL)
control_index = {}
for collection, rows in (("CATALOG", catalog), ("PROPOSAL", proposals)):
    for row in rows:
        key = (collection, row["id"], row["revision"])
        require("unique_control_identity", key not in control_index)
        control_index[key] = row
old_by_id = {r["claim"]["claim_id"]: (i, r) for i, r in enumerate(old)}
draft_by_id = {r["claim"]["claim_id"]: r for r in draft}
origin_by_id = {r["claim_id"]: r for r in origins}
require("historical_unique_2164", len(old_by_id) == len(old) == 2164)
require("draft_unique_2174", len(draft_by_id) == len(draft) == 2174)
require("origin_unique_2174", len(origin_by_id) == len(origins) == 2174)
require("exact_membership", not (set(old_by_id) & new_ids) and set(draft_by_id) == set(origin_by_id) == set(old_by_id) | new_ids)
require("sorted_draft", [x["claim"]["claim_id"] for x in draft] == sorted(draft_by_id))
require("sorted_origins", [x["claim_id"] for x in origins] == sorted(origin_by_id))
fields = {"schema", "claim", "claim_input_digest", "catalog_digest", "proposal_digest", "disposition", "control_references", "details", "rationale", "reconciler", "independent_reviewer", "reconciled_at", "reviewed_at", "accepted_policy", "adopted_obligation"}
mutable = {"schema", "claim_input_digest", "reconciler", "independent_reviewer", "reconciled_at", "reviewed_at"}
role_fields = mutable - {"schema", "claim_input_digest"}
preserved_field_comparisons = 0
all_reference_checks = 0
for cid, row in draft_by_id.items():
    require("exact_draft_keys:" + cid, set(row) == fields)
    require("nonissued_schema:" + cid, row["schema"] == "ges.claim-reconciliation-receipt.draft.v1")
    require("null_issuance_fields:" + cid, all(row[k] is None for k in role_fields))
    require("nonadoption:" + cid, row["accepted_policy"] is False and row["adopted_obligation"] is None)
    require("current_bindings:" + cid, (row["claim_input_digest"], row["catalog_digest"], row["proposal_digest"]) == (CURRENT, CATALOG, PROPOSAL))
    require("current_exact_subject:" + cid, norm(row["claim"]) == norm(subjects[cid]))
    require("nonempty_rationale:" + cid, type(row["rationale"]) is str and bool(row["rationale"].strip()))
    for ref in row["control_references"]:
        require("exact_reference_shape:" + cid, set(ref) == {"collection", "id", "revision"} and type(ref["revision"]) is int)
        require("actual_reference:" + cid, (ref["collection"], ref["id"], ref["revision"]) in control_index)
        all_reference_checks += 1
    if cid in old_by_id:
        old_index, prior = old_by_id[cid]
        require("historical_keys_and_binding:" + cid, set(prior) == fields and prior["schema"] == "ges.claim-reconciliation-receipt.v1" and prior["claim_input_digest"] == HISTORICAL)
        for field in sorted(fields - mutable):
            require("preserved_field:" + cid + ":" + field, norm(row[field]) == norm(prior[field]))
            preserved_field_comparisons += 1
        require("exact_carried_origin:" + cid, norm(origin_by_id[cid]) == norm({"claim_id": cid, "kind": "UNCHANGED_CARRIED_DECISION", "historical_array_index": old_index, "historical_receipt_canonical_digest": digest(prior)}))
require("preserved_field_count", preserved_field_comparisons == 2164 * 9)

wa_path = WORK / "sources/github__github-well-architected.text.jsonl.gz"
wa_raw = read(wa_path, "67fb276d9d21e636ff8f4d90c2ecac3bdb41c44a61bd15021c92af07601afeed")
wa_rows = [parse(line) for line in gzip.decompress(wa_raw).splitlines()]
source_matches = [r for r in wa_rows if (r["source"], r["commit"], r["path"]) == (SOURCE, COMMIT, SOURCE_PATH)]
require("unique_source_target", len(source_matches) == 1)
source = source_matches[0]
body = source["content"].encode()
require("source_body_sha", hashlib.sha256(body).hexdigest() == source["sha256"] == SOURCE_SHA)
require("source_body_git_blob", hashlib.sha1(b"blob " + str(len(body)).encode() + b"\0" + body).hexdigest() == source["git_blob_sha"] == SOURCE_BLOB)
require("source_size", len(body) == source["size"] == 13719)
require("source_original_metadata_identity", artifacts[(SOURCE, COMMIT, SOURCE_PATH)]["sha256"] == SOURCE_SHA and artifacts[(SOURCE, COMMIT, SOURCE_PATH)]["git_blob_sha"] == SOURCE_BLOB)
lines = source["content"].splitlines()
approved = {r["predecessor"]: r for r in audit["proposed_decisions"]}
require("exact_approved_pairs", len(approved) == len(audit["proposed_decisions"]) == 5 and set(approved) == {p[0] for p in PAIRS})
semantic_findings = []
for pred, line, cat, prop, structured in PAIRS:
    succ = pred + "-CORRECTION-01"
    old_draft, new_draft = draft_by_id[pred], draft_by_id[succ]
    approval = approved[pred]
    require("approved_pair_and_refs:" + pred, (approval["successor"], approval["catalog"], approval["proposal"], approval["revision"], approval["predecessor_disposition"], approval["basis"], approval["successor_disposition"]) == (succ, cat, prop, 1, "EXCLUDED_WITH_REASON", "SUPERSEDED", "SPECIALIZE"))
    require("exact_supersession:" + pred, old_draft["disposition"] == "EXCLUDED_WITH_REASON" and old_draft["control_references"] == [] and set(old_draft["details"]) == {"basis", "exclusion_reason", "related_claim_ids"} and old_draft["details"]["basis"] == "SUPERSEDED" and old_draft["details"]["related_claim_ids"] == [succ] and bool(old_draft["details"]["exclusion_reason"].strip()))
    require("exact_specialization:" + succ, new_draft["disposition"] == "SPECIALIZE" and norm(new_draft["control_references"]) == norm([{"collection": "CATALOG", "id": cat, "revision": 1}, {"collection": "PROPOSAL", "id": prop, "revision": 1}]) and set(new_draft["details"]) == {"scope", "distinction"} and all(type(v) is str and bool(v.strip()) for v in new_draft["details"].values()))
    require("exact_reverse_relation:" + succ, claims[succ]["supersedes_claim_id"] == pred)
    for cid in (pred, succ):
        subject = subjects[cid]
        require("same_source_identity_and_span:" + cid, (subject["source"], subject["commit"], subject["path"], subject["content_sha256"], subject["start_line"], subject["end_line"], subject["artifact_id"]) == (SOURCE, COMMIT, SOURCE_PATH, SOURCE_SHA, line, line, "8109355ec58c910ed86a2618"))
        require("same_structured_occurrence:" + cid, claims[cid]["structured_requirement_ids"] == [structured])
        require("new_exact_origin:" + cid, norm(origin_by_id[cid]) == norm({"claim_id": cid, "kind": "NEW_PREDECESSOR_SUPERSESSION" if cid == pred else "NEW_SUCCESSOR_SPECIALIZATION"}))
    require("structured_id_from_actual_line:" + pred, "SRC-WA-" + digest([SOURCE_PATH, line, lines[line - 1].strip()[2:]])[:16] == structured)
    catalog_record = control_index[("CATALOG", cat, 1)]
    proposal_record = control_index[("PROPOSAL", prop, 1)]
    require("catalog_still_draft:" + cat, catalog_record["status"] == "REVIEWED_DRAFT" and catalog_record["enforcement"]["native_deployed"] is False)
    require("proposal_still_quarantined:" + prop, proposal_record["status"] == "NON_ADOPTED_DRAFT" and bool(proposal_record["quarantine_reason"]) and proposal_record["enforcement"]["native_deployed"] is False)
    semantic_findings.append({
        "predecessor": pred, "successor": succ, "source_line": line,
        "predecessor_disposition": "EXCLUDED_WITH_REASON", "basis": "SUPERSEDED", "successor_disposition": "SPECIALIZE",
        "result": "PASS_FOR_EXACT_NONISSUED_DRAFT_DISPOSITIONS",
        "reviewer_reasoning": SEMANTIC[pred],
        "source_line_utf8_sha256": hashlib.sha256(lines[line - 1].encode()).hexdigest(),
        "predecessor_draft_canonical_digest": digest(old_draft), "successor_draft_canonical_digest": digest(new_draft),
        "catalog": {"id": cat, "revision": 1, "canonical_digest": digest(catalog_record)},
        "proposal": {"id": prop, "revision": 1, "canonical_digest": digest(proposal_record)},
    })
require("exact_successor_document_membership", {c for c, s in subjects.items() if s["claim_document"] == "wa-application-security-correction-01-claims.json"} == successors)
require("exact_origin_kind_counts", Counter(x["kind"] for x in origins) == {"UNCHANGED_CARRIED_DECISION": 2164, "NEW_PREDECESSOR_SUPERSESSION": 5, "NEW_SUCCESSOR_SPECIALIZATION": 5})
require("actual_replay_bindings", provenance["valid"] is True and provenance["reference_claims"] == 61941 and accounting["valid"] is True and accounting["claim_provenance_validated"] is True and (accounting["claim_input_digest"], accounting["catalog_digest"], accounting["proposal_digest"]) == (CURRENT, CATALOG, PROPOSAL))
require("actual_accounting_still_no_receipts", accounting["validated_count"] == 0 and accounting["unresolved_count"] == 61941 and accounting["validated_claim_ids"] == [] and accounting["receipts_digest"] == digest([]) and accounting["policy_digest"] == digest({}))
require("preparation_correct", preparation["revision"] == HEAD and preparation["carried_decisions"] == 2164 and preparation["draft_decisions"] == 2174 and preparation["claim_denominator"] == 61941 and preparation["draft_sha256"] == fingerprints[str(draft_path)]["sha256"] and preparation["draft_canonical_digest"] == digest(draft) and preparation["replacement_envelopes_issued"] is False and preparation["validated_current_receipts"] == 0)
for name, expected in (("claim_input_digest", CURRENT), ("catalog_digest", CATALOG), ("proposal_digest", PROPOSAL)):
    require("preparation_binding:" + name, preparation[name] == expected)
require("fresh_replay_scope", execution["head"] == HEAD and execution["status"] == "PASS" and execution["text_artifacts_authenticated"] == 11828)

for path, fingerprint in list(fingerprints.items()):
    read(Path(path), fingerprint["sha256"])
require("final_document_membership_unchanged", {p.name for p in (ROOT / "evidence/source-reviews").glob("*-claims.json")} == set(expected_docs))
require("final_head_unchanged", subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip() == HEAD)
script_sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
result = {
    "schema": "ges.independent-nonissued-replacement-draft-review.v1",
    "status": "PASS_EXACT_CARRYFORWARD_AND_TEN_DRAFT_DISPOSITIONS",
    "reviewer": ACTOR, "reviewer_role": "Actual current independent agent performing read-only comparison and semantic review; not an original Codex actor, authorized receipt issuer, or human approver.",
    "revision": HEAD, "started_at": started, "completed_at": datetime.now(timezone.utc).isoformat(),
    "elapsed_seconds": round(time.monotonic() - tick, 6),
    "duration_scope": "Actual bounded verification-script runtime; semantic reading and reasoning occurred in this agent turn before execution and are not assigned a fabricated runtime.",
    "command": ["timeout", "60s", "python", str(Path(__file__))],
    "actual_python_executable": sys.executable, "python_version": sys.version, "python_optimization": sys.flags.optimize,
    "script_sha256": script_sha, "draft_sha256": fingerprints[str(draft_path)]["sha256"], "draft_canonical_digest": digest(draft),
    "historical_receipts_sha256": fingerprints[str(old_path)]["sha256"], "historical_receipts_canonical_digest": digest(old),
    "historical_receipts_unchanged": True,
    "known_current_claims": len(subjects), "claim_documents": len(paths), "source_artifact_metadata_rows": len(artifacts),
    "current_claim_input_digest": CURRENT, "historical_claim_input_digest_reproduced": HISTORICAL,
    "catalog_digest": CATALOG, "proposal_digest": PROPOSAL,
    "carried_decisions_compared": len(old), "carried_exact_subjects_compared": len(old),
    "carried_subject_field_count": 2164 * 11, "preserved_top_level_field_comparisons": preserved_field_comparisons,
    "preserved_fields": sorted(fields - mutable), "permitted_envelope_changes": sorted(mutable),
    "carried_subject_mismatches": 0, "carried_decision_field_mismatches": 0,
    "draft_decisions": len(draft), "origin_records_checked": len(origins), "control_reference_records_checked": all_reference_checks,
    "missing_extra_or_duplicate_draft_claims": 0, "new_predecessor_supersessions": 5, "new_successor_specializations": 5,
    "logical_repairs": 5, "raw_claim_growth": 5,
    "null_actor_fields_checked": 2174 * 2, "null_timestamp_fields_checked": 2174 * 2,
    "nonadoption_rows_checked": 2174, "current_subjects_checked": 2174,
    "independent_mechanical_checks_passed": checks,
    "all_consumed_files_regular_without_symlinks_and_stable_before_after": True,
    "input_file_count": len(fingerprints),
    "input_file_sha256": {str(Path(p).relative_to(ROOT)): x["sha256"] for p, x in sorted(fingerprints.items())},
    "source_semantic_review": {"source": SOURCE, "commit": COMMIT, "path": SOURCE_PATH, "content_sha256": SOURCE_SHA, "git_blob_sha": SOURCE_BLOB, "size": len(body), "context_lines_read": [19, 42], "source_snapshot_sha256": fingerprints[str(wa_path)]["sha256"], "findings": semantic_findings},
    "replacement_envelopes_issued": False, "validated_current_receipts": 0, "actual_unresolved_current_claims": 61941,
    "conditional_after_authentic_grant_issuance_and_validation": {"validated_dispositions": 2174, "unresolved_claims": 59767, "is_actual_result": False},
    "material_findings": [],
    "limits": [
        "This compares an explicitly nonissued custom-schema draft. Null actors and timestamps remain null. No receipt grant, valid receipt, adoption, rights clearance, publication clearance, human approval or v0.2 acceptance is issued here.",
        "All 2164 carried subjects and decision fields are exactly preserved against the pinned historical receipt. This is independent carryforward comparison, not a fresh semantic adjudication of every carried decision or a claim that the historical receipt envelopes validate against the enlarged universe.",
        "All ten new dispositions were semantically reviewed by the actual current reviewer against authenticated source content and exact catalog/proposal records. The script binds that authored review and reproduces its mechanical checks; it does not automate semantic judgment.",
        "Referenced proposals remain NON_ADOPTED_DRAFT and quarantined, with generic repository scope and unfilled source digest fields. Exact current input/subject bindings and explicit decision scope support these draft mappings, but do not promote the proposal records, erase quarantine, or verify evaluators, deployments or operational bindings.",
        "The completed fresh-pinned replay authenticated the current source provenance; original native caches, retained rendered bodies and the complete original A3 capsule were not restored or certified. This bounded review directly reread only the WA source snapshot, while reconstructing every current subject from committed metadata and claim-document bytes.",
        "An authentic renewed current-actor role grant remains pending. After grant and actual issuance, every final envelope must be compared again with this exact reviewed draft, including fresh bindings, real actors, actual chronological timestamps and receipt policy. This earlier draft-review time must not be reused to backdate a later envelope review.",
        "Historical 2164 in the replay driver was a prior-report reference; the replay without receipt inputs validated zero current dispositions. The later 2174/59767 accounting remains conditional until authorized envelopes pass validation."
    ],
}
with OUTPUT.open("x") as stream:
    json.dump(result, stream, indent=2, sort_keys=True)
    stream.write("\n")
print(json.dumps({"status": result["status"], "elapsed_seconds": result["elapsed_seconds"], "checks_passed": checks, "carried_rows": 2164, "new_dispositions": 10, "output": str(OUTPUT), "output_sha256": hashlib.sha256(OUTPUT.read_bytes()).hexdigest(), "script_sha256": script_sha}, sort_keys=True))
