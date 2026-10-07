# Actions security implementation batch

This batch reads five previously unreviewed pinned articles in full (1,075 lines),
45 recursive literal dependencies (121 lines) and 22 selected variable bindings.
It authors 105 propositions and accounts for all 382 candidate spans. Referenced
screenshots and external navigation receive no new visual or whole-file credit.
The input manifest binds the exact source pin, file digests and dependencies.

The independent review identified concrete checker errors. Workflow permission
checks previously passed absent/empty jobs; both checks could pass a step with
both `run` and `uses`, or parse an unresolved symlink as ordinary YAML. They now
reject these malformed execution shapes or require symlink review. Unknown
permission scopes require review, and invalid known scope values fail. The scope
table was cross-checked against the [official workflow syntax reference](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#permissions);
this additional syntax read supplies no pinned artifact credit.

GES-ACT-001 already calls for separately justified job-scoped elevation. The
checker now keeps broad root write as FAIL while returning MANUAL_REVIEW for
valid job-scoped write, including OIDC token issuance. It does not automatically
accept elevation. These are bounded shape and permission checks, not complete
GitHub schema, execution, injection or cloud-trust verification. Local reusable
workflow effective permissions still require separate review.

Use the [implementation review record](../templates/actions-security-review.md)
to carry the remaining accountable decisions from source claims into workflow
review: secret timing and limits, injection boundaries, pin origin, runner
isolation, caller versus called OIDC identity and provider trust conditions.
The template supplies no tokens, live writes, preset PASS or adoption authority.
It complements existing generic draft-control bindings without revising catalog
obligations or claiming that operational completeness has been achieved.

Two upstream illustrative limitations are retained explicitly: the secure-use
article spells `./github/workflows/` where local tooling uses `.github/workflows/`,
and the reusable OIDC example inserts whitespace after `@` before its SHA.
OIDC and large-secret examples that print sensitive material are illustrations,
not approved production snippets. The guide's job-bounded access-token wording
is qualified by its provider-configurable expiry statement. These observations
do not silently rewrite the pinned source or manufacture a policy conflict.

The combined reconciliation retains 303 earlier decisions and adds this batch's
105 audited decisions. Earlier receipts are rebound only to the new global claim
digest; their timestamps, subjects and historical decisions are not new review
credit. All controls remain drafts; source review is not policy adoption, rights
clearance, rendered-page assurance, native enforcement or estate rollout.
