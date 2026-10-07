# Claim workload audit

The current 61,936 denominator counts recorded source-reference claims, not
61,936 distinct obligations. The audit preserves every occurrence and leaves
the unique actionable-obligation count unknown. Reconciliation remains
474 / 61,936; no gate or review numerator changes through this audit.
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

Run from the repository root against the original private corpus inventory:

```sh
python -m ges.claim_workload --reviews evidence/source-reviews --artifacts .cache/corpus/artifacts.jsonl --reconciliation evidence/provider-oidc-reconciliation.json --output .cache/claim-workload.json
```

The output must not already exist. The audit checks unique claim identities,
artifact/receipt source bindings, input hashes and document membership stability.
It records typed metadata without verifying the underlying source values,
authority, semantic fidelity, adoption, rights or native behavior. Those remain
the responsibility of their existing validators and actual reviewers.
