# Governance

Repository owner and decision authority: @4444J99.

Contributors, including automated contributors, propose versioned changes. They do not appoint themselves independent human reviewers or approve protected rollout on the owner's behalf.

Controls begin as PROPOSED or REVIEWED_DRAFT. ACCEPTED requires an explicit, recorded target-policy adoption decision and verified implementation/evidence requirements. Upstream recommendation severity is not automatically the owner's obligation level.

**Definition of "Verified" / "Done"**:
"Verified" means merged to `main` AND accepted by the organization. Branch-only verification (such as passing a 6-script harness on a feature branch) is necessary but NOT sufficient. This requires:
1. All verification commands (tests, validate, compile) pass on the merged commit in `main`.
2. Remote CI passes (source acquisition + reconciliation workflow).
3. Human code review approval received.
4. Organization acceptance: explicit acknowledgment by designated owner that the merged state meets acceptance criteria.
5. No open gates remain for the merged scope.

The standard owns reusable specifications, validators and templates. Consumer repositories own application-specific implementation and deployment. Existing credential custody remains outside this repository.

No numerical service-response promise, universal two-reviewer policy, automatic age-based waiver, public visibility change or estate-wide security setting is established by copying upstream examples.

Exceptions identify control revision, target, approver, reason, compensating safeguard and expiry. An exception never rewrites failure into compliance. Evidence and declared authorization inputs require a trustworthy, access-controlled review process; this CLI is not an identity provider.

## Definition of "Verified" (Effective 2026-10-05)

**"Verified" = Merged to `main` AND accepted by the organization.**

This is the operational definition for all work in this repository. It replaces the prior branch-only definition.

### Required Conditions for "Verified"

A change is **only** "Verified" when ALL of the following are true:

1. **Merged to `main`**: The change exists as a commit on the `main` branch (not a feature branch, not a PR branch, not a draft)
2. **All 6 verification commands pass on the merged commit in `main`**:
   - `python -m ges.claim_review --artifacts .cache/corpus/artifacts.jsonl --sources .cache/sources --reviews evidence/source-reviews --review-policy evidence/source-review-policy.json`
   - `python -m ges.recovery --sources .cache/sources --corpus .cache/corpus --reviews evidence/source-reviews --review-policy evidence/source-review-policy.json --rendered-directory .cache/rendered-docs --output evidence/recovery-status.json`
   - `python -m unittest discover -s tests -v`
   - `python -m ges validate`
   - `python -m ges compile`
   - `git diff --check`
3. **Remote CI passes**: Source acquisition + reconciliation workflow complete successfully on `main`
4. **Human code review approval**: At least one explicit human review approval on the merged PR
5. **Human security review** (where applicable): For changes touching security policies, workflows, or secret-handling — explicit security reviewer sign-off on historical findings triage (e.g., the 146 historical secret-scan entries)
6. **Organization acceptance**: Explicit acknowledgment by the repository owner (@4444J99) that the merged state meets acceptance criteria for the delivered scope
7. **No open gates for merged scope**: All 9 gates documented in `docs/remaining-work.md` are either satisfied or explicitly deferred with recorded rationale for the merged scope

### What is NOT "Verified"

- ✅ Branch-only test passes → **"Staged"** (necessary but insufficient)
- ✅ PR checks green → **"Staged"** (necessary but insufficient)
- ✅ Local validation passes → **"Staged"** (necessary but insufficient)
- ✅ "Ready to merge" → **Not verified until actually merged and accepted**

### Terminology

| State | Meaning |
|-------|---------|
| **Staged** | Passes local/remote checks on a branch; ready for review |
| **Reviewed** | Human review approval received |
| **Secured** | Security review complete (where required) |
| **Merged** | Commit exists on `main` |
| **Verified** | **All of the above + organization acceptance** |
| **Done** | Synonym for **Verified** — no lesser state qualifies |

### Enforcement

- No PR may be labeled "verified", "done", or "complete" until the merged commit on `main` satisfies all conditions
- CI/CD pipelines must gate on `main` branch verification, not PR branch verification
- Release tags may only be created from `Verified` commits on `main`
- The 6 verification commands are **gate checks**, not the definition of verification
