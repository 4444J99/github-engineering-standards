# Pinned source-table validation

The full provider/CodeQL table workload now has a reproducible literal-source
check. All 35,094 recorded table claims match 35,094 source facts, with no missing
or extra fact subjects within the 22 selected source tables. The results are in
[source-table verification](../evidence/source-table-verification.json), with
every matched claim ID retained and the complete workload bound by digest.

| Exact source-data scope | Verified facts | Original rows |
|---|---:|---:|
| Provider capability fields across 12 product/version paths | 31,456 | 5,132 |
| CodeQL cells across 10 language tables | 3,638 | 544 |

The provider scope retains 608 Liquid-valued fields,30,848 literal boolean fields
and 4,468 absent optional field positions. Absence is not recorded as false.
All 527 rows explicitly marked `isduplicate: true` remain in the matrix; the
marker is not a deletion instruction. Product paths, raw identifiers, row
ordinals and field lines stay separate. No conditional expression is executed
or rendered by this check. CWE identities retain their leading zeros, query
help URLs remain distinct, and exact column/header meanings are checked.

[The governing review](source-table-governing-review.md) contains 28 primary
interpretation propositions across 33 pinned source files. Its independent
review is recorded separately in
[the independent report](../evidence/source-table-independent-review.json).
The primary's pending-independent status records its historical production
stage; use the independently bound report for the subsequent review verdict.

## Findings and scope qualifications

Existing `isPublic`/`isPrivateWithGhas` claim labels are legacy public/private
wording. The pinned renderer presents Partner and User alert columns. This
batch supplies an exact-source glossary and discrepancy decision, rather than
claiming the legacy wording proves repository coverage. The pinned subject
README describes older renderer behavior; the actual pinned page/component
and middleware establish the matrix interpretation.

Liquid values and absent fields stay distinct from request-context UI boolean
values. CodeQL suite membership and Autofix flags do not establish installed
queries, entitlement, successful execution or remediation. GHES bundle/version
and Autofix feature gates qualify the raw table facts. Display names and URL
suffixes do not establish actual query severity metadata. Governing source
propositions carry the necessary source spans and dependency qualifications.

## Accounting and next work

Report 35,094 /35,094 mechanically verified table facts separately from the 28
governing interpretations and existing reconciliation. The existing legacy
reconciliation remains 474 /61,936; accepted controls remain zero. This delivery
adds no legacy gate credit, control adoption, rights clearance or live native
behavior evidence. No raw upstream bodies are published.

The 26,842 non-table recorded claims are in 3,551 source-artifact context packets.
Existing 474 reconciliation decisions remain; 26,368 records currently lack
reconciliation. Preserve the existing decisions and review unresolved contextual
claims, alongside separate source-omission work. Retain these verified table
facts as reference data and review their governing rules when mapping policy;
do not assign every table cell an invented independent obligation. Source
omissions, rendered-page assurance and individual query-help semantics remain
separate work. This check covers the selected tables, not the entire source
corpus or all possible upstream table fields.

## Reproduction

Run from the repository root with the original private corpus/snapshot paths
and a new output path. The existing output must not be overwritten:

```sh
python -m ges.source_tables --reviews evidence/source-reviews --artifacts .cache/corpus/artifacts.jsonl --reconciliation evidence/provider-oidc-reconciliation.json --workload evidence/claim-workload-inventory.json --snapshots .cache/sources/github__docs.text.jsonl.gz --lock sources/sources.lock.json --output .cache/source-table-verification.json
```

A source fact mismatch, duplicate subject or omitted fact is reported and exits 1.
Invalid input bindings, unknown structures, conflicting icons or input mutation
fail before producing passing evidence. The report is deterministic and binds
the full workload, lock and snapshot. Full reconciliation authority/disposition
validation remains in the existing reconciliation contract.
