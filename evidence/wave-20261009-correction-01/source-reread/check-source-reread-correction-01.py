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
        raise AssertionError(f"expected one pinned source row, found {len(matches)}")
    return matches[0]


def git_object(spec: str, repo_root: Path) -> str:
    return subprocess.check_output(
        ["git", "rev-parse", spec], cwd=repo_root, text=True
    ).strip()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cache-snapshot", required=True, type=Path)
    args = parser.parse_args()

    script_path = Path(__file__).resolve()
    repo_root = script_path.parents[3]
    receipt_path = script_path.parent / "source-byte-reread-CORRECTION-01.json"
    receipt = load_json(receipt_path)
    assert sha256(args.cache_snapshot.read_bytes()) == CACHE_SNAPSHOT_SHA256
    source_row = load_source_row(args.cache_snapshot)

    cache_binding = receipt["cache_binding"]
    assert cache_binding["snapshot_sha256"] == CACHE_SNAPSHOT_SHA256
    authentication = load_json(repo_root / cache_binding["authentication_receipt"])
    assert authentication["status"] == "AUTHENTICATED"
    authenticated_source = next(
        item for item in authentication["snapshot_files"] if item["source"] == SOURCE
    )
    assert authenticated_source["commit"] == COMMIT
    assert authenticated_source["snapshot_sha256"] == CACHE_SNAPSHOT_SHA256
    assert authenticated_source["snapshot_sha256_match"] is True
    assert authenticated_source["verify_snapshot"] == "PASS"

    integration = receipt["integration_binding"]
    for role, (worker_head, root) in WORKER_ROOTS.items():
        assert integration["worker_heads"][role] == worker_head
        assert git_object(f"{worker_head}:{root}", repo_root) == git_object(
            f"HEAD:{root}", repo_root
        )

    content_bytes = source_row["content"].encode("utf-8")
    assert source_row["commit"] == COMMIT
    assert source_row["sha256"] == CONTENT_SHA256
    assert source_row["size"] == len(content_bytes)
    assert sha256(content_bytes) == CONTENT_SHA256

    binding = receipt["source_binding"]
    assert binding["source"] == SOURCE
    assert binding["commit"] == COMMIT
    assert binding["path"] == SOURCE_PATH
    assert binding["content_sha256"] == CONTENT_SHA256
    assert binding["size_bytes"] == len(content_bytes)

    lines = content_bytes.splitlines(keepends=True)
    findings = {item["claim_id"]: item for item in receipt["claim_rereads"]}
    assert set(findings) == set(CLAIM_LINES)

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

        assert finding["line_number"] == line_number
        assert finding["line_utf8_hex"] == exact_line.hex()
        assert finding["line_sha256"] == sha256(exact_line)
        assert finding["line_text"] == exact_line.decode("utf-8").rstrip("\n")
        assert finding["successor_record"] == str(correction_path.relative_to(repo_root))
        assert finding["successor_statement"] == successor
        assert finding["successor_statement_sha256"] == sha256(successor.encode("utf-8"))
        assert finding["fidelity_result"] == "MATCH_WITH_RETAINED_QUALIFICATIONS"
        assert finding["clears_only"] == "SOURCE_BYTES_NOT_REREAD_HERE"

    boundaries = receipt["boundaries"]
    assert boundaries["delivery_status"] == "Staged"
    assert boundaries["reconciliation_receipt_created"] is False
    assert boundaries["policy_or_mapping_changed"] is False
    assert boundaries["rights_or_publication_clearance_granted"] is False
    assert boundaries["human_approval_granted"] is False
    assert boundaries["heavy_verification_run"] is False
    assert receipt["status"] == "SOURCE_BYTES_REREAD_MATCH_CORRECTION_SCOPE"

    print("PASS: authenticated pinned source bytes and five correction spans match receipt")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
