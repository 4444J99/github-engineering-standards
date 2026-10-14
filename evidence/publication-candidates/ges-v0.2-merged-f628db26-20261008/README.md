# Frozen merged-main publication review candidate

This packet inventories the complete tracked GES tree at merged main commit
`f628db26cee1e6fc8fcc5ad5513959de0401d73d`. It adds authenticated source comparison
and a concrete review queue for that exact candidate. **All 2,396 output files
remain `UNREVIEWED`; exact-use clearance and distribution authorization remain
unknown.** The packet grants no rights, records no publication approval, and
accepts no controls.

The prior candidate at `db7517449f5c11750ca55dfeccc47167c10c3fb4` remains a
separate, unchanged historical checkpoint. A later toolkit commit, source-review
continuation, or review packet is outside this candidate unless its bytes were
already tracked at the exact merged-main revision named here.

## Exact scope and accounting

| Item | Observation |
|---|---|
| Candidate ID | `ges-v0.2-merged-main-f628db26-20261008` |
| Candidate revision | `f628db26cee1e6fc8fcc5ad5513959de0401d73d` |
| Candidate Git tree | `51f2ae5030dddce8add625dbc709c48ac37ebbf2` |
| Output scope | Every tracked regular file in that tree, including existing evidence and historical review packets |
| Inventory | 2,396 files; 129,939,371 bytes |
| Output inventory digest | `87db152e1e263409e1b385e103c525b70e8b6a4c45292112634a4122aef06e25` |
| Output classifications | 2,396 `UNREVIEWED` |
| Actual-use register | No classified use rows; declared denominator 0 is uncertified |
| Review policy / receipts | Empty object / empty array |
| Accounting command | Exit 1; valid accounting with clearance unknown |
| Acceptance or publication credit from this packet | Zero |

[manifest.json](manifest.json) lists each output's exact path, SHA256 and byte
size. [register.json](register.json) binds the same complete output set to its
unreviewed dispositions. [accounting.json](accounting.json) records complete
output inventory coverage while leaving `use_register_complete`,
`exact_use_clearance` and `authorized_distribution_decision` null.
`zero_use_clearance` is false. An empty register does not establish an absence of
upstream expression.

The exported candidate directory and this packet are disjoint. The packet was
written after the frozen export, outside its tree, so its own manifest, register,
triage and review notes do not change the candidate's accounting denominator.
[scope.json](scope.json) binds every other packet file by exact file hash and
size. Its own identity is supplied by the containing Git commit.

## Review priorities grounded in actual output bytes

[output-triage.json.gz](output-triage.json.gz) contains one record for every
output, with its immutable Git blob, SHA256, size, structural role, source
associations, precise expression locations, comparison results and remaining
review requirements. [review-priorities.json](review-priorities.json) provides a
compact navigation layer, including all 593 proposal IDs and their detected
matched-field locations. Neither file replaces the actual-use register.

| Machine observation | Outputs | Meaning for the next review |
|---|---:|---|
| `EXACT_SOURCE_EXPRESSION_MATCHES` | 7 | Inspect the detected equal spans and determine the actual use, rights holder, component grant and necessary notices. |
| `SOURCE_ASSOCIATED_EXPRESSION_CANDIDATES` | 677 | Source-associated wording needs comparison and classification beyond this exact-match method. |
| `SOURCE_LOCATORS_PRESENT` | 743 | Inspect the actual file and its ancestry; a locator alone does not establish either expression use or reference-only status. |
| `NO_SOURCE_LOCATOR_DETECTED` | 968 | Review uncited, inherited and transformed material; the detector provides no originality determination. |
| `CONTENT_PARSE_REQUIRES_REVIEW` | 1 | Inspect the retained exact bytes and intended rendering before relying on format-level classification. |
| **Total** | **2,396** | **Every output remains in the review denominator.** |

The method found 62,591 candidate fields or paragraphs and 1,491 candidates with
at least one exact pinned-source match. These are detector units, not distinct
works, legal uses, accepted claims or certified clearance units. The seven
outputs with exact matches are:

