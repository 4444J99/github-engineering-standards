# Bounded publication primary review

Status: **Staged**, primary review by `codex:/root/publication_worker_c`.
This packet reviews the 50 frozen lexical proposal assignments against the
actual `f628db26cee1e6fc8fcc5ad5513959de0401d73d` candidate. It supplies proposed
use rows for reconciliation and independent omission review, not an approved
register, inventory attestation, publication receipt or distribution decision.

`primary-review.json` binds the assignment, original candidate packet, retained
source cache and pinned source identities. Each selected proposal's title,
objective and first acceptance item has an exact JSON pointer and source/output
byte range. Direct source-block comparisons cover short titles below the original
detector threshold. Every selected source is a GHQR definition; no selected YAML
block contains a separate component notice. The Microsoft MIT license is present
verbatim in the frozen candidate's `THIRD_PARTY_NOTICES.md`, with its precise
notice span bound in every proposed expressive use.

The proposed classifications are 148 raw-identical `LICENSED_COPY` rows and 50
`REFERENCES_ONLY` source URLs. Two more expression rows, GES-OPS-008 objective
and acceptance, remain unresolved: JSON escapes preserve the decoded wording but
break the validator's raw-byte equality requirement for `LICENSED_COPY`. Encoding
alone does not justify inventing an `ADAPTATION` judgment. The `kind: null` rows
are deliberately unresolved proposed evidence and cannot enter a valid use register.

The reviewer inspected the selected source recommendation contexts and remaining
proposal fields, including generic acceptance boilerplate and source metadata.
No identified additional GHQR expression in those generic fields is recorded;
their independent authorship and whole-proposal clearance are not certified.
Shared metadata and generic wording remain subject to omission review.

All **2,396 candidate files remain UNREVIEWED**. Coverage is 50 of 593 proposals,
including 50 of 543 with detected matches; 543 proposals remain outside this
packet, including 493 detected-match proposals. Candidate bytes, original
register, empty policy/receipts and historical packets remain unchanged. All
human, independent review and distribution approvals remain outstanding.

Replay the direct byte observations from this worktree root:

```sh
env PYTHONPATH=. python evidence/wave-20261009/publication/replay.py /path/to/authenticated/sources
```

Observed exit 0, 50 proposals/150 expression fields, with all cache, source,
candidate and source-block membership assertions passing. The replay writes no
raw upstream text. The existing triage span parser locates original JSON bytes;
it does not reserialize the candidate.

`accounting-replay.json` comes from the actual `ges.publication_use` validator,
using the untouched original candidate manifest/register/policy/receipts, the
conductor's exact tracked-blob export, retained authenticated source cache and
decompressed authenticated artifact inventory. Observed exit **1**, valid but
uncleared, complete 2,396-file inventory and 2,396 unreviewed outputs. The initial
invocation incorrectly supplied unsupported `--output`; argparse interpreted it
as `--output-root`, yielding exit 2 (`Missing output directory`). The corrected
invocation used stdout redirection and produced the preserved actual result.
This validator replay does not validate or approve the proposed partial use rows.

Unit tests, catalog validation and compilation are owned by the sole integrator;
this lane changes no catalog, shared receipts, policies or generated views.
