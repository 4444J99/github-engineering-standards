# Bounded warning-only pilot — staged implementation

Owner: @4444J99. Implementation lane: Codex. Authorization: the owner's October 12, 2026 bounded pilot approval and subsequent instruction to resolve eligibility/CI gaps and implement the first advisory controls. This scope does not activate required checks or expand the portfolio. Prior proposal versions remain unchanged in their requested document location.

## Executable scope

`python -m ges.warning_pilot --snapshot SNAPSHOT --plan TRUSTED_PLAN --receipt RECEIPT --output NEW_REPORT`

The first module reuses existing duplicate-key-rejecting workflow permission and immutable-action checks and adds planned execution-receipt inspection. It performs no network requests, executes no candidate code, and changes no repository or account settings. Omit `--receipt` to obtain an explicit NOT_VERIFIABLE execution finding.

Supply a separately retrieved, authorized plan containing positive integer `repository_id`, lowercase 40-character `revision`, lowercase 64-character `plan_digest`, and an ordered, unique, nonempty `checks` list. Neither a candidate-modified plan nor a self-authored receipt authenticates execution. Policy retrieval and producer authentication remain outside this structural inspector and require independent review. Each check observation must carry its name, matching revision, completed/success status, positive runner ID and nonempty completed/success steps. This deliberately narrow first contract does not credit reused or conditionally skipped evidence; those need later reviewed contracts.

Snapshot format: repository ID and revision, plus `observations.files` with `status: OK`, `complete: true` and a `data` mapping from repository paths to source text or typed file entries. It is the existing collector check format with explicit target binding. Incomplete, permission-denied, malformed and mismatched observations never become a positive finding.

Exit 0 means the advisory inspection produced a report; WARN and unknown findings remain visible. Exit 2 means bad input, write error or failed inspection. Output files are exclusive-created to avoid overwriting evidence. Never make exit 0 an aggregate compliance claim or a substitute for existing required checks. New consumers must retain all existing check identities and protections.

## Boundaries

The report always denies compliance certification and native enforcement verification. Permission/pinning checks inspect observed configuration only. They do not establish least privilege in application context, complete GitHub workflow validity, trusted privileged-trigger dataflow, execution authenticity, publication safety, checker integrity, retention, restoration, or six-source completeness. These missing evaluations remain listed in each report.

No workflow or release is activated by adding this CLI. Consumer integration follows positive/adversarial tests, review and an immutable accepted toolkit version. Existing native-enforcement issue #471 and acceptance/rights gates remain distinct. This limited source addition neither clears historical findings nor authorizes a release tag.

## Eligibility and ownership

The three consumer roles remain public package, private site, and documentation. Exact consumer identities, private observations, captured protection payloads and remediation evidence belong in restricted consumer custody, not this public toolkit. Account owner @4444J99 owns restoration of runner admission; Codex owns source remediation, evidence comparison, and bounded onboarding. A source-only assessment is permitted while hosted execution is unavailable; hosted eligibility and observation commencement remain pending. Open unrelated PRs are preserved and do not grant authority over their branches.

A read-only current issue search found existing execution-admission work in the package lane and independent reader-mode work in the documentation lane. The latter's generated instruction outputs remain excluded from this pilot. The first source repair is confined to the runner contract and adversarial regression tests; no unrelated feature, generated file, or protection is changed.

## Acceptance and rollback

Observe each onboarded consumer for seven calendar days and at least two representative changes. Do not count baseline inspection as onboarding or fabricate changes. Require expected fixture outcomes, zero false green, exact revision evidence, owned findings, no unresolved detector defect, applicable artifact/restore proof, and measured governance overhead at most two minutes per run. Incomplete samples remain incomplete.

Stop expansion on false green, unintended publication, privilege violations, check disruption or repeated budget overruns. Roll back the isolated integration through its repository PR rail; retain evidence and verify original protections. As no integration has been activated yet, a source revert is reversible but is not a demonstrated hosted rollback. Required-check activation and any fourth consumer need separate authorization.
