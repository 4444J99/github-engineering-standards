# Enforcement and trust boundaries

The `gate` command returns nonzero when required applicable controls fail, lack evidence, are stale, or have unknown applicability. It checks report cardinality, control revisions, obligations and catalog digest against the selected control catalog. It is a component of enforcement, not proof that a hosting platform actually requires it.

`--require-accepted` rejects draft controls. `--allow-exceptions` permits current approved exceptions only for observed FAIL/PARTIAL results; it does not mask ERROR, missing observations, stale evidence or unknown applicability. Exceptions preserve the original outcome. All report input files and reviewer allowlists must be controlled by a trusted workflow; this local CLI does not cryptographically authenticate a JSON author's identity.

Reports must be produced from current, authentic observations in the same trusted job that runs the gate. A saved report is not a signed compliance certificate. Catalog, profile, snapshot and attestation trust must be established outside this evaluator. Do not execute fork-supplied checker code with privileged credentials.

## Native activation

First approve a target profile and control set. Collect a baseline. Repair failures through reviewed changes. Exercise acceptance and rejection in a dedicated test repository. Validate required check names, events, branch selection, merge-queue behavior, human review availability, bot permissions, legacy protections, inherited rules and bypass actors. Only then activate a versioned ruleset with a tested rollback plan.

The supplied ruleset template is parameterized, not auto-applied. Solo profiles do not require an unavailable independent native reviewer by default; they retain a separate accountable review requirement. Team thresholds are illustrative and require staffing validation. Age alone never waives a review.

No native protections or other repositories are changed by the toolkit's assessment commands. CI for this repository verifies the toolkit and generated outputs; green toolkit CI does not certify complete source review or all target controls.
