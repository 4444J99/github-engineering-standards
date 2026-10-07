# Approved private native pilot

Owner approval: the user approved execution of the specific private pilot plan
on 2026-10-06. Payload baseline: 4d3aa01d85f22e78799d3de6589ee8f398e8b200,
PR #485. Run only the disposable private target named in
`docs/native-branch-pilot-plan.md`; preserve visibility, other targets and #453.

1. Provision the absent private target and measure private ruleset capability.
2. If supported, bootstrap the reviewed workflow, exercise actual passing and
   rejecting behavior, restore experimental payloads, and exercise rollback.
3. Keep detailed observations in the private target; independently review the
   evidence and publish safe aggregate results in this repository.

Stop on unsupported private capability. Never replace a provider failure with
public visibility or an upgrade. One 30-minute attempt; no synchronous CI waits.
Source review, merge, policy acceptance and live enforcement remain separate.
