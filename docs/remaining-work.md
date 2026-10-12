# Open acceptance gates

These are remaining work, not completed features or background jobs.

## Completion milestones

The fixed first synthesis boundary is the six pinned original repositories.
GitHub Docs supplies authoritative GitHub platform language and behavior;
source authority remains separate from owner-adopted policy. Later external
standards and internal implementation ancestors enter after the accepted GES
baseline, as separate provenance layers for Engineering Environment Standards.

| Milestone | Required evidence | Release boundary |
|---|---|---|
| Six-source synthesis | Artifact accounting, published content assurance, semantic extraction, consolidation, generalization, and operational completeness (gates 1–6 below). | Immutable semantic release candidate; every source proposition and GES output has an accountable disposition. |
| Public release clearance | Exact-use rights review of expression actually redistributed or adapted, required attribution, and approved distribution. | Only cleared expression enters public release artifacts. Reference-only source locators do not require blanket per-artifact publication grants. |
| Native pilot acceptance | Approved public disposable target, effective policy readback, positive/negative behavior, bypass review, rollback, and unchanged second-run verification. | GES v0.2 requires synthesis, public release clearance, and this pilot. Private support remains unverified. |
| Estate rollout | Separately approved target inventory, rollout batches, freshness, exceptions, and drift reconciliation. | Independent follow-on program; not a GES synthesis or release blocker. |

The 2026-10-06 private attempt remains historical and unverified; see its
[pilot observation](private-native-pilot-result.md). The owner has since selected
the public `4444J99/ges-native-enforcement-pilot` target. Current runner/publisher
evidence, approved rule activation, partial negative behavior, restoration and
unchanged reapplication are recorded in the
[2026-10-10 continuation](../evidence/v02-finish-20261010/README.md).
The rule was returned to Disabled and main to its original baseline after tests.
Cancelled/skipped behavior and isolated deletion/bypass acceptance remain open;
neither this public evidence nor provisioning verifies private support.
The historical [branch pilot plan](native-branch-pilot-plan.md),
[operational procedure](branch-policy-operations.md), draft profile and payloads
are now concrete review inputs. Their publication does not activate policy.
Upstream contribution packets require current-upstream verification and individual
user approval before submission; upstream acceptance does not block GES release.
Broader EES requires separate source admission, ancestry reconciliation, ownership
decisions, composition, and existing/new repository pilots before its own release.

## Evidence gates

| # | Gate | Evidence needed to close |
|---|---|---|
| 1 | Exhaustive artifact accounting | Complete Git tree/archive comparison, explicit disposition of export-ignored files, symlinks, submodules and supporting assets. |
| 2 | Published content assurance | Retrieved rendered bodies for every in-scope language/version page, generated API reference reconciliation, redirects and conditional/include rendering verified. |
| 3 | Semantic extraction | Every actionable statement and material caveat accounted for at page/file/section level; reviewed zero-control dispositions where justified. |
| 4 | Consolidation | Every source claim mapped to a canonical control, specialization, conflict decision, preserved reference or reasoned exclusion; independent omission review. |
| 5 | Generalization | Technology, owner, threshold, plan, platform, lifecycle, human staffing and optional/destructive operation assumptions explicit; unique intent preserved. |
| 6 | Operational completeness | Every accepted control has executable checks or accountable manual review, implementation templates/procedures, remediation and evidence contracts. Missing API adapters remain visible. |
| 7 | Native enforcement | Safe test-repository proof, approved target profiles, effective policy readback, negative/positive behavior tests, rollback and bypass review. |
| 8 | Rights and publication | Review each actual redistributed or adapted expression, applicable notices, attribution, and distribution decision; no unsupported relicensing or implied upstream endorsement. |
| 9 | Estate rollout | Explicit inventory of in-scope targets, pilot outcomes, owner-approved rollout batches, evidence freshness, exceptions and drift reconciliation. |

### Scanner-predicate coverage remains open

Implementing all upstream scanner predicates as local deterministic checks remains
an explicit open gap within gate 6. Required evaluator bindings are related but
do not replace that inventory: each upstream predicate needs an identified local
implementation and tests, or an explicit reviewed disposition explaining a
limitation or alternative review procedure. No such complete coverage/disposition
ledger is claimed by this tranche. Missing predicates remain visible until that
ledger is reviewed; generic binding coverage cannot silently close this gap.

The review queue in the corpus ledger is the authoritative remaining-item inventory. Referencing a source file from a draft control does not close review of that entire file. The current 95 controls do not subsume all 605 structured requirements or 150,903 candidate blocks.

## Reporting boundary

