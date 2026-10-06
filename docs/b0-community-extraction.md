# B0 community extraction

Status: staged proposal; **HOLD**. A0 remains Primary. Foundation PRs #472–#478
require their own acceptance. B0 does not certify extraction, approve policy or
advance to C0. The branch is stacked on A6 commit
`551e2650ec03e22ddb3b34627702bf51dfc620c4`; its PR targets the A6 branch so reviewers
see only this tranche. Integration into main remains conditional on foundation acceptance.

## Inputs and output

The immutable `evidence/semantics/b0/input-manifest.v3.json` names all 22 artifact
IDs: one tmcw README, 13 jlcanovas artifacts and eight atapas artifacts. It binds
commits, archive identities, inventory/snapshot hashes, Git blob hashes, line
counts, A3 capsule identity, A4 charter commit/file hashes and authored annotation
hash. All source bytes were read from the already acquired pinned snapshots.
No source refresh, linked-source admission or upstream execution occurred.

The primary deliverable is `evidence/semantics/b0/ledger/`: 178 source occurrences,
227 source-local proposition proposals, artifact/line accounting, residual ledger
and an output-digest receipt. The annotator read the full files; the compiler
consumes authored spans and interpretations rather than detecting keywords.
No authorized primary or omission review is asserted. Every review field remains
PROPOSED with null reviewer/evidence. The 227 pending proposition IDs and all 22
artifact/nonclaim reviews remain explicitly assigned to B0 in residual.json.

Each occurrence binds an exact inclusive line span; its digest includes original
line endings. If a single source span contains several independently actionable
statements, one occurrence links to several atomic proposition records. A5's
occurrence ID is span-based and its AST field holds the first proposition's AST;
formalization describes all linked propositions. The proposition ledger preserves
the other ASTs individually. This avoids duplicate occurrence identities without
silently consolidating different statements. Source-local file scopes remain
intact; C0 alone decides duplicate/equivalent/conflicting relationships.

Every source line belongs to exactly one occurrence or reasoned nonclaim span.
Nonclaim reasons describe file-specific headings, scaffolding, contextual rationale,
reference metadata or placeholders. Both license files are explicitly reference-only
legal supporting inputs, not assertions that their legal text is nonoperative.
They do not add project-engineering propositions; D3 owns exact-use rights review.
Human review must approve these dispositions as well as all semantic interpretations.
Line accounting alone cannot establish omission-free meaning.

## Retained interpretation limits

- tmcw's long-lived continuous-delivery context, optional branch naming/deletion,
  prerequisite branching alternatives and author-merge exceptions remain explicit.
- jlcanovas retains source must/should/could distinctions, owner/admin assumptions,
  48-hour replies, two approvals, the more-than-14-day one-approval alternative,
  maintainer vetoes and all identity/parameter placeholders.
- The CC-BY-SA description versus CC BY 4.0 identities, differently enumerated
  conduct pledges and CODEOWNERS comments implying required approvals remain
  distinct source statements or ambiguity flags. No conflict is resolved here.
- atapas preserves template checklists, two-other-developer sign-off and delegated
  merge, differing embedded/standalone conduct versions, example stack commands,
  unrelated TryShape links and optional versus promotional starring language.
  None establishes native enforcement, a running app or consumer facts.

## Reproduction

Use the existing ignored snapshot directory as SOURCES; never execute upstream
setup or run a fresh sync. The three pinned archives can separately be hydrated
through A3's existing capsule workflow when access/custody permits.

```sh
python -m ges semantics extract --manifest evidence/semantics/b0/input-manifest.v3.json --annotations evidence/semantics/b0/annotations.v3.json --sources SOURCES --output NEW_OUTPUT
python -m ges semantics extract --manifest evidence/semantics/b0/input-manifest.v3.json --annotations evidence/semantics/b0/annotations.v3.json --sources SOURCES --output evidence/semantics/b0/ledger --check
python -m ges semantics validate --input evidence/semantics/b0/ledger/occurrences.jsonl
python -m ges semantics validate --input evidence/semantics/b0/ledger/propositions.jsonl
```

NEW_OUTPUT must not exist. Compilation validates the fixed three-source pins and
full artifact denominators, inventory membership, content and Git blob digests,
authored annotation hash, complete nonoverlapping line accounting, closed semantic
schemas, stable unique IDs and the 250-proposition cap. Invalid inputs publish
nothing. `--check` compares exact output membership and bytes without writing.
Receipt status stays HOLD even when these structural checks pass.

Excluded: GHQR, Well-Architected, Docs, external linked content, reconciliation,
controls, consumer templates, rights clearance, native operations and rollout.
The next tranche is C0 only after B0's approved exact head is merged and verified
on main with an empty in-scope residual ledger. Pending B0 judgments cannot move
into C0. The worktree is retained for review and dependency integration.

## Correction revision 2

The original manifest and annotations remain unchanged as revision-1 evidence.
`input-manifest.v2.json` and `annotations.v2.json` freeze the corrected input set;
`revision-v2.json` maps all 207 old proposition IDs to their successors and names
nine added operative issue-template bindings. No source pins or source bytes changed.
Prohibitions apply to the underlying action: PROHIBITED + NEGATIVE means the
subject must not perform that action, never that avoiding it is prohibited.
The compiler rejects negated avoidance verbs in prohibited predicates.
All four pledge enumerations are explicitly represented as source-bound
characteristic parameters; omitted or reordered members fail validation.
Nonempty template name/about/title/labels/assignee values require authored
implementation parameters even if their lines otherwise have nonclaim accounting.
These bounded guards do not certify arbitrary semantic truth or reviewer authority.

## Full primary and independent review correction (v3)

The original v2 review remains in history and its immutable inputs remain present.
Full source review found eight groups of defects across fourteen records/spans: mixed
permissions and duties, a lost citation condition/actor, moderation responsibility,
incomplete conduct terms, graceful feedback and the warning trigger.
`revision-v3.json` maps all 216 predecessor proposition IDs to 227 successors.
Compilation still emits PROPOSED records and HOLD; reviewed acceptance is a separate
digest-bound record, never a side effect of generation.
