# Proposed amendment: JSON string representation, version 2

Status: OWNER_APPROVAL_PENDING. This proposal does not change the v1 validator,
classify any use, grant rights, or authorize distribution. Preserve all historical
candidate bytes and approvals, including candidate f628db26.

## Owner decision requested

Approve implementation of an opt-in v2 publication-use contract which distinguishes
JSON string encoding from changes to the decoded expression. Retain raw source and
output digest binding and all existing independent rights, audit, human acceptance
and distribution gates. Approval of this engineering amendment is not approval of
any individual expression use or release.

## Exact interface

Keep v1 records and raw-byte comparison unchanged. A v2 use record adds exactly
one `representation` object with:

- `mode`: `RAW` or `JSON_STRING`.
- For `RAW`, no additional fields; current byte equality applies.
- For `JSON_STRING`, `json_pointer`, `token_start_byte`, `token_end_byte`, and
  `decoded_expression_sha256`. The token bounds include both JSON quote delimiters;
  existing output expression bounds still identify the encoded token interior.

Use UTF-8 byte offsets into the digest-bound complete output file, never character
indices. Parse the complete JSON document with duplicate object keys rejected.
Resolve the RFC 6901 pointer, including array indices, to a string. Parse the
complete token with a standards-conforming JSON decoder and require it to be the
specific string token selected by that pointer, not another equal-valued occurrence.
Require the expression bounds to equal the interior of that token. Reject trailing
garbage, unpaired surrogates, malformed UTF-8, ambiguous paths and nonstring values.

Keep existing raw source/output span hashes and whole-file hashes. Separately hash
the UTF-8 encoding of the decoded expression. Compare that decoded expression with
the exact source-span UTF-8 expression, without whitespace normalization, Unicode
normalization, case folding or punctuation rewriting. Record both raw and decoded
equality outcomes. Do not rewrite source bytes to resemble output serialization.

`LICENSED_COPY` in `JSON_STRING` mode requires decoded equality AND a separately
reviewed lawful-use decision, attribution and obligation satisfaction. A substantive
decoded change remains an adaptation question; it is never excused as encoding.
Reference/paraphrase classification and whole-output audit requirements remain
unchanged. New v2 policy approval must bind the complete manifest and use register.

## The two held fields

The historical publication review identifies two GES-OPS-008 fields whose JSON
serialization adds two escape bytes: raw output is 170 bytes while decoded source
expression is 168 bytes. Their locations and exact digests remain in
`evidence/wave-20261009/publication/primary-review.json` and
`evidence/wave-20261009-correction-01/publication/`.

Proposed rights-review package for EACH field:

1. Exact source repository, pin, artifact/full-file/span hashes and byte bounds.
2. Exact candidate revision, output path/full-file/span hashes, pointer and token.
3. Raw comparison failure and decoded comparison result, each independently replayed.
4. Accountable reviewer decision on expression kind, applicable upstream license,
   attribution, notices, obligations and any unresolved restrictions.
5. Distinct independent use audit, complete inventory audit, human acceptance and
   distribution approval on the new immutable candidate; no inferred approvals.

These fields remain HOLD until that package is populated and accepted. A corrected
validator cannot clear either field by itself.

## Acceptance tests before implementation is accepted

Escaped quotes/backslashes/control characters and valid Unicode escapes must decode
without altering wording; literal UTF-8 and escaped Unicode must compare by decoded
expression. Reject substantive wording/whitespace/punctuation changes, wrong pointer,
equal string at a different location, duplicate keys, incomplete tokens, misaligned
multibyte offsets, strings nested in arrays, surrogate errors, stale raw hashes,
changed output files, unauthorized rights reviewers and missing audit subjects.
Unmodified v1 fixtures must retain their current behavior, including rejection of
raw unequal `LICENSED_COPY`. JSON representation never bypasses independent rights.
