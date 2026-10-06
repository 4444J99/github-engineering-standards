# A3 review repair

Address the owner's independent review of PR #475 at 8d46cf1. Require an
independently supplied structured-occurrence count; reject coordinated row and
summary removal. Add a CI check tying the committed receipt to the source lock
and its manifest fingerprint. Explain historical source-lock tree flags, repair
the command formatting, and link the documentation from README.

Validate the new regression, full suite, catalog, generated views, receipt
reproduction, and diff. Push the repaired PR head and submit it once through the
existing merge rail under the owner's conditional approval. Do not represent
the prior approval as a GitHub review of the repaired commit or claim Verified
before merged-main and organization acceptance gates are satisfied.
