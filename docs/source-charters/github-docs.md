# Source charter: github/docs

Status: proposed; owner approval pending.
Pin: `56fcfa816f27bca239e5d39fff0d4f74f77ec995`.

## Declared intention and audience

The repository supports GitHub's documentation site and contributions to its
content. Its English Markdown content, version metadata and reusable data support
product documentation for GitHub users and documentation contributors.
Evidence: [README, lines 3–22](https://github.com/github/docs/blob/56fcfa816f27bca239e5d39fff0d4f74f77ec995/README.md#L3-L22),
[content conventions, lines 1–59](https://github.com/github/docs/blob/56fcfa816f27bca239e5d39fff0d4f74f77ec995/content/README.md#L1-L59),
[data conventions, lines 1–37](https://github.com/github/docs/blob/56fcfa816f27bca239e5d39fff0d4f74f77ec995/data/README.md#L1-L37).

## GES interpretation: authority and limits

Use the pinned official documentation as the primary source for documented
GitHub behavior, capabilities, constraints and implementation procedures.
Preserve product, version, plan, role, permission and conditional qualifications.
Content pages express documentation; frontmatter determines applicability;
reusables and variables contribute meaning; site code supports publication and is
not itself a universal engineering obligation.

Documentation does not establish live target configuration, exhaustive capability
coverage, current behavior after the pin, local policy adoption or redistribution
permission. A documented possibility is not a mandatory local requirement.

## Synthesis and upstream contribution boundary

Formalization must retain exact language and locators, distinguish descriptive
facts from instructions, and resolve reusable/version dependencies explicitly.
Ambiguity remains unresolved evidence until reviewed, not a guessed predicate.

The README permits external content and selected data contributions but excludes
infrastructure, workflow and site-build changes from that channel. Reproducible
content defects discovered during formalization may warrant separate upstream
proposals; GES-specific controls and compiler changes do not automatically qualify.
No verified upstream contribution candidate is asserted by this charter.
