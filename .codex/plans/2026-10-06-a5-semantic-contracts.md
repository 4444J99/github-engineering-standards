# A5 — Semantic contracts

Implement the five versioned semantic JSON Schemas, deterministic record IDs,
JSONL validation, and reserved extract/reconcile/audit command interfaces on an
independent branch from main. Use synthetic fixtures only.

Acceptance: schema round trips, missing/unknown fields, unsafe spans/paths,
stale identity, duplicate and empty ledgers, deterministic IDs, and unavailable
commands are covered; repository tests, validation, compilation and diff checks
pass. Push one reviewable PR. Human review and merged-main acceptance remain
pending until recorded. Corpus extraction, review authority, policy adoption,
and reconciliation machinery are outside A5.
