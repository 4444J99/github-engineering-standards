# Worker B correction records, wave 20261009-correction-01

Scope: role B of the serialized correction wave for PR #496. Exclusive write root
`evidence/wave-20261009-correction-01/source`. Branch
`review/wa-source-wave-20261009`, starting HEAD
`2ad83ba6a3029eebadfd9c97e80cf6def8e98234`. Delivery status stays **Staged**;
nothing here is an approval, receipt, reconciliation, audit, or verification of
the heavy/Governance suite (that runs later at integration).

## Inputs used (all committed in this checkout, read-only)

| Input | sha256 | Field used |
|---|---|---|
| `evidence/source-reviews/wa-application-security-checklist-claims.json` | `a41ba69a8ea30a5338ad56d8bd2c1909a4912eb219ab862e9e4b1af460959993` | predecessor `claims[...]statement`, `start_line`/`end_line`, `mapping_status`, `accepted_policy`, top-level `policy_adoption`/`rights_clearance`/`independent_omission_audit` |
| `evidence/wave-20261009/source/residuals.json` | `cbf159cf9c9d70be0a74bddaee581e67d50b7e0c6fa3444950429114fa7a7124` | `source_fidelity_repairs_required[0..4]` — the five holds |
| `evidence/wave-20261009/source/primary-review.json` | `8e27182d8562f1cd85f1062c07cf43ba81efae76c6df71d8c93593379cfb26f1` | per-claim `interpretation`, `residual`, `decision_id`, `source_span_sha256` |
| `evidence/wave-20261009/source/draft-dispositions.json` | `7f87225f90b1aa2c581242eb2b09531dab2fc3f74b93f9f8c260802540828c52` | `details.distinction`, `rationale`, `status` |
| `evidence/wave-20261009/source/proposed-decisions.json` | `1acf2be74a71744708589d0f0042a4b46d9f881fc2bb2d8e84125e00d377e1db` | decision `rationale`, `control_references`, `review.status`/`reviewer` |
| `evidence/wave-20261009/source/README.md` | (committed) | wave state, boundaries, "five paraphrases require fidelity repair" |
| `evidence/wave-20261009/source/input-bindings.json`, `occurrence-crosswalk.json` | (committed) | source span digests and claim/occurrence identity |
| `evidence/claim-workload-inventory.json`, `evidence/claim-workload-current-inventory.json` | (committed) | claim index context: checklist family holds all 162 `WA-APPSEC-*` claims under artifact `8109355ec58c910ed86a2618`; `reconciled_claim_ids` empty, `semantic_equivalence_verified` false |
| `evidence/semantics/wa/source-scope.json` | (committed) | checklist artifact role `substantive_guidance`, 162 existing text claims, existing receipts |
| Conductor freeze (read-only, other checkout) | `evidence/wave-20261009-correction-01/serialized-admission-03/execution-freeze-20261010.json` | role bindings, claim assignment, `-CORRECTION-01` suffix, serialization contract |

No network access. Nothing read or executed from the stale nested checkout
`/Users/4jp/Workspace/4444J99/engineering-environment-standards/`. The pinned
source bytes (`content/library/application-security/checklist.md` at commit
`a30275bc2d7eb860e612f93cbc1f26d0ff20c0c7`) are **not** in this checkout, so no
corrected statement was re-derived from source text directly.

## Method

1. Preflight (head, tracked tree, remote match, lock files, live writers) — all
   clean; execution lease reacquired under owner `ges-correction-20261009`.
2. Located the hold for each of the five claims:
   `residuals.json → source_fidelity_repairs_required[]` states the defect, and
   `primary-review.json → interpretation/residual` states what the committed
   reviewer established the source requires and what the original paraphrase
   got wrong. `draft-dispositions.json` and `proposed-decisions.json` corroborate
   the same distinction per claim.
3. For each claim, wrote ONE successor record
   `WA-APPSEC-0NN-CORRECTION-01.json` containing: predecessor claim id and
   byte-level identity (statement, line span, statement sha256, source-span
   sha256, document sha256), the exact hold being corrected (quoted with its
   file + index), the correction (a corrected statement plus change summary,
   derivation and qualification), explicit `evidence_references`
   (file + sha256 + field), the linked proposed decision, an outcome, and the
   remaining holds that committed evidence does NOT let this stage close.
