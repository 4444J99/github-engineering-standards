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
rejected by the private Git endpoint; expiration or revocation was not inferred.
That field was removed from all seven exclusively pilot-owned branch histories
with exact leases. The independent corrective audit verified sanitized reachable
history and current manifest; its SHA256 is
`b4a1c6c9ddbd00f664ccf0084a69b14ae468568d936bdccc662bb0df1d8a382b`.
Provider-held unreferenced caches are not measured as purged.

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

This is a blocked execution attempt, not native acceptance. Resume only after
the provider can execute the approved workflow, or after the owner approves a
specific alternative. Confirm actual workflow execution and canary command
behavior before activation; then test accepted/rejected native operations under
the Active rule, followed by rollback and unchanged second-run verification.

The reviewed source payload is PR #485 at `4d3aa01`; that PR was still open at
the execution preflight. Its earlier merge submission was deferred and is not
represented as merged. This observation does not change source-review coverage,
adoption accounting or any of the nine legacy gate verdicts.
