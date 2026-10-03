"""Immutable metadata handoff and source-only hydration; never certification.

Raw upstream bytes are fetched into an ignored worker cache, not included in the
metadata capsule. Neither command launches an agent, approves a reviewer or
establishes encrypted remote custody. Trust the capsule fingerprint through an
independent exact-head receipt, not a checksum supplied by the capsule itself.
"""
from __future__ import annotations

import argparse
from collections import Counter
import gzip
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import re
import tarfile
import tempfile

from .core import ROOT, digest, dump, load
from .sources import fetch

SCHEMA = 'ges.frozen-review-inputs.v1'
CORPUS_FILES = ('artifacts.jsonl', 'candidates.jsonl', 'dependencies.jsonl',
                'published-page-ledger.json')
INVENTORY_KEYS = {'source', 'commit', 'path', 'sha256', 'git_blob_sha', 'size',
                  'kind', 'retrieval_status', 'retrieved_at', 'review_status',
                  'url', 'link_target'}
METADATA_KEYS = {
    'artifacts.jsonl': INVENTORY_KEYS | {'artifact_id', 'candidate_count', 'proposed_disposition'},
    'candidates.jsonl': {'artifact_id', 'candidate_id', 'canonical_control_ids', 'commit',
                       'end_line', 'kind', 'normative_signal', 'path', 'reference',
                       'review_status', 'section', 'source', 'start_line', 'text_sha256'},
    'dependencies.jsonl': {'artifact_id', 'kind', 'reference', 'resolution',
                          'resolved_artifact_ids', 'source_line',
                          'value_or_conditional_rendering_verified'},
    'published-page-ledger.json': {'function', 'page_id', 'path', 'reconciliation',
                                  'rendered_body_review', 'review_checklist',
                                  'source_matches', 'version'},
}
MAX_FILE_BYTES = 150_000_000
MAX_TOTAL_BYTES = 256_000_000
TREE_KEYS = {'status', 'git_tree_artifacts', 'archive_artifacts',
             'missing_from_archive', 'extra_in_archive', 'blob_mismatches',
             'reason', 'error_type', 'http_status'}


def _metadata_only(value) -> None:
    if isinstance(value, dict):
        if {'content', 'body', 'text', 'token', 'transcript', 'private_key'} & set(value):
            raise ValueError('Restricted payload field in metadata transport')
        for item in value.values():
            _metadata_only(item)
    elif isinstance(value, list):
        for item in value:
            _metadata_only(item)


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _no_links(path: Path) -> None:
    if any(part.is_symlink() for part in (path, *path.parents)):
        raise ValueError('Symlink input/output is not admitted')


def _read(path: Path) -> bytes:
    _no_links(path)
    if not path.is_file() or path.stat().st_size > MAX_FILE_BYTES:
        raise ValueError('Missing, nonregular or oversized metadata input')
    return path.read_bytes()


def _fresh(path: Path) -> None:
    _no_links(path)
    if path.exists():
        raise FileExistsError('Output must be a new directory')


def _specs(lock: dict) -> dict:
    specs = {}
    for spec in lock['sources']:
        repo, commit = spec['repository'], spec['commit']
        if (not re.fullmatch(r'[\w.-]+/[\w.-]+', repo) or
                not re.fullmatch(r'[a-f0-9]{40}', commit) or repo in specs or
                not re.fullmatch(r'[a-f0-9]{64}', spec['archive_sha256']) or
                type(spec['archive_bytes']) is not int or spec['archive_bytes'] <= 0 or
                type(spec['artifacts']) is not int or spec['artifacts'] <= 0):
            raise ValueError('Invalid or duplicate locked source')
        specs[repo] = spec
    if not specs:
        raise ValueError('Empty source lock')
    return specs


def _names(specs: dict) -> set[str]:
    return {'sources.lock.json', *(f'corpus/{name}' for name in CORPUS_FILES),
            *(f'sources/{repo.replace("/", "__")}.{suffix}.json'
              for repo in specs for suffix in ('inventory', 'tree-reconciliation'))}


