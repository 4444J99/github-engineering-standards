# Shared warning-only workflow

Owner: @4444J99; implementation and finding disposition: Codex pilot lane.
Scope: the already authorized bounded pilot. This source addition does not onboard
a consumer, alter required checks, grant paid capacity or expand the portfolio.

## Runtime contract

`.github/workflows/warning-pilot.yml` exposes only `workflow_call` with a required
`expected-checks` JSON array. The caller must supply reviewed literal check names
from its existing CI contract and pin the reusable workflow to its reviewed full
commit SHA. No consumer caller is activated in this change. The only runtime
inspector is the merged CLI at immutable commit
`a5cdf48e9f255cb407a1ae69be62397f1151847d`; wrapper code lives in the separately
pinned reusable-workflow file. There is no release tag or mutable runtime branch.

The workflow reads the caller's PR head, or its exact event SHA for push/manual
calls. It checks the checkout SHA and reads Git blobs as data. Consumer blobs are fetched during authenticated checkout so subsequent private
repository reads do not require lazy-fetch credentials. No consumer scripts, local actions,
dependencies, build hooks or Python modules execute. Inspector dependencies come
only from the pinned toolkit's approved PyYAML 6.0.3 dependency, restricted to the
SHA-256-locked CPython 3.12 Linux x86_64 wheel from PyPI. All actions use full SHAs, credentials are not
persisted, submodules/LFS are off, and the token has only `contents: read` and `actions: read` (for exact run metadata).
Unsupported events, including `pull_request_target` and `workflow_run`, fail
inspection visibly. No inherited secrets or publication/deployment operation is
requested. The workflow never changes settings or existing job identities.

Tree enumeration streams with a 1 MiB output ceiling and stops at the file cap.
Local action/reusable-workflow references conservatively make dependency resolution
incomplete; missing manifests cannot become false warnings.
Inspection is bounded to 128 direct workflow files, 1 MiB per blob, 8 MiB of decoded
source input, 15 seconds per Git command, and a three-minute job deadline.
Skipped oversized/binary files and count/size truncation mark the inventory
incomplete, preventing positive configuration findings. These bounds do not claim
to cap Git's network/object-store transfer before an object size is known. Symlinks
remain manual-review findings. Empty inventories, malformed YAML, missing read-only
declarations and mutable actions remain visible warnings/unknowns.

## Honest result semantics

Configuration observations and warnings complete with advisory exit zero. Input,
dependency, checkout, inspection and artifact failures remain failed job results;
there is no `continue-on-error` or failure suppression. Consumers must keep this
new job outside their required contexts. Existing required checks remain intact.

The caller's declared check list is hashed for invocation binding, but it is not an
independently authenticated execution policy. The wrapper accepts no execution
receipt and always reports execution `NOT_VERIFIABLE`. It cannot certify its own
job, the caller's tests, complete workflow validity, privilege correctness,
publication artifacts, checker protection, restoration or compliance. The report
retains the CLI's explicit `not_evaluated` list.

## Evidence and acceptance

Only `plan.json`, `report.json` and `manifest.json` upload into the caller
repository's Actions artifact custody. Raw workflow text and the snapshot are not
uploaded. The manifest binds repository ID, exact revision, inspector commit,
run/attempt identity, source fork repository name/ID separately from target identity,
invoked wrapper SHA/ref read from GitHub's run metadata, dependency wheel digest, observed file count, inventory completeness, SHA-256/byte
length of the retained plan/report, access scope and a conservative 30-day expiry.
Retrieval and restoration start explicitly false. No attestation is fabricated.

Before consumer acceptance, independently download the artifact, verify the
manifest bindings and content digests, reconstruct the snapshot from the named
source revision, and reproduce the report using the recorded plan and inspector.
Record retrieval/restoration results in that consumer's evidence owner. Archive
reviewed evidence before expiry if acceptance still relies on it; an expired
artifact invalidates availability claims. Keep private reports in private custody.

The manifest's duration covers inspection only. Measure whole hosted job time,
including setup and artifact upload, independently against the two-minute added
governance target. Local fixture timing is not hosted overhead. Observe seven days
and two representative changes only after actual onboarding; do not manufacture
changes or extend the window automatically.

## Verification and rollback

The tests execute the actual inline producer against isolated Git repositories,
including consumer-side code that must not execute. Positive and adversarial
fixtures test the resulting report, inventory completeness and retained hashes,
alongside structural checks for permissions, immutable dependencies and narrow
artifact boundaries. Actionlint validates the workflow independently. Hosted
execution, artifact retrieval and rollback are not claimed by local passes.

The next consumer integration uses one isolated PR at a time and retains original
protection readbacks. Revert that caller PR to remove the advisory invocation or
restore its previous reviewed SHA, then verify original checks/protections and
retain the evidence. Rehearse this before accepting the consumer. Stop further
onboarding on false green, privilege/publication violations, check disruption or
repeated budget overruns. Required-check activation and expansion beyond the three
approved consumers require separate authorization.

Platform contract references: [reusable workflow context and permissions](https://docs.github.com/en/actions/reference/workflows-and-actions/reusing-workflow-configurations),
[immutable workflow references](https://docs.github.com/en/actions/how-tos/reuse-automations/reuse-workflows),
and [workflow permissions](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax).
