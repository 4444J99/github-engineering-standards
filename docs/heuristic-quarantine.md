# Legacy heuristic quarantine

The ordered keyword router and its 61,427 dispositions are preserved in the
original checkout under `.cache/quarantine/a1-legacy-semantic-review/`.
The tracked receipt is `evidence/a1-heuristic-quarantine.json`; the private
quarantine also contains its own receipt. Original paths are recorded there.

The result is `INVALIDATED_HEURISTIC_PROPOSAL_ONLY`. Its MAP, SPECIALIZE, and
DEFER labels do not establish semantic equivalence, conflict resolution,
review coverage, policy adoption, or certification. The identity
`automated:semantic-review-v0.2.0` is rejected by artifact accounting and claim
provenance even if a supplied policy lists it. PR #472's certification adapters
consume these same validators.

To recover an artifact, verify its SHA-256 against the tracked receipt and copy
the quarantined relative path to a new scratch location. Preservation is local;
the raw script and output have not been added to Git or published remotely.

The containment utility refuses existing quarantine directories and verifies
both copies before removing active originals. A1 performed no source refresh
or semantic decisions. Its independent branch is based on main `1dab672`.
