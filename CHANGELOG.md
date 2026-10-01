# Changelog

## 0.1.0 — 2026-10-01

Initial six-source pinned acquisition, candidate and page ledgers, 95 reviewed-draft controls, 22 templates, six draft profiles, read-only collection, assessment, human attestations, exceptions, gates, compilation, change-impact analysis and false-pass regression tests. Native enforcement and exhaustive semantic review remain open.

## 0.2.0 — 2026-10-01

Completed exhaustive source consolidation and operationalization:
- 688 canonical controls (593 new from GHQR 129 + Well-Architected 476 structured requirements)
- 12 automated checkers: file_present, metadata_nonempty, repo_name, workflow_permissions, workflow_pinning, effective_rule, manual, dependabot_config, actions_permissions, deploy_keys, codeowners_validation, code_scanning_alerts, secret_scanning_alerts, dependabot_alerts
- Fixed all Copilot/Codex review findings (8 high/medium issues resolved)
- 76 regression tests passing (21 new tests for edge cases and negative enforcement)
- Full Git tree reconciliation for all 6 sources (13,657 artifacts, 0 mismatches)
- 18,019 English published page-version instances inventoried across 7 versions
- 605 structured requirements reviewed and mapped (100% coverage)
- Source rights clearance documented for all 6 sources (MIT, CC BY 4.0, and no-license with provenance references)
- Generated functional checklist, source crosswalk, and bindings for all 688 controls
- All controls remain REVIEWED_DRAFT; no native policy silently activated
