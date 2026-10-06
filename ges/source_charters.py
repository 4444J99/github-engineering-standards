"""Replay charter citations against pinned source text using canonical spans."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path

from .core import ROOT


def validate_citations(manifest, sources, pins):
    texts = {}
    for repository in {row['repository'] for row in manifest['citations']}:
        with gzip.open(sources / (repository.replace('/', '__') + '.text.jsonl.gz'), 'rt') as stream:
            for line in stream:
                row = json.loads(line)
                texts[(row['source'], row['commit'], row['path'])] = row['content']
    for citation in manifest['citations']:
        if pins.get(citation['repository']) != citation['commit']:
            raise ValueError('Charter source differs from locked pin')
        content = texts[(citation['repository'], citation['commit'], citation['path'])]
        if hashlib.sha256(content.encode()).hexdigest() != citation['content_sha256']:
            raise ValueError('Pinned source content digest mismatch')
        lines = content.splitlines()
        start, end = citation['start_line'], citation['end_line']
        if type(start) is not int or type(end) is not int or not 1 <= start <= end <= len(lines):
            raise ValueError('Invalid charter citation line bounds')
        span = '\n'.join(lines[start - 1:end])
        if hashlib.sha256(span.encode()).hexdigest() != citation['span_sha256']:
            raise ValueError('Pinned source span digest mismatch')
    return {'valid': True, 'citations': len(manifest['citations']),
            'owner_approval': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sources', type=Path, required=True)
    args = parser.parse_args()
    manifest = json.loads((ROOT / 'evidence/a4-source-charters.json').read_text())
    pins = {row['repository']: row['commit'] for row in
            json.loads((ROOT / 'sources/sources.lock.json').read_text())['sources']}
    print(json.dumps(validate_citations(manifest, args.sources, pins)))
