#!/usr/bin/env python3
"""Verify the bounded pinned-source reread for correction wave 01."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any


SOURCE = "github/github-well-architected"
COMMIT = "a30275bc2d7eb860e612f93cbc1f26d0ff20c0c7"
SOURCE_PATH = "content/library/application-security/checklist.md"
CONTENT_SHA256 = "d460c2c2daf45d6914cc15b908f1e487d0e4afe8e28632706b58ccddaab27773"
CACHE_SNAPSHOT_SHA256 = "8f13d7adfc4b6d1a108acc7381936ec471ddbc7d932f4f9991c8012067ca4b27"
INVENTORY_DIGEST = "b5939b61905bd3b0d4f9a6c7449e382748a59af2c04f6ede214859cd7d3c73c4"
GIT_BLOB_SHA = "defd8205c96f51216141ce047dc9f91971bd47a7"
A_BEFORE_INTEGRATION = "3d4c0bf7504e69719c8c5d8edc613cffb2c27052"
A_AFTER_WORKER_INTEGRATION = "e8f3d5eb772bd8cba16a665d59ab3322c7d87d91"
EXCLUSIVE_ROOT_IDENTITY = "MATCH for B/C/D/E after additions-only cherry-picks"
CLAIM_LINES = {
    "WA-APPSEC-005": 21,
    "WA-APPSEC-009": 27,
    "WA-APPSEC-011": 31,
    "WA-APPSEC-017": 41,
    "WA-APPSEC-018": 42,
}
WORKER_ROOTS = {
    "B": (
        "c034c82d6e15b29e30711f3cb77b53d5a61e206c",
        "evidence/wave-20261009-correction-01/source",
    ),
    "C": (
        "a29214dc5ff55dd5df6176a80d1f4478789a9beb",
        "evidence/wave-20261009-correction-01/publication",
    ),
    "D": (
        "4e137f69448ac10fe20002838941369b72d255b1",
        "evidence/wave-20261009-correction-01/omission",
    ),
    "E": (
        "2dad9e426d75977d1e436679c0d20ecb036ad774",
        "evidence/wave-20261009-correction-01/audit",
    ),
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def load_source_row(path: Path) -> dict[str, Any]:
    matches: list[dict[str, Any]] = []
    with gzip.open(path, "rt", encoding="utf-8") as handle:
        for raw_line in handle:
            row = json.loads(raw_line)
            if row.get("source") == SOURCE and row.get("path") == SOURCE_PATH:
                matches.append(row)
    if len(matches) != 1:
        raise ValueError(f"expected one pinned source row, found {len(matches)}")
    return matches[0]


def git_object(spec: str, repo_root: Path) -> str:
    return subprocess.check_output(
        ["git", "rev-parse", spec], cwd=repo_root, text=True
    ).strip()


def validate_declared_bindings(
    receipt: dict[str, Any], authentication: dict[str, Any], repo_root: Path
) -> None:
    cache_binding = receipt["cache_binding"]
    require(
        cache_binding["authentication_status"] == "AUTHENTICATED",
        "cache authentication status mismatch",
    )
    require(
        cache_binding["inventory_digest"] == INVENTORY_DIGEST,
        "inventory digest mismatch",
    )
    require(authentication["status"] == "AUTHENTICATED", "authentication receipt status mismatch")
    authenticated_source = next(
        item for item in authentication["snapshot_files"] if item["source"] == SOURCE
    )
    require(authenticated_source["commit"] == COMMIT, "authenticated source commit mismatch")
    require(
        authenticated_source["inventory_digest"] == INVENTORY_DIGEST,
        "authenticated inventory digest mismatch",
    )
    require(
        authenticated_source["snapshot_sha256"] == CACHE_SNAPSHOT_SHA256,
        "authenticated snapshot digest mismatch",
    )
    require(authenticated_source["snapshot_sha256_match"] is True, "snapshot digest match not true")
    require(authenticated_source["verify_snapshot"] == "PASS", "snapshot verification not PASS")

    source_binding = receipt["source_binding"]
    require(source_binding["git_blob_sha"] == GIT_BLOB_SHA, "git blob sha mismatch")
    require(source_binding["retrieval_status"] == "RETRIEVED", "retrieval status mismatch")

    integration = receipt["integration_binding"]
    require(
        integration["A_before_worker_integration"] == A_BEFORE_INTEGRATION,
        "A before integration mismatch",
    )
    require(
        integration["A_after_worker_integration"] == A_AFTER_WORKER_INTEGRATION,
        "A after worker integration mismatch",
    )
    require(
        integration["exclusive_root_tree_identity"] == EXCLUSIVE_ROOT_IDENTITY,
        "exclusive root identity mismatch",
    )
    require(
        git_object(A_BEFORE_INTEGRATION, repo_root) == A_BEFORE_INTEGRATION,
        "A before integration object unavailable",
    )
    require(
        git_object(A_AFTER_WORKER_INTEGRATION, repo_root) == A_AFTER_WORKER_INTEGRATION,
        "A after worker integration object unavailable",
    )
    ancestor = subprocess.run(
        ["git", "merge-base", "--is-ancestor", A_AFTER_WORKER_INTEGRATION, "HEAD"],
        cwd=repo_root,
        check=False,
    )
    require(ancestor.returncode == 0, "A after worker integration is not an ancestor of HEAD")

    for role, (worker_head, root) in WORKER_ROOTS.items():
        require(integration["worker_heads"][role] == worker_head, f"worker {role} head mismatch")
        require(
            git_object(f"{worker_head}:{root}", repo_root)
            == git_object(f"HEAD:{root}", repo_root),
            f"worker {role} exclusive root identity mismatch",
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cache-snapshot", required=True, type=Path)
    args = parser.parse_args()

    script_path = Path(__file__).resolve()
    repo_root = script_path.parents[3]
    receipt_path = script_path.parent / "source-byte-reread-CORRECTION-01.json"
    receipt = load_json(receipt_path)
    require(
        sha256(args.cache_snapshot.read_bytes()) == CACHE_SNAPSHOT_SHA256,
        "cache snapshot digest mismatch",
    )
    source_row = load_source_row(args.cache_snapshot)

    cache_binding = receipt["cache_binding"]
    require(cache_binding["snapshot_sha256"] == CACHE_SNAPSHOT_SHA256, "receipt snapshot digest mismatch")
    authentication = load_json(repo_root / cache_binding["authentication_receipt"])
    validate_declared_bindings(receipt, authentication, repo_root)

    content_bytes = source_row["content"].encode("utf-8")
    require(source_row["commit"] == COMMIT, "source row commit mismatch")
    require(source_row["sha256"] == CONTENT_SHA256, "source row content digest mismatch")
    require(source_row["git_blob_sha"] == GIT_BLOB_SHA, "source row git blob sha mismatch")
    require(source_row["retrieval_status"] == "RETRIEVED", "source row retrieval status mismatch")
    require(source_row["size"] == len(content_bytes), "source row byte size mismatch")
    require(sha256(content_bytes) == CONTENT_SHA256, "source content digest mismatch")

    binding = receipt["source_binding"]
    require(binding["source"] == SOURCE, "source binding source mismatch")
    require(binding["commit"] == COMMIT, "source binding commit mismatch")
    require(binding["path"] == SOURCE_PATH, "source binding path mismatch")
    require(binding["content_sha256"] == CONTENT_SHA256, "source binding content digest mismatch")
    require(binding["size_bytes"] == len(content_bytes), "source binding byte size mismatch")

    lines = content_bytes.splitlines(keepends=True)
    findings = {item["claim_id"]: item for item in receipt["claim_rereads"]}
    require(set(findings) == set(CLAIM_LINES), "claim reread set mismatch")

    for claim_id, line_number in CLAIM_LINES.items():
        finding = findings[claim_id]
        exact_line = lines[line_number - 1]
        correction_path = (
            repo_root
            / "evidence/wave-20261009-correction-01/source"
            / f"{claim_id}-CORRECTION-01.json"
        )
        correction = load_json(correction_path)
        successor = correction["correction"]["corrected_statement"]

        require(finding["line_number"] == line_number, f"{claim_id} line number mismatch")
        require(finding["line_utf8_hex"] == exact_line.hex(), f"{claim_id} line bytes mismatch")
        require(finding["line_sha256"] == sha256(exact_line), f"{claim_id} line digest mismatch")
        require(
            finding["line_text"] == exact_line.decode("utf-8").rstrip("\n"),
            f"{claim_id} line text mismatch",
        )
        require(
            finding["successor_record"] == str(correction_path.relative_to(repo_root)),
            f"{claim_id} successor record mismatch",
        )
        require(finding["successor_statement"] == successor, f"{claim_id} successor statement mismatch")
        require(
            finding["successor_statement_sha256"] == sha256(successor.encode("utf-8")),
            f"{claim_id} successor statement digest mismatch",
        )
        require(
            finding["fidelity_result"] == "MATCH_WITH_RETAINED_QUALIFICATIONS",
            f"{claim_id} fidelity result mismatch",
        )
        require(
            finding["clears_only"] == "SOURCE_BYTES_NOT_REREAD_HERE",
            f"{claim_id} cleared-hold boundary mismatch",
        )

    boundaries = receipt["boundaries"]
    require(boundaries["delivery_status"] == "Staged", "delivery status mismatch")
    require(boundaries["reconciliation_receipt_created"] is False, "reconciliation receipt boundary changed")
    require(boundaries["policy_or_mapping_changed"] is False, "policy or mapping boundary changed")
    require(
        boundaries["rights_or_publication_clearance_granted"] is False,
        "rights or publication boundary changed",
    )
    require(boundaries["human_approval_granted"] is False, "human approval boundary changed")
    require(boundaries["heavy_verification_run"] is False, "heavy verification boundary changed")
    require(
        receipt["status"] == "SOURCE_BYTES_REREAD_MATCH_CORRECTION_SCOPE",
        "receipt status mismatch",
    )

    print("PASS: authenticated pinned source bytes and five correction spans match receipt")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
