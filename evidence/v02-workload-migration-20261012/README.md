# Workload migration repair — Staged

This repair restores the Toolkit workload gate while preserving its historical
accounting guarantee. It is based on draft PR #497 at
`afdd2ffe03bd840516947a9256ff9aea380335fb`, dependent on unchanged PR #496.
It establishes metadata reproduction, not GES v0.2 completion.

## What changed

The failed test enumerated all current claim documents and compared that expanded
set with a frozen report written before five approved successors were consumed.
The original failure was reproduced: nine integrity tests ran, with one error in
`test_real_current_baseline_and_independent_a3_bytes_reproduce_unchanged`.
The comparison correctly detected changed inputs, counts, family membership,
and claim membership; merely increasing expected counts would lose preservation.

The repair preserves these exact files:

| Preserved file | SHA-256 |
|---|---|
| `evidence/claim-workload-inventory.json` | `6151dcc71dda756610f371337bebe9981c0f9656cc6f7b252ad60e007701f5ec` |
| `evidence/claim-workload-current-inventory.json` | `2e718486119b29cf286f4b21f067d67dc3bea17f2559a45fbc01105931a22658` |
| `evidence/claim-workload-current-provenance.json` | `239fc3e89643202c9a7935749249eb4a0ca14e67a32c6e2a0517166a81e9bbf8` |

`ges.claim_workload_migration` reproduces the frozen report from its exact
654-document membership and applies the original strict historical-equivalence
and A3 provenance checks. It independently reproduces the complete current glob
against [current-inventory.json](current-inventory.json), then permits only the
previously reviewed successor document and its five exact predecessor/successor
pairs. All original claim documents, receipts, approval files, and source metadata
remain unchanged. CI requires both states and the transition.

The new report SHA-256 is
`ed4ee7e8be9a5369d4651769dc8717456473063d2db21010544349a9848b8a00`.

| Metadata workload measure | Frozen | Current |
|---|---:|---:|
| Recorded claims | 61,936 | 61,941 |
| Claim documents | 654 | 655 |
| Advisory families | 4,651 | 4,651 |
| Source-bound records in the frozen provider/OIDC input | 474 | 474 |
| Claims without a record in that input | 61,462 | 61,467 |
| New review or reconciliation credit | 0 | 0 |

Those 474 records belong to this workload's frozen input. They are not the later
2,164 validated dispositions. The conditional future 2,174 dispositions and
59,767 unresolved claims still require authenticated replay and legitimate
replacement-envelope issuance and review.

## Verification and independent review

[verification.json](verification.json) records the exact precommit commands,
runtime, elapsed times, outcomes, and code/report hashes. The prepared review
package records the exact committed head and its subsequent verification.

| Check | Observed result |
|---|---|
| `python -m unittest discover -s tests -v` | 707 tests pass; 0 failures, errors, or skips |
| `python -m ges.claim_workload_migration` with all eight bound inputs | MATCH: both inventories and exactly five successors |
| `python -m ges validate` | Valid; 95 controls |
| `python -m ges compile` | Exit 0 |
| Generated checklist/crosswalk/bindings diff | No changes |
| `git diff --check` | Exit 0 |

These checks ran in the isolated Linux session using Python 3.12 and public
committed metadata. They do not claim either native source authentication or the
six merged-main governance checks. The configured CI Python 3.11/3.13 matrix
remains required; local success does not manufacture a remote result.

The current `/root/migration_review` helper independently reconstructed every
count, family, claim/document membership and source binding without importing
GES code. [independent-review.json](independent-review.json) preserves that
actor's exact observation, commands, reviewed file hashes, and limitations.
The retained [independent-reconstruction.py](independent-reconstruction.py) runs
from the repository root, enforces a 30-second alarm, and rejects optimized Python
instead of silently disabling its assertions. This is an audit reproduction;
the production CI checker uses explicit exceptions.

The reviewer found one resource-safety gap: changed compressed bytes could reach
decompression before the later provenance check rejected them. The repair now
compares the compressed input fingerprint with the independently pinned provenance
before replay. Its new regression was observed failing before the change and
passing afterward. The reviewer independently ran all 15 migration tests.

