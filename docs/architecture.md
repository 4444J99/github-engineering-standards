# Architecture and ownership

## Logical pipeline

Pinned source archives + published page inventories -> artifact ledger -> candidate and structured-source claims -> reviewed normalization decisions -> canonical controls -> compiled checklists/templates/checker bindings -> scoped target assessment -> approved enforcement -> evidence and change impact.

The current implementation owns one cohesive function: reusable engineering standards. It is not a merge of the user's product repositories. Applications consume versioned controls and configuration through explicit references. Credential custody stays in CLAVIS; this repository is a consumer of scoped read access, not a secret issuer.

## Distinct data objects

A source artifact is pinned by repository, commit, path and digest. A candidate identifies exact source lines but is not necessarily normative or atomic. A structured source requirement preserves an upstream definition without adopting its severity as policy. A canonical control has its own stable ID and revision. A profile supplies explicit applicability and policy parameters. An observation identifies target, exact revision, collection time and transport limitations. A human attestation has authorized reviewer, expiry, rationale and evidence. An exception preserves the observed result and adds an approved time-limited risk decision.

The repository factory introduces five deliberately separate construction objects. A **repository spec** declares the intended consumer's identity, proposed metadata, purpose, required profile and template parameters. A **profile** supplies the draft target-policy context used to resolve control applicability; it remains independently reviewable and does not become adopted merely because it is selected. An **artifact catalog** maps supported file-presence controls and their exact revisions to template destinations while naming unsupported capabilities. A generated **standard lock** records the generator name/version and source-module digests and digest-pins the canonical catalog, selected profile, artifact catalog and repository spec. A generated **manifest** records applicability decisions, materialized and omitted artifacts, unsupported work, output digests and negative status assertions. The lock identifies inputs and generator implementation; the manifest records construction. Neither is an assessment, adoption decision, semantic-review receipt or enforcement receipt.

## Execution boundaries

Source acquisition never executes downloaded code. YAML parsing uses a safe loader and rejects duplicate keys. Source archives are never extracted to arbitrary filesystem paths. Template rendering rejects missing parameters, escape paths and overwrites; structured output is parsed before writing. The GitHub collector performs only GET requests. Audit and gate consume explicit JSON records. Actual API configuration mutations are not implemented in this release.

Repository scaffolding is also local-only. It validates the defined repository-spec and artifact-catalog contracts, type-checks control-relevant profile context, requires the spec's named profile, resolves every control against that explicit context, renders only cataloged artifacts, stages complete files and reserves a new destination without overwriting an existing path. It does not initialize Git, create a remote, apply proposed GitHub metadata, change credentials or settings, publish content, adopt policy, assess compliance, or activate native enforcement. `LICENSE`, `.gitignore`, CI, build/package files and native GitHub settings remain unsupported and visible in the generation manifest rather than being guessed. See [Repository scaffolding](repository-scaffolding.md) for the command and output contract.

## Scope of deterministic checks

The implemented checker families are metadata presence, repository naming, accepted-location file presence, workflow root permissions, immutable action references and effective branch-rule presence/parameters. Manual review is a seventh binding kind. A rule observation establishes only returned active rule state; bypass behavior, legacy equivalence and end-to-end rejection need separate review. File presence is not document quality. SHA syntax is not provenance validation.

## Scale

Large candidate ledgers and raw material are cache/workflow artifacts. Small lockfiles, source receipts, canonical definitions and generated function views stay versioned. No repository is created per control, per source, or per checklist item.
