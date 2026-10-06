# A6 reconciliation machinery

A6 consumes the A5 proposition and decision contracts. It produces deterministic
comparison proposals and validates independently reviewed disposition receipts.
It does not generate adopted policy or certify the truth of source meanings.

## Commands

```sh
python -m ges semantics reconcile --propositions propositions.jsonl --controls controls/catalog.json --output .cache/comparisons.json
python -m ges semantics audit --propositions propositions.jsonl --controls controls/catalog.json --decisions decisions.jsonl --authority authority.json --audits audits.json --evidence-root . --output .cache/reconciliation-audit.json
```

Outputs cannot overwrite an existing file. Proposal generation returns exit 0
when valid proposals are written. Audit returns exit 0 for complete decision
accounting, exit 1 for valid but incomplete accounting, and exit 2 for malformed,
stale, or unauthorized inputs. An audit batch contains at most 250 propositions.
The existing structure-only `semantics validate` remains available separately.

## Comparison proposals

Propositions with identical subject/action/object strings share a comparison
group. The report preserves every member and every differing AST field and
applicability expression. Modality or polarity differences yield
`POSSIBLE_CONFLICT`; other differences yield `RELATED`. These conservative
labels are retrieval aids, not equivalence or contradiction judgments. Different
predicates do not share a group merely because their text contains the same
keywords. This detector is deliberately incomplete: reviewers must still
identify conflicts expressed using different predicates.

Every proposal remains `PROPOSED`. Proposed records cannot satisfy review gates.
The input digest binds complete proposition records (including qualifiers,
exceptions, applicability, occurrence membership, and reviews) and complete
catalog records, sorted by identity. Order within semantic arrays is preserved.

## Authority and evidence

The authority object has exactly these fields:

```json
{
  "schema": "ges.reconciliation-authority.v1",
  "approval_reference": "owner-approved authority record",
  "input_digest": "digest returned by semantics reconcile",
  "primary_reviewers": ["primary"],
  "omission_reviewers": ["omission"],
  "reconcilers": ["reconciler"],
  "auditors": ["auditor"]
}
```

For each reviewed proposition, primary and omission identities must be
authorized. Each reviewed decision requires an authorized reconciler and an
independent auditor. All four roles must have distinct identities for each
proposition handled by the decision. This CLI checks the supplied authority;
the approved authority file and reviewer identities require the repository's
trusted review process. No real authorization is included by A6.

The audit-receipts JSON array contains one entry per decision:

```json
[{"decision_id": "reconciliation-decision:...", "auditor": "auditor",
  "evidence_reference": "evidence/independent-audit.json"}]
```

Every review reference points to a JSON file below `evidence/` under the explicit
evidence root. Absolute paths, traversal, symlink components, and files larger
than 1 MB are rejected. Evidence objects have exactly these fields:

```json
{
  "schema": "ges.reconciliation-evidence.v1",
  "kind": "INDEPENDENT_AUDIT",
  "reviewer": "auditor",
  "subject_digest": "canonical subject SHA-256",
  "input_digest": "current reconciliation input digest",
  "outcome": "PASS"
}
```

Kinds are `PRIMARY`, `OMISSION`, `RECONCILIATION`, and `INDEPENDENT_AUDIT`.
Proposition subject digests cover every field except the two review objects,
avoiding self-referential evidence hashes. Decision subject digests cover the
entire decision, including its stable ID and review reference. The audit report
records the actual evidence-file SHA-256 values, authority digest, decision
digest, and audit-receipt digest. Evidence remains an attestation by the named
reviewer; receipt validation does not independently prove their judgment.

## Dispositions and residuals

Every AST field must occur exactly once in `preserved_fields` or `lost_fields`.
Control dispositions require current catalog references; other dispositions
cannot map controls. Proposed controls must enter the explicitly supplied
catalog input before `NEW_CONTROL` or `SPECIALIZATION` can reference them.

`DUPLICATE` requires identical AST and applicability, at least two occurrences,
no preserved differences or ambiguities, and no lost fields. `SUPERSEDED`
requires predecessor and successor identities. Exclusion requires `OMITTED`
treatment and the contract's nonempty rationale.

`CONFLICT` requires known counterpart proposition IDs and `CONFLICTING`
treatment. A conflict stays in the residual ledger even after its receipt is
validated. Detected possible conflicts cannot be covered by non-conflict
dispositions. Resolve them in a later reviewed input revision, preserving the
prior report as history. Ambiguities and unmapped propositions likewise remain
unresolved. Multiple dispositions for one proposition are rejected.

Complete decision accounting concerns only the supplied immutable batch. It
does not establish corpus completeness, source fidelity, policy adoption,
rights, release acceptance, or effective native enforcement.
