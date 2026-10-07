# Actions security source review and capture hardening

Five previously unreviewed pinned GitHub Docs articles were read in full:
GITHUB_TOKEN, secrets, OpenID Connect, script injections and compromised runners.
The batch adds 70 authored claims across 446 lines. Eight literal dependencies,
14 selected variable bindings and two digest-verified images were inspected;
only the five original articles receive new artifact receipt credit.

The [primary review](../evidence/actions-security-primary-review.json),
[dependency observations](../evidence/actions-security-review-inputs.json) and
[independent audit](../evidence/actions-security-independent-review.json) preserve
exact source spans and qualifications. Corrections restore recommendation modality,
limit OIDC claims to their actual source support, preserve platform conditions and
conditional PAT advice, and distinguish write-capable workflow editors from fork
jobs without manufacturing a conflict. The injected-title image and OIDC diagram
are illustrative dependencies, not execution or cloud-trust evidence.

The [combined reconciliation](../evidence/actions-security-reconciliation.json)
contains 303 receipts: 233 historical decisions rebound to the enlarged known-claim
input plus 70 new decisions (52 partial supporting MAPs and 18 references), subject to
the linked independent audit. Previous decisions retain their
original reviewers and review times; rebinding grants no new review credit. Partial
supporting MAPs cover specific facets of existing draft controls, not whole-control
completion or policy adoption. The prior squash-metadata ambiguity remains open.

`ges collect` now omits known credential-bearing response properties before retaining
normal, nested, paginated and enveloped data. It drops object properties whose keys
contain the active request credential, redacts literal echoes in strings and file
content decoded by the collector, and retains omission counts after partial page
failures. It preserves permission metadata, alert states, revision identities and
coverage flags. The upstream blob SHA identifies the original file even when
captured content is redacted. Synthetic adversarial fixtures verify serialized
output and retained assessment failures. Unknown fields, transformed secrets and
arbitrary source content remain outside this bounded guarantee; snapshots stay
private.

## Acceptance accounting

Reviewed artifact receipts: 3,575 → 3,580 of 13,657.
Known source claims: 61,695 → 61,765. Reviewed reconciliation: 233 → 303.
The substantive GitHub Docs unreviewed remainder: 6,335 → 6,330 of 9,116.
All 95 controls remain draft with zero accepted; all nine legacy gates remain open.
No published-page assurance, rights clearance, native acceptance or estate rollout
is credited. Frozen #453 is untouched.

Reproduce the current report with the existing private caches:

```sh
python3 -m ges.recovery --sources /path/to/cache/sources --corpus /path/to/cache/corpus --reviews evidence/source-reviews --review-policy evidence/source-review-policy.json --rendered-directory /path/to/cache/rendered-docs --claim-reconciliation evidence/actions-security-reconciliation.json --claim-reconciliation-policy evidence/actions-security-reconciliation-policy.json --output evidence/recovery-status.json
```

Historical batch documents retain their original input digests and counts. Use the
combined inputs above for current accounting. A fresh private pilot availability
[observation](https://github.com/4444J99/ges-native-enforcement-pilot/blob/ab08f2e67922db1c3b093e36c3d7f90021ac75c4/evidence/actions-availability-20261007.json)
is published at immutable private commit `ab08f2e`; it executed zero steps. The pilot
ruleset remains Disabled and the positive/negative native matrix remains unproved.
No billing settings, substitute runner, public visibility or estate settings were
changed.
