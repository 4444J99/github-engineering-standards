# A4 review correction

Address PR #476 review without adopting or approving any charter:

1. Recompute span hashes using the existing ledger convention; rename the whole
   source digest to `content_sha256`.
2. Add atapas roadmap, deployment and support locators.
3. Share the existing pinned-span verifier with a read-only charter replay command.
4. Test committed locator coverage and canonical replay, including rejection of
   the original trailing-newline error; replay real pinned bytes separately.
5. Run full tests, validate, compile and diff checks, then push to the same PR.

Retain this worktree for ongoing review. Owner approval and A3 acceptance remain
pending; no merge or acceptance is authorized by the request-changes review.
