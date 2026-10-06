# A4 original-intent matrix

Status: staged proposal; human approval pending. These six charters interpret the
original sources at the commits in `sources/sources.lock.json`. They establish
source roles, not exhaustive semantic coverage, adopted policy, rights clearance,
or compliance. Source statements and GES interpretation are separated below.

| Original source | Original intention | Authority within the synthesis | Boundary | Charter |
|---|---|---|---|---|
| github/docs | Explain GitHub products and their use | Primary documented platform behavior and implementation details | Preserve version, product, plan, permission and conditional applicability | [Docs](github-docs.md) |
| github/github-well-architected | Help organizations adopt and design GitHub solutions | Strategic principles, recommendations and assessment structure | Implementation details defer to Docs; guidance is not automatic policy | [Well-Architected](github-well-architected.md) |
| microsoft/ghqr | Assess GitHub configuration and identify gaps | Its check definitions, evaluation behavior and explicit limitations | Scanner coverage or missing data cannot prove complete compliance | [GHQR](microsoft-ghqr.md) |
| tmcw/github-best-practices | Advise long-lived, continuously deployed product teams | Contextual collaboration and change-management advice | Author opinion; explicitly unopinionated choices stay unopinionated | [Best practices](tmcw-github-best-practices.md) |
| jlcanovas/gh-best-practices-template | Kickstart an adaptable repository | Template structure, governance examples and stated modalities | Placeholders and example thresholds require local decisions | [Template](jlcanovas-gh-best-practices-template.md) |
| atapas/model-repo | Model welcoming presentation and participation | Onboarding, contribution and engagement examples | Sample stacks, links and deployment commands are not universal requirements | [Model repo](atapas-model-repo.md) |

## Reconciliation rules

1. Preserve source identity and original modality before proposing a GES rule.
2. Use Docs for documented platform mechanics, Well-Architected for strategic
   recommendations, and GHQR for what its evaluator actually checks. These are
   different questions, not a universal ranking of every source claim.
3. Keep contradictions, limitations and unknown applicability explicit. Record
   retained, generalized, strengthened, omitted or conflicting dispositions in
   later semantic reconciliation; this tranche does not adjudicate those claims.
4. Local policy decisions require an owner, rationale and approval. Never turn
   an example, descriptive fact or recommendation into an unmarked obligation.
5. The six original sources remain the founding synthesis boundary. Later external
   standards and internal ancestral implementations belong to separate comparison
   layers before the broader Engineering Environment Standards architecture.

## The two GitHub Docs questions

Exact source language is the semantic input, not a keyword proxy. Later extraction
must retain exact locators and distinguish actor, action, object, modality,
conditions, exceptions, product/version scope and reusable-content dependencies.
This is a GES interpretation of how to formalize the documentation, not a claim
that GitHub publishes a formal policy language.

Potential upstream contributions are a separate output of that work: reproducible
documentation defects, unclear wording or missing examples may become proposals
within Docs' contribution scope. Our compiler, local policy and infrastructure
changes are not automatically Docs contributions. A4 identifies the channel; it
does not assert that a contribution-worthy defect has already been verified.

## Acceptance boundary

The current source pins are the preparation baseline. Revalidate these charters
against the accepted A3 capsule before accepting the original-intent baseline.
Independent work does not depend on PR #472 merging, but changes to source pins or
scope must trigger review. Owner approval remains pending for every charter.
The linked evidence manifest records inspected root spans, not an exhaustive
review denominator or a human-acceptance receipt.

See [provenance manifest](../../evidence/a4-source-charters.json).

Replay all citations against an existing pinned source cache:

```sh
python -m ges.source_charters --sources .cache/sources --capsule-receipt evidence/a4-capsule-baseline.json --capsule-sha256 TRUSTED_A3_CAPSULE_SHA256 --receipt-sha256 TRUSTED_A3_RECEIPT_SHA256
```

`content_sha256` hashes the complete UTF-8 source text. `span_sha256` uses the
canonical ledger convention: `"\n".join(text.splitlines()[start_line-1:end_line])`,
without an appended newline. The replay uses the same verifier as structured
review and fails on missing source bytes. The validator compares visible charter
links with the manifest and retains only cited text while verifying every snapshot
row against the complete inventory. Independently supplied receipt and capsule
fingerprints bind the full A3 baseline bytes and content identities; unchanged
cited spans in an altered corpus are insufficient. CI acquires the same pinned
archives and runs this replay on changes to its inputs, with fresh acquisition
timestamps excluded from content identity. Synthetic tests remain separate.

The reviewed repository commit is the trust rail for the two expected fingerprints
in the manifest. Do not trust replacement fingerprints supplied alongside an
unreviewed baseline. This baseline is prepared from the repaired A3 receipt, not
an assertion that A3 has been accepted. Replay always reports owner approval and
A3 owner acceptance as unverified; those remain separately recorded human gates.
