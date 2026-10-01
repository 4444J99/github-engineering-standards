# GitHub Engineering Standards — functional checklist

Version 0.1.0 — reviewed draft controls, not an exhaustive source consolidation.
Check a box only when scoped, current evidence satisfies the stated criterion.

## Act

- [ ] **GES-ACT-007 r1 — GitHub Actions is not enabled on the GHES instance** (SHOULD; REVIEWED_DRAFT)
  Consider enabling GitHub Actions for CI/CD workflows. Ensure self-hosted runners are properly secured
  Acceptance: Consider enabling GitHub Actions for CI/CD workflows. Ensure self-hosted runners are properly secured; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: enterprise.
  Applicability: `{'enterprise_server': True, 'actions': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-ACT-008 r1 — GitHub Actions is enabled on the GHES instance** (MAY; REVIEWED_DRAFT)
  Ensure self-hosted runners are isolated, hardened, and do not run on the GHES appliance itself. Use ephemeral runners where possible
  Acceptance: Ensure self-hosted runners are isolated, hardened, and do not run on the GHES appliance itself. Use ephemeral runners where possible; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: enterprise.
  Applicability: `{'enterprise_server': True, 'actions': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-ACT-009 r1 — GitHub Actions status could not be confirmed on this GHES instance** (MAY; REVIEWED_DRAFT)
  A non-2xx response can mean (a) the feature is not supported on this GHES version, (b) the feature exists but is not licensed or enabled at the appliance level, or (c) the scanning token lacks the required scope. Verify which case applies before treating this as a misconfiguration
  Acceptance: A non-2xx response can mean (a) the feature is not supported on this GHES version, (b) the feature exists but is not licensed or enabled at the appliance level, or (c) the scanning token lacks the required scope. Verify which case applies before treating this as a misconfiguration; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: enterprise.
  Applicability: `{'enterprise_server': True, 'actions': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-ACT-010 r1 — Default GITHUB_TOKEN permission is write** (MUST; REVIEWED_DRAFT)
  Change the default workflow permission to 'read' in Organization → Settings → Actions → Workflow permissions. Grant write access only in individual workflows that explicitly require it.
  Acceptance: Change the default workflow permission to 'read' in Organization → Settings → Actions → Workflow permissions. Grant write access only in individual workflows that explicitly require it.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `actions_permissions`; scope: organization.
  Applicability: `{'organization': True, 'actions': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-ACT-011 r1 — GitHub Actions allows all third-party actions** (MUST; REVIEWED_DRAFT)
  Restrict allowed actions to 'local_only' or 'selected' (trusted publishers and verified creators) to reduce supply-chain risk.
  Acceptance: Restrict allowed actions to 'local_only' or 'selected' (trusted publishers and verified creators) to reduce supply-chain risk.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `actions_permissions`; scope: organization.
  Applicability: `{'organization': True, 'actions': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-ACT-012 r1 — Actions restricted to local repositories only** (MAY; REVIEWED_DRAFT)
  Consider using 'selected' to allow specific trusted third-party actions from verified creators, which provides a good balance of security and flexibility.
  Acceptance: Consider using 'selected' to allow specific trusted third-party actions from verified creators, which provides a good balance of security and flexibility.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `actions_permissions`; scope: organization.
  Applicability: `{'organization': True, 'actions': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

## Ai

- [ ] **GES-AI-002 r1 — Copilot allowed to suggest code matching public repositories** (MUST; REVIEWED_DRAFT)
  Set public code suggestions to 'blocked' to reduce IP and license risk from Copilot suggestions.
  Acceptance: Set public code suggestions to 'blocked' to reduce IP and license risk from Copilot suggestions.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: organization.
  Applicability: `{'organization': True, 'ai_tools': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-AI-003 r1 — Copilot CLI access enabled for the organization** (MAY; REVIEWED_DRAFT)
  Review whether CLI and agent mode access is appropriate for your organization's security posture. Consider restricting to specific teams if broad access is not needed.
  Acceptance: Review whether CLI and agent mode access is appropriate for your organization's security posture. Consider restricting to specific teams if broad access is not needed.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: organization.
  Applicability: `{'organization': True, 'ai_tools': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-AI-004 r1 — Copilot IDE chat is disabled** (MAY; REVIEWED_DRAFT)
  Consider enabling IDE chat to maximize Copilot's value for developers. IDE chat is the most impactful Copilot feature for developer productivity.
  Acceptance: Consider enabling IDE chat to maximize Copilot's value for developers. IDE chat is the most impactful Copilot feature for developer productivity.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: organization.
  Applicability: `{'organization': True, 'ai_tools': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-AI-005 r1 — Copilot platform chat enabled (GitHub.com / mobile)** (MAY; REVIEWED_DRAFT)
  Ensure your data governance policies cover Copilot usage on web and mobile platforms. Review content exclusion settings if sensitive repositories exist.
  Acceptance: Ensure your data governance policies cover Copilot usage on web and mobile platforms. Review content exclusion settings if sensitive repositories exist.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: organization.
  Applicability: `{'organization': True, 'ai_tools': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

## Com

- [ ] **GES-COM-006 r1 — GitHub Discussions not enabled** (MAY; REVIEWED_DRAFT)
  Consider enabling GitHub Discussions to provide a dedicated channel for community Q&A and to reduce noise in the issue tracker.
  Acceptance: Consider enabling GitHub Discussions to provide a dedicated channel for community Q&A and to reduce noise in the issue tracker.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `file_present`; scope: repository.
  Applicability: `{'community': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-COM-007 r1 — Repository has no description** (SHOULD; REVIEWED_DRAFT)
  Add a concise description to every repository to improve discoverability and help new contributors understand the project's purpose quickly.
  Acceptance: Add a concise description to every repository to improve discoverability and help new contributors understand the project's purpose quickly.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `file_present`; scope: repository.
  Applicability: `{'community': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-COM-008 r1 — Repository has no topics** (MAY; REVIEWED_DRAFT)
  Add relevant GitHub topics to this repository to improve searchability and enable org-wide automation based on topics.
  Acceptance: Add relevant GitHub topics to this repository to improve searchability and enable org-wide automation based on topics.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `file_present`; scope: repository.
  Applicability: `{'community': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

## Dep

- [ ] **GES-DEP-002 r1 — Dependabot alerts not enabled as enterprise default** (MUST; REVIEWED_DRAFT)
  Enable Dependabot alerts enterprise-wide to surface vulnerable dependencies across all organizations.
  Acceptance: Enable Dependabot alerts enterprise-wide to surface vulnerable dependencies across all organizations.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: enterprise.
  Applicability: `{'enterprise_server': True, 'uses_dependabot': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-DEP-003 r1 — Dependabot security updates not enabled as enterprise default** (SHOULD; REVIEWED_DRAFT)
  Enable Dependabot security updates enterprise-wide to automatically open pull requests that remediate vulnerable dependencies.
  Acceptance: Enable Dependabot security updates enterprise-wide to automatically open pull requests that remediate vulnerable dependencies.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: enterprise.
  Applicability: `{'enterprise_server': True, 'uses_dependabot': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-DEP-004 r1 — Dependency graph not enabled as enterprise default** (SHOULD; REVIEWED_DRAFT)
  Enable the dependency graph enterprise-wide to power Dependabot alerts and dependency review across all organizations.
  Acceptance: Enable the dependency graph enterprise-wide to power Dependabot alerts and dependency review across all organizations.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: enterprise.
  Applicability: `{'enterprise_server': True, 'uses_dependabot': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-DEP-005 r1 — Critical Dependabot alerts open across enterprise** (MUST; REVIEWED_DRAFT)
  Immediately remediate critical dependency vulnerabilities across all affected repositories and organizations in the enterprise.
  Acceptance: Immediately remediate critical dependency vulnerabilities across all affected repositories and organizations in the enterprise.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: enterprise.
  Applicability: `{'enterprise_server': True, 'uses_dependabot': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-DEP-006 r1 — High-severity Dependabot alerts open across enterprise** (MUST; REVIEWED_DRAFT)
  Prioritize fixing high-severity dependency vulnerabilities across all affected organizations and repositories.
  Acceptance: Prioritize fixing high-severity dependency vulnerabilities across all affected organizations and repositories.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: enterprise.
  Applicability: `{'enterprise_server': True, 'uses_dependabot': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-DEP-007 r1 — Critical Dependabot alerts open across the GHES instance** (MUST; REVIEWED_DRAFT)
  Immediately remediate critical dependency vulnerabilities across all organizations
  Acceptance: Immediately remediate critical dependency vulnerabilities across all organizations; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: enterprise.
  Applicability: `{'enterprise_server': True, 'uses_dependabot': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-DEP-008 r1 — High-severity Dependabot alerts open across the GHES instance** (MUST; REVIEWED_DRAFT)
  Prioritize fixing high-severity dependency vulnerabilities
  Acceptance: Prioritize fixing high-severity dependency vulnerabilities; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: enterprise.
  Applicability: `{'enterprise_server': True, 'uses_dependabot': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-DEP-009 r1 — Dependabot alerts are not enabled on the GHES instance** (MUST; REVIEWED_DRAFT)
  Enable Dependabot alerts to receive notifications about vulnerable dependencies
  Acceptance: Enable Dependabot alerts to receive notifications about vulnerable dependencies; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: enterprise.
  Applicability: `{'enterprise_server': True, 'uses_dependabot': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-DEP-010 r1 — Dependabot alerts status could not be confirmed on this GHES instance** (MAY; REVIEWED_DRAFT)
  A non-2xx response can mean (a) the feature is not supported on this GHES version, (b) the feature exists but is not licensed or enabled at the appliance level, or (c) the scanning token lacks the required scope. Verify which case applies before treating this as a misconfiguration
  Acceptance: A non-2xx response can mean (a) the feature is not supported on this GHES version, (b) the feature exists but is not licensed or enabled at the appliance level, or (c) the scanning token lacks the required scope. Verify which case applies before treating this as a misconfiguration; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: enterprise.
  Applicability: `{'enterprise_server': True, 'uses_dependabot': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-DEP-011 r1 — Dependabot security updates are not enabled on the GHES instance** (SHOULD; REVIEWED_DRAFT)
  Enable Dependabot security updates to automatically create PRs that fix vulnerable dependencies
  Acceptance: Enable Dependabot security updates to automatically create PRs that fix vulnerable dependencies; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: enterprise.
  Applicability: `{'enterprise_server': True, 'uses_dependabot': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-DEP-012 r1 — Dependabot alerts API could not be confirmed on this GHES instance** (MAY; REVIEWED_DRAFT)
  A non-2xx response can mean (a) the feature is not supported on this GHES version, (b) the feature exists but is not licensed or enabled at the appliance level, or (c) the scanning token lacks the required scope. Verify which case applies before treating this as a misconfiguration
  Acceptance: A non-2xx response can mean (a) the feature is not supported on this GHES version, (b) the feature exists but is not licensed or enabled at the appliance level, or (c) the scanning token lacks the required scope. Verify which case applies before treating this as a misconfiguration; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: enterprise.
  Applicability: `{'enterprise_server': True, 'uses_dependabot': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-DEP-013 r1 — Critical Dependabot alerts open across organization** (MUST; REVIEWED_DRAFT)
  Immediately remediate critical dependency vulnerabilities across all affected repositories.
  Acceptance: Immediately remediate critical dependency vulnerabilities across all affected repositories.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: organization.
  Applicability: `{'organization': True, 'uses_dependabot': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-DEP-014 r1 — High-severity Dependabot alerts open across organization** (MUST; REVIEWED_DRAFT)
  Prioritize fixing high-severity dependency vulnerabilities across all affected repositories.
  Acceptance: Prioritize fixing high-severity dependency vulnerabilities across all affected repositories.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: organization.
  Applicability: `{'organization': True, 'uses_dependabot': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-DEP-015 r1 — Open Dependabot alerts across organization** (SHOULD; REVIEWED_DRAFT)
  Review and remediate all remaining open Dependabot alerts across the organization.
  Acceptance: Review and remediate all remaining open Dependabot alerts across the organization.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: organization.
  Applicability: `{'organization': True, 'uses_dependabot': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-DEP-016 r1 — Dependabot alerts not enabled by default for new repositories** (MUST; REVIEWED_DRAFT)
  Enable 'Dependabot alerts' in Organization → Settings → Code security and analysis to apply this protection automatically to all new repositories.
  Acceptance: Enable 'Dependabot alerts' in Organization → Settings → Code security and analysis to apply this protection automatically to all new repositories.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: organization.
  Applicability: `{'organization': True, 'uses_dependabot': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-DEP-017 r1 — Dependabot security updates not enabled by default for new repositories** (SHOULD; REVIEWED_DRAFT)
  Enable 'Dependabot security updates' in Organization → Settings → Code security and analysis.
  Acceptance: Enable 'Dependabot security updates' in Organization → Settings → Code security and analysis.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: organization.
  Applicability: `{'organization': True, 'uses_dependabot': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-DEP-018 r1 — Dependency graph not enabled by default for new repositories** (SHOULD; REVIEWED_DRAFT)
  Enable the dependency graph in Organization → Settings → Code security and analysis.
  Acceptance: Enable the dependency graph in Organization → Settings → Code security and analysis.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: organization.
  Applicability: `{'organization': True, 'uses_dependabot': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

## Gov

- [ ] **GES-GOV-011 r1 — High number of site administrators on the GHES instance** (MUST; REVIEWED_DRAFT)
  Limit site admin access to the minimum number of trusted administrators. Follow the principle of least privilege
  Acceptance: Limit site admin access to the minimum number of trusted administrators. Follow the principle of least privilege; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: enterprise.
  Applicability: `{'enterprise_server': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-GOV-012 r1 — Default repository permission set to admin** (MUST; REVIEWED_DRAFT)
  Change the default repository permission to 'read' or 'write' to ensure members only have the minimum access required.
  Acceptance: Change the default repository permission to 'read' or 'write' to ensure members only have the minimum access required.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: organization.
  Applicability: `{'organization': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-GOV-013 r1 — Members can create public repositories** (SHOULD; REVIEWED_DRAFT)
  Consider restricting public repository creation to organization owners or admins to prevent accidental data exposure.
  Acceptance: Consider restricting public repository creation to organization owners or admins to prevent accidental data exposure.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: organization.
  Applicability: `{'organization': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-GOV-014 r1 — No security manager team assigned** (SHOULD; REVIEWED_DRAFT)
  Assign a security manager team to ensure that security alerts and configurations are reviewed by the right people.
  Acceptance: Assign a security manager team to ensure that security alerts and configurations are reviewed by the right people.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: organization.
  Applicability: `{'organization': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-GOV-015 r1 — Excessive admin collaborators** (MUST; REVIEWED_DRAFT)
  Review admin access and apply the principle of least privilege. Consider using teams with limited permissions instead of direct admin grants.
  Acceptance: Review admin access and apply the principle of least privilege. Consider using teams with limited permissions instead of direct admin grants.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-GOV-016 r1 — Direct collaborators instead of teams** (SHOULD; REVIEWED_DRAFT)
  Prefer team-based access over direct collaborators for better auditability and easier access management.
  Acceptance: Prefer team-based access over direct collaborators for better auditability and easier access management.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-GOV-017 r1 — No CODEOWNERS file found** (SHOULD; REVIEWED_DRAFT)
  Add a CODEOWNERS file to assign code ownership and ensure that changes to sensitive paths require review from the appropriate team.
  Acceptance: Add a CODEOWNERS file to assign code ownership and ensure that changes to sensitive paths require review from the appropriate team.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `codeowners_validation`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

## Iam

- [ ] **GES-IAM-005 r1 — Password authentication is enabled on the GHES instance** (MUST; REVIEWED_DRAFT)
  Consider disabling password authentication in favor of SSO (SAML/LDAP) to enforce stronger authentication controls
  Acceptance: Consider disabling password authentication in favor of SSO (SAML/LDAP) to enforce stronger authentication controls; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: enterprise.
  Applicability: `{'enterprise_server': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-IAM-006 r1 — GHES is using built-in authentication instead of an external identity provider** (MUST; REVIEWED_DRAFT)
  Configure SAML SSO or LDAP authentication to integrate with your enterprise identity provider. Built-in authentication lacks centralized user lifecycle management
  Acceptance: Configure SAML SSO or LDAP authentication to integrate with your enterprise identity provider. Built-in authentication lacks centralized user lifecycle management; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: enterprise.
  Applicability: `{'enterprise_server': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-IAM-007 r1 — GHES authentication mode observed** (MAY; REVIEWED_DRAFT)
  External authentication provider is configured
  Acceptance: External authentication provider is configured; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: enterprise.
  Applicability: `{'enterprise_server': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-IAM-008 r1 — Open signup is enabled on the GHES instance** (MUST; REVIEWED_DRAFT)
  Disable open signup to prevent unauthorized users from creating accounts. Use your identity provider for user provisioning
  Acceptance: Disable open signup to prevent unauthorized users from creating accounts. Use your identity provider for user provisioning; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: enterprise.
  Applicability: `{'enterprise_server': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-IAM-009 r1 — High percentage of GHES users are suspended** (SHOULD; REVIEWED_DRAFT)
  Review user account hygiene. Consider removing or archiving suspended accounts if no longer needed
  Acceptance: Review user account hygiene. Consider removing or archiving suspended accounts if no longer needed; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: enterprise.
  Applicability: `{'enterprise_server': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

## Ops

- [ ] **GES-OPS-006 r1 — No billing budgets configured** (MUST; REVIEWED_DRAFT)
  Configure at least one budget at the enterprise level to establish spending limits and enable cost governance. Consider adding budgets at the organization and cost center levels as well.
  Acceptance: Configure at least one budget at the enterprise level to establish spending limits and enable cost governance. Consider adding budgets at the organization and cost center levels as well.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: enterprise.
  Applicability: `{'enterprise_server': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-007 r1 — No budgets have alerting enabled** (MUST; REVIEWED_DRAFT)
  Enable alerting on at least one budget and configure alert recipients (enterprise admins or billing managers) to receive notifications when spending thresholds are approached.
  Acceptance: Enable alerting on at least one budget and configure alert recipients (enterprise admins or billing managers) to receive notifications when spending thresholds are approached.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: enterprise.
  Applicability: `{'enterprise_server': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-008 r1 — Budgets without usage prevention when exceeded** (SHOULD; REVIEWED_DRAFT)
  Enable "prevent further usage" on budgets where hard spending caps are required. For advisory-only budgets, ensure alerting is enabled so overages are at least visible.
  Acceptance: Enable "prevent further usage" on budgets where hard spending caps are required. For advisory-only budgets, ensure alerting is enabled so overages are at least visible.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: enterprise.
  Applicability: `{'enterprise_server': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-009 r1 — Administrative SSH access is enabled on the GHES instance** (SHOULD; REVIEWED_DRAFT)
  Review SSH access policies. Consider restricting SSH access to specific IP ranges and ensure SSH keys are regularly rotated
  Acceptance: Review SSH access policies. Consider restricting SSH access to specific IP ranges and ensure SSH keys are regularly rotated; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: enterprise.
  Applicability: `{'enterprise_server': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-010 r1 — GHES management settings could not be read; configuration checks were skipped** (MAY; REVIEWED_DRAFT)
  Provide a site-admin token with access to /manage/v1/config/settings so subdomain isolation, private mode, GHAS enablement, and related checks can run
  Acceptance: Provide a site-admin token with access to /manage/v1/config/settings so subdomain isolation, private mode, GHAS enablement, and related checks can run; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: enterprise.
  Applicability: `{'enterprise_server': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-011 r1 — GHES backup configuration cannot be verified automatically** (MUST; REVIEWED_DRAFT)
  Manually verify that GitHub Enterprise Server Backup Utilities (backup-utils) are configured, run on a schedule, and tested regularly for restoration
  Acceptance: Manually verify that GitHub Enterprise Server Backup Utilities (backup-utils) are configured, run on a schedule, and tested regularly for restoration; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: enterprise.
  Applicability: `{'enterprise_server': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-012 r1 — High availability (HA) replica configuration cannot be verified automatically** (SHOULD; REVIEWED_DRAFT)
  Manually verify that a replica is configured for failover if high availability is required for your deployment
  Acceptance: Manually verify that a replica is configured for failover if high availability is required for your deployment; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: enterprise.
  Applicability: `{'enterprise_server': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-013 r1 — GHES user population summary** (MAY; REVIEWED_DRAFT)
  Regularly audit user accounts and admin access
  Acceptance: Regularly audit user accounts and admin access; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: enterprise.
  Applicability: `{'enterprise_server': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-014 r1 — GHES organization summary** (MAY; REVIEWED_DRAFT)
  Monitor organization growth and ensure governance policies are enforced
  Acceptance: Monitor organization growth and ensure governance policies are enforced; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: enterprise.
  Applicability: `{'enterprise_server': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-015 r1 — GHES repository summary** (MAY; REVIEWED_DRAFT)
  Monitor repository growth and storage consumption
  Acceptance: Monitor repository growth and storage consumption; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: enterprise.
  Applicability: `{'enterprise_server': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-016 r1 — Disabled organisations present on the GHES instance** (MAY; REVIEWED_DRAFT)
  Review disabled organizations and consider removing them if no longer needed
  Acceptance: Review disabled organizations and consider removing them if no longer needed; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: enterprise.
  Applicability: `{'enterprise_server': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-017 r1 — Subdomain isolation is not enabled** (MUST; REVIEWED_DRAFT)
  Enable subdomain isolation to prevent cross-site scripting attacks. This is critical for security and should always be enabled in production
  Acceptance: Enable subdomain isolation to prevent cross-site scripting attacks. This is critical for security and should always be enabled in production; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: enterprise.
  Applicability: `{'enterprise_server': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-018 r1 — Private mode is disabled** (MUST; REVIEWED_DRAFT)
  Enable private mode so all access (UI, API, and Git over HTTPS) requires authentication. Private mode is expected for any production or internal GHES appliance; leave it disabled only for instances intentionally exposed to the public internet
  Acceptance: Enable private mode so all access (UI, API, and Git over HTTPS) requires authentication. Private mode is expected for any production or internal GHES appliance; leave it disabled only for instances intentionally exposed to the public internet; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: enterprise.
  Applicability: `{'enterprise_server': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-019 r1 — Public GitHub Pages are enabled on the GHES instance** (SHOULD; REVIEWED_DRAFT)
  Consider disabling public Pages if the instance is internal-only to prevent accidental content exposure
  Acceptance: Consider disabling public Pages if the instance is internal-only to prevent accidental content exposure; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: enterprise.
  Applicability: `{'enterprise_server': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-020 r1 — GitHub Pages is enabled while subdomain isolation is disabled** (MUST; REVIEWED_DRAFT)
  Enable subdomain isolation before (or instead of) enabling GitHub Pages. GitHub documents subdomain isolation as a prerequisite for safely serving Pages from a GHES appliance
  Acceptance: Enable subdomain isolation before (or instead of) enabling GitHub Pages. GitHub documents subdomain isolation as a prerequisite for safely serving Pages from a GHES appliance; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: enterprise.
  Applicability: `{'enterprise_server': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-021 r1 — GHES license is expiring soon** (MUST; REVIEWED_DRAFT)
  Plan your GHES license renewal — contact GitHub Sales
  Acceptance: Plan your GHES license renewal — contact GitHub Sales; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: enterprise.
  Applicability: `{'enterprise_server': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-022 r1 — GHES license expires within 30 days** (MUST; REVIEWED_DRAFT)
  Renew your GitHub Enterprise Server license immediately to avoid service interruption
  Acceptance: Renew your GitHub Enterprise Server license immediately to avoid service interruption; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: enterprise.
  Applicability: `{'enterprise_server': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-023 r1 — GHES license seat utilisation is high** (MUST; REVIEWED_DRAFT)
  You are approaching your license seat limit. Consider purchasing additional seats or reviewing inactive users
  Acceptance: You are approaching your license seat limit. Consider purchasing additional seats or reviewing inactive users; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: enterprise.
  Applicability: `{'enterprise_server': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-024 r1 — GHES license seat utilisation summary** (MAY; REVIEWED_DRAFT)
  Monitor seat utilization regularly
  Acceptance: Monitor seat utilization regularly; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: enterprise.
  Applicability: `{'enterprise_server': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-025 r1 — GHES license is unlimited** (MAY; REVIEWED_DRAFT)
  Unlimited seats — monitor active user growth for capacity planning
  Acceptance: Unlimited seats — monitor active user growth for capacity planning; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: enterprise.
  Applicability: `{'enterprise_server': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-026 r1 — GHES instance version detected** (MAY; REVIEWED_DRAFT)
  Keep your GHES instance up-to-date with the latest patch release to receive security fixes and improvements
  Acceptance: Keep your GHES instance up-to-date with the latest patch release to receive security fixes and improvements; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: enterprise.
  Applicability: `{'enterprise_server': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-027 r1 — GHES version is within the supported release window** (MAY; REVIEWED_DRAFT)
  No action needed — continue tracking new GHES releases for upcoming upgrades
  Acceptance: No action needed — continue tracking new GHES releases for upcoming upgrades; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: enterprise.
  Applicability: `{'enterprise_server': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-028 r1 — GHES version is no longer in support** (MUST; REVIEWED_DRAFT)
  Upgrade to a supported release. GitHub only ships security patches for the latest 3 minor versions
  Acceptance: Upgrade to a supported release. GitHub only ships security patches for the latest 3 minor versions; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: enterprise.
  Applicability: `{'enterprise_server': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-029 r1 — GHES version string could not be parsed** (SHOULD; REVIEWED_DRAFT)
  Confirm the appliance reports a standard semantic version via /meta
  Acceptance: Confirm the appliance reports a standard semantic version via /meta; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: enterprise.
  Applicability: `{'enterprise_server': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-030 r1 — GHES server version could not be determined** (SHOULD; REVIEWED_DRAFT)
  Ensure the token has sufficient permissions to read server metadata
  Acceptance: Ensure the token has sufficient permissions to read server metadata; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: enterprise.
  Applicability: `{'enterprise_server': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-031 r1 — GHES instance is currently in maintenance mode** (MUST; REVIEWED_DRAFT)
  Maintenance mode prevents user access. Ensure this is intentional and plan to disable it after maintenance is complete
  Acceptance: Maintenance mode prevents user access. Ensure this is intentional and plan to disable it after maintenance is complete; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: enterprise.
  Applicability: `{'enterprise_server': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-032 r1 — Copilot seats assigned to all organization members** (SHOULD; REVIEWED_DRAFT)
  Switch to 'assign_selected' to control costs and limit Copilot access to members who actively use it.
  Acceptance: Switch to 'assign_selected' to control costs and limit Copilot access to members who actively use it.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: organization.
  Applicability: `{'organization': True, 'ai_tools': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-033 r1 — High percentage of inactive Copilot seats** (SHOULD; REVIEWED_DRAFT)
  Reclaim unused Copilot seats to reduce costs. Review seat assignments and remove seats for members who are not actively using Copilot.
  Acceptance: Reclaim unused Copilot seats to reduce costs. Review seat assignments and remove seats for members who are not actively using Copilot.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: organization.
  Applicability: `{'organization': True, 'ai_tools': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-034 r1 — Issues and Discussions both disabled** (MAY; REVIEWED_DRAFT)
  Consider enabling Issues or Discussions to provide a structured channel for community feedback and bug reports.
  Acceptance: Consider enabling Issues or Discussions to provide a structured channel for community feedback and bug reports.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-035 r1 — Auto-delete branches on merge not enabled** (MAY; REVIEWED_DRAFT)
  Enable auto-delete branch after merge in repository settings to keep the repository clean.
  Acceptance: Enable auto-delete branch after merge in repository settings to keep the repository clean.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-036 r1 — Repository appears dormant but is not archived** (MAY; REVIEWED_DRAFT)
  Archive inactive repositories to reduce maintenance burden and signal to developers that the project is no longer actively maintained.
  Acceptance: Archive inactive repositories to reduce maintenance burden and signal to developers that the project is no longer actively maintained.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-037 r1 — Ensure automated scanning of dependencies for vulnerabilities.** (SHOULD; REVIEWED_DRAFT)
  Ensure automated scanning of dependencies for vulnerabilities.
  Acceptance: Ensure automated scanning of dependencies for vulnerabilities.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-038 r1 — Regularly update dependency scanning tools.** (SHOULD; REVIEWED_DRAFT)
  Regularly update dependency scanning tools.
  Acceptance: Regularly update dependency scanning tools.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-039 r1 — Review and address identified vulnerabilities promptly.** (SHOULD; REVIEWED_DRAFT)
  Review and address identified vulnerabilities promptly.
  Acceptance: Review and address identified vulnerabilities promptly.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-040 r1 — Implement code scanning tools to identify potential security issues.** (SHOULD; REVIEWED_DRAFT)
  Implement code scanning tools to identify potential security issues.
  Acceptance: Implement code scanning tools to identify potential security issues.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-041 r1 — Integrate code scanning into the CI/CD pipeline.** (SHOULD; REVIEWED_DRAFT)
  Integrate code scanning into the CI/CD pipeline.
  Acceptance: Integrate code scanning into the CI/CD pipeline.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-042 r1 — Regularly review and update scanning rules and configurations.** (SHOULD; REVIEWED_DRAFT)
  Regularly review and update scanning rules and configurations.
  Acceptance: Regularly review and update scanning rules and configurations.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-043 r1 — Assess practices for managing secrets and sensitive information.** (SHOULD; REVIEWED_DRAFT)
  Assess practices for managing secrets and sensitive information.
  Acceptance: Assess practices for managing secrets and sensitive information.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-044 r1 — Use secret management tools to store and manage secrets.** (SHOULD; REVIEWED_DRAFT)
  Use secret management tools to store and manage secrets.
  Acceptance: Use secret management tools to store and manage secrets.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-045 r1 — Regularly rotate secrets and credentials.** (SHOULD; REVIEWED_DRAFT)
  Regularly rotate secrets and credentials.
  Acceptance: Regularly rotate secrets and credentials.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-046 r1 — Review the presence and enforcement of security policies and guidelines.** (SHOULD; REVIEWED_DRAFT)
  Review the presence and enforcement of security policies and guidelines.
  Acceptance: Review the presence and enforcement of security policies and guidelines.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-047 r1 — Ensure policies are accessible to all team members.** (SHOULD; REVIEWED_DRAFT)
  Ensure policies are accessible to all team members.
  Acceptance: Ensure policies are accessible to all team members.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-048 r1 — Regularly update policies to reflect new threats and best practices.** (SHOULD; REVIEWED_DRAFT)
  Regularly update policies to reflect new threats and best practices.
  Acceptance: Regularly update policies to reflect new threats and best practices.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-049 r1 — Establish and enforce secure coding guidelines across all development teams.** (SHOULD; REVIEWED_DRAFT)
  Establish and enforce secure coding guidelines across all development teams.
  Acceptance: Establish and enforce secure coding guidelines across all development teams.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-050 r1 — Provide training on secure coding practices.** (SHOULD; REVIEWED_DRAFT)
  Provide training on secure coding practices.
  Acceptance: Provide training on secure coding practices.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-051 r1 — Conduct code reviews to ensure adherence to guidelines.** (SHOULD; REVIEWED_DRAFT)
  Conduct code reviews to ensure adherence to guidelines.
  Acceptance: Conduct code reviews to ensure adherence to guidelines.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-052 r1 — Implement strict access controls and regularly review permissions.** (SHOULD; REVIEWED_DRAFT)
  Implement strict access controls and regularly review permissions.
  Acceptance: Implement strict access controls and regularly review permissions.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-053 r1 — Use role-based access control (RBAC) to limit access to GitHub and other busines...** (SHOULD; REVIEWED_DRAFT)
  Use role-based access control (RBAC) to limit access to GitHub and other business systems.
  Acceptance: Use role-based access control (RBAC) to limit access to GitHub and other business systems.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-054 r1 — Regularly audit access logs for suspicious activity for GitHub and other busines...** (SHOULD; REVIEWED_DRAFT)
  Regularly audit access logs for suspicious activity for GitHub and other business systems.
  Acceptance: Regularly audit access logs for suspicious activity for GitHub and other business systems.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-055 r1 — List regulations and standards your organization must comply with (e.g., GDPR, H...** (SHOULD; REVIEWED_DRAFT)
  List regulations and standards your organization must comply with (e.g., GDPR, HIPAA).
  Acceptance: List regulations and standards your organization must comply with (e.g., GDPR, HIPAA).; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-056 r1 — Ensure compliance with relevant regulations and standards (e.g., GDPR, HIPAA).** (SHOULD; REVIEWED_DRAFT)
  Ensure compliance with relevant regulations and standards (e.g., GDPR, HIPAA).
  Acceptance: Ensure compliance with relevant regulations and standards (e.g., GDPR, HIPAA).; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-057 r1 — Conduct regular compliance audits.** (SHOULD; REVIEWED_DRAFT)
  Conduct regular compliance audits.
  Acceptance: Conduct regular compliance audits.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-058 r1 — Maintain documentation of compliance efforts.** (SHOULD; REVIEWED_DRAFT)
  Maintain documentation of compliance efforts.
  Acceptance: Maintain documentation of compliance efforts.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-059 r1 — Implement comprehensive audit logging for all critical actions and access.** (SHOULD; REVIEWED_DRAFT)
  Implement comprehensive audit logging for all critical actions and access.
  Acceptance: Implement comprehensive audit logging for all critical actions and access.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-060 r1 — Ensure logs are tamper-proof and securely stored, including RBAC for these artif...** (SHOULD; REVIEWED_DRAFT)
  Ensure logs are tamper-proof and securely stored, including RBAC for these artifacts.
  Acceptance: Ensure logs are tamper-proof and securely stored, including RBAC for these artifacts.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-061 r1 — Regularly review audit logs for anomalies.** (SHOULD; REVIEWED_DRAFT)
  Regularly review audit logs for anomalies.
  Acceptance: Regularly review audit logs for anomalies.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-062 r1 — Verify and/or request data protection practices from GitHub and other business s...** (SHOULD; REVIEWED_DRAFT)
  Verify and/or request data protection practices from GitHub and other business systems.
  Acceptance: Verify and/or request data protection practices from GitHub and other business systems.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-063 r1 — Use strong encryption algorithms and key management practices.** (SHOULD; REVIEWED_DRAFT)
  Use strong encryption algorithms and key management practices.
  Acceptance: Use strong encryption algorithms and key management practices.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-064 r1 — Regularly test encryption mechanisms for effectiveness.** (SHOULD; REVIEWED_DRAFT)
  Regularly test encryption mechanisms for effectiveness.
  Acceptance: Regularly test encryption mechanisms for effectiveness.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-065 r1 — Develop and regularly update an incident response plan.** (SHOULD; REVIEWED_DRAFT)
  Develop and regularly update an incident response plan.
  Acceptance: Develop and regularly update an incident response plan.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-066 r1 — Conduct regular incident response drills.** (SHOULD; REVIEWED_DRAFT)
  Conduct regular incident response drills.
  Acceptance: Conduct regular incident response drills.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-067 r1 — Ensure all team members are aware of their roles in the plan.** (SHOULD; REVIEWED_DRAFT)
  Ensure all team members are aware of their roles in the plan.
  Acceptance: Ensure all team members are aware of their roles in the plan.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-068 r1 — Provide regular compliance training for all team members.** (SHOULD; REVIEWED_DRAFT)
  Provide regular compliance training for all team members.
  Acceptance: Provide regular compliance training for all team members.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-069 r1 — Include training on new regulations and standards.** (SHOULD; REVIEWED_DRAFT)
  Include training on new regulations and standards.
  Acceptance: Include training on new regulations and standards.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-070 r1 — Track and document training completion.** (SHOULD; REVIEWED_DRAFT)
  Track and document training completion.
  Acceptance: Track and document training completion.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-071 r1 — Conduct regular threat modeling exercises to identify potential vulnerabilities.** (SHOULD; REVIEWED_DRAFT)
  Conduct regular threat modeling exercises to identify potential vulnerabilities.
  Acceptance: Conduct regular threat modeling exercises to identify potential vulnerabilities.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-072 r1 — Involve cross-functional teams in threat modeling.** (SHOULD; REVIEWED_DRAFT)
  Involve cross-functional teams in threat modeling.
  Acceptance: Involve cross-functional teams in threat modeling.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-073 r1 — Update threat models to reflect new threats and changes in the environment.** (SHOULD; REVIEWED_DRAFT)
  Update threat models to reflect new threats and changes in the environment.
  Acceptance: Update threat models to reflect new threats and changes in the environment.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-074 r1 — Perform regular penetration testing to identify and mitigate security weaknesses...** (SHOULD; REVIEWED_DRAFT)
  Perform regular penetration testing to identify and mitigate security weaknesses.
  Acceptance: Perform regular penetration testing to identify and mitigate security weaknesses.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-075 r1 — Use both internal and external testers for comprehensive coverage.** (SHOULD; REVIEWED_DRAFT)
  Use both internal and external testers for comprehensive coverage.
  Acceptance: Use both internal and external testers for comprehensive coverage.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-076 r1 — Address findings from penetration tests promptly.** (SHOULD; REVIEWED_DRAFT)
  Address findings from penetration tests promptly.
  Acceptance: Address findings from penetration tests promptly.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-077 r1 — Document and track remediation efforts.** (SHOULD; REVIEWED_DRAFT)
  Document and track remediation efforts.
  Acceptance: Document and track remediation efforts.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-078 r1 — Ensure timely application of security patches and updates.** (SHOULD; REVIEWED_DRAFT)
  Ensure timely application of security patches and updates.
  Acceptance: Ensure timely application of security patches and updates.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-079 r1 — Automate patch management where possible.** (SHOULD; REVIEWED_DRAFT)
  Automate patch management where possible.
  Acceptance: Automate patch management where possible.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-080 r1 — Maintain an inventory of all software and hardware to track updates.** (SHOULD; REVIEWED_DRAFT)
  Maintain an inventory of all software and hardware to track updates.
  Acceptance: Maintain an inventory of all software and hardware to track updates.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-081 r1 — Implement a robust vulnerability management program.** (SHOULD; REVIEWED_DRAFT)
  Implement a robust vulnerability management program.
  Acceptance: Implement a robust vulnerability management program.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-082 r1 — Regularly scan for vulnerabilities in applications and infrastructure.** (SHOULD; REVIEWED_DRAFT)
  Regularly scan for vulnerabilities in applications and infrastructure.
  Acceptance: Regularly scan for vulnerabilities in applications and infrastructure.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-083 r1 — Prioritize and remediate identified vulnerabilities based on risk.** (SHOULD; REVIEWED_DRAFT)
  Prioritize and remediate identified vulnerabilities based on risk.
  Acceptance: Prioritize and remediate identified vulnerabilities based on risk.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-084 r1 — Deploy continuous security monitoring tools to detect and respond to threats in ...** (SHOULD; REVIEWED_DRAFT)
  Deploy continuous security monitoring tools to detect and respond to threats in real-time.
  Acceptance: Deploy continuous security monitoring tools to detect and respond to threats in real-time.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-085 r1 — Set up alerts for suspicious activities.** (SHOULD; REVIEWED_DRAFT)
  Set up alerts for suspicious activities.
  Acceptance: Set up alerts for suspicious activities.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-086 r1 — Regularly review and update monitoring configurations.** (SHOULD; REVIEWED_DRAFT)
  Regularly review and update monitoring configurations.
  Acceptance: Regularly review and update monitoring configurations.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-087 r1 — Provide ongoing security training and awareness programs for all employees.** (SHOULD; REVIEWED_DRAFT)
  Provide ongoing security training and awareness programs for all employees.
  Acceptance: Provide ongoing security training and awareness programs for all employees.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-088 r1 — Include training on the latest security threats and best practices.** (SHOULD; REVIEWED_DRAFT)
  Include training on the latest security threats and best practices.
  Acceptance: Include training on the latest security threats and best practices.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-089 r1 — Track and document training completion.** (SHOULD; REVIEWED_DRAFT)
  Track and document training completion.
  Acceptance: Track and document training completion.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-090 r1 — Conduct regular phishing simulations to educate employees on recognizing phishin...** (SHOULD; REVIEWED_DRAFT)
  Conduct regular phishing simulations to educate employees on recognizing phishing attempts.
  Acceptance: Conduct regular phishing simulations to educate employees on recognizing phishing attempts.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-091 r1 — Analyze results and provide feedback to employees.** (SHOULD; REVIEWED_DRAFT)
  Analyze results and provide feedback to employees.
  Acceptance: Analyze results and provide feedback to employees.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-092 r1 — Adjust training based on simulation outcomes.** (SHOULD; REVIEWED_DRAFT)
  Adjust training based on simulation outcomes.
  Acceptance: Adjust training based on simulation outcomes.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-093 r1 — Establish a security champions program to promote security best practices within...** (SHOULD; REVIEWED_DRAFT)
  Establish a security champions program to promote security best practices within teams.
  Acceptance: Establish a security champions program to promote security best practices within teams.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-094 r1 — Provide additional training and resources to security champions.** (SHOULD; REVIEWED_DRAFT)
  Provide additional training and resources to security champions.
  Acceptance: Provide additional training and resources to security champions.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-095 r1 — Recognize and reward contributions from security champions.** (SHOULD; REVIEWED_DRAFT)
  Recognize and reward contributions from security champions.
  Acceptance: Recognize and reward contributions from security champions.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-096 r1 — Create clear communication channels for reporting security incidents and concern...** (SHOULD; REVIEWED_DRAFT)
  Create clear communication channels for reporting security incidents and concerns.
  Acceptance: Create clear communication channels for reporting security incidents and concerns.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-097 r1 — Ensure anonymity for those reporting security issues.** (SHOULD; REVIEWED_DRAFT)
  Ensure anonymity for those reporting security issues.
  Acceptance: Ensure anonymity for those reporting security issues.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-098 r1 — Regularly review and improve communication processes.** (SHOULD; REVIEWED_DRAFT)
  Regularly review and improve communication processes.
  Acceptance: Regularly review and improve communication processes.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-099 r1 — Foster a culture of security awareness and responsibility across the organizatio...** (SHOULD; REVIEWED_DRAFT)
  Foster a culture of security awareness and responsibility across the organization.
  Acceptance: Foster a culture of security awareness and responsibility across the organization.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-100 r1 — Encourage open discussions about security.** (SHOULD; REVIEWED_DRAFT)
  Encourage open discussions about security.
  Acceptance: Encourage open discussions about security.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-101 r1 — Integrate security into all aspects of the development lifecycle.** (SHOULD; REVIEWED_DRAFT)
  Integrate security into all aspects of the development lifecycle.
  Acceptance: Integrate security into all aspects of the development lifecycle.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-102 r1 — Ensure GitHub Enterprise is configured according to best practices for security ...** (SHOULD; REVIEWED_DRAFT)
  Ensure GitHub Enterprise is configured according to best practices for security and compliance.
  Acceptance: Ensure GitHub Enterprise is configured according to best practices for security and compliance.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{'enterprise_server': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-103 r1 — Name individuals responsible for GitHub Enterprise configuration and establish r...** (SHOULD; REVIEWED_DRAFT)
  Name individuals responsible for GitHub Enterprise configuration and establish regular communication with GitHub Support, Services, and Partners.
  Acceptance: Name individuals responsible for GitHub Enterprise configuration and establish regular communication with GitHub Support, Services, and Partners.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{'enterprise_server': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-104 r1 — Regularly review and update configuration settings as needed.** (SHOULD; REVIEWED_DRAFT)
  Regularly review and update configuration settings as needed.
  Acceptance: Regularly review and update configuration settings as needed.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-105 r1 — Document configuration changes and approvals.** (SHOULD; REVIEWED_DRAFT)
  Document configuration changes and approvals.
  Acceptance: Document configuration changes and approvals.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-106 r1 — Implement Single Sign-On (SSO) for GitHub Enterprise.** (SHOULD; REVIEWED_DRAFT)
  Implement Single Sign-On (SSO) for GitHub Enterprise.
  Acceptance: Implement Single Sign-On (SSO) for GitHub Enterprise.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{'enterprise_server': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-107 r1 — Ensure SSO configurations are secure and regularly reviewed.** (SHOULD; REVIEWED_DRAFT)
  Ensure SSO configurations are secure and regularly reviewed.
  Acceptance: Ensure SSO configurations are secure and regularly reviewed.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-108 r1 — Provide training on SSO usage and benefits.** (SHOULD; REVIEWED_DRAFT)
  Provide training on SSO usage and benefits.
  Acceptance: Provide training on SSO usage and benefits.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-109 r1 — Establish and regularly test backup and recovery procedures for GitHub Enterpris...** (SHOULD; REVIEWED_DRAFT)
  Establish and regularly test backup and recovery procedures for GitHub Enterprise data.
  Acceptance: Establish and regularly test backup and recovery procedures for GitHub Enterprise data.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{'enterprise_server': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-110 r1 — Ensure backups are stored securely.** (SHOULD; REVIEWED_DRAFT)
  Ensure backups are stored securely.
  Acceptance: Ensure backups are stored securely.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-111 r1 — Document backup and recovery processes.** (SHOULD; REVIEWED_DRAFT)
  Document backup and recovery processes.
  Acceptance: Document backup and recovery processes.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-112 r1 — Regularly test not only backups, but also restores into a staging environment.** (SHOULD; REVIEWED_DRAFT)
  Regularly test not only backups, but also restores into a staging environment.
  Acceptance: Regularly test not only backups, but also restores into a staging environment.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-113 r1 — Implement network security measures such as VPNs and firewalls to protect GitHub...** (SHOULD; REVIEWED_DRAFT)
  Implement network security measures such as VPNs and firewalls to protect GitHub Enterprise instances.
  Acceptance: Implement network security measures such as VPNs and firewalls to protect GitHub Enterprise instances.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{'enterprise_server': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-114 r1 — Regularly review and update network security configurations.** (SHOULD; REVIEWED_DRAFT)
  Regularly review and update network security configurations.
  Acceptance: Regularly review and update network security configurations.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-115 r1 — Monitor network traffic for suspicious activities.** (SHOULD; REVIEWED_DRAFT)
  Monitor network traffic for suspicious activities.
  Acceptance: Monitor network traffic for suspicious activities.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-116 r1 — Automate user provisioning and de-provisioning to ensure timely access managemen...** (SHOULD; REVIEWED_DRAFT)
  Automate user provisioning and de-provisioning to ensure timely access management, such as using SCIM.
  Acceptance: Automate user provisioning and de-provisioning to ensure timely access management, such as using SCIM.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-117 r1 — Regularly review user access and permissions.** (SHOULD; REVIEWED_DRAFT)
  Regularly review user access and permissions.
  Acceptance: Regularly review user access and permissions.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-118 r1 — Implement two-factor authentication (2FA) for all users.** (SHOULD; REVIEWED_DRAFT)
  Implement two-factor authentication (2FA) for all users.
  Acceptance: Implement two-factor authentication (2FA) for all users.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-119 r1 — Develop and enforce custom security policies specific to your GitHub Enterprise ...** (SHOULD; REVIEWED_DRAFT)
  Develop and enforce custom security policies specific to your GitHub Enterprise environment.
  Acceptance: Develop and enforce custom security policies specific to your GitHub Enterprise environment.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{'enterprise_server': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-120 r1 — Regularly review and update security policies.** (SHOULD; REVIEWED_DRAFT)
  Regularly review and update security policies.
  Acceptance: Regularly review and update security policies.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-121 r1 — Ensure policies are communicated to all relevant stakeholders.** (SHOULD; REVIEWED_DRAFT)
  Ensure policies are communicated to all relevant stakeholders.
  Acceptance: Ensure policies are communicated to all relevant stakeholders.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-122 r1 — Secure GitHub Enterprise APIs with appropriate authentication and authorization ...** (SHOULD; REVIEWED_DRAFT)
  Secure GitHub Enterprise APIs with appropriate authentication and authorization mechanisms.
  Acceptance: Secure GitHub Enterprise APIs with appropriate authentication and authorization mechanisms.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{'enterprise_server': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-123 r1 — Monitor API usage for anomalies.** (SHOULD; REVIEWED_DRAFT)
  Monitor API usage for anomalies.
  Acceptance: Monitor API usage for anomalies.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-124 r1 — Establish proper best practice guidelines for API usage, including token usage.** (SHOULD; REVIEWED_DRAFT)
  Establish proper best practice guidelines for API usage, including token usage.
  Acceptance: Establish proper best practice guidelines for API usage, including token usage.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-125 r1 — Set up monitoring and alerting for unusual activities within GitHub Enterprise.** (SHOULD; REVIEWED_DRAFT)
  Set up monitoring and alerting for unusual activities within GitHub Enterprise.
  Acceptance: Set up monitoring and alerting for unusual activities within GitHub Enterprise.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{'enterprise_server': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-126 r1 — Regularly review and update monitoring rules and audit logs.** (SHOULD; REVIEWED_DRAFT)
  Regularly review and update monitoring rules and audit logs.
  Acceptance: Regularly review and update monitoring rules and audit logs.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-127 r1 — Ensure alerts are actionable and promptly addressed.** (SHOULD; REVIEWED_DRAFT)
  Ensure alerts are actionable and promptly addressed.
  Acceptance: Ensure alerts are actionable and promptly addressed.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-128 r1 — Ensure compliance with any data residency requirements, especially when replicat...** (SHOULD; REVIEWED_DRAFT)
  Ensure compliance with any data residency requirements, especially when replicating with GitHub Enterprise Server.
  Acceptance: Ensure compliance with any data residency requirements, especially when replicating with GitHub Enterprise Server.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{'enterprise_server': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-129 r1 — Regularly review data residency configurations.** (SHOULD; REVIEWED_DRAFT)
  Regularly review data residency configurations.
  Acceptance: Regularly review data residency configurations.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-130 r1 — Document data residency policies and procedures.** (SHOULD; REVIEWED_DRAFT)
  Document data residency policies and procedures.
  Acceptance: Document data residency policies and procedures.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-131 r1 — Review and secure third-party integrations with GitHub Enterprise to prevent pot...** (SHOULD; REVIEWED_DRAFT)
  Review and secure third-party integrations with GitHub Enterprise to prevent potential security risks.
  Acceptance: Review and secure third-party integrations with GitHub Enterprise to prevent potential security risks.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{'enterprise_server': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-132 r1 — Regularly assess the security of third-party integrations.** (SHOULD; REVIEWED_DRAFT)
  Regularly assess the security of third-party integrations.
  Acceptance: Regularly assess the security of third-party integrations.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-133 r1 — Ensure third-party providers comply with your security standards.** (SHOULD; REVIEWED_DRAFT)
  Ensure third-party providers comply with your security standards.
  Acceptance: Ensure third-party providers comply with your security standards.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-134 r1 — Assess the organization and structure of repositories for clarity and scalabilit...** (SHOULD; REVIEWED_DRAFT)
  Assess the organization and structure of repositories for clarity and scalability.
  Acceptance: Assess the organization and structure of repositories for clarity and scalability.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-135 r1 — Determine whether repositories follow a naming convention, and ensure all reposi...** (SHOULD; REVIEWED_DRAFT)
  Determine whether repositories follow a naming convention, and ensure all repositories have a description.
  Acceptance: Determine whether repositories follow a naming convention, and ensure all repositories have a description.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-136 r1 — Check for the use of [custom properties](https://docs.github.com/enterprise-clou...** (SHOULD; REVIEWED_DRAFT)
  Check for the use of [custom properties](https://docs.github.com/enterprise-cloud@latest/organizations/managing-organization-settings/managing-custom-properties-for-repositories-in-your-organization) to organize repositories and target them with rulesets.
  Acceptance: Check for the use of [custom properties](https://docs.github.com/enterprise-cloud@latest/organizations/managing-organization-settings/managing-custom-properties-for-repositories-in-your-organization) to organize repositories and target them with rulesets.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-137 r1 — Verify that repositories are appropriately segmented as to avoid monolithic stru...** (SHOULD; REVIEWED_DRAFT)
  Verify that repositories are appropriately segmented as to avoid monolithic structures unnecessarily, or determine the necessity of such an architecture.
  Acceptance: Verify that repositories are appropriately segmented as to avoid monolithic structures unnecessarily, or determine the necessity of such an architecture.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-138 r1 — Check for the use of branch protection rules to maintain code quality.** (SHOULD; REVIEWED_DRAFT)
  Check for the use of branch protection rules to maintain code quality.
  Acceptance: Check for the use of branch protection rules to maintain code quality.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-139 r1 — Evaluate the modularity of the codebase for maintainability and scalability.** (SHOULD; REVIEWED_DRAFT)
  Evaluate the modularity of the codebase for maintainability and scalability.
  Acceptance: Evaluate the modularity of the codebase for maintainability and scalability.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-140 r1 — Ensure that code modules are reusable and loosely coupled.** (SHOULD; REVIEWED_DRAFT)
  Ensure that code modules are reusable and loosely coupled.
  Acceptance: Ensure that code modules are reusable and loosely coupled.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-141 r1 — Promote usage of design patterns that promote modularity.** (SHOULD; REVIEWED_DRAFT)
  Promote usage of design patterns that promote modularity.
  Acceptance: Promote usage of design patterns that promote modularity.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-142 r1 — Verify that dependencies between modules are well-documented.** (SHOULD; REVIEWED_DRAFT)
  Verify that dependencies between modules are well-documented.
  Acceptance: Verify that dependencies between modules are well-documented.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-143 r1 — Review the consistency of the technology stack across projects for efficiency an...** (SHOULD; REVIEWED_DRAFT)
  Review the consistency of the technology stack across projects for efficiency and interoperability.
  Acceptance: Review the consistency of the technology stack across projects for efficiency and interoperability.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-144 r1 — Ensure that the tech stack is standardized to reduce complexity.** (SHOULD; REVIEWED_DRAFT)
  Ensure that the tech stack is standardized to reduce complexity.
  Acceptance: Ensure that the tech stack is standardized to reduce complexity.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-145 r1 — Verify that the chosen technologies are well-supported and have a strong communi...** (SHOULD; REVIEWED_DRAFT)
  Verify that the chosen technologies are well-supported and have a strong community.
  Acceptance: Verify that the chosen technologies are well-supported and have a strong community.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-146 r1 — Check for the use of version control to manage tech stack dependencies.** (SHOULD; REVIEWED_DRAFT)
  Check for the use of version control to manage tech stack dependencies.
  Acceptance: Check for the use of version control to manage tech stack dependencies.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-147 r1 — Ensure ephemeral resources can be recreated on-demand.** (SHOULD; REVIEWED_DRAFT)
  Ensure ephemeral resources can be recreated on-demand.
  Acceptance: Ensure ephemeral resources can be recreated on-demand.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-148 r1 — Ensure non-ephemeral compute resources contains sufficient headroom from growth ...** (SHOULD; REVIEWED_DRAFT)
  Ensure non-ephemeral compute resources contains sufficient headroom from growth and scale.
  Acceptance: Ensure non-ephemeral compute resources contains sufficient headroom from growth and scale.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-149 r1 — Implement a load balancer to direct traffic to the appropriate resources.** (SHOULD; REVIEWED_DRAFT)
  Implement a load balancer to direct traffic to the appropriate resources.
  Acceptance: Implement a load balancer to direct traffic to the appropriate resources.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-150 r1 — Verify that the system can handle increased load without performance degradation...** (SHOULD; REVIEWED_DRAFT)
  Verify that the system can handle increased load without performance degradation.
  Acceptance: Verify that the system can handle increased load without performance degradation.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-151 r1 — Check for the use of scalable storage solutions.** (SHOULD; REVIEWED_DRAFT)
  Check for the use of scalable storage solutions.
  Acceptance: Check for the use of scalable storage solutions.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-152 r1 — Regularly test disaster recovery procedures to ensure they work as expected.** (SHOULD; REVIEWED_DRAFT)
  Regularly test disaster recovery procedures to ensure they work as expected.
  Acceptance: Regularly test disaster recovery procedures to ensure they work as expected.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-153 r1 — Verify that test results are documented and reviewed.** (SHOULD; REVIEWED_DRAFT)
  Verify that test results are documented and reviewed.
  Acceptance: Verify that test results are documented and reviewed.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-154 r1 — Ensure that any issues identified during testing are addressed.** (SHOULD; REVIEWED_DRAFT)
  Ensure that any issues identified during testing are addressed.
  Acceptance: Ensure that any issues identified during testing are addressed.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-155 r1 — Implement data replication strategies to ensure data is not lost in the event of...** (SHOULD; REVIEWED_DRAFT)
  Implement data replication strategies to ensure data is not lost in the event of a disaster.
  Acceptance: Implement data replication strategies to ensure data is not lost in the event of a disaster.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-156 r1 — Verify that replication processes are monitored.** (SHOULD; REVIEWED_DRAFT)
  Verify that replication processes are monitored.
  Acceptance: Verify that replication processes are monitored.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-157 r1 — Ensure that replicated data is consistent and up-to-date.** (SHOULD; REVIEWED_DRAFT)
  Ensure that replicated data is consistent and up-to-date.
  Acceptance: Ensure that replicated data is consistent and up-to-date.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-158 r1 — Ensure that application services are modular and can be developed, deployed, and...** (SHOULD; REVIEWED_DRAFT)
  Ensure that application services are modular and can be developed, deployed, and scaled independently.
  Acceptance: Ensure that application services are modular and can be developed, deployed, and scaled independently.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-159 r1 — Verify that modules have clear and well-defined interfaces.** (SHOULD; REVIEWED_DRAFT)
  Verify that modules have clear and well-defined interfaces.
  Acceptance: Verify that modules have clear and well-defined interfaces.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-160 r1 — Assess the modularity of codebases to facilitate easier updates and maintenance.** (SHOULD; REVIEWED_DRAFT)
  Assess the modularity of codebases to facilitate easier updates and maintenance.
  Acceptance: Assess the modularity of codebases to facilitate easier updates and maintenance.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-161 r1 — Ensure that code modules are reusable and loosely coupled.** (SHOULD; REVIEWED_DRAFT)
  Ensure that code modules are reusable and loosely coupled.
  Acceptance: Ensure that code modules are reusable and loosely coupled.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-162 r1 — Check for the use of design patterns that promote modularity.** (SHOULD; REVIEWED_DRAFT)
  Check for the use of design patterns that promote modularity.
  Acceptance: Check for the use of design patterns that promote modularity.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-163 r1 — Verify that dependencies between modules are well-documented.** (SHOULD; REVIEWED_DRAFT)
  Verify that dependencies between modules are well-documented.
  Acceptance: Verify that dependencies between modules are well-documented.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-164 r1 — Consider using a microservices architecture where appropriate.** (SHOULD; REVIEWED_DRAFT)
  Consider using a microservices architecture where appropriate.
  Acceptance: Consider using a microservices architecture where appropriate.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-165 r1 — Verify that microservices are independently deployable.** (SHOULD; REVIEWED_DRAFT)
  Verify that microservices are independently deployable.
  Acceptance: Verify that microservices are independently deployable.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-166 r1 — Ensure that microservices communicate effectively with each other.** (SHOULD; REVIEWED_DRAFT)
  Ensure that microservices communicate effectively with each other.
  Acceptance: Ensure that microservices communicate effectively with each other.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-167 r1 — Check for the use of service discovery mechanisms.** (SHOULD; REVIEWED_DRAFT)
  Check for the use of service discovery mechanisms.
  Acceptance: Check for the use of service discovery mechanisms.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-168 r1 — Assess the need for custom integrations and ensure they are implemented securely...** (SHOULD; REVIEWED_DRAFT)
  Assess the need for custom integrations and ensure they are implemented securely and efficiently.
  Acceptance: Assess the need for custom integrations and ensure they are implemented securely and efficiently.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-169 r1 — Verify that custom integrations are documented and maintained.** (SHOULD; REVIEWED_DRAFT)
  Verify that custom integrations are documented and maintained.
  Acceptance: Verify that custom integrations are documented and maintained.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-170 r1 — Ensure that custom integrations do not introduce security vulnerabilities.** (SHOULD; REVIEWED_DRAFT)
  Ensure that custom integrations do not introduce security vulnerabilities.
  Acceptance: Ensure that custom integrations do not introduce security vulnerabilities.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-171 r1 — Ensure that network configurations are optimized for performance and security.** (SHOULD; REVIEWED_DRAFT)
  Ensure that network configurations are optimized for performance and security.
  Acceptance: Ensure that network configurations are optimized for performance and security.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-172 r1 — Verify that firewalls and security groups are properly configured.** (SHOULD; REVIEWED_DRAFT)
  Verify that firewalls and security groups are properly configured.
  Acceptance: Verify that firewalls and security groups are properly configured.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-173 r1 — Ensure that network traffic is monitored and analyzed for potential threats.** (SHOULD; REVIEWED_DRAFT)
  Ensure that network traffic is monitored and analyzed for potential threats.
  Acceptance: Ensure that network traffic is monitored and analyzed for potential threats.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-174 r1 — Regularly apply updates and patches to maintain security and performance.** (SHOULD; REVIEWED_DRAFT)
  Regularly apply updates and patches to maintain security and performance.
  Acceptance: Regularly apply updates and patches to maintain security and performance.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-175 r1 — Ensure that maintenance windows are scheduled and communicated to stakeholders.** (SHOULD; REVIEWED_DRAFT)
  Ensure that maintenance windows are scheduled and communicated to stakeholders.
  Acceptance: Ensure that maintenance windows are scheduled and communicated to stakeholders.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-176 r1 — Verify that update procedures are documented and tested.** (SHOULD; REVIEWED_DRAFT)
  Verify that update procedures are documented and tested.
  Acceptance: Verify that update procedures are documented and tested.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-177 r1 — Plan for hardware scalability to accommodate future growth.** (SHOULD; REVIEWED_DRAFT)
  Plan for hardware scalability to accommodate future growth.
  Acceptance: Plan for hardware scalability to accommodate future growth.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-178 r1 — Ensure that capacity planning is regularly reviewed and updated.** (SHOULD; REVIEWED_DRAFT)
  Ensure that capacity planning is regularly reviewed and updated.
  Acceptance: Ensure that capacity planning is regularly reviewed and updated.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-179 r1 — Check for the use of scalable infrastructure components.** (SHOULD; REVIEWED_DRAFT)
  Check for the use of scalable infrastructure components.
  Acceptance: Check for the use of scalable infrastructure components.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-180 r1 — Implement robust backup solutions tailored to the on-premises nature.** (SHOULD; REVIEWED_DRAFT)
  Implement robust backup solutions tailored to the on-premises nature.
  Acceptance: Implement robust backup solutions tailored to the on-premises nature.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-181 r1 — Verify that backup procedures are documented and tested.** (SHOULD; REVIEWED_DRAFT)
  Verify that backup procedures are documented and tested.
  Acceptance: Verify that backup procedures are documented and tested.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-182 r1 — Ensure that backups are stored securely and can be restored quickly.** (SHOULD; REVIEWED_DRAFT)
  Ensure that backups are stored securely and can be restored quickly.
  Acceptance: Ensure that backups are stored securely and can be restored quickly.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-183 r1 — Ensure that codebases are simple and easy to understand.** (SHOULD; REVIEWED_DRAFT)
  Ensure that codebases are simple and easy to understand.
  Acceptance: Ensure that codebases are simple and easy to understand.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-184 r1 — Verify that code follows best practices and coding standards.** (SHOULD; REVIEWED_DRAFT)
  Verify that code follows best practices and coding standards.
  Acceptance: Verify that code follows best practices and coding standards.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-185 r1 — Check for the use of code reviews to maintain code quality.** (SHOULD; REVIEWED_DRAFT)
  Check for the use of code reviews to maintain code quality.
  Acceptance: Check for the use of code reviews to maintain code quality.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-186 r1 — Ensure that code is well-documented.** (SHOULD; REVIEWED_DRAFT)
  Ensure that code is well-documented.
  Acceptance: Ensure that code is well-documented.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-187 r1 — Design systems to be as simple as possible while meeting requirements.** (SHOULD; REVIEWED_DRAFT)
  Design systems to be as simple as possible while meeting requirements.
  Acceptance: Design systems to be as simple as possible while meeting requirements.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-188 r1 — Verify that system architectures are straightforward and easy to understand.** (SHOULD; REVIEWED_DRAFT)
  Verify that system architectures are straightforward and easy to understand.
  Acceptance: Verify that system architectures are straightforward and easy to understand.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-189 r1 — Ensure that system configurations are straightforward and easy to manage.** (SHOULD; REVIEWED_DRAFT)
  Ensure that system configurations are straightforward and easy to manage.
  Acceptance: Ensure that system configurations are straightforward and easy to manage.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-190 r1 — Check for the use of design patterns that promote simplicity.** (SHOULD; REVIEWED_DRAFT)
  Check for the use of design patterns that promote simplicity.
  Acceptance: Check for the use of design patterns that promote simplicity.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-191 r1 — Maintain clear and concise documentation for all systems and processes.** (SHOULD; REVIEWED_DRAFT)
  Maintain clear and concise documentation for all systems and processes.
  Acceptance: Maintain clear and concise documentation for all systems and processes.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-192 r1 — Verify that documentation is up-to-date and accessible.** (SHOULD; REVIEWED_DRAFT)
  Verify that documentation is up-to-date and accessible.
  Acceptance: Verify that documentation is up-to-date and accessible.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-193 r1 — Ensure that documentation includes examples and use cases.** (SHOULD; REVIEWED_DRAFT)
  Ensure that documentation includes examples and use cases.
  Acceptance: Ensure that documentation includes examples and use cases.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-194 r1 — Check for the use of documentation tools to manage and publish documentation.** (SHOULD; REVIEWED_DRAFT)
  Check for the use of documentation tools to manage and publish documentation.
  Acceptance: Check for the use of documentation tools to manage and publish documentation.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-195 r1 — Implement comprehensive logging to track system behavior and issues.** (SHOULD; REVIEWED_DRAFT)
  Implement comprehensive logging to track system behavior and issues.
  Acceptance: Implement comprehensive logging to track system behavior and issues.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-196 r1 — Verify that logs are stored securely and are accessible for analysis.** (SHOULD; REVIEWED_DRAFT)
  Verify that logs are stored securely and are accessible for analysis.
  Acceptance: Verify that logs are stored securely and are accessible for analysis.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-197 r1 — Ensure that log retention policies are in place.** (SHOULD; REVIEWED_DRAFT)
  Ensure that log retention policies are in place.
  Acceptance: Ensure that log retention policies are in place.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-198 r1 — Check for the use of log aggregation tools.** (SHOULD; REVIEWED_DRAFT)
  Check for the use of log aggregation tools.
  Acceptance: Check for the use of log aggregation tools.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-199 r1 — Assess the organization and structure of repositories for clarity and scalabilit...** (SHOULD; REVIEWED_DRAFT)
  Assess the organization and structure of repositories for clarity and scalability.
  Acceptance: Assess the organization and structure of repositories for clarity and scalability.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-200 r1 — Determine whether repositories follow a naming convention, and ensure all reposi...** (SHOULD; REVIEWED_DRAFT)
  Determine whether repositories follow a naming convention, and ensure all repositories have a description.
  Acceptance: Determine whether repositories follow a naming convention, and ensure all repositories have a description.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-201 r1 — Check for the use of [custom properties](https://docs.github.com/en/enterprise-c...** (SHOULD; REVIEWED_DRAFT)
  Check for the use of [custom properties](https://docs.github.com/en/enterprise-cloud@latest/organizations/managing-organization-settings/managing-custom-properties-for-repositories-in-your-organization) to dynamically manage and enforce.
  Acceptance: Check for the use of [custom properties](https://docs.github.com/en/enterprise-cloud@latest/organizations/managing-organization-settings/managing-custom-properties-for-repositories-in-your-organization) to dynamically manage and enforce.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-202 r1 — Verify that repositories are appropriately segmented as to avoid monolithic stru...** (SHOULD; REVIEWED_DRAFT)
  Verify that repositories are appropriately segmented as to avoid monolithic structures unnecessarily, or determine the necessity of such an architecture.
  Acceptance: Verify that repositories are appropriately segmented as to avoid monolithic structures unnecessarily, or determine the necessity of such an architecture.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-203 r1 — Check for the use of branch protection rules to maintain code quality.** (SHOULD; REVIEWED_DRAFT)
  Check for the use of branch protection rules to maintain code quality.
  Acceptance: Check for the use of branch protection rules to maintain code quality.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-204 r1 — Evaluate the modularity of the codebase for maintainability and scalability.** (SHOULD; REVIEWED_DRAFT)
  Evaluate the modularity of the codebase for maintainability and scalability.
  Acceptance: Evaluate the modularity of the codebase for maintainability and scalability.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-205 r1 — Ensure that code modules are reusable and loosely coupled.** (SHOULD; REVIEWED_DRAFT)
  Ensure that code modules are reusable and loosely coupled.
  Acceptance: Ensure that code modules are reusable and loosely coupled.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-206 r1 — Promote usage of design patterns that promote modularity.** (SHOULD; REVIEWED_DRAFT)
  Promote usage of design patterns that promote modularity.
  Acceptance: Promote usage of design patterns that promote modularity.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-207 r1 — Verify that dependencies between modules are well-documented.** (SHOULD; REVIEWED_DRAFT)
  Verify that dependencies between modules are well-documented.
  Acceptance: Verify that dependencies between modules are well-documented.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-208 r1 — Review the consistency of the technology stack across projects for efficiency an...** (SHOULD; REVIEWED_DRAFT)
  Review the consistency of the technology stack across projects for efficiency and interoperability.
  Acceptance: Review the consistency of the technology stack across projects for efficiency and interoperability.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-209 r1 — Ensure that the tech stack is standardized to reduce complexity.** (SHOULD; REVIEWED_DRAFT)
  Ensure that the tech stack is standardized to reduce complexity.
  Acceptance: Ensure that the tech stack is standardized to reduce complexity.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-210 r1 — Verify that the chosen technologies are well-supported and have a strong communi...** (SHOULD; REVIEWED_DRAFT)
  Verify that the chosen technologies are well-supported and have a strong community.
  Acceptance: Verify that the chosen technologies are well-supported and have a strong community.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-211 r1 — Check for the use of version control to manage tech stack dependencies.** (SHOULD; REVIEWED_DRAFT)
  Check for the use of version control to manage tech stack dependencies.
  Acceptance: Check for the use of version control to manage tech stack dependencies.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-212 r1 — Ensure ephemeral resources can be recreated on-demand.** (SHOULD; REVIEWED_DRAFT)
  Ensure ephemeral resources can be recreated on-demand.
  Acceptance: Ensure ephemeral resources can be recreated on-demand.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-213 r1 — Ensure non-ephemeral compute resources contains sufficient headroom from growth ...** (SHOULD; REVIEWED_DRAFT)
  Ensure non-ephemeral compute resources contains sufficient headroom from growth and scale.
  Acceptance: Ensure non-ephemeral compute resources contains sufficient headroom from growth and scale.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-214 r1 — Implement a load balancer to direct traffic to the appropriate resources.** (SHOULD; REVIEWED_DRAFT)
  Implement a load balancer to direct traffic to the appropriate resources.
  Acceptance: Implement a load balancer to direct traffic to the appropriate resources.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-215 r1 — Verify that the system can handle increased load without performance degradation...** (SHOULD; REVIEWED_DRAFT)
  Verify that the system can handle increased load without performance degradation.
  Acceptance: Verify that the system can handle increased load without performance degradation.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-216 r1 — Check for the use of scalable storage solutions.** (SHOULD; REVIEWED_DRAFT)
  Check for the use of scalable storage solutions.
  Acceptance: Check for the use of scalable storage solutions.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-217 r1 — Ensure systems can continue to operate in the event of a failure.** (SHOULD; REVIEWED_DRAFT)
  Ensure systems can continue to operate in the event of a failure.
  Acceptance: Ensure systems can continue to operate in the event of a failure.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-218 r1 — Verify that backup and restore procedures are in place and tested regularly.** (SHOULD; REVIEWED_DRAFT)
  Verify that backup and restore procedures are in place and tested regularly.
  Acceptance: Verify that backup and restore procedures are in place and tested regularly.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-219 r1 — Minimize/eliminate configuration drift between environments.** (SHOULD; REVIEWED_DRAFT)
  Minimize/eliminate configuration drift between environments.
  Acceptance: Minimize/eliminate configuration drift between environments.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-220 r1 — Ensure that backup and restore procedures are in place and tested regularly.** (SHOULD; REVIEWED_DRAFT)
  Ensure that backup and restore procedures are in place and tested regularly.
  Acceptance: Ensure that backup and restore procedures are in place and tested regularly.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-221 r1 — Verify that backups are stored securely and can be restored quickly.** (SHOULD; REVIEWED_DRAFT)
  Verify that backups are stored securely and can be restored quickly.
  Acceptance: Verify that backups are stored securely and can be restored quickly.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-222 r1 — Check for the use of automated backup solutions.** (SHOULD; REVIEWED_DRAFT)
  Check for the use of automated backup solutions.
  Acceptance: Check for the use of automated backup solutions.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-223 r1 — Regularly test restore procedures to staging environments to ensure they work as...** (SHOULD; REVIEWED_DRAFT)
  Regularly test restore procedures to staging environments to ensure they work as expected and to be able to test new product features.
  Acceptance: Regularly test restore procedures to staging environments to ensure they work as expected and to be able to test new product features.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-224 r1 — Implement high availability configurations to minimize downtime.** (SHOULD; REVIEWED_DRAFT)
  Implement high availability configurations to minimize downtime.
  Acceptance: Implement high availability configurations to minimize downtime.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-225 r1 — Verify that failover mechanisms are in place and tested.** (SHOULD; REVIEWED_DRAFT)
  Verify that failover mechanisms are in place and tested.
  Acceptance: Verify that failover mechanisms are in place and tested.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-226 r1 — Ensure that critical components have redundancy.** (SHOULD; REVIEWED_DRAFT)
  Ensure that critical components have redundancy.
  Acceptance: Ensure that critical components have redundancy.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-227 r1 — Continuously monitor system performance and optimize as needed.** (SHOULD; REVIEWED_DRAFT)
  Continuously monitor system performance and optimize as needed.
  Acceptance: Continuously monitor system performance and optimize as needed.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-228 r1 — Ensure efficient use of resources to avoid waste.** (SHOULD; REVIEWED_DRAFT)
  Ensure efficient use of resources to avoid waste.
  Acceptance: Ensure efficient use of resources to avoid waste.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-229 r1 — Automate repetitive tasks to improve efficiency and reduce human error.** (SHOULD; REVIEWED_DRAFT)
  Automate repetitive tasks to improve efficiency and reduce human error.
  Acceptance: Automate repetitive tasks to improve efficiency and reduce human error.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-230 r1 — Check for the use of performance profiling tools to identify bottlenecks.** (SHOULD; REVIEWED_DRAFT)
  Check for the use of performance profiling tools to identify bottlenecks.
  Acceptance: Check for the use of performance profiling tools to identify bottlenecks.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-231 r1 — Verify that resource allocation is optimized.** (SHOULD; REVIEWED_DRAFT)
  Verify that resource allocation is optimized.
  Acceptance: Verify that resource allocation is optimized.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-232 r1 — Check for the use of resource management tools.** (SHOULD; REVIEWED_DRAFT)
  Check for the use of resource management tools.
  Acceptance: Check for the use of resource management tools.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-233 r1 — Verify that automation scripts are well-documented.** (SHOULD; REVIEWED_DRAFT)
  Verify that automation scripts are well-documented.
  Acceptance: Verify that automation scripts are well-documented.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-234 r1 — Ensure that automation tools are regularly updated.** (SHOULD; REVIEWED_DRAFT)
  Ensure that automation tools are regularly updated.
  Acceptance: Ensure that automation tools are regularly updated.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-235 r1 — **Simplicity**** (SHOULD; REVIEWED_DRAFT)
  **Simplicity**
  Acceptance: **Simplicity**; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-236 r1 — Design systems to be as simple as possible while meeting requirements.** (SHOULD; REVIEWED_DRAFT)
  Design systems to be as simple as possible while meeting requirements.
  Acceptance: Design systems to be as simple as possible while meeting requirements.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-237 r1 — Verify that system architectures are straightforward and easy to understand.** (SHOULD; REVIEWED_DRAFT)
  Verify that system architectures are straightforward and easy to understand.
  Acceptance: Verify that system architectures are straightforward and easy to understand.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-238 r1 — Ensure that system configurations are straightforward and easy to manage.** (SHOULD; REVIEWED_DRAFT)
  Ensure that system configurations are straightforward and easy to manage.
  Acceptance: Ensure that system configurations are straightforward and easy to manage.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-239 r1 — Check for the use of design patterns that promote simplicity.** (SHOULD; REVIEWED_DRAFT)
  Check for the use of design patterns that promote simplicity.
  Acceptance: Check for the use of design patterns that promote simplicity.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-240 r1 — **Documentation**** (SHOULD; REVIEWED_DRAFT)
  **Documentation**
  Acceptance: **Documentation**; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-241 r1 — Maintain clear and concise documentation for all systems and processes.** (SHOULD; REVIEWED_DRAFT)
  Maintain clear and concise documentation for all systems and processes.
  Acceptance: Maintain clear and concise documentation for all systems and processes.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-242 r1 — Verify that documentation is up-to-date and accessible.** (SHOULD; REVIEWED_DRAFT)
  Verify that documentation is up-to-date and accessible.
  Acceptance: Verify that documentation is up-to-date and accessible.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-243 r1 — Ensure that documentation includes examples and use cases.** (SHOULD; REVIEWED_DRAFT)
  Ensure that documentation includes examples and use cases.
  Acceptance: Ensure that documentation includes examples and use cases.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-244 r1 — Check for the use of documentation tools to manage and publish documentation.** (SHOULD; REVIEWED_DRAFT)
  Check for the use of documentation tools to manage and publish documentation.
  Acceptance: Check for the use of documentation tools to manage and publish documentation.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-245 r1 — Develop and maintain a disaster recovery plan.** (SHOULD; REVIEWED_DRAFT)
  Develop and maintain a disaster recovery plan.
  Acceptance: Develop and maintain a disaster recovery plan.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-246 r1 — Regularly test disaster recovery procedures to ensure they work as expected.** (SHOULD; REVIEWED_DRAFT)
  Regularly test disaster recovery procedures to ensure they work as expected.
  Acceptance: Regularly test disaster recovery procedures to ensure they work as expected.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-247 r1 — Implement data replication strategies to ensure data is not lost in the event of...** (SHOULD; REVIEWED_DRAFT)
  Implement data replication strategies to ensure data is not lost in the event of a disaster.
  Acceptance: Implement data replication strategies to ensure data is not lost in the event of a disaster.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-248 r1 — Verify that disaster recovery plans include clear roles and responsibilities.** (SHOULD; REVIEWED_DRAFT)
  Verify that disaster recovery plans include clear roles and responsibilities.
  Acceptance: Verify that disaster recovery plans include clear roles and responsibilities.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-249 r1 — Be able to recover git repositories in the event users erroneously force push.** (SHOULD; REVIEWED_DRAFT)
  Be able to recover git repositories in the event users erroneously force push.
  Acceptance: Be able to recover git repositories in the event users erroneously force push.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-250 r1 — Verify that test results are documented and reviewed.** (SHOULD; REVIEWED_DRAFT)
  Verify that test results are documented and reviewed.
  Acceptance: Verify that test results are documented and reviewed.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-251 r1 — Ensure that any issues identified during testing are addressed.** (SHOULD; REVIEWED_DRAFT)
  Ensure that any issues identified during testing are addressed.
  Acceptance: Ensure that any issues identified during testing are addressed.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-252 r1 — Verify that replication processes are monitored.** (SHOULD; REVIEWED_DRAFT)
  Verify that replication processes are monitored.
  Acceptance: Verify that replication processes are monitored.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-253 r1 — Ensure that replicated data is consistent and up-to-date.** (SHOULD; REVIEWED_DRAFT)
  Ensure that replicated data is consistent and up-to-date.
  Acceptance: Ensure that replicated data is consistent and up-to-date.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-254 r1 — Ensure that application services are modular and can be developed, deployed, and...** (SHOULD; REVIEWED_DRAFT)
  Ensure that application services are modular and can be developed, deployed, and scaled independently.
  Acceptance: Ensure that application services are modular and can be developed, deployed, and scaled independently.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-255 r1 — Verify that modules have clear and well-defined interfaces.** (SHOULD; REVIEWED_DRAFT)
  Verify that modules have clear and well-defined interfaces.
  Acceptance: Verify that modules have clear and well-defined interfaces.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-256 r1 — Assess the modularity of codebases to facilitate easier updates and maintenance.** (SHOULD; REVIEWED_DRAFT)
  Assess the modularity of codebases to facilitate easier updates and maintenance.
  Acceptance: Assess the modularity of codebases to facilitate easier updates and maintenance.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-257 r1 — Ensure that code modules are reusable and loosely coupled.** (SHOULD; REVIEWED_DRAFT)
  Ensure that code modules are reusable and loosely coupled.
  Acceptance: Ensure that code modules are reusable and loosely coupled.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-258 r1 — Check for the use of design patterns that promote modularity.** (SHOULD; REVIEWED_DRAFT)
  Check for the use of design patterns that promote modularity.
  Acceptance: Check for the use of design patterns that promote modularity.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-259 r1 — Verify that dependencies between modules are well-documented.** (SHOULD; REVIEWED_DRAFT)
  Verify that dependencies between modules are well-documented.
  Acceptance: Verify that dependencies between modules are well-documented.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-260 r1 — Consider using a microservices architecture where appropriate.** (SHOULD; REVIEWED_DRAFT)
  Consider using a microservices architecture where appropriate.
  Acceptance: Consider using a microservices architecture where appropriate.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-261 r1 — Verify that microservices are independently deployable.** (SHOULD; REVIEWED_DRAFT)
  Verify that microservices are independently deployable.
  Acceptance: Verify that microservices are independently deployable.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-262 r1 — Ensure that microservices communicate effectively with each other.** (SHOULD; REVIEWED_DRAFT)
  Ensure that microservices communicate effectively with each other.
  Acceptance: Ensure that microservices communicate effectively with each other.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-263 r1 — Check for the use of service discovery mechanisms.** (SHOULD; REVIEWED_DRAFT)
  Check for the use of service discovery mechanisms.
  Acceptance: Check for the use of service discovery mechanisms.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-264 r1 — Ensure that APIs are well-documented and can be easily integrated with other sys...** (SHOULD; REVIEWED_DRAFT)
  Ensure that APIs are well-documented and can be easily integrated with other systems.
  Acceptance: Ensure that APIs are well-documented and can be easily integrated with other systems.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-265 r1 — Verify that APIs follow industry standards.** (SHOULD; REVIEWED_DRAFT)
  Verify that APIs follow industry standards.
  Acceptance: Verify that APIs follow industry standards.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-266 r1 — Ensure that APIs are versioned and backward compatible.** (SHOULD; REVIEWED_DRAFT)
  Ensure that APIs are versioned and backward compatible.
  Acceptance: Ensure that APIs are versioned and backward compatible.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-267 r1 — Check for the use of API gateways to manage and secure APIs.** (SHOULD; REVIEWED_DRAFT)
  Check for the use of API gateways to manage and secure APIs.
  Acceptance: Check for the use of API gateways to manage and secure APIs.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-268 r1 — Ensure compliance with industry standards to facilitate interoperability.** (SHOULD; REVIEWED_DRAFT)
  Ensure compliance with industry standards to facilitate interoperability.
  Acceptance: Ensure compliance with industry standards to facilitate interoperability.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-269 r1 — Ensure compliance with license obligations for open sourced and vendor-managed s...** (SHOULD; REVIEWED_DRAFT)
  Ensure compliance with license obligations for open sourced and vendor-managed software packages.
  Acceptance: Ensure compliance with license obligations for open sourced and vendor-managed software packages.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-270 r1 — Verify that systems are compatible across different platforms and environments.** (SHOULD; REVIEWED_DRAFT)
  Verify that systems are compatible across different platforms and environments.
  Acceptance: Verify that systems are compatible across different platforms and environments.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-271 r1 — Check for the use of middleware to facilitate communication between different sy...** (SHOULD; REVIEWED_DRAFT)
  Check for the use of middleware to facilitate communication between different systems.
  Acceptance: Check for the use of middleware to facilitate communication between different systems.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-272 r1 — Ensure that data formats are standardized.** (SHOULD; REVIEWED_DRAFT)
  Ensure that data formats are standardized.
  Acceptance: Ensure that data formats are standardized.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-273 r1 — Ensure that cross-platform testing is performed regularly.** (SHOULD; REVIEWED_DRAFT)
  Ensure that cross-platform testing is performed regularly.
  Acceptance: Ensure that cross-platform testing is performed regularly.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-274 r1 — Check for the use of platform-agnostic technologies.** (SHOULD; REVIEWED_DRAFT)
  Check for the use of platform-agnostic technologies.
  Acceptance: Check for the use of platform-agnostic technologies.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-275 r1 — Verify that system dependencies are well-documented.** (SHOULD; REVIEWED_DRAFT)
  Verify that system dependencies are well-documented.
  Acceptance: Verify that system dependencies are well-documented.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-276 r1 — Implement comprehensive logging to track system behavior and issues.** (SHOULD; REVIEWED_DRAFT)
  Implement comprehensive logging to track system behavior and issues.
  Acceptance: Implement comprehensive logging to track system behavior and issues.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-277 r1 — Verify that logs are stored securely and are accessible for analysis.** (SHOULD; REVIEWED_DRAFT)
  Verify that logs are stored securely and are accessible for analysis.
  Acceptance: Verify that logs are stored securely and are accessible for analysis.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-278 r1 — Ensure that log retention policies are in place.** (SHOULD; REVIEWED_DRAFT)
  Ensure that log retention policies are in place.
  Acceptance: Ensure that log retention policies are in place.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-279 r1 — Check for the use of log aggregation tools.** (SHOULD; REVIEWED_DRAFT)
  Check for the use of log aggregation tools.
  Acceptance: Check for the use of log aggregation tools.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-280 r1 — Use monitoring tools to gain insights into system performance and health.** (SHOULD; REVIEWED_DRAFT)
  Use monitoring tools to gain insights into system performance and health.
  Acceptance: Use monitoring tools to gain insights into system performance and health.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-281 r1 — Verify that monitoring dashboards are set up and regularly reviewed.** (SHOULD; REVIEWED_DRAFT)
  Verify that monitoring dashboards are set up and regularly reviewed.
  Acceptance: Verify that monitoring dashboards are set up and regularly reviewed.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-282 r1 — Ensure that monitoring alerts are configured and actionable.** (SHOULD; REVIEWED_DRAFT)
  Ensure that monitoring alerts are configured and actionable.
  Acceptance: Ensure that monitoring alerts are configured and actionable.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-283 r1 — Check for the use of monitoring tools that support anomaly detection.** (SHOULD; REVIEWED_DRAFT)
  Check for the use of monitoring tools that support anomaly detection.
  Acceptance: Check for the use of monitoring tools that support anomaly detection.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-284 r1 — Set up alerting mechanisms to notify relevant teams of issues in real-time.** (SHOULD; REVIEWED_DRAFT)
  Set up alerting mechanisms to notify relevant teams of issues in real-time.
  Acceptance: Set up alerting mechanisms to notify relevant teams of issues in real-time.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-285 r1 — Verify that alert thresholds are appropriately configured.** (SHOULD; REVIEWED_DRAFT)
  Verify that alert thresholds are appropriately configured.
  Acceptance: Verify that alert thresholds are appropriately configured.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-286 r1 — Ensure that alerts are actionable and include relevant context.** (SHOULD; REVIEWED_DRAFT)
  Ensure that alerts are actionable and include relevant context.
  Acceptance: Ensure that alerts are actionable and include relevant context.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-287 r1 — Check for the use of alert management tools to handle alert fatigue.** (SHOULD; REVIEWED_DRAFT)
  Check for the use of alert management tools to handle alert fatigue.
  Acceptance: Check for the use of alert management tools to handle alert fatigue.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-288 r1 — Ensure that user management practices are in place, including role-based access ...** (SHOULD; REVIEWED_DRAFT)
  Ensure that user management practices are in place, including role-based access control and regular audits.
  Acceptance: Ensure that user management practices are in place, including role-based access control and regular audits.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-289 r1 — Verify that user permissions are regularly reviewed and updated.** (SHOULD; REVIEWED_DRAFT)
  Verify that user permissions are regularly reviewed and updated.
  Acceptance: Verify that user permissions are regularly reviewed and updated.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-290 r1 — Check for the use of single sign-on (SSO) for user authentication.** (SHOULD; REVIEWED_DRAFT)
  Check for the use of single sign-on (SSO) for user authentication.
  Acceptance: Check for the use of single sign-on (SSO) for user authentication.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-291 r1 — Verify that security measures comply with organizational and regulatory requirem...** (SHOULD; REVIEWED_DRAFT)
  Verify that security measures comply with organizational and regulatory requirements.
  Acceptance: Verify that security measures comply with organizational and regulatory requirements.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-292 r1 — Ensure that security policies are documented and enforced.** (SHOULD; REVIEWED_DRAFT)
  Ensure that security policies are documented and enforced.
  Acceptance: Ensure that security policies are documented and enforced.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-293 r1 — Assess the need for custom integrations and ensure they are implemented securely...** (SHOULD; REVIEWED_DRAFT)
  Assess the need for custom integrations and ensure they are implemented securely and efficiently.
  Acceptance: Assess the need for custom integrations and ensure they are implemented securely and efficiently.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-294 r1 — Verify that custom integrations are documented and maintained.** (SHOULD; REVIEWED_DRAFT)
  Verify that custom integrations are documented and maintained.
  Acceptance: Verify that custom integrations are documented and maintained.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-295 r1 — Ensure that custom integrations do not introduce security vulnerabilities.** (SHOULD; REVIEWED_DRAFT)
  Ensure that custom integrations do not introduce security vulnerabilities.
  Acceptance: Ensure that custom integrations do not introduce security vulnerabilities.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-296 r1 — Ensure that data residency requirements are met.** (SHOULD; REVIEWED_DRAFT)
  Ensure that data residency requirements are met.
  Acceptance: Ensure that data residency requirements are met.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-297 r1 — Verify that data storage locations comply with regional regulations.** (SHOULD; REVIEWED_DRAFT)
  Verify that data storage locations comply with regional regulations.
  Acceptance: Verify that data storage locations comply with regional regulations.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-298 r1 — Check for the use of data localization strategies where necessary.** (SHOULD; REVIEWED_DRAFT)
  Check for the use of data localization strategies where necessary.
  Acceptance: Check for the use of data localization strategies where necessary.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-299 r1 — Ensure that user management practices are in place, including role-based access ...** (SHOULD; REVIEWED_DRAFT)
  Ensure that user management practices are in place, including role-based access control and regular audits.
  Acceptance: Ensure that user management practices are in place, including role-based access control and regular audits.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-300 r1 — Verify that user permissions are regularly reviewed and updated.** (SHOULD; REVIEWED_DRAFT)
  Verify that user permissions are regularly reviewed and updated.
  Acceptance: Verify that user permissions are regularly reviewed and updated.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-301 r1 — Check for the use of single sign-on (SSO) for user authentication.** (SHOULD; REVIEWED_DRAFT)
  Check for the use of single sign-on (SSO) for user authentication.
  Acceptance: Check for the use of single sign-on (SSO) for user authentication.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-302 r1 — Verify that security measures comply with organizational and regulatory requirem...** (SHOULD; REVIEWED_DRAFT)
  Verify that security measures comply with organizational and regulatory requirements.
  Acceptance: Verify that security measures comply with organizational and regulatory requirements.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-303 r1 — Ensure that security policies are documented and enforced.** (SHOULD; REVIEWED_DRAFT)
  Ensure that security policies are documented and enforced.
  Acceptance: Ensure that security policies are documented and enforced.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-304 r1 — Assess the need for custom integrations and ensure they are implemented securely...** (SHOULD; REVIEWED_DRAFT)
  Assess the need for custom integrations and ensure they are implemented securely and efficiently.
  Acceptance: Assess the need for custom integrations and ensure they are implemented securely and efficiently.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-305 r1 — Verify that custom integrations are documented and maintained.** (SHOULD; REVIEWED_DRAFT)
  Verify that custom integrations are documented and maintained.
  Acceptance: Verify that custom integrations are documented and maintained.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-306 r1 — Ensure that custom integrations do not introduce security vulnerabilities.** (SHOULD; REVIEWED_DRAFT)
  Ensure that custom integrations do not introduce security vulnerabilities.
  Acceptance: Ensure that custom integrations do not introduce security vulnerabilities.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-307 r1 — Ensure that network configurations are optimized for performance and security.** (SHOULD; REVIEWED_DRAFT)
  Ensure that network configurations are optimized for performance and security.
  Acceptance: Ensure that network configurations are optimized for performance and security.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-308 r1 — Verify that firewalls and security groups are properly configured.** (SHOULD; REVIEWED_DRAFT)
  Verify that firewalls and security groups are properly configured.
  Acceptance: Verify that firewalls and security groups are properly configured.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-309 r1 — Ensure that network traffic is monitored and analyzed for potential threats.** (SHOULD; REVIEWED_DRAFT)
  Ensure that network traffic is monitored and analyzed for potential threats.
  Acceptance: Ensure that network traffic is monitored and analyzed for potential threats.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-310 r1 — Regularly apply updates and patches to maintain security and performance.** (SHOULD; REVIEWED_DRAFT)
  Regularly apply updates and patches to maintain security and performance.
  Acceptance: Regularly apply updates and patches to maintain security and performance.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-311 r1 — Ensure that maintenance windows are scheduled and communicated to stakeholders.** (SHOULD; REVIEWED_DRAFT)
  Ensure that maintenance windows are scheduled and communicated to stakeholders.
  Acceptance: Ensure that maintenance windows are scheduled and communicated to stakeholders.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-312 r1 — Verify that update procedures are documented and tested.** (SHOULD; REVIEWED_DRAFT)
  Verify that update procedures are documented and tested.
  Acceptance: Verify that update procedures are documented and tested.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-313 r1 — Plan for hardware scalability to accommodate future growth.** (SHOULD; REVIEWED_DRAFT)
  Plan for hardware scalability to accommodate future growth.
  Acceptance: Plan for hardware scalability to accommodate future growth.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-314 r1 — Ensure that capacity planning is regularly reviewed and updated.** (SHOULD; REVIEWED_DRAFT)
  Ensure that capacity planning is regularly reviewed and updated.
  Acceptance: Ensure that capacity planning is regularly reviewed and updated.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-315 r1 — Check for the use of scalable infrastructure components.** (SHOULD; REVIEWED_DRAFT)
  Check for the use of scalable infrastructure components.
  Acceptance: Check for the use of scalable infrastructure components.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-316 r1 — Implement robust backup solutions tailored to the on-premises nature.** (SHOULD; REVIEWED_DRAFT)
  Implement robust backup solutions tailored to the on-premises nature.
  Acceptance: Implement robust backup solutions tailored to the on-premises nature.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-317 r1 — Verify that backup procedures are documented and tested.** (SHOULD; REVIEWED_DRAFT)
  Verify that backup procedures are documented and tested.
  Acceptance: Verify that backup procedures are documented and tested.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-318 r1 — Ensure that backups are stored securely and can be restored quickly.** (SHOULD; REVIEWED_DRAFT)
  Ensure that backups are stored securely and can be restored quickly.
  Acceptance: Ensure that backups are stored securely and can be restored quickly.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-319 r1 — Does the team encourage open communication and early-stage collaboration?** (SHOULD; REVIEWED_DRAFT)
  Does the team encourage open communication and early-stage collaboration?
  Acceptance: Does the team encourage open communication and early-stage collaboration?; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-320 r1 — Are there established channels for proactive engagement and feedback?** (SHOULD; REVIEWED_DRAFT)
  Are there established channels for proactive engagement and feedback?
  Acceptance: Are there established channels for proactive engagement and feedback?; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-321 r1 — Ensure pull requests are used effectively for code collaboration and review.** (SHOULD; REVIEWED_DRAFT)
  Ensure pull requests are used effectively for code collaboration and review.
  Acceptance: Ensure pull requests are used effectively for code collaboration and review.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-322 r1 — Is there a formalized code review process in place?** (SHOULD; REVIEWED_DRAFT)
  Is there a formalized code review process in place?
  Acceptance: Is there a formalized code review process in place?; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-323 r1 — Are conversation tools integrated seamlessly with the development workflow?** (SHOULD; REVIEWED_DRAFT)
  Are conversation tools integrated seamlessly with the development workflow?
  Acceptance: Are conversation tools integrated seamlessly with the development workflow?; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-324 r1 — Are discussions linked directly to the codebase to reduce context-switching?** (SHOULD; REVIEWED_DRAFT)
  Are discussions linked directly to the codebase to reduce context-switching?
  Acceptance: Are discussions linked directly to the codebase to reduce context-switching?; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-325 r1 — Check for integrations with external communication tools like Slack or Microsoft...** (SHOULD; REVIEWED_DRAFT)
  Check for integrations with external communication tools like Slack or Microsoft Teams.
  Acceptance: Check for integrations with external communication tools like Slack or Microsoft Teams.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-326 r1 — Are GitHub Enterprise-specific communication tools and features being utilized e...** (SHOULD; REVIEWED_DRAFT)
  Are GitHub Enterprise-specific communication tools and features being utilized effectively?
  Acceptance: Are GitHub Enterprise-specific communication tools and features being utilized effectively?; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{'enterprise_server': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-327 r1 — Verify that code follows best practices and coding standards.** (SHOULD; REVIEWED_DRAFT)
  Verify that code follows best practices and coding standards.
  Acceptance: Verify that code follows best practices and coding standards.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-328 r1 — Ensure that code is well-documented.** (SHOULD; REVIEWED_DRAFT)
  Ensure that code is well-documented.
  Acceptance: Ensure that code is well-documented.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-329 r1 — Is there an onboarding process that incorporates key tooling concepts for new te...** (SHOULD; REVIEWED_DRAFT)
  Is there an onboarding process that incorporates key tooling concepts for new team members?
  Acceptance: Is there an onboarding process that incorporates key tooling concepts for new team members?; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-330 r1 — Are new team members trained to understand existing processes, workflows, and pr...** (SHOULD; REVIEWED_DRAFT)
  Are new team members trained to understand existing processes, workflows, and practices?
  Acceptance: Are new team members trained to understand existing processes, workflows, and practices?; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-331 r1 — Does the team foster a culture of learning and mentoring?** (SHOULD; REVIEWED_DRAFT)
  Does the team foster a culture of learning and mentoring?
  Acceptance: Does the team foster a culture of learning and mentoring?; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-332 r1 — Are there initiatives to ensure that diverse perspectives are included in decisi...** (SHOULD; REVIEWED_DRAFT)
  Are there initiatives to ensure that diverse perspectives are included in decision-making?
  Acceptance: Are there initiatives to ensure that diverse perspectives are included in decision-making?; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-333 r1 — Are GitHub Enterprise-specific onboarding and training materials provided to new...** (SHOULD; REVIEWED_DRAFT)
  Are GitHub Enterprise-specific onboarding and training materials provided to new team members?
  Acceptance: Are GitHub Enterprise-specific onboarding and training materials provided to new team members?; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{'enterprise_server': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-334 r1 — Are there virtual spaces for exchanging ideas, posing questions, and deliberatin...** (SHOULD; REVIEWED_DRAFT)
  Are there virtual spaces for exchanging ideas, posing questions, and deliberating issues?
  Acceptance: Are there virtual spaces for exchanging ideas, posing questions, and deliberating issues?; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-335 r1 — Are there processes for communicating security findings throughout the project l...** (SHOULD; REVIEWED_DRAFT)
  Are there processes for communicating security findings throughout the project lifecycle?
  Acceptance: Are there processes for communicating security findings throughout the project lifecycle?; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-336 r1 — Is there a comprehensive knowledge repository for documentation and guidelines?** (SHOULD; REVIEWED_DRAFT)
  Is there a comprehensive knowledge repository for documentation and guidelines?
  Acceptance: Is there a comprehensive knowledge repository for documentation and guidelines?; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-337 r1 — Evaluate the use of GitHub Discussions or other tools for team communication.** (SHOULD; REVIEWED_DRAFT)
  Evaluate the use of GitHub Discussions or other tools for team communication.
  Acceptance: Evaluate the use of GitHub Discussions or other tools for team communication.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-338 r1 — Review access controls to ensure appropriate permissions for collaborators.** (SHOULD; REVIEWED_DRAFT)
  Review access controls to ensure appropriate permissions for collaborators.
  Acceptance: Review access controls to ensure appropriate permissions for collaborators.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-339 r1 — Are GitHub Enterprise-specific features like internal repositories and wikis bei...** (SHOULD; REVIEWED_DRAFT)
  Are GitHub Enterprise-specific features like internal repositories and wikis being used to promote openness?
  Acceptance: Are GitHub Enterprise-specific features like internal repositories and wikis being used to promote openness?; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{'enterprise_server': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-340 r1 — Are there standardized processes for communicating security findings?** (SHOULD; REVIEWED_DRAFT)
  Are there standardized processes for communicating security findings?
  Acceptance: Are there standardized processes for communicating security findings?; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-341 r1 — Are all team members informed about the project’s progress in real-time?** (SHOULD; REVIEWED_DRAFT)
  Are all team members informed about the project’s progress in real-time?
  Acceptance: Are all team members informed about the project’s progress in real-time?; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-342 r1 — Are there automated workflows that trigger notifications and updates across diff...** (SHOULD; REVIEWED_DRAFT)
  Are there automated workflows that trigger notifications and updates across different teams?
  Acceptance: Are there automated workflows that trigger notifications and updates across different teams?; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-343 r1 — Are GitHub Projects or other project management tools used to provide visibility...** (SHOULD; REVIEWED_DRAFT)
  Are GitHub Projects or other project management tools used to provide visibility into project status?
  Acceptance: Are GitHub Projects or other project management tools used to provide visibility into project status?; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-344 r1 — Are GitHub Enterprise-specific audit logs and monitoring tools used to ensure tr...** (SHOULD; REVIEWED_DRAFT)
  Are GitHub Enterprise-specific audit logs and monitoring tools used to ensure transparency?
  Acceptance: Are GitHub Enterprise-specific audit logs and monitoring tools used to ensure transparency?; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{'enterprise_server': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-345 r1 — Does the team model facilitate a culture of open dialogue and collective ownersh...** (SHOULD; REVIEWED_DRAFT)
  Does the team model facilitate a culture of open dialogue and collective ownership?
  Acceptance: Does the team model facilitate a culture of open dialogue and collective ownership?; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-346 r1 — Are there automated workflows to boost productivity and maintain high-quality st...** (SHOULD; REVIEWED_DRAFT)
  Are there automated workflows to boost productivity and maintain high-quality standards?
  Acceptance: Are there automated workflows to boost productivity and maintain high-quality standards?; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-347 r1 — Are standard project management methodologies adopted to streamline the code del...** (SHOULD; REVIEWED_DRAFT)
  Are standard project management methodologies adopted to streamline the code delivery process?
  Acceptance: Are standard project management methodologies adopted to streamline the code delivery process?; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-348 r1 — Is there integration with third-party tools to enhance functionality and product...** (SHOULD; REVIEWED_DRAFT)
  Is there integration with third-party tools to enhance functionality and productivity?
  Acceptance: Is there integration with third-party tools to enhance functionality and productivity?; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-349 r1 — Are GitHub Enterprise-specific customization options and integrations being leve...** (SHOULD; REVIEWED_DRAFT)
  Are GitHub Enterprise-specific customization options and integrations being leveraged to enhance flexibility to various team needs?
  Acceptance: Are GitHub Enterprise-specific customization options and integrations being leveraged to enhance flexibility to various team needs?; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{'enterprise_server': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-350 r1 — Ensure teams are well-versed in the intent of branch rules and verify rules are ...** (SHOULD; REVIEWED_DRAFT)
  Ensure teams are well-versed in the intent of branch rules and verify rules are in place.
  Acceptance: Ensure teams are well-versed in the intent of branch rules and verify rules are in place.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-351 r1 — Leverage pull requests and enforce branch rules to maintain code quality.** (SHOULD; REVIEWED_DRAFT)
  Leverage pull requests and enforce branch rules to maintain code quality.
  Acceptance: Leverage pull requests and enforce branch rules to maintain code quality.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-352 r1 — Verify that required status checks are enabled.** (SHOULD; REVIEWED_DRAFT)
  Verify that required status checks are enabled.
  Acceptance: Verify that required status checks are enabled.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-353 r1 — Ensure code review requirements are set.** (SHOULD; REVIEWED_DRAFT)
  Ensure code review requirements are set.
  Acceptance: Ensure code review requirements are set.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-354 r1 — Review compliance checks for code and dependencies.** (SHOULD; REVIEWED_DRAFT)
  Review compliance checks for code and dependencies.
  Acceptance: Review compliance checks for code and dependencies.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-355 r1 — Ensure automated tools are integrated for continuous compliance.** (SHOULD; REVIEWED_DRAFT)
  Ensure automated tools are integrated for continuous compliance.
  Acceptance: Ensure automated tools are integrated for continuous compliance.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-356 r1 — Check the usage and monitoring of GitHub audit logs for governance.** (SHOULD; REVIEWED_DRAFT)
  Check the usage and monitoring of GitHub audit logs for governance.
  Acceptance: Check the usage and monitoring of GitHub audit logs for governance.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-357 r1 — Ensure audit logs are retained for an appropriate period, depending on usage of ...** (SHOULD; REVIEWED_DRAFT)
  Ensure audit logs are retained for an appropriate period, depending on usage of GitHub Enterprise Cloud/Server or another business application.
  Acceptance: Ensure audit logs are retained for an appropriate period, depending on usage of GitHub Enterprise Cloud/Server or another business application.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{'enterprise_server': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-358 r1 — Regularly review audit logs for unusual activities.** (SHOULD; REVIEWED_DRAFT)
  Regularly review audit logs for unusual activities.
  Acceptance: Regularly review audit logs for unusual activities.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-359 r1 — Ensure all modifications to documents and code are tracked using version control...** (SHOULD; REVIEWED_DRAFT)
  Ensure all modifications to documents and code are tracked using version control.
  Acceptance: Ensure all modifications to documents and code are tracked using version control.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-360 r1 — Verify that version control policies are enforced.** (SHOULD; REVIEWED_DRAFT)
  Verify that version control policies are enforced.
  Acceptance: Verify that version control policies are enforced.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-361 r1 — Implement continuous logging for all critical resources within the environment.** (SHOULD; REVIEWED_DRAFT)
  Implement continuous logging for all critical resources within the environment.
  Acceptance: Implement continuous logging for all critical resources within the environment.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-362 r1 — Ensure logs are securely stored and accessible for audits.** (SHOULD; REVIEWED_DRAFT)
  Ensure logs are securely stored and accessible for audits.
  Acceptance: Ensure logs are securely stored and accessible for audits.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-363 r1 — Utilize [custom properties](https://docs.github.com/en/enterprise-cloud@latest/o...** (SHOULD; REVIEWED_DRAFT)
  Utilize [custom properties](https://docs.github.com/en/enterprise-cloud@latest/organizations/managing-organization-settings/managing-custom-properties-for-repositories-in-your-organization) to manage and categorize repositories.
  Acceptance: Utilize [custom properties](https://docs.github.com/en/enterprise-cloud@latest/organizations/managing-organization-settings/managing-custom-properties-for-repositories-in-your-organization) to manage and categorize repositories.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-364 r1 — Ensure custom properties are consistently applied across repositories.** (SHOULD; REVIEWED_DRAFT)
  Ensure custom properties are consistently applied across repositories.
  Acceptance: Ensure custom properties are consistently applied across repositories.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-365 r1 — Regularly review and update custom properties to reflect organizational needs.** (SHOULD; REVIEWED_DRAFT)
  Regularly review and update custom properties to reflect organizational needs.
  Acceptance: Regularly review and update custom properties to reflect organizational needs.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-366 r1 — Assess the implementation of role-based access control for repository and organi...** (SHOULD; REVIEWED_DRAFT)
  Assess the implementation of role-based access control for repository and organization access.
  Acceptance: Assess the implementation of role-based access control for repository and organization access.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-367 r1 — Ensure roles are clearly defined and documented.** (SHOULD; REVIEWED_DRAFT)
  Ensure roles are clearly defined and documented.
  Acceptance: Ensure roles are clearly defined and documented.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-368 r1 — Create a process for requesting and granting access, and have the timestamps of ...** (SHOULD; REVIEWED_DRAFT)
  Create a process for requesting and granting access, and have the timestamps of access requests available.
  Acceptance: Create a process for requesting and granting access, and have the timestamps of access requests available.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-369 r1 — Clearly define and document each role's access rights and responsibilities.** (SHOULD; REVIEWED_DRAFT)
  Clearly define and document each role's access rights and responsibilities.
  Acceptance: Clearly define and document each role's access rights and responsibilities.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-370 r1 — Regularly review and update access rights documentation.** (SHOULD; REVIEWED_DRAFT)
  Regularly review and update access rights documentation.
  Acceptance: Regularly review and update access rights documentation.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-371 r1 — Regularly monitor user activities to ensure compliance with access policies.** (SHOULD; REVIEWED_DRAFT)
  Regularly monitor user activities to ensure compliance with access policies.
  Acceptance: Regularly monitor user activities to ensure compliance with access policies.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-372 r1 — Implement alerts for suspicious activities at both the administrative and reposi...** (SHOULD; REVIEWED_DRAFT)
  Implement alerts for suspicious activities at both the administrative and repository level.
  Acceptance: Implement alerts for suspicious activities at both the administrative and repository level.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-373 r1 — Establish and test incident response procedures for unauthorized access or polic...** (SHOULD; REVIEWED_DRAFT)
  Establish and test incident response procedures for unauthorized access or policy violations.
  Acceptance: Establish and test incident response procedures for unauthorized access or policy violations.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-374 r1 — Ensure incident response plans are documented and accessible.** (SHOULD; REVIEWED_DRAFT)
  Ensure incident response plans are documented and accessible.
  Acceptance: Ensure incident response plans are documented and accessible.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-375 r1 — Ensure governance policies are regularly reviewed and updated to adapt to new re...** (SHOULD; REVIEWED_DRAFT)
  Ensure governance policies are regularly reviewed and updated to adapt to new requirements.
  Acceptance: Ensure governance policies are regularly reviewed and updated to adapt to new requirements.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-376 r1 — Involve stakeholders in the policy update process, such as application owners an...** (SHOULD; REVIEWED_DRAFT)
  Involve stakeholders in the policy update process, such as application owners and change managers.
  Acceptance: Involve stakeholders in the policy update process, such as application owners and change managers.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-377 r1 — Implement training programs to keep team members updated on governance policies ...** (SHOULD; REVIEWED_DRAFT)
  Implement training programs to keep team members updated on governance policies and best practices.
  Acceptance: Implement training programs to keep team members updated on governance policies and best practices.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-378 r1 — Ensure training materials are accessible and up-to-date.** (SHOULD; REVIEWED_DRAFT)
  Ensure training materials are accessible and up-to-date.
  Acceptance: Ensure training materials are accessible and up-to-date.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-379 r1 — Ensure governance processes can scale with the growth of the organization and it...** (SHOULD; REVIEWED_DRAFT)
  Ensure governance processes can scale with the growth of the organization and its projects.
  Acceptance: Ensure governance processes can scale with the growth of the organization and its projects.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-380 r1 — Regularly assess and adjust processes to accommodate scaling needs.** (SHOULD; REVIEWED_DRAFT)
  Regularly assess and adjust processes to accommodate scaling needs.
  Acceptance: Regularly assess and adjust processes to accommodate scaling needs.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-381 r1 — Establish a feedback mechanism to continuously improve governance practices base...** (SHOULD; REVIEWED_DRAFT)
  Establish a feedback mechanism to continuously improve governance practices based on user input.
  Acceptance: Establish a feedback mechanism to continuously improve governance practices based on user input.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-382 r1 — Regularly review and act on feedback received.** (SHOULD; REVIEWED_DRAFT)
  Regularly review and act on feedback received.
  Acceptance: Regularly review and act on feedback received.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-383 r1 — Conduct periodic access reviews to ensure only authorized individuals have acces...** (SHOULD; REVIEWED_DRAFT)
  Conduct periodic access reviews to ensure only authorized individuals have access to critical resources.
  Acceptance: Conduct periodic access reviews to ensure only authorized individuals have access to critical resources.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-384 r1 — Document and address any discrepancies found during reviews.** (SHOULD; REVIEWED_DRAFT)
  Document and address any discrepancies found during reviews.
  Acceptance: Document and address any discrepancies found during reviews.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-385 r1 — Implement configuration management practices to maintain consistency and control...** (SHOULD; REVIEWED_DRAFT)
  Implement configuration management practices to maintain consistency and control over the environment.
  Acceptance: Implement configuration management practices to maintain consistency and control over the environment.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-386 r1 — Regularly review and update configuration management policies.** (SHOULD; REVIEWED_DRAFT)
  Regularly review and update configuration management policies.
  Acceptance: Regularly review and update configuration management policies.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-387 r1 — Ensure robust backup and recovery processes are in place for critical data and c...** (SHOULD; REVIEWED_DRAFT)
  Ensure robust backup and recovery processes are in place for critical data and configurations.
  Acceptance: Ensure robust backup and recovery processes are in place for critical data and configurations.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-388 r1 — Regularly test backup and recovery procedures.** (SHOULD; REVIEWED_DRAFT)
  Regularly test backup and recovery procedures.
  Acceptance: Regularly test backup and recovery procedures.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-389 r1 — Regularly perform compliance audits to ensure adherence to governance policies a...** (SHOULD; REVIEWED_DRAFT)
  Regularly perform compliance audits to ensure adherence to governance policies and regulatory requirements.
  Acceptance: Regularly perform compliance audits to ensure adherence to governance policies and regulatory requirements.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-390 r1 — Document and address any findings from compliance audits.** (SHOULD; REVIEWED_DRAFT)
  Document and address any findings from compliance audits.
  Acceptance: Document and address any findings from compliance audits.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-391 r1 — Review and configure GitHub Enterprise settings to align with organizational gov...** (SHOULD; REVIEWED_DRAFT)
  Review and configure GitHub Enterprise settings to align with organizational governance policies.
  Acceptance: Review and configure GitHub Enterprise settings to align with organizational governance policies.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{'enterprise_server': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-392 r1 — Ensure settings are documented and regularly reviewed.** (SHOULD; REVIEWED_DRAFT)
  Ensure settings are documented and regularly reviewed.
  Acceptance: Ensure settings are documented and regularly reviewed.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-393 r1 — Ensure high availability and disaster recovery plans are in place for GitHub Ent...** (SHOULD; REVIEWED_DRAFT)
  Ensure high availability and disaster recovery plans are in place for GitHub Enterprise Server.
  Acceptance: Ensure high availability and disaster recovery plans are in place for GitHub Enterprise Server.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{'enterprise_server': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-394 r1 — Regularly test high availability and disaster recovery plans.** (SHOULD; REVIEWED_DRAFT)
  Regularly test high availability and disaster recovery plans.
  Acceptance: Regularly test high availability and disaster recovery plans.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-395 r1 — Integrate GitHub Enterprise with existing security tools and frameworks (e.g., S...** (SHOULD; REVIEWED_DRAFT)
  Integrate GitHub Enterprise with existing security tools and frameworks (e.g., SSO, SCIM).
  Acceptance: Integrate GitHub Enterprise with existing security tools and frameworks (e.g., SSO, SCIM).; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{'enterprise_server': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-396 r1 — Regularly review and update security integrations.** (SHOULD; REVIEWED_DRAFT)
  Regularly review and update security integrations.
  Acceptance: Regularly review and update security integrations.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-397 r1 — Implement performance monitoring to ensure the GitHub Enterprise environment is ...** (SHOULD; REVIEWED_DRAFT)
  Implement performance monitoring to ensure the GitHub Enterprise environment is running efficiently.
  Acceptance: Implement performance monitoring to ensure the GitHub Enterprise environment is running efficiently.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{'enterprise_server': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-398 r1 — Regularly review performance metrics and address any issues.** (SHOULD; REVIEWED_DRAFT)
  Regularly review performance metrics and address any issues.
  Acceptance: Regularly review performance metrics and address any issues.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-399 r1 — Ensure data residency requirements are met for GitHub Enterprise deployments.** (SHOULD; REVIEWED_DRAFT)
  Ensure data residency requirements are met for GitHub Enterprise deployments.
  Acceptance: Ensure data residency requirements are met for GitHub Enterprise deployments.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{'enterprise_server': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-400 r1 — Document and regularly review data residency policies.** (SHOULD; REVIEWED_DRAFT)
  Document and regularly review data residency policies.
  Acceptance: Document and regularly review data residency policies.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-401 r1 — Develop and enforce custom policies specific to the organization's use of GitHub...** (SHOULD; REVIEWED_DRAFT)
  Develop and enforce custom policies specific to the organization's use of GitHub Enterprise.
  Acceptance: Develop and enforce custom policies specific to the organization's use of GitHub Enterprise.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{'enterprise_server': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-402 r1 — Regularly review and update custom policies.** (SHOULD; REVIEWED_DRAFT)
  Regularly review and update custom policies.
  Acceptance: Regularly review and update custom policies.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-403 r1 — Automate user provisioning and de-provisioning to maintain control over access.** (SHOULD; REVIEWED_DRAFT)
  Automate user provisioning and de-provisioning to maintain control over access.
  Acceptance: Automate user provisioning and de-provisioning to maintain control over access.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-404 r1 — Regularly review and update user provisioning processes.** (SHOULD; REVIEWED_DRAFT)
  Regularly review and update user provisioning processes.
  Acceptance: Regularly review and update user provisioning processes.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-405 r1 — Establish a support and maintenance plan for GitHub Enterprise, including regula...** (SHOULD; REVIEWED_DRAFT)
  Establish a support and maintenance plan for GitHub Enterprise, including regular updates and patches for Server, or communication of features for both Cloud and Server.
  Acceptance: Establish a support and maintenance plan for GitHub Enterprise, including regular updates and patches for Server, or communication of features for both Cloud and Server.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{'enterprise_server': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-406 r1 — Ensure support and maintenance plans are documented and accessible.** (SHOULD; REVIEWED_DRAFT)
  Ensure support and maintenance plans are documented and accessible.
  Acceptance: Ensure support and maintenance plans are documented and accessible.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-407 r1 — **Identify Manual Processes**** (SHOULD; REVIEWED_DRAFT)
  **Identify Manual Processes**
  Acceptance: **Identify Manual Processes**; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-408 r1 — Document all current manual processes.** (SHOULD; REVIEWED_DRAFT)
  Document all current manual processes.
  Acceptance: Document all current manual processes.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-409 r1 — Identify repetitive, time-consuming, and error-prone tasks.** (SHOULD; REVIEWED_DRAFT)
  Identify repetitive, time-consuming, and error-prone tasks.
  Acceptance: Identify repetitive, time-consuming, and error-prone tasks.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-410 r1 — Involve key stakeholders to gain insights and perspectives on the needs of the o...** (SHOULD; REVIEWED_DRAFT)
  Involve key stakeholders to gain insights and perspectives on the needs of the organization and any frictions to resolve.
  Acceptance: Involve key stakeholders to gain insights and perspectives on the needs of the organization and any frictions to resolve.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-411 r1 — **Evaluate Automation Potential**** (SHOULD; REVIEWED_DRAFT)
  **Evaluate Automation Potential**
  Acceptance: **Evaluate Automation Potential**; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-412 r1 — Assess the scalability and future growth potential of automation solutions.** (SHOULD; REVIEWED_DRAFT)
  Assess the scalability and future growth potential of automation solutions.
  Acceptance: Assess the scalability and future growth potential of automation solutions.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-413 r1 — Prioritize processes based on pain points and inefficiencies.** (SHOULD; REVIEWED_DRAFT)
  Prioritize processes based on pain points and inefficiencies.
  Acceptance: Prioritize processes based on pain points and inefficiencies.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-414 r1 — **Implement Automation Solutions**** (SHOULD; REVIEWED_DRAFT)
  **Implement Automation Solutions**
  Acceptance: **Implement Automation Solutions**; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-415 r1 — Foster a culture of automation within the organization.** (SHOULD; REVIEWED_DRAFT)
  Foster a culture of automation within the organization.
  Acceptance: Foster a culture of automation within the organization.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-416 r1 — Incorporate automation concepts into documentation and processes.** (SHOULD; REVIEWED_DRAFT)
  Incorporate automation concepts into documentation and processes.
  Acceptance: Incorporate automation concepts into documentation and processes.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-417 r1 — Automate repetitive tasks and integrate CI/CD pipelines.** (SHOULD; REVIEWED_DRAFT)
  Automate repetitive tasks and integrate CI/CD pipelines.
  Acceptance: Automate repetitive tasks and integrate CI/CD pipelines.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-418 r1 — Implement GitHub Actions using GitHub-hosted runners for CI/CD.** (SHOULD; REVIEWED_DRAFT)
  Implement GitHub Actions using GitHub-hosted runners for CI/CD.
  Acceptance: Implement GitHub Actions using GitHub-hosted runners for CI/CD.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-419 r1 — **Enhance Automation Capabilities**** (SHOULD; REVIEWED_DRAFT)
  **Enhance Automation Capabilities**
  Acceptance: **Enhance Automation Capabilities**; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-420 r1 — Provide learning sessions on automated workflows and security features.** (SHOULD; REVIEWED_DRAFT)
  Provide learning sessions on automated workflows and security features.
  Acceptance: Provide learning sessions on automated workflows and security features.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-421 r1 — Evaluate the benefits of automation against cost and maintenance.** (SHOULD; REVIEWED_DRAFT)
  Evaluate the benefits of automation against cost and maintenance.
  Acceptance: Evaluate the benefits of automation against cost and maintenance.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-422 r1 — Establish a strategy for platform automation adoption.** (SHOULD; REVIEWED_DRAFT)
  Establish a strategy for platform automation adoption.
  Acceptance: Establish a strategy for platform automation adoption.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-423 r1 — Leverage GitHub Enterprise features like Actions, Packages, Code Scanning, Secre...** (SHOULD; REVIEWED_DRAFT)
  Leverage GitHub Enterprise features like Actions, Packages, Code Scanning, Secret Scanning, and Dependabot.
  Acceptance: Leverage GitHub Enterprise features like Actions, Packages, Code Scanning, Secret Scanning, and Dependabot.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{'enterprise_server': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-424 r1 — **Optimize and Refine Automation**** (SHOULD; REVIEWED_DRAFT)
  **Optimize and Refine Automation**
  Acceptance: **Optimize and Refine Automation**; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-425 r1 — Develop automated workflows for notifications and updates.** (SHOULD; REVIEWED_DRAFT)
  Develop automated workflows for notifications and updates.
  Acceptance: Develop automated workflows for notifications and updates.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-426 r1 — Establish and enforce code implementation and deployment standards.** (SHOULD; REVIEWED_DRAFT)
  Establish and enforce code implementation and deployment standards.
  Acceptance: Establish and enforce code implementation and deployment standards.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-427 r1 — Continuously monitor and optimize automated workflows.** (SHOULD; REVIEWED_DRAFT)
  Continuously monitor and optimize automated workflows.
  Acceptance: Continuously monitor and optimize automated workflows.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-428 r1 — Regularly review and optimize GitHub Enterprise automation configurations.** (SHOULD; REVIEWED_DRAFT)
  Regularly review and optimize GitHub Enterprise automation configurations.
  Acceptance: Regularly review and optimize GitHub Enterprise automation configurations.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{'enterprise_server': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-429 r1 — **Establish Integration Standards**** (SHOULD; REVIEWED_DRAFT)
  **Establish Integration Standards**
  Acceptance: **Establish Integration Standards**; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-430 r1 — Define clear standards and guidelines for platform integration.** (SHOULD; REVIEWED_DRAFT)
  Define clear standards and guidelines for platform integration.
  Acceptance: Define clear standards and guidelines for platform integration.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-431 r1 — Ensure compatibility and scalability across different systems.** (SHOULD; REVIEWED_DRAFT)
  Ensure compatibility and scalability across different systems.
  Acceptance: Ensure compatibility and scalability across different systems.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-432 r1 — **Govern Integration Efforts**** (SHOULD; REVIEWED_DRAFT)
  **Govern Integration Efforts**
  Acceptance: **Govern Integration Efforts**; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-433 r1 — Identify individuals or teams responsible for driving integration.** (SHOULD; REVIEWED_DRAFT)
  Identify individuals or teams responsible for driving integration.
  Acceptance: Identify individuals or teams responsible for driving integration.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-434 r1 — Develop and enforce consistent policies, standards, and best practices.** (SHOULD; REVIEWED_DRAFT)
  Develop and enforce consistent policies, standards, and best practices.
  Acceptance: Develop and enforce consistent policies, standards, and best practices.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-435 r1 — **Document Integration Processes**** (SHOULD; REVIEWED_DRAFT)
  **Document Integration Processes**
  Acceptance: **Document Integration Processes**; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-436 r1 — Create comprehensive integration process documentation for developers.** (SHOULD; REVIEWED_DRAFT)
  Create comprehensive integration process documentation for developers.
  Acceptance: Create comprehensive integration process documentation for developers.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-437 r1 — Ensure consistency and standardization in integration practices.** (SHOULD; REVIEWED_DRAFT)
  Ensure consistency and standardization in integration practices.
  Acceptance: Ensure consistency and standardization in integration practices.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-438 r1 — **Implement Key Integrations**** (SHOULD; REVIEWED_DRAFT)
  **Implement Key Integrations**
  Acceptance: **Implement Key Integrations**; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-439 r1 — Identify key integration points and evaluate potential solutions.** (SHOULD; REVIEWED_DRAFT)
  Identify key integration points and evaluate potential solutions.
  Acceptance: Identify key integration points and evaluate potential solutions.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-440 r1 — Prioritize integrations based on organizational needs and goals.** (SHOULD; REVIEWED_DRAFT)
  Prioritize integrations based on organizational needs and goals.
  Acceptance: Prioritize integrations based on organizational needs and goals.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-441 r1 — Integrate GitHub Enterprise with other enterprise systems, or look to migrate to...** (SHOULD; REVIEWED_DRAFT)
  Integrate GitHub Enterprise with other enterprise systems, or look to migrate to GitHub where possible.
  Acceptance: Integrate GitHub Enterprise with other enterprise systems, or look to migrate to GitHub where possible.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{'enterprise_server': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-442 r1 — **Enhance and Monitor Integrations**** (SHOULD; REVIEWED_DRAFT)
  **Enhance and Monitor Integrations**
  Acceptance: **Enhance and Monitor Integrations**; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-443 r1 — Implement advanced monitoring and management tools for integrated systems.** (SHOULD; REVIEWED_DRAFT)
  Implement advanced monitoring and management tools for integrated systems.
  Acceptance: Implement advanced monitoring and management tools for integrated systems.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-444 r1 — Continuously evaluate and refine integration processes.** (SHOULD; REVIEWED_DRAFT)
  Continuously evaluate and refine integration processes.
  Acceptance: Continuously evaluate and refine integration processes.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-445 r1 — Use GitHub Enterprise APIs and webhooks for custom integrations.** (SHOULD; REVIEWED_DRAFT)
  Use GitHub Enterprise APIs and webhooks for custom integrations.
  Acceptance: Use GitHub Enterprise APIs and webhooks for custom integrations.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{'enterprise_server': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-446 r1 — **Foster a Learning Culture**** (SHOULD; REVIEWED_DRAFT)
  **Foster a Learning Culture**
  Acceptance: **Foster a Learning Culture**; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-447 r1 — Promote a culture of continuous improvement and learning.** (SHOULD; REVIEWED_DRAFT)
  Promote a culture of continuous improvement and learning.
  Acceptance: Promote a culture of continuous improvement and learning.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-448 r1 — Encourage employees to take ownership of their process skills.** (SHOULD; REVIEWED_DRAFT)
  Encourage employees to take ownership of their process skills.
  Acceptance: Encourage employees to take ownership of their process skills.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-449 r1 — **Provide Learning Opportunities**** (SHOULD; REVIEWED_DRAFT)
  **Provide Learning Opportunities**
  Acceptance: **Provide Learning Opportunities**; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-450 r1 — Offer training sessions on new tools, technologies, and best practices.** (SHOULD; REVIEWED_DRAFT)
  Offer training sessions on new tools, technologies, and best practices.
  Acceptance: Offer training sessions on new tools, technologies, and best practices.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-451 r1 — Facilitate knowledge sharing and collaboration across teams.** (SHOULD; REVIEWED_DRAFT)
  Facilitate knowledge sharing and collaboration across teams.
  Acceptance: Facilitate knowledge sharing and collaboration across teams.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-452 r1 — Provide administrative and user training on GitHub Enterprise features and best ...** (SHOULD; REVIEWED_DRAFT)
  Provide administrative and user training on GitHub Enterprise features and best practices.
  Acceptance: Provide administrative and user training on GitHub Enterprise features and best practices.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{'enterprise_server': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-453 r1 — **Leverage Feedback for Improvement**** (SHOULD; REVIEWED_DRAFT)
  **Leverage Feedback for Improvement**
  Acceptance: **Leverage Feedback for Improvement**; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-454 r1 — Gather user feedback on automated and integrated processes.** (SHOULD; REVIEWED_DRAFT)
  Gather user feedback on automated and integrated processes.
  Acceptance: Gather user feedback on automated and integrated processes.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-455 r1 — Use feedback to identify areas for enhancement and optimization.** (SHOULD; REVIEWED_DRAFT)
  Use feedback to identify areas for enhancement and optimization.
  Acceptance: Use feedback to identify areas for enhancement and optimization.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-456 r1 — Collect feedback on GitHub Enterprise usage and performance.** (SHOULD; REVIEWED_DRAFT)
  Collect feedback on GitHub Enterprise usage and performance.
  Acceptance: Collect feedback on GitHub Enterprise usage and performance.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{'enterprise_server': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-457 r1 — **Adapt and Evolve**** (SHOULD; REVIEWED_DRAFT)
  **Adapt and Evolve**
  Acceptance: **Adapt and Evolve**; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-458 r1 — Continuously update process documentation and tooling.** (SHOULD; REVIEWED_DRAFT)
  Continuously update process documentation and tooling.
  Acceptance: Continuously update process documentation and tooling.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-459 r1 — Stay informed about emerging technologies and integration platforms.** (SHOULD; REVIEWED_DRAFT)
  Stay informed about emerging technologies and integration platforms.
  Acceptance: Stay informed about emerging technologies and integration platforms.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-460 r1 — Regularly review and update GitHub Enterprise configurations and policies.** (SHOULD; REVIEWED_DRAFT)
  Regularly review and update GitHub Enterprise configurations and policies.
  Acceptance: Regularly review and update GitHub Enterprise configurations and policies.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{'enterprise_server': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-461 r1 — **Measure and Reflect**** (SHOULD; REVIEWED_DRAFT)
  **Measure and Reflect**
  Acceptance: **Measure and Reflect**; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-462 r1 — Monitor performance metrics of automated and integrated systems.** (SHOULD; REVIEWED_DRAFT)
  Monitor performance metrics of automated and integrated systems.
  Acceptance: Monitor performance metrics of automated and integrated systems.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-463 r1 — Reflect on successes and areas for improvement to drive future initiatives.** (SHOULD; REVIEWED_DRAFT)
  Reflect on successes and areas for improvement to drive future initiatives.
  Acceptance: Reflect on successes and areas for improvement to drive future initiatives.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-464 r1 — Track and analyze GitHub Enterprise usage metrics and user satisfaction.** (SHOULD; REVIEWED_DRAFT)
  Track and analyze GitHub Enterprise usage metrics and user satisfaction.
  Acceptance: Track and analyze GitHub Enterprise usage metrics and user satisfaction.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{'enterprise_server': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-465 r1 — **Identify Feedback Channels**** (SHOULD; REVIEWED_DRAFT)
  **Identify Feedback Channels**
  Acceptance: **Identify Feedback Channels**; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-466 r1 — Determine the various channels through which feedback can be collected (e.g., su...** (SHOULD; REVIEWED_DRAFT)
  Determine the various channels through which feedback can be collected (e.g., surveys, user interviews, feedback forms).
  Acceptance: Determine the various channels through which feedback can be collected (e.g., surveys, user interviews, feedback forms).; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-467 r1 — Ensure feedback channels are accessible and user-friendly.** (SHOULD; REVIEWED_DRAFT)
  Ensure feedback channels are accessible and user-friendly.
  Acceptance: Ensure feedback channels are accessible and user-friendly.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-468 r1 — Set up dedicated feedback channels for GitHub Enterprise users to both gather fe...** (SHOULD; REVIEWED_DRAFT)
  Set up dedicated feedback channels for GitHub Enterprise users to both gather feedback for administrators as well as to discuss GitHub with others in a community-style forum.
  Acceptance: Set up dedicated feedback channels for GitHub Enterprise users to both gather feedback for administrators as well as to discuss GitHub with others in a community-style forum.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{'enterprise_server': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-469 r1 — **Establish Clear Objectives**** (SHOULD; REVIEWED_DRAFT)
  **Establish Clear Objectives**
  Acceptance: **Establish Clear Objectives**; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-470 r1 — Define the goals and objectives for collecting feedback (e.g., improving user ex...** (SHOULD; REVIEWED_DRAFT)
  Define the goals and objectives for collecting feedback (e.g., improving user experience, identifying bugs).
  Acceptance: Define the goals and objectives for collecting feedback (e.g., improving user experience, identifying bugs).; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-471 r1 — Align feedback objectives with organizational goals.** (SHOULD; REVIEWED_DRAFT)
  Align feedback objectives with organizational goals.
  Acceptance: Align feedback objectives with organizational goals.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-472 r1 — Focus on specific objectives related to GitHub Enterprise deployment and usage.** (SHOULD; REVIEWED_DRAFT)
  Focus on specific objectives related to GitHub Enterprise deployment and usage.
  Acceptance: Focus on specific objectives related to GitHub Enterprise deployment and usage.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{'enterprise_server': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-473 r1 — **Analyze Feedback Data**** (SHOULD; REVIEWED_DRAFT)
  **Analyze Feedback Data**
  Acceptance: **Analyze Feedback Data**; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-474 r1 — Regularly analyze feedback data to identify trends, common issues, and areas for...** (SHOULD; REVIEWED_DRAFT)
  Regularly analyze feedback data to identify trends, common issues, and areas for improvement.
  Acceptance: Regularly analyze feedback data to identify trends, common issues, and areas for improvement.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-475 r1 — Use both qualitative and quantitative methods to gain comprehensive insights.** (SHOULD; REVIEWED_DRAFT)
  Use both qualitative and quantitative methods to gain comprehensive insights.
  Acceptance: Use both qualitative and quantitative methods to gain comprehensive insights.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-476 r1 — Pay special attention to feedback related to GitHub Enterprise performance and f...** (SHOULD; REVIEWED_DRAFT)
  Pay special attention to feedback related to GitHub Enterprise performance and features.
  Acceptance: Pay special attention to feedback related to GitHub Enterprise performance and features.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{'enterprise_server': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-477 r1 — **Close the Feedback Loop**** (SHOULD; REVIEWED_DRAFT)
  **Close the Feedback Loop**
  Acceptance: **Close the Feedback Loop**; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-478 r1 — Ensure that feedback is acknowledged, addressed, and communicated back to the st...** (SHOULD; REVIEWED_DRAFT)
  Ensure that feedback is acknowledged, addressed, and communicated back to the stakeholders who provided it.
  Acceptance: Ensure that feedback is acknowledged, addressed, and communicated back to the stakeholders who provided it.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-479 r1 — Provide updates on actions taken based on feedback.** (SHOULD; REVIEWED_DRAFT)
  Provide updates on actions taken based on feedback.
  Acceptance: Provide updates on actions taken based on feedback.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-480 r1 — Communicate specific changes and improvements made to GitHub Enterprise based on...** (SHOULD; REVIEWED_DRAFT)
  Communicate specific changes and improvements made to GitHub Enterprise based on user feedback.
  Acceptance: Communicate specific changes and improvements made to GitHub Enterprise based on user feedback.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{'enterprise_server': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-481 r1 — **Integrate Feedback into Development Cycles**** (SHOULD; REVIEWED_DRAFT)
  **Integrate Feedback into Development Cycles**
  Acceptance: **Integrate Feedback into Development Cycles**; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-482 r1 — Incorporate feedback into product development and improvement cycles to ensure c...** (SHOULD; REVIEWED_DRAFT)
  Incorporate feedback into product development and improvement cycles to ensure continuous enhancement.
  Acceptance: Incorporate feedback into product development and improvement cycles to ensure continuous enhancement.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-483 r1 — Track the implementation of feedback-driven changes.** (SHOULD; REVIEWED_DRAFT)
  Track the implementation of feedback-driven changes.
  Acceptance: Track the implementation of feedback-driven changes.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-484 r1 — Ensure that GitHub Enterprise-specific feedback is integrated into development a...** (SHOULD; REVIEWED_DRAFT)
  Ensure that GitHub Enterprise-specific feedback is integrated into development and operational processes and to establish a regular cadence with GitHub to provide feedback using Services, Support, or Partners.
  Acceptance: Ensure that GitHub Enterprise-specific feedback is integrated into development and operational processes and to establish a regular cadence with GitHub to provide feedback using Services, Support, or Partners.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{'enterprise_server': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-485 r1 — **Understand Current Engineering System**** (SHOULD; REVIEWED_DRAFT)
  **Understand Current Engineering System**
  Acceptance: **Understand Current Engineering System**; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-486 r1 — Audit existing engineering processes and workflows.** (SHOULD; REVIEWED_DRAFT)
  Audit existing engineering processes and workflows.
  Acceptance: Audit existing engineering processes and workflows.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-487 r1 — Gather baseline data across the engineering system.** (SHOULD; REVIEWED_DRAFT)
  Gather baseline data across the engineering system.
  Acceptance: Gather baseline data across the engineering system.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-488 r1 — Identify friction points and analyze root causes of the bottlenecks.** (SHOULD; REVIEWED_DRAFT)
  Identify friction points and analyze root causes of the bottlenecks.
  Acceptance: Identify friction points and analyze root causes of the bottlenecks.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-489 r1 — Interview developers about experiences, challenges, cultural and process perform...** (SHOULD; REVIEWED_DRAFT)
  Interview developers about experiences, challenges, cultural and process performance impacting factors.
  Acceptance: Interview developers about experiences, challenges, cultural and process performance impacting factors.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-490 r1 — Map engineering efforts to organizational priorities.** (SHOULD; REVIEWED_DRAFT)
  Map engineering efforts to organizational priorities.
  Acceptance: Map engineering efforts to organizational priorities.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-491 r1 — **Map and Prioritize Findings**** (SHOULD; REVIEWED_DRAFT)
  **Map and Prioritize Findings**
  Acceptance: **Map and Prioritize Findings**; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-492 r1 — Categorize barriers by the [four engineering system success zones](./recommendat...** (SHOULD; REVIEWED_DRAFT)
  Categorize barriers by the [four engineering system success zones](./recommendations/engineering-system-metrics).
  Acceptance: Categorize barriers by the [four engineering system success zones](./recommendations/engineering-system-metrics).; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-493 r1 — Map barriers' interconnections between zones and capability areas.** (SHOULD; REVIEWED_DRAFT)
  Map barriers' interconnections between zones and capability areas.
  Acceptance: Map barriers' interconnections between zones and capability areas.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-494 r1 — Prioritize barriers based on impact and organizational alignment.** (SHOULD; REVIEWED_DRAFT)
  Prioritize barriers based on impact and organizational alignment.
  Acceptance: Prioritize barriers based on impact and organizational alignment.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-495 r1 — Select metrics to track progress.** (SHOULD; REVIEWED_DRAFT)
  Select metrics to track progress.
  Acceptance: Select metrics to track progress.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-496 r1 — **Evaluate and Implement Interventions**** (SHOULD; REVIEWED_DRAFT)
  **Evaluate and Implement Interventions**
  Acceptance: **Evaluate and Implement Interventions**; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-497 r1 — Assess potential solutions based on cost, risk, and benefits.** (SHOULD; REVIEWED_DRAFT)
  Assess potential solutions based on cost, risk, and benefits.
  Acceptance: Assess potential solutions based on cost, risk, and benefits.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-498 r1 — Prioritize high-impact interventions.** (SHOULD; REVIEWED_DRAFT)
  Prioritize high-impact interventions.
  Acceptance: Prioritize high-impact interventions.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-499 r1 — Pilot and evaluate solutions before full-scale implementation.** (SHOULD; REVIEWED_DRAFT)
  Pilot and evaluate solutions before full-scale implementation.
  Acceptance: Pilot and evaluate solutions before full-scale implementation.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-500 r1 — **Establish Balanced Metrics**** (SHOULD; REVIEWED_DRAFT)
  **Establish Balanced Metrics**
  Acceptance: **Establish Balanced Metrics**; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-501 r1 — Define leading and lagging indicators for all [four engineering system success z...** (SHOULD; REVIEWED_DRAFT)
  Define leading and lagging indicators for all [four engineering system success zones](./recommendations/engineering-system-metrics).
  Acceptance: Define leading and lagging indicators for all [four engineering system success zones](./recommendations/engineering-system-metrics).; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-502 r1 — Track metrics across all zones in a balanced way.** (SHOULD; REVIEWED_DRAFT)
  Track metrics across all zones in a balanced way.
  Acceptance: Track metrics across all zones in a balanced way.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-503 r1 — Review metrics periodically to identify emerging trends.** (SHOULD; REVIEWED_DRAFT)
  Review metrics periodically to identify emerging trends.
  Acceptance: Review metrics periodically to identify emerging trends.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-504 r1 — **Scale and Refine Successful Interventions**** (SHOULD; REVIEWED_DRAFT)
  **Scale and Refine Successful Interventions**
  Acceptance: **Scale and Refine Successful Interventions**; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-505 r1 — Scale proven interventions while continuously monitoring for outliers.** (SHOULD; REVIEWED_DRAFT)
  Scale proven interventions while continuously monitoring for outliers.
  Acceptance: Scale proven interventions while continuously monitoring for outliers.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-506 r1 — Use AIOps and automation to analyze early signals and performance data.** (SHOULD; REVIEWED_DRAFT)
  Use AIOps and automation to analyze early signals and performance data.
  Acceptance: Use AIOps and automation to analyze early signals and performance data.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-OPS-507 r1 — Foster a growth mindset that values both successes and failures.** (SHOULD; REVIEWED_DRAFT)
  Foster a growth mindset that values both successes and failures.
  Acceptance: Foster a growth mindset that values both successes and failures.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

## Rule

- [ ] **GES-RULE-010 r1 — No approving reviews required before merge** (MUST; REVIEWED_DRAFT)
  CRITICAL: Require at least 1 approving review before merge to enforce code review and catch errors or malicious changes.
  Acceptance: CRITICAL: Require at least 1 approving review before merge to enforce code review and catch errors or malicious changes.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `effective_rule`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-RULE-011 r1 — Stale reviews not dismissed on new commits** (MUST; REVIEWED_DRAFT)
  Enable stale review dismissal so that existing approvals are invalidated when new commits are pushed, ensuring reviewers always see the latest code.
  Acceptance: Enable stale review dismissal so that existing approvals are invalidated when new commits are pushed, ensuring reviewers always see the latest code.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `effective_rule`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-RULE-012 r1 — Code owner review not required** (SHOULD; REVIEWED_DRAFT)
  Enable the code owner review requirement so changes to paths defined in CODEOWNERS must be approved by the designated owner.
  Acceptance: Enable the code owner review requirement so changes to paths defined in CODEOWNERS must be approved by the designated owner.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `effective_rule`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-RULE-013 r1 — Pull request reviews not configured** (MUST; REVIEWED_DRAFT)
  CRITICAL: Configure PR review requirements including required approver count, stale review dismissal, and code owner reviews.
  Acceptance: CRITICAL: Configure PR review requirements including required approver count, stale review dismissal, and code owner reviews.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `effective_rule`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-RULE-014 r1 — No required status checks configured** (MUST; REVIEWED_DRAFT)
  Configure CI/CD checks that must pass before any pull request can be merged.
  Acceptance: Configure CI/CD checks that must pass before any pull request can be merged.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `effective_rule`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-RULE-015 r1 — Force pushes allowed on protected branch** (MUST; REVIEWED_DRAFT)
  CRITICAL: Disable force pushes on all protected branches to prevent history rewriting.
  Acceptance: CRITICAL: Disable force pushes on all protected branches to prevent history rewriting.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `effective_rule`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-RULE-016 r1 — Branch deletion allowed on protected branch** (MUST; REVIEWED_DRAFT)
  Disable branch deletion for all protected branches.
  Acceptance: Disable branch deletion for all protected branches.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `effective_rule`; scope: repository.
  Applicability: `{}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

## Sec

- [ ] **GES-SEC-012 r1 — Suspicious audit log events detected** (MUST; REVIEWED_DRAFT)
  Review the flagged events in the Enterprise audit log immediately. Actions like repo.destroy, org.remove_member, and oauth_access.revoke can indicate account compromise. Investigate and remediate as needed.
  Acceptance: Review the flagged events in the Enterprise audit log immediately. Actions like repo.destroy, org.remove_member, and oauth_access.revoke can indicate account compromise. Investigate and remediate as needed.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: enterprise.
  Applicability: `{'enterprise_server': True, 'software': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-SEC-013 r1 — Audit log streaming configuration cannot be verified** (MUST; REVIEWED_DRAFT)
  Manually verify that audit log streaming is enabled and targeting a SIEM or secure storage in Enterprise → Settings → Audit log → Audit log streaming.
  Acceptance: Manually verify that audit log streaming is enabled and targeting a SIEM or secure storage in Enterprise → Settings → Audit log → Audit log streaming.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: enterprise.
  Applicability: `{'enterprise_server': True, 'software': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-SEC-014 r1 — GitHub Advanced Security not enabled at enterprise level** (MUST; REVIEWED_DRAFT)
  Enable GHAS enterprise-wide to unlock code scanning, secret scanning, and dependency review across all organizations. Requires a GHAS license.
  Acceptance: Enable GHAS enterprise-wide to unlock code scanning, secret scanning, and dependency review across all organizations. Requires a GHAS license.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: enterprise.
  Applicability: `{'enterprise_server': True, 'software': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-SEC-015 r1 — Secret scanning not enabled as enterprise default** (MUST; REVIEWED_DRAFT)
  Enable secret scanning as an enterprise default to detect leaked credentials across all repositories.
  Acceptance: Enable secret scanning as an enterprise default to detect leaked credentials across all repositories.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: enterprise.
  Applicability: `{'enterprise_server': True, 'software': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-SEC-016 r1 — Secret scanning push protection not enabled as enterprise default** (MUST; REVIEWED_DRAFT)
  Enable push protection as an enterprise default to block commits containing secrets before they reach repositories.
  Acceptance: Enable push protection as an enterprise default to block commits containing secrets before they reach repositories.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: enterprise.
  Applicability: `{'enterprise_server': True, 'software': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-SEC-017 r1 — Secret scanning for non-provider patterns not enabled as enterprise default** (MAY; REVIEWED_DRAFT)
  Enable detection of generic and non-provider secrets as an enterprise default for broader secret scanning coverage.
  Acceptance: Enable detection of generic and non-provider secrets as an enterprise default for broader secret scanning coverage.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: enterprise.
  Applicability: `{'enterprise_server': True, 'software': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-SEC-018 r1 — Code scanning alerts open across enterprise** (MUST; REVIEWED_DRAFT)
  Review and address all open code scanning findings across affected organizations and repositories.
  Acceptance: Review and address all open code scanning findings across affected organizations and repositories.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: enterprise.
  Applicability: `{'enterprise_server': True, 'software': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-SEC-019 r1 — Secret scanning alerts open across enterprise** (MUST; REVIEWED_DRAFT)
  Immediately revoke and rotate any exposed secrets, then close the secret scanning alerts after confirming remediation.
  Acceptance: Immediately revoke and rotate any exposed secrets, then close the secret scanning alerts after confirming remediation.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: enterprise.
  Applicability: `{'enterprise_server': True, 'software': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-SEC-020 r1 — Audit log forwarding configuration cannot be verified automatically** (MUST; REVIEWED_DRAFT)
  Manually verify that audit log forwarding (syslog) is enabled and targeting a SIEM or secure log aggregation service (Site Admin → Monitoring → Log forwarding)
  Acceptance: Manually verify that audit log forwarding (syslog) is enabled and targeting a SIEM or secure log aggregation service (Site Admin → Monitoring → Log forwarding); Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: enterprise.
  Applicability: `{'enterprise_server': True, 'software': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-SEC-021 r1 — GHES signing key rotation status cannot be verified automatically** (MUST; REVIEWED_DRAFT)
  Manually verify that the GHES trusted update signing key has been rotated per GitHub guidance so future updates and security patches can be verified and applied
  Acceptance: Manually verify that the GHES trusted update signing key has been rotated per GitHub guidance so future updates and security patches can be verified and applied; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: enterprise.
  Applicability: `{'enterprise_server': True, 'software': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-SEC-022 r1 — Suspicious audit log events detected** (MUST; REVIEWED_DRAFT)
  Review these events in the GHES site admin audit log immediately. Actions like repo.destroy, staff.fake_login, and staff.set_site_admin can indicate account compromise or insider threats
  Acceptance: Review these events in the GHES site admin audit log immediately. Actions like repo.destroy, staff.fake_login, and staff.set_site_admin can indicate account compromise or insider threats; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: enterprise.
  Applicability: `{'enterprise_server': True, 'software': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-SEC-023 r1 — No suspicious audit log events detected** (MAY; REVIEWED_DRAFT)
  Continue monitoring the audit log regularly. Configure log forwarding to a SIEM for centralized monitoring
  Acceptance: Continue monitoring the audit log regularly. Configure log forwarding to a SIEM for centralized monitoring; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: enterprise.
  Applicability: `{'enterprise_server': True, 'software': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-SEC-024 r1 — GitHub Advanced Security (GHAS) is not enabled on the GHES instance** (MUST; REVIEWED_DRAFT)
  Enable GHAS to unlock code scanning, secret scanning, and dependency review across all organizations
  Acceptance: Enable GHAS to unlock code scanning, secret scanning, and dependency review across all organizations; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: enterprise.
  Applicability: `{'enterprise_server': True, 'software': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-SEC-025 r1 — Secret scanning is not enabled on the GHES instance** (MUST; REVIEWED_DRAFT)
  Enable secret scanning to detect leaked credentials in repositories
  Acceptance: Enable secret scanning to detect leaked credentials in repositories; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: enterprise.
  Applicability: `{'enterprise_server': True, 'software': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-SEC-026 r1 — Secret scanning status could not be confirmed on this GHES instance** (MAY; REVIEWED_DRAFT)
  A non-2xx response can mean (a) the feature is not supported on this GHES version, (b) the feature exists but is not licensed or enabled at the appliance level, or (c) the scanning token lacks the required scope. Verify which case applies before treating this as a misconfiguration
  Acceptance: A non-2xx response can mean (a) the feature is not supported on this GHES version, (b) the feature exists but is not licensed or enabled at the appliance level, or (c) the scanning token lacks the required scope. Verify which case applies before treating this as a misconfiguration; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: enterprise.
  Applicability: `{'enterprise_server': True, 'software': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-SEC-027 r1 — Secret scanning push protection is not enabled** (MUST; REVIEWED_DRAFT)
  Enable push protection to block commits containing secrets before they reach the repository
  Acceptance: Enable push protection to block commits containing secrets before they reach the repository; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: enterprise.
  Applicability: `{'enterprise_server': True, 'software': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-SEC-028 r1 — Code scanning is not enabled on the GHES instance** (MUST; REVIEWED_DRAFT)
  Enable code scanning (CodeQL) to automatically find security vulnerabilities in code
  Acceptance: Enable code scanning (CodeQL) to automatically find security vulnerabilities in code; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: enterprise.
  Applicability: `{'enterprise_server': True, 'software': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-SEC-029 r1 — Code scanning status could not be confirmed on this GHES instance** (MAY; REVIEWED_DRAFT)
  A non-2xx response can mean (a) the feature is not supported on this GHES version, (b) the feature exists but is not licensed or enabled at the appliance level, or (c) the scanning token lacks the required scope. Verify which case applies before treating this as a misconfiguration
  Acceptance: A non-2xx response can mean (a) the feature is not supported on this GHES version, (b) the feature exists but is not licensed or enabled at the appliance level, or (c) the scanning token lacks the required scope. Verify which case applies before treating this as a misconfiguration; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: enterprise.
  Applicability: `{'enterprise_server': True, 'software': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-SEC-030 r1 — Code scanning alerts open across the GHES instance** (MUST; REVIEWED_DRAFT)
  Review and address open code scanning findings
  Acceptance: Review and address open code scanning findings; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: enterprise.
  Applicability: `{'enterprise_server': True, 'software': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-SEC-031 r1 — Secret scanning alerts open across the GHES instance** (MUST; REVIEWED_DRAFT)
  Immediately revoke and rotate any exposed secrets
  Acceptance: Immediately revoke and rotate any exposed secrets; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: enterprise.
  Applicability: `{'enterprise_server': True, 'software': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-SEC-032 r1 — Code scanning alerts API could not be confirmed on this GHES instance** (MAY; REVIEWED_DRAFT)
  A non-2xx response can mean (a) the feature is not supported on this GHES version, (b) the feature exists but is not licensed or enabled at the appliance level, or (c) the scanning token lacks the required scope. Verify which case applies before treating this as a misconfiguration
  Acceptance: A non-2xx response can mean (a) the feature is not supported on this GHES version, (b) the feature exists but is not licensed or enabled at the appliance level, or (c) the scanning token lacks the required scope. Verify which case applies before treating this as a misconfiguration; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: enterprise.
  Applicability: `{'enterprise_server': True, 'software': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-SEC-033 r1 — Secret scanning alerts API could not be confirmed on this GHES instance** (MAY; REVIEWED_DRAFT)
  A non-2xx response can mean (a) the feature is not supported on this GHES version, (b) the feature exists but is not licensed or enabled at the appliance level, or (c) the scanning token lacks the required scope. Verify which case applies before treating this as a misconfiguration
  Acceptance: A non-2xx response can mean (a) the feature is not supported on this GHES version, (b) the feature exists but is not licensed or enabled at the appliance level, or (c) the scanning token lacks the required scope. Verify which case applies before treating this as a misconfiguration; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: enterprise.
  Applicability: `{'enterprise_server': True, 'software': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-SEC-034 r1 — Code scanning alerts open across organization** (MUST; REVIEWED_DRAFT)
  Review and address all open code scanning findings across affected repositories.
  Acceptance: Review and address all open code scanning findings across affected repositories.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: organization.
  Applicability: `{'organization': True, 'software': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-SEC-035 r1 — Secret scanning alerts open across organization** (MUST; REVIEWED_DRAFT)
  Immediately revoke and rotate any exposed secrets, then close the secret scanning alerts after confirming remediation.
  Acceptance: Immediately revoke and rotate any exposed secrets, then close the secret scanning alerts after confirming remediation.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: organization.
  Applicability: `{'organization': True, 'software': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-SEC-036 r1 — Two-factor authentication not required** (MUST; REVIEWED_DRAFT)
  Enable the 2FA requirement in organization security settings to ensure all members must use two-factor authentication.
  Acceptance: Enable the 2FA requirement in organization security settings to ensure all members must use two-factor authentication.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: organization.
  Applicability: `{'organization': True, 'software': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-SEC-037 r1 — Web commit signoff not required** (SHOULD; REVIEWED_DRAFT)
  Consider enabling web commit signoff to improve the audit trail for changes made directly through the GitHub UI.
  Acceptance: Consider enabling web commit signoff to improve the audit trail for changes made directly through the GitHub UI.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: organization.
  Applicability: `{'organization': True, 'software': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-SEC-038 r1 — EMU enabled: two-factor authentication is controlled by your identity provider** (MAY; REVIEWED_DRAFT)
  Ensure MFA is enforced in your identity provider. For Microsoft Entra ID, configure a Conditional Access policy requiring MFA for all users.
  Acceptance: Ensure MFA is enforced in your identity provider. For Microsoft Entra ID, configure a Conditional Access policy requiring MFA for all users.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: organization.
  Applicability: `{'organization': True, 'software': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-SEC-039 r1 — Secret scanning not enabled by default for new repositories** (MUST; REVIEWED_DRAFT)
  Enable 'Secret scanning' in Organization → Settings → Code security and analysis to protect all new repositories from the moment they are created.
  Acceptance: Enable 'Secret scanning' in Organization → Settings → Code security and analysis to protect all new repositories from the moment they are created.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: organization.
  Applicability: `{'organization': True, 'software': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-SEC-040 r1 — Secret scanning push protection not enabled by default for new repositories** (MUST; REVIEWED_DRAFT)
  Enable 'Push protection' in Organization → Settings → Code security and analysis to block commits containing secrets before they reach the repository.
  Acceptance: Enable 'Push protection' in Organization → Settings → Code security and analysis to block commits containing secrets before they reach the repository.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: organization.
  Applicability: `{'organization': True, 'software': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-SEC-041 r1 — GitHub Advanced Security not enabled by default for new repositories** (SHOULD; REVIEWED_DRAFT)
  Enable 'GitHub Advanced Security' in Organization → Settings → Code security and analysis (requires a GHAS license).
  Acceptance: Enable 'GitHub Advanced Security' in Organization → Settings → Code security and analysis (requires a GHAS license).; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: organization.
  Applicability: `{'organization': True, 'software': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-SEC-042 r1 — Private vulnerability reporting not enabled by default for new repositories** (SHOULD; REVIEWED_DRAFT)
  Enable 'Private vulnerability reporting' in Organization → Settings → Code security and analysis to allow security researchers to privately report vulnerabilities for all new repositories.
  Acceptance: Enable 'Private vulnerability reporting' in Organization → Settings → Code security and analysis to allow security researchers to privately report vulnerabilities for all new repositories.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: organization.
  Applicability: `{'organization': True, 'software': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-SEC-043 r1 — Deploy keys with write access** (MUST; REVIEWED_DRAFT)
  Use read-only deploy keys where possible. For write operations, prefer GitHub Apps or OIDC federation, which provide better auditability and can be rotated more easily.
  Acceptance: Use read-only deploy keys where possible. For write operations, prefer GitHub Apps or OIDC federation, which provide better auditability and can be rotated more easily.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `deploy_keys`; scope: repository.
  Applicability: `{'software': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-SEC-044 r1 — Unverified deploy keys** (SHOULD; REVIEWED_DRAFT)
  Verify all deploy keys to ensure they are associated with authorized systems and remove any unknown keys.
  Acceptance: Verify all deploy keys to ensure they are associated with authorized systems and remove any unknown keys.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `deploy_keys`; scope: repository.
  Applicability: `{'software': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-SEC-045 r1 — Deploy keys present — consider GitHub Apps or OIDC** (SHOULD; REVIEWED_DRAFT)
  Consider migrating to GitHub Apps or OIDC federation for automated deployment credentials, which offer better security, auditability, and key rotation.
  Acceptance: Consider migrating to GitHub Apps or OIDC federation for automated deployment credentials, which offer better security, auditability, and key rotation.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `deploy_keys`; scope: repository.
  Applicability: `{'software': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-SEC-046 r1 — Dependabot alerts not enabled** (MUST; REVIEWED_DRAFT)
  Enable Dependabot alerts in repository settings to receive security vulnerability notifications for your dependencies.
  Acceptance: Enable Dependabot alerts in repository settings to receive security vulnerability notifications for your dependencies.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `dependabot_alerts`; scope: repository.
  Applicability: `{'software': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-SEC-047 r1 — Critical Dependabot alerts open** (MUST; REVIEWED_DRAFT)
  Immediately address critical security vulnerabilities by updating the affected dependencies or applying patches.
  Acceptance: Immediately address critical security vulnerabilities by updating the affected dependencies or applying patches.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `dependabot_alerts`; scope: repository.
  Applicability: `{'software': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-SEC-048 r1 — High-severity Dependabot alerts open** (MUST; REVIEWED_DRAFT)
  Prioritize fixing high-severity dependency vulnerabilities to reduce the attack surface of this repository.
  Acceptance: Prioritize fixing high-severity dependency vulnerabilities to reduce the attack surface of this repository.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `dependabot_alerts`; scope: repository.
  Applicability: `{'software': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-SEC-049 r1 — No SECURITY.md file found** (MAY; REVIEWED_DRAFT)
  Add a SECURITY.md file to document how security vulnerabilities should be reported for this project.
  Acceptance: Add a SECURITY.md file to document how security vulnerabilities should be reported for this project.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `file_present`; scope: repository.
  Applicability: `{'software': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-SEC-050 r1 — Dependabot alerts enabled but no dependabot.yml found** (SHOULD; REVIEWED_DRAFT)
  Create a .github/dependabot.yml file to enable automated dependency version update pull requests in addition to alerts.
  Acceptance: Create a .github/dependabot.yml file to enable automated dependency version update pull requests in addition to alerts.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `dependabot_config`; scope: repository.
  Applicability: `{'software': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-SEC-051 r1 — Dependabot not configured** (MUST; REVIEWED_DRAFT)
  Enable Dependabot alerts and create .github/dependabot.yml for automated security and version updates of dependencies.
  Acceptance: Enable Dependabot alerts and create .github/dependabot.yml for automated security and version updates of dependencies.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `dependabot_config`; scope: repository.
  Applicability: `{'software': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-SEC-052 r1 — Code scanning (CodeQL) not configured** (MUST; REVIEWED_DRAFT)
  Enable GitHub code scanning with CodeQL to automatically detect security vulnerabilities in your source code on every pull request.
  Acceptance: Enable GitHub code scanning with CodeQL to automatically detect security vulnerabilities in your source code on every pull request.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `code_scanning_alerts`; scope: repository.
  Applicability: `{'software': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-SEC-053 r1 — No custom CodeQL configuration file** (MAY; REVIEWED_DRAFT)
  Consider creating a custom CodeQL configuration file to extend scanning with additional security queries or to exclude false-positive paths.
  Acceptance: Consider creating a custom CodeQL configuration file to extend scanning with additional security queries or to exclude false-positive paths.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `manual`; scope: repository.
  Applicability: `{'software': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

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

- [ ] **GES-RULE-001 r1 — Protected branch cannot be deleted** (MUST; REVIEWED_DRAFT)
  Verify the effective active rule and any declared policy parameter on the assessed branch. Review legacy equivalents and bypass actors separately.
  Acceptance: Verify the effective active rule and any declared policy parameter on the assessed branch. Review legacy equivalents and bypass actors separately.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `effective_rule`; scope: repository.
  Applicability: `{'protected_branch': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-RULE-002 r1 — Protected branch rejects non-fast-forward updates** (MUST; REVIEWED_DRAFT)
  Verify the effective active rule and any declared policy parameter on the assessed branch. Review legacy equivalents and bypass actors separately.
  Acceptance: Verify the effective active rule and any declared policy parameter on the assessed branch. Review legacy equivalents and bypass actors separately.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `effective_rule`; scope: repository.
  Applicability: `{'protected_branch': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-RULE-003 r1 — Pull request integration is required** (MUST; REVIEWED_DRAFT)
  Verify the effective active rule and any declared policy parameter on the assessed branch. Review legacy equivalents and bypass actors separately.
  Acceptance: Verify the effective active rule and any declared policy parameter on the assessed branch. Review legacy equivalents and bypass actors separately.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `effective_rule`; scope: repository.
  Applicability: `{'protected_branch': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-RULE-004 r1 — Approving review threshold matches policy** (MUST; REVIEWED_DRAFT)
  Verify the effective active rule and any declared policy parameter on the assessed branch. Review legacy equivalents and bypass actors separately.
  Acceptance: Verify the effective active rule and any declared policy parameter on the assessed branch. Review legacy equivalents and bypass actors separately.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `effective_rule`; scope: repository.
  Applicability: `{'protected_branch': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-RULE-005 r1 — Stale approvals are dismissed** (MUST; REVIEWED_DRAFT)
  Verify the effective active rule and any declared policy parameter on the assessed branch. Review legacy equivalents and bypass actors separately.
  Acceptance: Verify the effective active rule and any declared policy parameter on the assessed branch. Review legacy equivalents and bypass actors separately.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
  Verification: `effective_rule`; scope: repository.
  Applicability: `{'protected_branch': True}`.
  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.

- [ ] **GES-RULE-006 r1 — Review conversations are resolved** (MUST; REVIEWED_DRAFT)
  Verify the effective active rule and any declared policy parameter on the assessed branch. Review legacy equivalents and bypass actors separately.
  Acceptance: Verify the effective active rule and any declared policy parameter on the assessed branch. Review legacy equivalents and bypass actors separately.; Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.
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

