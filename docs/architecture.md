# Architecture and ownership

## Logical pipeline

Pinned source archives + published page inventories -> artifact ledger -> candidate and structured-source claims -> reviewed normalization decisions -> canonical controls -> compiled checklists/templates/checker bindings -> scoped target assessment -> approved enforcement -> evidence and change impact.

The current implementation owns one cohesive function: reusable engineering standards. It is not a merge of the user's product repositories. Applications consume versioned controls and configuration through explicit references. Credential custody stays in CLAVIS; this repository is a consumer of scoped read access, not a secret issuer.

## Distinct data objects

A source artifact is pinned by repository, commit, path and digest. A candidate identifies exact source lines but is not necessarily normative or atomic. A structured source requirement preserves an upstream definition without adopting its severity as policy. A canonical control has its own stable ID and revision. A profile supplies explicit applicability and policy parameters. An observation identifies target, exact revision, collection time and transport limitations. A human attestation has authorized reviewer, expiry, rationale and evidence. An exception preserves the observed result and adds an approved time-limited risk decision.

## Execution boundaries

Source acquisition never executes downloaded code. YAML parsing uses a safe loader and rejects duplicate keys. Source archives are never extracted to arbitrary filesystem paths. Template rendering rejects missing parameters, escape paths and overwrites; structured output is parsed before writing. The GitHub collector performs only GET requests. Audit and gate consume explicit JSON records. Actual API configuration mutations are not implemented in this release.

## Scope of deterministic checks

The implemented checker families are metadata presence, repository naming, accepted-location file presence, workflow root permissions, immutable action references and effective branch-rule presence/parameters. Manual review is a seventh binding kind. A rule observation establishes only returned active rule state; bypass behavior, legacy equivalence and end-to-end rejection need separate review. File presence is not document quality. SHA syntax is not provenance validation.

## Scale

Large candidate ledgers and raw material are cache/workflow artifacts. Small lockfiles, source receipts, canonical definitions and generated function views stay versioned. No repository is created per control, per source, or per checklist item.
