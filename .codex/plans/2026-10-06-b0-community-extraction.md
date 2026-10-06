# B0 — Community extraction

Status: authorized staging; HOLD. A0 remains Primary under the supplied roadmap.
One primary deliverable: deterministic semantic ledgers for all 22 pinned community artifacts.
Branch: feat/b0-community-extraction, stacked on A6 exact head 551e2650ec03e22ddb3b34627702bf51dfc620c4 (PR #478; includes A5).

## Immutable inputs

`evidence/semantics/b0/input-manifest.json` freezes all artifact IDs, commits,
Git blob identities, line denominators, snapshot and inventory digests, authored
annotation digest, and the A3 capsule identity. No refresh or upstream execution.
A4 charter inputs are referenced by exact commit and file digest; their approval remains pending.
In-scope IDs: the manifest's complete artifact_id list, and only the generated
occurrence/proposition IDs bound by receipt.json. Maximum 250 propositions; zero controls.

## Work

1. Read every full artifact; author source-local semantic ASTs preserving modality,
   conditions, examples, literal parameters, and differences across files.
2. Explicitly account for remaining source lines with reasoned nonclaim spans.
   Compile annotated spans rather than infer semantics with keyword matching.
3. Validate source bytes, inventory denominators, annotation identity, line accounting,
   schema and stable IDs; regenerate twice without overwriting; compare byte-for-byte.
4. Run unit/negative tests, full unittest discovery, ges validate, ges compile,
   diff check and applicable existing provenance/recovery checks.
5. Commit/push exact branch; prepare one stacked draft PR and exact-head validation receipt.

## Exclusions and residual

Exclude GHQR, Well-Architected, Docs, source refresh, linked external materials,
C0 reconciliation, control adoption, templates generated for consumers, rights
clearance, upstream submission, native operations and estate rollout.
License texts are reference-only supporting inputs with explicit engineering-nonclaim
dispositions; no license interpretation or redistribution grant is asserted by B0.
All generated records remain PROPOSED. residual.json names every pending proposition
and artifact/nonclaim review. Human approval, foundation acceptance, remote-head CI,
merge to main and merged-head verification remain in B0 and cannot spill into C0.
GO requires an empty in-scope residual ledger and the user's universal verification.
Checkout retained; no automatic continuation beyond this bounded implementation attempt.