| Output | Matched candidate spans | Specific review work |
|---|---:|---|
| `controls/review_queue.json` | 1,477 | Review generated proposal titles, objectives and acceptance wording against 24 pinned source artifacts. |
| `THIRD_PARTY_NOTICES.md` | 9 | Check the applicability and completeness of notices. Nine paragraphs match three pinned license files, yielding 27 source associations. Shared legal text does not establish copying direction or a grant for other material. |
| `evidence/sdk-persistence-independent-claim-audit.json` | 1 | Review `/audited_inputs/0/snapshot/claims/95/statement` against the pinned SDK session-persistence source. |
| `evidence/source-reviews/docs-sdk-byok-claims.json` | 1 | Review `/claims/101/statement` against the pinned SDK BYOK source. |
| `evidence/source-reviews/docs-sdk-persistence-claims.json` | 1 | Review `/claims/95/statement` against the pinned SDK session-persistence source. |
| `evidence/source-reviews/docs-sdk-server-token-claims.json` | 1 | Review `/claims/23/statement` against the pinned SDK server-to-server token source. |
| `evidence/source-reviews/wa-governance-productivity-checklists-claims.json` | 1 | Review `/claims/123/statement` against the pinned Well-Architected productivity checklist. |

The proposal queue contains 593 records, all still `NON_ADOPTED_DRAFT`. Of those,
543 have at least one detected exact field match. The 1,477 matched fields
comprise 542 objectives, 542 acceptance fields and 393 titles: 315 are associated
with GHQR and 1,162 with Well-Architected. Of these matches, 1,475 match the stored
output span's raw bytes; two match a decoded JSON string whose stored escaping
differs. The remaining 50 proposals have no detected exact match under the
declared method and receive no independent-authorship credit.

Each priority output carries its exact SHA256 and size, source repository,
commit, path and content hash in the JSON packet. The full triage supplies the
zero-based, end-exclusive output and source ranges, range hashes, JSON pointers,
and distinction between raw equality and decoded-string equality. It preserves
52 references to existing rights findings by original file hash, record digest
and JSON pointer. Existing finding statuses supply no publication clearance.

There are 224 unresolved locators across 32 outputs. These include directory
references, stale or mismatched paths, and references outside the fixed corpus;
the count is not 224 confirmed content defects. The single incomplete format
scan is `templates/ruleset.json`, an unrendered template with placeholder syntax
that is not valid standalone JSON. Its complete 632 bytes remain inventoried
and require review in their intended rendering context.

## Source evidence and limits

The source metadata must match the complete, independently pinned A3 source
inventory reference:
`05dab95bfbc88c2401a97da702339f4f1be89545c8f8c9f48198194aac07bb15`.
Canonical IDs, source commits, paths, SHA256 digests, Git blobs, sizes, artifact
kinds and complete per-source identities are checked. A fabricated artifact row
that merely matches a source commit cannot establish a valid association.

All six complete pinned text snapshots passed `verify_snapshot` before the
comparison run. The triage records each source commit and exact snapshot hash.
The comparison reads source bytes only from that validated cache and writes no
source body text into the review packet. The global source index contains all
13,657 source artifacts because the candidate includes complete metadata; that
membership does not mean the candidate uses expression from every artifact.

The method uses selected JSON fields or associated paragraphs of at least 40
UTF-8 bytes and six words, without fuzzy matching, normalization or semantic
inference. It does not exhaust short, transformed, uncited, binary, inherited or
externally sourced expression. A missing exact match cannot prove independence.
For compressed containers, recorded ranges locate the explicitly hashed decoded
payload; they cannot be pasted into an actual-use register as raw compressed
output spans.

These observations validate the pinned repository text snapshots. They do not
reproduce the missing original historical artifact-input bytes, certify the
historical workload totals from those unavailable bytes, or reconfirm the
historical 18,019 rendered-page body count. Current preserved artifact metadata
and historical unavailable input identities remain distinct.

## Reproduce a new local observation

