# Structured-occurrence reconciliation receipts v1

Reference accounting remains unchanged and cannot claim consolidation. The optional
recovery pair `--structured-reconciliation` / `--structured-reconciliation-policy`
requires source review and claim-reconciliation receipt/policy inputs. It consumes
underlying records, never an alleged completed accounting report.

The adapter re-extracts the complete structured set from the pinned GHQR definition
and Well-Architected checklist artifacts using the same extractor as the ledger.
Missing/duplicate/altered rows fail. Source hashes and actual pin identities must
match the corpus; missing source artifacts fail. All claim documents are revalidated
through the existing claim-reconciliation validator. Associations are derived from
every current claim document, including additive successors and retained predecessors.
All associated claims must have validated dispositions before an operative occurrence
can count. Nothing erases duplicate source occurrences or collapses caveats.

The exact policy fields are `schema` (`ges.structured-reconciliation-policy.v1`),
`approval_reference`, `subject`, `authorized_reviewers`, and
`authorized_independent_reviewers`. The subject returned by the adapter binds the
complete structured ledger, artifact bytes, source snapshots, claim documents,
associations, current claim input, catalog, proposals, claim receipts and authority.
The policy must be genuinely approved outside the validator. It cannot authorize
known quarantined heuristic identities.

Receipts are an array of exact-field objects:

- `schema`: `ges.structured-reconciliation-receipt.v1`.
- `subject`: exact `occurrence` row, sorted complete `claim_ids`, and the policy's
  full `inputs` subject.
- `disposition`: `CLAIMS_RECONCILED` when associations exist; otherwise `NONOPERATIVE`.
- `rationale`: accountable, nonempty justification. An unassociated occurrence is
  not automatically nonoperative: both review and independent evidence are required.
- `reviewer`, `independent_reviewer`, `reviewed_at`, `audited_at`.
- `evidence`: exactly `review` and `independent_audit`, each a relative evidence
  JSON `path` plus raw `sha256`.

Each evidence document has exactly `schema`
(`ges.structured-reconciliation-evidence.v1`), `kind`, `identity`, `subject`,
`disposition`, `reviewed_at`, `outcome` (`PASS`), `unresolved` (empty array), and
`observations` (1–100 distinct nonempty strings, each <=4,000 characters).
Evidence must match the receipt exactly, be <=1 MB, and be inside the evidence
root without symlinks or traversal. Inputs and evidence are reread before success.

The independent reviewer must differ from the occurrence reviewer, associated
claim authors, and associated claim reconcilers. Review must follow all linked
claim reviews; audit follows review; no timestamps may be future or naive.

Absent evidence remains unknown. Empty/partial supplied evidence retains the full
denominator and is incomplete. A zero denominator stays undefined. Complete validated
occurrence receipts close only the structured prerequisite; unstructured omission,
semantic truth, adoption, rights, native behavior and human acceptance remain separate.
Synthetic fixtures in tests are not actual receipts or authority grants.
