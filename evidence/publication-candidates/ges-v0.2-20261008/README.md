# Exact GES v0.2 candidate: initial publication-use inventory

**Status: inventoried, all use classifications unreviewed, clearance unknown.**

This draft binds all **2,379 tracked files / 128,548,510 bytes** in candidate
commit [`db7517449f5c11750ca55dfeccc47167c10c3fb4`](https://github.com/4444J99/github-engineering-standards/commit/db7517449f5c11750ca55dfeccc47167c10c3fb4),
tree `b2f57e6181c6973bf5f529d2bff9469e34572c30`. The complete repository at that
revision is the proposed `GES_V0_2` output scope. No subset is represented as
the complete release. These later review-input files are retained outside the
exact candidate to avoid a self-referential file inventory.

| File | Meaning |
|---|---|
| `manifest.json` | Exact complete candidate file set, byte sizes and SHA256 values. |
| `register.json` | Every output has an explicit `UNREVIEWED` disposition. The empty use list is unfinished classification, not a finding of zero upstream expression. |
| `policy.json` | Empty pending separately authorized, exact-scope review policy. |
| `receipts.json` | Empty; no reviewer, human acceptor or distribution approval is fabricated. |
| `accounting.json` | Actual validator result for these bytes and inputs. Clearance is `null`, and `zero_use_clearance` is false. |
| `recovery-status.json` | Recovery actually invokes the publication validator on this candidate. All four milestones and all nine legacy gates remain open. |
| `scope.json` | Candidate identity, file bindings and limitations for this observation. |

The validator observed the complete declared output set and **2,379 unreviewed
outputs**. The number of actual upstream uses is not certified. The declared
use denominator of zero must not be reported as 100% coverage or approved zero
use. Use classifications, exact copied/adapted spans, necessary pinned source
evidence, attribution decisions, omission review, approved authority and human
distribution/acceptance evidence still need to be supplied.

## Reproduce the draft's blocked result

Use a clean, dedicated candidate directory. The following exports only tracked
files from the immutable candidate commit and decompresses the committed public
artifact metadata. The publication command is expected to exit **1** with
valid accounting and unknown clearance. Exit 1 here is the intended blocked
release result.

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

Any change to candidate output bytes requires a new candidate identity and
manifest, newly bound classifications and applicable approvals. Updating these
review inputs does not authorize release or policy adoption. Human authenticity
and policy custody retain the external trust requirements documented in
[`docs/publication-use-register.md`](../../../docs/publication-use-register.md).
