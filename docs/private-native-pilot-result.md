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

The immutable private [outcome and independent audit](https://github.com/4444J99/ges-native-enforcement-pilot/tree/255358a6740ac6f4bdc14c5b6740456e81ec8af4/evidence)
are retained at commit `255358a`. The independent audit's SHA256 is
`975c0a5408bd4154a8df822637792c700000e458191ac5c01ec8d02ed4cbd481`.
Its verdict is truthful observation accounting PASS, native acceptance BLOCKED;
it is agent review, not human policy adoption or a completed enforcement test.

The Disabled rule was created before publisher confirmation. That ordering
deviation is recorded in the private evidence. Activation was never attempted;
the unfulfilled workflow prerequisite is preserved. Provider-added parameters
were retained in full readback rather than treated as byte-identical input.

This is a blocked execution attempt, not native acceptance. Resume only after
the provider can execute the approved workflow, or after the owner approves a
specific alternative. Confirm actual workflow execution and canary command
behavior before activation; then test accepted/rejected native operations under
the Active rule, followed by rollback and unchanged second-run verification.

The reviewed source payload is PR #485 at `4d3aa01`; that PR was still open at
the execution preflight. Its earlier merge submission was deferred and is not
represented as merged. This observation does not change source-review coverage,
adoption accounting or any of the nine legacy gate verdicts.
