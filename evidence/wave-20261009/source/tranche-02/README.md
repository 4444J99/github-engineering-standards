# B primary review tranche 02

State: Staged primary proposals awaiting D omission review, A reconciliation and
E audit. This is an additive packet; the first packet at `53d274be18bb5293685d14628b6d73b4a9476593`
is unchanged.

Detailed review covers WA-APPSEC-019 through WA-APPSEC-059: 41 authored claims
and their 41 corresponding structured occurrences, source lines 47–115. These
are two representations, not 82 independent propositions. Together with the first
18 primary reviews, 59 of the assigned 162 claims now have B primary proposals.
The remaining 103 are listed explicitly in `residuals.json`. No new reconciliation
receipt is supplied and no semantic mapping is counted as validated.

The source requires distinctions missing from existing broad controls: actual
compliance versus identifying obligations; comprehensive critical-action logging
versus retaining available logs; tamper protection, secure storage and RBAC;
encryption and key management; recurring drills and threat analysis; actual use
of internal and external penetration testers; patch-management and asset-inventory
scope; continuous real-time threat monitoring; all-employee awareness programs;
phishing simulations; and establishment and support of security-champions programs.

Twenty-six original paraphrases narrow or weaken explicit source fields. Each is
identified with its actual claim subject and an authored explanation in
`primary-review.json`. Some add sensible local authorization conditions; those
conditions remain local safeguards and do not replace source recurrence, actors,
actions, objects or outcomes. These are proposed fidelity findings for D review;
the historical claims are preserved. Claimed source scope does not depend on
classifying an obligation as reference merely because no canonical objective exists.

All 41 proposed decisions retain an exact existing quarantined proposal identity
(GES-OPS-055 through GES-OPS-095, revision 1), with related catalog references
where useful. These are proposed SPECIALIZE dispositions, including cases that
need a new objective through the existing proposal, not claims that specialization
has been implemented or adopted. Existing proposals' blank source-hash fields,
unspecified applicability, generic manual verification and quarantine status remain
unresolved; the review packet separately binds the authenticated source spans.

The existing semantic-decision schema is used. `proposition_ids` refers to existing
claim IDs and does not assert newly created semantic propositions. Empty
`preserved_fields` and `lost_fields` arrays make no field-completeness assertion:
actual distinctions and fidelity defects are individually authored in the primary
review and draft disposition rationale. No independent reviewer identities,
approvals or timestamps are supplied. `draft-dispositions.json` is a projection
for A, not a completed claim-reconciliation receipt.

Context read: application-security design principles lines 59–181, and the
threat-model recommendation lines 1–230. The latter is expressly scoped to source
integrity; it does not exhaust the broader application-security checklist. Its
remaining threat analysis, diagrams, linked frameworks and platform statements
are not certified by this packet. Other dependencies are outside this tranche's
review boundary. No upstream code was executed or source resynced.

Reproduce from the repository root:

```sh
env PYTHONPATH=. python evidence/wave-20261009/source/tranche-02/build_packet.py /PATH/TO/AUTHENTICATED/.cache
```

The builder serializes individually authored judgments. It binds the original
packet crosswalk, current assignment, exact catalog/proposal inputs, retained
compressed snapshot and source/context artifact identities. It validates all 41
records using `ges.semantics.validate_record`, exit 0. Structural validity does
not supply semantic approval. Full integration validation belongs to A.

No human approval, distribution permission, publication clearance, owner policy
adoption, operational deployment or whole-source completeness is asserted.
The worker checkout is retained for review and integration.
