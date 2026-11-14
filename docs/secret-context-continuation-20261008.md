# Secret context continuation — 2026-10-08

This is a bounded primary review of **245 existing claims in eight complete
GitHub Docs contexts** at pin
`56fcfa816f27bca239e5d39fff0d4f74f77ec995`. It proposes 18 narrow mappings,
226 references and one unsupported-source exclusion. The original 1,866
reconciliation records and all 95 draft controls remain unchanged by this packet.

The [scope manifest](../evidence/secret-context-continuation-20261008-scope.json)
binds the exact selected claim IDs, five original claim documents, source hashes,
catalog and proposal digests, frozen workload and existing receipt ledger at
baseline `c785a0abb6a5ac085f796b129472732335343f76`. The
[primary review](../evidence/secret-context-continuation-20261008-primary-review.json)
records every original statement, exact subject, disposition, individual rationale
and source-fidelity judgment. It is frozen as
`PRIMARY_REVIEW_PENDING_INDEPENDENT_AUDIT`; the independent review and any receipt
integration must be separately recorded against these exact bytes.

## Complete source contexts

These full paths select complete source-artifact families that the prior packet's
path selection missed. No same-basename neighboring concept pages are included.

| Pinned source path | Selected claims |
|---|---:|
| `content/code-security/concepts/secret-security/secret-leakage-risks.md` | 38 |
| `content/code-security/concepts/secret-security/secret-security-with-github.md` | 23 |
| `content/code-security/concepts/secret-security/about-alerts.md` | 25 |
| `content/code-security/concepts/secret-security/push-protection.md` | 31 |
| `content/code-security/concepts/secret-security/validity-checks.md` | 26 |
| `content/code-security/concepts/secret-security/bypass-requests.md` | 21 |
| `content/code-security/reference/secret-security/secret-types.md` | 62 |
| `content/code-security/reference/secret-security/custom-patterns.md` | 19 |
| **Total** | **245** |

The eight contexts contain 45,148 original bytes across 688 lines. Their full
frontmatter, version branches, tables, expressions and prose were read. The
`secret-types.md` reference page concerns credential storage and access across
Dependabot, Actions and Codespaces; it is not the provider-pattern data table.

The primary reviewer also read 19 complete reusable or feature files (6,321
bytes), the exact referenced keys in two variable files, and three additional
complete interpretation pages (24,322 bytes). Those additional pages constrain
fork event behavior and Codespaces limit denominators. The report separately
lists their hashes, read scope and the literal interpretation spans used. Linked
procedures, external implementations and nested includes outside the stated
dependency scope receive no implicit review credit.

## Proposed decisions

| Disposition | Count | Meaning in this packet |
|---|---:|---|
| `MAP` | 18 | Narrow support for an existing draft control objective. |
| `REFERENCE` | 226 | Preserved source capability, constraint, example or contextual guidance. |
| `EXCLUDED_WITH_REASON` / `UNSUPPORTED_SOURCE` | 1 | The original assertion exceeds the cited source's scope. |

The mappings support only these parts of the existing revision-1 controls:

| Draft control | Supporting claims | Relationship |
|---|---:|---|
| `GES-SEC-004` | 13 | Preventing disclosure and handling exposed credentials. |
| `GES-SEC-006` | 2 | Assessing exposure and prioritizing active findings. |
| `GES-GOV-006` | 3 | Recording a bypass reason and obtaining a bypass decision. |

These relations do not establish whole-control equivalence, implementation,
accepted risk records, remediation-age measurement or approved exception expiry.
All decisions retain `accepted_policy: false` and `adopted_obligation: null`.

### Preserved extraction failure

`DOCS-SECRET-CONT-ALERT-BYPASS-019` says that a repository alert requires
repository push protection. Its cited note concerns alerts from bypassing
**personal** push protection. The complete alert-generation fragments also
describe ordinary scanning alerts without that prerequisite. The packet excludes
the unqualified assertion, retains its original bytes and keeps source fidelity
`FAIL`. It creates no replacement claim.

The result is **244 source-fidelity passes and one failed extraction with an
explicit exclusion**, not 245 faithful extractions.

### Interpretation boundaries retained

Personal push protection retains its public/cloud scope. Repository and
user-only bypasses have different alert behavior; the reason table distinguishes
closed alerts from open alerts. Delegated approval and exemptions remain separate.
Seven days describes expiry of an unresolved request, without establishing the
lifetime of an approved exception.

The source's Dependabot `pull_request_target` prose identifies a base-ref creator,
while its expression tests the pull-request author's login. That ambiguity stays
explicit. Separately, the overview's fork-secret wording is constrained by the
same-pin Actions security page: fork `pull_request` and related review events
withhold other secrets, while `pull_request_target` workflows can receive
repository and organization secrets. No universal fork-secret predicate is
invented.

The Codespaces overview abbreviates its 100-secret denominator. Its linked pages
separately describe 100 per organization, 100 per repository and 100 in the
personal-account context. Those scopes are retained. Regex anchors, supported
syntax, separate before/secret/after fields and example restrictions also remain
literal source statements; no engine execution or inferred matching guarantee is
recorded.

## Accounting and remaining acceptance

This packet appends zero receipts. A total of **2,111** is conditional on a distinct
independent reviewer approving the exact 245 decisions, an applicable authority
policy binding both roles, and successful receipt validation after integration.
The 61,936 recorded-claim denominator is unchanged. Completing these eight
families does not certify the source-to-claim omission denominator, create
whole-artifact dispositions or add provider-cell credit.

Fresh exact-pin source hydration matched the unchanged A3 inventory identity and
authenticated the complete source snapshots. It did not reproduce missing
historical inputs or reconfirm the historical 18,019 rendered-body count. Raw
upstream bodies remain outside tracked evidence.

At this checkpoint, synthesis is incomplete, release clearance is unverified,
the native pilot is blocked, all nine legacy gates remain open, and zero controls
are accepted. The repository's human review, applicable human security review,
merged-main validation and owner-acceptance requirements remain separate from
this agent-authored primary review.

## Local validation

The following required commands were run in this isolated continuation worktree
with the three new packet files and otherwise unchanged baseline inputs:

| Command | Observed result |
|---|---|
| `python -m unittest discover -s tests -v` | Exit 0; 647 tests passed in 15.467 seconds. |
| `python -m ges validate` | Exit 0; `valid: true`, 95 controls. |
| `python -m ges compile` | Exit 0; no changes to tracked generated files. |
| `git diff --check` | Exit 0; no whitespace errors. |

A direct binding check also rebuilt all 245 exact subjects from the five original
claim documents and the frozen artifact inventory, checked every disposition
against the unchanged catalog, and confirmed all 13 bound baseline inputs and
claim documents were byte-identical to the base commit. This local validation
does not append receipts or substitute for the independent review, integrated
receipt validation, merged-main checks or human acceptance.
