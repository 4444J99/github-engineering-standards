# TEST_INFRA — End-to-End Test Suite Infrastructure & Architecture

## 1. Test Philosophy: Opaque-Box & Requirement-Driven

The testing infrastructure of `github-engineering-standards` (`ges`) follows a strict **opaque-box, requirement-driven methodology**.

### 1.1 Opaque-Box Execution
- **Interface Confinement**: Tests interact with `ges` exclusively through standard command-line interfaces (`python -m ges <command> <args>`), published file contracts (`controls/catalog.json`, `profiles/*.json`, `templates/*`), and structured JSON snapshots/reports.
- **No White-Box Monkeypatching**: The test runner never patches internal functions, swaps private variables, or alters evaluator control flow. Components execute in their authentic runtime environment.
- **Process & Filesystem Isolation**: CLI commands run via isolated processes (`subprocess.run`) or clean top-level CLI entrypoints, validating true exit codes, standard streams (`stdout`/`stderr`), disk persistence, and file permissions.

### 1.2 Requirement-Driven Expected Output Derivation
Every test case in the suite directly traces to authoritative requirements specified in `ORIGINAL_REQUEST.md` (R1–R4) and the project master document `PROJECT.md` (Features 1–30):
- **Explicit Authoritative Oracles**: Expected outputs are derived mathematically from specification contracts (e.g. SHA-256 catalog digests, exact JSON schema structures `ges.assessment.v1`, RFC 3339 timestamp validations, and boolean evaluation gates).
- **Integrity Over Convenience**: Tests never adapt to incorrect behavior. Evaluator rules must strictly return `ERROR` or `FAIL` on missing/empty payloads, never a vacuous `PASS`.
- **Adversarial Integrity**: In accordance with the project guidelines, edge cases exercise control-character injections, directory traversal attempts (`../`), symlink de-referencing hazards, unpinned dependencies, and timestamp manipulations.

---

## 2. Feature Inventory & Coverage Mapping

The test infrastructure covers the full lifecycle of standards definition, compilation, evaluation, and remediation:

| Component / Subcommand | Specification Source | Test Tier | Primary Verification Objectives |
|------------------------|----------------------|-----------|--------------------------------|
| `ges validate` | ORIGINAL_REQUEST §R3, PROJECT #26 | Tier 1, 2 | Catalog schema validation, control IDs, unpinned source detection, duplicate ID rejection |
| `ges compile` | ORIGINAL_REQUEST §R3, PROJECT #23 | Tier 1, 3 | Generation of `functional-checklist.md`, `source-crosswalk.md`, `bindings.json`, digest tracking |
| `ges audit` (evaluate) | ORIGINAL_REQUEST §R3, PROJECT #26 | Tier 1, 2, 3, 4 | Multi-evaluator assessment, snapshot processing, profile binding, schema `ges.assessment.v1` |
| `ges gate` | ORIGINAL_REQUEST §R1, PROJECT #1 | Tier 1, 2, 3 | Release gate compliance, blocker reporting, `--require-accepted`, `--allow-exceptions` |
| `ges render` | ORIGINAL_REQUEST §R3, PROJECT #26 | Tier 1, 2, 3, 4 | Parameterized template compilation (JSON, YAML, Markdown), read-only safety (no overwrite) |
| `ges impact` | ORIGINAL_REQUEST §R3, PROJECT #23 | Tier 1, 2 | Upstream change detection and control reopening triggers |
| Profiles (`solo-software`, `team-service`) | ORIGINAL_REQUEST §R3, PROJECT #24 | Tier 1, 3 | Parameterization of thresholds (`required_reviews`: 0 vs 2), solo-maintainer deadlock prevention |
| Snapshot Contracts | ORIGINAL_REQUEST §R1, PROJECT #14 | Tier 2, 4 | Typed payload enforcement (rejection of `{}`/`None` as pass), timestamp freshness (`FRESH`, `STALE`, `FUTURE`) |
| Read-Only Remediation Safety | ORIGINAL_REQUEST §R3, PROJECT #26 | Tier 4 | Non-destructive dry-run, remediation plan/diff generation without uncontrolled remote writes |

