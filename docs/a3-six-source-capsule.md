# A3 frozen six-source inputs

`evidence/a3-six-source-capsule-repair.json` supersedes the historical
`evidence/a3-six-source-capsule.json` receipt for current validation. It records the independently tracked capsule
fingerprint, member digests, six source-tree matches, structured-input digests,
and rendered acquisition identities. It contains no raw upstream text.

The freeze uses the current six source pins. An isolated ledger rebuild restored
61,801 dependencies after a corpus rebuild had emptied `dependencies.jsonl`.
The source inventories, candidate ledger, and published-page ledger are unchanged.

Run the receipt tool from the repository root:

```sh
python -m scripts.a3_tree_evidence --capsule CAPSULE --output NEW_TREE_EVIDENCE
python -m scripts.a3_capsule_receipt --capsule CAPSULE --capsule-sha256 TRUSTED_SHA --expected-structured-count 605 --tree-evidence NEW_TREE_EVIDENCE --sources SOURCES --corpus CORPUS --rendered RENDERED --output NEW_RECEIPT
```
It validates capsule members, tree parity, supplement counts, and every cached
rendered body before writing the receipt. Compare regenerated receipt bytes to
the tracked receipt; changed inputs require a new capsule and receipt revision.

The required `--expected-structured-count` is an independently supplied assertion
from the reviewed A3 baseline, not a value read from the supplement directory.
It rejects consistent removal of structured rows and summary counts. Supplement
bytes remain bound by the tracked receipt digests rather than the capsule.

The source lock's historical `git_tree_reconciled: false` flags describe its
initial acquisition state. Historical frozen tree reports are not pin-bound proof.
The repair captures fresh GitHub commit/tree API observations, checks each exact
commit and inventory, and binds their bytes in the repaired receipt. These are
reviewable API observations, not signed third-party attestations.

Every gzip row must match its frozen source, commit, path, size, content digest
and Git blob digest; text coverage must be complete and unique. Structured rows
must have unique identities, matching provenance and exact source spans. Page
matches must reference appropriate frozen Docs paths. Rendered validation holds
the acquisition writer lock and rejects an index that changes between reads.
Other input changes between reads are detected, but arbitrary concurrent writers
are not locked: keep the input capsule and supplements immutable during replay.
Checkout retention is unknown, not manufactured from a successful replay.

The receipt binds 13,657 artifacts, 150,903 candidate blocks, 18,019 page
applications, and 605 structured occurrences. Fourteen page-source mappings
remain unresolved. Rendered bodies were acquired from published Docs and are
not thereby assured to match the pinned source commit. Semantic interpretation
belongs to later tranches. Source charters belong to A4.

The metadata capsule and raw caches are retained locally; independent remote
custody and restoration remain unverified. The Git receipt preserves identities
but cannot substitute for the capsule payload. No acquisition or review gate is
closed merely by publishing this receipt.
