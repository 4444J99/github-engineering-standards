# Serialized admission 03 - execution freeze addendum (2026-10-10)

This directory's original receipts (`blocked-recovery.json`, `README.md`) are
preserved byte-identical: they remain the record that A admission was blocked on
two items. Both items have since been supplied by the human owner, and this
addendum records their receipt plus the resulting execution freeze. No prior
receipt was rewritten and no second blocked receipt was published.

| File | Contents |
|------|----------|
| `authorization-20261010.json` | Owner authorization: nine-checkout custody transfer, continuation #2821 reapplied (supersedes the 120-minute stop), tranche and measurement policy, execution directive, retained gates. |
| `custody-transfer-20261010.json` | Nine worker checkouts at their recorded transfer heads plus conductor at `e3ba18e`; tracked trees clean, zero locks, zero live writers, ignored-payload manifests recorded; new custodian `opencode:ses_edcbc89dcffe1pHZoV5eWgrR33`. |
| `cache-authentication-20261010.json` | Input authentication replay: reference hash and all six source snapshots MATCH `evidence/wave-20261009/cache-validation.json` (status AUTHENTICATED, gate OPEN). Read-only; stale nested checkout never executed. |
| `host-admission-20261010.json` | Execution leases (30-minute tranches) under owner `ges-correction-20261009`; heavy admission deferred to the final verification tranche, gate intact. |
| `broker-status-20261010.json` | OpenCode-scoped registration and inspection; root-run reservation rejected `execution_priority_not_approved` (owner-gated, `4444J99/limen#2840`); recorded once, not bypassed, zero runs claimed. |
| `execution-freeze-20261010.json` | The new execution freeze: identities, role-to-checkout-to-head bindings, exclusive roots, serialized order B -> C -> D -> A reconcile -> E -> A integrate, stage budgets and deadlines, cumulative accounting with distinct meters, all gates retained. |

Status remains **Staged**. The planning freeze (`../assignment.json`) is
untouched; this addendum publishes the execution freeze alongside it.
