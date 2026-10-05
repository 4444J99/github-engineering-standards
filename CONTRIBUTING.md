# Contributing

Use a focused issue and pull request for substantive changes. Preserve source commit/path/section/hash provenance and describe which unique requirement is added, generalized, specialized, superseded or rejected.

## Development

Use Python 3.11+ from the repository root. Install requirements.txt in a virtual environment. Run `python -m unittest discover -s tests -v`; then `python -m ges validate` and `python -m ges compile`.

## Control changes

Edit controls/catalog.json, increment the affected control revision, preserve old evidence as historical, and regenerate functional-checklist.md, source-crosswalk.md and bindings.json. Changes to a checker require positive, negative, unknown, unavailable and stale-evidence tests. A source pin change reopens affected review work.

## Review

Provide exact verification commands, output and target revision. State which claims remain unverified. Do not convert draft or incomplete work into passing compliance. Source acquisition and semantic review are separate deliverables. No actual workload or commit quota defines quality.

## Sensitive reports

Follow SECURITY.md; never include credentials or private records in issues or artifacts.
