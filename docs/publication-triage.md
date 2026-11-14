# Publication output review triage

`python -m ges.publication_triage` prepares concrete review work for every
tracked file in an immutable candidate Git tree. It supplies file identities,
source associations, candidate expression locations and, when authenticated
source text is available, exact comparison results. It does not classify a
whole output as original, independently paraphrased or licensed. Every output
retains `UNREVIEWED`.

This packet advances the investigation behind the
[actual-use publication register](publication-use-register.md). It is not that
register, a clearance result, an approval policy or an acceptance receipt.
Structural evidence and byte equality cannot grant rights or authenticate a
human. The semantic review, independent omission audit, exact-use judgments,
approved authority and applicable acceptance/distribution evidence remain
separate work.

## Choose and preserve the exact candidate

Use the exact 40-character commit SHA selected for the candidate. The tool reads
all regular Git blobs directly from that commit, including normally hidden
tracked files. It verifies each Git blob hash and records SHA256 and byte size.
Mutable worktree contents, untracked files, checkout filters and new report files
cannot change the selected tree. Symlinks and submodules are rejected rather
than silently omitted. The tool never runs imported source code or Git hooks.

The scope is the entire tracked repository at the named revision. Selecting a
subset for a later package is a separate scope decision. A package subset must
not be represented as the complete GES v0.2 release. Keep this report outside
any directory exported as the candidate's actual publication outputs.

```sh
python -m ges.publication_triage \
  --repository . \
  --revision EXACT_40_CHARACTER_CANDIDATE_COMMIT_SHA \
  --artifacts evidence/claim-workload-inputs/artifacts.jsonl.gz \
  --output .cache/publication/review-inputs/output-triage.json.gz
```

The output is compact JSON; a `.gz` destination produces deterministic gzip
compression with no timestamp or original filename in its header. Existing
output files are never overwritten. The CLI prints a small factual summary.
Exit `0` means the triage report was produced, not that publication is cleared.
Exit `2` means an input or inventory check prevented report generation. An
individual candidate file that cannot be parsed is still inventoried and marked
`CONTENT_PARSE_REQUIRES_REVIEW`; the summary counts incomplete scans explicitly.
For example, an unrendered JSON template can require manual format review even
when its placeholders are intentional.

## What each observation establishes

| Observation | Meaning and required next judgment |
|---|---|
| `EXACT_SOURCE_EXPRESSION_MATCHES` | At least one candidate field or paragraph matched authenticated source text. Review the actual expression, inherited components, intended distribution and applicable notices. A match does not determine copying direction or grant permission. |
| `SOURCE_ASSOCIATED_EXPRESSION_CANDIDATES` | A source-associated field or paragraph meets the declared detector thresholds. Comparison and semantic classification remain necessary. Without source bodies, this is an investigation lead. |
| `SOURCE_LOCATORS_PRESENT` | The file contains at least one source identity that resolves to the authenticated pinned inventory. This does not mean the rest of the file is reference-only. |
| `NO_SOURCE_LOCATOR_DETECTED` | These rules found no authentic source locator. This is not evidence of original authorship or absence of upstream expression. Inspect authorship, implementation/template ancestry and uncited material. |
| `CONTENT_PARSE_REQUIRES_REVIEW` | The exact output is retained, but the parser could not inspect its declared format completely. Inspect the bytes manually or prepare a new candidate after any intended format repair. |

`content_role` is an independent path-based routing label: evidence record,
control draft, generated view, notice, template, implementation, test, instruction,
documentation, profile, schema or support file. A routing label has no copyright
or authorship significance.

The detector follows explicit source/repository, commit and path fields through
structured records, resolves pinned GitHub file locators, and records unresolved
identities without fabricating artifacts. Directory URLs, stale paths and
unsupported source associations can appear among unresolved locators; that list
is review work, not a claim that every URL is erroneous. The global source index
contains only identities accepted against the independent inventory authority.
Pinned references to external repositories are retained as
`OUTSIDE_AUTHENTICATED_SOURCE_INVENTORY`; they do not expand the adopted corpus
or acquire authority from appearing in a candidate. This retains concrete
component and licensing provenance for separate review.

For structured records, the detector observes named fields such as `statement`,
`source_statement`, `objective`, `title`, `description`, `excerpt`, `quote` and
`acceptance`. It retains fields with at least 40 UTF-8 bytes and six whitespace
separated words. These explicit thresholds bound the investigation; shorter
expression remains review work. The packet contains JSON pointers and hashes,
not copies of the field text.

For source-linked text files, the detector observes paragraphs meeting the same
thresholds. For generated views, it also locates exact occurrences of candidate
fields from `controls/catalog.json`, recording the canonical JSON pointer. This
preserves a concrete dependency when a generated checklist does not repeat
source locators. Repeated identical canonical fields are grouped, retaining
their additional JSON pointers and source associations. It does not prove that every possible generated or transformed
expression was discovered.

