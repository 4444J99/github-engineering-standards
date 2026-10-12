"""Bounded source-bound accounting using retained inputs; no acquisition or issuance."""
import argparse
import hashlib
import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--retained-work', type=Path, required=True)
p.add_argument('--receipts', type=Path, required=True)
p.add_argument('--output-directory', type=Path, required=True)
a = p.parse_args()
root = Path(__file__).resolve().parents[2]
out = a.output_directory
policy = root / 'evidence/v02-authorized-reconciliation-20261012/claim-reconciliation-policy.json'
execution = json.loads((root / 'evidence/v02-cloud-replay-20261012/execution.v1.json').read_bytes())
reference = execution['source_input_hashes_after_replay']
expected_closure = json.loads((root / 'evidence/v02-cloud-replay-20261012/input-closure-after.json').read_bytes())


def sha(path):
    if not path.is_file() or any(part.is_symlink() for part in (path, *path.parents)):
        raise ValueError('Not a regular nonsymlink file: ' + str(path))
    return hashlib.sha256(path.read_bytes()).hexdigest()


def closure():
    hashes = {name: sha(a.retained_work / name) for name in reference}
    if hashes != reference:
        raise ValueError('Retained source inputs differ from completed cloud replay')
    artifact = sha(a.retained_work / 'artifacts.oct7.jsonl')
    if artifact != execution['artifact_inventory_sha256']:
        raise ValueError('Artifact metadata differs')
    repo = {name: sha(root / name) for name in expected_closure}
    if repo != expected_closure:
        raise ValueError('Replayed repository inputs differ')
    return dict(sources=hashes, artifacts=artifact, repository=repo,
                receipts=sha(a.receipts), policy=sha(policy))


before = closure()
started = datetime.now(timezone.utc).isoformat()
command = [sys.executable, '-m', 'ges.claim_reconciliation',
    '--artifacts', str(a.retained_work / 'artifacts.oct7.jsonl'),
    '--sources', str(a.retained_work / 'sources'),
    '--reviews', 'evidence/source-reviews', '--review-policy', 'evidence/source-review-policy.json',
    '--pins', 'sources/sources.lock.json', '--catalog', 'controls/catalog.json',
    '--proposals', 'controls/review_queue.json', '--receipts', str(a.receipts), '--policy', str(policy)]
tick = time.monotonic()
result = subprocess.run(command, cwd=root, capture_output=True, timeout=60)
elapsed = time.monotonic() - tick
(out / 'current-accounting.json').write_bytes(result.stdout)
(out / 'current-accounting.stderr.txt').write_bytes(result.stderr)
after = closure()
if before != after:
    raise ValueError('Accounting inputs changed')
report = json.loads(result.stdout)
if result.returncode != 0 or report.get('valid') is not True:
    raise ValueError('Accounting did not validate: ' + result.stdout.decode())
record = dict(schema='ges.authorized-accounting-execution.v1', started_at=started,
    completed_at=datetime.now(timezone.utc).isoformat(), actual_seconds=elapsed,
    process_deadline_seconds=60, command=command, code_revision=subprocess.check_output(
        ['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip(), exit_code=result.returncode,
    output_sha256=sha(out / 'current-accounting.json'), stderr_sha256=sha(out / 'current-accounting.stderr.txt'),
    input_closure=before, input_closure_unchanged=True, source_acquisition_repeated=False,
    source_provenance_revalidated_by_accounting=True,
    known_claim_denominator=report['known_claim_denominator'], validated_count=report['validated_count'],
    unresolved_count=report['unresolved_count'], mapping_complete=report['mapping_complete'])
(out / 'accounting-execution.json').write_text(json.dumps(record, indent=2, sort_keys=True)+'\n')
print(json.dumps({key:record[key] for key in ('exit_code','actual_seconds','known_claim_denominator','validated_count','unresolved_count','mapping_complete')}, indent=2))
