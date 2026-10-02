"""Inventory-complete rights triage. No generated record is rights clearance."""
import json
from pathlib import Path

from .core import ROOT, dump, load, now


def triage(artifacts: list[dict], pins: dict[str, str], findings: list[dict]) -> dict:
    if not artifacts:
        raise ValueError('Empty rights inventory')
    identities = set()
    index = {}
    for artifact in artifacts:
        key = (artifact['source'], artifact['commit'], artifact['path'])
        if key in index or artifact['artifact_id'] in identities:
            raise ValueError('Duplicate rights artifact')
        if pins.get(key[0]) != key[1]:
            raise ValueError('Rights inventory differs from source pin')
        index[key] = artifact
        identities.add(artifact['artifact_id'])
    existing = {}
    for finding in findings:
        key = (finding['source'], finding['commit'], finding['path'])
        if key not in index or key in existing:
            raise ValueError('Foreign or duplicate rights finding')
        if finding['content_sha256'] != index[key]['sha256']:
            raise ValueError('Rights finding digest mismatch')
        if finding.get('redistribution_approved') is not False:
            raise ValueError('Triage cannot import distribution approval')
        existing[key] = finding
    records = []
    for key, artifact in index.items():
        finding = existing.get(key)
        records.append({
            'artifact_id': artifact['artifact_id'], 'source': key[0], 'commit': key[1],
            'path': key[2], 'content_sha256': artifact['sha256'], 'url': artifact['url'],
            'status': 'PENDING_RIGHTS_ACCEPTANCE', 'redistribution_approved': False,
            'file_specific_review_performed': finding is not None,
            'repository_notice': finding.get('repository_notice') if finding else None,
            'file_specific_issues': finding.get('file_specific_issues', []) if finding else [],
            'required_decisions': ['Inspect file-specific and inherited notices',
                                   'Verify applicable grant and exceptions',
                                   'Record permitted use and attribution obligations',
                                   'Obtain applicable authorized distribution decision']})
    return {'schema': 'ges.rights-triage.v1', 'generated_at': now(),
            'denominator': len(artifacts), 'rights_accepted': 0,
            'existing_file_findings': len(existing), 'records': records,
            'rights_clearance_certified': False, 'publication_authorized': False}


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--artifacts', type=Path, required=True)
    parser.add_argument('--findings', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    artifacts = [json.loads(line) for line in args.artifacts.read_text().splitlines() if line.strip()]
    pins = {p['repository']: p['commit'] for p in load(ROOT/'sources/sources.lock.json')['sources']}
    report = triage(artifacts, pins, load(args.findings)['records'])
    dump(args.output, report)
    print(json.dumps({key: report[key] for key in ('denominator', 'rights_accepted', 'existing_file_findings')}))
