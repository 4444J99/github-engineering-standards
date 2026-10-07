# Actions security implementation review

Target repository and workflow revision: <required>
Reviewer, accountable owner, review date and expiry: <required>
Platform/version, event, caller and called workflow: <required>
Outcome: <UNKNOWN until reviewed; record PASS/FAIL/PARTIAL with evidence>

Use this record alongside GES-ACT-001 through GES-ACT-006 and GES-SEC-004.
Record names, scope and evidence locations; omit credential values, JWTs, request
authorization tokens and decrypted secret contents. An empty field is unknown.
This review does not grant policy adoption or permission to change cloud settings.

| Boundary | Required observation and decision |
|---|---|
| Workflow observation | Bind the complete file inventory to the target revision. Resolve symlink targets before treating their contents as a workflow or local dependency. Check nonempty jobs and one execution form per step. |
| Default token | Record the explicit read-only or empty root permissions and inherited organization/repository settings. Broad root write is a failed default-permission check. |
| Elevated job | For each job with write permission, name the exact scope, consuming step, purpose, event/input trust, approval owner and expiry. Setting the `id-token` permission to `write` enables JWT issuance; cloud-role and repository-write authority are separate. A valid elevation remains MANUAL_REVIEW until justified. |
| Untrusted input | Trace expressions into generated scripts, argv, environment and action inputs. Use quoted intermediate variables or reviewed action inputs; inspect privileged pull_request_target/workflow_run checkout, cache and artifact boundaries. |
| Dependencies | Record full action/workflow commit SHAs or container digests, upstream origin verification, source audit, update owner and reviewed revision changes. Syntactic pinning alone does not prove provenance. |
| Secret scope | Record accessible organization/repository/environment secret names and repository access policy. Account for overrides, alphabetical organization limits, queue-time versus job-start reads, missing values and reusable-workflow passing. |
| Disclosure | Review stdout/stderr on success and failure, generated/transformed values and process arguments. Mask sensitive generated values before output. Base64 does not encrypt, and decrypted large-secret files are not automatically redacted. Remove demonstration token/plaintext printing. |
| Runner | Record hosted/self-hosted eligibility, runner-group/cross-repository reach, resident credentials and network access. Environment approval is not isolation; one-job JIT registration is not proof of clean reused hardware. Bind cleanup evidence to the actual runner. |
| OIDC trust | Identify provider/issuer, audience, caller identity, called job_workflow_ref, exact reviewed called-workflow revision, allowed event/ref/environment and at least one condition excluding untrusted repositories. Check provider support for custom claims and subject customization; record actual access-token lifetime. |
| Environment | Record required reviewers, allowed branches/tags, secret release and bypass authority using effective configuration and behavior evidence. A proposed environment name or YAML reference does not prove enforcement. |
| Updates and audit | Check advisories separately for SHA-pinned Actions because semantic-version Dependabot alert coverage is narrower. Record update/review owners and audit-log evidence without copying secrets. |

For each finding, record the source proposition/control, exact affected job or
dependency, repair, repeatable positive and negative checks, and the unresolved
limit. Mark native/cloud behavior unverified until separately authorized tests
and effective-policy readback establish it. Retain missing evidence as UNKNOWN.
