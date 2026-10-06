# Claim reconciliation receipts

`ges.claim_reconciliation` validates explicit, independently reviewed dispositions
for the exact claims already accepted by `ges.claim_review`'s provenance checks. It
does not infer mappings from text, identifiers, keywords or substring matches, and it
does not generate reconciliation receipts.

The adapter first reruns source-claim provenance validation against the locked source
pins, artifact inventory, source snapshots, source-review policy and known control
identities. Each known claim is then represented by an exact subject containing:

- `claim_id`, `source`, `commit` and `path`;
- `artifact_id` and the artifact `content_sha256`;
- exact `start_line` and `end_line`;
- `statement_sha256`;
- the relative `claim_document` name and its byte `claim_document_sha256`.

The canonical digest of the sorted subject set is `claim_input_digest`. Catalog and
proposal arrays are separately bound as `catalog_digest` and `proposal_digest` using
`ges.core.digest`. Changed claims, claim documents, catalog revisions or proposal
revisions require new receipts and renewed authority binding.

## Authority policy

Supplied receipts require a separately approved policy with exactly these fields:

- `schema: "ges.claim-reconciliation-policy.v1"`;
- a nonempty external `approval_reference`;
- exact `claim_input_digest`, `catalog_digest` and `proposal_digest`;
- nonempty unique `authorized_reconcilers` and
  `authorized_independent_reviewers` identity arrays.

The policy is a trusted authority input. JSON cannot authenticate a person or prove
that the approval reference is adequate. A reconciler and independent reviewer must
be distinct on every receipt. Source-review permission alone grants neither role.

Omitting both certification inputs returns zero validated claims and the exact input
digests so an authority policy can be prepared outside this tool. A paired empty
receipt array still requires a valid bound policy. Neither mode reports completion.

## Receipt contract

Each receipt uses schema `ges.claim-reconciliation-receipt.v1` and binds the exact
claim subject and all three input digests. It also records a nonempty `rationale`, an
authorized `reconciler`, a distinct authorized `independent_reviewer`, ordered
timezone-bearing `reconciled_at` and `reviewed_at` timestamps, and the literal
nonadoption boundary `accepted_policy: false` plus `adopted_obligation: null`.
Future, naive, pre-source-review or out-of-order timestamps are rejected.

`control_references` is an array of exact `{id, revision, collection}` objects.
`collection` is `CATALOG` or `PROPOSAL`; the ID and revision must exist in that exact
input collection. Multiple distinct control references are supported. Unknown IDs,
stale revisions, duplicate references and an ID present in both collections fail.

The disposition and its exact `details` contract are:

| Disposition | Control references | Required details |
|---|---|---|
| `MAP` | One or more canonical catalog controls | Empty object. |
| `SPECIALIZE` | One or more references, including a proposal | Nonempty `scope` and `distinction`. |
| `CONFLICT` | Zero or more | Nonempty known `conflicting_claim_ids` excluding the subject itself, plus a nonempty `resolution`. |
| `REFERENCE` | None | Nonempty `reference_reason`. |
| `EXCLUDED_WITH_REASON` | None | Supported `basis`, nonempty `exclusion_reason`, and `related_claim_ids`. `DUPLICATE` and `SUPERSEDED` require at least one known related claim; other bases forbid invented relations. |

Supported exclusion bases are `NON_ACTIONABLE`, `DUPLICATE`, `OUT_OF_SCOPE`,
`SUPERSEDED` and `UNSUPPORTED_SOURCE`. `DEFER`, fuzzy output, free-form mapping text,
unknown fields and truthy strings do not count as completed reconciliation.

## Accounting and limits

The deterministic result reports the known-claim denominator, validated and
unresolved counts, counts for every supported disposition, sorted validated claim
IDs, all input/receipt/policy digests, and `mapping_complete`. That flag is true only
when one valid receipt exists for every known claim. A partial receipt set remains
partial and retains the complete denominator.

Even a full receipt set keeps these boundaries explicit:

- semantic truth is not automatically certified;
- the source-to-claim omission denominator is not certified;
- rights are not cleared;
- policy is not adopted.

This adapter alone cannot close the consolidation gate. Independent source-to-claim
omission evidence, conflict/generalization review, adoption decisions, operational
bindings and the other acceptance gates remain separate.

Heuristic suggestions and intermediate model output belong only in ignored `.cache`
workspace paths. They must never be placed in `evidence/`, described as receipts, or
counted until accountable reviewers produce contract-valid records. No populated
authority policy or real reconciliation receipt is shipped by this tranche.

Standalone validation:

```sh
python -m ges.claim_reconciliation \
  --artifacts .cache/corpus/artifacts.jsonl \
  --sources .cache/sources \
  --reviews evidence/source-reviews \
  --review-policy evidence/source-review-policy.json \
  --receipts RECEIPTS.json \
  --policy POLICY.json
```

Valid inputs return exit `0`. Any malformed, foreign, stale, unauthorized or
unsupported supplied input returns exit `2` and a JSON error report. Omit both
`--receipts` and `--policy` for accounting-only output; supplying only one is invalid.