`ges.recovery` now adds `milestone_accounting` with the four completion
milestones and a separate `ges_v0_2` aggregate requiring the first three.
The existing `project_complete` field retains its exact legacy meaning: all
nine legacy gates are closed. Estate rollout remains independently reported.
Every gate is preserved and its identity, conditions, counts and claimed state
are checked before milestone projection. Existing receipts retain their original
scope and timestamps. See [completion reporting](completion-milestones.md).

Gate 8 also retains legacy runtime semantics: `ges.recovery` still describes
per-file rights review, and `ges.rights_acceptance` computes
`per_file_rights_acceptance` over the entire artifact inventory. The exact-use
publication boundary uses a separate validated candidate output manifest,
actual-use register, scoped review receipts and approved authority policy.
The candidate directory's complete file set and exact bytes must match that
manifest. A bounded package cannot establish clearance of the full GES v0.2
release. Missing publication inputs leave this milestone `UNVERIFIED`; existing
per-file receipts cannot be silently reinterpreted as exact-use clearance.

Construction reporting now distinguishes observed incomplete coverage from
unverified prerequisites. Every gate lists `incomplete_conditions` and
`unverified_conditions`; its state is calculated instead of universally assigned
OPEN. Zero or undeclared legacy gate denominators cannot pass. Publication may
clear an explicitly reviewed zero-use register only for a nonempty exact output
set with the separately validated inventory, review and distribution approvals;
an empty register alone is insufficient. Pinned tree matching and
durable-body acquisition are observed checks, not semantic certification.

Source-fidelity/omission and exact-claim reconciliation now have fail-closed,
digest-bound receipt validators. In the absence of separately authorized
receipts, their required inputs remain explicitly unknown. The structured-occurrence
adapter is now implemented with focused adversarial tests, but no actual occurrences
have acquired new certified reconciliation through it. Generalization, adoption,
binding, native-enforcement, and estate adapters remain unfinished; rights and published-content adapters retain their
narrower documented scopes.
The reporter does not invent failed audits or permit a boolean sidecar to close
any gate. Gate evaluation is not itself source review or native verification.
See the individual conditions in `evidence/recovery-status.json` for the actual
outstanding work at that report's recorded timestamp. New milestone reporting
does not rewrite that historical receipt or claim that any acceptance gate has
closed. Calculated `PROVEN` evidence is not the governed designation `Verified`;
the merged-main, review and owner-acceptance requirements in `GOVERNANCE.md`
remain in force.

## Current staged checkpoint — October 12, 2026

The [cloud source replay in PR #506](../evidence/v02-cloud-replay-20261012/README.md)
authenticated all six locked sources and replayed provenance for 61,941 claims in
655 documents. Its independent audit and retained input hashes are recorded with
the execution. The earlier native host admission denials remain historical
observations; the completed cloud replay uses its own execution evidence.

The [authorized reconciliation in PR #507](../evidence/v02-authorized-reconciliation-20261012/README.md)
records the owner's exact current-role grant, actual issuance of 2,174 receipts,
distinct final-envelope review and successful source-bound accounting. The result
is **2,174 validated dispositions and 59,767 unresolved claims out of 61,941**,
with `mapping_complete=false`. Historical grants, receipts and the original
nonissued draft are preserved. Agent review does not supply human approval or
extend the recorded grant to adoption, publication, merge or release acceptance.

The subsequent [recovery integration](../evidence/v02-recovery-integration-20261012/README.md)
recovers the candidate and historical page ledgers, reconstructs the dependency
ledger and historical summary, and restores the structured requirements. All five
match independently recorded A3 byte hashes. With the preserved October 7 artifact
metadata and authenticated October 12 source files, the actual reporter now
succeeds and carries the authorized 2,174-receipt accounting into its gates and
milestones. The earlier failed attempt remains preserved; missing candidates are
no longer the current blocker. A required-input preflight now identifies missing
corpus/source files before expensive processing, preserving the existing trusted
Darwin path-alias policy.

The report contains 3,590 valid artifact disposition receipts out of 13,657;
10,067 artifacts remain without such receipts. It retains 150,903 candidate
blocks, 605 structured occurrences, 18,019 published page applications and the
original 14 unresolved source mappings. No new structured-occurrence certification,
control adoption or semantic-omission certification is claimed. The frozen summary
retains its historical 31 catalog-referenced artifacts; the current catalog's
reference count is independently 35.

Complete original capsule and historical rendered-body authentication, omission completeness, remaining
generalization/adoption/binding/native adapters, six-source synthesis and the full
public pilot matrix remain open. The approved JSON representation amendment is
implemented, but its two exact-expression rights decisions remain HOLD. The final
release candidate, publication clearance, human review, governed integration,
merged-main verification and owner acceptance remain pending.
