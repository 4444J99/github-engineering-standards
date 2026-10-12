# Recovery integration after authorized reconciliation

**Staged recovery repair.** The missing candidate-ledger dependency is resolved.
The actual full `ges.recovery` execution completed successfully in the independent
Linux cloud workspace and incorporated the unchanged, previously authorized and
independently reviewed reconciliation receipts.

This adds recovery integration and an early input check. It does not issue new
receipts, increase semantic-review credit, accept controls, authorize publication,
complete the pilot, merge the PR stack or establish v0.2 acceptance.

## Actual result

The final reviewed-code recovery command exited **0 in 32.009 seconds**. Its
input closure and driver bytes remained unchanged. The executed code is bound by
the recorded `code/*` hashes; the record labels the checkout revision as a base
revision and explicitly records the staged preflight edit. This avoids attributing
modified code to an unchanged parent commit.

| Measure | Observed result |
|---|---:|
| Known source claims | 61,941 |
| Validated reconciliation dispositions | 2,174 |
| Unresolved claims | 59,767 |
| Artifact disposition receipts | 3,590 / 13,657 |
| Artifacts without disposition receipts | 10,067 |
| Candidate blocks | 150,903 |
| Structured occurrences | 605 |
| Structured occurrences certified by supplied receipts | 0 |
| Published page applications | 18,019 |
| Original unresolved page-source mappings | 14 |
| Accepted canonical controls | 0 / 95 |

The reconciliation disposition counts remain MAP 382, SPECIALIZE 57, CONFLICT 3,
REFERENCE 1,721 and EXCLUDED_WITH_REASON 11. The final receipts retain byte digest
`b4147bf94b13d18188b7acc775c1f7508f1653f2737bcecc7f27920afe58b73f`
and canonical digest
`9085ac042ae2b951aa582b390faf36e78380d8108199de1c4073e84557a17e8f`.
No reconciler/reviewer identity or timestamp was substituted.

The actual report retains `mapping_complete=false` and all nine legacy gates
remain open. Six-source synthesis is `INCOMPLETE`; exact-use public clearance and
native pilot acceptance are `UNVERIFIED`. The GES v0.2 result is `INCOMPLETE`.
Estate rollout remains separately `UNVERIFIED` and does not block that aggregate.
A zero exit from this reporting command means a valid report was produced; it
does not mean the reported acceptance gates passed.

## How the missing metadata was recovered

The initial source-only cache was sufficient for claim provenance but lacked the
complete corpus required by recovery. Existing GitHub workflow artifacts supplied
the missing metadata without any new upstream source acquisition or live page-list
fetch. `historical-reconstruction.json` records exact provenance and hashes.

| Corpus member | Recovery method | Independent A3 byte identity |
|---|---|---|
| Candidate ledger | Unchanged October 1 artifact member | Exact match |
| Published-page ledger | Unchanged October 1 artifact member | Exact match |
| Dependency ledger | Reorder two intact source groups; preserve every row byte | Exact match |
| Ledger summary | Recompute one historical reference count from the exact A3 catalog | Exact match |
| Structured requirements | Unchanged October 12 artifact member | Exact match |

The source workflow artifacts are run
[`36920555495`](https://github.com/4444J99/github-engineering-standards/actions/runs/36920555495),
artifact `11191578546`, and run
[`38313171881`](https://github.com/4444J99/github-engineering-standards/actions/runs/38313171881),
artifact `11775861352`. Both downloaded ZIP digests were authenticated before
member use. `reconstruct-historical-corpus.py` retains the executed reconstruction
logic and rejects any mismatch against the independently recorded A3 digests.

The dependency reconstruction changes only source-group ordering: 61,800 Docs
rows followed by one GHQR row. The summary reconstructs the A3 catalog's 31
referenced artifacts from historical commit
`e848c9a4f0fb9499c957ad3185ee99061fd57f8d`; its prior artifact recorded 30. All
other summary values remain unchanged. The current catalog references 35
artifacts, so the frozen summary's 31 is historical metadata, not a current count.

The assembled recovery corpus uses the preserved October 7 artifact metadata
already consumed by successful #506/#507 accounting. Its byte SHA-256 is
`86225491fb70197b893a0bfb1fa96ebfc1f5a6e33c21c86ab874d9d34f5db9a2`.
These are not the original A3 artifact bytes. Their complete stable source identity
projection matches the independent A3 reference. The 23 retained October 12 source
files match the previously executed cloud replay hashes. A distinct agent also
decompressed and authenticated all 11,828 text artifacts across the 13,657 source
identities. The original acquisition timestamps are preserved.

## Repair and verification

`ges.recovery` now checks all five required corpus files and each locked source's
inventory/tree files before loading large candidate and review inputs. Source
snapshots are required when claim documents need them. Missing or nonregular
files produce one actionable error describing the incomplete cache. No empty
ledger is manufactured, and the existing provenance and gate validators remain
responsible for interpreting and validating the bytes.

Independent review caught an initial Darwin compatibility regression in the new
check. The final implementation reuses the existing `canonical_path` policy:
trusted system aliases retain their existing ownership/target validation, while
caller-created symlinks remain rejected. Focused tests cover this distinction,
missing corpus files, nonregular paths, source-only caches, snapshot requirements
and optional argument-pair errors.

The full suite passed **721 tests**. Catalog validation passed for **95 controls**;
compilation, generated-view parity and whitespace verification passed. The separate
`ges.claim_review` command and full recovery execution have their own actual
records. `verification.json`, the independent software review and the independent
recovery review distinguish these executions from historical and remote CI runs.

`run-recovery.py` records the actual command, times, exit status, output hashes,
driver continuity and the complete supplied source/corpus/code/review/control/
template/profile/supporting-evidence closure. It uses a 150-second deadline and
bounded Linux process resources. The raw inputs remain private and are preserved
as a restart package; the public tranche contains code and metadata only.

## Remaining scope

Five exact corpus members are recovered, but the complete original A3 capsule,
its original inventory/artifact bytes and the historical rendered-body cache have
not been restored. No historical rendered bodies were supplied to this execution;
the resulting zero acquired-body count describes this run's inputs and does not
erase the separate historical acquisition record.

The remaining 59,767 claim dispositions, 10,067 artifact receipt gaps, independent
source-to-claim omission review, 605 structured-occurrence certifications,
generalization/adoption/binding/native adapters, full public pilot behavior matrix,
exact-use publication decisions and final release inventory remain substantive
work. The two existing JSON-expression rights decisions remain on HOLD.

The original scoped authorization remains intact. Human code review, applicable
security review, governed merging of #496 -> #497 -> #503 -> #506 -> #507,
merged-main checks and owner acceptance remain required. This tranche resolves
the concrete missing-ledger/recovery integration failure; it does not redefine
the repository's `Verified` designation.
