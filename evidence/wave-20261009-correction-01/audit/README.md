# Worker E audit — wave-20261009-correction-01 (`-CORRECTION-01`)

Independent audit of the serialized correction execution (PR #496) against the
execution freeze published by the wave conductor (role A). Worker E is the
fourth writer and the final stage before A-integrate.

**Status: Staged. This directory grants no approval, release, clearance,
verification receipt, or merge authority.**

## Identity and bindings

| Field | Value |
|---|---|
| Role | E (audit) |
| Session | `ses_edb94c890ffeK7iqZc9PU59AgI` (source: env `OPENCODE_SESSION_ID`) |
| Runtime | agent `opencode`, provider `opencode`, model `mimo-v2.6-flash-free` |
| Checkout | `/Users/4jp/Workspace/4444J99/.worktrees/ges-wave-e-20261009` |
| Branch | `review/wave-20261009-e` |
| Starting HEAD | `509f4a4f3268d1d91c97d898f1c90e48a6946a52` (local = remote) |
| Execution lease | `fb2e8ffd19aa43b5894eaad67c21d636`, owner `ges-correction-20261009`, acquired 2026-10-10T06:06:26Z, expires 2026-10-10T06:36:26Z, `allowed: true` |
| Exclusive write root | `evidence/wave-20261009-correction-01/audit/` |

## Verified input heads (all pre-read, all clean)

| Input | Checkout | Head |
|---|---|---|
| E (self) | `ges-wave-e-20261009` | `509f4a4f3268d1d91c97d898f1c90e48a6946a52` |
| A (conductor, read-only) | `ges-wave-20261009` | `21e9719af490740b7807bf4fa5ce3931d120ed5d` |
| B | `ges-wave-b-20261009` | `c034c82d6e15b29e30711f3cb77b53d5a61e206c` |
| C | `ges-wave-c-20261009` | `a29214dc5ff55dd5df6176a80d1f4478789a9beb` |
| D | `ges-wave-d-20261009` | `4e137f69448ac10fe20002838941369b72d255b1` |

Each was verified with `git rev-parse HEAD` plus an empty
`git status --porcelain -uno` before any read. Stage ranges audited:
B `2ad83ba..c034c82`, C `a2b81ff..a29214d`, D `4768db8..4e137f6`.

## Method

Committed bytes only; no network, no fetch, no new checkout, no sibling write,
no stale nested checkout read or executed, no heavy/Governance suite (deferred
to A-integrate by the freeze).

1. Preflight (head, cleanliness, remote match, zero git locks, no live writer),
   then execution-lease reacquisition, then `identity.json` written first in the
   exclusive root.
2. Mechanical re-derivation with `check-audit-correction-01.py` — 60 bounded,
   read-only checks: heads/cleanliness, `git diff --name-only` and
   `--numstat` exclusivity and additions-only stats, identity/session binding,
   B/C disposition fields, D coverage matrix vs `assignment.json` counts,
   lease-record consistency, gate-retention strings in the freeze and admission
   receipts, and hash bindings.
3. Inline independent re-hash of the nine publication-candidate files against
   `assignment.json` bindings (9/9 MATCH).
4. Narrative reconciliation of the lease story across the four `identity.json`
   files, `reconciliation-CORRECTION-01.json`, and a read-only
   `host-work-admission.py status` call.

## Verdicts summary

| Check group | Verdict |
|---|---|
| Preflight / input binding | PASS |
| Role binding (identity files, distinct sessions, A identity) | PASS |
| Exclusivity of write roots (B, C, D) | PASS |
| Additions-only preservation (651 / 478 / 2195 insertions, 0 deletions) | PASS |
| Serialization: single lease id across B/C/D, non-overlapping commits | PASS |
| Explicit lease release before A-reconcile | NOT_VERIFIED (assertion only) |
| **Lease-record consistency (C identity + reconciliation narrative)** | **FAIL — sole failed check of 60** |
| Honest dispositions: B 5 records retain holds | PASS |
| Honest dispositions: C 2 fields `REMAINING_HOLD`, no clearance | PASS |
| D coverage matrix = 5 claims + 2 fields, 270/0 checks | PASS |
| Planning-freeze selected counts (5 / 2, assignment sha verified) | PASS |
| Gate retention (storage latch closed, broker closed-not-bypassed 0 runs, ≤30 min, review deferred, publication HOLD, Staged) | PASS |
| Hash bindings (freeze sha ↔ reconciliation; assignment sha ↔ freeze) | PASS |
| Candidate integrity re-derived independently | PASS 9/9 |

Overall: **PASS_WITH_FINDINGS** — see `decision-audit-CORRECTION-01.json`.

## Findings

* **E-FINDING-01 (MINOR, record accuracy)** — C's `identity.json` lease block
  records `acquired_at_utc 05:16:00.270654Z` (stage B's instant) with
  `expires_at_utc 05:55:52.484409Z`, which cannot be produced by that acquire
  plus the stated 1800 s TTL (→ 05:46:00); an unrecorded refresh at 05:25:52Z
  is implied, and the reconciliation narrative records only the 05:16:00Z
  acquire and the 05:41:10Z refresh. C's `preflight.completed_at` (05:16:00Z)
  also predates B's release (05:24:09Z) although B was still writing. B's
  cancelled-attempt identity shows the same class of defect (TTL 1800 s vs a
  45.6-minute span). Not evidence of concurrent writers: same single lease id,
  commit times strictly ordered (B 05:23:50Z → C 05:36:18Z → D 06:00:53Z →
  A 06:04:59Z), C's writes follow B's release.
* **E-FINDING-02 (INFORMATIONAL, evidence gap)** — the explicit release of wave
  lease `2faae7b2…` after stage D is asserted only in the reconciliation; no
  release receipt is committed. Corroborated indirectly: E's acquire at
  06:06:26Z returned `inherited: false` with no other live lease under the
  owner, and `status` at 06:09:34Z listed only E's lease.

## Unresolved / NOT_VERIFIED

* Exact release event of lease `2faae7b2…` (no committed receipt).
* Source-byte re-reads (pinned checklist / ghqr budgets.yaml bytes absent from
  the reviewed checkouts) — inherited from committed review records.
* Semantic or rights approval; ADAPTATION classification; publication
  clearance (both use fields remain HOLD).
* Reconciliation receipt, mapping status, policy adoption (decision still
  `PROPOSED`, reviewer `null`).
* D's 270 checker results verified as recorded, not re-executed by E.
* Stage wall-clock durations are self-reported; only commit timestamps were
  corroborated.
* Heavy/Governance suite — not run; deferred to A-integrate.
* Live vitals: read-only admission `status` at 06:09:34Z reported
  `allowed: false, reason: vitals-shed` while E's execution lease (granted
  `allowed: true` at 06:06:26Z) remained live; the heavy gate may deny at the
  final tranche and is never overridden.

## Files

* `identity.json` — worker E identity, preflight, lease, verified input heads.
* `decision-audit-CORRECTION-01.json` — per-check verdicts, findings,
  NOT_VERIFIED/approval section, overall verdict.
* `check-audit-correction-01.py` — bounded read-only checker (60 checks).
* `README.md` — this file.
