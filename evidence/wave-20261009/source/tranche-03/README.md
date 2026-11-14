# B primary review tranche 03

State: Staged primary proposals awaiting D omission review, A reconciliation and
E audit. The first two packets are unchanged at `53d274be18bb5293685d14628b6d73b4a9476593`
and `3d4e49a6c4fec45332366394a3a9b4b7c5353509` respectively.

This tranche covers WA-APPSEC-060 through WA-APPSEC-162: 103 claims and their
103 corresponding structured occurrences, source lines 118–291. These are two
representations, not 206 independent propositions. All 162 originally assigned
claims and occurrences now have bounded B primary proposals across three packets.
That is primary-review coverage only. It supplies zero completed reconciliation
receipts and does not establish source omission completeness or independent audit
coverage. The earlier packets retain their own historical residual denominators.

`judgments.txt` contains 103 individually authored judgments against the original
checklist and draft control objectives. These preserve the difference between
assessment and implementation; all-team and all-user coverage; recurring review,
actual updates and timely response; Cloud/Server deployment distinctions; full
backup and recovery; repository segmentation and the justified-monolith alternative;
microservice suitability versus universal adoption; independent scaling and
deployment; efficient and secure integrations; current storage and infrastructure
use; documentation accessibility; and log integrity and retention.

Sixty-one original claim paraphrases have explicit fidelity findings. Examples
include evaluating SSO in place of implementing it, monitoring API anomalies
replaced by investigation, replication implementation replaced by assessment,
and loss of independent service scaling. These remain proposed findings for D.
The original source claims, occurrence ledger and quarantined proposals are intact.
Repeated modularity and dependency-documentation passages remain distinct source
occurrences pending a scope-aware duplicate decision.

All 103 proposals use SPECIALIZE projections referencing exact existing
GES-OPS-096 through GES-OPS-198 at revision 1. Related catalog controls are
identified only where their actual objective supplies supporting scope; many
items need a new objective through the existing proposal. This does not claim that
specialization is implemented, canonical coverage is sufficient, or a quarantined
proposal is operational. Empty applicability, blank proposal source-hash fields,
generic manual evaluator bindings and quarantine status remain unresolved.

The general awareness items 060–065 retain their general scope. The subsequent
items remain under the source's Additional Checklist Items for GitHub Enterprise
Deployments heading, including its architecture, modularity and observability
subsections. The Enterprise Server backup heading and explicit on-premises backup
wording remain narrower than a universal Cloud obligation. Deployment-specific
feature availability requires later target interpretation; it is not assumed
from the frozen checklist or an outbound URL.

The existing semantic-decision schema validates all proposed records. Its
`proposition_ids` are the existing claim IDs, not manufactured semantic-proposition
identities. Empty `preserved_fields`/`lost_fields` arrays assert no completeness;
individual source meanings and fidelity defects appear in `primary-review.json`.
No reconciler, independent-reviewer approval or audit timestamps are fabricated.
`draft-dispositions.json` is a receipt-compatible projection for A, not a receipt.

The checklist was inspected directly from the authenticated frozen source cache.
Additional context is explicitly bounded in `input-bindings.json`: application
security navigation/overview, awareness principles, and initial architecture
principles. Other architecture text visible during inspection is not claimed as
complete dependency review. No source sync, upstream code execution, source-text
export, external platform certification or live native execution occurred.

Reproduce from the repository root:

```sh
env PYTHONPATH=. python evidence/wave-20261009/source/tranche-03/build_packet.py /PATH/TO/AUTHENTICATED/.cache
```

Observed builder result: all 103 decisions passed `ges.semantics.validate_record`,
exit 0. All exact subjects/occurrence associations reuse the digest-bound original
crosswalk, preserving claim-document hashes. Full integration validation and any
newly bound reconciliation receipts belong to A after D and E perform their roles.
No owner acceptance, human approval, publication clearance, policy adoption,
native enforcement or whole-corpus completion is asserted. Checkout retained.