---

## 3. Four-Tier Test Suite Architecture

The end-to-end test suite in `tests/test_e2e_suite.py` is partitioned into four progressive tiers:

```
+-------------------------------------------------------------------------+
|                  TIER 4: REAL-WORLD SCENARIOS                           |
|  - Full Estate Assessment Snapshot                                      |
|  - Remediation Plan & Diff Generation (Read-Only Safety)                |
|  - Multi-Check End-to-End Compliance Pipeline                          |
+-------------------------------------------------------------------------+
                                    ▲
+-------------------------------------------------------------------------+
|              TIER 3: CROSS-FEATURE INTERACTIONS                         |
|  - Profile Overrides (Solo-Maintainer vs Strict Team Service)           |
|  - Ruleset Compilation & Remediation Template Generation                |
|  - Exception Lifecycle without Outcome Rewriting                        |
+-------------------------------------------------------------------------+
                                    ▲
+-------------------------------------------------------------------------+
|              TIER 2: BOUNDARY & CORNER CASES                            |
|  - Empty & Truncated Snapshots (No Vacuous Passes)                      |
|  - Corrupted YAML/JSON & Encoding Injections                            |
|  - Missing Files, Symlink Hazards & Path Traversal Rejection            |
|  - Stale / Future / Missing Timestamp Boundaries                        |
+-------------------------------------------------------------------------+
                                    ▲
+-------------------------------------------------------------------------+
|                  TIER 1: FEATURE COVERAGE                               |
|  - CLI Happy-Path: validate, compile, audit, gate, render, impact       |
|  - Canonical Catalog Loading & Standards Digest Verification            |
|  - Profile Context Resolution & Output Schema Compliance                |
+-------------------------------------------------------------------------+
```

### Tier 1: Feature Coverage (Happy-Path)
Validates core command-line subcommands with valid inputs under nominal operating conditions.
- `test_tier1_validate_canonical_catalog`: CLI `ges validate` succeeds on canonical catalog with exit code 0 and valid control count.
- `test_tier1_compile_artifacts`: CLI `ges compile` writes `bindings.json`, `functional-checklist.md`, and `source-crosswalk.md` with verifiable cryptographic digests.
- `test_tier1_audit_execution`: CLI `ges audit` processes a valid repository snapshot against `profiles/solo-software.json`, generating valid `ges.assessment.v1` output.
- `test_tier1_gate_nominal_pass`: CLI `ges gate` approves an audit report with zero failing MUST controls.
- `test_tier1_render_template`: CLI `ges render` compiles Markdown, YAML, and JSON templates with valid parameters.
- `test_tier1_impact_detection`: CLI `ges impact` reports unchanged state when inventory hashes match.

### Tier 2: Boundary & Corner Cases
Exercises adversarial and edge inputs, verifying system resilience and absence of false assurances.
- `test_tier2_empty_snapshot_rejected`: An empty snapshot `{}` fails with error outcomes, never silent passes.
- `test_tier2_missing_target_or_revision`: Snapshots missing `target` or `target_revision` fail audit with descriptive error messages.
- `test_tier2_timestamp_freshness_boundaries`: Validates `FRESH`, `STALE` (> 24h), `FUTURE` (< -60s), and invalid timezone rejections.
- `test_tier2_corrupted_workflow_yaml`: Syntax errors and duplicate keys in GitHub Actions workflow YAML trigger `FAIL`/`ERROR`.
- `test_tier2_unpinned_actions_and_docker_images`: Workflows referencing floating tags (`@v4`, `@latest`) fail pinning evaluators.
- `test_tier2_path_traversal_rejection`: Unsafe relative paths (`../`, absolute paths) are rejected by template and safe path validators.
- `test_tier2_symlink_not_dereferenced`: Symlinks in file inventories result in `MANUAL_REVIEW`, preventing symlink confusion.
- `test_tier2_deploy_keys_write_access`: Deploy keys with `read_only: false` or unverified status trigger immediate failure.

