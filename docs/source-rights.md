# Source provenance and redistribution

Sources are ingested at the commits in sources/sources.lock.json. Preserve per-file notices and source modification records. Acquisition is not license clearance.

The github/docs README declares CC BY 4.0 for documentation/content in assets, content and data, and MIT for code. The well-architected project declares MIT notices. GHQR and model-repo provide MIT license files. The jlcanovas template's LICENSE.md identifies Attribution 4.0, while its guideline text mentions a different Creative Commons starting point: record this inconsistency rather than silently relabeling it. The tmcw snapshot has no license file in its tree; this distribution uses independently phrased principles and provenance references, not a copy of its README.

Raw upstream text belongs in an ignored private cache. The default corpus exporter produces references, line ranges and hashes without source text. The structured GHQR and well-architected extraction outputs contain MIT-covered source definitions and must retain the notices in THIRD_PARTY_NOTICES. Other bundled templates and control wording are generalized project drafts, not claims of upstream endorsement.

This initial private bootstrap makes no decision to publish, sublicense or replace the user's rights policy. Public distribution and inherited material require the separate rights acceptance gate.

## File-specific recovery findings

`evidence/rights-review-queue.json` binds 22 artifacts to their pinned commit, path
and digest. All remain pending rights acceptance; these records do not increase the
rights-cleared numerator. Model-repo's CODE_OF_CONDUCT.md attributes Contributor
Covenant 2.0, while CONTRIBUTING.md attributes 1.4. The governance template's
CODE_OF_CONDUCT.md attributes 2.1. A repository MIT or CC BY declaration is not
substituted for verification of these inherited passages.

The linked version pages were checked live, not added to the six-source pinned corpus:
[1.4](https://www.contributor-covenant.org/version/1/4/code-of-conduct/),
[2.0](https://www.contributor-covenant.org/version/2/0/code_of_conduct/), and
[2.1](https://www.contributor-covenant.org/version/2/1/code_of_conduct/).
Current website footers do not resolve historical licensing or modifications in the
pinned source adaptations. Verify version-specific license history, preserve required
attribution, reconcile the template's conflicting declarations, and record the
authorized distribution decision before approving copies of inherited expression.

The complete pinned Docs README, LICENSE and LICENSE-CODE were subsequently read.
Their 51 independently phrased observations are in
`evidence/source-reviews/docs-root-rights-claims.json`. Documentation/assets/content/data
and code remain separately declared license scopes; no file-specific exceptions,
third-party authority, publisher trademarks or adapted-material distribution are
cleared by this review. These observations are not legal advice or permission to
publish. Rights-cleared coverage remains zero.

## Complete per-artifact work queue

```sh
python -m ges.rights --artifacts .cache/corpus/artifacts.jsonl --findings evidence/rights-review-queue.json --output .cache/corpus/rights-triage.json
```

The triage queue covers all 13,657 pinned artifacts, retaining the 22 existing
file-specific findings. It checks source pins, artifact uniqueness and finding
digests. Unreviewed files have no inferred repository license. Every record
remains pending: this queue neither grants rights nor authorizes distribution.
The workflow queue stays in the ignored cache; its generator and tests are tracked.
Actual clearance requires file-specific grants, exceptions, permitted-use decisions
and attribution duties, plus the applicable authorized distribution decision.
Published bodies need separate version and rights reconciliation; this pinned
artifact queue does not cover that denominator.

## Contributor Covenant historical evidence

Historical upstream evidence now narrows the inherited-text question. At commit
`91532d80ea5f39b6685aff4892bc6854bf2f6d6f` (2022-01-10), the upstream
[README license section](https://github.com/EthicalSource/contributor_covenant/blob/91532d80ea5f39b6685aff4892bc6854bf2f6d6f/README.md)
declares Contributor Covenant under CC BY 4.0 and links its
[license](https://github.com/EthicalSource/contributor_covenant/blob/91532d80ea5f39b6685aff4892bc6854bf2f6d6f/LICENSE.md).
The same commit's tree contains English versions
[1.4](https://github.com/EthicalSource/contributor_covenant/blob/91532d80ea5f39b6685aff4892bc6854bf2f6d6f/content/version/1/4/code-of-conduct.md),
[2.0](https://github.com/EthicalSource/contributor_covenant/blob/91532d80ea5f39b6685aff4892bc6854bf2f6d6f/content/version/2/0/code_of_conduct.md), and
[2.1](https://github.com/EthicalSource/contributor_covenant/blob/91532d80ea5f39b6685aff4892bc6854bf2f6d6f/content/version/2/1/code_of_conduct.md).
Their Git blob IDs observed through the upstream tree API are respectively
`a18dd4b3a25e8280eddee11790375ce6968fea7f`,
`8f34868eff556be879f81c908ecff3e4ec9a8ee7`, and
`f346f0b123e2e3de1a20ef0225af7c6c91747b81`.
The earlier
[2016 license revision](https://github.com/EthicalSource/contributor_covenant/blob/519ee05a2a6c888129d5318db60893a8238f5c96/LICENSE.md)
also identifies CC BY 4.0. This evidence is external licensing support, not a
seventh adopted corpus or an instruction to execute the upstream build process.

Remaining adjudication is narrower than an unknown historic repository license:
compare each pinned adaptation to its declared version, identify adapter additions
and their grants, preserve attribution and modification disclosures, and verify
the intended distribution's compliance. Do not use the current site-source
Hippocratic license or Contributor Covenant 3.0's CC BY-SA notice to retroactively
relabel these older texts. No per-file clearance numerator changes from this
historical declaration alone.
