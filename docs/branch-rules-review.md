# Branch protection and ruleset source review

This batch reads five previously unreviewed pinned GitHub Docs articles: about
protected branches, managing a classic protection rule, about rulesets, available
rules, and creating repository rulesets. It adds 156 authored claims with exact
source spans and content/span digests. The reviewers read all 855 original lines,
62 reusable/feature dependencies and 22 variable bindings, and compared the
GHQR evaluator's callers, query and parser. Ordinary navigation links and external
recipes remain references rather than additional reviewed article bodies.

The [primary record](../evidence/branch-rules-primary-review.json) and separate
[independent review](../evidence/branch-rules-independent-review.json) identify the
source bodies, corrections and review limits. Five artifact receipts account for
all 369 parser candidates. Candidate accounting is bookkeeping after reading;
it generates no semantic decisions.

The final [exact-claim receipts](../evidence/branch-rules-reconciliation.json) use
the existing two-role reconciliation contract: 109 partial supporting mappings
to existing catalog objectives, 44 references and three conflict records. A
supporting mapping does not establish equivalence to every control criterion,
adoption, a verified native setting or a complete source-to-control omission audit.
No new control or proposal was generated. This contract does not substitute for
the separate four-role A6 proposition-review contract.

Three concrete catalog provenance repairs update GES-RULE-007/008/009 to revision
2: replace the frontmatter citation for effective layering with actual body
evidence, and add precise required-check/publisher/trigger and signing/merge
compatibility references. Their obligations, verification procedures and draft
status remain unchanged; generated catalog views are rebuilt.

## Findings retained in the result

GHQR chooses classic protection **or** rulesets, rather than their combined
effective policy. Its ruleset query caps results at 25 rulesets and 30 rules
without pagination, branch-target conditions or bypass details. Parsed presence,
OR aggregation, maximum approval counts and check-name unions cannot certify
effective protection. These observations constrain the use of GHQR results;
they are not a new implementation of that upstream scanner.

The pinned metadata reusable says every commit on a squash-merged branch must
meet the metadata requirement. The available-rules article instead says only
the resulting squash commit is checked. Both assertions and the creating-guide
repeat are recorded as an unresolved conflict. Neither interpretation is credited
as settled native behavior.

Two regex examples are retained as references rather than recommended rules:
the positive-lookahead workaround conflicts with the linked
[primary RE2 syntax](https://github.com/google/re2/wiki/Syntax), and the Windows
branch-name expression lacks repetition for its multi-character example.
This external syntax check does not refresh the pinned Docs source or prove
current GitHub enforcement.

Independent review corrected draft overstatements about Copilot opening versus
approving a PR, deployment availability, Actions budget failures, optional
status-author inspection, signature behavior, feature gates and source spans.
The corrected statements retain their actual modality and product conditions.

## Acceptance accounting

This batch adds **five** artifact receipts: GitHub Docs 3,128 → 3,133; all six
sources 3,565 → 3,570 out of the unchanged 13,657-artifact inventory. Known text
claims become 61,618, of which this batch supplies 156 validated reconciliation
dispositions. The three conflict records account for one contradiction; they do
not resolve it. All nine project gates remain open and accepted controls remain
zero.

The routing documents from PRs #482/#483 are dated routing snapshots. Their
historical receipt counts are not rewritten as new semantic review. Within the
9,116 substantive Docs inputs, these five new reviews reduce the unreviewed
remainder from 6,345 to 6,340. Included dependencies were inspected for this
interpretation; they receive no additional whole-artifact review credit here.

Reproduce the current acceptance report with the private pinned cache and full
rendered-body cache available:

```sh
python3 -m ges.recovery --sources /path/to/cache/sources --corpus /path/to/cache/corpus --reviews evidence/source-reviews --review-policy evidence/source-review-policy.json --rendered-directory /path/to/cache/rendered-docs --claim-reconciliation evidence/branch-rules-reconciliation.json --claim-reconciliation-policy evidence/branch-rules-reconciliation-policy.json --output evidence/recovery-status.json
```

Neither source review nor owner authorization for this batch grants publication
rights, adopts the draft catalog, activates native policy, closes whole-corpus
omission certification, or supplies estate rollout evidence. Frozen #453 is
outside the batch.
