# Completion milestone reporting

Recovery reports separate evidence states for six-source synthesis, public
release clearance, native pilot acceptance, and estate rollout. The GES v0.2
aggregate requires the first three. Estate rollout keeps its independent
authorization and acceptance boundary.

This is an additive reporting implementation. It does not accept controls,
activate protection, authorize publication, or assert owner acceptance.

## Evidence mapping

| Output | Required evidence | Independent boundary |
|---|---|---|
| `six_source_synthesis` | All original conditions and coverage requirements of legacy gates 1–6. | Source completeness, generalization and operational completeness retain every existing gate. |
| `public_release_clearance` | Separately validated `ges.publication-use-accounting.v1` for a `GES_V0_2` candidate, including complete output inventory, complete actual-use accounting, exact-use clearance and authorized distribution. | Legacy per-artifact rights gate 8 cannot supply this result. |
| `native_pilot_acceptance` | All original conditions and coverage requirements of legacy gate 7. | Provisioning or configuration presence is insufficient. |
| `estate_rollout` | All original conditions and coverage requirements of legacy gate 9. | Does not block GES v0.2; remains required for the legacy all-nine-gate program. |
| `ges_v0_2` | Synthesis, public release clearance and native pilot acceptance. | Does not automatically authorize release or replace organizational acceptance. |
| Legacy `project_complete` | All nine original legacy gates are `CLOSED`. | Preserved for compatibility; not a synonym for `ges_v0_2`. |

The complete nine-gate array remains mandatory even though gate 8 is not used to
derive exact-use public clearance. Missing, duplicate and unknown gate identities
are rejected. Each gate's conditions, completed count, denominator, remaining
count, state and failed/unknown condition lists are recalculated and checked.
An extra approval field or a claimed `CLOSED` status cannot override the evidence.

The module continues to expose the same legacy `evaluate_gate` function through
`ges.recovery`; its evaluator contract and all nine original gate prerequisites
are unchanged.

## Result states

Every milestone has both a `status` and an `evaluation`:

| `status` | `evaluation` | Meaning |
|---|---|---|
| `CLOSED` | `PROVEN` | Every required observation is explicitly satisfied by the supplied validated accounting. |
| `OPEN` | `INCOMPLETE` | At least one required condition is observably unsatisfied; other evidence may also be missing. |
| `OPEN` | `UNVERIFIED` | No condition is observably false, but at least one required observation is unavailable. |

`incomplete_conditions` and `unverified_conditions` remain separate, including
when the overall evaluation is `INCOMPLETE`. A partially reviewed source set
with no independent omission audit therefore reports both the observed review
gap and the missing audit. Missing native-pilot evidence remains unknown.

`PROVEN` retains the evaluator's bounded evidence meaning. It is not the
repository's governed `Verified` designation. Human review, merged-main checks,
remote CI, applicable security review, and owner acceptance remain necessary
under [GOVERNANCE.md](../GOVERNANCE.md).

## JSON and command-line output

The report retains `schema_version: ges.recovery.v1`, `project_complete`,
`gates`, and existing accounting fields. It adds:

- `publication_use_accounting`: a fresh result from the exact-use validator,
  or `null` when no publication input group was supplied.
- `milestone_accounting`: schema `ges.completion-milestones.v1`, a `milestones`
  mapping containing the four named results, and the separate `ges_v0_2` result.

Each milestone includes its required gates, evidence-input references, evaluated
conditions and failed/unknown condition lists. Public clearance also records
the actual-use accounting digest, release scope and use counts. The CLI summary
prints the four milestone evaluations and `ges_v0_2` beside the existing legacy
fields.

With no publication inputs, public release clearance is `UNVERIFIED` even when
legacy gate 8 is closed. Existing per-file receipts retain their existing
meaning and cannot be reused as an actual-use clearance result.

The following command shows the complete optional publication input group;
the referenced files must contain real, separately authorized evidence:

```sh
python -m ges.recovery \
  --sources .cache/sources \
  --corpus .cache/corpus \
  --reviews evidence/source-reviews \
  --review-policy evidence/source-review-policy.json \
  --publication-manifest .cache/publication-manifest.json \
  --publication-register .cache/publication-register.json \
  --publication-receipts .cache/publication-receipts.json \
  --publication-policy .cache/publication-policy.json \
  --publication-output-root .cache/release-candidate \
  --output .cache/completion-report.json
```

All five publication arguments must be supplied together. The reporter validates
the underlying records and candidate files in the current process; it does not
accept a precomputed milestone report or an approval boolean as an input.
Malformed inputs fail before producing a report. Successfully writing a report
does not mean its milestones passed: the existing reporting command's successful
exit is not itself a release gate.

## Publication scope and denominators

The exact-use validator observes the candidate directory's complete file set and
bytes, validates the actual-use register against pinned source evidence, and
checks the separately approved scoped review and distribution evidence. See the
[actual-use contract](publication-use-register.md) for its trust requirements.

A validated `BOUNDED_PACKAGE` result remains visible in
`publication_use_accounting`, but cannot close the project's `GES_V0_2` public
release milestone. Naming a package does not establish its completeness; the
approved inventory and register must cover the exact claimed output set.

An undeclared legacy denominator remains unknown; a zero legacy denominator is
not a passing gate. Publication has one explicit separate case: a nonempty
candidate output set may contain no upstream expression. Its zero-use register
may clear only when every output has an explicit reviewed zero-use disposition
and the validator has checked the complete inventory, independent review, human
acceptance and distribution approvals. An empty register or a summary claiming
`zero_use_clearance: true` cannot establish that exception.

## Current limits and validation boundary

Structured-occurrence reconciliation, generalization, policy adoption, binding
verification, native enforcement and estate evidence adapters remain unfinished.
The milestone projection does not implement those adapters or invent evidence
for them. Recovery consequently retains their unknown or incomplete conditions.

Regression tests exercise inconsistent gate identities, altered conditions and
counts, false closure claims, missing publication inputs, legacy-rights
substitution, actual-use scope mismatch, and a valid synthetic publication
receipt chain. Positive projection fixtures can show the GES v0.2 aggregate
closing while estate rollout remains open. Those are tests of the scope mapping,
not evidence of a real accepted pilot or actual public clearance.

Existing committed recovery reports retain their recorded evidence and
timestamps. New reporting code does not update those historical receipts or
establish that any currently open project gate has closed.
