"""Preserve and invalidate the two known legacy heuristic artifacts."""
import argparse
import hashlib
import json
import shutil
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--checkout', type=Path, required=True)
    args = parser.parse_args()
    root = args.checkout.resolve()
    paths = ['scripts/semantic_review.py', 'evidence/semantic-review-dispositions.json']
    destination = root / '.cache/quarantine/a1-legacy-semantic-review'
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
    document = json.loads((root / paths[1]).read_text())
    counts = {}
    rows = document if isinstance(document, list) else document['dispositions']
    for row in rows:
        key = row['disposition']
        counts[key] = counts.get(key, 0) + 1
    destination.mkdir(parents=True, mode=0o700)
    for record in records:
        target = destination / record['original_path']
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(root / record['original_path'], target)
        if hashlib.sha256(target.read_bytes()).hexdigest() != record['sha256']:
            raise ValueError('Preservation digest mismatch')
    receipt = {'schema': 'ges.heuristic-quarantine.v1',
               'status': 'INVALIDATED_HEURISTIC_PROPOSAL_ONLY',
               'artifacts': records, 'disposition_counts': counts,
               'claim_count': len(rows), 'certification_evidence': False,
               'quarantine': '.cache/quarantine/a1-legacy-semantic-review'}
    (destination / 'receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
    for record in records:
        original = root / record['original_path']
        if hashlib.sha256(original.read_bytes()).hexdigest() != record['sha256']:
            raise ValueError('Input changed; retained originals')
    for record in records:
        (root / record['original_path']).unlink()
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
