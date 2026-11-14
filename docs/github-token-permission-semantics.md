# GITHUB_TOKEN permission semantics from GitHub Docs

This tranche turns a bounded set of GitHub Docs passages into formal semantics: an
executable model (`ges/token_semantics.py`) plus a source-bound ledger
(`evidence/semantics/github-token-permissions/`). It is the first GitHub Docs slice
that is both extracted and executable; it does not review the 13,219-file corpus
(see [GitHub Docs source scope](github-docs-source-scope.md)).

Scope: how the `GITHUB_TOKEN` gets its permissions, how fork runs and the two
pull-request triggers change them, token lifetime, which events a token-made change
re-triggers, and what `GITHUB_SHA`/`GITHUB_REF` denote for the two pull-request
triggers. These are the rules the [agent verification receipt](agent-verification-receipts.md)
action depends on (it writes a pull request body with the job token).

## Status and limits

Every record is `PROPOSED` with no reviewer. Structural validity, source binding and
model conformance do not certify that the prose was read correctly, and the
documentation is not a specification of GitHub's server behaviour. No policy is
adopted, no control accepted, and no live GitHub behaviour was observed. Where the
prose is silent or hedged the model says so (see Ambiguities) rather than guessing.

Source: `github/docs` at `56fcfa816f27bca239e5d39fff0d4f74f77ec995` (the commit in
`sources/sources.lock.json`), ten files, 32 occurrences, 36 propositions. 32
propositions name a model rule; 4 are preserved without one. The ledger stores
hashes and formalized ASTs, not the prose.

## The model

Access levels are ordered `none < read < write`. Scopes and their allowed levels come
from the docs' permission list; `id-token` allows `write|none` (fpt/ghec),
`vulnerability-alerts` allows `read|none`, and four scopes appear only under named
`ifversion` flags.

| Rule | Statement | Function |
| --- | --- | --- |
| T3 | The token is valid until the job finishes or the runner's maximum lifetime: 6 h on GitHub-hosted runners, refreshable for at most 24 h on self-hosted | `token_is_valid` |
| T4 | A `permissions` value assigns `read`, `write` or `none` per scope; `write` includes `read`; disallowed levels are invalid | `apply_permissions_key`, `allows` |
| T5 | Specifying any scope sets every unspecified scope to `none` | `apply_permissions_key` |
| T6 | `read-all` / `write-all` give every scope that level, clipped to the scope's allowed levels | `apply_permissions_key` |
| T7 | `permissions: {}` sets every scope to `none` | `apply_permissions_key` |
| T8 | Calculation: enterprise/organization/repository default, then workflow-level `permissions`, then job-level `permissions`, then (pull request event other than `pull_request_target`, from a fork, `Send write tokens to workflows from pull requests` off) every `write` becomes `read` | `resolve_token_permissions` |
| T9 | `permissions` may sit at workflow level or on a job; a job's key replaces the workflow's for that job | `resolve_token_permissions` |
| T10 | In a fork run the key can add or remove `read` but typically not grant `write` | `resolve_token_permissions` |
| T11 | The admin setting above is the exception that allows fork `write` | `resolve_token_permissions` |
| T12 | `pull_request_target` runs are not downgraded, even from a public fork | `resolve_token_permissions` |
| T13 | From a fork, no secret except `GITHUB_TOKEN` reaches the runner, except that `pull_request_target` (a privileged trigger that may access referenced secrets) is not withheld | `secrets_reach_runner` |
| E1 | `pull_request`: `GITHUB_SHA` is the merge commit, `GITHUB_REF` is `refs/pull/N/merge` (the destination branch when closed by merge); skipped on a merge conflict | `pull_request_event_context` |
| E2 | Both triggers run by default for `opened`, `synchronize`, `reopened` | `pull_request_event_context` |
| E3 | Events caused by the repository token create no run, except `workflow_dispatch`/`repository_dispatch` (always) and `pull_request` `opened`/`synchronize`/`reopened` (approval-required, behind the docs' version flag) | `workflow_run_for_token_event` |
| E4 | `pull_request_target` runs against the default branch of the base repository (base branch on GHES before 3.20), never the merge commit | `pull_request_event_context` |

The default access map is a caller input. The pinned pages do not enumerate the
restricted and permissive presets, so the model does not invent them; the conformance
cases use `contents: read, packages: read` as an illustration.

## Conformance

`evidence/semantics/github-token-permissions/conformance.json` holds 40 cases. Each
cites rules; `check_conformance` fails when the model disagrees with a case, when a
case cites a rule no source statement supports, and when a rule that source statements
support has no case. Cases include the error results the model must produce (for
example `read` for `id-token`).

```
python -m ges token-semantics conformance
python -m ges token-semantics validate
python -m ges token-semantics verify --sources PINNED_DOCS_CHECKOUT
python -m ges token-semantics build  --sources PINNED_DOCS_CHECKOUT [--output DIR]
```

`build` and `verify` need the nine pinned files laid out as in the `github/docs`
checkout; `verify` rebuilds the ledger and fails on any difference, so a changed
content digest, a moved line range or a missing anchor phrase is reported. CI exercises
the same code on a synthetic source (`tests/test_token_semantics.py`); the real files
are not vendored.

## Consequences for the receipt action

Derived by the model and asserted in tests:

- A fork `pull_request` run cannot hold `pull-requests: write` by default, so the action's
  body update fails visibly there, as documented. With the admin setting on it can write.
- A `pull_request_target` run keeps `write` from a fork, which is why the action refuses
  that event: the token is writable while the receipt would come from untrusted context.
- `GITHUB_SHA` on `pull_request` is the merge commit, so a receipt `head_sha` must come
  from the event payload (`github.event.pull_request.head.sha`), as the action requires.
- The action's own `PATCH` of the body uses the job token and its `edited` event creates no
  workflow run (E3), so the action cannot recurse.

## Ambiguities preserved

- T12: whether `pull_request_target` overrides a restricted default or only skips the fork
  downgrade is unstated; the weaker reading is implemented.
- T6/T8: `id-token` has no `read`; `read-all` and the fork downgrade give it `none`. The
  docs do not say this.
- T11: "typically you can't" is not defined; the setting is treated as the only exception.
- The docs state the `pull_request` payload "is empty for merged pull requests and pull
  requests that come from forked repositories". It conflicts with common use of the
  payload and is preserved without a rule; verify against a real run before relying on it.
- The `pull_request_target` branch-name pattern restriction is preserved without a rule:
  the patterns are not given.

## Not covered

The remaining GitHub Docs corpus, the GitHub App permission tables, REST and webhook
reference data, org-level default-permission pages, reviewer approval of these
propositions, and any comparison with live GitHub behaviour.
