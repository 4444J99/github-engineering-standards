# GES v0.2 fresh cloud provenance replay — October 12, 2026

**Staged evidence.** The complete current claim-source provenance replay succeeded
in the independent Linux cloud workspace at repository revision
`6c37fe5eb98039341cb49444305703dc43048685`. Execution ran from
`2026-10-12T20:15:26.719047+00:00` to
`2026-10-12T20:17:15.825220+00:00`.

This continuation depends on draft PR #503, which preserves the independently
committed A3 identity through historical/current workload verification. PR #503
depends on #497, and #497 depends on #496. Nothing in this record constitutes a
merged-main result, human review, owner acceptance or release clearance.

## Actual result

| Measure | Observed value |
| --- | ---: |
| Locked public source repositories acquired | 6 |
| Artifact identities matching the independent A3 reference | 13,657 |
| Text artifacts authenticated for complete snapshot coverage | 11,828 |
| Current claim documents | 655 |
| Current raw claims with validated provenance | 61,941 |
| Source artifacts referenced by current claims | 3,556 |
| Validated duplicate relationships | 7 |
| Current validated reconciliation receipts in the envelope-free command | 0 |
| Unresolved claims in that command | 61,941 |

All six archive digests matched their locked values. All six independently fetched
Git trees reconciled with `MATCH`, without missing, extra or mismatched blobs.
Snapshot verification checked the actual text content SHA-256, Git blob identity,
size, source identity, uniqueness and complete text-artifact coverage.

The source snapshots were newly acquired at their locked commits. Their metadata
was compared with the preserved October 7 artifact rows, whose compressed and raw
digests were checked before use. No source retrieval timestamp was backdated, and
fresh snapshot bytes were not represented as the original cache bytes.

| Binding | Actual digest |
| --- | --- |
| Complete current claim universe | `4c9c65b1c59f656d0a8bc423ee84c26e835754f7fca02ac4cc8df8e27f5bd20b` |
| Catalog | `125555b58ee9cfc66af0fb335429911005f1f9ad1da555ea4f0acd51602ec24c` |
| Proposals | `e16b506ada35741ea1d61f93bcf11b846893b643eb6e25eaed4a6edb70cf59d4` |
| Preserved October 7 artifact metadata bytes | `86225491fb70197b893a0bfb1fa96ebfc1f5a6e33c21c86ab874d9d34f5db9a2` |

The claim, catalog and proposal digests agree with the earlier correction audit.
Agreement is now supported by actual source replay. It does not convert the earlier
metadata-only observation into a historical full-replay result.

## Execution and independent review

The actual outer command, run from the repository root, was:

```sh
/usr/bin/timeout --signal=TERM --kill-after=3s 300s \
  /usr/bin/prlimit --as=3221225472 --cpu=240:245 \
  --fsize=536870912 --nofile=256 -- \
  /opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python \
  -u .cache/cloud-replay-20261012/fresh_source_replay.py
```

`fresh-source-replay.v1.py` retains the exact executed driver bytes. Its SHA-256 is
`cefd1049a88ef4515efad1407c82c09d681368455292998b82eb4949cafeddd4`.
`execution.v1.json` records the exact two inner commands, source identities,
acquisition hashes, timestamps and results. They were:

| Command | Elapsed seconds | Exit |
| --- | ---: | ---: |
| `python -m ges.claim_review` with the retained artifact metadata and fresh snapshots | 8.801 | 0 |
| `python -m ges.claim_reconciliation` with the same inputs and no receipt envelopes or receipt-authority policy | 10.926 | 0 |

`claim-provenance.json` and `reconciliation-without-envelopes.json` are exact copies
of the commands' stdout. Both repository input closures are retained without
rewriting their paths or contents. The execution's source hash maps show continuity
from acquisition verification through the beginning and end of claim replay.

The distinct current reviewer `/root/migration_review` completed 2,855 explicit
post-run checks in 1.023263 seconds. Its retained script independently reconstructed
every current claim subject and all three canonical digests, checked exact current
document membership and hashes, recomputed source identity projections, hashed the
retained source files and repository inputs, and verified recorded hash continuity.
The exact reviewer script is retained in `independent-replay-check.py.gz`; its decompressed SHA-256 is the script hash in the review. It observed regular files without symlink components at review time. It did not
repeat acquisition or decompress all source bodies.

The original v1 driver uses assertions for some outer guards and did not record its
optimization mode. Its hash helper also did not reject symlinks. The independent
post-run checker uses explicit conditions and documents what it actually checked;
it does not invent historical process flags or file-type observations. Content and
claim-span verification inside the reviewed repository modules use explicit
exceptions. No unexecuted hardened successor driver is substituted for v1.

The v1 field `historical_validated_dispositions_preserved: 2164` is a reference to
prior historical accounting. **The source-replay driver did not revalidate those
historical decisions.** The separately recorded replacement-decision comparison
must be used for any preservation claim about the prepared ledger.

