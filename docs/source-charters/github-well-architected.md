# Source charter: github/github-well-architected

Status: proposed; owner approval pending.
Pin: `a30275bc2d7eb860e612f93cbc1f26d0ff20c0c7`.

## Declared intention and audience

The framework supplies community-driven, opinionated guidance for organizations
adopting GitHub, including strategic principles, recommendations and self-service
assessments. Five pillars organize productivity, collaboration, application
security, governance and architecture.
Evidence: [README, lines 12–21](https://github.com/github/github-well-architected/blob/a30275bc2d7eb860e612f93cbc1f26d0ff20c0c7/README.md#L12-L21),
[overview, lines 5–34](https://github.com/github/github-well-architected/blob/a30275bc2d7eb860e612f93cbc1f26d0ff20c0c7/docs/framework-overview.md#L5-L34),
[pillars, lines 49–59](https://github.com/github/github-well-architected/blob/a30275bc2d7eb860e612f93cbc1f26d0ff20c0c7/docs/framework-overview.md#L49-L59).

## GES interpretation: authority and limits

Use its framework structure and recommendations to organize strategic engineering
practice and assessment questions. Preserve recommendation context and distinguish
principles, recommended actions and assessment evidence.

The source itself distinguishes strategic guidance from GitHub Docs' implementation
details: [overview, lines 105–121](https://github.com/github/github-well-architected/blob/a30275bc2d7eb860e612f93cbc1f26d0ff20c0c7/docs/framework-overview.md#L105-L121).
It cannot override documented platform constraints, prove live compliance or
silently adopt every recommendation as local mandatory policy. Site tooling is
publication infrastructure, not an estate-wide implementation requirement.

## Synthesis obligations

Carry pillar and recommendation provenance into the crosswalk. Determine target
applicability and evidence requirements separately. Record conflicting advice for
reconciliation rather than treating framework breadth as platform certification.
