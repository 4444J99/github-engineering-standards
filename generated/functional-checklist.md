# GitHub Engineering Standards — functional checklist

Version 0.1.0 — reviewed draft controls, not an exhaustive source consolidation.
Check a box only when scoped, current evidence satisfies the stated criterion.

## Act

- [ ] **GES-ACT-001 r1 — Workflow root permissions are explicitly read-only** (MUST; REVIEWED_DRAFT)
  Declare read-only or no default workflow permissions; separately justify job-scoped elevated privileges.
  Acceptance: Declare read-only or no default workflow permissions; separately justify job-scoped elevated privileges.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `workflow_permissions`; scope: repository.
  Applicability: `{'actions': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-ACT-002 r1 — Action and reusable-workflow references are immutable** (MUST; REVIEWED_DRAFT)
  Pin external action and reusable workflow uses to complete commit SHAs; container actions use image digests. Verify provenance and update safely.
  Acceptance: Pin external action and reusable workflow uses to complete commit SHAs; container actions use image digests. Verify provenance and update safely.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `workflow_pinning`; scope: repository.
  Applicability: `{'actions': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-ACT-003 r1 — Untrusted change execution is isolated** (MUST; REVIEWED_DRAFT)
  Do not execute untrusted pull-request content in privileged event contexts or expose secrets to it; validate expression and shell injection boundaries.
  Acceptance: Do not execute untrusted pull-request content in privileged event contexts or expose secrets to it; validate expression and shell injection boundaries.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{'actions': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-ACT-004 r1 — Privileged jobs have least authority** (MUST; REVIEWED_DRAFT)
  Review effective job permissions, secret availability, approval authority and reusable workflow trust boundaries.
  Acceptance: Review effective job permissions, secret availability, approval authority and reusable workflow trust boundaries.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{'actions': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-ACT-005 r1 — Runner isolation matches the threat model** (MUST; REVIEWED_DRAFT)
  Restrict self-hosted runners and groups, isolate untrusted jobs and demonstrate ephemeral cleanup or equivalent controls.
  Acceptance: Restrict self-hosted runners and groups, isolate untrusted jobs and demonstrate ephemeral cleanup or equivalent controls.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{'actions': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-ACT-006 r1 — Workflow credentials have bounded lifetimes** (MUST; REVIEWED_DRAFT)
  Prefer scoped short-lived credentials where supported; review OIDC trust subjects, audiences and allowed workflows.
  Acceptance: Prefer scoped short-lived credentials where supported; review OIDC trust subjects, audiences and allowed workflows.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{'actions': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

## Ai

- [ ] **GES-AI-001 r1 — AI tooling has an explicit access and review policy** (MUST; REVIEWED_DRAFT)
  Document approved tools and models, data boundaries, installation permissions, generated-change review and cost controls; treat source content as untrusted input.
  Acceptance: Document approved tools and models, data boundaries, installation permissions, generated-change review and cost controls; treat source content as untrusted input.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{'ai_tools': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

## Arc

- [ ] **GES-ARC-001 r1 — Function-owned repository boundaries** (MUST; REVIEWED_DRAFT)
  Define cohesive responsibilities, explicit cross-repository interfaces and independent change ownership; use the universe polyrepo default without creating arbitrary micro-repositories.
  Acceptance: Define cohesive responsibilities, explicit cross-repository interfaces and independent change ownership; use the universe polyrepo default without creating arbitrary micro-repositories.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-ARC-002 r1 — Dependency and interface contracts** (MUST; REVIEWED_DRAFT)
  Document module and service dependencies, version exposed interfaces and test backward compatibility or planned migrations.
  Acceptance: Document module and service dependencies, version exposed interfaces and test backward compatibility or planned migrations.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-ARC-003 r1 — Modular implementation and justified complexity** (MUST; REVIEWED_DRAFT)
  Favor reusable loosely coupled components; justify services, gateways and additional infrastructure by requirements rather than template presence.
  Acceptance: Favor reusable loosely coupled components; justify services, gateways and additional infrastructure by requirements rather than template presence.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-ARC-004 r1 — Reproducible development resources** (MUST; REVIEWED_DRAFT)
  Define supported technology versions and recreate ephemeral environments from configuration; identify non-ephemeral capacity needs.
  Acceptance: Define supported technology versions and recreate ephemeral environments from configuration; identify non-ephemeral capacity needs.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-ARC-005 r1 — Recovery of code and state** (MUST; REVIEWED_DRAFT)
  Test backup restoration, mistaken-history recovery and dependency reconstruction against explicit recovery objectives.
  Acceptance: Test backup restoration, mistaken-history recovery and dependency reconstruction against explicit recovery objectives.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-ARC-006 r1 — Service reliability and failure handling** (MUST; REVIEWED_DRAFT)
  Define fault tolerance, failure isolation and tested failover according to service criticality.
  Acceptance: Define fault tolerance, failure isolation and tested failover according to service criticality.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{'deployed_service': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-ARC-007 r1 — Performance and resource use are monitored** (MUST; REVIEWED_DRAFT)
  Measure actual load, resource utilization and bottlenecks; verify growth assumptions and avoid needless infrastructure.
  Acceptance: Measure actual load, resource utilization and bottlenecks; verify growth assumptions and avoid needless infrastructure.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{'deployed_service': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-ARC-008 r1 — Operational logs and retention** (MUST; REVIEWED_DRAFT)
  Provide actionable logs with controlled access, sensitive-data handling and approved retention.
  Acceptance: Provide actionable logs with controlled access, sensitive-data handling and approved retention.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{'deployed_service': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-ARC-009 r1 — Alerts have owners and response procedures** (MUST; REVIEWED_DRAFT)
  Set useful thresholds, route alerts to accountable responders and regularly test alert delivery and remediation.
  Acceptance: Set useful thresholds, route alerts to accountable responders and regularly test alert delivery and remediation.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{'deployed_service': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

## Art

- [ ] **GES-ART-001 r1 — Large artifacts use suitable storage** (MUST; REVIEWED_DRAFT)
  Route large binary or dataset artifacts to approved LFS, release or external storage, with access, retention and retrieval verification.
  Acceptance: Route large binary or dataset artifacts to approved LFS, release or external storage, with access, retention and retrieval verification.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

## Br

- [ ] **GES-BR-001 r1 — Bounded branch dependency depth** (MUST; REVIEWED_DRAFT)
  Use a comprehensible branch dependency strategy; deeply stacked branches require explicit lifecycle and merge-order handling.
  Acceptance: Use a comprehensible branch dependency strategy; deeply stacked branches require explicit lifecycle and merge-order handling.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-BR-002 r1 — Branch naming and cleanup are deliberate policy choices** (MUST; REVIEWED_DRAFT)
  Avoid imposing aesthetic branch-name or deletion rules without a delivery need; document any machine-readable constraints.
  Acceptance: Avoid imposing aesthetic branch-name or deletion rules without a delivery need; document any machine-readable constraints.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-BR-003 r1 — Merge strategy fits the repository contract** (MUST; REVIEWED_DRAFT)
  Choose merge, squash or rebase for integration needs; do not claim one history shape is universally correct.
  Acceptance: Choose merge, squash or rebase for integration needs; do not claim one history shape is universally correct.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-BR-004 r1 — Work is checkpointed and backed up** (MUST; REVIEWED_DRAFT)
  Publish useful development checkpoints before work is at risk; do not substitute commit volume for delivered value.
  Acceptance: Publish useful development checkpoints before work is at risk; do not substitute commit volume for delivered value.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-BR-005 r1 — Commit messages convey the change** (MUST; REVIEWED_DRAFT)
  Use meaningful change descriptions and normalize uninformative generated history where the selected merge strategy supports it.
  Acceptance: Use meaningful change descriptions and normalize uninformative generated history where the selected merge strategy supports it.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

## Ci

- [ ] **GES-CI-001 r1 — Default branch remains testable** (MUST; REVIEWED_DRAFT)
  Keep required tests passing on the default branch; treat a regression or flaky test as tracked remediation rather than normalization.
  Acceptance: Keep required tests passing on the default branch; treat a regression or flaky test as tracked remediation rather than normalization.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

## Com

- [ ] **GES-COM-001 r1 — Community conduct policy** (MUST; REVIEWED_DRAFT)
  Provide a nonempty community conduct policy at a recognized location. Content adequacy and inherited defaults require separate review.
  Acceptance: Provide a nonempty community conduct policy at a recognized location. Content adequacy and inherited defaults require separate review.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `file_present`; scope: repository.
  Applicability: `{'community': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-COM-002 r1 — Funding metadata** (MUST; REVIEWED_DRAFT)
  Provide a nonempty funding metadata at a recognized location. Content adequacy and inherited defaults require separate review.
  Acceptance: Provide a nonempty funding metadata at a recognized location. Content adequacy and inherited defaults require separate review.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `file_present`; scope: repository.
  Applicability: `{'funding': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-COM-003 r1 — Feedback is connected to engineering work** (MUST; REVIEWED_DRAFT)
  Keep decisions and feedback linked to versioned work; establish communication channels without leaking sensitive findings.
  Acceptance: Keep decisions and feedback linked to versioned work; establish communication channels without leaking sensitive findings.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{'accepts_contributions': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-COM-004 r1 — Contributors can onboard and learn** (MUST; REVIEWED_DRAFT)
  Test onboarding, document necessary tools and processes and support learning across experience levels.
  Acceptance: Test onboarding, document necessary tools and processes and support learning across experience levels.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{'accepts_contributions': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-COM-005 r1 — Project state is visible to authorized participants** (MUST; REVIEWED_DRAFT)
  Publish accurate work status and accountable ownership; use automation to reduce conflicting manual updates.
  Acceptance: Publish accurate work status and accountable ownership; use automation to reduce conflicting manual updates.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{'accepts_contributions': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

## Dep

- [ ] **GES-DEP-001 r1 — Dependency update configuration** (MUST; REVIEWED_DRAFT)
  Provide a nonempty dependency update configuration at a recognized location. Content adequacy and inherited defaults require separate review.
  Acceptance: Provide a nonempty dependency update configuration at a recognized location. Content adequacy and inherited defaults require separate review.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `file_present`; scope: repository.
  Applicability: `{'uses_dependabot': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

## Doc

- [ ] **GES-DOC-001 r1 — README file** (MUST; REVIEWED_DRAFT)
  Provide a nonempty readme file at a recognized location. Content adequacy and inherited defaults require separate review.
  Acceptance: Provide a nonempty readme file at a recognized location. Content adequacy and inherited defaults require separate review.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `file_present`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-DOC-002 r1 — Contribution guide** (MUST; REVIEWED_DRAFT)
  Provide a nonempty contribution guide at a recognized location. Content adequacy and inherited defaults require separate review.
  Acceptance: Provide a nonempty contribution guide at a recognized location. Content adequacy and inherited defaults require separate review.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `file_present`; scope: repository.
  Applicability: `{'accepts_contributions': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-DOC-003 r1 — Reproducible onboarding and usage** (MUST; REVIEWED_DRAFT)
  Document actual prerequisites, installation, configuration, repository structure and working examples; test the documented path from a clean environment.
  Acceptance: Document actual prerequisites, installation, configuration, repository structure and working examples; test the documented path from a clean environment.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-DOC-004 r1 — Documentation matches the proposed revision** (MUST; REVIEWED_DRAFT)
  Update interface documentation, environment-variable instructions, versions and operational examples alongside implementation changes.
  Acceptance: Update interface documentation, environment-variable instructions, versions and operational examples alongside implementation changes.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-DOC-005 r1 — No inherited placeholders or misdirected links** (MUST; REVIEWED_DRAFT)
  Replace source-specific names, accounts, example links, technology assumptions and promotional elements; validate rendered template outputs.
  Acceptance: Replace source-specific names, accounts, example links, technology assumptions and promotional elements; validate rendered template outputs.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-DOC-006 r1 — Developer documentation is version-correlated** (MUST; REVIEWED_DRAFT)
  Keep engineering documentation versioned with its implementation or maintain an explicit immutable cross-reference.
  Acceptance: Keep engineering documentation versioned with its implementation or maintain an explicit immutable cross-reference.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

## Gov

- [ ] **GES-GOV-001 r1 — Governance document** (MUST; REVIEWED_DRAFT)
  Provide a nonempty governance document at a recognized location. Content adequacy and inherited defaults require separate review.
  Acceptance: Provide a nonempty governance document at a recognized location. Content adequacy and inherited defaults require separate review.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `file_present`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-GOV-002 r1 — Ownership mapping** (MUST; REVIEWED_DRAFT)
  Provide a nonempty ownership mapping at a recognized location. Content adequacy and inherited defaults require separate review.
  Acceptance: Provide a nonempty ownership mapping at a recognized location. Content adequacy and inherited defaults require separate review.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `file_present`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-GOV-003 r1 — Role and permission assignments are explicit** (MUST; REVIEWED_DRAFT)
  Separate decision authority from platform administration; define access request, approval, offboarding and escalation procedures.
  Acceptance: Separate decision authority from platform administration; define access request, approval, offboarding and escalation procedures.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-GOV-004 r1 — Code owners are operationally valid** (MUST; REVIEWED_DRAFT)
  Validate ownership syntax, precedence, team visibility, write access and protection of the ownership file itself; prove required reviewer routing.
  Acceptance: Validate ownership syntax, precedence, team visibility, write access and protection of the ownership file itself; prove required reviewer routing.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-GOV-005 r1 — Review policy is risk- and staffing-aware** (MUST; REVIEWED_DRAFT)
  Choose explicit review thresholds and qualified reviewers per profile. Do not silently inherit two-person or elapsed-time waivers.
  Acceptance: Choose explicit review thresholds and qualified reviewers per profile. Do not silently inherit two-person or elapsed-time waivers.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-GOV-006 r1 — Exceptions are accountable and expire** (MUST; REVIEWED_DRAFT)
  Document owner, reason, compensating safeguard, approval and expiry for every exception. Preserve the underlying result and reopen expired decisions.
  Acceptance: Document owner, reason, compensating safeguard, approval and expiry for every exception. Preserve the underlying result and reopen expired decisions.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-GOV-007 r1 — Periodic access review** (MUST; REVIEWED_DRAFT)
  Review human, team, bot and external collaborator access; remove unnecessary privileges through approved changes.
  Acceptance: Review human, team, bot and external collaborator access; remove unnecessary privileges through approved changes.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-GOV-008 r1 — Audit retention and integrity** (MUST; REVIEWED_DRAFT)
  Retain actionable audit evidence with controlled access and approved retention; record collection gaps and investigate anomalies.
  Acceptance: Retain actionable audit evidence with controlled access and approved retention; record collection gaps and investigate anomalies.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-GOV-009 r1 — Versioned configuration and policy change** (MUST; REVIEWED_DRAFT)
  Maintain reviewed configuration and policy changes with traceable approvals and rollback information.
  Acceptance: Maintain reviewed configuration and policy changes with traceable approvals and rollback information.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-GOV-010 r1 — Governance feedback and training** (MUST; REVIEWED_DRAFT)
  Review governance policies, train affected contributors and close the loop on reported process failures.
  Acceptance: Review governance policies, train affected contributors and close the loop on reported process failures.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

## Iam

- [ ] **GES-IAM-001 r1 — Strong organization authentication** (MUST; REVIEWED_DRAFT)
  Verify the chosen organizational authentication policy, recovery arrangements and applicability of SSO or two-factor requirements.
  Acceptance: Verify the chosen organizational authentication policy, recovery arrangements and applicability of SSO or two-factor requirements.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: organization.
  Applicability: `{'organization': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-IAM-002 r1 — Provisioning and offboarding are reconciled** (MUST; REVIEWED_DRAFT)
  Reconcile authoritative identity records with active organization access and revoke obsolete entitlements.
  Acceptance: Reconcile authoritative identity records with active organization access and revoke obsolete entitlements.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: organization.
  Applicability: `{'organization': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-IAM-003 r1 — Enterprise server recovery is tested** (MUST; REVIEWED_DRAFT)
  Test backups and restores of the self-managed platform into an isolated environment; record restoration objectives and outcomes.
  Acceptance: Test backups and restores of the self-managed platform into an isolated environment; record restoration objectives and outcomes.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: enterprise.
  Applicability: `{'enterprise_server': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-IAM-004 r1 — Data residency and external obligations are scoped** (MUST; REVIEWED_DRAFT)
  Identify applicable contractual and regulatory obligations and record qualified review; do not certify compliance from a checklist alone.
  Acceptance: Identify applicable contractual and regulatory obligations and record qualified review; do not certify compliance from a checklist alone.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: organization.
  Applicability: `{'regulated': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

## Id

- [ ] **GES-ID-001 r1 — Repository description** (MUST; REVIEWED_DRAFT)
  Declare discoverable purpose and classification in repository metadata.
  Acceptance: Declare discoverable purpose and classification in repository metadata.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `metadata_nonempty`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-ID-002 r1 — Repository topics** (MUST; REVIEWED_DRAFT)
  Declare discoverable purpose and classification in repository metadata.
  Acceptance: Declare discoverable purpose and classification in repository metadata.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `metadata_nonempty`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-ID-003 r1 — Stable readable repository slug** (MUST; REVIEWED_DRAFT)
  Use a lowercase, single-hyphenated slug expressing enduring responsibility; record compatibility impacts before renaming.
  Acceptance: Use a lowercase, single-hyphenated slug expressing enduring responsibility; record compatibility impacts before renaming.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `repo_name`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-ID-004 r1 — Repository purpose and ownership classification** (MUST; REVIEWED_DRAFT)
  Identify function, lifecycle, criticality, accountable owner and repository type without encoding transient organizational hierarchy in the slug.
  Acceptance: Identify function, lifecycle, criticality, accountable owner and repository type without encoding transient organizational hierarchy in the slug.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-ID-005 r1 — Renames preserve external compatibility** (MUST; REVIEWED_DRAFT)
  Inventory and migrate consumers before a repository identity change; test consumers that do not follow redirects.
  Acceptance: Inventory and migrate consumers before a repository identity change; test consumers that do not follow redirects.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{'renaming': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

## Issue

- [ ] **GES-ISSUE-001 r1 — Bug report template** (MUST; REVIEWED_DRAFT)
  Provide a nonempty bug report template at a recognized location. Content adequacy and inherited defaults require separate review.
  Acceptance: Provide a nonempty bug report template at a recognized location. Content adequacy and inherited defaults require separate review.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `file_present`; scope: repository.
  Applicability: `{'uses_issues': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-ISSUE-002 r1 — Feature proposal template** (MUST; REVIEWED_DRAFT)
  Provide a nonempty feature proposal template at a recognized location. Content adequacy and inherited defaults require separate review.
  Acceptance: Provide a nonempty feature proposal template at a recognized location. Content adequacy and inherited defaults require separate review.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `file_present`; scope: repository.
  Applicability: `{'uses_issues': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-ISSUE-003 r1 — Issues and pull requests explain intent** (MUST; REVIEWED_DRAFT)
  Record enough context, behavior, constraints and acceptance criteria for a contributor other than the author to understand the work.
  Acceptance: Record enough context, behavior, constraints and acceptance criteria for a contributor other than the author to understand the work.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-ISSUE-004 r1 — Project boards do not fork the work record** (MUST; REVIEWED_DRAFT)
  Use project views to organize authoritative work items, not maintain a conflicting parallel backlog.
  Acceptance: Use project views to organize authoritative work items, not maintain a conflicting parallel backlog.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-ISSUE-005 r1 — Labels and milestones encode different dimensions** (MUST; REVIEWED_DRAFT)
  Use labels for categories and milestones for bounded deliverables with explicit completion scope and dates.
  Acceptance: Use labels for categories and milestones for bounded deliverables with explicit completion scope and dates.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

## Ops

- [ ] **GES-OPS-001 r1 — Automation has a value and maintenance case** (MUST; REVIEWED_DRAFT)
  Identify repetitive work and measure time, risk, cost and maintenance consequences before and after automation.
  Acceptance: Identify repetitive work and measure time, risk, cost and maintenance consequences before and after automation.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-002 r1 — Integrations have owners and contracts** (MUST; REVIEWED_DRAFT)
  Document integration purpose, ownership, APIs, error handling and ongoing support expectations.
  Acceptance: Document integration purpose, ownership, APIs, error handling and ongoing support expectations.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-003 r1 — Metrics reflect delivery and reliability** (MUST; REVIEWED_DRAFT)
  Use balanced leading and lagging indicators tied to outcomes; do not optimize commit, issue or pull-request counts as ends in themselves.
  Acceptance: Use balanced leading and lagging indicators tied to outcomes; do not optimize commit, issue or pull-request counts as ends in themselves.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-004 r1 — Feedback produces verified changes** (MUST; REVIEWED_DRAFT)
  Acknowledge input, prioritize a response, trace resulting changes and tell affected stakeholders what changed.
  Acceptance: Acknowledge input, prioritize a response, trace resulting changes and tell affected stakeholders what changed.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-005 r1 — Process interventions are piloted** (MUST; REVIEWED_DRAFT)
  Baseline bottlenecks, pilot improvements, assess costs and risks, and scale only after measuring results.
  Acceptance: Baseline bottlenecks, pilot improvements, assess costs and risks, and scale only after measuring results.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

## Pr

- [ ] **GES-PR-001 r1 — Pull request template** (MUST; REVIEWED_DRAFT)
  Provide a nonempty pull request template at a recognized location. Content adequacy and inherited defaults require separate review.
  Acceptance: Provide a nonempty pull request template at a recognized location. Content adequacy and inherited defaults require separate review.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `file_present`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-PR-002 r1 — Substantial changes reference planned work** (MUST; REVIEWED_DRAFT)
  Link substantive changes to a scoped issue; document the minor-change exception without manufacturing issue or commit quotas.
  Acceptance: Link substantive changes to a scoped issue; document the minor-change exception without manufacturing issue or commit quotas.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-PR-003 r1 — Merge and deployment responsibility is assigned** (MUST; REVIEWED_DRAFT)
  Assign a qualified merge owner and post-merge observer; author-led merging is a profile choice subject to permissions and absence handling.
  Acceptance: Assign a qualified merge owner and post-merge observer; author-led merging is a profile choice subject to permissions and absence handling.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-PR-004 r1 — Pull requests are focused and reviewable** (MUST; REVIEWED_DRAFT)
  Separate unrelated changes and keep the review scope coherent; define escalation for long-lived or large changes.
  Acceptance: Separate unrelated changes and keep the review scope coherent; define escalation for long-lived or large changes.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

## Rel

- [ ] **GES-REL-001 r1 — Release version and documentation correspond** (MUST; REVIEWED_DRAFT)
  Document release contents, versioned interface changes and accurate examples; adopt version semantics appropriate to the artifact.
  Acceptance: Document release contents, versioned interface changes and accurate examples; adopt version semantics appropriate to the artifact.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{'releases': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-REL-002 r1 — Deployment protection is configured and exercised** (MUST; REVIEWED_DRAFT)
  Scope production deployment branches, credentials, reviewers and rollback procedures; verify self-review and bypass decisions against risk.
  Acceptance: Scope production deployment branches, credentials, reviewers and rollback procedures; verify self-review and bypass decisions against risk.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{'deployed_service': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

## Rights

- [ ] **GES-RIGHTS-001 r1 — License and attribution are resolved** (MUST; REVIEWED_DRAFT)
  Identify rights and notices for source code, documentation, templates, datasets and media; preserve required attribution and withhold unsupported redistribution.
  Acceptance: Identify rights and notices for source code, documentation, templates, datasets and media; preserve required attribution and withhold unsupported redistribution.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-RIGHTS-002 r1 — Source conflicts have explicit disposition** (MUST; REVIEWED_DRAFT)
  Resolve conflicting authority, time thresholds, default paths and license statements; preserve rejected alternatives with rationale.
  Acceptance: Resolve conflicting authority, time thresholds, default paths and license statements; preserve rejected alternatives with rationale.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

## Rule

- [ ] **GES-RULE-001 r2 — Protected branch cannot be deleted** (MUST; REVIEWED_DRAFT)
  Reject deletion of the assessed protected branch under the effective active policy; evaluate legacy equivalents and bypass principals separately.
  Acceptance: Reject deletion of the assessed protected branch under the effective active policy; evaluate legacy equivalents and bypass principals separately.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `effective_rule`; scope: repository.
  Applicability: `{'protected_branch': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-RULE-002 r2 — Protected branch rejects non-fast-forward updates** (MUST; REVIEWED_DRAFT)
  Reject non-fast-forward updates to the assessed protected branch under the effective active policy; evaluate legacy equivalents and bypass principals separately.
  Acceptance: Reject non-fast-forward updates to the assessed protected branch under the effective active policy; evaluate legacy equivalents and bypass principals separately.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `effective_rule`; scope: repository.
  Applicability: `{'protected_branch': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-RULE-003 r2 — Pull request integration is required** (MUST; REVIEWED_DRAFT)
  Require changes to the assessed protected branch to be integrated through a pull request; review bypass paths separately from approval requirements.
  Acceptance: Require changes to the assessed protected branch to be integrated through a pull request; review bypass paths separately from approval requirements.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `effective_rule`; scope: repository.
  Applicability: `{'protected_branch': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-RULE-004 r2 — Approving review threshold matches policy** (MUST; REVIEWED_DRAFT)
  Require at least the target profile's explicitly adopted approval count for protected-branch pull requests; do not infer a universal two-review threshold or invent an independent solo reviewer.
  Acceptance: Require at least the target profile's explicitly adopted approval count for protected-branch pull requests; do not infer a universal two-review threshold or invent an independent solo reviewer.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `effective_rule`; scope: repository.
  Applicability: `{'protected_branch': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-RULE-005 r2 — Stale approvals are dismissed** (MUST; REVIEWED_DRAFT)
  Require the effective pull-request policy to dismiss stale approvals when pushed commits affect the reviewed diff; configuration presence does not prove native rejection behavior.
  Acceptance: Require the effective pull-request policy to dismiss stale approvals when pushed commits affect the reviewed diff; configuration presence does not prove native rejection behavior.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `effective_rule`; scope: repository.
  Applicability: `{'protected_branch': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-RULE-006 r2 — Review conversations are resolved** (MUST; REVIEWED_DRAFT)
  Require the effective pull-request policy to resolve review conversations before integration; do not substitute code-owner review or stale approval dismissal for this requirement.
  Acceptance: Require the effective pull-request policy to resolve review conversations before integration; do not substitute code-owner review or stale approval dismissal for this requirement.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `effective_rule`; scope: repository.
  Applicability: `{'protected_branch': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-RULE-007 r1 — Effective protection includes all inheritance and bypass paths** (MUST; REVIEWED_DRAFT)
  Inspect active rulesets, legacy protection, repository/organization inheritance and bypass permissions together. Exercise rejected and accepted changes in a safe test repository.
  Acceptance: Inspect active rulesets, legacy protection, repository/organization inheritance and bypass permissions together. Exercise rejected and accepted changes in a safe test repository.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{'protected_branch': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-RULE-008 r1 — Required checks execute on the right integration revision** (MUST; REVIEWED_DRAFT)
  Ensure required check names exist and run on the proposed or queued merge revision; validate triggers, filters and trusted publishers.
  Acceptance: Ensure required check names exist and run on the proposed or queued merge revision; validate triggers, filters and trusted publishers.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{'protected_branch': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-RULE-009 r1 — Signing and history policies have justified applicability** (SHOULD; REVIEWED_DRAFT)
  Decide commit-signing and history requirements by trust and delivery needs; verify compatibility with automated contributors before enabling them.
  Acceptance: Decide commit-signing and history requirements by trust and delivery needs; verify compatibility with automated contributors before enabling them.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{'protected_branch': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

## Sch

- [ ] **GES-SCH-001 r1 — Citation metadata** (MUST; REVIEWED_DRAFT)
  Provide a nonempty citation metadata at a recognized location. Content adequacy and inherited defaults require separate review.
  Acceptance: Provide a nonempty citation metadata at a recognized location. Content adequacy and inherited defaults require separate review.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `file_present`; scope: repository.
  Applicability: `{'scholarly': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-SCH-002 r1 — Scholarly citation identifies an actual work** (MUST; REVIEWED_DRAFT)
  Render valid citation metadata for the intended authors, version, date and publication rather than inheriting a template identity.
  Acceptance: Render valid citation metadata for the intended authors, version, date and publication rather than inheriting a template identity.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{'scholarly': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-SCH-003 r1 — Funding and promotional claims are verified** (MUST; REVIEWED_DRAFT)
  Use only intended support accounts, real deployment options and accurate badges; do not require stars or sponsorship as engineering compliance.
  Acceptance: Use only intended support accounts, real deployment options and accurate badges; do not require stars or sponsorship as engineering compliance.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{'funding': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

## Sec

- [ ] **GES-SEC-001 r1 — Security reporting policy** (MUST; REVIEWED_DRAFT)
  Provide a nonempty security reporting policy at a recognized location. Content adequacy and inherited defaults require separate review.
  Acceptance: Provide a nonempty security reporting policy at a recognized location. Content adequacy and inherited defaults require separate review.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `file_present`; scope: repository.
  Applicability: `{'software': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-SEC-002 r1 — Dependency vulnerabilities are scanned and triaged** (MUST; REVIEWED_DRAFT)
  Scan supported dependency ecosystems and maintain ownership, severity-based triage and remediation evidence.
  Acceptance: Scan supported dependency ecosystems and maintain ownership, severity-based triage and remediation evidence.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{'software': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-SEC-003 r1 — Security analysis runs in delivery workflows** (MUST; REVIEWED_DRAFT)
  Run supported code security analysis and verify the analyses actually completed on relevant revisions; maintain scan rules.
  Acceptance: Run supported code security analysis and verify the analyses actually completed on relevant revisions; maintain scan rules.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{'software': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-SEC-004 r1 — Credential exposure has a response path** (MUST; REVIEWED_DRAFT)
  Prevent secret disclosure, rotate or revoke exposed credentials and document remediation; removing text alone is not incident resolution.
  Acceptance: Prevent secret disclosure, rotate or revoke exposed credentials and document remediation; removing text alone is not incident resolution.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{'software': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-SEC-005 r1 — Threat modeling follows architecture changes** (MUST; REVIEWED_DRAFT)
  Identify assets, trust boundaries, adversaries and mitigations; update the model after material system changes.
  Acceptance: Identify assets, trust boundaries, adversaries and mitigations; update the model after material system changes.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{'software': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-SEC-006 r1 — Security findings receive risk-based remediation** (MUST; REVIEWED_DRAFT)
  Inventory and prioritize findings, record accepted risks and measure remediation age instead of only alert counts.
  Acceptance: Inventory and prioritize findings, record accepted risks and measure remediation age instead of only alert counts.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{'software': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-SEC-007 r1 — Incident response is rehearsed** (MUST; REVIEWED_DRAFT)
  Define response owners and escalation, test response procedures, preserve evidence and track improvements from exercises.
  Acceptance: Define response owners and escalation, test response procedures, preserve evidence and track improvements from exercises.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{'software': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-SEC-008 r1 — Third-party integrations are inventoried** (MUST; REVIEWED_DRAFT)
  Review application installation scope, permissions, owners, need and revocation paths; avoid assuming scanner omissions mean no apps exist.
  Acceptance: Review application installation scope, permissions, owners, need and revocation paths; avoid assuming scanner omissions mean no apps exist.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{'software': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-SEC-009 r1 — Security education is maintained** (MUST; REVIEWED_DRAFT)
  Provide appropriate secure-development guidance and track training applicability and completion.
  Acceptance: Provide appropriate secure-development guidance and track training applicability and completion.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{'software': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-SEC-010 r1 — Security testing is authorized and scoped** (MUST; REVIEWED_DRAFT)
  Plan relevant security testing with system owner authorization, bounded scope and tracked findings.
  Acceptance: Plan relevant security testing with system owner authorization, bounded scope and tracked findings.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{'software': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-SEC-011 r1 — Private disclosure channel works** (MUST; REVIEWED_DRAFT)
  Verify the stated security contact or private vulnerability reporting channel is reachable and monitored; state supported releases and disclosure expectations.
  Acceptance: Verify the stated security contact or private vulnerability reporting channel is reachable and monitored; state supported releases and disclosure expectations.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{'software': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

