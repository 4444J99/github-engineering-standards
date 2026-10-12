# Five-successor workload migration — staged evidence

This repair preserves the historical workload while adding an independently
checked current inventory for the five already approved WA successors. It is a
bounded metadata migration on PR #497, based on
`afdd2ffe03bd840516947a9256ff9aea380335fb`, and remains dependent on PR #496.
GES v0.2 remains **Staged and unfinished**.

## Defect and repair

Toolkit push run [38081454423](https://github.com/4444J99/github-engineering-standards/actions/runs/38081454423)
at the parent revision ran 692 tests with one workload-integrity error. The test
compared the full current claim directory with a preserved 654-document report.
Five successors in one new document made that comparison correctly reject
changed membership, counts, families and inputs. Later workload and governance
steps were skipped. The separate source-acquisition run
[38081456873](https://github.com/4444J99/github-engineering-standards/actions/runs/38081456873)
succeeded at that parent revision; it does not establish this repair's CI status
or authenticated current reconciliation.

The repair makes historical membership explicit with `--recorded-membership`
and keeps the original full-directory behavior as the default. Both preserved
reports, their provenance, artifact metadata, A3 reference and workload receipts
remain byte unchanged. A new `claim-workload-v02-inventory.json` records complete
current membership. A separately pinned transition contract requires exactly
the approved successor document and five predecessor/successor pairs. It rejects
unrelated additions, changed old bytes, changed receipt or family membership,
unsafe paths, symlinks, stale bindings and inputs changed during either replay.

The updated real-data tests and Toolkit workflow require both historical
preservation and complete current reproduction. No full-suite or downstream CI
step has been disabled. The generated inventory is 4,651 advisory families;
families provide workload grouping, not semantic acceptance or deduplication.

## Actual metadata accounting

| Measure | Preserved baseline | Independently checked current metadata |
|---|---:|---:|
| Recorded claims | 61,936 | 61,941 |
| Claim documents | 654 | 655 |
| Advisory families | 4,651 | 4,651 |
| Frozen workload receipt subjects | 474 | 474 |
| Records without a workload receipt | 61,462 | 61,467 |
| New review credit | 0 | 0 |
| New reconciliation credit | 0 | 0 |

The added document is
`evidence/source-reviews/wa-application-security-correction-01-claims.json`.
It adds `WA-APPSEC-005-CORRECTION-01`, `009-CORRECTION-01`,
`011-CORRECTION-01`, `017-CORRECTION-01` and `018-CORRECTION-01`, each retaining
its full `WA-APPSEC-` prefix and linking to the corresponding preserved
predecessor. All five join the existing artifact-context family.

These 474 workload subjects are a separate input from the broader historical
ledger's 2,164 validated dispositions. The conditional broader expectation of
2,174 dispositions and 59,767 unresolved claims remains **unexecuted**. This
repair provides no new semantic decision, envelope or reconciliation credit.

## Verification actually performed

The original native checkout was clean at the parent revision before this
repair. The integrator used Python 3.14.8 and a granted isolated execution lease.
Every native source file matched the independently reviewed implementation
fingerprints before the focused tests ran.

| Check | Actual outcome |
|---|---|
| Generate separate current inventory from retained artifact metadata | Exit 0; 1.774 seconds |
| Independently authored metadata audit, root executed | PASS; 1.091 seconds |
| `python -m unittest discover -s tests -p 'test_claim_workload*.py' -v` | 51 tests, all passed; subprocess 3.486 seconds |
| Preserved workload reproduction with `--recorded-membership` | Exit 0, `MATCH`; 1.319 seconds |
| Complete current workload transition | Exit 0, `MATCH`; 1.993 seconds |
| `git diff --check` before evidence closeout | Exit 0 |

[verification-execution.json](verification-execution.json) contains the exact
native interpreter, argument arrays, working directory, timestamps, return
codes and complete stdout/stderr. The two workload CLI commands are also in
[the workload audit](../../docs/claim-workload-audit.md).

The independent audit checked every one of the 655 document hashes, all 61,941
unique IDs, every family and count field, all 474 frozen receipt subjects, the
exact five successor pairs, historical byte preservation and input stability.
Its [preserved script](independent_metadata_audit.py) does not import the GES
workload implementation or read retained raw source bodies. It must be run with
ordinary Python; optimized mode is explicitly rejected.

[metadata-review-execution.json](metadata-review-execution.json) records the
root-executed audit at `2026-10-12T19:14:46.431519+00:00`.
[independent-review.json](independent-review.json) records the actual
`/root/accounting_review` agent's subsequent review of its complete output and
exact software files at `2026-10-12T19:15:54.156565+00:00`. The execution record's
`PENDING` field is preserved as its execution-time observation; the later review
supplies that output review without rewriting history. This is agent software
and metadata review, not human review or original semantic-envelope authority.

## Admission and finite continuation

[host-observation.json](host-observation.json) preserves the actual deployed
Limen admission responses. Heavy acquisition at 3:20 p.m. EDT on October 12
was denied for `swap-fraction`: 11,739,070,464 swap bytes on a 17,179,869,184-byte
physical-memory host, with vitals action `throttle`. An isolated writer lease
was allowed. No heavy lease was acquired, no full source replay was launched,
and full-suite/native governance verification remained blocked.

Terminal transport lost its live session handles during this work. Completed
metadata results were recovered from files. Own idle REPLs were closed through
their already registered deadline handlers; canonical admission cleanup reaped
dead own leases. Replacement scoped leases retained the same tranche start
(`19:08:19Z`) and deadline (`19:37:19Z`), rather than resetting elapsed work.
Historical cumulative usage remains **UNKNOWN_NOT_RESET**. Recorded native
metadata command/audit durations total approximately 9.68 seconds; this is not
the session's total wall time. No other process, host threshold or peer lease
was changed to obtain admission.

The metadata driver's child verification commands all completed successfully.
Its later lease-release call supplied `lease_id` positionally, although the
deployed API requires that argument by keyword. No successful driver cleanup
receipt was recorded, and no clean overall driver exit is claimed. This does
not change the already captured child return codes. The publication update
on [PR #497](https://github.com/4444J99/github-engineering-standards/pull/497)
records the final scoped lease outcome separately.

## Input fingerprints

| Artifact | SHA-256 |
|---|---|
| Historical inventory | `6151dcc71dda756610f371337bebe9981c0f9656cc6f7b252ad60e007701f5ec` |
| Preserved October 7 inventory | `2e718486119b29cf286f4b21f067d67dc3bea17f2559a45fbc01105931a22658` |
| Preserved provenance | `239fc3e89643202c9a7935749249eb4a0ca14e67a32c6e2a0517166a81e9bbf8` |
| Compressed metadata input | `9bf57e2bdf62d37026d5c06981c34e2c9db593e44bf03f39c7e441c9751358ac` |
| Decompressed metadata input | `86225491fb70197b893a0bfb1fa96ebfc1f5a6e33c21c86ab874d9d34f5db9a2` |
| Frozen workload receipts | `91f52141398c7670bd4e3335b5dad89c88815c3141c75d6007fc52a674e54485` |
| Approved successor document | `3830522db4425a0e7e267479fff32b00cc12541b36bfacd01033faa009df2589` |
| New current inventory | `ed4ee7e8be9a5369d4651769dc8717456473063d2db21010544349a9848b8a00` |
| Pinned transition contract | `f92cbe31c618e793b9bdc07f51b609d0b464fa5f8698fe715efc6bb542089dd8` |

Current claim-membership digest:
`c23a807acdb2e2972b07c4bb8d96e07c93d7478aa577e9e5835170db083459fb`.
Neither the preserved metadata nor this digest restores the unavailable
original artifact cache or authenticates the underlying source bodies.

## Remaining sequence

Obtain actual heavy admission, authenticate retained inputs and replay complete
claim provenance with the actual denominator and fresh input digests. Recheck
the preserved/current workload transition against those inputs. Replacement
envelopes then require the original authorized actors or an authentic renewed
grant covering current actors, plus independent comparison of every carried
decision and all ten new dispositions. Do not substitute identities or backdate.
Only then record current reconciliation and recovery accounting.

Remaining adapters and synthesis, retained-body authentication, complete public
disposable pilot evidence, final publication clearance, human code/security
review, owner acceptance and merged-main checks remain open. The approved
[implementation plan](../../.codex/plans/2026-10-10-finish-ges-v02.md) governs;
private support remains unverified. This metadata repair closes no v0.2
acceptance gate and changes no protection, visibility, pilot state or release.
