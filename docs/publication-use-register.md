# Exact candidate publication-use accounting

`ges.publication_use.publication_accounting` implements the actual-use publication
boundary adopted for GES v0.2. It checks a concrete candidate directory, its
complete file inventory, the registered uses of upstream expression, and
separately authorized attestations for those exact inputs. It does not publish
anything, grant rights, authenticate human identities, or establish legal truth.
The earlier `ges.rights_acceptance.rights_accounting` function and its whole-source
inventory denominator retain their original meaning and implementation.

The structural contracts are in
[`schemas/publication-use.v1.json`](../schemas/publication-use.v1.json).
The executable validator adds file membership, byte/span hashing, provenance,
authority, independence, time order, and completeness checks that JSON Schema
alone cannot establish.

## Release boundary and independent authority

A manifest must declare `release_scope` as `GES_V0_2` or `BOUNDED_PACKAGE`.
Clearing a bounded patch or control package does not clear the complete GES v0.2
release. The candidate ID, candidate Git revision, audience/distribution scope,
release boundary, complete output bytes, register, full source inventory, source
pins, and used-source evidence all enter the reviewed subject. A change to any
of those inputs requires newly bound evidence.

The candidate directory is a dedicated staging directory containing **every file
intended for that candidate**. The manifest, register, receipts and authority
policy belong outside it. The observer walks the entire directory, including
normally hidden files, and rejects missing or extra files, mismatched sizes or
digests, duplicate paths, noncanonical relative paths, symlinks and nonregular
files. Empty directories have no distributed file bytes and are not counted.
Changing output bytes during validation is detected by a second inventory pass.
Git revision labels identify a candidate; they do not themselves prove how the
candidate was built or whether omitted repository content should be released.

The manifest cannot attest to its own completeness. Before accepting a candidate,
the caller must obtain a **separately approved authority policy** from a trusted,
access-controlled approval process. That policy binds the exact input digests
and names the roles authorized for that subject. A reviewer and independent
omission auditor must assess the intended output inventory and every upstream
use, followed by authorized human acceptance and distribution approval. This
independent process is responsible for detecting expression omitted from an
otherwise internally consistent register and for establishing which repository
outputs constitute the intended release.

An attacker who replaces both candidate data and its supposedly trusted policy
has replaced the trust input. A JSON file containing a person's name cannot
authenticate that person. The validator therefore always reports
`authority_authenticity_automatically_certified: false`. It rejects unauthorized
identities, missing approval references, unsupported approval objects, invalidated
review identities, mismatched subjects and altered proof bytes; it does not
pretend to cryptographically verify the external approval process. No real
authority grant, source-use classification, human approval or publication
clearance is supplied by this implementation.

## Prepare an honest unreviewed candidate

```sh
python -m ges.publication_use prepare-draft \
  --output-root .cache/publication/candidate \
  --draft-directory .cache/publication/review-inputs \
  --candidate-id ges-v0.2-candidate-01 \
  --candidate-revision EXACT_40_CHARACTER_COMMIT_SHA \
  --distribution-scope 'Proposed GES v0.2 public source release' \
  --release-scope GES_V0_2
```

This command writes four new files: `manifest.json`, `register.json`, empty
`receipts.json` (`[]`) and empty `policy.json` (`{}`). It refuses to overwrite an
existing draft directory. It does not classify existing source material as
original, independent paraphrase or licensed content. Each observed output starts
with the explicit `UNREVIEWED` disposition and a rationale; missing judgments
remain visible through `unreviewed_output_count` and diagnostics. No complete
inventory receipt is accepted while any output is `UNREVIEWED`.

The equivalent Python helper is:

```python
from ges.publication_use import prepare_draft

draft = prepare_draft(
    output_root, candidate_id, candidate_revision, distribution_scope,
    release_scope="GES_V0_2",
)
```

The helper returns `manifest`, `register`, `receipts`, and `policy` objects. Its
default release scope is `BOUNDED_PACKAGE`; callers must explicitly identify a
full GES v0.2 candidate.

## Output manifest and use register

The manifest schema is `ges.publication-output-manifest.v1`. It contains the
candidate identity, exact 40-character Git revision, distribution and release
scopes, timezone-bearing `prepared_at`, and a nonempty `outputs` array. Every
output has its canonical relative `path`, raw-byte SHA256, and integer
`size_bytes`. The observer compares the sorted path/byte/size inventory with the
complete actual directory.

