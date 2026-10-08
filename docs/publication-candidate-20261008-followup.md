# Publication candidate follow-up — 2026-10-08

This dated note carries the current clarification of the
[frozen candidate README](../evidence/publication-candidates/ges-v0.2-20261008/README.md)
and its [historical scope record](../evidence/publication-candidates/ges-v0.2-20261008/scope.json).
The scope record binds the README as well as the six other evidence files.
The README has been restored to its exact bytes at `dc799db`, with SHA256
`7ee71ce970ab3534bcf0c132ce3d31084eff1d112467b78f83a6447d3a2e4a75`.
All seven file bindings in the unchanged scope record match. Later context and
replay observations belong outside those bound historical files.

**Status: historical parent inventory; all use classifications unreviewed,
clearance unknown.**

The frozen draft binds all **2,379 tracked files / 128,548,510 bytes** in candidate
commit [`db7517449f5c11750ca55dfeccc47167c10c3fb4`](https://github.com/4444J99/github-engineering-standards/commit/db7517449f5c11750ca55dfeccc47167c10c3fb4),
tree `b2f57e6181c6973bf5f529d2bff9469e34572c30`. The complete repository at that
revision is the frozen `GES_V0_2` output scope. No subset is represented as
the complete release. The candidate review-input files were added in PR #494's
reviewed head `dc799dbb62b6bb698cae1390aed30fb0c32a4249` and sit outside the
exact candidate to avoid a self-referential file inventory.

This manifest covers only `db751744`; it does not inventory the current PR
head or an eventual merge commit. PR #494 is the sole merge candidate, with
#492 and #493 retained as integration ancestry and excluded from separate
merges. The implementation merge is not the release candidate described here.
After the accounting fixes, release requires a newly selected exact candidate,
a complete new inventory, reviewed classifications and newly bound applicable
approvals. The seven files bound by the historical scope record retain their
original bytes.

The following records remain under
`evidence/publication-candidates/ges-v0.2-20261008/`.

| File | Meaning |
|---|---|
| `manifest.json` | Exact complete candidate file set, byte sizes and SHA256 values. |
| `register.json` | Every output has an explicit `UNREVIEWED` disposition. The empty use list is unfinished classification, not a finding of zero upstream expression. |
| `policy.json` | Empty pending separately authorized, exact-scope review policy. |
| `receipts.json` | Empty; no reviewer, human acceptor or distribution approval is fabricated. |
| `accounting.json` | Historical validator result for these bytes and inputs from the implementation staged at `dc799db`. Clearance is `null`, and `zero_use_clearance` is false. |
| `recovery-status.json` | Historical recovery invocation of the publication validator on this candidate. All four milestones and all nine legacy gates remain open. |
| `scope.json` | Candidate identity, file bindings and limitations for this observation. |

The original validator observed the complete declared output set and
**2,379 unreviewed outputs**. The number of actual upstream uses is not
certified. The declared use denominator of zero must not be reported as 100%
coverage or approved zero use. Use classifications, exact copied/adapted spans,
necessary pinned source
evidence, attribution decisions, omission review, approved authority and human
distribution/acceptance evidence still need to be supplied.

The adversarial review of `dc799db` found that a fabricated artifact row could
pass with only a matching source pin, and that preparing draft metadata inside
an output root invalidated its own inventory. Those defects prevent a
fail-closed claim for the original implementation. The saved unknown-clearance
result is preserved; it does not certify the validator's resistance to either
counterexample or validate their repairs.

## Replay the frozen draft's blocked result

Run from the repository root, using a clean, dedicated candidate directory.
The following exports only tracked files from the immutable candidate commit
and decompresses the committed public artifact metadata. The publication command
is expected to exit **1** with
valid accounting and unknown clearance. Exit 1 here is the intended blocked
release result. Record the implementation revision used for a replay separately
from the frozen candidate revision. The saved `accounting.json` records the
original observation and must not be overwritten to imply a new run.

```sh
mkdir -p .cache/publication/ges-v0.2-20261008/candidate
git archive db7517449f5c11750ca55dfeccc47167c10c3fb4 \
  | tar -x -C .cache/publication/ges-v0.2-20261008/candidate
gzip -dc evidence/claim-workload-inputs/artifacts.jsonl.gz \
  > .cache/publication/ges-v0.2-20261008/artifacts.jsonl
python3 -m ges.publication_use \
  --manifest evidence/publication-candidates/ges-v0.2-20261008/manifest.json \
  --register evidence/publication-candidates/ges-v0.2-20261008/register.json \
  --receipts evidence/publication-candidates/ges-v0.2-20261008/receipts.json \
  --policy evidence/publication-candidates/ges-v0.2-20261008/policy.json \
  --artifacts .cache/publication/ges-v0.2-20261008/artifacts.jsonl \
  --output-root .cache/publication/ges-v0.2-20261008/candidate \
  --source-root .cache/publication/ges-v0.2-20261008/source-evidence
```

This initial register declares no classified uses, so no source-body record is
read from the final path. Once actual-use rows are added, their necessary source
bytes must be supplied and must match the locked identities; empty source
evidence cannot clear those rows. The supplied `accounting.json` is an output,
not an authority input. Recovery recomputes it from manifest, register, policy,
receipts, source metadata and the actual candidate files.

The corrected validator also authenticates the complete source inventory
against the independently trusted reference and binds
`source_inventory_reference_digest` into its accounting subject. With the
repository's six-source lock, the default A3 reference supplies that anchor;
the command above needs no alternate-reference flags. A replay with the
corrected validator therefore has additional provenance binding and need not
be byte-identical to the saved historical `accounting.json`. Store new replay
outputs outside both the frozen candidate and these historical JSON records.

Any change to candidate output bytes requires a new candidate identity and
manifest, newly bound classifications and applicable approvals, including the
current source-inventory reference binding. Updating these review inputs does
not authorize release or policy adoption. Human authenticity and policy custody
retain the external trust requirements documented in
[`publication-use-register.md`](publication-use-register.md).
