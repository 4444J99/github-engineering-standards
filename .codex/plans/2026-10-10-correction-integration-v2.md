# Correction integration and pinned-source reread

Objective: produce one custody-bound exact head for draft PR #496 that contains
the A, B, C, D, and E correction-wave evidence, then separately reread the five
assigned claim spans from the authenticated pinned
`github/github-well-architected` cache.

Constraints:

- Preserve every predecessor and worker commit byte-for-byte.
- Keep the two publication fields on HOLD.
- Do not manufacture a reconciliation receipt, rights determination, policy
  adoption, human approval, merge, or `Verified` status.
- Do not run upstream code or publish raw cache files.
- Treat the source reread as a bounded fidelity check only. It may retire only
  the `SOURCE_BYTES_NOT_REREAD_HERE` limitation when the authenticated cache
  identity, full content digest, selected line bytes, and correction statements
  all match.
- Keep cumulative accounting unknown and do not run the heavy tranche merely as
  part of this integration.

## Task 1: Integrate retained worker evidence

1. Re-fetch the remote and verify A/B/C/D/E exact heads and clean retained
   checkouts.
2. Demonstrate that B/C/D/E are not ancestors of the A integration head.
3. Cherry-pick the four additions-only worker commits in execution order:
   B `c034c82`, C `a29214d`, D `4e137f6`, E `2dad9e4`.
4. Verify that the resulting head contains each worker commit and every bound
   evidence root while retaining `Staged`/HOLD language.

## Task 2: Perform the pinned-source byte reread

1. Read only the retained authenticated cache entry for
   `content/library/application-security/checklist.md` at
   `a30275bc2d7eb860e612f93cbc1f26d0ff20c0c7`.
2. Verify the full content SHA-256 against the inventory/cache record.
3. Re-read exact lines 21, 27, 31, 41, and 42 and bind each line's UTF-8 bytes,
   SHA-256, predecessor, and successor statement.
4. Add a deterministic checker and receipt under
   `evidence/wave-20261009-correction-01/source-reread/`.
5. Retain all remaining mapping, decision, authority, enforcement, cadence,
   publication, approval, and verification holds.

## Task 3: Verify and update PR #496

1. Run the bounded integration/reread checker and `git diff --check`.
2. Confirm the exact integration head contains A+B+C+D+E plus the reread
   evidence.
3. Push the custody-bound branch and update draft PR #496 to that exact branch.
4. Re-read the live PR head and body; correct the stale integration-head field
   while preserving draft/Staged/HOLD status.
5. Record exact local/remote/PR head equality. Do not merge.

Completion requires one live PR head containing all five role evidence sets and
the independently generated pinned-source reread receipt. It remains `Staged`.
