# A0 — Validator Repair

**State:** Primary

## Objective

Repair PR #472 so recovery accepts valid source-review directories that contain
no `*-claims.json` documents while keeping the consolidation gate open and its
claim denominator unknown.

## Changes

- Add recovery regressions for review directories without claim documents.
- Skip claim-reconciliation accounting when no reviewed claim documents exist.
- Reject supplied claim-reconciliation receipts when no reviewed claim
  documents exist.
- Preserve all existing source-fidelity, authority, and fail-closed behavior.

## Acceptance

- Focused recovery and semantic-certification tests pass.
- The repository test, validate, compile, provenance, recovery, and diff checks
  pass on the exact branch head.
- The repaired head is pushed to PR #472 for human review.

## Non-goals

No semantic extraction, reconciliation decisions, control changes, rights
decisions, native enforcement, source refresh, or later-tranche work.
