## Scope

Dependent implementation tranche based on #496 at a9ab644. The PR targets
`wave/wa-publication-20261009` so #496 retains its declared scope and unchanged
head. After its governed acceptance, retarget this tranche to main; do not replay
#495, which is already an ancestor. This PR is Staged, not Verified or release-ready.

- Add five consumed successor claims, exact scoped owner authority, independently
  reviewed semantic dispositions and full metadata digest/carryforward-subject audit.
  Preserve historical claims and receipts; replacement envelopes remain unissued.
- Implement a fail-closed structured-occurrence adapter and paired recovery inputs.
- Implement the explicitly owner-approved JSON representation amendment, including
  v2 schema and unchanged independent rights, human and distribution gates.
- Record actual public-pilot execution/rollback and a precise remaining matrix.
  Pilot main is restored and rule Disabled; private support is not established.

## Observed verification

100 focused tests pass: structured reconciliation 15, JSON representation 8,
publication use 31, completion milestones 21, structured reference review 25.
V2 JSON Schema validation plus 14 synthetic documents pass. Pinned WA source spans
and actual GHQR decoded expression comparison pass. `git diff --check` passes.
Independent agent code review found three issues; regression tests and fixes were
subsequently rechecked. Agent review does not replace required human review.

## Holds

Heavy host admission denied full suite/corpus replay and prescribed governance
checks. No current full reconciliation accounting or accepted control is claimed.
Remaining evidence adapters, six-source extraction, retained-body authentication,
full pilot matrix, final release-file inventory/rights, human code/security review,
owner acceptance, main checks/CI and distribution/tagging all remain open.

The durable evidence and exact results are in
`evidence/v02-finish-20261010/README.md`; the approved implementation plan is
`.codex/plans/2026-10-10-finish-ges-v02.md`.
