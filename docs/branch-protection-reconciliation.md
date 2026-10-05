# Branch protection source reconciliation

Owner: PR #1. Status: reviewed drafts, not adopted or activated.

The pinned GHQR branch-protection definition and scanner were read in full. Fourteen
source recommendations are separately paraphrased in
`evidence/source-reviews/ghqr-branch-protection-claims.json`. The generic extractor
returned zero candidates for both files despite their actionable content. The
structured ledger, full-file review and scanner audit are therefore necessary;
candidate accounting alone cannot certify semantic completeness.

Canonical GES-RULE-001 through 006 are revision 2. Deletion maps to repo-bp-011,
non-fast-forward protection to 010, pull-request policy to 006, quorum to 002/003,
and stale approval dismissal to 004. The former shared 014 mapping is informational,
not evidence for those specific objectives. Thread resolution has no equivalent
in this GHQR file; its 014 reference is explicitly background-only. Exact passages
in the pinned GitHub Docs `available-rules-for-rulesets.md` now support all six
objectives, replacing frontmatter-only citations. The general ruleset page is
background context, not a substitute for rule-specific semantics. Stale approval
dismissal concerns changes to the reviewed diff, not every newly pushed commit.
Reading these passages does not certify the complete page or its includes rendered
for every product version. Those pages remain uncounted in exhaustive review.

Template review: `templates/ruleset.json` includes deletion, non-fast-forward,
pull-request integration, the parameterized review count, stale approval dismissal,
and thread resolution. It does not require code-owner review, strict status checks,
signatures or linear history. These remain gaps when the target adopts those
recommendations. The template is data, not authorization to enable its active policy.

Applicability review: protected-branch applicability remains explicit. The solo
profile declares zero native independent approvals and a separate accountable
manual review obligation. GHQR's one-review recommendation conflicts with that
capacity assumption; its two-review recommendation is high-risk advisory guidance.
No profile is accepted and no nonexistent independent reviewer is invented.

Scanner limits: missing legacy detail produces a finding; ruleset handling is a
separate function and the caller remains unaudited. The full ruleset collector was
also reviewed: its queries cap rulesets/rules without pagination, omit branch
conditions and bypass actors, combine active branch rules without evaluating
whether the named branch matches, and label protection by active ruleset count.
The REST fallback is an inert skeleton. These limitations prohibit adopting that
projection as equivalent to the effective-branch-rules API. Protection flags do not prove
bypass coverage or actual rejected writes. Signature requirements do not alone
prove the identity of the human who authored a change. Linear history is contextual
and must be reconciled with the tmcw history-policy alternatives.

Next: audit upstream collection and caller composition, review exact GitHub Docs
passages supporting thread resolution and ruleset semantics, resolve policy conflicts,
author missing objective-specific bindings with counterexamples, and conduct an
explicitly approved native behavior pilot. No native changes were executed.
