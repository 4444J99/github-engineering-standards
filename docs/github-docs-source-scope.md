# GitHub Docs source scope

The owner requested GitHub Docs after the Well-Architected and four-source splits.
This split uses the existing snapshot at
`56fcfa816f27bca239e5d39fff0d4f74f77ec995`. Its complete inventory is **13,219
files**, not 13,219 independently authored policy documents. The separate published
ledger contains **18,019 page/version instances**; neither number is silently
replaced by the smaller synthesis queue.

Start with **3,698 authored product-documentation files**, then follow their
reusables, conditional data, illustrations and generated references. There are
**9,116 substantive content/reference files** when the shared passages and
reference data are included. This is a 31.0% reduction from the indiscriminate
13,219-file synthesis queue, not a claim of 31.0% less work or completed review.
The article starting queue is smaller, but its dependencies remain required.

| Role | Files | Existing artifact receipts | Existing authored text claims |
|---|---:|---:|---:|
| Authored product documentation | 3,698 | 362 | 10,848 |
| Shared reusable content | 3,409 | 2,396 | 12,103 |
| Substantive reference data | 2,009 | 13 | 31,483 |
| Applicability and variable data | 319 | 316 | 2,275 |
| Interpretation dependencies | 684 | 28 | 261 |
| Illustration dependencies | 1,787 | 2 | 0 |
| Explicit synthetic fixtures | 384 | 0 | 0 |
| Source contract tests | 333 | 5 | 24 |
| Contributor/site context | 116 | 1 | 7 |
| Website infrastructure | 478 | 3 | 22 |
| Rights metadata | 2 | 2 | 44 |
| **Total** | **13,219** | **3,128** | **57,067** |

The [per-file routing](../evidence/semantics/source-scope/github__docs.json)
retains every artifact ID, pinned content digest, role, existing receipt and
claim-document reference. Referenced evidence files have a digest-bound index.
The substantive roles retain **54,434 of the 57,067 existing text claims (95.4%)**;
the other 2,633 claims remain available in supporting roles. These are existing
authored claims indexed by source path, not newly audited semantic truths.
No path-local text claim is required for a file to matter: screenshots and
generated inputs can contribute meaning without having extracted prose claims.
The two already reviewed SDK diagrams separately retain **27 existing visual
observations** and their independent asset audit, with both companion files
bound in the evidence index. Those observations are not added to the text-claim
total and were not re-reviewed by this routing change.

## What must remain in synthesis

All product domains remain in scope, including billing, identity, Copilot,
security, administration and site policies. Article and index frontmatter retains
permissions, product/plan/version, platform/tool, layout, redirects and navigation
context. `content/contributing/` is upstream contribution context, rather than
general requirements imposed on repository consumers. The three content README
files explain authoring or generation and remain interpretation dependencies.

The 3,409 reusable passages are substantive. Review a shared passage once for its
source meaning, then preserve each consuming article's conditions; an include is
not permission to erase a caveat. Features and variables remain necessary to
resolve availability and rendered terminology. Reference tables, the customer
glossary and actual GHES release notes remain substantive inputs. The explicitly
dated-2099 release-note placeholder template remains contributor context, with its
warnings retained; it is not evidence of an actual release.

Most files under the following `src/` data directories are generated documentation,
not site implementation to discard:

| Generated reference family | Files, including its conventions README where present |
|---|---:|
| REST | 513 |
| GraphQL | 338 |
| Webhooks | 995 |
| GitHub App/PAT permissions | 57 |
| Audit logs | 23 |
| Secret-scanning patterns | 13 |

The GraphQL data README is retained as an interpretation dependency; the other
1,938 files in these families are substantive reference data. Preserve FPT,
GHEC, GHES release and REST calendar-version distinctions. Generated schemas,
permission tables and webhook payloads can supply material absent from Markdown.
Their generators/renderers and version mapping remain linked interpretation
inputs. No live schema refresh or upstream build/install/sync script was run.

The 1,787 illustration dependencies include screenshots, diagrams and example
CSVs. They have **not** been declared decorative or newly visually reviewed.
Explicit fixture payload paths and `_fixtures` assets take precedence over
mirrored content/data names; synthetic pages and schemas are not independent
platform documentation. The `src/fixtures` subject's own tests, helpers and
conventions remain tests or interpretation dependencies, rather than payloads.
Tests retain source contracts, without proving live enforcement.

## Use existing work before reviewing new material

There are **3,128 existing artifact receipts**, leaving **10,091 files without an
artifact receipt**. The 9,116 substantive files contain 2,771 existing receipts;
6,345 of those files lack receipts. Routing does not certify receipt quality or
independent omission completeness, and a claim document does not substitute for
a full-artifact review receipt.

Reuse the completed bounded Actions pilot and prior source reviews. For the
next genuinely unreviewed article, trace its exact reusable/feature/variable and
generated-data dependencies, retain source spans and limitations, and reconcile
the resulting claims. Supporting code is reopened for a concrete dependency;
it is not independently mined for universal policies merely because it is in the
source archive. This prevents restarting source extraction across site plumbing.

This change adds **zero artifact reviews, zero claim reviews, zero reconciled
claims and zero adopted controls**. The six-source denominator remains 13,657,
and all nine acceptance gates remain open. Routing grants no rights clearance,
whole-source completeness or native/estate acceptance. It changes where synthesis
starts and what must be followed, without changing acceptance accounting.

The classification follows the pinned [content conventions](https://github.com/github/docs/blob/56fcfa816f27bca239e5d39fff0d4f74f77ec995/content/README.md),
[data conventions](https://github.com/github/docs/blob/56fcfa816f27bca239e5d39fff0d4f74f77ec995/data/README.md),
[subject-folder explanation](https://github.com/github/docs/blob/56fcfa816f27bca239e5d39fff0d4f74f77ec995/src/README.md)
and the REST, GraphQL and Webhooks subject explanations in that same snapshot.
