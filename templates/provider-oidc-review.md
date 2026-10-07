# Provider OIDC credential review

Control and revision: {{CONTROL_ID}} revision {{CONTROL_REVISION}}
Target and exact workflow revision: {{TARGET_REVISION}}
Reviewer and accountable owner: {{REVIEWER}}
Review date and expiration: {{REVIEW_WINDOW}}
Provider, platform/version and intended resource scope: {{PROVIDER_SCOPE}}
Evidence locations and observed outcome: {{EVIDENCE_AND_OUTCOME}}

Use this record for GES-ACT-006 alongside
[the common Actions security review](actions-security-review.md). Values identify
the review; filling or rendering this form is not a passing attestation. Missing
observations remain UNKNOWN. Record identifiers and evidence references, never
JWTs, credential values, decrypted secrets or authorization headers.

| Boundary | Observation and accountable decision |
|---|---|
| Credential choice | Identify the supported federation mechanism, resulting resource permissions, credential lifetime and renewal/revocation behavior. Explain any long-lived credential still needed and its scope. Do not copy an illustrative lifetime as policy. |
| Issuer and platform | Observe the actual issuer, discovery/JWKS access and supported platform/version. Separate GitHub.com, GHE.com and GHES assumptions. Name-only and immutable-ID subjects differ; compare the actual subject with effective provider conditions. |
| Trust | Record the audience, subject/claim conditions, admitted owner/repository/workflow revision, event/ref/environment and at least one condition excluding untrusted repositories. Record provider-supported fields and the reason for each restriction or omission. A repository wildcard admits broader callers than an exact branch/environment condition. |
| Issuance and elevation | Identify the exact job allowed to request OIDC, its consuming step and approval owner. Setting the id-token permission to write enables issuance, not repository or cloud resource write. Justify resource privilege separately. |
| Environment and runner | Record environment reviewers, deployment branches/tags, bypass authority, secret release, runner eligibility/isolation and network reach. YAML names alone do not establish protection or isolation. |
| Dependencies and material | Check immutable action origin and reviewed revision, caller/build artifact integrity, credential-file handling, logs/argv and cleanup on failure. A 40-character reference is not origin verification. Use the common Actions record for the full dependency and disclosure review. |
| Behavior and freshness | Link effective-policy readback and separately authorized positive/negative tests to the exact target revision. Record evidence expiry, failures, limitations and drift. Without those observations, native/cloud behavior remains unverified. |

The pinned guides provide the following qualified reference points. These are
review prompts, not universal upstream requirements or verified provider state.

| Provider | Distinctions to retain |
|---|---|
| AWS | This pin excludes custom OIDC claims. The official AWS action uses sts.amazonaws.com as audience. Compare branch, environment and wildcard subjects; the guide's immutable-ID wording covers new or opted-in repositories and excludes GHES. GHES needs accessible discovery/JWKS endpoints; IP filtering is an option. |
| Azure | api://AzureADTokenExchange is recommended; alternatives are allowed and need review. The guide includes post-date renames/transfers in immutable-ID subject wording. GHES issuer must be publicly routable, with no fixed Entra IP ranges for discovery/JWKS. |
| Google Cloud | Review identity pool, claim mapping/conditions, service account and actual role bindings. The guide includes renames/transfers in subject wording; source role descriptions are not proof of effective IAM semantics. GHES requires publicly routable issuer/discovery/JWKS access without fixed GCP IP ranges. |
| Vault | At least one bound-claim condition is required in this guide; bound subject/audiences are optional. The 10-minute TTL and repository-wide example are illustrative. Unique enterprise issuer settings must agree. Enterprise/HCP namespace is required where applicable. Immediate revocation is optional; exporting a token and verbose curl cleanup need disclosure review. |
| PyPI | This guide covers FPT/GHEC, not GHES. Match exact publisher owner/repository/workflow; environment is optional. The publishing job requests OIDC and omits username/password. Separating build and publish still requires artifact integrity and action-origin evidence. Wrong publisher identity exposes publication authority. |

For each finding, record the affected job/condition, source/control relation,
remediation owner, repair, repeatable checks and remaining uncertainty. Record
the actual review date and expiration in an authorized attestation bound to this
control revision and target revision. This form grants no cloud mutation,
package publication, organization policy adoption or estate rollout authority.
