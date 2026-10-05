# GitHub Systems Standard — Implementation Contract

Version: 0.1  
Date: 2026-10-01  
Status: Implementation contract; NOT a completed six-source extraction or deployed enforcement system.

## 1. Objective

Combine all six source corpora into one provenance-preserving collection, consolidate overlapping requirements, generalize their reusable intent, and operationalize the result as scripts, checklists, templates, enforcement policies, and measurable evidence.

The deliverable is an executable systems standard, not six independent summaries. A single logical standard does not require merging upstream Git histories or consolidating the user's function-owned product repositories into a monorepo.

## 2. Source boundary

All six sources receive full inventory and explicit disposition, rather than selective README-level coverage:

1. `github/docs`, the source repository for the supplied `docs.github.com/en` documentation entry point.
2. `github/github-well-architected`.
3. `microsoft/ghqr`.
4. `tmcw/github-best-practices`.
5. `jlcanovas/gh-best-practices-template`.
6. `atapas/model-repo`.

Inventory all files in pinned source snapshots, including documentation, reusable fragments, templates, configuration, implementation code, tests, and supporting assets. Inventory is not the same as mandatory inclusion in the final standard. Every artifact receives a recorded disposition: control source, reference, template, implementation, test, supporting asset, duplicate, superseded, or excluded with reason.

For GitHub Docs, preserve page metadata, shared content dependencies, conditional content, and product/platform/version distinctions. Reconcile source files with published/generated page coverage. Declare the version and language scope; do not claim coverage of every published page from a raw repository file count alone. Follow source-linked material necessary to interpret requirements; record other outbound references without implying the entire linked web has been ingested.

## 3. Transformation pipeline

### Merge

Preserve each source's identity, snapshot commit, path, content digest, retrieved-at time, attribution, and licensing information. Combine the corpora without flattening their provenance or claiming that all material shares a common license. Record any restrictions or unresolved reuse questions before redistribution.

### Consolidate

Extract atomic claims with source sections or line spans and their actual normative language. Map each claim to a canonical control, specialization, reference, conflict, superseded item, or justified exclusion. Many claims can support one control; a single paragraph can produce multiple controls.

A repeated instruction is not several independent obligations. A contradictory instruction must not disappear through deduplication. Retain the conflicting claims and record the decision, scope, rationale, and reviewer.

### Generalize

Separate reusable intent from source-specific names, technologies, hosting assumptions, reviewers, contact details, numerical thresholds, product versions, and placeholder values. Parameterize these values through explicit profiles.

Keep source authority and adopted policy distinct. Official platform documentation governs claims about platform behavior; community recommendations inform policy without becoming platform requirements. A local policy may strengthen a recommendation, but must identify that as a deliberate local decision.

Profile dimensions include entity type, repository function, lifecycle stage, visibility, deployment model, platform/version, available features, language/toolchain, risk, and maintainer capacity. Feature unavailability is not automatically proof that a security objective is inapplicable.

### Operationalize

Every accepted control has one authoritative machine-readable definition. Generate or validate its checklists, templates, script bindings, enforcement policies, and reports from that definition. Do not maintain disconnected prose, script, and policy versions of the same rule.

Each control specifies applicability, implementation, verification, evidence, remediation, enforcement, metrics, and exception handling. A control may reference shared scripts or templates; it does not require a new repository or script file of its own.

Not all requirements can be automatically implemented or semantically verified. In those cases, bind the control to a structured review procedure, accountable reviewer, evidence record, review deadline, and gate. Automating the review workflow is not evidence that the underlying judgment is correct.

## 4. Required operational representations

| Representation | Required content |
|---|---|
| Canonical control | Stable ID, revision, precise objective, source mappings, adopted obligation, scope, applicability, parameters, dependencies, acceptance criteria. |
| Script binding | Read-only inspection; optional safe remediation; explicit required permissions, prerequisites, error handling, and capability limits. |
| Checklist item | Function-based question or instruction, acceptance criteria, evidence fields, and links to the canonical control and source items. |
| Template/configuration | Parameterized file, policy, form, configuration, runbook, or evidence form; omit inapplicable deployment artifacts with an explicit reason. |
| Enforcement | Native setting, CI gate, deployment gate, periodic drift check, or governed human review; include bypass and recovery design. |
| Measurement | Defined unit and denominator, evidence freshness, observed result, evaluation time, standard revision, owner, and remediation age. |
| Remediation | Resolution guidance; safe automation where justified; reviewed change proposal otherwise; post-change verification and rollback where applicable. |

All representations carry the same control ID and revision so a requirement can be traced from its source to its observed result.

## 5. Safety and authority

Importing a source does not authorize installing its dependencies, executing its code, granting permissions, or deploying every feature it describes. A page explaining deletion, for example, supplies conditional lifecycle safeguards rather than a universal instruction to delete repositories.

Read-only assessment is the default execution mode. Proposed changes must display a diff and affected entities. Writes require appropriate authorization, least-privilege credentials, precondition checks, bounded concurrency, idempotent behavior where applicable, post-change verification, and rollback or recovery instructions. Do not self-authorize bypasses or silently lower requirements to obtain a passing result.

Template material is data until intentionally reviewed for execution. Remove source-specific accounts, contacts, example links, and placeholders from deployable output; preserve necessary attribution separately. Do not redistribute unlicensed or otherwise restricted source expression as though it were permissively licensed.

## 6. Assessment model

Keep applicability, observed outcome, exception status, and enforcement capability separate.

