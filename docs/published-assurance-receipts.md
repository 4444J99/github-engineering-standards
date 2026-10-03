# Published assurance receipts

`ges.published_assurance` validates digest-bound, independently reviewed page
assurance attestations. It does not infer semantic truth from file existence,
reference extraction, successful acquisition, a title or a basename match.
The accountable reviewers own the truth of their recorded judgments.

Recovery accepts optional paired `--published-assurance RECEIPTS.json` and
`--published-assurance-policy POLICY.json` inputs. Without them, completion is
zero and the render/version prerequisite stays unknown. Invalid supplied receipts
fail rather than count. All pages in the original ledger remain the denominator.
Neither this implementation nor its synthetic tests certify any real page.

The authority policy must be separately approved, with schema
`ges.published-assurance-policy.v1`, a durable `approval_reference`, and nonempty
unique lists `authorized_claim_authors`, `authorized_certifiers` and
`authorized_omission_auditors`. Policies are trusted authority inputs: a string
in an agent-authored file is not a human approval or a cryptographic signature.
The existing source-disposition policy does not grant these certification roles.
This tranche creates no real policy, approval or assurance receipt.

Each receipt has schema `ges.published-assurance-receipt.v1` and binds:

- `page_id`, `path`, `version` and the exact `ledger_sha256`;
- the durable acquired `body_sha256` and a post-acquisition `reviewed_at`;
- `source_identity` with exactly `artifact_id`, `source`, `commit`, `path` and
  `sha256`, matching the locked GitHub Docs artifact inventory and the page's
  declared source mapping;
- distinct `claim_author`, `reviewer` and `independent_auditor` identities in
  their approved policy roles;
- nonempty `claims` references, each with a relative evidence JSON `path` and
  `sha256`, to authored `ges.published-reference-claims.v1` documents;
- an `evidence` object with exactly the five kinds below.

| Evidence kind | Responsible role | Required judgment scope |
|---|---|---|
| `source_identity` | Certifier | Published body/deployment relation to the exact locked artifact; a path match alone is insufficient. |
| `version_rendering` | Certifier | Applicable version/product/platform branches and rendered content. |
| `dependency_resolution` | Certifier | Required includes, variables, linked interpretive material and assets, with no unresolved dependency. |
| `claim_mapping` | Certifier | Every identified atomic claim has a justified mapping; accepted policy remains separate. |
| `independent_omission_audit` | Independent auditor | Full body-to-claim audit, including noncandidate material, and fidelity of the exact referenced claim set. |

Each evidence reference has relative `path` under `evidence/` and `sha256`.
Absolute/parent traversal paths, symlinks, non-JSON targets and evidence over
1 MB are rejected. Its document uses schema
`ges.published-assurance-evidence.v1`, exact `kind`, page/ledger/body/source
identity, exact `claims` reference array, the required `reviewer`, and a
`reviewed_at` between acquisition and certificate time. It also needs
`outcome: "PASS"`, nonempty `method`, nonempty unique string `observations`, and
`unresolved: []`. These are scoped accountable attestations, not a generic
Boolean that overrides a missing gate predicate.

Claim files are independently subjected to the existing published claim
provenance validator: body/ledger identities, span bounds and hashes, author,
timestamps and reference-only/nonadoption flags must all validate. One validation
pass covers the deduplicated document set; it is not run once per page. An audit
of one claim-file digest cannot be reused for an altered claim file.
The final provenance-read digests must also equal the advertised references,
rejecting a replacement between the initial digest check and provenance read.
This is not a guarantee against every malicious concurrent filesystem race;
run against an immutable evidence snapshot for release acceptance.

The adapter currently accepts locked-source mappings only. The fourteen
published drift instances remain unresolved, not excluded or assigned invented
matches. Supplement/deployment identity and its authorized review pathway still
require implementation and evidence; neither the locked pin nor the published
denominator is changed here.

The resulting count is *validated authorized assurance attestations*, not an
automatic semantic-truth certificate. It does not certify rights, native
behavior, accepted policy, source-wide omission or estate rollout. Recovery
still requires acquisition of every body and reconciliation of every source
path before the published gate can close. Other gates remain independent.

For standalone read-only validation:

```sh
python -m ges.published_assurance --ledger .cache/corpus/published-page-ledger.json --cache .cache/rendered-docs --artifacts .cache/corpus/artifacts.jsonl --receipts RECEIPTS.json --policy POLICY.json
```

No sample populated authority or PASS receipt is shipped: actual approval and
review evidence must precede their creation.