## Native replay and concurrent work

[native-prerequisites.json](native-prerequisites.json) records actual read-only
observations. At 19:07:42 UTC the host still denied heavy admission for
`swap-fraction`; at 19:15:14 UTC it denied `swap-fraction` and `vitals-shed`, with
10,324,541,440 swap bytes on a 17,179,869,184-byte host. No native execution or
heavy lease was acquired by this session, and no source replay was launched.

The retained original cache is present. Bounded metadata hashing found the exact
original artifact SHA-256 `d53ff71f…47c87c` in both its corpus locations, plus
the expected v2 frozen capsule manifest fingerprint `0a177df2…1d83`.
That corrects the available-location knowledge while leaving the old unavailable
observation intact. Snapshot contents and rendered bodies still require actual
authentication; an index-file hash is not a full-body verification.

Another GES session acquired the retained checkout's writer lease at 19:08:19 UTC
and left its own untracked `evidence/claim-workload-v02-inventory.json`. This
session preserved that checkout and its owner's work. The repair is prepared on
a separate local dependent branch for review and integration into #497.
Automatic approval review rejected the GitHub push because the evidence payload
may contain private organizational metadata and this exact public upload needs
explicit authorization. No remote branch or draft PR was created. Publication
remains pending approval of the concrete review package.

The original-head Toolkit run 38081454423 failed and skipped the later gate steps.
Source-acquisition run 38081456873 is independently observed successful. Neither
is an execution receipt for the new repair or current replacement envelopes.

## Concrete next execution

The retained source locator is in `evidence/wave-20261009/cache-validation.json`.
After the active writer releases or intentionally integrates this repair, obtain
actual scoped execution and heavy admission. Use the retained v2 capsule,
`a3-corpus-20261006`, sources, and rendered cache. Within a finite verification
deadline, run:

```sh
python -m scripts.a3_capsule_receipt \
  --capsule <original-cache>/a3-six-source-capsule-20261006-v2 \
  --capsule-sha256 0a177df2e99bd3add5a8701a2f3a1e1ebd0ca1ba51fdb1676947a79f21ea1d83 \
  --sources <original-cache>/sources \
  --corpus <original-cache>/a3-corpus-20261006 \
  --rendered <original-cache>/rendered-docs \
  --expected-structured-count 605 \
  --tree-evidence evidence/a3-pin-bound-tree-observations.json \
  --output <new-ignored-output>/authenticated-capsule.json

python -m ges.claim_reconciliation \
  --artifacts <original-cache>/a3-corpus-20261006/artifacts.jsonl \
  --sources <original-cache>/sources \
  --reviews evidence/source-reviews \
  --review-policy evidence/source-review-policy.json
```

The second command intentionally omits both receipt and reconciliation-policy
inputs. It can produce current provenance accounting and input digests without
inventing certification. It reports zero validated dispositions for that absent
receipt input, not a repudiation of preserved historical decisions.

The original owner grant names the October 10 Codex reconciler and its
`finishline_gates` reviewer. It does not authorize the current actors to use those
identities. After genuine renewed authority, prepare new envelopes without
altering originals; independently compare all 2,164 carried decisions and the
ten proposed new dispositions; then execute reconciliation and recovery with
the new exact-input policy. Provisional decisions stay in ignored cache until
that authentic evidence exists.

## Remaining acceptance and custody

The native/adapters/synthesis, retained-body assurance, complete public pilot,
release-file inventory and rights, human code/security review, owner acceptance,
merged-main checks, and release distribution remain governed by the October 10
plan. Private support is unverified. No gate is closed by this repair.

This tranche began at 19:04:54 UTC and has a 19:34:54 UTC checkpoint boundary.
The recorded root verification work is below 600 seconds; helper script timeouts
remain explicit in its observation. Historical cumulative usage remains UNKNOWN;
this session is additive. Native checkouts and caches are retained. The isolated
repair checkout is retained and its tracked products are preserved in Git.
