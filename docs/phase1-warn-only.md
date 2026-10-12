# Phase 1 — secrets & supply chain (warn-only)

Status: **staged, warn-only**. Source: Code-room standards proposal (2026-10-10), Phase 1, approved to build by Anthony on 2026-10-12. Nothing here is a required check, and no ruleset or branch protection changes come with it.

## What the reusable workflow checks

`.github/workflows/phase1-warn.yml` (thin; one script plus two pinned tools):

| Rule | How |
|---|---|
| Third-party actions / reusable workflows pinned by commit SHA | `standards/phase1/check.py` |
| Least-privilege `permissions:` declared | check.py |
| Runner images pinned (no `*-latest`) | check.py |
| Every job has `timeout-minutes`; workflow or job `concurrency` | check.py |
| No `continue-on-error: true`, `\|\| true`, `exit 0` | check.py |
| Dependabot configured; weekly + grouped per ecosystem | check.py |
| Lockfile committed for root manifests | check.py |
| `actionlint` | pinned v1.7.7, sha256-verified |
| Secret scan of the current tree | gitleaks v8.21.2, sha256-verified, output redacted |
| Honest-green aggregate | `standards/phase1/honest_green.py`: skipped, cancelled, failed, missing, or 0-step jobs are **not** green |

All findings are emitted as `::warning` annotations; the job exits 0 unless `enforce: true` (not used during warn-only rollout). OpenSSF Scorecard stays a separate warn-only signal and is not bundled here, to keep this workflow thin.

## Caller example (do not roll out until Anthony opts a repo in)

```yaml
jobs:
  test: { ... }
  standards:
    needs: [test]
    if: ${{ always() }}
    permissions: { contents: read, actions: read }
    uses: 4444J99/github-engineering-standards/.github/workflows/phase1-warn.yml@<40-char-sha>
    with:
      standards-ref: <same 40-char-sha>
      needs-json: ${{ toJSON(needs) }}
```

## Verification receipt format (agent-opened PRs)

Minimal and machine-parsable; append a new block for every new head, and merge pinned with `--match-head-commit <sha>`:

```
### Receipt
head: <40-char sha>
commands:
- `<exact command>` → pass|fail (<counts / observed output>)
note: <one line, e.g. "no logic change: file add only">
```

No receipt ⇒ not eligible for green merge. Dependabot PRs merge on honest green alone unless an agent pushes a commit.

## Token hygiene (process rules, not machine-checked here)

1. Tokens for connectors and `gh` enter only via masked secret input or the box secret store — never chat, repo, or plain workspace files. (gitleaks above catches the repo case only.)
2. Every token has an owner, scope, and rotation note; the old token is revoked on rotation. CodeAudit audits this.

## Rollout

Warn-only everywhere first → pass/fail fixtures (in `tests/fixtures/phase1`) green in this repo's CI → warn-only on sample repos → opt-in required only where Anthony says so. Required checks on this repo's `main` stay off until Anthony decides.
