"""Validate published-body claim provenance, never semantic or adoption truth.

Published bodies are keyed by immutable acquisition digests, not an invented
deployment commit. Imported statements and examples are inert evidence.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
from pathlib import Path

from .core import now, timestamp
from .pages import cached_pages, MAX_BYTES


def validate_published_claims(ledger: Path, cache: Path, documents: list[Path],
                             reviewers: list[str]) -> dict:
    if (not isinstance(reviewers, list) or not reviewers or
            any(not isinstance(r, str) or not r.strip() for r in reviewers) or
            len(set(reviewers)) != len(reviewers)):
        raise ValueError('Invalid authorized reviewer policy')
    if not documents or len(set(documents)) != len(documents):
        raise ValueError('Missing or duplicate review documents')
    ledger_bytes = ledger.read_bytes()
    ledger_sha = hashlib.sha256(ledger_bytes).hexdigest()
    pages = json.loads(ledger_bytes)
    acquired = cached_pages(cache, pages, ledger_sha)
    indexed = {p['page_id']: p for p in pages}
    claim_ids, page_ids, receipts = set(), set(), []
    applications = 0
    for path in documents:
        raw = path.read_bytes()
        doc = json.loads(raw)
        if not isinstance(doc, dict) or doc.get('schema') != 'ges.published-reference-claims.v1':
            raise ValueError('Unsupported published claim schema')
        if doc.get('reviewer') not in reviewers:
            raise ValueError('Unauthorized reviewer')
        reviewed = timestamp(doc['reviewed_at'])
        if reviewed > timestamp(now()):
            raise ValueError('Future review timestamp')
        if doc.get('ledger_sha256') != ledger_sha:
            raise ValueError('Review belongs to a different page ledger')
        if doc.get('disposition') != 'REFERENCE_ONLY':
            raise ValueError('Published reference cannot assert policy adoption')
        for flag in ('accepted_policy', 'rights_accepted', 'source_revision_verified',
                     'native_behavior_verified', 'independent_omission_audit_passed',
                     'automated_provenance_validation_passed'):
            if doc.get(flag) is not False:
                raise ValueError('Reference receipt asserts unsupported completion: '+flag)
        for flag in ('project_complete', 'acceptance_gate_closed', 'semantic_truth_certified'):
            if flag in doc and doc[flag] is not False:
                raise ValueError('Reference receipt asserts unsupported completion: '+flag)
        instances, spans, claims = doc.get('instances'), doc.get('spans'), doc.get('claims')
        if not isinstance(instances, list) or not instances:
            raise ValueError('Missing page instances')
        if not isinstance(spans, dict) or not spans:
            raise ValueError('Missing source spans')
        if not isinstance(claims, list) or not claims:
            raise ValueError('Missing claims')
        for count, actual in (('page_instance_denominator', len(instances)),
                              ('claim_statements', len(claims))):
            if type(doc.get(count)) is not int or doc[count] != actual:
                raise ValueError('Declared count mismatch: '+count)
        local_ids = set()
        for instance in instances:
            if not isinstance(instance, dict):
                raise ValueError('Malformed page instance')
            identity = instance.get('page_id')
            if not isinstance(identity, str) or identity in local_ids:
                raise ValueError('Duplicate or invalid page instance')
            local_ids.add(identity)
            if identity not in indexed or identity not in acquired:
                raise ValueError('Page instance has no verified acquisition')
            page, row = indexed[identity], acquired[identity]
            if any(instance.get(k) != page[k] for k in ('version', 'path')):
                raise ValueError('Page instance does not match ledger identity')
            if instance.get('body_sha256') != row['sha256']:
                raise ValueError('Review body digest mismatch')
            if reviewed < timestamp(row['retrieved_at']):
                raise ValueError('Review precedes body acquisition')
            with gzip.open(cache / row['body_file'], 'rb') as stream:
                body = stream.read(MAX_BYTES+1)
            # Recheck after reading: a concurrent replacement cannot become evidence.
            if len(body) != row['bytes'] or hashlib.sha256(body).hexdigest() != row['sha256']:
                raise ValueError('Body changed during provenance validation')
            lines = body.decode('utf-8').splitlines()
            for name, span in spans.items():
                if not isinstance(name, str) or not name.strip() or not isinstance(span, dict):
                    raise ValueError('Malformed source span')
                bounds = span.get('lines')
                if (not isinstance(bounds, list) or len(bounds) != 2 or
                        any(type(n) is not int for n in bounds) or
                        not 1 <= bounds[0] <= bounds[1] <= len(lines)):
                    raise ValueError('Source span exceeds body bounds')
                sha = hashlib.sha256('\n'.join(lines[bounds[0]-1:bounds[1]]).encode()).hexdigest()
                if span.get('sha256') != sha:
                    raise ValueError('Source span digest mismatch')
            page_ids.add(identity)
        for claim in claims:
            if not isinstance(claim, dict) or set(claim) != {'id', 'span', 'statement'}:
                raise ValueError('Malformed or unsupported reference claim')
            identity, span, statement = claim['id'], claim['span'], claim['statement']
            if not isinstance(identity, str) or not identity.strip() or identity in claim_ids:
                raise ValueError('Invalid or duplicate claim identity')
            if not isinstance(span, str) or span not in spans:
                raise ValueError('Claim references unknown source span')
            if not isinstance(statement, str) or not statement.strip():
                raise ValueError('Missing independent claim statement')
            claim_ids.add(identity)
        applications += len(claims)*len(instances)
        receipts.append({'path': str(path), 'sha256': hashlib.sha256(raw).hexdigest()})
    return {'valid': True, 'reference_claims': len(claim_ids),
            'claim_page_applications': applications, 'page_instances': len(page_ids),
            'published_denominator': len(pages), 'review_documents': receipts,
            'semantic_truth_certified': False, 'omission_completeness_certified': False,
            'source_revision_verified': False, 'rights_cleared': False,
            'native_behavior_verified': False, 'policy_adopted': False}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--ledger', type=Path, required=True)
    parser.add_argument('--cache', type=Path, required=True)
    parser.add_argument('--claims', type=Path, nargs='+', required=True)
    parser.add_argument('--review-policy', type=Path, required=True)
    args = parser.parse_args()
    try:
        policy = json.loads(args.review_policy.read_text())
        result = validate_published_claims(args.ledger, args.cache, args.claims,
                                          policy['authorized_reviewers'])
    except (ValueError, KeyError, TypeError, OSError) as exc:
        print(json.dumps({'valid': False, 'error': str(exc)}))
        return 2
    print(json.dumps(result))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
