# Pinned-source reread, correction wave 01

This directory records the separate, bounded source-byte reread requested after
the B/C/D/E evidence was brought onto one A integration head.

`source-byte-reread-CORRECTION-01.json` binds the authenticated retained cache,
the exact pinned source document, the newline-terminated bytes for lines 21, 27,
31, 41, and 42, and the five statement-level successor records. The checker
recomputes the cache snapshot digest, authentication binding, full content
digest, exact line bytes, successor statement digests, and B/C/D/E exclusive-root
tree identities.

Replay from the repository root with the retained private cache path:

```sh
python evidence/wave-20261009-correction-01/source-reread/check-source-reread-correction-01.py \
  --cache-snapshot /absolute/path/to/github__github-well-architected.text.jsonl.gz
```

The reread retires only the later-stage limitation that the five corrected
statements had not been checked against the pinned bytes. It does not rewrite the
historically accurate B records, create a reconciliation receipt, accept a
decision, change a mapping or policy, establish authority/enforcement/cadence,
clear either publication field, grant approval, run the heavy suite, merge the
PR, or make the work `Verified`. Status remains **Staged**.