4. Predecessor records and historical packets are untouched; only files under
   this exclusive root were created (plus the required rename of the cancelled
   attempt's identity file).

Record shape follows existing repair-record precedents in `evidence/`
(`*-repair*.json`, `*-recheck.json`, `docs-sdk-quickstart-review-repairs-claims.json`,
`byok-independent-claim-audit.json` findings with `finding`/`correction`/`status`):
a declared `schema`, predecessor binding, quoted hold, correction, evidence
pointers with hashes, and explicit non-certification boundaries.

## Outcome per claim

| Claim | Hold (from `residuals.json`) | Outcome |
|---|---|---|
| WA-APPSEC-005 | static restriction absent from original source | **Corrected at statement level.** Corrected statement drops the static-only narrowing: "Include code scanning in delivery pipelines." Remaining holds: source bytes not re-read here; no reconciliation receipt; decision still PROPOSED; mapping/policy unchanged. |
| WA-APPSEC-009 | reviewed practice does not establish regular actual rotation | **Corrected at statement level.** Corrected statement restores recurring actual rotation, both object classes (secrets and credentials), and the exposure-independent trigger. Same four remaining holds, plus rotation authority (claims-document `conflicts`) unresolved. |
| WA-APPSEC-011 | relevant contributors narrows all team members | **Corrected at statement level.** Corrected statement restores the all-team audience and keeps access distinct from training. Same four remaining holds. |
| WA-APPSEC-017 | connected business systems narrows other business systems | **Corrected at statement level.** Corrected statement restores "other business systems" and records that explicit role assignments do not prove enforcement. Same four remaining holds, plus enforcement not evidenced. |
| WA-APPSEC-018 | investigation does not establish recurring audit | **Corrected at statement level.** Corrected statement restores recurring audit and names both system scopes. Same four remaining holds, plus cadence not numerically determined by committed evidence. |

"Corrected at statement level" means: the successor record supplies the corrected
claim statement the hold demanded, bound to committed evidence. It does **not**
mean the claim is reconciled, mapped, audited, adopted, or verified against the
pinned source bytes.

## Unresolved (explicit)

- **Source-byte re-verification**: every corrected statement is derived from the
  committed `primary-review.json` interpretation, not from re-reading the pinned
  checklist. A later stage with authenticated cache access should confirm the
  corrected wording against `content/library/application-security/checklist.md`
  lines 21, 27, 31, 41, 42 at commit `a30275bc2d7eb860e612f93cbc1f26d0ff20c0c7`.
- **Reconciliation receipt**: `draft-dispositions.json` status remains
  `PROPOSED_NOT_RECONCILIATION_RECEIPT`; no reconciler, independent reviewer,
  timestamps, or authority-policy bindings exist in committed inputs, so none
  were asserted.
- **D/A/E gates**: `residuals.json → all_decisions_pending_D_A_E` is true;
  `proposed-decisions.json → review.status` is `PROPOSED`, `reviewer` null.
- **Mapping and policy**: all five predecessors keep
  `mapping_status=UNMAPPED_REQUIRES_OBJECTIVE_AND_BINDING_REVIEW`,
  `accepted_policy=false`; claims document keeps `policy_adoption=NONE`,
  `rights_clearance=UNRESOLVED`, `independent_omission_audit=false`.
- **Conductor accounting**: correction-wave `assignment.json` accounting fields
  (`new_raw_claim_records`, `new_repaired_logical_claims`, both frozen at 0) are
  owned by the conductor; this stage does not rewrite them.
- **Heavy/Governance suite**: not run here by instruction; deferred to
  integration.

## Files in this root

- `identity.json` — this stage's worker identity (supersedes the cancelled attempt's file).
- `identity-cancelled-ses_edbeebdceffe8CrNpIv5HJMXtW.json` — preserved bytes of the cancelled 2026-10-10T04:38:22Z attempt's identity file (renamed, unmodified).
- `WA-APPSEC-005-CORRECTION-01.json`, `WA-APPSEC-009-CORRECTION-01.json`,
  `WA-APPSEC-011-CORRECTION-01.json`, `WA-APPSEC-017-CORRECTION-01.json`,
  `WA-APPSEC-018-CORRECTION-01.json` — the five successor records.
- `README.md` — this file.
