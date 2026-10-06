# Source-fidelity and omission receipts

`ges.source_fidelity` validates two corpus-wide gate prerequisites:

1. an atomic-claim fidelity audit; and
2. an independent source-to-claim omission audit.

It does not infer semantic truth from an artifact count, candidate count, claim
count, file presence, or a successful provenance check. The accountable
auditors own the truth of their judgments. This adapter cannot replace the
remaining artifact reviews or make an unaudited paraphrase correct.

## Bound inputs

The adapter reruns source-review accounting with `coverage_with_reviews` and
reference-claim provenance with `validate_provenance`. Its immutable subject
binds canonical digests and counts, plus raw SHA-256 hashes where byte identity
matters, for:

- the complete artifact inventory and candidate ledger;
- the ordered source-review document manifest, source-review receipts,
  source-review accounting, and source-review authority policy;
- locked source pins, the canonical control catalog, and quarantined proposal
  queue; and
- every reviewed claim-document path/digest plus the resulting provenance
  report.

Invalid review receipts or claim provenance fail validation. Partial artifact
review remains `INCOMPLETE`. A zero inventory has unknown coverage. Neither can
receive a passing certificate. With neither certification input, both audit
outcomes remain `null` without error even when artifact coverage is complete.
A supplied policy is validated even when the paired receipt array is empty.

The source-review policy authorizes bounded disposition work only. It is not a
source-fidelity certification policy and cannot grant either audit role.

## Authority policy

Schema: `ges.source-fidelity-authority-policy.v1`.

The policy requires:

- a durable, nonempty `approval_reference`;
- `subject` exactly equal to the adapter's computed subject; and
- nonempty, unique `authorized_fidelity_auditors` and
  `authorized_independent_omission_auditors` identity lists.

This policy is a separately approved trusted input. JSON names and digests do
not authenticate people or establish the adequacy of their review.
Unknown policy, receipt, or evidence fields are rejected so contradictory
side-channel assertions cannot coexist with a passing result.

## Certification receipt

One corpus-wide receipt uses schema
`ges.source-fidelity-certification-receipt.v1`. It repeats the exact subject,
names one authorized `fidelity_auditor`, names a distinct authorized
`independent_omission_auditor`, supplies a timezone-bearing `certified_at`, and
references exactly two evidence documents:

- `atomic_claim_fidelity_audit`; and
- `independent_source_to_claim_omission_audit`.

Certification must postdate the bound source and claim reviews and cannot be in
the future. Multiple corpus receipts, self-audit, foreign roles, changed counts,
or changed input digests fail validation.

## Evidence documents

Each evidence reference contains a relative `evidence/*.json` path and exact
SHA-256 digest. The shared evidence loader rejects absolute or parent-traversal
paths, symlinks, missing files, non-JSON values, changed bytes, and files over
1 MB.

The document uses schema `ges.source-fidelity-evidence.v1` and records the exact
`kind`, authorized `identity`, complete `subject`, timezone-bearing
`reviewed_at`, literal `outcome: "PASS"`, literal `unresolved: []`, and bounded
nonempty `method` and `observations`. Fidelity evidence belongs to the fidelity
auditor; omission evidence belongs to the independent omission auditor. Both
must postdate the reviewed inputs and not postdate certification.

Evidence, the complete review-directory manifest (including claim documents),
and all pinned compressed source snapshots are read again before success is
returned. Snapshot content digests are bound in `source_snapshots_digest` in
the subject; adding a claim document or replacing source bytes invalidates
certification. Existing certificates must be regenerated for the expanded
subject. These checks detect changes between reads; callers must keep the
input capsule immutable because the validator does not lock concurrent writers.

## Result boundary

A valid receipt changes only these prerequisite fields to `true`:

- `atomic_claim_fidelity_audit`; and
- `independent_source_to_claim_omission_audit`.

The result always keeps
`semantic_truth_automatically_certified: false`, `rights_cleared: false`, and
`policy_adopted: false`. Even a valid adapter result is not control adoption,
rights clearance, published-page assurance, native enforcement, estate rollout,
or project completion. Human or otherwise independently authorized audit truth
remains external to the validator.

## Command

Run from the repository root with the exact frozen corpus and source snapshots:

```sh
python -m ges.source_fidelity \
  --artifacts .cache/corpus/artifacts.jsonl \
  --candidates .cache/corpus/candidates.jsonl \
  --reviews evidence/source-reviews \
  --review-policy evidence/source-review-policy.json \
  --sources .cache/sources \
  --catalog controls/catalog.json \
  --proposals controls/review_queue.json \
  --certification-receipts RECEIPTS.json \
  --certification-policy POLICY.json
```

Omit both certification options for accounting-only output with unknown audit
outcomes. Supplying only one is invalid. Invalid inputs print
`{"valid": false, ...}` and exit 2.
