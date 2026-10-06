"""Validate reference accounting, never certify semantic completeness or adoption."""
from __future__ import annotations

import hashlib
import gzip
import json
from datetime import datetime, timezone
from pathlib import Path


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_pinned_span(text: str, row: dict) -> None:
    """Check source content and canonical newline-joined span (no final LF)."""
    lines = text.splitlines()
    start, end = row['start_line'], row['end_line']
    if (type(start) is not int or type(end) is not int or
            not 1 <= start <= end <= len(lines)):
        raise ValueError('Ledger span exceeds pinned source')
    if hashlib.sha256(text.encode()).hexdigest() != row['content_sha256']:
        raise ValueError('Pinned source content digest mismatch')
    span = '\n'.join(lines[start-1:end])
    if hashlib.sha256(span.encode()).hexdigest() != row['span_sha256']:
        raise ValueError('Pinned source span digest mismatch')


def validate_accounting(root: Path, ledger: Path, accounting: Path,
                        authorized_reviewers: list[str], sources: Path | None = None) -> dict:
    """Fail closed on changed evidence or unsupported reference-accounting claims."""
    if (not isinstance(authorized_reviewers, list) or not authorized_reviewers or
            any(not isinstance(r, str) or not r.strip() for r in authorized_reviewers)):
        raise ValueError('Authorized reviewers must be a nonempty list of identities')
    evidence = json.loads(accounting.read_text())
    rows = json.loads(ledger.read_text())
    if not isinstance(rows, list) or not rows:
        raise ValueError('Structured ledger must be a nonempty array')
    if _sha(ledger) != evidence['structured_ledger_sha256']:
        raise ValueError('Structured ledger digest mismatch')
    indexed = {r['requirement_id']: r for r in rows}
    if len(indexed) != len(rows):
        raise ValueError('Duplicate structured ledger ID')
    advertised = evidence['accounted_occurrence_ids']
    if len(advertised) != len(set(advertised)) or set(advertised) != set(indexed):
        raise ValueError('Advertised IDs differ from the complete ledger')
    if type(evidence['structured_occurrences']) is not int or evidence['structured_occurrences'] != len(rows):
        raise ValueError('Incorrect structured denominator')
    for key in ('consolidation_complete', 'generalization_complete',
                'operational_completeness', 'policy_accepted', 'independent_omission_certified'):
        if evidence.get(key) is not False:
            raise ValueError('Reference accounting cannot certify '+key)
    claims_seen, referenced, labels, paths_seen = set(), set(), set(), set()
    claim_occurrences = {}
    statement_count = 0
    root = root.resolve()
    source_texts = {}
    if sources is not None:
        needed = {(r['source'], r['commit'], r['path']) for r in rows}
        for source in sorted({r['source'] for r in rows}):
            with gzip.open(sources / (source.replace('/', '__')+'.text.jsonl.gz'), 'rt') as stream:
                for line in stream:
                    artifact = json.loads(line)
                    key = (artifact['source'], artifact['commit'], artifact['path'])
                    if key not in needed:
                        continue
                    if key in source_texts:
                        raise ValueError('Duplicate pinned source artifact')
                    source_texts[key] = artifact['content']
        if set(source_texts) != needed:
            raise ValueError('Missing pinned source artifacts')
        for row in rows:
            text = source_texts[(row['source'], row['commit'], row['path'])]
            validate_pinned_span(text, row)

    def match(identity: str, item: dict, doc: dict) -> None:
        if identity not in indexed:
            raise ValueError('Unknown structured occurrence: '+identity)
        row = indexed[identity]
        for key in ('source', 'commit', 'path'):
            if item.get(key, doc.get(key)) != row[key]:
                raise ValueError('Occurrence provenance mismatch: '+identity+' '+key)
        start = item.get('start_line', item.get('line'))
        end = item.get('end_line', start)
        if type(start) is not int or type(end) is not int or start < 1 or end < start:
            raise ValueError('Invalid source span: '+identity)
        if start < row['start_line'] or end > row['end_line']:
            raise ValueError('Reference lies outside occurrence span: '+identity)
        for key in ('content_sha256', 'span_sha256'):
            supplied = item.get(key, doc.get(key) if key == 'content_sha256' else None)
            if supplied is not None and supplied != row[key]:
                raise ValueError('Occurrence digest mismatch: '+identity+' '+key)
        if sources is not None:
            text = source_texts[(row['source'], row['commit'], row['path'])]
            raw = '\n'.join(text.splitlines()[start-1:end])
            if 'source_definition_sha256' in item:
                ds, de = item['source_definition_start_line'], item['source_definition_end_line']
                if ds != row['start_line'] or de != row['end_line']:
                    raise ValueError('Source definition span mismatch: '+identity)
                convention = doc.get('digest_convention', '')
                if 'definition lines with a final LF' not in convention:
                    raise ValueError('Unsupported source definition digest convention')
                definition = '\n'.join(text.splitlines()[ds-1:de])+'\n'
                if hashlib.sha256(definition.encode()).hexdigest() != item['source_definition_sha256']:
                    raise ValueError('Source definition digest mismatch: '+identity)
            for key in ('text_sha256', 'raw_line_sha256'):
                if key in item and hashlib.sha256(raw.encode()).hexdigest() != item[key]:
                    raise ValueError('Reference text digest mismatch: '+identity)

    for entry in evidence['review_documents']:
        path = (root / entry['path']).resolve()
        if not path.is_relative_to(root) or path in paths_seen:
            raise ValueError('Unsafe or duplicate review document')
        paths_seen.add(path)
        if _sha(path) != entry['sha256']:
            raise ValueError('Review document digest mismatch: '+entry['path'])
        doc = json.loads(path.read_text())
        if doc.get('reviewer') not in authorized_reviewers:
            raise ValueError('Unauthorized claim reviewer')
        timestamp = datetime.fromisoformat(doc['reviewed_at'].replace('Z', '+00:00'))
        if timestamp.tzinfo is None or timestamp > datetime.now(timezone.utc):
            raise ValueError('Invalid claim review timestamp')
        claims = doc['claims']
        if not isinstance(claims, list) or not claims:
            raise ValueError('Claims must be a nonempty array')
        local_ids = set()
        for claim in claims:
            cid = claim['claim_id']
            if not isinstance(cid, str) or not cid.strip() or cid in claims_seen:
                raise ValueError('Invalid or duplicate reference claim ID')
            claims_seen.add(cid)
            local_ids.add(cid)
            if not isinstance(claim.get('statement'), str) or not claim['statement'].strip():
                raise ValueError('Empty reference statement')
            if claim.get('accepted_policy', False) is not False or claim.get('adopted_obligation') is not None:
                raise ValueError('Reference claim asserts adopted policy')
            identities = claim.get('structured_requirement_ids', claim.get('source_occurrence_ids', []))
            if 'structured_requirement_id' in claim:
                identities = [claim['structured_requirement_id']]
            if 'source_id' in claim:
                identities = ['SRC-GHQR-'+claim['source_id']]
            if 'source_definition_id' in claim and not identities:
                identities = ['SRC-GHQR-'+claim['source_definition_id']]
            if not isinstance(identities, list) or not identities:
                raise ValueError('Reference claim has no structured identity: '+cid)
            if len(identities) != len(set(identities)):
                raise ValueError('Repeated occurrence within a claim')
            for identity in identities:
                match(identity, claim, doc)
                referenced.add(identity)
            spans = claim.get('source_occurrence_spans', [])
            if spans:
                if {s['requirement_id'] for s in spans} != set(identities):
                    raise ValueError('Nested occurrence spans differ from claim identities')
                for span in spans:
                    match(span['requirement_id'], {**claim, **span}, doc)
            claim_occurrences[cid] = set(identities)
            statement_count += 1
        dispositions = doc.get('non_actionable_structured_occurrences', [])
        dispositions += [r for r in doc.get('structured_occurrence_dispositions', [])
                         if r.get('disposition') == 'NO_ACTIONABLE_CONTENT']
        for item in dispositions:
            identity = item.get('structured_requirement_id', item.get('requirement_id'))
            match(identity, item, doc)
            if identity in labels or not isinstance(item.get('rationale'), str) or not item['rationale'].strip():
                raise ValueError('Duplicate or unjustified nonoperative label')
            labels.add(identity)
        for item in doc.get('structured_occurrence_dispositions', []):
            if item.get('disposition') == 'REFERENCE':
                identity = item['requirement_id']
                match(identity, item, doc)
                links = item.get('reference_claim_ids', [])
                if (not links or not set(links) <= local_ids or
                        any(identity not in claim_occurrences[cid] for cid in links)):
                    raise ValueError('Dangling reference disposition')
    if labels & referenced:
        raise ValueError('Occurrence is both a label and an operative reference')
    if labels | referenced != set(indexed):
        raise ValueError('Actual reference records do not cover the ledger')
    if set(evidence['nonoperative_labels']) != labels or len(evidence['nonoperative_labels']) != len(labels):
        raise ValueError('Advertised labels differ from review records')
    if type(evidence['reviewed_reference_statements']) is not int or evidence['reviewed_reference_statements'] != statement_count:
        raise ValueError('Incorrect reference statement count')
    if evidence.get('missing_ids') != [] or evidence.get('extra_ids') != []:
        raise ValueError('Accounting advertises unresolved membership')
    return {'valid': True, 'structured_occurrences': len(rows),
            'reference_statements': statement_count, 'nonoperative_labels': len(labels),
            'pinned_source_spans_verified': sources is not None,
            'consolidation_complete': False, 'independent_omission_certified': False}


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path('.'))
    parser.add_argument('--ledger', type=Path, required=True)
    parser.add_argument('--accounting', type=Path, required=True)
    parser.add_argument('--review-policy', type=Path, required=True)
    parser.add_argument('--sources', type=Path, help='Verify full-file and span digests against pinned text snapshots')
    args = parser.parse_args()
    try:
        report = validate_accounting(args.root, args.ledger, args.accounting,
                                     json.loads(args.review_policy.read_text())['authorized_reviewers'], args.sources)
    except (ValueError, KeyError, TypeError, OSError) as exc:
        print(json.dumps({'valid': False, 'error': str(exc)}))
        return 2
    print(json.dumps(report))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
