# C0 — Community reconciliation

This is a **HOLD staging deliverable**, stacked on B0 PR #479 at
`5f2f3b8d4141a8e1be1e6aac0e002378f46c6fa2`. The user's instruction to proceed
authorizes this preparation; it does not constitute approval of the 207 B0
propositions or independent review of C0. B0's residual obligations remain B0's.

The immutable input manifest binds the full B0 proposition/occurrence ledgers,
annotations, input manifest and receipt. C0's authored annotations classify every
one of the 207 propositions and record explicit reciprocal relationships.
The compiler performs structural validation and deterministic projection only;
it contains no keyword or similarity-based semantic classifier.

| Source relationship | Propositions | Meaning |
| --- | ---: | --- |
| DISTINCT | 45 | Retained independently; no equivalent or successor asserted within this batch. |
| SPECIALIZED | 128 | Related source-specific variants, with differences retained. No directional subsumption is asserted. |
| REFERENTIAL | 28 | Source examples, descriptions or illustrative implementation instructions retained as evidence. |
| CONFLICTING | 6 | Three paired source tensions remain open, with explicit counterparts. |

The A5 decision vocabulary has no source-only DISTINCT or SPECIALIZED disposition.
C0 therefore projects retained source propositions to `REFERENCE` with their
authored relationship rationale, and tensions to `CONFLICT`. A `REFERENCE`
decision here preserves actionable source guidance for C4/D0; it is **not** an
exclusion, a policy rejection, a completeness certificate, or a claim that the
guidance is nonnormative. No canonical control is referenced or created. The
source relationship view is supplementary authored staging data, not a new
approval schema or replacement for the A5/A6 review contracts.

No exact duplicates or supersessions are asserted. Source scope, applicability,
roles and Covenant-version distinctions prevent flattening apparently similar
conduct statements. Full AST fields, source locators, applicability, authority,
ambiguities and B0 review status are preserved in `relationships.json` and its
human-readable `review.md`. The decision ledger accounts for every AST field as
preserved and none as lost; this is structurally testable preservation, not an
independent endorsement of B0 formalization or omission completeness.

## Findings retained for review

- Conduct pledges differ across short/long and Covenant 1.4/2.0-derived versions;
  characteristic lists, sexual-conduct wording, leadership roles and conduct
  response scope remain distinct.
- Merge guidance differs by project and role. The two-maintainer rule retains
  its one-approval exception after more than 14 days; the two-other-developer
  rule retains its delegation condition; maintainer opposition remains a veto.
  No universal approval threshold or 48-hour service promise is adopted.
- Security-policy selection is optional in the coulds category, while file
  adaptation is should-level with a removal exception. That modal tension is
  recorded rather than resolved through an unreviewed interpretation.
- The jlcanovas README's CC BY 4.0 description and guidelines' CC-BY-SA starting
  point remain an explicit inconsistency. LICENSE.md retains its B0 legal-support
  disposition; C0 makes no license interpretation or redistribution decision.
- Atapas optional starring and promotional must wording remain a modal tension.
  Promotional language is not adopted as an enforceable requirement.
- CODEOWNERS examples and funding location assertions remain community source
  claims. C4 must compare relevant claims with authoritative platform evidence.
  Template identities, support links, example environments, deployment links,
  citation metadata and TryShape links remain examples rather than consumer facts.

## Reproduction and acceptance boundary

```sh
python -m ges.community_reconciliation
python -m ges.community_reconciliation --check
python -m ges semantics validate --input evidence/semantics/c0/ledger/decisions.jsonl
```

Generation refuses an existing destination. `--check` requires exact generated
membership and bytes. An unchanged regeneration does not produce a GO receipt.
Use `--output` for a fresh temporary destination when comparing a second run.

All 207 decisions remain `PROPOSED` with null reviewer/evidence. The residual
ledger lists every pending decision and all six tension participants. Acceptance
requires accepted B0/foundations, authorized reconciliation reviews, independent
audit, reviewed resolution of tensions, exact-head review/CI, merged-main
verification and owner acceptance. No reviewers or approval receipts are invented.

Exclude GHQR, Well-Architected, Docs, C4, owner policy adoption, consumer templates,
rights clearance, native operations, upstream submissions and release. Checkout
retained. C0 cannot be labeled verified or complete from these local checks.
