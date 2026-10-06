# A3 frozen six-source inputs

`evidence/a3-six-source-capsule.json` records the independently tracked capsule
fingerprint, member digests, six source-tree matches, structured-input digests,
and rendered acquisition identities. It contains no raw upstream text.

The freeze uses the current six source pins. An isolated ledger rebuild restored
61,801 dependencies after a corpus rebuild had emptied `dependencies.jsonl`.
The source inventories, candidate ledger, and published-page ledger are unchanged.

Run the receipt tool from the repository root with `python -m
scripts.a3_capsule_receipt --capsule CAPSULE --capsule-sha256 TRUSTED_SHA
--sources SOURCES --corpus CORPUS --rendered RENDERED --output NEW_RECEIPT`.
It validates capsule members, tree parity, supplement counts, and every cached
rendered body before writing the receipt. Compare regenerated receipt bytes to
the tracked receipt; changed inputs require a new capsule and receipt revision.

The receipt binds 13,657 artifacts, 150,903 candidate blocks, 18,019 page
applications, and 605 structured occurrences. Fourteen page-source mappings
remain unresolved. Rendered bodies were acquired from published Docs and are
not thereby assured to match the pinned source commit. Semantic interpretation
belongs to later tranches. Source charters belong to A4.

The metadata capsule and raw caches are retained locally; independent remote
custody and restoration remain unverified. The Git receipt preserves identities
but cannot substitute for the capsule payload. No acquisition or review gate is
closed merely by publishing this receipt.
