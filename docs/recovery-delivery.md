# Recovery delivery — 2026-10-01

Owner: [PR #1](https://github.com/4444J99/github-engineering-standards/pull/1).
Project status: **NOT COMPLETE**. This is a verified repair and preserved handoff,
not a release or an exhaustive six-source standard.

## Recovered work

Historical checkpoint `30b1f83c5eeb3db48ea168bdd9d4cfeb8532c040` is retained.
All 688 historical IDs, objectives and source mappings are preserved: 95 canonical
reviewed drafts and 593 non-adopted proposals. Proposal bindings are experiments,
not accepted policy. The legacy category-based generators now refuse execution.
No control was marked ACCEPTED, no protection was activated and no target was renamed.

Collector repairs enforce authenticated HTTPS redirect boundaries, bounded pagination,
typed observations, snapshot-pinned Contents requests, and coverage of local action
manifests outside `.github`/`docs`. Organization and enterprise flags are exposed in
the CLI; unsupported or inaccessible observations remain explicit. Enterprise adapter
completeness is not established. `--ref` allows inspection of an implementation branch.
Organization defaults use metadata fields documented in the
[organization API](https://docs.github.com/en/rest/orgs/orgs) and the
[code security defaults endpoint](https://docs.github.com/en/rest/code-security/configurations#get-default-code-security-configurations);
they do not infer effective protection on existing repositories from new-repository defaults.

Evaluator repairs reject missing key properties, malformed/null/incomplete alert
collections, boolean review thresholds, malformed actions and job permission overrides.
Missing inherited scope evidence remains UNKNOWN; repository attestations cannot
satisfy organization/enterprise manual controls. Non-adopted proposals block a gate.
Ruleset presence never counts as verified enforcement. CodeQL syntax alone remains
NOT_VERIFIABLE for configuration/coverage objectives.

Review accounting now validates reviewer authority, timestamps, candidate identities,
digests, dispositions, control IDs/revisions and complete candidate accounting. Invalid
or duplicate receipts do not increase review totals. Source-change impact compares
stable source/path identities across commits and can invalidate transitive include
dependents using a validated dependency ledger; rendered conditionals remain unverified.
Provenance requires digests and ordered
line spans. Structured GHQR extraction records full definition spans; WA heading
classification excludes SPDX headings. These repairs do not certify semantic extraction.

The pinned `atapas/model-repo/LICENSE` was read and its MIT notice corrected. Notice
discovery now recognizes extensionless license files. Acquisition failures return nonzero,
and packaging preserves failure reports even without a corpus, including third-party notices.
Per-file rights clearance remains unfinished.

## Observed verification

- `python -m unittest discover -s tests -v`: 155 tests passed, exit 0.
- `python -m ges validate`: 95 controls valid, exit 0.
- `python -m ges compile`: generated canonical views, exit 0.
- `git diff --check`: exit 0 after whitespace correction.
- `python -m ges ledger --snapshots .cache/sources --corpus .cache/corpus`: exit 0;
  3,742 Docs files, 18,019 published instances, 14 unresolved instances, 605 structured
  requirements and 61,801 dependencies. Rebuilding does not mark any item reviewed.
- `python -m ges.recovery --sources .cache/sources --corpus .cache/corpus --output evidence/recovery-status.json`:
  exit 0; all nine gates OPEN, 13,657 artifacts.

Tests include synthetic local CLI fixtures and counterexamples. They are not native
GitHub behavior tests, and do not prove every quarantined objective correctly bound.
No disposable native enforcement experiment was performed.

The authenticated read-only self-collection succeeded at the live default-branch SHA
`0c7a069ea1f36e269ad72995fee21cc9b64f31ca`. This proves access to the repository,
not merge of the implementation. With the draft solo-software profile: 95 expected,
81 applicable, 3 PASS, 12 FAIL, 60 MANUAL_REVIEW and 6 NOT_VERIFIABLE.
`python -m ges gate --report .cache/recovery-self-assessment.json --require-accepted`
returned exit 1, as required. Raw snapshot details remain ignored; only sanitized
summary evidence is committed. Observed endpoint statuses were Dependabot 400,
code scanning 403, secret scanning 404, and configuration/CODEOWNERS 404. Those
statuses do not establish a particular licensing or permission cause.

Read-only collection of the pushed implementation at `168abf90dfbc78fab36240cae8e33b041a80e0cc`
produced 13 PASS, 2 FAIL, 60 MANUAL_REVIEW and 6 NOT_VERIFIABLE across the same
81 applicable controls. No instance had verified native enforcement, and the accepted
gate remained false. `evidence/recovery-self-assessment.json` retains the sanitized result.

## Remaining acceptance and resumption

`evidence/recovery-status.json` owns the nine-gate construction counts, pins and
unresolved published entries. Validated source-review receipts now cover 22/13,657
artifacts: `atapas/model-repo` 8/8, `tmcw/github-best-practices` 1/1, and the
governance template 13/13. They account for 465 candidate blocks and phrase 222
atomic reference claims. This is not an independent omission audit.
Mappings, adoption and independent omission audit remain open. The other source
review counts remain `github/docs` 0/13,219, Well-Architected 0/244, GHQR 0/172,
with no source-wide rights acceptance established.
The 12 earlier purported exclusions remain unsubstantiated, not justified.
All 605 structured occurrences need reconciliation; 150,903 candidates are not a
complete claim denominator. Accepted-control implementation coverage is undefined
because the accepted-control denominator is zero. Native/estate target denominators
remain undefined until an authorized inventory is declared.

Next implementation work belongs to this same PR: review pinned partitions, preserve
all duplicate occurrences and conflicts, author exact objective-specific bindings,
review templates/profiles, and validate omission coverage. Then prepare an exact
disposable-target policy diff and obtain the applicable approval before native
activation. Rights acceptance, release publication and estate rollout retain their
separate human authority gates. Passing local tests does not permit bypassing them.

To reproduce the review queue and status without running upstream code:

```sh
python -m ges corpus --snapshots .cache/sources --output .cache/corpus
python -m ges ledger --snapshots .cache/sources --corpus .cache/corpus
python -m ges.recovery --sources .cache/sources --corpus .cache/corpus --reviews evidence/source-reviews --review-policy evidence/source-review-policy.json --output evidence/recovery-status.json
python -m ges coverage --artifacts .cache/corpus/artifacts.jsonl --candidates .cache/corpus/candidates.jsonl --reviews reviews.json --review-policy review-policy.json
python -m ges impact --old old/artifacts.jsonl --new new/artifacts.jsonl --output .cache/impact.json
```

The review policy must name genuinely authorized reviewers. Receipts supply a mapping
for each candidate with its digest and either an exact control/revision or a reasoned
reference/exclusion disposition. The tool validates records, not the truth of judgments.
The acquisition workflow is on-demand; no scheduled drift service was activated.

Checkout retained for continued implementation. No corpus cache, transcript, private
assessment payload, token or unrelated repository change is included in this delivery.
Session release, four historical closeout indices and project completion are unproven.
