# Current reconciliation issuance after cloud replay

Status: staged authorized partial reconciliation; v0.2 acceptance remains open.

## Authorized execution — October 12, 2026

After this runbook was staged in PR #507, the owner directly approved the exact
current actor pair and 2,174-decision scope at 21:44:17 UTC. The additive grant,
actual issuance, distinct final-envelope review and successful source-bound
accounting are retained in `evidence/v02-authorized-reconciliation-20261012/`.
Accounting now reports **2,174 validated / 59,767 unresolved out of 61,941**, with
`mapping_complete=false`. No historical grant, receipt or report was overwritten.
The private final ledger is preserved separately. The original authority finding
below describes the pre-grant inspection; it is superseded for this exact scope.

Full recovery integration was attempted and failed for the missing full frozen
corpus `candidates.jsonl`; no successful recovery report was produced. Original
capsule/rendered-body restoration, publication, pilot and acceptance gates remain
open. The completed source cache was reused without acquisition; source provenance
was revalidated as part of the accounting contract.


PR #506 preserves completed current source replay at `6c37fe5` and its independent
review. Reuse those executed results for the same locked archives and unchanged
input hashes. Do not rerun acquisition merely to address the role-grant gap.
Fresh verification of final accounting by `ges.claim_reconciliation` still reruns
claim provenance as part of its existing contract. It can consume the retained
fresh-pinned source cache without network acquisition. Do not add a flag that trusts
a saved success report in place of source-bound accounting.

## Authority finding

The preserved `evidence/v02-finish-20261010/owner-authorization.json` names:

| Role | Granted actor |
|---|---|
| Reconciler | `codex:01a12707-22ff-7f52-b05b-937b45b7ce0c:/root` |
| Independent reviewer | `codex:01a12707-22ff-7f52-b05b-937b45b7ce0c:/root/finishline_gates` |

Its scope covers five successor claims, predecessor supersession and unchanged
carryforward audit, with exact complete claim/catalog/proposal bindings. It forbids
identity substitution and backdating. These actors are not the current cloud root
and reviewer. The historical combined policy binds the old universe; the separate
OpenCode serialized-execution grant names other actual roles and does not grant
these cloud actors replacement issuance authority. Source-review, continuation,
publication and mechanical-review permissions do not supply the missing grant.
No authentic replacement grant was found in the inspected tracked records, PR #506
conversation or retained preparation records. This finding is bounded to those
accessible records; it does not assert absence in inaccessible owner conversations.

The concrete proposed replacement pair is:

| Role requested, not granted | Actual current actor |
|---|---|
| Reconciler | `chatgpt-cloud:20261012:2aefcbff59bd:/root` |
| Independent receipt reviewer | `chatgpt-cloud:20261012:2aefcbff59bd:/root/envelope_review` |

The latter is currently a read-only software reviewer. Code review alone is not
receipt review, and neither task is an independent human approver. A direct owner
decision must name the pair and exact package before either actor issues or reviews
receipt envelopes. Preserve the authentic decision reference and actual recording
time in a new record; do not edit the historical grant or imply broader authority.

## Exact requested package

| Binding | SHA-256 |
|---|---|
| Reviewed nonissued draft bytes | `a8b9065b0a5a43e950451683badcbeaa335cc344bbce78940dac4420fb6d7185` |
| Canonical draft | `010aa6e9003301d96825cb1f34b317bafb401783e9f7462c40ac1c7d05bbb8e6` |
| Current claim universe | `4c9c65b1c59f656d0a8bc423ee84c26e835754f7fca02ac4cc8df8e27f5bd20b` |
| Catalog | `125555b58ee9cfc66af0fb335429911005f1f9ad1da555ea4f0acd51602ec24c` |
| Proposals | `e16b506ada35741ea1d61f93bcf11b846893b643eb6e25eaed4a6edb70cf59d4` |

Scope: 2,164 unchanged carried decisions plus five predecessor SUPERSEDED exclusions
and five successor SPECIALIZE decisions. Preserve all subjects and substantive
fields. Keep `accepted_policy=false` and `adopted_obligation=null`. Permitted envelope
changes are schema, actual reconciler/reviewer identities and actual issuance/review
timestamps only; the reviewed draft already binds the current universe.

The fresh retained-draft check reconstructs every current subject from hash-checked
metadata and all 655 claim documents, verifies all 2,174 dispositions structurally,
and compares 19,476 carried fields. It reuses the ten-disposition semantic review
recorded in #506; it does not claim a new semantic adjudication or source replay.
The private draft remains private. Its recorded hash is the review anchor.

## Sequence after genuine owner grant

1. Authenticate the decision and record a separately named current-role policy with
   all three bindings. The CLI cannot establish identity or approval authenticity.
2. The granted reconciler authenticates the pinned draft, inspects its decision
   package, and issues a separate final ledger with actual current issuance times.
   Preserve the original draft, historical receipts, policies and execution reports.
3. The distinct granted reviewer compares every final envelope with the exact draft
   and policy and records actual final review evidence and times after issuance.
   Do not reuse the October 12 earlier draft-review timestamps. Keep final review
   evidence separate from both prior semantic review and this software review.
4. Use the read-only comparator, with the actual private paths:

   ```sh
   python -m ges.reconciliation_envelopes \
     --draft PRIVATE_DRAFT.json \
     --draft-sha256 a8b9065b0a5a43e950451683badcbeaa335cc344bbce78940dac4420fb6d7185 \
     --receipts ISSUED_RECEIPTS.json --policy AUTHORIZED_POLICY.json
   ```

   It compares exact membership and every substantive field and checks role strings
   against the supplied policy and ordered nonfuture timestamps. Its output is
   expressly mechanical comparison, with no authorization or accounting credit.
   It neither writes envelopes nor proves that declared actors actually acted.
5. Run `ges.claim_reconciliation` using retained authenticated artifact metadata,
   fresh-pinned sources, current reviews/catalog/proposals, and the same issued
   receipts/policy pair. Capture actual output, exit, times, code/input/output hashes.
   Pass that same pair into `ges.recovery`; missing other gate inputs remain unknown.

Only successful actual accounting can establish the conditional 2,174 validated /
59,767 unresolved out of 61,941. A discrepancy is a finding to investigate, not a
reason to alter evidence to match arithmetic. Reconciliation remains partial.

## Integration and remaining acceptance

This narrow verification addition is a dependent draft after #506, retaining
#496 -> #497 -> #503 -> #506 and their review/merge boundaries. It changes no historical
receipt or owner grant. Final merged-main verification and owner acceptance remain
required; green branch tests constitute staged evidence.

Original A3 capsule restoration, historical rendered-body authentication,
source-to-claim omission completeness, remaining adapters and six-source synthesis,
full public disposable pilot evidence, exact-use publication clearance, human
code/security review, distribution approval and owner acceptance remain separate.
Private pilot support remains unverified. No reconciliation grant approves those
milestones, policy adoption, native rollout, estate rollout or a release.
