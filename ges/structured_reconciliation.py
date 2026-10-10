"""Exact structured-occurrence receipts; reference inventory is not reconciliation."""
from __future__ import annotations

import gzip
import hashlib
import json
from pathlib import Path

from .claim_reconciliation import reconciliation_accounting as claim_accounting
from .core import ROOT, digest, now
from .evidence_integrity import validate_authority
from .ledger import structured_rows
from .published_assurance import _evidence, _require, _strings, _time


def _sha(path):
    _require(path.is_file() and not path.is_symlink(), 'Missing or symlinked structured input')
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def _is_structured(source, path):
    return ((source == 'microsoft/ghqr' and
             path.startswith('internal/recommendations/definitions/') and path.endswith('.yaml')) or
            (source == 'github/github-well-architected' and
             path.startswith('content/library/') and path.endswith('/checklist.md')))


def _inventory(requirements, artifacts, sources, pins):
    structured_sources = {'microsoft/ghqr', 'github/github-well-architected'}
    _require(isinstance(pins, dict) and structured_sources <= set(pins),
             'Missing complete structured source pins')
    index = {}
    for line in artifacts.read_text().splitlines():
        if not line.strip():
            continue
        item = json.loads(line)
        if not _is_structured(item['source'], item['path']):
            continue
        key = (item['source'], item['commit'], item['path'])
        _require(key not in index and pins.get(item['source']) == item['commit'],
                 'Duplicate or unpinned structured artifact')
        index[key] = item
    seen, rebuilt, snapshots, texts = set(), [], {}, {}
    for source in sorted(structured_sources):
        path = sources / (source.replace('/', '__') + '.text.jsonl.gz')
        snapshots[path] = _sha(path)
        with gzip.open(path, 'rt', encoding='utf-8') as stream:
            for line in stream:
                record = json.loads(line)
                if not _is_structured(record['source'], record['path']):
                    continue
                key = (record['source'], record['commit'], record['path'])
                _require(record['source'] == source and key in index and key not in seen,
                         'Foreign or duplicate structured source artifact')
                seen.add(key)
                rebuilt.extend(structured_rows(record, index[key]))
                texts[key] = record['content']
    _require(seen == set(index), 'Missing pinned structured artifacts')
    sort = lambda rows: sorted(rows, key=lambda row: row['requirement_id'])
    _require(digest(sort(rebuilt)) == digest(sort(requirements)),
             'Structured denominator differs from complete pinned extraction')
    return snapshots, texts


def _location(row, item, document, text):
    _require(all(item.get(k, document.get(k)) == row[k]
                 for k in ('source', 'commit', 'path')), 'Foreign claim association provenance')
    start, end = item.get('start_line'), item.get('end_line')
    _require(type(start) is int and type(end) is int and
             row['start_line'] <= start <= end <= row['end_line'],
             'Claim association outside occurrence span')
    for key in ('content_sha256', 'span_sha256'):
        supplied = item.get(key, document.get(key) if key == 'content_sha256' else None)
        _require(supplied is None or supplied == row[key], 'Association digest mismatch: ' + key)
    lines = text.splitlines()
    raw_sha = hashlib.sha256('\n'.join(lines[start-1:end]).encode()).hexdigest()
    for key in ('text_sha256', 'raw_line_sha256'):
        _require(key not in item or item[key] == raw_sha, 'Association digest mismatch: ' + key)
    if 'source_definition_sha256' in item:
        ds, de = item.get('source_definition_start_line'), item.get('source_definition_end_line')
        _require(type(ds) is int and type(de) is int and
                 (ds, de) == (row['start_line'], row['end_line']) and
                 'definition lines with a final LF' in document.get('digest_convention', ''),
                 'Unsupported source definition span or digest convention')
        definition_sha = hashlib.sha256(('\n'.join(lines[ds-1:de]) + '\n').encode()).hexdigest()
        _require(item['source_definition_sha256'] == definition_sha,
                 'Source definition digest mismatch')


