"""Measure full-corpus accounting only; timing is not semantic certification."""
import argparse
import hashlib
import json
import statistics
import tempfile
import time
from pathlib import Path

from ges.core import ROOT, load
from ges.corpus import coverage_with_reviews


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--samples', type=int, default=3)
    args = parser.parse_args()
    if not 1 <= args.samples <= 5:
        parser.error('samples must be between 1 and 5')
    corpus = ROOT/'.cache/corpus'
    candidates = [json.loads(line) for line in (corpus/'candidates.jsonl').read_text().splitlines() if line]
    receipts = []
    for path in sorted((ROOT/'evidence/source-reviews').glob('*.json')):
        if not path.name.endswith('-claims.json'):
            receipts.extend(load(path))
    controls = load(ROOT/'controls/catalog.json')
    reviewers = load(ROOT/'evidence/source-review-policy.json')['authorized_reviewers']
    seconds = []
    reports = []
    with tempfile.TemporaryDirectory() as scratch:
        receipt_path = Path(scratch)/'reviews.json'
        receipt_path.write_text(json.dumps(receipts), encoding='utf-8')
        for _ in range(args.samples):
            started = time.perf_counter()
            report = coverage_with_reviews(corpus/'artifacts.jsonl', receipt_path,
                                           candidates=candidates, controls=controls,
                                           authorized_reviewers=reviewers)
            seconds.append(time.perf_counter()-started)
            reports.append(report)
    if any(report != reports[0] for report in reports):
        raise ValueError('Accounting changed across samples')
    canonical = json.dumps(reports[0], sort_keys=True, separators=(',', ':')).encode()
    inputs = {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
              for path in (corpus/'artifacts.jsonl', corpus/'candidates.jsonl',
                           ROOT/'controls/catalog.json', ROOT/'evidence/source-review-policy.json')}
    inputs['decoded_receipts'] = hashlib.sha256(json.dumps(receipts, sort_keys=True).encode()).hexdigest()
    print(json.dumps({'samples_seconds': seconds, 'median_seconds': statistics.median(seconds),
                      'candidate_count': len(candidates), 'receipt_count': len(receipts),
                      'accounting': reports[0], 'accounting_sha256': hashlib.sha256(canonical).hexdigest(),
                      'input_hashes_recorded_after_samples': inputs,
                      'scope': 'coverage_with_reviews only; excludes input loading, claim extraction, published bodies and recovery rendering'}))


if __name__ == '__main__':
    main()
