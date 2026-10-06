"""Reference-claim provenance audit; does not adjudicate semantics or rights."""
from __future__ import annotations

from datetime import datetime, timezone
import gzip
import hashlib
import json
from pathlib import Path
import re

from .evidence_integrity import invalidated_reviewer


def validate_provenance(artifacts: Path, sources: Path, reviews: Path,
                        reviewers: list[str], pins: dict[str, str],
                        control_ids: set[str] | None = None) -> dict:
    from .evidence_integrity import validate_authority
    validate_authority({'authorized_reviewers': reviewers})
    if not isinstance(reviewers, list) or not reviewers or any(not isinstance(r, str) for r in reviewers):
        raise ValueError('Invalid authorized reviewer policy')
    rows = [json.loads(line) for line in artifacts.read_text().splitlines() if line.strip()]
    index = {(r['source'], r['commit'], r['path']): r for r in rows}
    if len(index) != len(rows):
        raise ValueError('Duplicate artifact identity')
    claims, ids, documents = [], set(), []
    for path in sorted(reviews.glob('*-claims.json')):
        doc = json.loads(path.read_text())
        if not isinstance(doc, dict):
            raise ValueError("Claim document must be an object: " + path.name)
        if invalidated_reviewer(doc.get("reviewer")):
            raise ValueError("Invalidated heuristic reviewer: " + path.name)

        if doc.get('reviewer') not in reviewers:
            raise ValueError('Unauthorized reviewer: '+path.name)
        stamp = datetime.fromisoformat(doc['reviewed_at'].replace('Z', '+00:00'))
        if stamp.tzinfo is None or stamp > datetime.now(timezone.utc):
            raise ValueError('Invalid review timestamp: '+path.name)
        if not isinstance(doc.get('claims'), list) or not doc['claims']:
            raise ValueError('Missing claims: '+path.name)
        documents.append({'path': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()})
        for claim in doc['claims']:
            cid = claim['claim_id']
            if not isinstance(cid, str) or not cid.strip() or cid in ids:
                raise ValueError('Invalid or duplicate claim ID')
            ids.add(cid)
            if not isinstance(claim.get('statement'), str) or not claim['statement'].strip():
                raise ValueError('Empty claim statement: '+cid)
            source, commit, source_path = (claim.get(k, doc.get(k)) for k in ('source', 'commit', 'path'))
            if not isinstance(source, str) or not re.fullmatch(r'[\w.-]+/[\w.-]+', source):
                raise ValueError('Invalid claim source: '+cid)
            if pins.get(source) != commit:
                raise ValueError('Claim differs from locked source pin: '+cid)
            identity = (source, commit, source_path)
            if identity not in index:
                raise ValueError('Claim artifact is absent from inventory: '+cid)
            if claim.get('artifact_id', index[identity]['artifact_id']) != index[identity]['artifact_id']:
                raise ValueError('Claim artifact identity mismatch: '+cid)
            if claim.get('accepted_policy', False) is not False or claim.get('adopted_obligation') is not None:
                raise ValueError('Reference claim asserts adoption: '+cid)
            proposals = claim.get('proposed_control_ids', [])
            if (not isinstance(proposals, list) or
                    any(not isinstance(value, str) or not value for value in proposals) or
                    len(set(proposals)) != len(proposals)):
                raise ValueError('Invalid proposed control references: '+cid)
            if control_ids is not None and any(value not in control_ids for value in proposals):
                raise ValueError('Unknown proposed control reference: '+cid)
            claims.append((identity, claim, doc))
    if not claims:
        raise ValueError('No reference claims to audit')
    duplicate_links = {}
    for _, claim, _ in claims:
        if 'duplicate_of' in claim:
            target = claim['duplicate_of']
            if not isinstance(target, str) or target not in ids:
                raise ValueError('Unknown duplicate claim target: '+claim['claim_id'])
            duplicate_links[claim['claim_id']] = target
    for origin in duplicate_links:
        visited, current = set(), origin
        while current in duplicate_links:
            if current in visited:
                raise ValueError('Cyclic duplicate claim mapping: '+origin)
            visited.add(current)
            current = duplicate_links[current]
    needed = {identity for identity, _, _ in claims}
    texts = {}
    for source in sorted({identity[0] for identity in needed}):
        with gzip.open(sources / (source.replace('/', '__')+'.text.jsonl.gz'), 'rt') as stream:
            for line in stream:
                row = json.loads(line)
                identity = (row['source'], row['commit'], row['path'])
                if identity not in needed:
                    continue
                if identity in texts:
                    raise ValueError('Duplicate source snapshot artifact')
                text = row['content']
                if hashlib.sha256(text.encode()).hexdigest() != index[identity]['sha256']:
                    raise ValueError('Pinned text differs from artifact digest')
                texts[identity] = text
    if set(texts) != needed:
        raise ValueError('Missing pinned text for reference claims')
    for identity, claim, doc in claims:
        start, end = claim.get('start_line'), claim.get('end_line')
        lines = texts[identity].splitlines()
        if type(start) is not int or type(end) is not int or not 1 <= start <= end <= len(lines):
            raise ValueError('Claim exceeds source span: '+claim['claim_id'])
        content_digest = claim.get('content_sha256', doc.get('content_sha256'))
        if content_digest is not None and content_digest != index[identity]['sha256']:
            raise ValueError('Claim content digest mismatch: '+claim['claim_id'])
        raw = '\n'.join(lines[start-1:end])
        if not raw.strip():
            raise ValueError('Blank claim source span: '+claim['claim_id'])
        for key in ('text_sha256', 'raw_line_sha256', 'span_sha256'):
            if key in claim and hashlib.sha256(raw.encode()).hexdigest() != claim[key]:
                raise ValueError('Claim span digest mismatch: '+claim['claim_id'])
    return {'valid': True, 'reference_claims': len(claims), 'source_artifacts': len(needed),
            'duplicate_relationships_validated': len(duplicate_links),
            'proposed_control_identities_verified': control_ids is not None,
            'proposed_mapping_equivalence_certified': False,
            'review_documents': documents, 'semantic_truth_certified': False,
            'omission_completeness_certified': False, 'rights_cleared': False,
            'policy_adopted': False}


def main() -> int:
    import argparse
    from .core import ROOT
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--artifacts', type=Path, required=True)
    parser.add_argument('--sources', type=Path, required=True)
    parser.add_argument('--reviews', type=Path, required=True)
    parser.add_argument('--review-policy', type=Path, required=True)
    parser.add_argument('--pins', type=Path, default=ROOT / 'sources/sources.lock.json')
    parser.add_argument('--catalog', type=Path, default=ROOT / 'controls/catalog.json')
    args = parser.parse_args()
    try:
        pins = {r['repository']: r['commit'] for r in json.loads(args.pins.read_text())['sources']}
        catalog = json.loads(args.catalog.read_text())
        control_ids = {control['id'] for control in catalog}
        if len(control_ids) != len(catalog):
            raise ValueError('Duplicate canonical control identity')
        report = validate_provenance(args.artifacts, args.sources, args.reviews,
                                    json.loads(args.review_policy.read_text())['authorized_reviewers'], pins,
                                    control_ids)
    except (ValueError, KeyError, TypeError, OSError) as exc:
        print(json.dumps({'valid': False, 'error': str(exc)}))
        return 2
    print(json.dumps(report))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
