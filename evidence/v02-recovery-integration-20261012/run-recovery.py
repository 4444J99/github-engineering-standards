"""Bounded Linux recovery execution with local input hash continuity."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import resource
import subprocess
import sys
import time


def sha(path):
    value = hashlib.sha256()
    with path.open('rb') as source:
        for block in iter(lambda: source.read(1048576), b''):
            value.update(block)
    return value.hexdigest()


def closure(root, sources, corpus, receipts, policy):
    groups = {'sources': sources, 'corpus': corpus, 'code': root/'ges',
              'reviews': root/'evidence/source-reviews', 'controls': root/'controls',
              'templates': root/'templates', 'profiles': root/'profiles'}
    files = {}
    for label, directory in groups.items():
        for path in sorted(directory.rglob('*')):
            if any(part.is_symlink() for part in (path, *path.parents)):
                raise ValueError('Symlink input: ' + label)
            if path.is_file() and '__pycache__' not in path.parts:
                files[label+'/'+str(path.relative_to(directory))] = sha(path)
    singles = {'issued-receipts': receipts, 'issued-policy': policy,
               'source-lock': root/'sources/sources.lock.json',
               'review-policy': root/'evidence/source-review-policy.json',
               'rights-queue': root/'evidence/rights-review-queue.json'}
    for label, path in singles.items():
        if any(part.is_symlink() for part in (path, *path.parents)):
            raise ValueError('Symlink input: ' + label)
        files[label] = sha(path)
    # Retain every advertised supporting evidence file, without running it.
    def references(value):
        if isinstance(value, dict):
            for child in value.values():
                yield from references(child)
        elif isinstance(value, list):
            for child in value:
                yield from references(child)
        elif isinstance(value, str) and value.startswith('evidence/') and value.endswith('.json'):
            yield value
    pending = list((root/'evidence/source-reviews').glob('*.json'))
    seen = set()
    while pending:
        path = pending.pop()
        if path in seen:
            continue
        seen.add(path)
        for ref in references(json.loads(path.read_text())):
            relative = Path(ref)
            target = root/relative
            if relative.is_absolute() or '..' in relative.parts:
                raise ValueError('Unsafe supporting evidence reference')
            if any(part.is_symlink() for part in (target, *target.parents)):
                raise ValueError('Symlink supporting evidence')
            if target.is_file():
                files['support/'+ref] = sha(target)
                pending.append(target)
    return dict(sorted(files.items()))


def main():
    parser = argparse.ArgumentParser()
    for name in ('repo', 'sources', 'corpus', 'receipts', 'policy', 'output'):
        parser.add_argument('--'+name, required=True, type=Path)
    args = parser.parse_args()
    root = args.repo.absolute()
    output = args.output.absolute()
    output.mkdir(mode=0o700)
    driver_sha256_before = sha(Path(__file__))
    before = closure(root, args.sources, args.corpus, args.receipts, args.policy)
    (output/'input-closure-before.json').write_text(json.dumps(before, indent=2)+'\n')
    command = [sys.executable, '-m', 'ges.recovery', '--sources', str(args.sources),
               '--corpus', str(args.corpus), '--reviews', 'evidence/source-reviews',
               '--review-policy', 'evidence/source-review-policy.json',
               '--claim-reconciliation', str(args.receipts),
               '--claim-reconciliation-policy', str(args.policy),
               '--output', str(output/'recovery-current.json')]
    code_state = subprocess.check_output(['git', 'status', '--porcelain', '--', 'ges'], cwd=root, text=True)
    def limits():
        resource.setrlimit(resource.RLIMIT_AS, (3*1024**3, 3*1024**3))
        resource.setrlimit(resource.RLIMIT_CPU, (120, 125))
        resource.setrlimit(resource.RLIMIT_FSIZE, (512*1024**2, 512*1024**2))
    start = datetime.now(timezone.utc).isoformat()
    monotonic = time.monotonic()
    timed_out = False
    with (output/'stdout.json').open('wb') as stdout, (output/'stderr.txt').open('wb') as stderr:
        try:
            result = subprocess.run(command, cwd=root, stdout=stdout, stderr=stderr,
                                    timeout=150, preexec_fn=limits)
            exit_code = result.returncode
        except subprocess.TimeoutExpired:
            exit_code = None
            timed_out = True
    elapsed = time.monotonic()-monotonic
    after = closure(root, args.sources, args.corpus, args.receipts, args.policy)
    driver_sha256_after = sha(Path(__file__))
    (output/'input-closure-after.json').write_text(json.dumps(after, indent=2)+'\n')
    record = {'schema': 'ges.recovery-integration-execution.v1', 'started_at': start,
              'completed_at': datetime.now(timezone.utc).isoformat(),
              'elapsed_seconds': round(elapsed, 6), 'command': command,
              'exit_code': exit_code, 'timed_out': timed_out, 'deadline_seconds': 150,
              'limits': {'address_space_bytes': 3*1024**3, 'cpu_seconds': [120, 125]},
              'base_revision': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip(),
              'code_worktree_state': code_state,
              'executed_code_binding': 'code/* entries in the input closure; includes the staged preflight change',
              'driver_sha256': driver_sha256_before,
              'driver_sha256_after': driver_sha256_after,
              'driver_unchanged': driver_sha256_before == driver_sha256_after,
              'input_closure_unchanged': before == after, 'input_files': len(before),
              'input_closure_sha256': sha(output/'input-closure-before.json'),
              'stdout_sha256': sha(output/'stdout.json'), 'stderr_sha256': sha(output/'stderr.txt'),
              'source_acquisition_performed': False, 'receipts_reissued_or_modified': False,
              'rendered_bodies_supplied': False, 'human_acceptance_claimed': False}
    report_path = output/'recovery-current.json'
    if report_path.is_file():
        report = json.loads(report_path.read_text())
        accounting = report['claim_reconciliation_accounting']
        record['recovery_report_sha256'] = sha(report_path)
        record['result'] = {key: accounting[key] for key in
                            ('known_claim_denominator', 'validated_count', 'unresolved_count',
                             'mapping_complete', 'claim_provenance_validated', 'receipts_digest')}
    (output/'execution.json').write_text(json.dumps(record, indent=2)+'\n')
    print(json.dumps({'exit_code': exit_code, 'elapsed_seconds': round(elapsed, 3),
                      'input_closure_unchanged': before == after, 'output': str(output)}))
    if timed_out or exit_code != 0 or before != after or driver_sha256_before != driver_sha256_after:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
