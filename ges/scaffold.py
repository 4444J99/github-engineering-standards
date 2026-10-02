"""Build a purpose-specific local repository scaffold from reviewed-draft controls.

The scaffold is a construction aid. It does not create a Git repository, call the
GitHub API, adopt policy, assess compliance, or activate native enforcement.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from . import __version__
from .core import applicable, digest, safe_path
from .render import render_template_content

SPEC_SCHEMA = "ges.repository-spec.v1"
ARTIFACT_SCHEMA = "ges.artifact-catalog.v1"
LOCK_SCHEMA = "ges.standard-lock.v1"
MANIFEST_SCHEMA = "ges.generation-manifest.v1"
INCOMPLETE_MARKER = ".ges-scaffold-incomplete"
RECORD_PATHS = {
    INCOMPLETE_MARKER,
    ".ges/repository-spec.json",
    ".ges/standard.lock.json",
    ".ges/standards-checklist.md",
    ".ges/generation-manifest.json",
}
GENERATOR_SOURCE_PATHS = (
    "ges/__init__.py",
    "ges/__main__.py",
    "ges/core.py",
    "ges/render.py",
    "ges/scaffold.py",
    "ges/yamlutil.py",
    "requirements.txt",
)
REQUIRED_UNSUPPORTED_CAPABILITIES = frozenset(
    {
        "license-selection",
        "ignore-rules",
        "continuous-integration",
        "build-and-package",
        "native-github-settings",
    }
)
DERIVED_PARAMETERS = {"PROJECT_TITLE", "PURPOSE"}
SLUG = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
PARAMETER = re.compile(r"[A-Z][A-Z0-9_]*")


@dataclass(frozen=True)
class ScaffoldPlan:
    files: dict[str, str]
    manifest: dict[str, Any]


def _json_text(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def _sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _nonempty_string(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip() or "\x00" in value:
        raise ValueError(f"{field} must be a non-empty string")
    return value


def _string_list(value: Any, field: str, *, required: bool = False) -> list[str]:
    if not isinstance(value, list) or (required and not value):
        raise ValueError(
            f"{field} must be a list" + (" with at least one item" if required else "")
        )
    for index, item in enumerate(value):
        _nonempty_string(item, f"{field}[{index}]")
    return value


def _exact_keys(value: dict, required: set[str], field: str) -> None:
    missing = required - value.keys()
    unknown = value.keys() - required
    if missing:
        raise ValueError(f"{field} missing fields: " + ", ".join(sorted(missing)))
    if unknown:
        raise ValueError(f"{field} has unknown fields: " + ", ".join(sorted(unknown)))


def validate_spec(spec: Any) -> None:
    if not isinstance(spec, dict):
        raise TypeError("Repository spec must be an object")
    _exact_keys(
        spec,
        {
            "schema_version",
            "repository",
            "proposed_github_metadata",
            "purpose",
            "standard",
            "template_parameters",
        },
        "Repository spec",
    )
    if spec["schema_version"] != SPEC_SCHEMA:
        raise ValueError("Unsupported repository spec schema")

    repository = spec["repository"]
    if not isinstance(repository, dict):
        raise TypeError("repository must be an object")
    _exact_keys(
        repository,
        {"name", "title", "owner", "visibility", "default_branch"},
        "repository",
    )
    name = _nonempty_string(repository["name"], "repository.name")
    if len(name) > 100 or not SLUG.fullmatch(name):
        raise ValueError("repository.name must be a lowercase hyphenated slug")
    _nonempty_string(repository["title"], "repository.title")
    _nonempty_string(repository["owner"], "repository.owner")
    if repository["visibility"] not in {"private", "public", "internal"}:
        raise ValueError("repository.visibility must be private, public, or internal")
    _nonempty_string(repository["default_branch"], "repository.default_branch")

    metadata = spec["proposed_github_metadata"]
    if not isinstance(metadata, dict):
        raise TypeError("proposed_github_metadata must be an object")
    _exact_keys(metadata, {"description", "topics"}, "proposed_github_metadata")
    description = _nonempty_string(
        metadata["description"], "proposed_github_metadata.description"
    )
    if len(description) > 350:
        raise ValueError("proposed_github_metadata.description exceeds 350 characters")
    topics = _string_list(
        metadata["topics"], "proposed_github_metadata.topics", required=True
    )
    if len(topics) > 20 or any(not SLUG.fullmatch(topic) for topic in topics):
        raise ValueError(
            "proposed_github_metadata.topics must contain at most 20 lowercase hyphenated topics"
        )

    purpose = spec["purpose"]
    if not isinstance(purpose, dict):
        raise TypeError("purpose must be an object")
    purpose_fields = {
        "statement",
        "function",
        "repository_type",
        "lifecycle_stage",
        "criticality",
        "deliverables",
        "in_scope",
        "out_of_scope",
        "interfaces",
        "toolchain",
    }
    _exact_keys(purpose, purpose_fields, "purpose")
    for field in (
        "statement",
        "function",
        "repository_type",
        "lifecycle_stage",
        "criticality",
    ):
        _nonempty_string(purpose[field], f"purpose.{field}")
    for field in ("deliverables", "in_scope"):
        _string_list(purpose[field], f"purpose.{field}", required=True)
    for field in ("out_of_scope", "interfaces", "toolchain"):
        _string_list(purpose[field], f"purpose.{field}")

    standard = spec["standard"]
    if not isinstance(standard, dict):
        raise TypeError("standard must be an object")
    _exact_keys(standard, {"profile", "materialization_mode"}, "standard")
    profile_name = _nonempty_string(standard["profile"], "standard.profile")
    if not SLUG.fullmatch(profile_name):
        raise ValueError("standard.profile must be a lowercase hyphenated name")
    if standard["materialization_mode"] != "review_candidate":
        raise ValueError("standard.materialization_mode must be review_candidate")

    parameters = spec["template_parameters"]
    if not isinstance(parameters, dict):
        raise TypeError("template_parameters must be an object")
    reserved = DERIVED_PARAMETERS & parameters.keys()
    if reserved:
        raise ValueError(
            "Derived template parameters must not be supplied: "
            + ", ".join(sorted(reserved))
        )
    for key, value in parameters.items():
        if not isinstance(key, str) or not PARAMETER.fullmatch(key):
            raise ValueError("Invalid template parameter name: " + repr(key))
        _nonempty_string(value, "template_parameters." + key)


def validate_profile(profile: Any, controls: list[dict]) -> None:
    if not isinstance(profile, dict):
        raise TypeError("Profile must be an object")
    for field in ("name", "policy_status", "context"):
        if field not in profile:
            raise ValueError("Profile missing field: " + field)
    _nonempty_string(profile["name"], "profile.name")
    if not SLUG.fullmatch(profile["name"]):
        raise ValueError("profile.name must be a lowercase hyphenated name")
    if profile["policy_status"] != "DRAFT_REQUIRES_TARGET_ADOPTION":
        raise ValueError(
            "profile.policy_status must be DRAFT_REQUIRES_TARGET_ADOPTION in this release"
        )
    if not isinstance(profile["context"], dict):
        raise TypeError("profile.context must be an object")
    expected_types: dict[str, set[type]] = {}
    numeric_parameters: set[str] = set()
    for control in controls:
        for key, expected in control.get("applicability", {}).items():
            values = expected if isinstance(expected, list) else [expected]
            expected_types.setdefault(key, set()).update(
                type(value) for value in values
            )
        verification = control.get("verification", {})
        parameter = verification.get("profile_parameter")
        if parameter and verification.get("operator") == "at_least":
            numeric_parameters.add(parameter)
    for key, types in expected_types.items():
        if key not in profile["context"]:
            continue
        actual = profile["context"][key]
        if type(actual) not in types:
            names = ", ".join(sorted(item.__name__ for item in types))
            raise ValueError(f"profile.context.{key} must have type {names}")
    for key in numeric_parameters:
        if key not in profile["context"]:
            raise ValueError(f"profile.context missing required parameter: {key}")
        value = profile["context"][key]
        if type(value) is not int or value < 0:
            raise ValueError(f"profile.context.{key} must be a non-negative integer")


def _validate_destination(value: Any) -> str:
    value = _nonempty_string(value, "artifact.destination")
    if "\\" in value or value.startswith("/") or "//" in value:
        raise ValueError("Unsafe artifact destination: " + value)
    parts = value.split("/")
    if any(part in {"", ".", ".."} for part in parts):
        raise ValueError("Unsafe artifact destination: " + value)
    folded_parts = [part.casefold() for part in parts]
    if ".git" in folded_parts or folded_parts[0] == ".ges":
        raise ValueError("Unsafe artifact destination: " + value)
    if value.casefold() in {path.casefold() for path in RECORD_PATHS}:
        raise ValueError("Artifact destination is reserved: " + value)
    return value


def validate_artifact_catalog(
    root: Path, controls: list[dict], artifact_catalog: Any
) -> None:
    if not isinstance(artifact_catalog, dict):
        raise TypeError("Artifact catalog must be an object")
    _exact_keys(
        artifact_catalog,
        {"schema_version", "name", "revision", "artifacts", "unsupported"},
        "Artifact catalog",
    )
    if artifact_catalog["schema_version"] != ARTIFACT_SCHEMA:
        raise ValueError("Unsupported artifact catalog schema")
    _nonempty_string(artifact_catalog["name"], "artifact_catalog.name")
    if (
        type(artifact_catalog["revision"]) is not int
        or artifact_catalog["revision"] < 1
    ):
        raise ValueError("artifact_catalog.revision must be a positive integer")
    if not isinstance(artifact_catalog["artifacts"], list):
        raise TypeError("artifact_catalog.artifacts must be a list")
    if not isinstance(artifact_catalog["unsupported"], list):
        raise TypeError("artifact_catalog.unsupported must be a list")

    by_id = {control["id"]: control for control in controls}
    file_controls = {
        control["id"]
        for control in controls
        if control.get("verification", {}).get("kind") == "file_present"
    }
    seen_ids: set[str] = set()
    seen_controls: set[str] = set()
    seen_destinations: set[str] = set()
    for index, artifact in enumerate(artifact_catalog["artifacts"]):
        if not isinstance(artifact, dict):
            raise TypeError(f"artifact_catalog.artifacts[{index}] must be an object")
        _exact_keys(
            artifact,
            {"id", "class", "control_id", "control_revision", "destination"},
            f"artifact_catalog.artifacts[{index}]",
        )
        artifact_id = _nonempty_string(
            artifact["id"], f"artifact_catalog.artifacts[{index}].id"
        )
        if not SLUG.fullmatch(artifact_id):
            raise ValueError("Invalid artifact id: " + artifact_id)
        if artifact_id in seen_ids:
            raise ValueError("Duplicate artifact id: " + artifact_id)
        seen_ids.add(artifact_id)
        if artifact["class"] != "consumer_file":
            raise ValueError("Unsupported artifact class: " + str(artifact["class"]))
        control_id = _nonempty_string(
            artifact["control_id"], f"artifact_catalog.artifacts[{index}].control_id"
        )
        if control_id in seen_controls:
            raise ValueError("Duplicate selection control: " + control_id)
        seen_controls.add(control_id)
        control = by_id.get(control_id)
        if control is None:
            raise ValueError("Unknown artifact control: " + control_id)
        if artifact["control_revision"] != control["revision"]:
            raise ValueError(
                f"Stale artifact control revision: {control_id} expected {control['revision']}"
            )
        if control.get("verification", {}).get("kind") != "file_present":
            raise ValueError("Artifact control is not file_present: " + control_id)
        if control.get("status") not in {"REVIEWED_DRAFT", "ACCEPTED"}:
            raise ValueError(
                f"Artifact control is not eligible for materialization: {control_id} ({control.get('status')})"
            )
        template = control.get("implementation", {}).get("template")
        if not template or not safe_path(root, template).is_file():
            raise ValueError("Artifact control has no valid template: " + control_id)
        destination = _validate_destination(artifact["destination"])
        if destination not in control["verification"]["paths"]:
            raise ValueError(
                f"{destination} is not an accepted destination for {control_id}"
            )
        folded = destination.casefold()
        if folded in seen_destinations:
            raise ValueError("Duplicate artifact destination: " + destination)
        if any(
            folded.startswith(existing + "/") or existing.startswith(folded + "/")
            for existing in seen_destinations
        ):
            raise ValueError(
                "Artifact destination collides with another path: " + destination
            )
        seen_destinations.add(folded)
    missing = file_controls - seen_controls
    extra = seen_controls - file_controls
    if missing:
        raise ValueError(
            "Artifact catalog missing file controls: " + ", ".join(sorted(missing))
        )
    if extra:
        raise ValueError(
            "Artifact catalog has non-file controls: " + ", ".join(sorted(extra))
        )

    unsupported_ids: set[str] = set()
    for index, item in enumerate(artifact_catalog["unsupported"]):
        if not isinstance(item, dict):
            raise TypeError(f"artifact_catalog.unsupported[{index}] must be an object")
        _exact_keys(item, {"id", "reason"}, f"artifact_catalog.unsupported[{index}]")
        item_id = _nonempty_string(
            item["id"], f"artifact_catalog.unsupported[{index}].id"
        )
        _nonempty_string(
            item["reason"], f"artifact_catalog.unsupported[{index}].reason"
        )
        if item_id in unsupported_ids:
            raise ValueError("Duplicate unsupported capability: " + item_id)
        unsupported_ids.add(item_id)
    missing_unsupported = REQUIRED_UNSUPPORTED_CAPABILITIES - unsupported_ids
    if missing_unsupported:
        raise ValueError(
            "Artifact catalog missing required unsupported capabilities: "
            + ", ".join(sorted(missing_unsupported))
        )


def _control_decisions(controls: list[dict], context: dict) -> list[dict]:
    decisions = []
    unknown = []
    for control in controls:
        state, reason = applicable(control, context)
        record = {
            "id": control["id"],
            "revision": control["revision"],
            "title": control["title"],
            "obligation": control["obligation"],
            "status": control["status"],
            "applicability": state,
            "reason": reason,
            "verification_kind": control["verification"]["kind"],
        }
        decisions.append(record)
        if state == "UNKNOWN":
            unknown.append(f"{control['id']}: {reason}")
    if unknown:
        raise ValueError(
            "Profile leaves applicability UNKNOWN for " + "; ".join(unknown)
        )
    return decisions


def _standards_checklist(
    controls: list[dict], decisions: list[dict], profile: dict, catalog_digest: str
) -> str:
    decision_by_id = {item["id"]: item for item in decisions}
    lines = [
        "# Project-specific engineering standards checklist",
        "",
        f"Profile: `{profile['name']}` (`{profile['policy_status']}`)",
        f"Canonical catalog digest: `{catalog_digest}`",
        "",
        "This is a planning checklist generated from applicable controls. A checked box is not, by itself,",
        "evidence of compliance, policy adoption, semantic review, or native enforcement.",
        "",
    ]
    applicable_controls = [
        control
        for control in controls
        if decision_by_id[control["id"]]["applicability"] == "APPLICABLE"
    ]
    for category in sorted({control["category"] for control in applicable_controls}):
        lines += ["## " + category.replace("-", " ").title(), ""]
        for control in applicable_controls:
            if control["category"] != category:
                continue
            lines += [
                (
                    f"- [ ] **{control['id']} r{control['revision']} — {control['title']}** "
                    f"({control['obligation']}; {control['status']})"
                ),
                "  " + control["objective"],
                "  Acceptance: " + "; ".join(control["implementation"]["acceptance"]),
                "  Verification: `" + control["verification"]["kind"] + "`.",
                "",
            ]
    return "\n".join(lines).rstrip() + "\n"


def plan_scaffold(
    root: Path, controls: list[dict], spec: dict, profile: dict, artifact_catalog: dict
) -> ScaffoldPlan:
    validate_spec(spec)
    validate_profile(profile, controls)
    if spec["standard"]["profile"] != profile["name"]:
        raise ValueError(
            f"Repository spec requires profile {spec['standard']['profile']}; "
            f"received {profile['name']}"
        )
    validate_artifact_catalog(root, controls, artifact_catalog)
    decisions = _control_decisions(controls, profile["context"])
    decision_by_id = {item["id"]: item for item in decisions}
    control_by_id = {control["id"]: control for control in controls}
    parameters = dict(spec["template_parameters"])
    parameters.update(
        {
            "PROJECT_TITLE": spec["repository"]["title"],
            "PURPOSE": spec["purpose"]["statement"],
        }
    )

    files: dict[str, str] = {}
    materialized = []
    omitted = []
    for artifact in artifact_catalog["artifacts"]:
        control = control_by_id[artifact["control_id"]]
        decision = decision_by_id[control["id"]]
        template = control["implementation"]["template"]
        related = [
            item
            for item in decisions
            if control_by_id[item["id"]].get("implementation", {}).get("template")
            == template
        ]
        base = {
            "artifact_id": artifact["id"],
            "class": artifact["class"],
            "destination": artifact["destination"],
            "template": template,
            "selection_control": {
                "id": control["id"],
                "revision": control["revision"],
                "status": control["status"],
                "applicability": decision["applicability"],
                "reason": decision["reason"],
            },
            "related_controls": [
                {
                    "id": item["id"],
                    "revision": item["revision"],
                    "status": item["status"],
                    "applicability": item["applicability"],
                }
                for item in related
            ],
        }
        if decision["applicability"] == "APPLICABLE":
            template_source = safe_path(root, template).read_bytes()
            rendered = render_template_content(
                template, template_source.decode("utf-8"), parameters
            )
            files[artifact["destination"]] = rendered
            materialized.append(
                {
                    **base,
                    "template_sha256": hashlib.sha256(template_source).hexdigest(),
                    "output_sha256": _sha256_text(rendered),
                }
            )
        else:
            omitted.append(base)

    for omitted_artifact in omitted:
        omitted_name = Path(omitted_artifact["destination"]).name
        references = [
            path
            for path, text in files.items()
            if omitted_name.casefold() in text.casefold()
        ]
        if references:
            raise ValueError(
                f"Rendered output references omitted artifact {omitted_artifact['destination']}: "
                + ", ".join(sorted(references))
            )

    catalog_digest = digest(controls)
    spec_text = _json_text(spec)
    checklist = _standards_checklist(controls, decisions, profile, catalog_digest)
    generator_sources = [
        {
            "path": path,
            "sha256": hashlib.sha256(safe_path(root, path).read_bytes()).hexdigest(),
        }
        for path in GENERATOR_SOURCE_PATHS
    ]
    standard_lock = {
        "schema_version": LOCK_SCHEMA,
        "generator": {
            "name": "github-engineering-standards",
            "version": __version__,
            "sources": generator_sources,
            "sources_sha256": digest(generator_sources),
        },
        "catalog": {"sha256": catalog_digest, "control_count": len(controls)},
        "profile": {
            "name": profile["name"],
            "policy_status": profile["policy_status"],
            "sha256": digest(profile),
        },
        "artifact_catalog": {
            "name": artifact_catalog["name"],
            "revision": artifact_catalog["revision"],
            "sha256": digest(artifact_catalog),
        },
        "repository_spec_sha256": digest(spec),
    }
    lock_text = _json_text(standard_lock)
    files[".ges/repository-spec.json"] = spec_text
    files[".ges/standard.lock.json"] = lock_text
    files[".ges/standards-checklist.md"] = checklist

    outputs = [
        {"path": path, "sha256": _sha256_text(text)}
        for path, text in sorted(files.items())
    ]
    manifest = {
        "schema_version": MANIFEST_SCHEMA,
        "repository": spec["repository"],
        "proposed_github_metadata": spec["proposed_github_metadata"],
        "standard_lock_sha256": _sha256_text(lock_text),
        "controls": decisions,
        "artifacts": {"materialized": materialized, "omitted": omitted},
        "unsupported": artifact_catalog["unsupported"],
        "outputs": outputs,
        "status_boundary": {
            "policy_adoption": "NOT_RECORDED",
            "compliance": "NOT_ASSESSED",
            "semantic_review": "NOT_ESTABLISHED",
            "native_changes_applied": False,
            "git_repository_initialized": False,
            "remote_repository_created": False,
        },
    }
    files[".ges/generation-manifest.json"] = _json_text(manifest)
    return ScaffoldPlan(files=files, manifest=manifest)


def write_scaffold(plan: ScaffoldPlan, output: Path) -> None:
    output = Path(output)
    if os.path.lexists(output):
        raise FileExistsError("Refusing to overwrite " + str(output))
    output.parent.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix="." + output.name + ".", dir=output.parent))
    output_created = False
    try:
        for relative, text in sorted(plan.files.items()):
            destination = safe_path(stage, relative)
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(text, encoding="utf-8")
        try:
            output.mkdir()
        except FileExistsError as exc:
            raise FileExistsError("Refusing to overwrite " + str(output)) from exc
        output_created = True
        (output / INCOMPLETE_MARKER).write_text(
            "Repository scaffold publication is incomplete; do not treat this tree as generated evidence.\n",
            encoding="utf-8",
        )
        staged_items = sorted(
            stage.iterdir(),
            key=lambda item: (item.name == ".ges", item.name.casefold()),
        )
        for staged_item in staged_items:
            staged_item.rename(output / staged_item.name)
        (output / INCOMPLETE_MARKER).unlink()
        stage.rmdir()
    except BaseException:
        if stage.exists():
            shutil.rmtree(stage)
        if output_created and output.exists():
            shutil.rmtree(output)
        raise
