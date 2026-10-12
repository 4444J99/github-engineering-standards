# A3 reference continuity during workload migration — Staged

This narrow follow-up retains the historical/current workload migration already
published on PR #497 at `25affa78bcbf16e89667cbe3cbcfbc3a7fa05006`. It protects
the independently pinned A3 source-identity reference through the complete
two-report check. It provides no new source authentication or reconciliation
credit and closes no v0.2 acceptance gate.

## Concurrent repair and preservation

The initial PR #503 implementation was published at
`f266c4d8fa3a1d81292c57556bfdd3f968552423`, reproducing the exact approved local
tree `28e707ffb971c5a6f3f25d0730e5ac742ed0589d`. While it was being published,
another session advanced PR #497 with an independently implemented repair.

Both implementations produced byte-identical current inventories with SHA-256
`ed4ee7e8be9a5369d4651769dc8717456473063d2db21010544349a9848b8a00`: 61,941 claims
in 655 documents, preserving the historical 61,936 claims in 654 documents.
Each required exactly the approved five successors and awarded zero new credit.

This follow-up keeps #497's implementation, CLI, workflow, transition contract,
canonical current inventory and evidence. The alternate implementation is
preserved in Git history at the initial #503 revision; the integration retains
both published histories. The final working tree has one production checker and
one canonical current report at `evidence/claim-workload-v02-inventory.json`.
No colliding dated evidence file is overwritten.

## Confirmed gap and change

The preserved report's provenance checker validates the A3 reference during the
historical replay. The surrounding transition checker snapshots the other
inputs across both historical and current replays, but it omitted this reference
from its final stability checks. Changing its bytes or replacing it with an
identical-byte symlink after either replay could therefore still return MATCH.

After the historical replay has validated the provenance and reference shape,
the transition checker now resolves that same reference, rejects symlinks, and
checks its bytes against the just-validated pinned digest before the current
replay. At the final boundary it requires the same canonical path and identical
bytes. The initial digest comparison also closes the interval between the
historical replay's return and the new snapshot. Existing authority constants,
transition/report/provenance bytes, claim decisions and public CLI remain intact.

## Observed regression

Two tests cover four cases: byte mutation and identical-byte symlink replacement,
each immediately after the preserved replay and after the current replay.
At 19:47:28 UTC, all four cases exposed the gap: `ValueError not raised`. After
the production change, both tests and all four cases passed at 19:47:49 UTC.

[regression-observation.json](regression-observation.json) preserves the exact
command, UTC times, return codes, durations, log digests and complete before/after
output. [independent-review.json](independent-review.json) records the separate
current reviewer's findings and reviewed file hashes. The final PR body records
the actual published integration head, complete bounded suite and workflow
results. Those results remain branch checks, not merged-main acceptance.

## Continuing prerequisites

Native admission was still denied at 19:36:09 UTC for swap-fraction,
disk-throughput and vitals-shed. This session acquired no native execution/heavy
lease and launched no full source replay. The exact original artifact metadata
was located by bounded hashing in the earlier
[native observation](https://github.com/4444J99/github-engineering-standards/blob/f266c4d8fa3a1d81292c57556bfdd3f968552423/evidence/v02-workload-migration-20261012/native-prerequisites.json);
that does not authenticate all source snapshots or rendered bodies.

The 474 frozen workload receipt subjects remain distinct from the later 2,164
validated dispositions. The expected 2,174 validated / 59,767 unresolved result
is still conditional. Replacement envelopes need authentic scoped actors and
independent comparison of all carried decisions plus ten new dispositions.
Public pilot evidence, retained-body assurance, adapters/synthesis, publication
clearance, human review, owner acceptance and merged-main checks remain open.
Private support remains unverified.
