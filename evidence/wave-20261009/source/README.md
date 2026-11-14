# B primary source review, 2026-10-09

State: Staged primary proposals, awaiting D omission review, A reconciliation,
and E independent decision audit. No reconciliation receipt is supplied here.

Plan: verify the assignment and pinned source, review a bounded tranche against
actual draft objectives, preserve every assigned claim/occurrence in the crosswalk,
then validate and publish this isolated artifact lane.

The frozen assignment contains 162 claims and 162 structured occurrences. These
are two representations of the same checklist, not an additive 324 propositions.
Detailed primary review covers WA-APPSEC-001 through WA-APPSEC-018 (source lines
15–42). It proposes one MAP and 17 SPECIALIZE dispositions. All 18 remain
unreconciled and unaudited. The other 144 claims are explicitly unreviewed in
this tranche. The full checklist was inspected; this does not certify omission
coverage or complete interpretation of its dependencies.

The review finds consequential differences between existing broad controls and
the checklist: scanner-tool maintenance, proactive credential rotation,
security-policy enforcement, all-team accessibility, secure-coding review content,
and business-system access scope must not disappear behind broad mappings.
Five existing claim paraphrases require fidelity repair or explicit qualification.
See `residuals.json`; original claims and historical evidence remain unchanged.

`proposed-decisions.json` uses the existing semantic-decision schema and stable
identity algorithm. Its `proposition_ids` are the existing claim IDs; it does not
assert that new semantic-proposition records have been created. `draft-dispositions.json`
contains exact claim subjects and receipt-compatible disposition/details/control
projections for A, but deliberately lacks the required reconciler, independent
reviewer, timestamps and authority-policy bindings of a completed receipt.
The referenced GES-OPS proposals already exist at revision 1. They remain quarantined,
with incomplete applicability and source-hash fields, and are not adopted here.

`build_packet.py` serializes explicitly authored judgments; it does not infer mappings
from keywords. Reproduce from the repository root with:

```sh
env PYTHONPATH=. python evidence/wave-20261009/source/build_packet.py /PATH/TO/AUTHENTICATED/.cache
```

The source cache is read-only. It is authenticated by the conductor's frozen
cache-validation evidence, the assignment, and the compressed/source hashes in
`input-bindings.json`. No sync, upstream execution or public source-copy export
was performed.

Observed local validation:

- Packet construction: 162 subjects/occurrence associations checked, 18 semantic
  decisions accepted by `ges.semantics.validate_record`; exit 0.
- `python -m unittest tests.test_semantics tests.test_claim_reconciliation -v`:
  25 tests passed, exit 0.
- `python -m ges validate`: 95 controls valid, exit 0.
- `python -m ges compile`: exit 0, no generated changes.
- `git diff --check`: exit 0.

The conductor owns full integration validation. These results establish local
structural validity only, not semantic approval, merged delivery, owner acceptance,
rights clearance, release completeness or native enforcement. Checkout retained
at the worker worktree for review and integration.
