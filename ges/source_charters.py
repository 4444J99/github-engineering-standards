"""Replay charter provenance; does not approve charters or semantic claims."""
import argparse
import hashlib
import json
import re
from pathlib import Path

from ges.structured_review import validate_pinned_span
from ges.pinned_sources import inventory_digest, verify_snapshot


def validate_manifest(root: Path, sources: Path | None = None, *,
                      capsule_receipt: Path | None = None,
                      capsule_sha256: str | None = None,
                      receipt_sha256: str | None = None) -> dict:
    manifest = json.loads((root / 'evidence/a4-source-charters.json').read_text())
    pins = {s['repository']: s['commit'] for s in
            json.loads((root / 'sources/sources.lock.json').read_text())['sources']}
    rows = manifest['citations']
    if not rows or {r['repository'] for r in rows} != set(pins):
        raise ValueError('Charter source set mismatch')
    if manifest['status'] != 'PROPOSED_REQUIRES_OWNER_APPROVAL':
        raise ValueError('Charter approval must remain pending')
    expected = set()
    for doc in (root / 'docs/source-charters').glob('*.md'):
        for repo, commit, path, start, end in re.findall(
                r'https://github.com/([^/]+/[^/]+)/blob/([a-f0-9]{40})/'
                r'([^)#]+)#L(\d+)-L(\d+)', doc.read_text()):
            expected.add((str(doc.relative_to(root)), repo, commit, path,
                          int(start), int(end)))
    actual = set()
    needed = set()
    for row in rows:
        if row['commit'] != pins[row['repository']]:
            raise ValueError('Charter pin mismatch')
        identity = tuple(row[k] for k in ('charter', 'repository', 'commit',
                                          'path', 'start_line', 'end_line'))
        if identity in actual:
            raise ValueError('Duplicate charter citation')
        actual.add(identity)
        needed.add((row['repository'], row['commit'], row['path']))
        if 'file_sha256' in row:
            raise ValueError('Use canonical content_sha256')
        for key in ('content_sha256', 'span_sha256'):
            if not re.fullmatch('[a-f0-9]{64}', row[key]):
                raise ValueError('Invalid charter digest')
    if actual != expected:
        raise ValueError('Charter locator set mismatch')
    if sources is not None:
        if (capsule_receipt is None or not isinstance(capsule_sha256, str) or
                not isinstance(receipt_sha256, str)):
            raise ValueError('Independently trusted A3 capsule receipt and fingerprint required')
        baseline_bytes = capsule_receipt.read_bytes()
        if (hashlib.sha256(baseline_bytes).hexdigest() != receipt_sha256 or
                manifest.get('a3_receipt_sha256') != receipt_sha256):
            raise ValueError('A3 receipt bytes differ from trusted fingerprint')
        baseline = json.loads(baseline_bytes)
        if baseline.get('schema') != 'ges.a3-capsule-receipt.v2':
            raise ValueError('A3 repaired receipt schema required')
        if (baseline.get('capsule_sha256') != capsule_sha256 or
                manifest.get('a3_capsule_sha256') != capsule_sha256):
            raise ValueError('A3 capsule fingerprint differs from trusted baseline')
        capsule_manifest = baseline['capsule_manifest']
        manifest_bytes = (json.dumps(capsule_manifest, indent=2, sort_keys=True)+'\n').encode()
        if hashlib.sha256(manifest_bytes).hexdigest() != capsule_sha256:
            raise ValueError('A3 capsule manifest fingerprint mismatch')
        lock_sha = hashlib.sha256((root / 'sources/sources.lock.json').read_bytes()).hexdigest()
        if capsule_manifest['source_lock_sha256'] != lock_sha:
            raise ValueError('Charters differ from trusted A3 source lock')
        if set(baseline['inventory_identity_digests']) != set(pins):
            raise ValueError('Incomplete A3 inventory identity baseline')
        texts = {}
        for repo in sorted(pins):
            slug = repo.replace('/', '__')
            inventory = json.loads((sources / (slug+'.inventory.json')).read_text())
            if inventory_digest(inventory) != baseline['inventory_identity_digests'][repo]:
                raise ValueError('Source inventory differs from trusted A3 capsule')
            retained = verify_snapshot(sources / (slug+'.text.jsonl.gz'), inventory,
                                       repo, pins[repo], retain={
                                           path for repository, _, path in needed if repository == repo})
            texts.update({(repo, pins[repo], path): content
                          for path, content in retained.items()})
        if set(texts) != needed:
            raise ValueError('Missing pinned source artifacts')
        for row in rows:
            validate_pinned_span(texts[(row['repository'], row['commit'], row['path'])], row)
    return {'valid': True, 'citations': len(rows),
            'source_bytes_replayed': sources is not None,
            'capsule_sha256': capsule_sha256 if sources is not None else None,
            'a3_receipt_sha256': receipt_sha256 if sources is not None else None,
            'a3_owner_acceptance_verified': False, 'owner_approved': False,
            'scope': 'PROVENANCE_REPLAY_ONLY' if sources is not None else 'LOCATORS_ONLY'}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path('.'))
    parser.add_argument('--sources', type=Path, required=True)
    parser.add_argument('--capsule-receipt', type=Path, required=True)
    parser.add_argument('--capsule-sha256', required=True)
    parser.add_argument('--receipt-sha256', required=True)
    args = parser.parse_args()
    print(json.dumps(validate_manifest(args.root, args.sources,
                                     capsule_receipt=args.capsule_receipt,
                                     capsule_sha256=args.capsule_sha256,
                                     receipt_sha256=args.receipt_sha256)))


if __name__ == '__main__':
    main()
