# Claim workload audit

The committed audit's 61,936 denominator counts recorded source-reference claims, not
61,936 distinct obligations. The audit preserves every occurrence and leaves
the unique actionable-obligation count unknown. Its frozen reconciliation input
records 474 / 61,936; this audit grants no gate closure or new review credit.
This is the 654-document `*-claims.json` lane, including 222 legacy community
claims. The separately reviewed 227-proposition B0/C0 community ledger retains
its own accounting and is not added to, removed from or re-reviewed here.

| Existing records | Occurrences | Advisory review families |
|---|---:|---:|
| Secret-scanning provider capability fields | 31,456 | 556 raw provider/credential identity families |
| CodeQL query-table fields with row identities | 3,638 | 544 exact query-row families |
| Remaining source-reference claims | 26,842 | 3,551 source-artifact contexts |
| Total | 61,936 | 4,651 |

The provider fields come from 5,132 dataset rows across product-version paths.
They include public/private support, push protection, validity checks, base64,
extended metadata and duplicate markers. Different versions, duplicate rows,
missing fields and differing flags remain separate evidence. The query rows
retain their source occurrence and exact query-help identity. A family is a
work packet, not an accepted requirement, equivalence class or safe exclusion.

Exact statement text has 59,395 distinct hashes and 2,541 repeated occurrences.
Exact source spans number 50,680, with 11,256 repeated span occurrences.
Neither shared text nor shared spans establishes semantic duplication: distinct
conditions, subjects and claims can occupy the same span. Deduplicating strings
alone offers limited relief and cannot substantiate a smaller obligation count.

## Execution change

Process provider and query metadata as source-bound matrices. Validate each
existing cell against the pinned source data and retain all occurrence IDs,
version predicates, absent fields and differences. Review the governing
capability/coverage decisions separately from these reference facts. A source
table fact does not need an invented independent policy control.

Use the remaining artifact-context families to review original bodies and
necessary literal dependencies together. Separate requirements, procedures,
examples, metadata, navigation and caveats through actual reading; existing
source-strength labels are observations, not an automatic exclusion rule.
Cross-source semantic relations need accountable decisions and independent
review. Candidate grouping does not provide those decisions.

The queue is disjoint and complete for the currently recorded claims. Workers
receive exact family/member identities and digest-bound documents; dispatch
must preserve source context and the existing 250-proposition review cap,
splitting oversized families without losing context. Run disjoint primary
reviews in parallel within admitted resource limits, then independent audits;
a single integrator updates canonical decisions and accounting. Do not launch
unadmitted cloud workers. This audit itself dispatches no semantic workers.

Measure throughput by new independently reviewed substantive propositions and
verified matrix cells separately. Report source omission coverage separately:
unextracted or genuinely unreviewed source material is outside this claim
inventory's completeness claim. The 4,651 packets are not a prediction of
review hours or a claim that all remaining source review has been enumerated.

## Reproduction

Two committed reports retain distinct provenance:

| Report | Input and scope |
|---|---|
| `evidence/claim-workload-inventory.json` | Historical report bound to the original private artifact inventory. Original-input byte replay is **UNAVAILABLE**. Existing review and source-table receipts retain this report's unchanged hash. |
| `evidence/claim-workload-current-inventory.json` | Newly observed October 7 workflow metadata, preserved under `evidence/claim-workload-inputs/`. This report can be reproduced locally without network access. |

The current report preserves every historical field except
`inputs.artifacts_sha256`. Neither report grants additional review credit.
The Toolkit validation workflow requires exact current-report reproduction and
historical accounting equivalence on every push and pull request, for both
supported Python versions. Run the same command locally:

```sh
python -m ges.claim_workload --reviews evidence/source-reviews --artifacts evidence/claim-workload-inputs/artifacts.jsonl.gz --reconciliation evidence/provider-oidc-reconciliation.json --check evidence/claim-workload-current-inventory.json --historical evidence/claim-workload-inventory.json --provenance evidence/claim-workload-current-provenance.json
```

The gzip input contains only artifact metadata from workflow run
[37571019639](https://github.com/4444J99/github-engineering-standards/actions/runs/37571019639),
artifact `11460399285`. Its decompressed SHA256 is
`86225491fb70197b893a0bfb1fa96ebfc1f5a6e33c21c86ab874d9d34f5db9a2`.
The downloaded ZIP matched GitHub's recorded SHA256
`33456e7d2d64f24eae94a4331603fe4aa48e6c36f8d4265148ffcda17f3bdf70`.
The new [provenance record](../evidence/claim-workload-current-provenance.json)
binds both report files, the compressed and decompressed metadata, the source
identity reference, acquisition timestamps and the observed workflow origin.
This is a new acquisition observation; it does not restore the original cache.

The check first requires the current input's exact decompressed SHA256 and
reproduces the current report byte for byte. It then requires every historical
report field to match except the artifact input hash. Changes to denominators,
memberships, document hashes, reconciliation bindings, JSON types or credit
fields fail. Provenance validation preserves the historical report's exact byte
hash, requires exact metadata fields and canonical values, and recomputes all six
complete pinned source memberships against the independently fingerprinted A3
receipt. URLs must be derived from the authenticated source, pin and path;
IDs, digests, enums, integer bounds and acquisition timestamps have closed
contracts. Duplicate JSON keys, optional gzip text/header fields and extra gzip
members are rejected. The A3 fingerprint comes from the reviewed validator
code shared with publication accounting, rather than the mutable provenance
record. Counts, pins and identity digests must all match. Missing, stale or changing inputs
produce a nonzero exit. CI reads committed local bytes; it does not download,
rewrite, accept or certify evidence.

The unavailable original artifact SHA256 remains
`d53ff71f62a5facec4c60f94ec66c967861e79f46f0af5bbb606654d5d47c87c`.
Bounded recovery inspected all October 1 workflow runs and the available
October 1 and October 7 metadata archives. Neither contained those exact bytes.
The two available inventories have the same 13,657 pinned artifact identities;
their acquisition timestamps and 653 proposed-disposition classifications
differ. Both reproduce all historical workload fields except the input hash.
No timestamps or source metadata were inferred or rewritten to simulate recovery.
This does not prove the original bytes are absent from every external location.

To propose a new report, write a separate output for review:

```sh
python -m ges.claim_workload --reviews evidence/source-reviews --artifacts evidence/claim-workload-inputs/artifacts.jsonl.gz --reconciliation evidence/provider-oidc-reconciliation.json --output .cache/claim-workload.json
```

The output directory must exist and the output file must not already exist.
`--artifacts` also accepts the original uncompressed `.cache/corpus/artifacts.jsonl`.
Regeneration and independent review of changed inputs and accounting remain
explicit work; `--check` cannot provide that approval. Changes to actual
accounting require a separately scoped revision; the historical-equivalence
check must not be silently broadened to admit them.

The audit checks unique claim identities,
artifact/receipt source bindings, input hashes and document membership stability.
Provider row identities comprise source, commit, path and entry ordinal; all
fields in one row must agree on provider, exact raw credential identifier and
definition span. Distinct raw identifiers remain separate families when they
belong to distinct rows. Either query-row metadata key requires both keys with
a valid source occurrence and nonempty query-help identity. A claim cannot
silently mix provider and query classifications.

It records typed metadata without verifying the underlying source values,
authority, semantic fidelity, adoption, rights or native behavior. Those remain
the responsibility of their existing validators and actual reviewers.
