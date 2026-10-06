# GHQR and community source scope

The owner approved merging the Well-Architected split and requested these four
sources next. PR #481 merged at `28587d052265fd2061c526846dbf05ff172bcb06` with the
same tree as its reviewed branch. This routing builds on that merged main state.

| Source | Inventory | Primary synthesis files | Existing artifact receipts | Existing authored text claims |
|---|---:|---:|---:|---:|
| [microsoft/ghqr](../evidence/semantics/source-scope/microsoft__ghqr.json) | 172 | 39 | 172 | 749 |
| [tmcw/github-best-practices](../evidence/semantics/source-scope/tmcw__github-best-practices.json) | 1 | 1 | 1 | 36 |
| [jlcanovas/gh-best-practices-template](../evidence/semantics/source-scope/jlcanovas__gh-best-practices-template.json) | 13 | 12 | 13 | 90 |
| [atapas/model-repo](../evidence/semantics/source-scope/atapas__model-repo.json) | 8 | 7 | 8 | 96 |
| **Total** | **194** | **59** | **194** | **971** |

Every file is retained with its exact artifact identity, pinned source commit,
content digest, role and existing evidence references. Each routing file includes
role definitions and a digest-bound evidence-file index. Files outside the primary
queue remain available for interpretation and synthesis; no acceptance denominator
is reduced and no existing claim is erased.

## GHQR: implemented assessment behavior is substantive

GHQR differs from a documentation-site repository. Its actual evaluator code is
an authority for what the tool checks. Code cannot be excluded wholesale.

| Role | Files | Treatment |
|---|---:|---|
| Assessment guidance | 7 | Purpose, usage, findings, recommendations and manual-check limitations. |
| Check definitions | 19 | All 129 source rule IDs across repository, organization, enterprise and GHES scopes. |
| Evaluator implementation | 13 | Actual best-practice predicates and common finding/result logic. |
| Assessment dependencies | 64 | Collectors, callers, authentication, registry, CLI/MCP, replay and renderers; trace them with each relevant evaluator. |
| Contract tests | 19 | Retain expected behavior and boundary cases with the implementation. |
| Synthetic fixtures | 4 | Keep mock-data limitations; synthetic entities are not live enforcement evidence. |
| Interpretation dependencies | 8 | Dependency manifests and site include/configuration inputs. |
| Context references | 21 | Contribution practices, installation, navigation and outbound references. |
| Tool/site infrastructure | 16 | Build/distribution/install support and branding; use existing dispositions and revisit when a concrete dependency requires it. |
| Rights metadata | 1 | Source license, without a redistribution grant. |
| **Total** | **172** | **All retained.** |

The 39 primary files contain 320 of the 749 existing authored text claims. The
remaining 429 claims are retained in supporting roles. Those roles can contain
important operational limitations: a smaller starting queue does not remove
the need to trace data collection, caller composition, missing permissions,
replay compaction or report omission. The 129 structured rule occurrences
remain unmapped in the existing ledger; definitions alone do not prove evaluator
coverage, successful target behavior or policy adoption.

Start consolidation from a rule definition and its actual predicate, then trace
the caller, data collector, registry enablement and reported result. Compare manual
guidance separately. Preserve what the code implements, what the source recommends,
what cannot be observed, and any local policy decision as separate facts. Read
upstream code as data; no setup, install, scan, mock or deployment command was run.

For example, `internal/scanners/bestpractices/branch_protection.go` has zero direct
authored text claims indexed under its own path, but the existing
`ghqr-branch-protection-claims.json` includes its three scanner observations and
limits alongside 14 YAML rule claims. The routing explicitly retains that linked
review. Zero path-local claims does not mean that the scanner was unreviewed or
contains no substantive behavior. Its caller-composition audit remains open.

## Community sources: reuse completed source review

The three community repositories contain 22 files together. Their advice,
contribution/governance templates, issue/PR templates, citation and funding examples
are the source's purpose. All 20 non-license files remain primary synthesis inputs;
the two license artifacts remain rights inputs. There is little infrastructure
to remove and no defensible broad reduction of this content.

These exact 22 artifacts already have the merged B0/C0 primary and independent
source reviews. The existing reviewed overlay contains **227 propositions and
227 source classifications**, including **four conflicting propositions retained**
for downstream decisions. This is one shared total across the three sources,
not 227 per repository. It is separate from their 222 legacy authored text claims.
Use the reviewed propositions and classifications rather than re-extracting or
re-reviewing the original files. Source classifications do not adopt controls.

The reviewed batch retains source-internal licensing and star-request tensions.
Example identities, deadlines, thresholds, commands, technologies, support accounts
and governance rules remain contextual until deliberately adapted and adopted.
The tmcw snapshot has no license artifact; its one-file inventory is not permission
to redistribute the source expression. This routing supplies no rights clearance.

## Accounting boundary

This change adds **zero artifact reviews, zero claim reviews, zero reconciled
claims and zero adopted controls**. All 194 existing receipts and 971 text claims
are reused. Exact per-file reference checks establish routing integrity, not the
truth or completeness of the underlying semantic reviews. The six-source
inventory remains 13,657; this routing closes no acceptance gate.

The [independent routing review](../evidence/semantics/source-scope/routing-review.md)
passed for all 194 entries and the role/evidence/accounting boundaries. Repository
checks passed, including 485 tests and unchanged prior bounded-review accounting.
