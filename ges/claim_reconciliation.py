"""Validate explicit claim reconciliation receipts without generating mappings.

The adapter proves receipt integrity, exact input binding and authorized independent
review. It does not prove semantic truth, extraction completeness, rights, policy
adoption or native enforcement.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from datetime import datetime
from pathlib import Path

from .claim_review import validate_provenance
from .core import ROOT, digest, now, timestamp

DISPOSITIONS = ('MAP', 'SPECIALIZE', 'CONFLICT', 'REFERENCE',
                'EXCLUDED_WITH_REASON')
SUBJECT_FIELDS = ('claim_id', 'source', 'commit', 'path', 'artifact_id',
                  'content_sha256', 'start_line', 'end_line',
                  'statement_sha256', 'claim_document',
                  'claim_document_sha256')
POLICY_FIELDS = {'schema', 'approval_reference', 'claim_input_digest',
                 'catalog_digest', 'proposal_digest', 'authorized_reconcilers',
                 'authorized_independent_reviewers'}
RECEIPT_FIELDS = {'schema', 'claim', 'claim_input_digest', 'catalog_digest',
                  'proposal_digest', 'disposition', 'control_references',
                  'details', 'rationale', 'reconciler', 'independent_reviewer',
                  'reconciled_at', 'reviewed_at', 'accepted_policy',
                  'adopted_obligation'}
CONTROL_REFERENCE_FIELDS = {'id', 'revision', 'collection'}
EXCLUSION_BASES = {'NON_ACTIONABLE', 'DUPLICATE', 'OUT_OF_SCOPE',
                   'SUPERSEDED', 'UNSUPPORTED_SOURCE'}


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def _text(value) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _strings(value, *, empty: bool = False) -> bool:
    return (isinstance(value, list) and (empty or bool(value)) and
            all(_text(item) for item in value) and len(value) == len(set(value)))


def _time(value) -> datetime:
    _require(_text(value), 'Missing reconciliation timestamp')
    return timestamp(value)


def _sha(value) -> bool:
    return isinstance(value, str) and re.fullmatch('[a-f0-9]{64}', value) is not None


def _control_index(records: list[dict], collection: str) -> dict[str, dict]:
    _require(isinstance(records, list), collection + ' controls must be an array')
    indexed = {}
    for record in records:
        _require(isinstance(record, dict) and _text(record.get('id')) and
                 type(record.get('revision')) is int and record['revision'] >= 1,
                 'Malformed ' + collection.lower() + ' control identity')
        _require(record['id'] not in indexed,
                 'Duplicate ' + collection.lower() + ' control identity')
        indexed[record['id']] = record
    return indexed


def _known_claims(artifacts: Path, reviews: Path, provenance: dict) -> tuple[list[dict], dict[str, datetime]]:
    rows = [json.loads(line) for line in artifacts.read_text().splitlines()
            if line.strip()]
    artifact_index = {(row['source'], row['commit'], row['path']): row for row in rows}
    _require(len(artifact_index) == len(rows), 'Duplicate artifact identity')
    provenance_documents = {item['path']: item['sha256']
                            for item in provenance['review_documents']}
    subjects = []
    ready_at = {}
    for path in sorted(reviews.glob('*-claims.json')):
        raw = path.read_bytes()
        document_sha = hashlib.sha256(raw).hexdigest()
        _require(provenance_documents.get(str(path)) == document_sha,
                 'Claim document changed after provenance validation')
        document = json.loads(raw)
        document_time = _time(document.get('reviewed_at'))
        for claim in document['claims']:
            source, commit, source_path = (claim.get(key, document.get(key))
                                           for key in ('source', 'commit', 'path'))
            artifact = artifact_index[(source, commit, source_path)]
            claim_id = claim['claim_id']
            _require(_text(artifact.get('artifact_id')) and
                     _sha(artifact.get('sha256')), 'Malformed claim artifact identity')
            subject = {
                'claim_id': claim_id,
                'source': source,
                'commit': commit,
                'path': source_path,
                'artifact_id': artifact['artifact_id'],
                'content_sha256': artifact['sha256'],
                'start_line': claim['start_line'],
                'end_line': claim['end_line'],
                'statement_sha256': hashlib.sha256(
                    claim['statement'].encode()).hexdigest(),
                'claim_document': path.relative_to(reviews).as_posix(),
                'claim_document_sha256': document_sha,
            }
            _require(set(subject) == set(SUBJECT_FIELDS), 'Malformed known claim subject')
            subjects.append(subject)
            claim_time = _time(claim.get('reviewed_at', document.get('reviewed_at')))
            ready_at[claim_id] = max(document_time, claim_time)
    subjects.sort(key=lambda item: item['claim_id'])
    _require(len(subjects) == provenance['reference_claims'] and
             len({item['claim_id'] for item in subjects}) == len(subjects),
             'Known claim set differs from provenance validation')
    for item in provenance['review_documents']:
        _require(hashlib.sha256(Path(item['path']).read_bytes()).hexdigest() ==
                 item['sha256'], 'Claim document changed during reconciliation')
    return subjects, ready_at


def _control_references(value, controls: dict[str, dict],
                        proposals: dict[str, dict]) -> list[dict]:
    _require(isinstance(value, list), 'Control references must be an array')
    seen = set()
    for reference in value:
        _require(isinstance(reference, dict) and
                 set(reference) == CONTROL_REFERENCE_FIELDS,
                 'Unsupported control reference fields')
        collection = reference.get('collection')
        _require(collection in {'CATALOG', 'PROPOSAL'},
                 'Unknown control reference collection')
        index = controls if collection == 'CATALOG' else proposals
        control_id = reference.get('id')
        _require(_text(control_id) and control_id in index,
                 'Unknown control identity: ' + str(control_id))
        _require(type(reference.get('revision')) is int and
                 reference['revision'] == index[control_id]['revision'],
                 'Control revision changed: ' + control_id)
        identity = (collection, control_id)
        _require(identity not in seen, 'Duplicate control reference')
        seen.add(identity)
    return value


def _claim_ids(value, known: set[str], own: str, label: str,
               *, empty: bool = False) -> list[str]:
    _require(_strings(value, empty=empty), 'Invalid ' + label)
    _require(own not in value and all(item in known for item in value),
             'Unknown or self-referential ' + label)
    return value


def _validate_disposition(receipt: dict, known: set[str],
                          controls: dict[str, dict], proposals: dict[str, dict]) -> None:
    disposition = receipt.get('disposition')
    _require(disposition in DISPOSITIONS, 'Unsupported claim disposition')
    references = _control_references(receipt.get('control_references'),
                                     controls, proposals)
    details = receipt.get('details')
    _require(isinstance(details, dict), 'Disposition details must be an object')
    claim_id = receipt['claim']['claim_id']
    if disposition == 'MAP':
        _require(bool(references) and
                 all(item['collection'] == 'CATALOG' for item in references) and
                 details == {}, 'MAP requires canonical catalog controls and empty details')
    elif disposition == 'SPECIALIZE':
        _require(any(item['collection'] == 'PROPOSAL' for item in references) and
                 set(details) == {'scope', 'distinction'} and
                 _text(details.get('scope')) and _text(details.get('distinction')),
                 'SPECIALIZE requires a proposal, scope and distinction')
    elif disposition == 'CONFLICT':
        _require(set(details) == {'conflicting_claim_ids', 'resolution'} and
                 _text(details.get('resolution')), 'CONFLICT requires an exact resolution')
        _claim_ids(details.get('conflicting_claim_ids'), known, claim_id,
                   'conflicting claim identities')
    elif disposition == 'REFERENCE':
        _require(not references and set(details) == {'reference_reason'} and
                 _text(details.get('reference_reason')),
                 'REFERENCE requires a reason and no control mapping')
    else:
        _require(not references and set(details) ==
                 {'basis', 'exclusion_reason', 'related_claim_ids'} and
                 details.get('basis') in EXCLUSION_BASES and
                 _text(details.get('exclusion_reason')),
                 'EXCLUDED_WITH_REASON requires an explicit supported basis and reason')
        related = _claim_ids(details.get('related_claim_ids'), known, claim_id,
                             'related claim identities', empty=True)
        if details['basis'] in {'DUPLICATE', 'SUPERSEDED'}:
            _require(bool(related), details['basis'] + ' requires a related claim')
        else:
            _require(not related, details['basis'] + ' cannot invent related claims')


def _validate_policy(policy: object, input_digest: str,
                     catalog_digest: str, proposal_digest: str) -> dict:
    _require(isinstance(policy, dict) and set(policy) == POLICY_FIELDS and
             policy.get('schema') == 'ges.claim-reconciliation-policy.v1',
             'Missing or unsupported claim reconciliation authority policy')
    _require(_text(policy.get('approval_reference')),
             'Missing reconciliation policy approval reference')
    for field in ('authorized_reconcilers', 'authorized_independent_reviewers'):
        _require(_strings(policy.get(field)), 'Invalid authority role: ' + field)
    _require(policy.get('claim_input_digest') == input_digest and
             policy.get('catalog_digest') == catalog_digest and
             policy.get('proposal_digest') == proposal_digest,
             'Authority policy does not bind exact reconciliation inputs')
    return policy


def reconciliation_accounting(artifacts: Path, sources: Path, reviews: Path,
                              review_policy: dict, pins: dict[str, str],
                              catalog: list[dict], proposals: list[dict],
                              receipts: list[dict] | None,
                              policy: dict | None) -> dict:
    """Return deterministic accounting for exact, independently reviewed receipts."""
    _require(isinstance(review_policy, dict) and
             _strings(review_policy.get('authorized_reviewers')),
             'Invalid source review policy')
    _require(isinstance(pins, dict) and bool(pins), 'Invalid locked source pins')
    controls = _control_index(catalog, 'CATALOG')
    proposal_index = _control_index(proposals, 'PROPOSAL')
    _require(not (set(controls) & set(proposal_index)),
             'Control identity appears in catalog and proposal queue')

    artifact_sha = hashlib.sha256(artifacts.read_bytes()).hexdigest()
    provenance = validate_provenance(
        artifacts, sources, reviews, review_policy['authorized_reviewers'], pins,
        set(controls) | set(proposal_index))
    _require(provenance.get('valid') is True, 'Claim provenance did not validate')
    _require(hashlib.sha256(artifacts.read_bytes()).hexdigest() == artifact_sha,
             'Artifact inventory changed during provenance validation')
    subjects, ready_at = _known_claims(artifacts, reviews, provenance)

    input_digest = digest(subjects)
    catalog_digest = digest(catalog)
    proposal_digest = digest(proposals)
    policy_supplied = policy is not None
    _require((receipts is None) == (not policy_supplied),
             'Reconciliation receipts and authority policy must be supplied together')
    receipts = [] if receipts is None else receipts
    policy = {} if policy is None else policy
    _require(isinstance(receipts, list), 'Reconciliation receipts must be an array')
    counts = Counter({name: 0 for name in DISPOSITIONS})
    result = {
        'schema': 'ges.claim-reconciliation-accounting.v1',
        'known_claim_denominator': len(subjects),
        'validated_count': 0,
        'unresolved_count': len(subjects),
        'disposition_counts': dict(counts),
        'validated_claim_ids': [],
        'claim_input_digest': input_digest,
        'catalog_digest': catalog_digest,
        'proposal_digest': proposal_digest,
        'receipts_digest': digest(receipts),
        'policy_digest': digest(policy),
        'claim_provenance_validated': True,
        'mapping_complete': False,
        'semantic_truth_automatically_certified': False,
        'source_to_claim_omission_denominator_certified': False,
        'rights_cleared': False,
        'policy_adopted': False,
        'scope': ('Validated exact-claim reconciliation receipts only; no mapping '
                  'is generated and independent gate evidence remains required.'),
    }
    if policy_supplied:
        policy = _validate_policy(policy, input_digest, catalog_digest, proposal_digest)
    if not receipts:
        return result

    indexed = {item['claim_id']: item for item in subjects}
    known_ids = set(indexed)
    seen = set()
    current = _time(now())
    for receipt in receipts:
        _require(isinstance(receipt, dict) and set(receipt) == RECEIPT_FIELDS and
                 receipt.get('schema') == 'ges.claim-reconciliation-receipt.v1',
                 'Malformed or unsupported reconciliation receipt')
        subject = receipt.get('claim')
        _require(isinstance(subject, dict) and set(subject) == set(SUBJECT_FIELDS),
                 'Malformed claim reconciliation subject')
        claim_id = subject.get('claim_id')
        _require(_text(claim_id) and claim_id in indexed and claim_id not in seen,
                 'Foreign or duplicate reconciliation receipt')
        _require(subject == indexed[claim_id], 'Known claim changed')
        _require(receipt.get('claim_input_digest') == input_digest and
                 receipt.get('catalog_digest') == catalog_digest and
                 receipt.get('proposal_digest') == proposal_digest,
                 'Receipt does not bind exact reconciliation inputs')
        reconciler = receipt.get('reconciler')
        reviewer = receipt.get('independent_reviewer')
        _require(reconciler in policy['authorized_reconcilers'] and
                 reviewer in policy['authorized_independent_reviewers'],
                 'Unauthorized reconciliation role')
        _require(reconciler != reviewer, 'Reconciler and reviewer must be independent')
        reconciled_at = _time(receipt.get('reconciled_at'))
        reviewed_at = _time(receipt.get('reviewed_at'))
        _require(ready_at[claim_id] <= reconciled_at <= reviewed_at <= current,
                 'Reconciliation timestamp is future or out of order')
        _require(receipt.get('accepted_policy') is False and
                 receipt.get('adopted_obligation') is None,
                 'Reconciliation receipt cannot assert policy adoption')
        _require(_text(receipt.get('rationale')), 'Missing reconciliation rationale')
        _validate_disposition(receipt, known_ids, controls, proposal_index)
        seen.add(claim_id)
        counts[receipt['disposition']] += 1

    result.update(
        validated_count=len(seen),
        unresolved_count=len(subjects) - len(seen),
        disposition_counts=dict(counts),
        validated_claim_ids=sorted(seen),
        mapping_complete=len(seen) == len(subjects),
    )
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--artifacts', type=Path, required=True)
    parser.add_argument('--sources', type=Path, required=True)
    parser.add_argument('--reviews', type=Path, required=True)
    parser.add_argument('--review-policy', type=Path, required=True)
    parser.add_argument('--receipts', type=Path)
    parser.add_argument('--policy', type=Path)
    parser.add_argument('--pins', type=Path, default=ROOT / 'sources/sources.lock.json')
    parser.add_argument('--catalog', type=Path, default=ROOT / 'controls/catalog.json')
    parser.add_argument('--proposals', type=Path, default=ROOT / 'controls/review_queue.json')
    args = parser.parse_args()
    try:
        _require((args.receipts is None) == (args.policy is None),
                 'Reconciliation receipts and authority policy must be supplied together')
        pins = {item['repository']: item['commit']
                for item in json.loads(args.pins.read_text())['sources']}
        report = reconciliation_accounting(
            args.artifacts, args.sources, args.reviews,
            json.loads(args.review_policy.read_text()), pins,
            json.loads(args.catalog.read_text()),
            json.loads(args.proposals.read_text()),
            json.loads(args.receipts.read_text()) if args.receipts else None,
            json.loads(args.policy.read_text()) if args.policy else None)
    except (ValueError, KeyError, TypeError, OSError, UnicodeError,
            json.JSONDecodeError) as exc:
        print(json.dumps({'valid': False, 'error': str(exc)}))
        return 2
    print(json.dumps({'valid': True, **report}))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
