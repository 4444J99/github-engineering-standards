"""Preserve and invalidate the two known legacy heuristic artifacts."""
import argparse
import hashlib
import json
import shutil
from pathlib import Path


def disposition_rows(path):
    """Read the legacy top-level array incrementally."""
    decoder = json.JSONDecoder()
    with path.open() as stream:
        buffer = ''
        started = False
        eof = False
        while True:
            if not eof:
                chunk = stream.read(65536)
                eof = not chunk
                buffer += chunk
            buffer = buffer.lstrip()
            if not started:
                if not buffer.startswith('['):
                    raise ValueError('Expected legacy disposition array')
                buffer = buffer[1:]
                started = True
            while True:
                buffer = buffer.lstrip()
                if buffer.startswith(','):
                    buffer = buffer[1:].lstrip()
                if buffer.startswith(']'):
                    return
                try:
                    row, end = decoder.raw_decode(buffer)
                except json.JSONDecodeError:
                    if eof:
                        raise ValueError('Incomplete disposition array')
                    break
                yield row
                buffer = buffer[end:]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--checkout', type=Path, required=True)
    parser.add_argument('--commit-delete', action='store_true',
                        help='Explicitly remove active originals after verified preservation')
    parser.add_argument('--validate', action='store_true',
                        help='Reverify existing quarantine against its receipt')
    parser.add_argument('--export-custody', type=Path,
                        help='Copy existing quarantine outside the checkout; never overwrite')
    args = parser.parse_args()
    root = args.checkout.resolve()
    paths = ['scripts/semantic_review.py', 'evidence/semantic-review-dispositions.json']
    destination = root / '.cache/quarantine/a1-legacy-semantic-review'
    if args.validate or args.export_custody:
        receipt = json.loads((destination / 'receipt.json').read_text())
        for record in receipt['artifacts']:
            relative = Path(record['original_path'])
            if relative.is_absolute() or '..' in relative.parts:
                raise ValueError('Unsafe receipt path')
            target = destination / relative
            if target.is_symlink() or not target.is_file():
                raise ValueError('Missing or symlinked quarantine artifact')
            raw = target.read_bytes()
            if len(raw) != record['bytes'] or hashlib.sha256(raw).hexdigest() != record['sha256']:
                raise ValueError('Quarantine digest mismatch')
        if args.export_custody:
            export = args.export_custody.resolve()
            if export.is_relative_to(root) or export.exists():
                raise ValueError('Custody must be a new directory outside checkout')
            export.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
            export.parent.chmod(0o700)
            shutil.copytree(destination, export)
            for directory in [export, *[p for p in export.rglob('*') if p.is_dir()]]:
                directory.chmod(0o700)
            for record in receipt['artifacts']:
                if hashlib.sha256((export / record['original_path']).read_bytes()).hexdigest() != record['sha256']:
                    raise ValueError('External custody digest mismatch')
        print(json.dumps({'quarantine_valid': True, 'certification_evidence': False}))
        return
    if not args.commit_delete:
        print(json.dumps({'dry_run': True, 'original_paths': paths,
                          'destination': str(destination)}))
        return
    if destination.exists():
        raise ValueError('Quarantine already exists; refusing overwrite')
    records = []
    for relative in paths:
        path = root / relative
        if not path.is_file() or path.is_symlink():
            raise ValueError('Missing or symlinked input: ' + relative)
        raw = path.read_bytes()
        records.append({'original_path': relative, 'bytes': len(raw),
                        'sha256': hashlib.sha256(raw).hexdigest()})
    counts = {}
    count = 0
    for row in disposition_rows(root / paths[1]):
        count += 1
        key = row['disposition']
        counts[key] = counts.get(key, 0) + 1
    for directory in (root / '.cache', root / '.cache/quarantine', destination):
        directory.mkdir(exist_ok=True, mode=0o700)
        directory.chmod(0o700)
    for record in records:
        target = destination / record['original_path']
        target.parent.mkdir(parents=True, exist_ok=True)
        target.parent.chmod(0o700)
        shutil.copy2(root / record['original_path'], target)
        if hashlib.sha256(target.read_bytes()).hexdigest() != record['sha256']:
            raise ValueError('Preservation digest mismatch')
    receipt = {'schema': 'ges.heuristic-quarantine.v1',
               'status': 'INVALIDATED_HEURISTIC_PROPOSAL_ONLY',
               'artifacts': records, 'disposition_counts': counts,
               'claim_count': count, 'certification_evidence': False,
               'quarantine': '.cache/quarantine/a1-legacy-semantic-review'}
    (destination / 'receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
    for record in records:
        original = root / record['original_path']
        if hashlib.sha256(original.read_bytes()).hexdigest() != record['sha256']:
            raise ValueError('Input changed; retained originals')
    for record in records:
        # Move originals into the quarantine after verifying the preserved copy.
        # This retains an additional recovery copy instead of permanent deletion.
        shutil.move(str(root / record['original_path']),
                    str(destination / (Path(record['original_path']).name + '.original')))
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
