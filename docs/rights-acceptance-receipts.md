# Scoped rights acceptance receipts

`ges.rights_acceptance.rights_accounting` validates accountable attestations. It does not establish legal truth, authenticate humans, grant a license, contact upstream authors, or publish content. A policy file is a separately approved trusted authority input; writing JSON with a human name is not approval. No real policy grant or acceptance receipt is supplied by this tranche.

Recovery accepts paired `--rights-acceptance RECEIPTS.json` and `--rights-acceptance-policy POLICY.json` inputs. A missing pair is rejected; no receipts leaves zero completed files and unknown acceptance/distribution conditions. All six locked sources and every artifact remain in the denominator. Published-page/body rights are not covered by these pinned-artifact receipts.

## Authority policy

The policy schema is `ges.rights-authority-policy.v1`. It needs an applicable external `approval_reference`, the exact complete `inventory_digest`, one approved `intended_use`, and the actual project `distribution_scope`. Roles are nonempty unique identity arrays: `authorized_reviewers`, `authorized_auditors`, `authorized_human_acceptors`, and `authorized_distribution_approvers`. Authority must be approved for that project use and distribution, not merely source reading. The adapter cannot prove the authenticity or adequacy of this external approval; the operator must establish it before supplying policy.

Inventory and finding digests use `ges.core.digest`: SHA256 over canonical JSON with sorted object keys and compact separators. Array order and all artifact/finding fields are retained. Source changes or new findings require renewed exact-scope evidence; absence of a finding is not proof of no exception.

## Per-artifact receipt

Schema: `ges.rights-acceptance-receipt.v1`. Fields:

- `artifact`: exactly `artifact_id`, `source`, `commit`, `path`, and `sha256`, matching the locked inventory.
- `inventory_digest`, `findings_digest`: complete current inventory and file-specific finding queue.
- `intended_use`: one of `REFERENCES_ONLY`, `INDEPENDENT_PARAPHRASE`, `LICENSED_COPY`, or `ADAPTATION`, matching policy exactly. These are use labels, not conclusions about applicable law.
- `distribution_scope`: the exact approved project bundle/release and audience description, matching policy. A private-reference approval does not authorize a public source-copy release.
- `obligations`: a nonempty unique list of explicit duties/restrictions for this use. An excluded component remains excluded; approval for references does not authorize artwork, text, trademarks, private material or adaptations by implication.
- `valid_until`: explicit timezone-bearing future validity limit. Changing it requires re-bound evidence. This is an acceptance validity limit, not an inferred license expiration.
- `reviewer`, `independent_auditor`, `human_acceptor`, `distribution_approver`: authorized identities. Reviewer, auditor and human acceptor must differ. Distribution approver cannot be the reviewer/auditor; an authorized human acceptor may also approve distribution.
- `evidence`: exactly four JSON file/digest references, keyed `file_rights_review`, `independent_exception_audit`, `human_acceptance`, and `distribution_approval`.

## Evidence documents

Each reference contains `path` (relative `evidence/*.json` path) and byte `sha256`. Paths escaping the evidence directory, symlinks, missing files, changed digests or files over 1 MB are rejected. Documents must be objects with schema `ges.rights-attestation.v1`, exact `kind`, the corresponding authorized `identity`, timezone-bearing `reviewed_at`, and `subject` containing exactly the seven receipt fields from `artifact` through `valid_until` listed above (excluding role/evidence fields). The document also needs:

- `decision`: `APPROVED_FOR_SPECIFIED_USE`.
- `file_specific_grant_and_components_reviewed`: literal `true`.
- `exceptions_and_restrictions_accounted_for`: literal `true`.
- `rationale`: substantive nonempty text documenting the accountable decision.

Reviewers must substantiate applicable grants and exceptions with file-specific analysis, including inherited expression, privacy, attribution, modification disclosures and restrictions as relevant. These booleans and prose are reviewer attestations, not machine verification of the legal analysis. An unresolved component cannot be silently bundled; a reviewed permitted use can explicitly exclude it.

Every evidence subject must equal the receipt subject, including all obligations. Evidence must postdate acquisition, not be future-dated, and remain within receipt validity. Order is file review → independent audit → human acceptance → distribution approval. Equal timestamps are allowed for one approved transaction. All referenced bytes are rechecked before returning accounting.

Partial valid receipts count only their exact artifact IDs. Both full-file acceptance and whole-inventory distribution conditions remain false until every inventoried artifact has a valid receipt. Recovery exposes approved use/scope alongside counts; even a scoped closed rights gate is not blanket permission or proof that publication occurred. All other gates are evaluated independently.

Synthetic tests demonstrate complete, partial and rejected receipt cases. They are not actual human decisions and must never be submitted as project clearance evidence.