The register schema is `ges.publication-use-register.v1`. It repeats the
candidate ID, binds the complete manifest with `manifest_digest`, records its
preparation time, and contains three arrays:

| Field | Required accounting |
|---|---|
| `outputs` | Exactly one disposition for every candidate output: `UNREVIEWED`, `USES_RECORDED`, or `NO_UPSTREAM_EXPRESSION`; exact associated `use_ids`; and a rationale. |
| `uses` | Every currently identified upstream use, preserving its unique ID, source identity, output location, use classification, attributable expression and rationale. |
| `source_evidence` | Exactly one durable evidence reference for each source artifact used by those rows; no foreign or duplicate source references. |

Known use rows remain attached to their outputs even while the output's complete
classification remains `UNREVIEWED`. Removing a use from a disposition without
removing the row is rejected. Removing both changes the register digest and
invalidates the separately approved policy and receipts. The independent
omission review is still required to assess whether all actual uses were found.

Each use row includes:

| Field | Contract |
|---|---|
| `use_id` | Stable nonempty unique identity within the exact register. |
| `kind` | `REFERENCES_ONLY`, `INDEPENDENT_PARAPHRASE`, `LICENSED_COPY`, or `ADAPTATION`. |
| `source` | Exact `artifact_id`, `source`, pinned `commit`, `path`, and `sha256`, matching the supplied artifact inventory and source lock. |
| `source_range` | `null` for reference-only locators; otherwise the exact source byte range and its digest. |
| `output_path`, `output_range` | An inventoried output and nonempty byte span identifying that precise use. |
| `attributions` | Array of actual notice/credit spans in inventoried output files; these byte references are checked, not merely asserted to exist. |
| `rationale` | Accountable explanation of the classification. Its correctness is reviewed, not inferred from nonempty prose. |

Byte ranges have zero-based inclusive `start_byte`, exclusive `end_byte`, and
`sha256` over that exact slice. They may refer to text or binary data. Each
`LICENSED_COPY` source span must be byte-identical to its output span; a changed
expression requires review under its actual use classification. Contradictory
classifications for overlapping output spans and duplicate source/output uses
under different IDs are rejected. A separate attribution entry has `output_path`
and `output_range` with the same byte contract.

Used-source evidence supports `RAW` local files and the existing
`SNAPSHOT_TEXT` cache (`owner__repo.text.jsonl.gz`). Its fields are `artifact_id`,
`format`, relative `path`, and the evidence file's raw-byte `sha256`. Raw source
bytes must match the pinned source artifact digest. Snapshot text is matched by
source, commit and path; its UTF-8 content bytes must match that artifact digest.
Missing, duplicate, changed, escaping or symlinked source evidence is rejected.
All referenced evidence files are checked again before returning accounting.
Unused corpus artifacts remain in the bound provenance inventory; they do not
acquire a requirement for individual publication grants merely by being cited
elsewhere in the corpus.

## Authority policy and approval receipts

The `ges.publication-use-authority-policy.v1` policy has an external
`approval_reference`, exact `subject`, timezone-bearing `issued_at` and
`valid_until`, and nonempty unique authority lists:

- `authorized_inventory_reviewers`
- `authorized_use_reviewers`
- `authorized_independent_auditors`
- `authorized_human_acceptors`
- `authorized_distribution_approvers`

The complete subject is returned by unapproved accounting after the candidate's
structural and byte validation. It includes `manifest_digest`, `register_digest`,
`output_inventory_digest`, `inventory_digest`, `pins_digest`, and
`source_evidence_digest`, plus the four candidate/scope fields. JSON digests use
`ges.core.digest`: sorted object keys, compact separators, and array order
preserved. Output inventories are sorted by path. File and span SHA256 values
hash their actual bytes.

Every receipt uses schema `ges.publication-use-receipt.v1`, the exact subject,
explicit future `valid_until` within policy validity, nonempty `obligations`,
four authorized role identities, and digest-bound evidence references. Reviewer,
independent auditor and human acceptor must differ. The distribution approver
cannot be the reviewer or auditor; an independently authorized human acceptor
may also approve distribution.

Two receipt types have distinct responsibilities:

