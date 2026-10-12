# Claim workload audit

The historical audit's 61,936 denominator counts recorded source-reference claims, not
61,936 distinct obligations. The audit preserves every occurrence and leaves
the unique actionable-obligation count unknown. Its frozen reconciliation input
records 474 / 61,936; this audit grants no gate closure or new review credit.
This is the 654-document `*-claims.json` lane, including 222 legacy community
claims. The separately reviewed 227-proposition B0/C0 community ledger retains
its own accounting and is not added to, removed from or re-reviewed here.

The October 12 successor migration adds a separately reproduced current report:
61,941 recorded claims in 655 documents, still 4,651 advisory families. The five
predecessors remain in the historical and current inventories. This is five added
records, not five new validated dispositions; see the migration section below.

| Historical records | Occurrences | Advisory review families |
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

Three committed reports retain distinct provenance:

| Report | Input and scope |
|---|---|
| `evidence/claim-workload-inventory.json` | Historical report bound to the original private artifact inventory. Original-input replay was **UNAVAILABLE** in its preservation observation. Existing review and source-table receipts retain this report's unchanged hash. |
| `evidence/claim-workload-current-inventory.json` | October 7 workflow metadata, preserved under `evidence/claim-workload-inputs/`, applied to the frozen 654-document membership. Its existing name and bytes remain unchanged. |
| `evidence/v02-workload-migration-20261012/current-inventory.json` | The same preserved workflow metadata with the complete current 655-document claim membership, including the five approved successor records. |

The October 7 report preserves every historical field except
`inputs.artifacts_sha256`. No report grants additional review credit.
The Toolkit validation workflow now requires both frozen-membership reproduction
with that strict historical equivalence and full-current reproduction with an
exact approved migration, for both supported Python versions. Run the same command
locally:

```sh
python -m ges.claim_workload_migration --reviews evidence/source-reviews --artifacts evidence/claim-workload-inputs/artifacts.jsonl.gz --reconciliation evidence/provider-oidc-reconciliation.json --baseline evidence/claim-workload-current-inventory.json --current evidence/v02-workload-migration-20261012/current-inventory.json --historical evidence/claim-workload-inventory.json --provenance evidence/claim-workload-current-provenance.json --approval evidence/v02-finish-20261010/claim-migration-audit.json
```

The gzip input contains only artifact metadata from workflow run
[37571019639](https://github.com/4444J99/github-engineering-standards/actions/runs/37571019639),
artifact `11460399285`. Its decompressed SHA256 is
`86225491fb70197b893a0bfb1fa96ebfc1f5a6e33c21c86ab874d9d34f5db9a2`.
The downloaded ZIP matched GitHub's recorded SHA256
`33456e7d2d64f24eae94a4331603fe4aa48e6c36f8d4265148ffcda17f3bdf70`.
The preserved October 7 [provenance record](../evidence/claim-workload-current-provenance.json)
binds both report files, the compressed and decompressed metadata, the source
identity reference, acquisition timestamps and the observed workflow origin.
This was the October 7 acquisition observation; it did not restore the original cache.

The preserved-state check requires the input's exact decompressed SHA256 and
reproduces the October 7 report byte for byte from its own recorded document
membership. It then requires every historical
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

The original artifact SHA256 recorded as unavailable in that observation remains
`d53ff71f62a5facec4c60f94ec66c967861e79f46f0af5bbb606654d5d47c87c`.
Bounded recovery inspected all October 1 workflow runs and the available
October 1 and October 7 metadata archives. Neither contained those exact bytes.
The two available inventories have the same 13,657 pinned artifact identities;
their acquisition timestamps and 653 proposed-disposition classifications
differ. Both reproduce all historical workload fields except the input hash.
No timestamps or source metadata were inferred or rewritten to simulate recovery.
This does not prove the original bytes are absent from every external location.

On October 12, a bounded read of the retained native cache located both original
artifact inventories with exactly that SHA256, and the v2 frozen capsule manifest
with its expected `0a177df2…1d83` fingerprint. These new observations do not rewrite
the historical provenance file. Full source authentication and provenance replay
remain blocked by native heavy-work admission.

### Exact successor migration

The migration checker pins the unchanged historical report, October 7 report,
October 7 provenance, and October 10 independent migration audit in reviewed code.
A changed report cannot authorize itself by rebinding neighboring hashes. Before
decompression, the compressed artifact input must match the pinned provenance.
The original A3 source-identity validation remains mandatory.

For the preserved reproduction, every recorded document must have its original
canonical filename, exact byte hash, and claim count. Current reproduction always
enumerates the complete `*-claims.json` set. That set must equal the historical
membership plus `wa-application-security-correction-01-claims.json`, with exactly
its independently reviewed SHA256 and the five approved predecessor/successor
pairs. All original claims, artifact and receipt inputs, and family memberships
must be preserved. Both reproductions and a final combined input-stability check
must pass; the CLI offers no subset-only mode.

| Metadata workload measure | Frozen membership | Current membership |
|---|---:|---:|
| Recorded claims | 61,936 | 61,941 |
| Claim documents | 654 | 655 |
| Advisory families | 4,651 | 4,651 |
| Records in the frozen provider/OIDC receipt input | 474 | 474 |
| Claims without a record in that specific input | 61,462 | 61,467 |
| New review or reconciliation credit | 0 | 0 |

The 474-record input here is `provider-oidc-reconciliation.json`. It is distinct
from the later 2,164-disposition validated ledger. The proposed ten replacement
dispositions and conditional 2,174 / 59,767 accounting require authenticated source
replay, authentic current role authority, actual envelope issuance, and independent
decision comparison. No migration check certifies those decisions.

The existing `ges.claim_workload --check` command still enumerates the full current
set and rejects the old 654-document report. Historical equivalence still permits
only the artifact-input hash difference; it rejects the 655-document state. A
future legitimate claim addition requires a separately reviewed migration scope.
See [execution and review evidence](../evidence/v02-workload-migration-20261012/README.md).

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
