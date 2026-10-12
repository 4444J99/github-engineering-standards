"""One bounded, source-only replay. No live pages or reconciliation issuance."""
from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timezone
import gzip
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT))
from ges.sources import acquire_source
from ges.pinned_sources import inventory_digest, verify_snapshot

HEAD = '6c37fe5eb98039341cb49444305703dc43048685'
A3_SHA = '05dab95bfbc88c2401a97da702339f4f1be89545c8f8c9f48198194aac07bb15'
PROVENANCE_SHA = '239fc3e89643202c9a7935749249eb4a0ca14e67a32c6e2a0517166a81e9bbf8'
WORK = ROOT / '.cache/cloud-replay-20261012/fresh-pinned'
WORK.mkdir(mode=0o700, exist_ok=False)
SOURCES = WORK / 'sources'
SOURCES.mkdir(mode=0o700)
os.umask(0o077)
for name in ('GH_TOKEN', 'GITHUB_TOKEN'):
    os.environ.pop(name, None)


def stamp():
    return datetime.now(timezone.utc).isoformat()


def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def dump(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')


def event(stage, **fields):
    print(json.dumps({'observed_at': stamp(), 'stage': stage, **fields}), flush=True)


def closure():
    paths = list(ROOT.glob('ges/**/*.py')) + list((ROOT / 'evidence/source-reviews').glob('*-claims.json'))
    paths += [ROOT / name for name in (
        'sources/sources.lock.json', 'controls/catalog.json', 'controls/review_queue.json',
        'evidence/source-review-policy.json', 'evidence/a3-six-source-capsule-repair.json',
        'evidence/claim-workload-current-provenance.json',
        'evidence/claim-workload-inputs/artifacts.jsonl.gz',
        'evidence/claim-workload-v02-inventory.json',
        'evidence/v02-finish-20261010/claim-migration-audit.json')]
    return {str(path.relative_to(ROOT)): sha(path) for path in sorted(paths)}


def run_json(name, argv):
    started = stamp()
    tick = time.monotonic()
    logfile = WORK / (name + '.log')
    with logfile.open('wb') as stream:
        result = subprocess.run(argv, cwd=ROOT, stdout=stream, stderr=subprocess.STDOUT, check=False)
    observation = {'name': name, 'argv': argv, 'started_at': started,
                   'elapsed_seconds': round(time.monotonic() - tick, 3),
                   'exit_code': result.returncode, 'log_sha256': sha(logfile)}
    record['commands'].append(observation)
    dump(WORK / 'execution.json', record)
    if result.returncode:
        raise RuntimeError(name + ' failed; retained output: ' + str(logfile))
    result = json.loads(logfile.read_text())
    if result.get('valid') is not True:
        raise ValueError(name + ' did not report valid=true')
    return result


record = {'schema': 'ges.fresh-cloud-claim-replay.v1', 'started_at': stamp(),
          'head': HEAD, 'executor': 'current cloud Linux workspace',
          'scope': 'FRESH_PINNED_SOURCE_REPLAY_WITH_PRESERVED_OCT7_ARTIFACT_METADATA',
          'historical_original_cache_restored': False,
          'rendered_cache_authenticated': False, 'replacement_envelopes_issued': False,
          'new_semantic_review_credit': 0, 'new_reconciliation_credit': 0,
          'native_host_execution': False, 'sources': [], 'commands': []}
try:
    assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip() == HEAD
    assert not subprocess.check_output(['git', 'status', '--porcelain=v1', '--untracked-files=no'], text=True)
    before = closure()
    dump(WORK / 'input-closure-before.json', before)
    a3_path = ROOT / 'evidence/a3-six-source-capsule-repair.json'
    provenance_path = ROOT / 'evidence/claim-workload-current-provenance.json'
    assert sha(a3_path) == A3_SHA and sha(provenance_path) == PROVENANCE_SHA
    a3, provenance = json.loads(a3_path.read_text()), json.loads(provenance_path.read_text())
    lock_path = ROOT / 'sources/sources.lock.json'
    assert sha(lock_path) == a3['capsule_manifest']['source_lock_sha256']
    specs = json.loads(lock_path.read_text())['sources']
    artifact_gz = ROOT / 'evidence/claim-workload-inputs/artifacts.jsonl.gz'
    assert sha(artifact_gz) == provenance['bindings']['compressed_artifact_inventory_sha256']
    with gzip.open(artifact_gz, 'rb') as stream:
        raw = stream.read(provenance['metadata_projection']['uncompressed_bytes'] + 1)
    assert len(raw) == provenance['metadata_projection']['uncompressed_bytes']
    assert hashlib.sha256(raw).hexdigest() == provenance['bindings']['artifact_inventory_sha256']
    artifacts = WORK / 'artifacts.oct7.jsonl'
    artifacts.write_bytes(raw)
    grouped = defaultdict(list)
    for line in raw.splitlines():
        row = json.loads(line)
        grouped[row['source']].append(row)
    del raw
    assert set(grouped) == {spec['repository'] for spec in specs}
    assert sum(map(len, grouped.values())) == a3['capsule_manifest']['accounting']['inventory_artifacts']
    for spec in specs:
        repo = spec['repository']
        assert len(grouped[repo]) == spec['artifacts']
        assert inventory_digest(grouped[repo]) == a3['inventory_identity_digests'][repo]
    record['artifact_inventory_sha256'] = sha(artifacts)
    record['artifact_rows'] = sum(map(len, grouped.values()))
    record['text_artifacts_authenticated'] = 0
    for spec in sorted(specs, key=lambda item: item['archive_bytes']):
        repo, commit = spec['repository'], spec['commit']
        event('ACQUIRE', repository=repo, archive_bytes=spec['archive_bytes'])
        tick = time.monotonic()
        acquired = acquire_source(spec, SOURCES)
        slug = repo.replace('/', '__')
        inventory_path = SOURCES / (slug + '.inventory.json')
        snapshot_path = SOURCES / (slug + '.text.jsonl.gz')
        inventory = json.loads(inventory_path.read_text())
        assert len(inventory) == spec['artifacts']
        assert inventory_digest(inventory) == a3['inventory_identity_digests'][repo]
        assert acquired['git_tree_reconciliation']['status'] == 'MATCH'
        assert acquired['git_tree_reconciliation']['git_tree_artifacts'] == spec['artifacts']
        verify_snapshot(snapshot_path, grouped[repo], repo, commit)
        count = sum(row['kind'] == 'text' for row in inventory)
        record['text_artifacts_authenticated'] += count
        observation = {**acquired, 'inventory_identity_digest': inventory_digest(inventory),
                       'inventory_file_sha256': sha(inventory_path),
                       'snapshot_sha256': sha(snapshot_path), 'snapshot_bytes': snapshot_path.stat().st_size,
                       'complete_text_coverage_authenticated': True,
                       'elapsed_seconds': round(time.monotonic() - tick, 3)}
        record['sources'].append(observation)
        dump(WORK / 'execution.json', record)
        event('SOURCE_AUTHENTICATED', repository=repo, text_artifacts=count)
    record['source_input_hashes_before_replay'] = {
        str(path.relative_to(WORK)): sha(path) for path in sorted(SOURCES.iterdir())}
    claim_files = sorted((ROOT / 'evidence/source-reviews').glob('*-claims.json'))
    record['claim_documents'] = len(claim_files)
    common = ['--artifacts', str(artifacts), '--sources', str(SOURCES),
              '--reviews', 'evidence/source-reviews', '--review-policy', 'evidence/source-review-policy.json']
    event('REPLAY', claim_documents=len(claim_files))
    provenance_result = run_json('claim-provenance', [sys.executable, '-m', 'ges.claim_review', *common])
    reconciliation = run_json('current-reconciliation-without-envelopes',
                              [sys.executable, '-m', 'ges.claim_reconciliation', *common])
    assert len(provenance_result['review_documents']) == len(claim_files)
    assert provenance_result['reference_claims'] == reconciliation['known_claim_denominator'] == 61941
    assert len(claim_files) == 655
    expected = json.loads((ROOT / 'evidence/v02-finish-20261010/claim-migration-audit.json').read_text())
    assert reconciliation['claim_input_digest'] == expected['current_claim_input_digest']
    assert reconciliation['validated_count'] == 0 and reconciliation['unresolved_count'] == 61941
    assert reconciliation['claim_provenance_validated'] is True
    record['source_input_hashes_after_replay'] = {
        str(path.relative_to(WORK)): sha(path) for path in sorted(SOURCES.iterdir())}
    assert record['source_input_hashes_before_replay'] == record['source_input_hashes_after_replay']
    assert sha(artifacts) == provenance['bindings']['artifact_inventory_sha256']
    after = closure()
    dump(WORK / 'input-closure-after.json', after)
    assert before == after
    assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip() == HEAD
    record.update(status='PASS', completed_at=stamp(), claim_input_digest=reconciliation['claim_input_digest'],
                  known_claim_denominator=61941, validated_current_receipts=0,
                  input_closure_unchanged=True, source_inputs_unchanged=True,
                  full_current_claim_source_provenance_replayed=True,
                  source_to_claim_omission_completeness_certified=False,
                  original_a3_capsule_fully_authenticated=False,
                  historical_validated_dispositions_preserved=2164)
    event('COMPLETE', known_claim_denominator=61941, claim_input_digest=record['claim_input_digest'])
except BaseException as exc:
    record.update(status='FAIL', completed_at=stamp(), error_type=type(exc).__name__, error=str(exc))
    dump(WORK / 'execution.json', record)
    raise
dump(WORK / 'execution.json', record)
