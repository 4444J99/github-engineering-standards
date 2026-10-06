# A3 — Six-source capsule

Freeze the existing six pins, inventories, candidate ledger, dependency ledger,
published page list, structured occurrences, and rendered acquisition identities.
Use the existing metadata-only freeze/validate contract and commit a small receipt
that independently binds the capsule fingerprint and supplement digests.

The initial source cache had an empty dependency ledger inconsistent with its
summary. Rebuild the ledger in an isolated cache copy before freezing; retain the
original cache and initial capsule. Do not retrieve live page lists or change pins.

Acceptance: capsule validation, six matching Git trees, balanced dependency and
structured counts, complete digest-checked rendered acquisition, deterministic
receipt regeneration, frozen-input tests, toolkit tests/validate/compile, and
diff checks. Push one scoped PR from current main independently of PR #472.

The capsule contains metadata only. Pinned source text and rendered bodies remain
in ignored caches. Record remote custody as unverified. Fourteen unresolved page
source mappings and conditional rendering semantics remain explicit downstream
review work. No source charter, semantic interpretation, or control adoption is
part of A3. Retain this checkout and all local caches.
