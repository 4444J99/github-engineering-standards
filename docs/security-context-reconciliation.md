# Secret-scanning and CodeQL reconciliation

Primary and independent reviewers adjudicated all 1,392 selected contextual claims,
retaining the exact pinned original statements and source identities. The scope is
source paths containing `secret-scanning` or `codeql` in the non-table queue, not
complete capability-corpus closure. The six packets retain whole source context;
their sizes are 249, 247, 218, 218, 240 and 220.

| New reviewed relations | Secret-scanning | CodeQL | Total |
|---|---:|---:|---:|
| Existing draft-control mapping | 14 | 1 | 15 |
| Source-specific reference | 697 | 675 | 1,372 |
| Unsupported-source exclusion | 3 | 2 | 5 |
| All selected decisions | 714 | 678 | 1,392 |

The [independent review](../evidence/security-context-independent-review.json)
binds the exact [secret-scanning primary](../evidence/secret-context-primary-review.json)
and [CodeQL primary](../evidence/codeql-context-primary-review.json) decisions,
original source hashes and prior evidence. Primary reports retain their historical
pending-independent status; the subsequent independent report supplies the verdict.
The [combined receipt ledger](../evidence/security-context-reconciliation.json)
preserves all 474 earlier decisions unchanged and appends these 1,392 decisions:
1,866 independently reviewed relations out of 61,936 recorded claims.

## Corrected classifications and retained gaps

Five historical extracted assertions remain source-fidelity FAIL. Their original
bytes are preserved; each is excluded with `UNSUPPORTED_SOURCE` and a narrower
corrected interpretation in its rationale. These are resolved classification
decisions, with zero faithful-extraction or control credit:

- `DOCS-SECRET-REF-CONT-103`: issuer-reporting prose does not establish the claimed REST filter predicate.
- `DOCS-SECRET-PROVIDER-RENDER-0262`: a reported PR number does not prove a newly created PR.
- `DOCS-SECRET-PROVIDER-RENDER-0278`: enumerating main-content headings does not test visibility.
- `DOCS-CODESCANOPS-0057`: a conditional direction to consult newer documentation is not a mandatory requirement.
- `DOCS-CODESCANOPS-0006`: ability to analyze/display results does not prove analysis or display occurred.

Thus 1,387 selected assertions passed source-fidelity review; five did not.
Consolidation accounting must not be presented as 1,392 faithful extractions.
The original claim-input digest, catalog revisions and proposal digest remain
unchanged. No historical claim rewrite or universal control is inferred.

Secret response mappings preserve rotation/revocation and investigation; deleting
text, closing an alert, bypassing protection or notifying a provider cannot establish
incident resolution. Custom-pattern preparation retains sample/false-positive
limits and retesting after edits. Bypass evidence, exceptions and logging mappings
retain their narrow source purpose and the catalog's additional local conditions.

CodeQL language-list synchronization maps to GES-DOC-004 r1. Source Code Quality
metadata stays reference data, with exact language/query/category/severity retained.
Source bundle sharing is not broadened into a large-artifact storage control.
Private synchronization destinations and actual synchronization remain unverified.
Security suite membership, Autofix support and GHES release prose do not establish
installed versions, successful analysis, a correct fix or live entitlement.

## Acceptance accounting

The prior 35,094 verified table facts and 28 governing interpretations are reused
without new credit. The 382 Code Quality metadata records reviewed here are separate
from that earlier security-table proof. They are metadata, not 382 adopted obligations.

The 26,842 non-table records now have 1,866 reviewed relations and 24,976 remaining
without reconciliation. The full legacy unresolved count is 60,070, including
35,094 table records whose separate literal-source verification does not supply
legacy policy reconciliation receipts. Neither denominator is a count of distinct
standards. Distinct actionable obligations remain uncertified.

Legacy artifact accounting remains 3,590 / 13,657, accepted controls remain zero,
and all nine project gates remain OPEN. This batch grants no new artifact-omission,
rendered-page, publication-rights, target-behavior or organization-acceptance credit.
The [recovery report](../evidence/recovery-status.json) uses the combined receipt
ledger and its scoped authority policy. Earlier workload/table reports retain their
historical reconciliation-input bindings; they do not silently become new reviews.

Unreviewed query-help predicates, outbound help/licence/procedure bodies, private
synchronization inputs, screenshots and runtime rendering/execution dependencies
remain explicit in the primary reports. No whole-source or live-platform certification
is inferred from inspected code or fixtures.

## Reproduction and remaining work

Use the original private cache for this worktree. With `GES_PRIVATE_CACHE` pointing
to that cache, run these existing validators from the repository root:

```sh
python -m ges.claim_reconciliation --artifacts "$GES_PRIVATE_CACHE/corpus/artifacts.jsonl" --sources "$GES_PRIVATE_CACHE/sources" --reviews evidence/source-reviews --review-policy evidence/source-review-policy.json --receipts evidence/security-context-reconciliation.json --policy evidence/security-context-reconciliation-policy.json
python -m ges.recovery --sources "$GES_PRIVATE_CACHE/sources" --corpus "$GES_PRIVATE_CACHE/corpus" --reviews evidence/source-reviews --review-policy evidence/source-review-policy.json --rendered-directory "$GES_PRIVATE_CACHE/rendered-docs" --claim-reconciliation evidence/security-context-reconciliation.json --claim-reconciliation-policy evidence/security-context-reconciliation-policy.json --output .cache/security-context-recovery.json
```

Continue with unresolved source-artifact contexts and their interpretation dependencies,
preserving table facts as reference data. Prioritize source obligations, caveats and
operational relationships rather than inventing one policy per metadata cell. Separate
source-omission review and unresolved query-help semantics remain necessary before
complete six-source synthesis can be accepted. Issue #471 owns the remaining work;
this checkout and the original private sources are retained.
