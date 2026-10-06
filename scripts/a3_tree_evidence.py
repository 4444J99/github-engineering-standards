"""Capture fresh, pin-bound GitHub tree observations; no source code is run."""
import argparse
import json

from pathlib import Path
from ges.core import dump, load
from ges.pinned_sources import inventory_digest
from ges.sources import fetch


def capture(capsule):
    records = {}
    for spec in load(capsule / 'sources.lock.json')['sources']:
        repo, commit = spec['repository'], spec['commit']
        prefix = 'https://api.github.com/repos/' + repo + '/git/'
        revision = json.loads(fetch(prefix + 'commits/' + commit))
        if revision['sha'] != commit:
            raise ValueError('GitHub revision differs from pinned commit')
        tree_sha = revision['tree']['sha']
        tree = json.loads(fetch(prefix + 'trees/' + tree_sha + '?recursive=1'))
        if tree['sha'] != tree_sha or tree.get('truncated'):
            raise ValueError('GitHub tree is changed or truncated')
        inventory = load(capsule / 'sources' / (repo.replace('/', '__') + '.inventory.json'))
        original = {row['path']: row for row in inventory}
        observed = {row['path']: row for row in tree['tree'] if row['type'] in ('blob', 'commit')}
        if (len(original) != len(inventory) or set(original) != set(observed) or
                any(row.get('git_blob_sha') != observed[path]['sha']
                    for path, row in original.items() if row.get('git_blob_sha'))):
            raise ValueError('Pinned Git tree differs from frozen inventory')
        records[repo] = {'repository': repo, 'commit': commit, 'tree_sha': tree_sha,
                         'inventory_digest': inventory_digest(inventory), 'status': 'MATCH',
                         'artifacts': len(original), 'method': 'GitHub pinned commit and recursive tree API'}
    return records


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--capsule', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError('Tree evidence output already exists')
    dump(args.output, capture(args.capsule))
