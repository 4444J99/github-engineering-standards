# Open acceptance gates

These are remaining work, not completed features or background jobs.

| Gate | Evidence needed to close |
|---|---|
| Exhaustive artifact accounting | Complete Git tree/archive comparison, explicit disposition of export-ignored files, symlinks, submodules and supporting assets. |
| Published content assurance | Retrieved rendered bodies for every in-scope language/version page, generated API reference reconciliation, redirects and conditional/include rendering verified. |
| Semantic extraction | Every actionable statement and material caveat accounted for at page/file/section level; reviewed zero-control dispositions where justified. |
| Consolidation | Every source claim mapped to a canonical control, specialization, conflict decision, preserved reference or reasoned exclusion; independent omission review. |
| Generalization | Technology, owner, threshold, plan, platform, lifecycle, human staffing and optional/destructive operation assumptions explicit; unique intent preserved. |
| Operational completeness | Every accepted control has executable checks or accountable manual review, implementation templates/procedures, remediation and evidence contracts. Missing API adapters remain visible. |
| Native enforcement | Safe test-repository proof, approved target profiles, effective policy readback, negative/positive behavior tests, rollback and bypass review. |
| Rights and publication | Per-file notices, attribution and redistribution decisions; no unsupported relicensing or implied upstream endorsement. |
| Estate rollout | Explicit inventory of in-scope targets, pilot outcomes, owner-approved rollout batches, evidence freshness, exceptions and drift reconciliation. |

The review queue in the corpus ledger is the authoritative remaining-item inventory. Referencing a source file from a draft control does not close review of that entire file. The current 95 controls do not subsume all 605 structured requirements or 150,903 candidate blocks.

## Reporting boundary

Construction reporting now distinguishes observed incomplete coverage from
unverified prerequisites. Every gate lists `incomplete_conditions` and
`unverified_conditions`; its state is calculated instead of universally assigned
OPEN. Zero or undeclared denominators cannot pass. Pinned tree matching and
durable-body acquisition are observed checks, not semantic certification.

Source-fidelity/omission and exact-claim reconciliation now have fail-closed,
digest-bound receipt validators. In the absence of separately authorized
receipts, their required inputs remain explicitly unknown. Structured-occurrence
reconciliation, generalization, adoption, binding, native-enforcement, and estate
adapters remain unfinished; rights and published-content adapters retain their
narrower documented scopes.
The reporter does not invent failed audits or permit a boolean sidecar to close
any gate. Gate evaluation is not itself source review or native verification.
See the individual conditions in `evidence/recovery-status.json` for the actual
outstanding work.