def _rows(data: bytes, name: str, allowed: set[str]):
    records = (json.loads(line) for line in data.decode('utf-8').splitlines() if line.strip()) \
        if name.endswith('.jsonl') else iter(json.loads(data))
    for record in records:
        if not isinstance(record, dict) or set(record) - allowed:
            raise ValueError('Unexpected or restricted metadata fields: ' + name)
        _metadata_only(record)
        yield record


def _account(payloads: dict[str, bytes], lock: dict) -> dict:
    specs = _specs(lock)
    inventory = {}
    for repo, spec in specs.items():
        tree = json.loads(payloads[f'sources/{repo.replace("/", "__")}.tree-reconciliation.json'])
        if not isinstance(tree, dict) or set(tree) - TREE_KEYS or 'status' not in tree:
            raise ValueError('Unexpected tree-reconciliation metadata')
        _metadata_only(tree)
        rows = list(_rows(payloads[f'sources/{repo.replace("/", "__")}.inventory.json'],
                          'inventory.json', INVENTORY_KEYS))
        if len(rows) != spec['artifacts']:
            raise ValueError('Frozen inventory differs from locked artifact denominator')
        for row in rows:
            path = PurePosixPath(row['path'])
            identity = (repo, spec['commit'], row['path'])
            if (row['source'] != repo or row['commit'] != spec['commit'] or
                    path.is_absolute() or '..' in path.parts or not path.parts or
                    '\\' in row['path'] or identity in inventory):
                raise ValueError('Invalid, changed or duplicate frozen artifact')
            inventory[identity] = row
    artifacts = {}
    for row in _rows(payloads['corpus/artifacts.jsonl'], 'artifacts.jsonl', METADATA_KEYS['artifacts.jsonl']):
        identity = (row['source'], row['commit'], row['path'])
        original = inventory.get(identity)
        artifact_id = digest(list(identity))[:24]
        if (original is None or row['artifact_id'] != artifact_id or artifact_id in artifacts or
                any(row.get(k) != v for k, v in original.items())):
            raise ValueError('Corpus does not match exact frozen inventories')
        artifacts[artifact_id] = row
    if len(artifacts) != len(inventory):
        raise ValueError('Incomplete frozen corpus inventory')
    candidates, candidate_counts = set(), Counter()
    for row in _rows(payloads['corpus/candidates.jsonl'], 'candidates.jsonl', METADATA_KEYS['candidates.jsonl']):
        candidate_id, artifact = row['candidate_id'], artifacts.get(row['artifact_id'])
        if (not isinstance(candidate_id, str) or not candidate_id or candidate_id in candidates or
                artifact is None or any(row[k] != artifact[k] for k in ('source', 'commit', 'path'))):
            raise ValueError('Invalid frozen candidate identity')
        candidates.add(candidate_id)
        candidate_counts[row['artifact_id']] += 1
    if any(row['candidate_count'] != candidate_counts[key] for key, row in artifacts.items()):
        raise ValueError('Frozen candidate accounting differs from inventory')
    for row in _rows(payloads['corpus/dependencies.jsonl'], 'dependencies.jsonl', METADATA_KEYS['dependencies.jsonl']):
        if (row['artifact_id'] not in artifacts or
                any(key not in artifacts for key in row.get('resolved_artifact_ids', []))):
            raise ValueError('Frozen dependency references unknown artifact')
    pages, routes = set(), set()
    for row in _rows(payloads['corpus/published-page-ledger.json'], 'published-page-ledger.json',
                     METADATA_KEYS['published-page-ledger.json']):
        identity = (row['version'], row['path'])
        if not row['page_id'] or row['page_id'] in pages or identity in routes:
            raise ValueError('Duplicate or empty frozen page identity')
        pages.add(row['page_id'])
        routes.add(identity)
    return {'inventory_artifacts': len(artifacts), 'published_pages': len(pages),
            'candidate_blocks': len(candidates), 'inventory_digest': digest(list(artifacts.values())),
            'published_ledger_sha256': _sha(payloads['corpus/published-page-ledger.json']),
            'semantic_review_performed': False, 'provider_dispatched': False,
            'remote_custody_verified': False}


