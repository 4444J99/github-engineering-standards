"""Digest-bound published assurance attestations, not inferred semantic truth.

Policy is an explicitly approved authority input, never inferred from source
disposition permissions. The validator checks identity, roles and evidence
integrity; accountable reviewers own the truth of their scoped judgments.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re

from .core import ROOT, digest, now, timestamp
from .pages import cached_pages, validate_pages
from .published_claim_review import validate_published_claims

KINDS = ('source_identity', 'version_rendering', 'dependency_resolution',
         'claim_mapping', 'independent_omission_audit')
SOURCE_KEYS = ('artifact_id', 'source', 'commit', 'path', 'sha256')
MAX_EVIDENCE_BYTES = 1_000_000


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def _time(value):
    _require(isinstance(value, str) and bool(value.strip()), 'Missing review timestamp')
    return timestamp(value)


def _strings(value) -> bool:
    return (isinstance(value, list) and bool(value) and
            all(isinstance(v, str) and bool(v.strip()) for v in value) and
            len(set(value)) == len(value))


def _evidence(root: Path, reference: dict) -> dict:
    _require(isinstance(reference, dict), 'Malformed evidence reference')
    path = reference.get('path')
    sha = reference.get('sha256')
    _require(isinstance(path, str) and bool(path) and '\\' not in path,
             'Invalid evidence path')
    relative = Path(path)
    _require(bool(relative.parts) and not relative.is_absolute() and '..' not in relative.parts and
             relative.parts[0] == 'evidence' and relative.suffix == '.json',
             'Evidence must be a relative evidence JSON path')
    _require(isinstance(sha, str) and re.fullmatch('[a-f0-9]{64}', sha) is not None,
             'Invalid evidence digest')
    base = root.resolve()
    target = base / relative
    _require(not target.is_symlink() and
             not any(p.is_symlink() for p in target.parents if p != base and p.is_relative_to(base)),
             'Symlink evidence is not permitted')
    _require(target.resolve().is_relative_to(base / 'evidence') and target.is_file(),
             'Evidence path escapes scope or is missing')
    with target.open('rb') as stream:
        raw = stream.read(MAX_EVIDENCE_BYTES + 1)
    _require(len(raw) <= MAX_EVIDENCE_BYTES and hashlib.sha256(raw).hexdigest() == sha,
             'Evidence changed or exceeded size bound')
    doc = json.loads(raw)
    _require(isinstance(doc, dict), 'Evidence must be an object')
    return doc


def assurance_accounting(ledger: Path, cache: Path | None, artifacts: Path,
                         receipts: list[dict], policy: dict, pins: dict[str, str],
                         *, evidence_root: Path = ROOT) -> dict:
    raw = ledger.read_bytes()
    pages = json.loads(raw)
    validate_pages(pages)
    ledger_sha = hashlib.sha256(raw).hexdigest()
    indexed = {p['page_id']: p for p in pages}
    _require(isinstance(receipts, list), 'Assurance receipts must be an array')
    result = {'schema': 'ges.published-assurance-accounting.v1',
              'completed': 0, 'denominator': len(pages), 'ledger_sha256': ledger_sha,
              'version_include_and_render_assurance': None,
              'validated_page_ids': [], 'receipts_digest': digest(receipts),
              'policy_digest': digest(policy), 'semantic_truth_automatically_certified': False,
              'rights_cleared': False, 'native_behavior_verified': False,
              'policy_adopted': False,
              'scope': 'Validated authorized assurance attestations only; reviewer judgments are not independently proved by machine validation.'}
    if not receipts:
        return result
    _require(isinstance(policy, dict) and
             policy.get('schema') == 'ges.published-assurance-policy.v1',
             'Missing explicit published assurance policy')
    _require(isinstance(policy.get('approval_reference'), str) and
             bool(policy['approval_reference'].strip()), 'Missing authority approval reference')
    for role in ('authorized_claim_authors', 'authorized_certifiers', 'authorized_omission_auditors'):
        _require(_strings(policy.get(role)), 'Invalid or absent authority role: ' + role)
    _require(cache is not None, 'Assurance needs durable acquired bodies')
    acquired = cached_pages(cache, pages, ledger_sha)
    source_index = {}
    for line in artifacts.read_text().splitlines():
        item = json.loads(line)
        _require(isinstance(item, dict) and isinstance(item.get('artifact_id'), str),
                 'Malformed artifact inventory')
        identity = item['artifact_id']
        _require(identity not in source_index, 'Duplicate source artifact identity')
        source_index[identity] = item
    seen = set()
    claim_documents = {}
    for receipt in receipts:
        _require(isinstance(receipt, dict) and
                 receipt.get('schema') == 'ges.published-assurance-receipt.v1',
                 'Malformed assurance receipt')
        identity = receipt.get('page_id')
        _require(isinstance(identity, str) and identity in indexed and identity not in seen,
                 'Unknown or duplicate assurance page')
        page = indexed[identity]
        _require(identity in acquired, 'Page has no durable verified body')
        body = acquired[identity]
        _require(all(receipt.get(k) == page[k] for k in ('version', 'path')) and
                 receipt.get('ledger_sha256') == ledger_sha and
                 receipt.get('body_sha256') == body['sha256'], 'Page, ledger or body mismatch')
        source = receipt.get('source_identity')
        _require(isinstance(source, dict) and set(source) == set(SOURCE_KEYS) and
                 all(isinstance(source[k], str) and bool(source[k]) for k in SOURCE_KEYS),
                 'Malformed source identity')
        artifact = source_index.get(source['artifact_id'])
        _require(artifact is not None and
                 all(source[k] == artifact.get(k) for k in SOURCE_KEYS) and
                 source['source'] == 'github/docs' and
                 pins.get(source['source']) == source['commit'], 'Source does not match locked Docs inventory')
        _require(isinstance(page.get('source_matches'), list) and
                 source['artifact_id'] in page['source_matches'],
                 'No declared source mapping; basename or supplemental match is insufficient')
        author, reviewer, auditor = (receipt.get(k) for k in
                                     ('claim_author', 'reviewer', 'independent_auditor'))
        _require(author in policy['authorized_claim_authors'] and
                 reviewer in policy['authorized_certifiers'] and
                 auditor in policy['authorized_omission_auditors'], 'Unauthorized assurance role')
        _require(len({author, reviewer, auditor}) == 3, 'Assurance roles must be independent')
        reviewed, retrieved = _time(receipt.get('reviewed_at')), _time(body['retrieved_at'])
        _require(retrieved <= reviewed <= _time(now()), 'Review is future or precedes acquisition')
        claims = receipt.get('claims')
        _require(isinstance(claims, list) and bool(claims), 'Missing digest-bound claim documents')
        local_claim_documents = set()
        for reference in claims:
            doc = _evidence(evidence_root, reference)
            target = evidence_root.resolve() / reference['path']
            _require(target not in local_claim_documents, 'Duplicate claim document in receipt')
            local_claim_documents.add(target)
            _require(doc.get('reviewer') == author and
                     _time(doc.get('reviewed_at')) <= reviewed and
                     any(isinstance(i, dict) and i.get('page_id') == identity
                         for i in doc.get('instances', [])), 'Claim author, timestamp or page scope mismatch')
            _require(target not in claim_documents or
                     claim_documents[target] == reference['sha256'],
                     'Conflicting digests for one claim document')
            claim_documents[target] = reference['sha256']
        evidence = receipt.get('evidence')
        _require(isinstance(evidence, dict) and set(evidence) == set(KINDS),
                 'Missing or unsupported assurance evidence kinds')
        for kind in KINDS:
            doc = _evidence(evidence_root, evidence[kind])
            _require(doc.get('schema') == 'ges.published-assurance-evidence.v1' and
                     doc.get('kind') == kind and doc.get('page_id') == identity and
                     doc.get('ledger_sha256') == ledger_sha and
                     doc.get('body_sha256') == body['sha256'] and
                     doc.get('source_identity') == source and
                     doc.get('claims') == claims, 'Evidence scope or claim-set mismatch')
            expected = auditor if kind == 'independent_omission_audit' else reviewer
            _require(doc.get('reviewer') == expected, 'Evidence reviewer role mismatch')
            _require(retrieved <= _time(doc.get('reviewed_at')) <= reviewed,
                     'Evidence timestamp outside review scope')
            _require(doc.get('outcome') == 'PASS' and doc.get('unresolved') == [] and
                     isinstance(doc.get('method'), str) and bool(doc['method'].strip()) and
                     _strings(doc.get('observations')), 'Evidence is incomplete or unverified')
        seen.add(identity)
    provenance = validate_published_claims(ledger, cache, sorted(claim_documents),
                                           policy['authorized_claim_authors'])
    _require({Path(r['path']): r['sha256'] for r in provenance['review_documents']} ==
             claim_documents, 'Claim document changed between digest and provenance validation')
    result.update(completed=len(seen), validated_page_ids=sorted(seen),
                  version_include_and_render_assurance=len(seen) == len(pages),
                  claim_provenance_validated=provenance['valid'],
                  reference_claims=provenance['reference_claims'])
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--ledger', type=Path, required=True)
    parser.add_argument('--cache', type=Path, required=True)
    parser.add_argument('--artifacts', type=Path, required=True)
    parser.add_argument('--receipts', type=Path, required=True)
    parser.add_argument('--policy', type=Path, required=True)
    parser.add_argument('--pins', type=Path, default=ROOT / 'sources/sources.lock.json')
    args = parser.parse_args()
    try:
        pins = {p['repository']: p['commit'] for p in json.loads(args.pins.read_text())['sources']}
        result = assurance_accounting(args.ledger, args.cache, args.artifacts,
                                      json.loads(args.receipts.read_text()),
                                      json.loads(args.policy.read_text()), pins)
    except (ValueError, KeyError, TypeError, OSError, UnicodeError, RuntimeError) as exc:
        print(json.dumps({'valid': False, 'error': str(exc)}))
        return 2
    print(json.dumps({'valid': True, **result}))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
