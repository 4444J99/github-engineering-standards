# GitHub Engineering Standards

A source-traceable standards toolkit for defining, inspecting, implementing and governing collaborative engineering systems on GitHub.

**Version 0.1.0 is a working toolkit and reviewed-draft control catalog, not a claim of exhaustive semantic consolidation or estate-wide compliance.**

## What exists

95 canonical draft controls; 22 parameterized templates; six applicability profiles; a read-only repository collector; deterministic configuration checks; scoped human-review attestations; time-bounded exceptions; blocking assessment gates; source ingestion, candidate extraction, structured requirement import, source/page ledgers, crosswalk generation and change-impact analysis.

The initial acquisition contains all six pinned source archives: 13,657 artifact entries, 3,742 documentation source Markdown files, and 18,015 published English page-version entries. The extraction ledger contains 150,903 candidate blocks and 605 explicitly structured source checklist requirements. These figures describe acquisition and extraction, **not completion of semantic review**.

## Source set

| Source | Responsibility in the corpus |
|---|---|
| `github/docs` | Platform capabilities, constraints, procedures, reusable content, generated-data inputs and version applicability. |
| `github/github-well-architected` | Architecture, security, governance, collaboration, productivity and assessment practices. |
| `microsoft/ghqr` | Source-defined checks, scanner implementations, manual checks and evaluator limitations. |
| `tmcw/github-best-practices` | Context-dependent collaboration and change-management recommendations. |
| `jlcanovas/gh-best-practices-template` | Repository governance, documentation and community templates. |
| `atapas/model-repo` | Contribution, presentation, onboarding and engagement conventions. |

Exact commits and artifact digests are in `sources/sources.lock.json` and the acquisition receipts. See `docs/source-rights.md` before redistributing upstream material.

## Run from a source checkout

Python 3.11 or newer is required. The supported interface is `python -m ges` from this repository root; a standalone installed wheel is not provided.

```sh
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python -m ges validate
python -m ges compile
```

### Inspect a repository without changing it

Supply `GH_TOKEN` through your authorized secret store or runner environment when permissioned observations are needed. The collector only calls read APIs. It never changes settings, creates issues, or pushes commits.

```sh
python -m ges collect --repository OWNER/REPOSITORY --output .cache/snapshot.json
python -m ges audit --snapshot .cache/snapshot.json --profile profiles/solo-software.json --output .cache/assessment.json
python -m ges gate --report .cache/assessment.json
```

The profile must be reviewed for the actual target. Missing dimensions remain unknown; private or inaccessible settings are not assumed disabled or passing. The gate returns exit code 1 for mandatory unmet requirements. `--require-accepted` additionally blocks draft controls. `--allow-exceptions` permits approved exceptions only for observed FAIL/PARTIAL results; it never hides missing observations or unknown applicability.

### Rebuild the complete source accounting

```sh
python -m ges sync --output .cache/sources
python -m ges corpus --snapshots .cache/sources --output .cache/corpus
python -m ges ledger --snapshots .cache/sources --corpus .cache/corpus
```

The sync command downloads the six exact source snapshots and published English page lists. `--rendered` additionally retrieves all published article bodies; `--rendered-limit N` is an explicitly partial bounded run. Acquisition is read-only. Raw text is a private, ignored cache, not material to copy blindly into a public repository.

`source-acquisition.yml` produces inspectable artifacts without committing upstream material or accepting extracted policy. It has no recurring schedule.

### Render a template

```sh
python -m ges render --template templates/README.md --parameters parameters.json --output .cache/rendered/README.md
```

All required parameters must be supplied. Existing output files are not overwritten. JSON and YAML outputs are syntax-checked; project-specific truth, schema requirements and operational suitability require separate verification.

### Trace changes

```sh
python -m ges impact --old old/artifacts.jsonl --new new/artifacts.jsonl --output .cache/impact.json
```

Changes reopen directly referenced controls. Add `--dependencies old/dependencies.jsonl`
to conservatively reopen controls through resolved include/variable dependencies.
Unresolved dependencies and conditional/version rendering remain explicit review work.

## Where to look

`controls/catalog.json` is the canonical authored control definition. `generated/functional-checklist.md`, `source-crosswalk.md` and `bindings.json` are generated from it. `templates/` contains implementation starting points; `profiles/` contains explicitly draft target policies. `ges/` owns acquisition, assessment and compilation behavior. `tests/` exercises false-pass prevention and deterministic outputs. `docs/` records architecture, limitations, decisions and acceptance criteria. `evidence/` records executed work, not aspirations.

The large source corpus and page-level review queues are workflow artifacts and a separate downloadable evidence bundle; they are not duplicated into every consumer repository.

## What is not finished

Full semantic page/file review; semantic deduplication of every source claim; rendered-content/version assurance; per-file licensing clearance; all upstream scanner predicates implemented as local deterministic checks; all platform feature/plan adapters; live human-review and exception services; native protection activation and cross-estate rollout. `docs/remaining-work.md` defines the open acceptance gates.

The recovery suite passes 199 local tests; this does not imply 95 controls implemented
as automatic checks or 150,903 candidates reviewed. Current catalog controls remain
`REVIEWED_DRAFT`; 593 non-adopted generated proposals are preserved separately in
`controls/review_queue.json`. No native policy is silently activated. See
[recovery delivery](docs/recovery-delivery.md) and `evidence/recovery-status.json`.

## Contributions and governance

See CONTRIBUTING.md, GOVERNANCE.md, AGENTS.md and SECURITY.md. The repository is initially private. No additional license is assigned to upstream material or to a public distribution through this bootstrap.