## Workload migration and replacement decisions

The historical report remains byte-preserved at its original 61,936 claims in 654
documents. The separate current inventory contains 61,941 claims in 655 documents.
The historical/current workflow and tests check both states; the A3 continuity
repair does not merely replace expected counts. Removing exactly the five approved
successor subjects reproduces the historical universe digest
`9e4116b7a70772c94f59e1f5b1a27b1a736c15a8cae78341586a12bf8f80bd0d`.

A separate, nonissued replacement package passed independent comparison against
every one of the 2,164 historical subjects and decisions plus the ten specified new
dispositions. The actual reviewer completed 144,504 explicit mechanical checks in
1.619496 seconds, with zero carried-field mismatches, missing rows, extra rows or
duplicates. All 19,476 preserved top-level field comparisons matched, including
every subject, disposition, rationale, detail, control reference, unchanged
catalog/proposal binding and nonadoption boundary.

The same distinct reviewer separately read the authenticated WA source context
and exact catalog/proposal records, and favorably reviewed all ten new dispositions.
Those authored semantic findings are recorded in `independent-decision-review.json`;
the check count does not represent automated semantic judgment. The proposed
controls remain non-adopted and quarantined, without verified operational bindings.

The reviewed draft has SHA-256
`a8b9065b0a5a43e950451683badcbeaa335cc344bbce78940dac4420fb6d7185`
and canonical digest
`010aa6e9003301d96825cb1f34b317bafb401783e9f7462c40ac1c7d05bbb8e6`.
Its exact scope is five predecessor supersessions and five successor specializations:
five logical repairs, five added raw records and ten additional dispositions. All
draft actor and issuance-time fields remain null. Preparation and comparison do
not themselves issue an envelope or add current validated reconciliation credit.

The existing owner grant names the original Codex root and its original
`finishline_gates` reviewer. The actual current cloud actors are different. The
current branch/cloud-work approvals do not supply a retained grant naming these
replacement roles. No identity was substituted, no approval reference was
manufactured and no timestamp was backdated. The original authorization and
envelopes remain unchanged. A concrete current-role request is prepared separately
and binds the complete reviewed decision package. Any later issued envelopes must
be independently compared with that package under authentic authority and actual
current timestamps; the earlier draft-review time cannot be reused for a later
envelope review.

The conditional result after authentic scoped issuance, independent envelope
review and successful full accounting remains 61,941 known claims, 2,174 validated
dispositions and 59,767 unresolved claims. That is not the result of the retained
envelope-free command, and reconciliation would still be partial.

## Execution location and historical-cache limits

Mac admission governs processes running on the Mac. This replay ran on the
independent Linux cloud executor with a 300-second deadline, a forced-kill grace
period and explicit address-space, CPU, file-size and descriptor limits. A tiny
TERM-ignoring-child test demonstrated deadline enforcement; its retained receipt
records a 0.402-second duration and exit -9. The test's exact UTC was not recorded.
No heavy Mac lease or Limen remote-broker admission is claimed for this execution.

The original native transfer and existing private ciphertext are separate recovery
routes. The attempted native pre-transfer stat failed at 20:14:51 UTC because the
device was offline. No source bytes were read. The existing 1,204,940,832-byte
private ciphertext exceeded the Drive connector's 268,435,456-byte whole-file limit;
that call returned HTTP 413 and no bytes. No range route was exposed. The exact
download-call timestamp was not captured; its failure receipt was recorded by
20:11:00.228826 UTC. These observations are documented in `cloud-routing.json`.

The successful fresh replay does not establish original-cache restoration,
byte-for-byte preservation of the complete frozen A3 capsule, or authentication of
the historical rendered-body cache. Source-to-claim omission completeness,
remaining adapters and synthesis, the complete public disposable pilot, publication
clearance, human review, owner acceptance and merged-main checks remain separate.
Private pilot support remains unverified.

## Retention and restart

This directory contains original execution outputs, their independent audit and
metadata only. Raw source bodies and nonissued decision drafts remain in private
working storage. `manifest.json` lists the public files and their SHA-256 values.

To inspect the executed revision, use a separate checkout at `6c37fe5`. The v1
driver is an exact execution record, including its original cache paths and
revision guard. Do not run it over an existing cache or change its bytes and then
claim to have repeated the same execution. For a new replay, use a fresh isolated
directory, preserve the locked inputs, assign a new execution record and bounded
deadline, and independently compare its actual outputs.

Before issuing replacement envelopes, authenticate the retained private package
against its recorded digest, obtain the exact current-role grant, preserve every
carried decision, use actual current reconciler/reviewer timestamps, and rerun
`ges.claim_reconciliation` against the authenticated inputs with both the real
policy and real receipts. Record the actual result, including the complete
denominator. Do not use the conditional arithmetic as a substitute.