The detector is deliberately not a semantic originality classifier. Its counts
describe observed candidate fields and spans. Repeated fields, overlapping
paragraphs, shared legal text and multiple source associations can produce
multiple candidates for related expression. Do not reuse those counts as the
number of distinct actual publication uses or as a completed-review numerator.
Likewise, a complete metadata inventory can mention all 13,657 source artifacts;
their presence in the locator index does not mean the candidate uses expression
from all of them.

## Source authority and optional body comparison

The complete supplied artifact inventory must pass the same independently
trusted source-tree binding used by the corrected publication validator. The
default is the pinned A3 reference and its built-in SHA256 fingerprint. Canonical
artifact IDs, commits, paths, content hashes, Git blob hashes, sizes, kinds and
complete per-source identity digests are checked. A fabricated row that merely
uses the right commit cannot establish a source association.

Alternate authority inputs require `--source-inventory-reference` and
`--source-inventory-sha256`. Supply the expected fingerprint through the
controlled review process; never derive trust from a replacement artifact row,
triage result or self-authored authority receipt. The source inventory supplied
by the preserved current workload metadata does not reproduce the missing
historical artifact-input bytes.

When the complete pinned text snapshots have been restored and validated, add:

```sh
python -m ges.publication_triage \
  --repository . \
  --revision EXACT_40_CHARACTER_CANDIDATE_COMMIT_SHA \
  --artifacts evidence/claim-workload-inputs/artifacts.jsonl.gz \
  --source-root .cache/sources \
  --output .cache/publication/review-inputs/output-triage-with-comparisons.json.gz
```

The snapshot filenames follow `SOURCE_OWNER__REPOSITORY.text.jsonl.gz`. For each
locked source, `verify_snapshot` checks every text artifact against the complete
authenticated inventory: unique membership, metadata identity, content SHA256,
Git blob hash, size, gzip completion and unchanged snapshot bytes. Only source
texts needed for comparison are retained in memory. The report records the
snapshot hash and completeness observation; it does not include source bodies.

Comparisons use the exact decoded JSON field or observed paragraph bytes. They
do not normalize whitespace, substitute synonyms or infer independence from a
failed match. Each candidate records compared and unavailable source artifact
IDs. Binary source artifacts remain unavailable to this text comparison. Missing
source bodies yield `NOT_SUPPLIED`; incomplete eligible comparisons remain
explicit. These snapshots are pinned repository text, not a replay of rendered
published page bodies or the historical 18,019-page body count.

## Byte locations and review handoff

| Field | Review use |
|---|---|
| `candidate_revision`, `candidate_tree`, `output_inventory_digest` | Bind the complete selected Git output scope. A changed candidate requires a new cut. |
| `outputs[].path`, `git_blob_sha`, `sha256`, `size_bytes` | Locate and independently check every actual output file. |
| `source_artifact_ids`, global `source_artifacts` | Join source associations to authenticated repository/commit/path/content identities. Mere membership does not establish use. |
| `expression_candidates[].locator` | Locate the exact JSON value or paragraph in the output; generated matches also record `derived_from`. |
| `output_range`, `range_encoding` | Locate the original encoded output bytes, or explicitly identified decoded container bytes. |
| `decoded_text_sha256`, `decoded_text_bytes` | Bind the comparison value without reproducing source expression in the packet. |
| `exact_matches[].source_range`, `match_kind` | Locate the corresponding pinned source bytes and distinguish raw output equality from decoded-string equality. |
| `existing_rights_finding_references` | Join authenticated artifacts to exact, hashed records in the candidate's existing rights-review queue. The recorded finding status is not adopted as clearance. |
| `review_requirements` | Route unresolved classification, authorship, source comparison, component grants, notices, template/code ancestry, omission review and exact-scope approval work. |

Ranges are zero-based and end-exclusive. JSON string ranges exclude their quote
delimiters and preserve escapes exactly as stored. If a source string contains
quotes, newlines or escaped Unicode, an exact decoded-string match may require
an adaptation or representation judgment; the tool does not choose that
classification. `EXACT_RAW_BYTES` is emitted only when the stored output span
hash also equals the matched source-expression hash.

For compressed JSON, ranges refer to the explicitly hashed decoded payload,
not to a slice of the compressed publication file. Such a range cannot be copied
into the actual-use register as a raw output span. Resolve the concrete
distribution form and corresponding source/output spans first.

Reviewers should begin with exact matches and source-associated control,
proposal, notice and template wording, while retaining every other output in
the omission-review denominator. Resolve the actual use classification and
component rights for each identified use, supply the necessary source evidence,
and add the exact rows to the publication register. Whole-output review remains
`UNREVIEWED` until the complete classification work is justified. No policy,
human attestation, approval receipt, adoption decision or distribution action
is created by this tool.