def freeze(sources: Path, corpus: Path, output: Path, *,
           manifest: Path = ROOT / 'sources/sources.lock.json') -> dict:
    _fresh(output)
    lock_bytes = _read(manifest)
    lock = json.loads(lock_bytes)
    specs = _specs(lock)
    payloads = {'sources.lock.json': lock_bytes}
    for name in _names(specs) - {'sources.lock.json'}:
        relative = PurePosixPath(name)
        root = sources if relative.parts[0] == 'sources' else corpus
        payloads[name] = _read(root / relative.name)
    if sum(map(len, payloads.values())) > MAX_TOTAL_BYTES:
        raise ValueError('Frozen metadata exceeds transport bound')
    report = _account(payloads, lock)
    record = {'schema_version': SCHEMA, 'source_lock_sha256': _sha(lock_bytes),
              'files': {name: {'sha256': _sha(data), 'bytes': len(data)}
                        for name, data in sorted(payloads.items())}, 'accounting': report}
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.ges-freeze-', dir=output.parent) as temporary:
        staging = Path(temporary) / 'capsule'
        staging.mkdir(mode=0o700)
        for name, data in payloads.items():
            target = staging / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
        dump(staging / 'manifest.json', record)
        capsule_sha = _sha((staging / 'manifest.json').read_bytes())
        _fresh(output)
        staging.rename(output)
    return {**report, 'capsule_sha256': capsule_sha}


def _validated(capsule: Path, expected_sha256: str, manifest: Path) -> tuple[dict, dict]:
    if not isinstance(expected_sha256, str) or not re.fullmatch(r'[a-f0-9]{64}', expected_sha256):
        raise ValueError('An independently trusted capsule fingerprint is required')
    data = _read(capsule / 'manifest.json')
    if _sha(data) != expected_sha256:
        raise ValueError('Capsule manifest fingerprint mismatch')
    record = json.loads(data)
    lock_bytes = _read(manifest)
    lock = json.loads(lock_bytes)
    if record['schema_version'] != SCHEMA or record['source_lock_sha256'] != _sha(lock_bytes):
        raise ValueError('Capsule differs from exact approved source lock')
    names = _names(_specs(lock))
    if set(record['files']) != names:
        raise ValueError('Unexpected or missing capsule file')
    _no_links(capsule)
    actual = set()
    for target in capsule.rglob('*'):
        _no_links(target)
        if target.is_file():
            actual.add(target.relative_to(capsule).as_posix())
        elif not target.is_dir():
            raise ValueError('Nonregular capsule member')
    if actual != names | {'manifest.json'}:
        raise ValueError('Capsule contains unmanifested files')
    payloads = {}
    for name in names:
        content = _read(capsule / name)
        if record['files'][name] != {'sha256': _sha(content), 'bytes': len(content)}:
            raise ValueError('Frozen payload digest/size mismatch')
        payloads[name] = content
    if payloads['sources.lock.json'] != lock_bytes or sum(map(len, payloads.values())) > MAX_TOTAL_BYTES:
        raise ValueError('Frozen lock or transport size mismatch')
    accounting = _account(payloads, lock)
    if accounting != record['accounting']:
        raise ValueError('Frozen accounting differs from payloads')
    return payloads, {**accounting, 'capsule_sha256': expected_sha256}


def validate_capsule(capsule: Path, expected_sha256: str, *,
                     manifest: Path = ROOT / 'sources/sources.lock.json') -> dict:
    return _validated(capsule, expected_sha256, manifest)[1]


