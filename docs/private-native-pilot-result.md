# Private native pilot execution

The owner-approved attempt on 2026-10-06 provisioned the disposable private
target and verified owner/admin permission. GitHub accepted the reviewed rule
in Disabled state. Five synthetic canary PRs were created, but the provider did
not start the Actions jobs. The nominal passing run had zero executed steps.
Failed check conclusions cannot establish execution of the test or aggregator.

| Acceptance requirement | Observed result |
|---|---|
| Private target and owner/admin permission | Confirmed |
| Ruleset payload accepted and read back | Confirmed, Disabled; server defaults retained |
| Required context associated with expected Actions publisher | Confirmed; execution not established |
| Actual passing canary | Not established |
| Failed/absent/cancelled/skipped dependency enforcement | Not established |
| Direct push, force update and deletion rejection | Not attempted |
| Activated policy, bypass behavior, rollback and repeat verification | Not attempted |
| Native pilot acceptance or estate adoption | Not established |

Main remained at its bootstrap SHA. The created rule remains Disabled. No
spending, visibility, existing estate policy or frozen #453 setting was changed.
Detailed observations, provider diagnosis and the independent review are stored
in the private target; public GES contains only this bounded aggregate result.

The current immutable private [sanitized evidence and independent audits](https://github.com/4444J99/ges-native-enforcement-pilot/tree/c5882e96eec46f2ea884703e5f8b300c228c5446/evidence)
are retained at commit `c5882e9`. A post-merge scan found a provider-generated
temporary clone credential in private metadata. The captured credential was
rejected by the private Git endpoint; expiration and revocation remain
unverified.
That field was removed from all seven exclusively pilot-owned branch histories
with exact leases. The independent corrective audit verified sanitized reachable
history and current manifest; its SHA256 is
`b4a1c6c9ddbd00f664ccf0084a69b14ae468568d936bdccc662bb0df1d8a382b`.
Provider-held cache purge also remains unverified.

The original native observation audit remains a historical attestation to
pre-redaction bytes and SHAs, not validation of current sanitized bytes. The
history correction changed branch SHAs and does not prove fresh native behavior.
The original verdict remains truthful observation accounting PASS, native
acceptance BLOCKED; the corrective custody verdict is PASS. These are agent
reviews, not human policy adoption or completed enforcement tests.

The Disabled rule was created before publisher confirmation. That ordering
deviation is recorded in the private evidence. Activation was never attempted;
the unfulfilled workflow prerequisite is preserved. Provider-added parameters
were retained in full readback rather than treated as byte-identical input.

This is a blocked execution attempt. The retry hold below requires independently
observed runner assignment and an executed step in the private pilot before another private-pilot
retry. Actual approved-workflow execution and canary command behavior are
prerequisites for activation. Accepted/rejected native operations under the
Active rule, rollback and unchanged second-run verification remain unperformed.

The reviewed source payload is PR #485 at `4d3aa01`; that PR was still open at
the execution preflight. Its earlier merge submission was deferred and is not
represented as merged. This observation does not change source-review coverage,
adoption accounting or any of the nine legacy gate verdicts.

## Bounded retry on 2026-10-08

The user authorized proceeding with the outstanding work package. One retry of
the existing nominal passing PR workflow was accepted by the provider:
[run 37560956698](https://github.com/4444J99/ges-native-enforcement-pilot/actions/runs/37560956698),
attempt 2. Both `pilot-test` and `pilot-required` completed with failure in about
three seconds, with `runner_id` 0, no runner name and zero executed steps. Job
logs returned HTTP 404. This records a repeated non-start; it supplies no
passing or failing canary behavior.

Billing is the standing suspect. The reported 3,000 / 3,000 included-minute
figure came from a quota email, not a billing-page readback. No current balance,
spending limit or billing cause was independently confirmed. Public Toolkit
checks on GES continued to pass at the reviewed integration head while the
private jobs failed to start. That pattern is consistent with a private-minutes
or spending-limit stop, but does not establish its cause. Any required billing
or spending change remains an owner decision.

The rule was read back as Disabled and the protected branch remained unchanged.
The workflow-execution prerequisite was not met, so activation, protected-branch
operation tests and rollback were not attempted. This observation supplies no
native acceptance, rights, source-review or estate credit.

The new sanitized observation and ruleset readback are retained in the private
[evidence commit 14c160d](https://github.com/4444J99/ges-native-enforcement-pilot/tree/14c160d0ac76a75e5528aa546f9a07c78e68e025/evidence).
That commit preserves earlier observations and the pre-redaction audit's
historical scope; it does not reconfirm the old audit against new bytes or
establish credential revocation or provider-cache purge.

**No further private-pilot retry until an independently observed job in the
private pilot receives a runner and executes a step.** Do not dispatch or rerun a pilot workflow to
test whether that condition has been met. Once execution availability is
established, the approved plan still requires the canary and aggregator to
execute with the expected publisher before activation. Positive/negative
operations, bypass assessment, rollback and unchanged second-run verification
must then be completed before native acceptance can be requested. No new retry,
activation or native acceptance is recorded by this checkpoint correction.
