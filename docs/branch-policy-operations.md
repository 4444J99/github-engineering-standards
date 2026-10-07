# Branch-policy operational procedure

This procedure uses the five articles in `branch-operations-primary-review.json`.
The 95 canonical controls remain drafts. Source review, observed check results,
policy adoption and native acceptance retain their separate requirements.

## Observe required checks on an explicit revision

The collector retrieves bounded, SHA-bound check runs, commit statuses and Actions
workflow runs. `branch-checks` checks selected App, latest same-name status,
completed SUCCESS and eligible Actions event. It rejects incomplete, stale,
wrong-target or wrong-revision observations. The [check-run API](https://docs.github.com/en/rest/checks/runs#list-check-runs-for-a-git-reference)
is capped at 1,000 recent suites; this is not exhaustive historical accounting.
[Commit statuses](https://docs.github.com/en/rest/commits/statuses#list-commit-statuses-for-a-reference)
are returned newest first. These live adapter references receive no pinned-source
semantic artifact review credit.

```sh
python3 -m ges collect --repository 4444J99/ges-native-enforcement-pilot --ref main --check-revision EXACT_SHA --output .cache/pilot-snapshot.json
python3 -m ges branch-checks --snapshot .cache/pilot-snapshot.json --profile profiles/branch-pilot.json --revision EXACT_SHA --revision-kind head --output .cache/pilot-checks.json
```

Substitute the actual 40-character lowercase SHA. For a PR record head, base,
test-merge SHA and which GitHub requires; choose `test_merge` when its checks take
precedence. For an eligible queue select its current group SHA and `merge_group`,
never an earlier PR SHA. Declaring a revision kind does not prove its relationship
to a PR. The checker reports selection, execution and native verification false.
Exit0 means only the bounded observed-check predicate passed; it does not close
RULE008 or native acceptance. For `head`, collect the actual head branch with
`--ref`, rather than using `main` when the selected revision is a PR head.

GitHub permits neutral/skipped results; this draft requires SUCCESS. Even SUCCESS
can be a skipped conditional job. Review the workflow at the tested SHA: exact
job/App, eligible event, no whole-workflow path/branch skip, no cancelling required
run, and an `always()` aggregator that fails unless required dependencies succeed.
The supplied aggregator checks `needs.pilot-test.result`; unconditional green
aggregators are unacceptable. `workflow_dispatch` is not a required PR-event
substitute. Same-name status and check run must BOTH pass. Status payloads do not
establish publisher App identity; review status-author restrictions separately.

## Accountable review and readback

Owner `4444J99` records target, PR/tested SHAs, timestamp, profile digest, check/App,
workflow review and approve/reject decision. Agent review is not a second human.
The solo draft native approval count is0; accountable review remains separate.

Read every applicable classic protection and inherited repository/organization/
enterprise ruleset, target conditions and enforcement state. Evaluate/Disabled
are not active protection. Capture bypass actors/modes, admin/custom-role
exemptions and fork-network push inheritance. Unknown access or plans stays
unknown. Inspect effective branch rules and test actors; presence, parameter
comparison or GHQR's legacy-OR-rulesets scan is partial evidence.

When code-owner review applies, inspect the BASE branch's first file in `.github`,
root, then `docs`, size/errors and case-sensitive matching. Test last-match and
empty-owner overrides and CODEOWNERS' own routing. Confirm users' write permission,
visible organization teams with explicit TEAM write, and fork-specific access.
ANY listed owner suffices. Presence or a gitignore parser does not prove routing.
This pilot leaves native code-owner review off pending those prerequisites and a
reviewed policy amendment. Signing/history requires its own product and merge
method review. Preserve the prior unresolved squash-metadata contradiction; optional
upstream capabilities do not establish a local signing/regex/queue mandate.

## Pilot and rollback

Use `native-branch-pilot-plan.md`. Capture complete original configuration AND
bypass lists before activation: historical JSON export omits bypass actors.
Record created rule ID, proposed/read-back digests, capability and permission
responses. Restore that exact rule's prior state and separate bypass settings
when a test fails; verify readback and baseline behavior. Do not delete a repo or
existing rule as a recovery shortcut. After positive/negative tests repeat
readback and assessment on unchanged configuration/evidence. Local tests and
publication do not replace live acceptance.
