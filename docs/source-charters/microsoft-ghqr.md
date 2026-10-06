# Source charter: microsoft/ghqr

Status: proposed; owner approval pending.
Pin: `02b89961921ac43f93aa8b3ff74cdcb7cd3d9244`.

## Declared intention and audience

GHQR is a CLI assessment tool for enterprises, organizations and repositories,
intended to identify security and configuration gaps and produce prioritized
findings and reports for administrators and reviewers.
Evidence: [README, lines 5–51](https://github.com/microsoft/ghqr/blob/02b89961921ac43f93aa8b3ff74cdcb7cd3d9244/README.md#L5-L51).

## GES interpretation: authority and limits

Use source-defined checks, scanner predicates, reports and manual-check guidance
as evidence of GHQR's intended and implemented assessment behavior. Distinguish
documented aspirations from actual evaluator predicates; implementation still
requires later source-level review. No upstream code was executed for this charter.

Manual guidance explicitly identifies automation and data limitations, including
partial batch evaluation and checks that require UI inspection:
[manual checks, lines 1–15](https://github.com/microsoft/ghqr/blob/02b89961921ac43f93aa8b3ff74cdcb7cd3d9244/.github/skills/ghqr-report/references/MANUAL_CHECKS.md#L1-L15),
[manual checks, lines 129–137](https://github.com/microsoft/ghqr/blob/02b89961921ac43f93aa8b3ff74cdcb7cd3d9244/.github/skills/ghqr-report/references/MANUAL_CHECKS.md#L129-L137).
Missing observations, limited access and unimplemented checks cannot be converted
to PASS. Tool severity is not automatically GES policy severity; scanner output
does not prove exhaustive compliance or native enforcement.

## Synthesis obligations

Preserve each check's target scope, data dependency and evaluator limitation.
Separate automatic, manual and unsupported evidence paths. Compare GitHub
mechanics with Docs and require explicit adoption of any resulting local rule.
