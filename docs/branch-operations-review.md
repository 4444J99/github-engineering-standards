# Branch workflow and ownership source review

This second batch reads five previously unreviewed pinned GitHub Docs articles:
required-status-check troubleshooting, merge queues, managing repository rulesets,
troubleshooting rules and code owners. It adds 77 authored claims across 704 original
lines, with 42 literal dependency files and 14 resolved variable bindings inspected.
Only the five originals receive new artifact receipt credit. Ordinary navigation
and screenshot references are not extra semantic reviews.

The [primary record](../evidence/branch-operations-primary-review.json) and
[actual independent pass](../evidence/branch-operations-independent-review.json)
bind the source statements and operational review. Independent review corrected
an omitted whitespace-trimmed feature gate, an invented explanation for the
managed-user email limitation, an overbroad organization-rule target claim,
seven-day wording, delegated-bypass details and example candidate accounting.
It also found and corrected missing-target and malformed-App-ID false passes
in the new observer. No prior source claim was rewritten. GOV004 frontmatter provenance was repaired
to actual body spans; GOV004 revision2 and RULE007/008 revision3 link the
accountable procedure while retaining manual verification, obligations and draft
status. Combined references are rebound to those current revisions.

The combined [reconciliation](../evidence/branch-operations-reconciliation.json)
contains 233 receipts: the prior 156 decisions rebound to the enlarged known-claim
input and current control revisions plus 77 new decisions (63 partial supporting MAPs, 14 references). The
prior ten source-review files and historical 156 receipts remain unchanged. Rebinding
earlier decisions gives no new review credit. The prior three conflict records
still account for one unresolved squash-metadata contradiction.

## Concrete operational result

`ges collect` now captures bounded check/status/Actions-run observations at an
explicit SHA. `ges branch-checks` inspects selected publisher, exact revision,
eligible event, latest same-name commit status and completed SUCCESS. The command
reports execution, correct integration-revision selection, adoption and native
enforcement unproved even if its observed-check predicate passes. It does not
replace RULE008's accountable review or claim the whole control is complete.

The draft [profile](../profiles/branch-pilot.json),
[ruleset](../templates/branch-pilot-ruleset.json),
[workflow](../templates/branch-pilot-workflow.yml),
[procedure](branch-policy-operations.md) and
[private pilot plan](native-branch-pilot-plan.md) provide an inspectable target
change. The required aggregator fails for failed, skipped or cancelled dependency
results; a successful API check alone still does not prove that job execution.
Historical exports omit bypass actors, so rollback captures them separately.
Private queue eligibility is not established; this pilot has no queue mandate.

## Acceptance accounting

New artifact receipts: GitHub Docs 3,133→3,138; all sources 3,570→3,575 of 13,657.
Known source claims 61,618→61,695; validated reconciliation 156→233.
The substantive Docs unreviewed remainder is 6,340→6,335 of 9,116 inputs.
Candidate accounting adds 241 exact parser-candidate records after source reading.
The catalog remains 95 draft controls with zero accepted; all nine legacy gates
remain open. No whole-corpus omission audit, public expression clearance,
native pilot acceptance or estate rollout is credited.

Reproduce current accounting with the existing private caches:

```sh
python3 -m ges.recovery --sources /path/to/cache/sources --corpus /path/to/cache/corpus --reviews evidence/source-reviews --review-policy evidence/source-review-policy.json --rendered-directory /path/to/cache/rendered-docs --claim-reconciliation evidence/branch-operations-reconciliation.json --claim-reconciliation-policy evidence/branch-operations-reconciliation-policy.json --output evidence/recovery-status.json
```

Prior batch/routing documents are historical snapshots, including their original
counts and reproduction inputs. The combined inputs above supersede their
claim-input digest for the current report. Frozen #453 is untouched.