Use a checkout containing the triage implementation introduced by local commit
`59052516d163cdaa7c137fa049bc877796b7a495`, whose parent is the frozen merged-main
revision. That implementation commit adds only the triage module, its tests and
its contract document. The publication-accounting implementation is unchanged
from the candidate. Do not export the later continuation checkout as though it
were the frozen main tree.

The commands below assume Bash and an already authenticated, complete six-source
text cache at the specified `source_root`. Create a new replay directory; retain
this packet and the prior candidate unchanged. Source hydration must use the
exact locked archives and trusted A3 inventory, without replacing historical
inputs with live page lists.

```sh
candidate_revision=f628db26cee1e6fc8fcc5ad5513959de0401d73d
review_root=.cache/publication/replay-f628db26
source_root=/path/to/validated/pinned/source-cache
mkdir -p .cache/publication
mkdir "$review_root"
mkdir "$review_root/candidate"
git archive "$candidate_revision" | tar -x -C "$review_root/candidate"
python -c 'import gzip,pathlib,sys; pathlib.Path(sys.argv[2]).write_bytes(gzip.decompress(pathlib.Path(sys.argv[1]).read_bytes()))' \
  evidence/claim-workload-inputs/artifacts.jsonl.gz "$review_root/artifacts.jsonl"

python -m ges.publication_use prepare-draft \
  --output-root "$review_root/candidate" \
  --draft-directory "$review_root/inputs" \
  --candidate-id ges-v0.2-merged-main-f628db26-20261008 \
  --candidate-revision "$candidate_revision" \
  --distribution-scope 'Proposed complete GES v0.2 public source release at frozen merged main; review inputs do not authorize distribution.' \
  --release-scope GES_V0_2

publication_exit=0
python -m ges.publication_use \
  --manifest "$review_root/inputs/manifest.json" \
  --register "$review_root/inputs/register.json" \
  --receipts "$review_root/inputs/receipts.json" \
  --policy "$review_root/inputs/policy.json" \
  --artifacts "$review_root/artifacts.jsonl" \
  --output-root "$review_root/candidate" \
  --source-root "$source_root" > "$review_root/accounting.json" || publication_exit=$?
test "$publication_exit" -eq 1

python -m ges.publication_triage \
  --repository . \
  --revision "$candidate_revision" \
  --artifacts evidence/claim-workload-inputs/artifacts.jsonl.gz \
  --source-root "$source_root" \
  --output "$review_root/output-triage.json.gz"
```

The accounting result must have `valid: true`, 2,396 unreviewed outputs, complete
output inventory and unknown clearance. Exit 1 is the expected uncleared
result, not sufficient evidence on its own. Preparation timestamps change the
new register's file hash and digest; compare the frozen output identities and
truthful state rather than expecting a new preparation to reproduce timestamps.
For a byte-identical accounting replay, use this packet's existing manifest,
register, empty policy and empty receipts with the new exact export. The triage
is deterministic for the same implementation, candidate and source inputs.

The rebased tooling continuation passed `python -m unittest discover -s tests -v`
(667 tests), `python -m ges validate` (95 controls), `python -m ges compile`, and
`git diff --check`. These observations concern the continuation implementation;
they do not substitute for remote checks on merged main or organization
acceptance. The packet's cross-binding check additionally compares manifest,
triage and accounting identities and preserves every prior candidate binding.

## Evidence required next

Review the seven exact-match outputs first and record each actual use with the
appropriate output/source spans, component-specific rights evidence, notices
and justification. Resolve source locator and rendering questions. Continue
classification across every other output, including authorship, template and
code ancestry, transformed expression and omissions beyond the detector's
rules. A reviewer must explicitly justify reference-only or independently
authored classifications; this packet supplies neither.

Complete output classification, the independent omission audit, an authorized
exact-scope policy, applicable human approvals and the final distribution
decision remain separate requirements under the
[actual-use contract](../../../docs/publication-use-register.md) and
[triage method](../../../docs/publication-triage.md). A code-review approval or
ordinary PR merge does not supply these publication decisions. All synthesis,
rights, human acceptance and native-enforcement gates retain their own evidence
requirements; this packet closes none of them.