- Applicability: `APPLICABLE`, `NOT_APPLICABLE_WITH_REASON`, `UNKNOWN`.
- Evaluation: `PASS`, `FAIL`, `PARTIAL`, `NOT_ASSESSED`, `MANUAL_REVIEW`, `NOT_VERIFIABLE`, `ERROR`, `STALE`.
- Exception: `NONE`, `APPROVED_UNTIL`, `EXPIRED`.
- Enforcement capability: `AUTOMATED`, `HUMAN_GATE`, `DETECT_ONLY`, `UNAVAILABLE`.

`PASS` requires evidence satisfying the acceptance criteria at the required freshness and scope. Missing permissions, unavailable API fields, absent runs, expired evidence, and scanner failures never become passing results. An approved exception does not rewrite the observed outcome.

Use control instances as the unit of repository assessment: a canonical control applied to a specific target entity and context. Organization-level evidence may support inherited controls, but inherited enforcement and actual target coverage must be verified.

## 7. Measurements

Report construction completeness separately from target compliance.

| Metric | Definition |
|---|---|
| Inventory retrieval | Retrieved artifacts / artifacts in the complete pinned inventory; disclose unresolved generated-page scope separately. |
| Semantic review coverage | Artifacts with completed semantic review and disposition / inventoried artifacts. |
| Claim reconciliation coverage | Reviewed actionable claims with a resolved mapping / reviewed actionable claims identified. |
| Control implementation coverage | Accepted controls with implemented and tested required bindings / accepted controls. |
| Assessment coverage | Applicable control instances with current valid evaluations / known-applicable control instances. |
| Verified pass rate | Applicable control instances with fresh passing evidence / known-applicable control instances. |
| Unknown applicability | Count and share of expected control instances with unresolved applicability; never silently exclude from reporting. |
| Enforcement coverage | Applicable control instances with verified effective enforcement / known-applicable control instances. |
| Operational health | Drift count and age, remediation latency, recurring failures, scan errors, stale evidence, exception count and age. |

Always display numerators, denominators, snapshot/version, and evaluation time. A zero denominator is `not applicable` or `undefined`, not 100%. Mapping every detected candidate does not prove every actionable statement was detected; semantic review and source-to-control audits are separate completion gates. Avoid a single score that conceals failures in critical controls.

## 8. Generated views

Produce four mutually traceable views:

1. Source view: every page/file, extracted claims, disposition, and mapped control IDs.
2. Function view: deduplicated implementation checklist organized by system capability.
3. Target view: applicable controls and actual evidence for an account, organization, repository, branch, workflow, release, or environment.
4. Change view: upstream source changes and the controls, templates, scripts, profiles, and targets potentially affected.

Repository architecture, community operations, security, CI/CD, release operations, access, recovery, research citation, agent workflows, and other domains must be populated from the actual source inventory rather than assumed to be exhausted by an initial category list.

## 9. Change management

Pin source snapshots and standard releases. New or modified upstream artifacts reopen the relevant review mappings. Removing an upstream passage does not automatically delete a local policy. Re-evaluate conflicts, feature availability, affected templates, and test fixtures before promoting a changed standard.

Consumers declare a standard version and applicability profile. Central policy changes roll out through reviewed changes or authorized reconciliation, not unbounded silent overwrites. Preserve local exceptions with owner, rationale, compensating controls, and expiry.

## 10. Acceptance gates

The six-source consolidation is not complete until:

- Every artifact in the declared corpus is inventoried, reviewed, and dispositioned, including any page-generation and shared-fragment gaps.
- Every identified actionable claim is mapped; source-to-control audits substantiate extraction completeness.
- Conflicts and reuse restrictions are resolved or explicitly blocked.
- Every accepted control has a reviewed definition and all required operational bindings.
- Tests cover valid, invalid, missing-data, permission-denied, stale-evidence, and not-applicable cases.
- Scripts, checklists, templates, and enforcement policies agree on the same control definitions.
- Target assessments provide reproducible evidence, explicit unknowns, and truthful coverage figures.
- Enforcement is tested at the intended scope; critical behavior is not inferred from configuration-file existence alone.

## 11. Status boundary for this delivery

This file records the implementation contract. It does not assert that the full source corpus has been imported, all controls have been extracted, executable bindings have been built, or repository changes have been applied. Earlier selective source reads are evidence for design decisions, not a completed exhaustive consolidation.

## 12. Source references used to establish this contract

- GitHub Docs: https://github.com/github/docs (README identifies content and data and its licensing distinction).
- GitHub Well-Architected: https://github.com/github/github-well-architected
- GHQR pinned branch-protection definitions: https://github.com/microsoft/ghqr/blob/02b89961921ac43f93aa8b3ff74cdcb7cd3d9244/internal/recommendations/definitions/repository/branch_protection.yaml
- GHQR manual-check limitations: https://github.com/microsoft/ghqr/blob/02b89961921ac43f93aa8b3ff74cdcb7cd3d9244/.github/skills/ghqr-report/references/MANUAL_CHECKS.md
- tmcw practices: https://github.com/tmcw/github-best-practices/blob/801411757531a8880cb315148160fde3079d7227/README.md
- Governance template: https://github.com/jlcanovas/gh-best-practices-template/blob/bf13cd2c7992876da01de065084e8af3e9c7db06/GOVERNANCE.md
- Model repository: https://github.com/atapas/model-repo/blob/9aa52517830a0e10043116ff768af8fabeeb4347/README.md

References are source locations, not an assertion that all linked content has been reviewed in this delivery.
