#!/usr/bin/env python3
"""Reconstruct five exact A3 corpus members from authenticated retained inputs.

Writes raw corpus bytes only into an explicitly supplied new private directory.
The generated metadata report does not claim restoration of the full capsule,
rendered bodies, historical inventories, or original artifacts.jsonl.
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import io
import json
from pathlib import Path
import subprocess
import tarfile
import zipfile


OLD_ZIP_SHA256 = "473d70ec984260549e3e736528ad6578b9216cb71b55c214c2ed6eb53849a1d0"
CURRENT_ZIP_SHA256 = "b5e8004f456c8f47afce497560a72ee90abb5ed226856875e4077ac1aa1fcc80"
CATALOG_COMMIT = "e848c9a4f0fb9499c957ad3185ee99061fd57f8d"
CATALOG_SHA256 = "27f7a05e5a848b956e3bb3b11e61af8eee1810917f4826358730efe5ac33166d"
EXPECTED = {
    "candidates.jsonl": (112346551, "1bd1c456fc141ad1afc02c0f4959f29d8835b224cf0196c411343dfd366ea6b6"),
    "published-page-ledger.json": (11700449, "df6a93828cba4cb3c3b98a4de5af47367e9924121be76f9c9a039dec7a4e5f19"),
    "dependencies.jsonl": (15766178, "1e084ea9e1a1949d880fa4d8792d0837170ff1cf4837a5946b9d5e34230cda72"),
    "ledger-summary.json": (508, "11835ac39c6aebd04a33c9cf94f95ceaa08fa305ebdf7e74583806d49357b7b6"),
    "structured-source-requirements.json": (616114, "24c542c98ce52613e009abb2820ddb694d1d2f6e986eaa8b1e8bb3b612f05f2e"),
}


def digest(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def get_members(path: Path, expected_hash: str, names: set[str]) -> dict[str, bytes]:
    payload = path.read_bytes()
    require(digest(payload) == expected_hash, "Workflow artifact ZIP digest mismatch")
    with zipfile.ZipFile(io.BytesIO(payload)) as archive:
        require(archive.namelist() == ["metadata-evidence.tar.gz"], "Unexpected ZIP membership")
        tar_bytes = archive.read("metadata-evidence.tar.gz")
    result = {}
    with tarfile.open(fileobj=io.BytesIO(tar_bytes), mode="r:gz") as archive:
        for member in archive.getmembers():
            if member.name in names:
                require(member.isfile() and member.name not in result, "Nonregular or duplicate member")
                result[member.name] = archive.extractfile(member).read()
    require(set(result) == names, "Missing requested archive member")
    return result


def rows(payload: bytes) -> list[dict]:
    require(payload.endswith(b"\n"), "JSONL missing final LF")
    return [json.loads(line) for line in payload[:-1].split(b"\n")]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--historical-zip", required=True, type=Path)
    parser.add_argument("--current-zip", required=True, type=Path)
    parser.add_argument("--repository", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    require(not args.output.exists(), "Output directory must not already exist")

    old_names = {"corpus/" + name for name in (
        "candidates.jsonl", "published-page-ledger.json", "dependencies.jsonl",
        "ledger-summary.json", "artifacts.jsonl")}
    old = get_members(args.historical_zip, OLD_ZIP_SHA256, old_names)
    current = get_members(args.current_zip, CURRENT_ZIP_SHA256,
                          {"corpus/structured-source-requirements.json"})
    catalog_bytes = subprocess.check_output([
        "git", "-C", str(args.repository), "show", CATALOG_COMMIT + ":controls/catalog.json"
    ])
    require(digest(catalog_bytes) == CATALOG_SHA256, "Historical catalog digest mismatch")
    catalog = json.loads(catalog_bytes)

    artifacts = rows(old["corpus/artifacts.jsonl"])
    require(len(artifacts) == 13657, "Historical workflow artifact inventory count mismatch")
    by_id = {r["artifact_id"]: r for r in artifacts}
    require(len(by_id) == len(artifacts), "Duplicate workflow artifact identity")
    dependency_lines = old["corpus/dependencies.jsonl"][:-1].split(b"\n")
    dependency_groups = collections.defaultdict(list)
    for line in dependency_lines:
        source = by_id[json.loads(line)["artifact_id"]]["source"]
        dependency_groups[source].append(line + b"\n")
    require({k: len(v) for k, v in dependency_groups.items()} == {
        "github/docs": 61800, "microsoft/ghqr": 1
    }, "Unexpected dependency source membership")
    dependencies = b"".join(line for source in ("github/docs", "microsoft/ghqr")
                            for line in dependency_groups[source])

    referenced_paths = {(s["repository"], s["path"]) for c in catalog for s in c["sources"]}
    referenced_artifacts = sum((a["source"], a["path"]) in referenced_paths for a in artifacts)
    require(referenced_artifacts == 31, "Historical canonical artifact-reference count mismatch")
    summary = json.loads(old["corpus/ledger-summary.json"])
    require(summary["source_artifacts_referenced_by_canonical_controls"] == 30,
            "Unexpected historical workflow reference count")
    summary["source_artifacts_referenced_by_canonical_controls"] = referenced_artifacts
    summary_bytes = (json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode()

    payloads = {
        "candidates.jsonl": old["corpus/candidates.jsonl"],
        "published-page-ledger.json": old["corpus/published-page-ledger.json"],
        "dependencies.jsonl": dependencies,
        "ledger-summary.json": summary_bytes,
        "structured-source-requirements.json": current["corpus/structured-source-requirements.json"],
    }
    for name, data in payloads.items():
        require((len(data), digest(data)) == EXPECTED[name], "A3 byte identity mismatch: " + name)
    pages = json.loads(payloads["published-page-ledger.json"])
    require(len(pages) == 18019 and sum(not p["source_matches"] for p in pages) == 14,
            "Historical page accounting mismatch")
    require(payloads["candidates.jsonl"].count(b"\n") == 150903, "Candidate count mismatch")
    require(len(json.loads(payloads["structured-source-requirements.json"])) == 605,
            "Structured occurrence count mismatch")

    origins = {
        "candidates.jsonl": "Unchanged member of October 1 authenticated workflow artifact",
        "published-page-ledger.json": "Unchanged member of October 1 authenticated workflow artifact",
        "dependencies.jsonl": "Reordered two intact source groups; no row bytes changed",
        "ledger-summary.json": "Historical summary with canonical reference count recomputed from exact A3 catalog",
        "structured-source-requirements.json": "Unchanged member of October 12 authenticated workflow artifact",
    }
    report = {
        "schema": "ges.historical-corpus-reconstruction.v1",
        "historical_artifact": {
            "repository": "4444J99/github-engineering-standards", "run_id": 36920555495,
            "artifact_id": 11191578546, "name": "standards-metadata-evidence",
            "head_sha": "2cbe5fd0022e59abfb66346b1f894a772d7412df", "zip_sha256": OLD_ZIP_SHA256,
            "created_at": "2026-10-01T20:19:28Z", "expires_at": "2026-10-31T20:19:27Z",
        },
        "current_artifact": {
            "repository": "4444J99/github-engineering-standards", "run_id": 38313171881,
            "artifact_id": 11775861352, "name": "standards-metadata-evidence",
            "head_sha": "8642b789f0ee8e4d9fdd40ef8497059cc95b5238", "zip_sha256": CURRENT_ZIP_SHA256,
            "created_at": "2026-10-12T21:52:17Z", "expires_at": "2026-11-11T21:52:15Z",
        },
        "catalog": {"commit": CATALOG_COMMIT, "path": "controls/catalog.json", "sha256": CATALOG_SHA256},
        "members": {name: {"bytes": len(data), "sha256": digest(data), "a3_identity_match": True,
                           "origin": origins[name]} for name, data in payloads.items()},
        "reconstruction_details": {
            "dependency_input_sha256": digest(old["corpus/dependencies.jsonl"]),
            "dependency_input_source_order": ["microsoft/ghqr", "github/docs"],
            "dependency_output_source_order": ["github/docs", "microsoft/ghqr"],
            "dependency_source_counts": {source: len(lines) for source, lines in dependency_groups.items()},
            "dependency_row_bytes_changed": False,
            "summary_input_sha256": digest(old["corpus/ledger-summary.json"]),
            "summary_changed_field": "source_artifacts_referenced_by_canonical_controls",
            "summary_prior_value": 30, "summary_historical_catalog_value": referenced_artifacts,
            "summary_other_values_changed": False,
            "workflow_artifacts_input_sha256": digest(old["corpus/artifacts.jsonl"]),
        },
        "accounting": {"artifacts_used_for_identity_lookup": 13657, "candidates": 150903,
                       "published_pages": 18019, "unresolved_page_source_mappings": 14,
                       "dependencies": 61801, "structured_occurrences": 605},
        "original_capsule_complete": False,
        "original_artifacts_jsonl_restored": False,
        "original_source_inventory_bytes_restored": False,
        "original_rendered_body_cache_restored": False,
        "semantic_review_performed": False,
        "limitations": [
            "The A3 capsule archive and its original artifacts.jsonl remain unavailable.",
            "Source inventory acquisition timestamps have not been invented or rewritten.",
            "Five exact member identities do not establish whole-capsule custody.",
            "No source review, adoption, publication clearance, pilot acceptance, or release acceptance is granted.",
        ],
    }
    args.output.mkdir(parents=True)
    for name, data in payloads.items():
        (args.output / name).write_bytes(data)
    report_path = args.output / "historical-reconstruction-report.json"
    report_path.write_text(json.dumps(report, sort_keys=True, indent=2) + "\n")
    print(json.dumps({"report": str(report_path), "exact_members": list(payloads),
                      "original_capsule_complete": False}))


if __name__ == "__main__":
    main()