def hydrate(capsule: Path, expected_sha256: str, partition: dict, output: Path, *,
            manifest: Path = ROOT / 'sources/sources.lock.json') -> dict:
    _fresh(output)
    payloads, accounting = _validated(capsule, expected_sha256, manifest)
    if (not isinstance(partition, dict) or set(partition) != {'schema_version', 'capsule_sha256', 'artifact_ids'} or
            partition['schema_version'] != 'ges.review-partition.v1' or
            partition['capsule_sha256'] != expected_sha256 or
            not isinstance(partition['artifact_ids'], list) or not partition['artifact_ids'] or
            any(not isinstance(key, str) for key in partition['artifact_ids']) or
            len(set(partition['artifact_ids'])) != len(partition['artifact_ids'])):
        raise ValueError('Invalid or changed review partition')
    artifacts = {row['artifact_id']: row for row in _rows(payloads['corpus/artifacts.jsonl'],
                 'artifacts.jsonl', METADATA_KEYS['artifacts.jsonl'])}
    if any(key not in artifacts for key in partition['artifact_ids']):
        raise ValueError('Partition artifact absent from frozen inventory')
    assigned = {key: artifacts[key] for key in partition['artifact_ids']}
    specs = _specs(json.loads(payloads['sources.lock.json']))
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.ges-hydrate-', dir=output.parent) as temporary:
        staging = Path(temporary) / 'worker'
        staging.mkdir(mode=0o700)
        for name, data in payloads.items():
            target = staging / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
        hydrated = set()
        for repo in sorted({row['source'] for row in assigned.values()}):
            spec = specs[repo]
            url = f'https://codeload.github.com/{repo}/tar.gz/{spec["commit"]}'
            raw_archive = fetch(url, expected_sha256=spec['archive_sha256'])
            if len(raw_archive) != spec['archive_bytes'] or _sha(raw_archive) != spec['archive_sha256']:
                raise ValueError('Assigned source archive differs from lock')
            wanted = {row['path']: row for row in assigned.values() if row['source'] == repo}
            textfile = staging / 'sources' / (repo.replace('/', '__') + '.text.jsonl.gz')
            with tarfile.open(fileobj=io.BytesIO(raw_archive), mode='r:gz') as archive, \
                    gzip.open(textfile, 'wt', encoding='utf-8') as texts:
                for member in archive:
                    parts = PurePosixPath(member.name).parts
                    if member.name.startswith('/') or '..' in parts:
                        raise ValueError('Unsafe archive member')
                    path = '/'.join(parts[1:])
                    if path not in wanted:
                        continue
                    row = wanted[path]
                    if row['artifact_id'] in hydrated or not member.isfile() or member.size != row['size']:
                        raise ValueError('Duplicate, nonregular or changed assigned source')
                    stream = archive.extractfile(member)
                    raw = stream.read(member.size + 1)
                    if len(raw) != row['size'] or _sha(raw) != row['sha256']:
                        raise ValueError('Assigned artifact digest differs from frozen inventory')
                    if row['kind'] == 'text':
                        content = raw.decode('utf-8')
                        if '\0' in content:
                            raise ValueError('Text artifact contains binary data')
                        texts.write(json.dumps({**row, 'content': content}, ensure_ascii=False) + '\n')
                    else:
                        # Review binary bytes as evidence; never execute or auto-dispose them.
                        asset = staging / 'assets' / row['artifact_id']
                        asset.parent.mkdir(parents=True, exist_ok=True)
                        asset.write_bytes(raw)
                    hydrated.add(row['artifact_id'])
        if hydrated != set(assigned):
            raise ValueError('Assigned archive artifacts missing')
        report = {**accounting, 'assigned_artifacts': len(hydrated), 'partition_sha256': digest(partition),
                  'source_lock_sha256': _sha(payloads['sources.lock.json']),
                  'raw_sources_are_restricted_cache': True}
        dump(staging / 'hydration-report.json', report)
        _fresh(output)
        staging.rename(output)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    freezing = sub.add_parser('freeze')
    freezing.add_argument('--sources', type=Path, required=True)
    freezing.add_argument('--corpus', type=Path, required=True)
    freezing.add_argument('--output', type=Path, required=True)
    for verb in ('validate', 'hydrate'):
        command = sub.add_parser(verb)
        command.add_argument('--capsule', type=Path, required=True)
        command.add_argument('--capsule-sha256', required=True)
        if verb == 'hydrate':
            command.add_argument('--partition', type=Path, required=True)
            command.add_argument('--output', type=Path, required=True)
    parser.add_argument('--pins', type=Path, default=ROOT / 'sources/sources.lock.json')
    args = parser.parse_args()
    try:
        if args.command == 'freeze':
            report = freeze(args.sources, args.corpus, args.output, manifest=args.pins)
        elif args.command == 'validate':
            report = validate_capsule(args.capsule, args.capsule_sha256, manifest=args.pins)
        else:
            report = hydrate(args.capsule, args.capsule_sha256, load(args.partition), args.output, manifest=args.pins)
    except (OSError, ValueError, KeyError, TypeError, tarfile.TarError) as exc:
        print(json.dumps({'valid': False, 'error': str(exc)}))
        return 2
    print(json.dumps(report))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
