"""Verify pinned text snapshots against complete source inventories."""
import gzip
import hashlib
import json
import zlib

from .core import digest

IDENTITY_FIELDS = ('source', 'commit', 'path', 'kind', 'sha256',
                   'git_blob_sha', 'size', 'link_target')


def inventory_digest(rows):
    """Bind content identities independently of acquisition timestamps."""
    return digest([{key: row.get(key) for key in IDENTITY_FIELDS}
                   for row in sorted(rows, key=lambda row: row['path'])])


def verify_snapshot(path, inventory, repository, commit, *, retain=()):
    """Stream every row, checking complete coverage; retain only requested text."""
    if not isinstance(inventory, list):
        raise ValueError('Pinned inventory must be an array')
    expected = {}
    for row in inventory:
        if (not isinstance(row, dict) or row.get('source') != repository or
                row.get('commit') != commit or row.get('path') in expected):
            raise ValueError('Invalid or duplicate pinned inventory identity')
        expected[row['path']] = row
    wanted = {key for key, row in expected.items() if row['kind'] == 'text'}
    seen, texts = set(), {}
    retain = set(retain)
    with path.open('rb') as stream:
        snapshot_sha = hashlib.file_digest(stream, 'sha256').hexdigest()
    try:
        with gzip.open(path, 'rt', encoding='utf-8') as stream:
            for line in stream:
                row = json.loads(line)
                if not isinstance(row, dict):
                    raise ValueError('Snapshot row must be an object')
                key = row.get('path')
                original = expected.get(key)
                if (key not in wanted or key in seen or original is None or
                        digest([row.get(field) for field in IDENTITY_FIELDS]) !=
                        digest([original.get(field) for field in IDENTITY_FIELDS])):
                    raise ValueError('Snapshot differs from pinned inventory identity')
                content = row.get('content')
                if not isinstance(content, str):
                    raise ValueError('Snapshot content must be text')
                raw = content.encode('utf-8')
                blob = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
                if (hashlib.sha256(raw).hexdigest() != original['sha256'] or
                        len(raw) != original['size'] or blob != original['git_blob_sha']):
                    raise ValueError('Snapshot content differs from pinned inventory digest')
                seen.add(key)
                if key in retain:
                    texts[key] = content
    except (OSError, EOFError, zlib.error, UnicodeError) as exc:
        raise ValueError('Invalid or truncated pinned gzip snapshot') from exc
    if seen != wanted:
        raise ValueError('Incomplete pinned text-artifact coverage')
    with path.open('rb') as stream:
        if hashlib.file_digest(stream, 'sha256').hexdigest() != snapshot_sha:
            raise ValueError('Pinned snapshot changed during validation')
    return texts
