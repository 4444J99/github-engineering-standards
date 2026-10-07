# Proposed private branch-enforcement pilot

Owner `4444J99`; target `4444J99/ges-native-enforcement-pilot`, private, disposable.
Scope: one `main` branch; no existing estate targets or frozen #453.
Native writes await the specific plan approval required by `remaining-work.md`
lines20–23. Source-review/merge approval is not counted as adoption or pilot proof.

1. Read target existence, authenticated owner/admin permission, visibility and
   plan capability. The authenticated owner is a User and its plan was not
   returned. Private ruleset eligibility remains unmeasured. If unsupported,
   stop with that result; do not make the repo public, buy/upgrade a plan or move
   it into another organization.
2. Once this plan is approved, create the private disposable repository only if
   absent. If present inspect ownership/content and stop unless its disposable
   pilot purpose and exclusive ownership are established; do not overwrite it. Bootstrap
   `main` with `.github/workflows/branch-pilot.yml`, `pilot_canary.py` and a pilot
   README. Bootstrap precedes protection to avoid required-workflow initialization
   traps. Templates here are the exact proposed payloads.
3. Confirm PR-event `pilot-required` and App15368 on this target. Import
   only after capturing classic protection, all inherited applicable rules and
   bypass grants as required by `branch-policy-operations.md`. Capture the created
   Disabled rule's complete JSON, bypass actors and stable ID before activation.
   Use
   `templates/branch-pilot-ruleset.json` initially Disabled, read it back, then
   activate ONLY the created rule ID after matching parameters. It requires PR
   integration, strict `pilot-required` from that App, conversation resolution,
   rejects deletion/non-fast-forward updates and has no bypass actors. Solo
   review count0, no code-owner mandate, signing, metadata regex or queue. Do not
   weaken unrelated/inherited rules.
4. Record a passing PR at its actual required head/test-merge SHA. Attempt and
   record blocked PRs with failed canary, absent check and cancelled/failed
   dependency. A temporary conditional skip of `pilot-test` MUST fail the
   aggregator. Attempt direct push, force update and branch deletion as the
   approved pilot actor; record rejection and unchanged protected SHA. Keep
   recovery refs; attempts are confined to this disposable target.
5. If inherited policy or owner privileges bypass restrictions, expose exact
   actors/modes and failed assumptions. Do not invent another identity or bypass
   receipt. Restore experimental workflows through reviewed pilot PRs.
6. Exercise rollback of the created rule's enforcement state, restoring full
   prior JSON AND separately captured bypass settings. Read back and confirm
   baseline behavior; reapply approved rule and repeat unchanged readback and
   assessment. Record times, PRs, SHAs, rule ID, failures, restoration digests and
   owner decision. Retention/deletion requires a separate decision.

Private merge queue is excluded: the reviewed source requires organization-owned
Enterprise Cloud for private queues. `merge_group` remains in the workflow for a
future eligible reviewed policy. Rights/public release and wider estate adoption
remain separate. No raw upstream body or credential enters the pilot.
