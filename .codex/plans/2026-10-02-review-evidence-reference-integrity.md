# Review evidence reference integrity

Issue: https://github.com/4444J99/github-engineering-standards/issues/9

Accounting ignores advertised supporting evidence paths. Reproduce missing-evidence false completeness first, then enforce readable nonempty JSON objects/arrays under repository-relative evidence paths, excluding parent/absolute paths and symlink escape. Validate all existing references without weakening gates. Add negative cases, run full unittest/validate/compile plus recovery, and commit/push all changes with exact receipts. Presence/integrity does not prove semantic truth, independent review quality or licensing.