### Tier 3: Cross-Feature Interactions
Tests integration between disparate modules, context overrides, and policy hierarchies.
- `test_tier3_solo_vs_team_review_profiles`: Compares `solo-software.json` (`required_reviews: 0`) against `team-service.json` (`required_reviews: 2`) on the identical branch protection rule; solo succeeds, team fails, preventing self-approval deadlocks while enforcing multi-party review when required.
- `test_tier3_exception_preserves_outcome_integrity`: An approved exception marks `exception_status: "APPROVED_UNTIL"` but strictly preserves `outcome: "FAIL"`, ensuring exceptions never falsify audit ledgers.
- `test_tier3_gate_with_and_without_allow_exceptions`: Validates that failing controls with valid exceptions are blocked by default and unblocked only with explicit `--allow-exceptions`.
- `test_tier3_ruleset_template_compilation`: Compiles `templates/ruleset.json` with dynamic branch rules and verifies valid JSON structure ready for native API dispatch.

### Tier 4: Real-World Scenarios
Simulates production estate workflows, end-to-end repository audits, and safe remediation.
- `test_tier4_complete_repo_assessment_lifecycle`: Full pipeline: synthetic comprehensive repository snapshot -> `ges audit` -> summary verification -> `ges gate` evaluation.
- `test_tier4_remediation_plan_and_diff_generation`: Simulates detecting compliance gaps (e.g., missing Dependabot configuration), generating remediation assets from templates, and computing unified diffs.
- `test_tier4_read_only_safety_guarantee`: Proves that remediation tools refuse to overwrite existing files on disk, ensuring zero destructive operations without explicit operator intervention.

---

## 4. Directory Layout

```
github-engineering-standards/
├── TEST_INFRA.md                   # This specification
├── TEST_READY.md                   # E2E test suite operational readiness certificate
├── controls/
│   ├── catalog.json                # 95 canonical reviewed-draft controls
│   └── review_queue.json           # Quarantined draft controls (pending individual review)
├── profiles/                       # Standard profiles (solo-software, team-service, etc.)
├── templates/                      # Parameterized templates (rulesets, workflows, docs)
├── ges/                            # Core executable standards framework
│   ├── __main__.py                 # CLI entrypoint
│   ├── checks.py                   # Control evaluators
│   ├── collect.py                  # Snapshot collector
│   ├── core.py                     # Data contracts, schema validation, safe pathing
│   ├── evaluate.py                 # Assessment and gating engine
│   └── render.py                   # Template engine and checklist generator
└── tests/
    ├── test_ges.py                 # Fast unit, contract, and evaluator tests
    └── test_e2e_suite.py           # 4-tier requirement-driven opaque-box E2E test suite
```

---

## 5. Invocation Commands & CI Integration

### 5.1 Running the Full E2E Test Suite
```bash
python -m unittest tests/test_e2e_suite.py -v
```

### 5.2 Running Individual Test Tiers
```bash
# Tier 1: Feature Coverage (CLI subcommands)
python -m unittest tests.test_e2e_suite.Tier1FeatureCoverage -v

# Tier 2: Boundary & Corner Cases
python -m unittest tests.test_e2e_suite.Tier2BoundaryCornerCases -v

# Tier 3: Cross-Feature Interactions
python -m unittest tests.test_e2e_suite.Tier3CrossFeatureInteractions -v

# Tier 4: Real-World Scenarios
python -m unittest tests.test_e2e_suite.Tier4RealWorldScenarios -v
```

### 5.3 Complete Project Test Discovery
```bash
python -m unittest discover -s tests -v
```

---

## 6. Pass/Fail Criteria & Quality Contracts

1. **Zero Flakiness**: All tests must execute deterministically without network dependencies or sleep calls.
2. **Strict Exit Codes**:
   - `0`: Successful execution / gate pass.
   - `1`: Gate failure (policy blocker detected).
   - `2`: Invalid CLI arguments, schema validation error, or corrupt input data.
3. **Write scope**: GitHub collection is read-only. Local commands write designated
   outputs; only template rendering explicitly refuses overwrites. Local fixture tests
   establish those tested behaviors, not estate-wide safety or effective enforcement.
