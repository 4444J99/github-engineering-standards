# Wave 20261009 correction — worker C publication lane (CORRECTION-01)

Role C (second writer), branch `codex/wave-publication-c-20261009`, starting
HEAD `a2b81ff848d0c4137f0df03baf09e9685473a016`. Exclusive write root:
`evidence/wave-20261009-correction-01/publication/`. Successor records carry the
`-CORRECTION-01` suffix. Predecessor records and the publication candidate are
byte-identical; this lane only ADDS files.

Status of every field in this lane: **remaining HOLD**. Nothing here grants
publication clearance; delivery status stays **Staged**; the frozen publication
gate (byte-identical `LICENSED_COPY` spans / byte-identical candidate bytes) is
unchanged.

## Inputs used (all committed, all in this checkout)

- `evidence/wave-20261009/publication/README.md` — lines 18–23: why the two
  fields stayed unresolved (JSON escapes preserve decoded wording, break the
  validator's raw-byte equality; encoding alone does not justify an `ADAPTATION`
  judgment).
- `evidence/wave-20261009/publication/primary-review.json` — the two
  `kind: null`, `UNRESOLVED_JSON_ENCODING` rows (spans, shas, rationales), plus
  the resolved title row used as a raw-identical control.
- `evidence/wave-20261009/publication/accounting-replay.json` + `replay.py` —
  prior replay method (frozen candidate register carries 0 use rows; 2,396
  outputs all `UNREVIEWED`). Re-read, not re-executed; no authenticated source
  cache is present in this checkout, so the replay's source-side assertions were
  out of scope here.
- `controls/review_queue.json` — pinned by the planning-freeze binding
  (sha256 `091b1afe…`); the actual output bytes for both held spans.
- `ges/publication_use.py` (lines 545–549) and
  `docs/publication-use-register.md` (use-row / byte-range contracts) — the
  committed validator and register rules the rows must satisfy.
- `evidence/publication-candidates/ges-v0.2-merged-f628db26-20261008/*` — nine
  candidate files, re-hashed for `candidate-integrity.json`;
  `review-priorities.json` used for the GES-OPS-008 cross-reference.
- Read-only planning freeze in the conductor checkout
  (`evidence/wave-20261009-correction-01/assignment.json`) — reference sha256
  values for the nine-file integrity comparison, and the C-lane bindings.

Not present at this HEAD and therefore not used: the wave omission/,
integration/ and audit/ files referenced by the conductor freeze (they live on
stage B's branch, not this one), and any authenticated upstream source cache.

## Method

1. Preflight (HEAD/status/remote/locks/processes) and execution-lease
   reacquisition; `identity.json` written first.
2. Byte forensics on `controls/review_queue.json` at the two frozen output
   spans: raw span bytes, escape counting, JSON-string decoding, sha256 of raw
   and decoded text vs the committed source-span sha256.
3. Classification-path analysis against the committed validator and register
   contract for all four `KINDS`.
4. Local re-hash of the nine candidate files vs the planning-freeze bindings.

## Per-field outcome

Both `GES-OPS-008-objective` and `GES-OPS-008-implementation-acceptance-0`
(**REMAINING HOLD**, successor records
`use-correction-ges-ops-008-objective-CORRECTION-01.json` and
`use-correction-ges-ops-008-implementation-acceptance-0-CORRECTION-01.json`):

What the correction establishes (new, byte-exact):

- Each output span is the interior of one JSON string literal; the ONLY
  difference from the source text is exactly two `\"` escapes around
  `prevent further usage` (raw 170 bytes vs decoded 168; +2 backslashes).
- Decoded span sha256 `5c22f1ab…` equals the committed source-span sha256
  (microsoft/ghqr `02b8996…`, `budgets.yaml` bytes 1897–2065) — verified
  locally against committed candidate bytes.
- Raw span sha256 `e429fb1a…` ≠ source sha — the predecessor's observation is
  reconfirmed.
- Structural finding: because the reused sentence contains ASCII double quotes,
  JSON syntax mandates escaping them; no candidate storing this text in JSON can
  ever satisfy the validator's raw-byte `LICENSED_COPY` identity. The hold is
  structural, not incidental.
- `INDEPENDENT_PARAPHRASE` is false (decoded text is identical);
  `REFERENCES_ONLY` is false (the expressive wording is present, decoded, in the
  output). `ADAPTATION` would pass the validator mechanically, but it is a
  substantive rights judgment that committed evidence does not establish —
  this worker neither invents it nor fabricates the approvals it would need.

Release therefore requires an authorized owner: an accountable `ADAPTATION`
decision (using these forensics as supporting evidence) or a policy/validator
amendment on JSON-escaping. Regenerating the candidate is a false path and is
recorded as such.

## Candidate integrity

`candidate-integrity.json`: **9 of 9 MATCH** against the read-only planning-freeze
bindings (sha256 and byte counts both agree for all nine files). Read-only check;
no clearance granted, candidate unmodified.

## Unresolved / out of scope

- The two fields' classification (above) — needs an authorized owner decision.
- The frozen validator replay (needs the authenticated source cache) — deferred
  to integration, along with the heavy/Governance suites, as directed.
- Wave omission/, integration/, audit/ files are not on this branch; the
  conductor's freeze shas were not re-verified here.
