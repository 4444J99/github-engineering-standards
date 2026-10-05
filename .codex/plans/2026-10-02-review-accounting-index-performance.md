# Review accounting index performance

Issue: https://github.com/4444J99/github-engineering-standards/issues/12

Benchmark full pinned accounting before and after replacing per-receipt scans of all candidates with one artifact-to-candidate index. Preserve exact result digest, denominators, errors and safety checks. Record three timing samples per implementation with honest scope (accounting only, not semantic throughput). Add observable own-artifact/foreign-artifact regression cases; run unittest/validate/compile plus recovery. Commit/push every authored artifact and post receipts; no completion or gate claims from speed.
