# A1 — Heuristic containment

Independent branch from main; PR #472 review may proceed concurrently.

Preserve the two untracked legacy artifacts with byte counts and SHA-256 hashes
in ignored quarantine, remove their active paths after preservation verification,
and reject their invalidated reviewer identity even if a policy lists it.

Acceptance: digest-checked custody receipt, negative provenance/accounting tests,
full tests, catalog validation, deterministic compile and diff checks.

No semantic decisions, control changes, source refresh, or native enforcement.
