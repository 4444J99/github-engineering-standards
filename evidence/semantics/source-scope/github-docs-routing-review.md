# Bounded GitHub Docs routing review

Result: **PASS for file-role routing**, with one evidence-link correction resolved.
This is agent primary and independent review, not human approval or a new full
source semantic/visual review.

Primary writer: Codex native session `01a11342-68e2-7851-9636-9af99289c0d7`.
Independent reviewer: existing agent `/root/bounded_independent_review`, read-only.
Base: merged main `28587d052265fd2061c526846dbf05ff172bcb06`.
Source: `github/docs` at `56fcfa816f27bca239e5d39fff0d4f74f77ec995`.

## Reviewed bytes and bounded checks

| Artifact | SHA-256 |
|---|---|
| `github__docs.json` | `c4f65a6a36ab3b509126d58d0fb1e4f14ef9d0060bbb20089a6fcf49802308b2` |
| `docs/github-docs-source-scope.md` | `002610ab6590bc93b39ee46955849e5c34758ef22f8351f87315d9178913cf06` |

The independent reviewer checked all 13,219 unique artifact IDs, paths, pins,
kinds and content digests against the existing corpus inventory, hashed all
11,418 cached text bodies, and recomputed every role, receipt and text-claim count.
The final 1,020 evidence-file hashes and 6,269 entry references match. The primary
writer performed the same inventory/text/evidence checks and checked the guide's
eleven table rows against the final manifest. The existing cached tree/archive
reconciliation is MATCH at 13,219/13,219, without missing/extra/blob mismatches.
No new live upstream tree or schema fetch was performed.

Role review retained the REST, GraphQL, Webhooks, GitHub App/PAT, audit-log and
secret-pattern production reference data. All product-content frontmatter remains
in scope; 3,409 reusable passages and 319 applicability-data files are retained.
Explicit payload fixtures (384) are distinguished from source tests (333) and
interpretation dependencies (684). The 1,787 illustrations were not declared
decorative. No upstream code was executed and no underlying corpus review was
restarted.

## Concrete corrections

The primary pass separated the fixture subject's own tests/helpers/conventions
from its synthetic payloads, and retained the explicitly dated-2099 release-note
placeholder as contributor context rather than an actual release reference.

Independent review found that the SDK diagrams' receipt links did not directly
bind their companion observations and independent audit into the evidence index.
The correction adds those companion references and hashes to both image entries,
retaining 14 + 13 = 27 existing visual observations separately from text claims.
The independent correction recheck passed with no remaining concrete findings.

## Repository checks and accounting boundary

Observed checks on this branch:

- `python3 -m unittest discover -s tests -v`: 485 tests passed.
- `python3 -m ges validate`: 95 controls valid.
- `python3 -m ges compile`: exit 0.
- `git diff --exit-code -- generated`: exit 0, unchanged generated outputs.
- `python3 -m ges.bounded_review --check`: existing 227/227 source propositions
  and classifications reviewed, zero adopted controls.
- `git diff --check`: exit 0.

The 3,128 existing receipts, 57,067 existing authored text claims and 27 existing
asset observations are retained. The 9,116 substantive files retain 54,434 text
claims. There are zero newly reviewed artifacts or claims, zero new reconciled
claims, and no adopted controls, rights clearance, whole-source completeness or
closed acceptance gates. The global 13,657-file and published 18,019-page/version
denominators remain unchanged. Retain this implementation checkout for the PR.