def reconciliation_accounting(*, requirements, artifacts: Path, sources: Path,
                             reviews: Path, review_policy, pins, catalog, proposals,
                             claim_receipts=None, claim_policy=None, receipts=None,
                             policy=None, evidence_root: Path = ROOT):
    """Revalidate underlying claims and source bytes, never consume a claimed report.

    A receipt certifies the entire association set, including superseded claims.
    Omission completeness remains the separate source-fidelity gate.
    """
    _require((receipts is None) == (policy is None),
             'Structured receipts and authority policy must be supplied together')
    _require(isinstance(requirements, list), 'Structured ledger must be an array')
    indexed = {}
    for row in requirements:
        _require(isinstance(row, dict) and isinstance(row.get('requirement_id'), str)
                 and row['requirement_id'].strip() and row['requirement_id'] not in indexed,
                 'Malformed or duplicate structured occurrence')
        indexed[row['requirement_id']] = row
    artifact_sha = _sha(artifacts)
    snapshots, texts = _inventory(requirements, artifacts, sources, pins)
    claims = claim_accounting(artifacts, sources, reviews, review_policy, pins,
                             catalog, proposals, claim_receipts, claim_policy)
    manifest, association, ready, authors = [], {key: [] for key in indexed}, {}, {}
    for path in sorted(reviews.glob('*-claims.json')):
        raw = path.read_bytes()
        manifest.append({'path': path.name, 'sha256': hashlib.sha256(raw).hexdigest()})
        document = json.loads(raw)
        for claim in document['claims']:
            ids = claim.get('structured_requirement_ids', claim.get('source_occurrence_ids', []))
            if 'structured_requirement_id' in claim:
                ids = [claim['structured_requirement_id']]
            if 'source_id' in claim:
                ids = ['SRC-GHQR-' + claim['source_id']]
            if 'source_definition_id' in claim and not ids:
                ids = ['SRC-GHQR-' + claim['source_definition_id']]
            _require(isinstance(ids, list) and all(isinstance(i, str) for i in ids)
                     and len(ids) == len(set(ids)), 'Invalid structured claim association')
            nested = claim.get('source_occurrence_spans', [])
            _require(isinstance(nested, list), 'Invalid nested occurrence spans')
            if nested:
                _require(len(nested) == len(ids) and
                         {span['requirement_id'] for span in nested} == set(ids),
                         'Nested occurrence spans differ from association set')
            spans = {span['requirement_id']: span for span in nested}
            for identity in ids:
                _require(identity in indexed, 'Unknown structured claim association')
                row = indexed[identity]
                text = texts[(row['source'], row['commit'], row['path'])]
                _location(row, claim, document, text)
                if identity in spans:
                    _location(row, {**claim, **spans[identity]}, document, text)
                association[identity].append(claim['claim_id'])
                ready[identity] = max(ready.get(identity, _time(document['reviewed_at'])),
                                      _time(document['reviewed_at']),
                                      _time(claim.get('reviewed_at', document['reviewed_at'])))
                authors.setdefault(identity, set()).add(document['reviewer'])
                for container in (document, claim):
                    for field in ('executor', 'reviewer'):
                        if field in container:
                            actor = container[field]
                            _require(isinstance(actor, str) and actor.strip(),
                                     'Invalid claim author identity')
                            authors[identity].add(actor)
    association = {key: sorted(values) for key, values in association.items()}
    subject = {'structured_ledger_digest': digest(sorted(requirements, key=lambda row: row['requirement_id'])),
               'artifacts_sha256': artifact_sha,
               'source_snapshots_digest': digest({path.name: value for path, value in snapshots.items()}),
               'review_documents_digest': digest(manifest), 'association_digest': digest(association),
               'claim_input_digest': claims['claim_input_digest'],
               'catalog_digest': claims['catalog_digest'], 'proposal_digest': claims['proposal_digest'],
               'claim_receipts_digest': claims['receipts_digest'], 'claim_policy_digest': claims['policy_digest']}
    result = {'schema': 'ges.structured-reconciliation-accounting.v1',
              'subject': subject, 'completed': 0, 'denominator': len(indexed),
              'remaining': len(indexed), 'validated_occurrence_ids': [],
              'all_structured_occurrences_reconciled': None,
              'semantic_truth_automatically_certified': False,
              'independent_omission_certified': False, 'policy_adopted': False}
    if receipts is None:
        return result
    _require(isinstance(receipts, list), 'Structured receipts must be an array')
    _require(isinstance(policy, dict) and set(policy) ==
             {'schema', 'approval_reference', 'subject', 'authorized_reviewers',
              'authorized_independent_reviewers'} and
             policy['schema'] == 'ges.structured-reconciliation-policy.v1',
             'Missing or malformed structured authority policy')
    validate_authority(policy)
    _require(isinstance(policy['approval_reference'], str) and policy['approval_reference'].strip()
             and digest(policy['subject']) == digest(subject), 'Structured authority subject changed')
    _require(_strings(policy['authorized_reviewers']) and
             _strings(policy['authorized_independent_reviewers']), 'Invalid structured authority roles')
    seen, evidence = set(), []
    validated = set(claims['validated_claim_ids'])
    claim_by_id = {r['claim']['claim_id']: r for r in (claim_receipts or [])}
    current = _time(now())
    for receipt in receipts:
        _require(isinstance(receipt, dict) and set(receipt) ==
                 {'schema', 'subject', 'disposition', 'rationale', 'reviewer',
                  'independent_reviewer', 'reviewed_at', 'audited_at', 'evidence'}
                 and receipt['schema'] == 'ges.structured-reconciliation-receipt.v1',
                 'Malformed structured receipt')
        provided = receipt['subject']
        _require(isinstance(provided, dict) and isinstance(provided.get('occurrence'), dict),
                 'Malformed occurrence subject')
        identity = provided['occurrence'].get('requirement_id')
        _require(isinstance(identity, str) and identity in indexed and identity not in seen,
                 'Unknown or duplicate structured receipt')
        expected = {'occurrence': indexed[identity], 'claim_ids': association[identity], 'inputs': subject}
        _require(digest(provided) == digest(expected), 'Occurrence subject or association changed')
        links = association[identity]
        disposition = 'CLAIMS_RECONCILED' if links else 'NONOPERATIVE'
        _require(receipt['disposition'] == disposition and
                 isinstance(receipt['rationale'], str) and bool(receipt['rationale'].strip()),
                 'Unsupported or unjustified structured disposition')
        _require(set(links) <= validated, 'Occurrence has unresolved associated claims')
        reviewer, auditor = receipt['reviewer'], receipt['independent_reviewer']
        _require(isinstance(reviewer, str) and isinstance(auditor, str) and
                 reviewer in policy['authorized_reviewers'] and
                 auditor in policy['authorized_independent_reviewers'], 'Unauthorized structured reviewer')
        authors_here = authors.get(identity, set()) | {claim_by_id[c]['reconciler'] for c in links}
        _require(reviewer != auditor and auditor not in authors_here,
                 'Structured audit must be independent of authors and reconciler')
        reviewed, audited = _time(receipt['reviewed_at']), _time(receipt['audited_at'])
        latest = max([ready.get(identity, reviewed),
                      *[_time(claim_by_id[c]['reviewed_at']) for c in links]])
        _require(latest <= reviewed <= audited <= current, 'Structured review chronology invalid')
        refs = receipt['evidence']
        _require(isinstance(refs, dict) and set(refs) == {'review', 'independent_audit'},
                 'Missing structured review and independent evidence')
        for kind, actor, stamp in (('review', reviewer, reviewed),
                                   ('independent_audit', auditor, audited)):
            reference = refs[kind]
            _require(isinstance(reference, dict) and set(reference) == {'path', 'sha256'},
                     'Malformed structured evidence reference')
            doc = _evidence(evidence_root, reference)
            _require(set(doc) == {'schema', 'kind', 'identity', 'subject', 'disposition',
                                  'reviewed_at', 'outcome', 'unresolved', 'observations'} and
                     doc['schema'] == 'ges.structured-reconciliation-evidence.v1' and
                     doc['kind'] == kind and doc['identity'] == actor and
                     digest(doc['subject']) == digest(expected) and
                     doc['disposition'] == disposition and _time(doc['reviewed_at']) == stamp and
                     doc['outcome'] == 'PASS' and doc['unresolved'] == [] and
                     _strings(doc['observations']) and len(doc['observations']) <= 100 and
                     all(len(x) <= 4000 for x in doc['observations']),
                     'Structured evidence is incomplete or differs from receipt')
            evidence.append(reference)
        seen.add(identity)
    for reference in evidence:
        _evidence(evidence_root, reference)
    _require(_sha(artifacts) == artifact_sha and all(_sha(p) == sha for p, sha in snapshots.items())
             and manifest == [{'path': p.name, 'sha256': _sha(p)}
                              for p in sorted(reviews.glob('*-claims.json'))],
             'Structured inputs changed during validation')
    result.update(completed=len(seen), remaining=len(indexed)-len(seen),
                  validated_occurrence_ids=sorted(seen),
                  all_structured_occurrences_reconciled=(len(seen) == len(indexed) if indexed else None))
    return result
