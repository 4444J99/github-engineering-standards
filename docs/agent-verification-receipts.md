# Agent verification receipts

`ges.agent-verification-receipt.v1` is a strict, closed JSON record of what an agent
observed when it verified a change, plus a validator, fixtures and a reusable GitHub
Action that embeds the receipt in a pull request body. It encodes this repository's
verification standard (AGENTS.md, GOVERNANCE.md) so that "Staged", "Merged" and
"Verified" are three machine-checkable claims instead of prose.

Contract files:

- schema: `schemas/receipts/agent-verification-receipt.v1.json`
- validator, injector and CLI: `ges/receipts.py` (standard library only)
- fixtures: `tests/fixtures/receipts/` (`valid/`, `invalid/`, `expected-errors.json`, `generate.py`)
- action: `.github/actions/inject-agent-receipt/action.yml`

## Formal semantics

Let a receipt `R` carry checks `C`, a claim `claim(R)`, optional merge evidence `M`
and optional human acceptance `A`. Every rule below is enforced by `validate_receipt`;
each has a negative fixture.

**Check status.** A check has exactly one status.

| Status | Meaning | Required | Forbidden |
| --- | --- | --- | --- |
| `PASS` | The command ran and exited 0 | `exit_code = 0`, `output_sha256`, both timestamps | none beyond the table |
| `FAIL` | The command ran and failed | `exit_code != 0`, both timestamps | `exit_code = 0` |
| `NOT_RUN` | No execution occurred | the command that was intended | exit code, output digest, timestamps, provider conclusion |
| `NOT_VERIFIABLE` | A run (or provider verdict) exists but does not establish success | the command or check name | exit code, output digest |

A check that mirrors a GitHub check run records the REST `conclusion` in
`github_conclusion`. The mapping is total and fixed:

| GitHub conclusion | Receipt status |
| --- | --- |
| `success` | `PASS` (exit code may be null; evidence digest still required) |
| `failure`, `timed_out` | `FAIL` |
| `cancelled`, `skipped`, `neutral`, `stale`, `action_required` | `NOT_VERIFIABLE` |
| no conclusion yet | `NOT_RUN` (`github_conclusion` null) |

So a skipped or neutral check can never read as green, matching the repository's
honest-green aggregate (`standards/phase1/honest_green.py`). Missing evidence is
never `PASS`.

**Overall status** is derived, never asserted: `FAIL` if any check is `FAIL`;
otherwise `INCOMPLETE` if any check is `NOT_RUN` or `NOT_VERIFIABLE`; otherwise `PASS`.
A receipt whose `overall_status` differs from the derivation is invalid.

**Claim ladder.** `claim` is the strongest statement the receipt makes.

| Claim | Requires | Forbids |
| --- | --- | --- |
| `STAGED` | nothing beyond valid checks (branch-only evidence) | merge evidence, acceptance |
| `MERGED` | `merge_evidence` (main SHA, merge time, CI run URL in the subject repository, CI conclusion) | acceptance |
| `VERIFIED` | `overall_status = PASS`, `merge_evidence.ci_conclusion = success`, human `acceptance` at or after the merge time | none |

`VERIFIED` therefore requires, in the receipt's own words, the merged-main and
organization-acceptance conditions of the Verification Standard. A receipt cannot
prove who the named human is; `acceptance.reference` is a pointer a reviewer follows.

**Identity and time.** `id` is `agent-verification-receipt:` plus the SHA-256 of the
canonical encoding (sorted keys, compact separators, UTF-8) of every other field.
Timestamps are UTC with a trailing `Z`; a check's finish does not precede its start,
and `generated_at` is not earlier than any check finish or merge/acceptance time.
Check names are unique; commit SHAs are 40 lowercase hex characters.

**What a receipt does not establish.** It does not authenticate the agent, prove the
commands ran, or replace human review. Validation is structural plus internal
consistency. The `limitations` array exists for the producer to state what was not
evaluated.

## Validator

The validator implements the closed JSON Schema vocabulary the schema uses
(`SUPPORTED_KEYWORDS` in `ges/receipts.py`); a test fails if the schema ever uses a
keyword the validator does not enforce, if an object schema is open, or if a property
is optional. It reports every violation, not only the first.

```
python -m ges receipt validate receipt.json          # exit 0 valid, 2 invalid
python -m ges receipt seal --input draft.json --output receipt.json
python -m ges receipt render --receipt receipt.json
python -m ges receipt inject --receipt receipt.json --body-file body.md --output new-body.md
python -m ges receipt extract --body-file new-body.md
```

`seal` adds `schema` and `id` and refuses to write an invalid receipt.
Regenerate fixtures with `python tests/fixtures/receipts/generate.py`; a test fails
if committed fixtures drift from the generator.

## PR-body injection

The block sits between `<!-- ges:agent-verification-receipt:begin -->` and
`<!-- ges:agent-verification-receipt:end -->`. Injection is idempotent: a re-run
replaces the block and leaves all other body text untouched. Repeated or unbalanced
markers fail. The visible table shows only the check name (reduced to a safe
character set, so mentions and links cannot render), status and exit code; all other
detail is inside a fenced JSON block whose fence is longer than any backtick run in
the content. Receipt text containing the marker is refused. `extract` re-renders the
embedded receipt and rejects a block that was edited after rendering.

## Action

```yaml
# Caller workflow (pull_request trigger, same-repository branches)
permissions:
  contents: read
  pull-requests: write
jobs:
  receipt:
    runs-on: ubuntu-24.04
    timeout-minutes: 5
    concurrency:
      group: agent-receipt-${{ github.event.pull_request.number }}
      cancel-in-progress: true
    steps:
      - uses: actions/checkout@11d5960a326750d5838078e36cf38b85af677262
        with:
          persist-credentials: false
      # ...a trusted step writes receipt.json from observed results...
      - uses: 4444J99/guide-github-standard/.github/actions/inject-agent-receipt@<full-commit-sha>
        with:
          receipt-path: receipt.json
```

Pin the action to a full commit SHA. The step:

1. refuses `pull_request_target` (the receipt would originate in an untrusted context);
2. validates the receipt and fails on any violation;
3. fetches the PR and refuses a receipt whose repository, PR number or `head_sha` differs
   from the PR's current head (stale or foreign evidence is never embedded);
4. patches the body, then re-reads it and confirms the same receipt id is present.

Failure is always visible: an invalid receipt, a read-only token (fork pull requests,
or a job without `pull-requests: write`) and a lost update from a concurrent body edit
each fail the step. Nothing is skipped silently. The action takes no inputs through
shell interpolation; values reach the script as environment variables. It has no
third-party `uses:` dependencies. The receipt path is read from the workspace, so the
producing step must not take its content from untrusted PR text.

Outputs: `receipt-id`.

## Limits

Concurrent edits to the PR description between the read and the write can still be
lost; the post-write check detects the case in which the receipt itself is lost but not
other overwritten text. This tranche adds no required check, ruleset change or consumer
onboarding.
