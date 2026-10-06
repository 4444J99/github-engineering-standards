# A5 semantic contracts

The five closed JSON Schemas under `schemas/semantics/` describe source charters,
exact source occurrences, deduplicated propositions, reconciliation decisions,
and separate policy decisions. These are interface definitions; A5 does not
populate the corpus, authorize reviewers, certify meaning, or adopt controls.

`python -m ges semantics validate --input records.jsonl` validates required
fields, types, digests, identity, spans, and review-reference structure. Empty
ledgers and duplicate identities fail. Records may contain review references;
this command does not authenticate those references or approve their judgments.
The validator implements the closed vocabulary used in these schemas rather
than being a general JSON Schema engine.

Canonical encoding uses sorted object keys, UTF-8, compact JSON separators,
preserved array order, and finite JSON values. IDs use the kind plus a full
SHA-256 digest. Occurrence IDs bind the complete source locator, commit, content
digest, span, and span digest. Proposition IDs bind the complete semantic AST,
including qualifiers and exceptions. Other IDs bind every field except `id`.
Revised formalizations retain occurrence identity; revised meaning changes
proposition identity. JSON strings are preserved byte-for-byte, without Unicode
normalization. Arrays must be supplied in canonical producer order.

Conditions and applicability are preserved as ordered expressions in v1;
parsing and executing those expressions belongs to the Docs resolver tranche.
Source text remains in the pinned cache. Records carry locators, digests, and
independently authored formalizations.

`extract` remains reserved and returns exit 2 with `UNAVAILABLE`. A6 implements
`reconcile` and `audit` with explicit proposition inputs; see
[reconciliation machinery](reconciliation-machinery.md). Calling these commands
without inputs retains the reserved-interface response. Validation returns exit
0 only for structural validity; malformed input returns exit 2.

A3 supplies the capsule and A4 supplies reviewed source charters later. Their
absence does not prevent this independent interface tranche from being reviewed.
