# A6 — Reconciliation machinery

Build on A5 commit `109a10d65179522d2f4e412c5b559858908d44cd` (PR #477).
The deliverable is a separate dependent PR. Retain this worktree for review.

## Implementation

- Group propositions by exact subject/action/object into deterministic comparison
  proposals; preserve all semantic-field and applicability differences.
- Bind full proposition records and the catalog to one immutable input digest.
- Validate A5 decisions, control revisions, semantic field accounting, explicit
  conflicts, duplicate equivalence, and separately authorized review roles.
- Require primary, omission, reconciliation, and independent-audit evidence
  for reviewed decisions. Keep partial coverage, conflicts, and ambiguities open.
- Expose `semantics reconcile` and `semantics audit`; keep extraction reserved.

## Acceptance

Focused negative tests cover false equivalence, stale digests, unauthorized or
collapsed reviewer roles, conflict erasure, and proposals asserted as evidence.
Run the full suite, catalog validation, deterministic compilation, claim
provenance, recovery accounting, and diff checks. Push the branch and open a PR
against A5. Human review and integration remain separate acceptance states.

## Scope

Synthetic fixtures only. No real semantic decisions, authority grants, adopted
controls, source ingestion, native settings, or construction-gate closure.