| Receipt kind | Required scope and evidence |
|---|---|
| `OUTPUT_INVENTORY` | One complete candidate inventory. Its disposition is `REGISTER_COMPLETE` for a nonempty use register or `NO_UPSTREAM_EXPRESSION` for an explicitly reviewed zero-use candidate. Evidence kinds: `inventory_review`, `independent_omission_audit`, `human_acceptance`, `distribution_approval`. |
| `EXPRESSION_USE` | One particular `LICENSED_COPY` or `ADAPTATION` use ID, its exact expression, obligations and attribution decision. Evidence kinds: `expression_rights_review`, `independent_exception_audit`, `human_acceptance`, `distribution_approval`. |

Reference-only and independently paraphrased rows require the complete inventory
and classification review but **no per-source expression grant**. The classification
review is an accountable judgment about the actual output; the program does not
infer independent creation from the label. Per-use expression receipts for these
rows are rejected so legacy whole-corpus grant accounting cannot be substituted
for the actual-use boundary.

Each expression-use receipt also declares `attribution_disposition` as
`REQUIRED_PROVIDED` or `NOT_REQUIRED_WITH_REASON`, with an explicit
`attribution_rationale`. Required attribution must reference actual candidate
bytes. The latter decision requires an authorized exact-use judgment; the program
does not assume that every source has the same attribution obligations.

Evidence paths follow the existing relative `evidence/*.json` contract, include
the exact raw-byte digest and stay within its 1 MB size limit. Each
`ges.publication-use-attestation.v1` document binds the evidence kind, authorized
identity, exact receipt subject, `reviewed_at`, `APPROVED_FOR_SPECIFIED_USE`
decision, nonempty rationale and an empty unresolved-findings list. All assurance
flags must be literal booleans with the expected values. Inventory attestations
address the complete output inventory, complete use inventory, reviewed
classifications and, where applicable, explicit absence of upstream expression.
Expression attestations address the exact expression/grant, restrictions, and
attribution. Evidence must follow preparation, used-source acquisition and policy
issuance; review → independent audit → human acceptance → distribution approval
must be chronological and within the receipt's validity.

## Run accounting and interpret it

```sh
python -m ges.publication_use \
  --manifest .cache/publication/review-inputs/manifest.json \
  --register .cache/publication/review-inputs/register.json \
  --receipts .cache/publication/review-inputs/receipts.json \
  --policy .cache/publication/review-inputs/policy.json \
  --artifacts .cache/corpus/artifacts.jsonl \
  --output-root .cache/publication/candidate \
  --source-root .cache/sources
```

The supported function signature is:

```python
publication_accounting(
    manifest, register, receipts, policy, artifacts, pins,
    output_root=output_root, source_root=source_root, evidence_root=evidence_root,
)
```

The output schema is `ges.publication-use-accounting.v1`. It reports actual
output count, unreviewed outputs, use counts by kind, the complete declared-use
denominator, validated use IDs, validated expression-receipt count, all input
digests, explicit release scope, diagnostics and these separate conditions:

| Condition | Meaning |
|---|---|
| `complete_output_inventory` | The declared file set exactly matches observed candidate bytes. It does not establish that the selected candidate includes every intended release artifact. |
| `use_register_complete` | Authorized inventory review and independent omission review, human acceptance and distribution evidence validate the complete scoped register. |
| `exact_use_clearance` | The complete inventory is accepted and all copied/adapted uses have valid exact-use receipts. |
| `authorized_distribution_decision` | The required scope-bound distribution attestations exist for that complete candidate and its expression uses. This does not mean publication happened. |

Missing approvals leave conditions unknown (`null`). Valid partial expression
approvals preserve all declared uses in the denominator and cannot close the
candidate. Unreviewed outputs mean even that declared-use denominator remains
uncertified. The CLI returns `0` only for exact-use clearance, `1` for valid but
uncleared accounting, and `2` for invalid data or evidence. The strict
`validate_accounting_result` helper checks internally consistent results; callers
must obtain results from the actual validator and must not accept an arbitrary
report sidecar as release evidence.

A candidate with zero registered uses can clear only when it contains at least
one actual output, every output explicitly declares `NO_UPSTREAM_EXPRESSION`,
and the independent complete inventory receipt approves precisely that
disposition. The output then sets `zero_use_clearance: true` while retaining
`completed: 0` and `denominator: 0`. It emits no fabricated 100% statistic. An
empty candidate, an absent register, or a draft with no reviewed uses cannot take
that path.

All committed test attestations are constructed dynamically in temporary test
directories under explicitly synthetic identities. They exercise validation and
are not project approval receipts. Native behavior, source synthesis, legacy
whole-corpus rights accounting, estate rollout and organization acceptance remain
separate evidence boundaries.
