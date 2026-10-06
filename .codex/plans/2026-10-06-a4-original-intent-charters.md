# A4: original-source authority charters

Scope: six founding-source charters and an original-intent matrix, independently
prepared while PR #472 is reviewed. No semantic extraction, policy adoption,
upstream submission, source refresh or estate rollout.

1. Inspect pinned root documentation and source-role evidence.
2. Write six charters separating declared intention from GES interpretation.
3. Record exact commit/path/line provenance and verify against cached source bytes.
4. Run toolkit tests, validation, compilation and whitespace checks.
5. Commit, push and open a separate review PR. Human approval remains pending;
   revalidate pins against the accepted A3 capsule before baseline acceptance.

Local verification: all six source identities and cited line bounds checked against
the lock and pinned cached text; file and span SHA-256 digests recorded in
`evidence/a4-source-charters.json`. 340 unittest tests passed; `ges validate`
accepted 95 controls; `ges compile` and `git diff --check` passed. Compilation
introduced no generated-file changes. Human approval is not claimed.
