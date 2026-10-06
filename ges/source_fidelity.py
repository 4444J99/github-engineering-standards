"""Validate source-fidelity certificates without inferring semantic truth.

Artifact dispositions and reference-claim provenance are inputs, not
certificates.  A separately approved authority policy and two independent,
digest-bound audits are required before the two recovery prerequisites can be
reported true.  The accountable auditors remain responsible for their
judgments.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from tempfile import TemporaryDirectory

from .claim_review import validate_provenance
from .core import ROOT, digest, now
from .corpus import coverage_with_reviews
from .published_assurance import _evidence, _require, _strings, _time

KINDS = (
    'atomic_claim_fidelity_audit',
    'independent_source_to_claim_omission_audit',
)
POLICY_SCHEMA = 'ges.source-fidelity-authority-policy.v1'
RECEIPT_SCHEMA = 'ges.source-fidelity-certification-receipt.v1'
EVIDENCE_SCHEMA = 'ges.source-fidelity-evidence.v1'
POLICY_FIELDS = {
    'schema', 'approval_reference', 'subject', 'authorized_fidelity_auditors',
    'authorized_independent_omission_auditors',
}
RECEIPT_FIELDS = {
    'schema', 'subject', 'fidelity_auditor', 'independent_omission_auditor',
    'certified_at', 'evidence',
}
EVIDENCE_FIELDS = {
    'schema', 'kind', 'identity', 'subject', 'reviewed_at', 'outcome',
    'unresolved', 'method', 'observations',
}
MAX_METHOD_CHARS = 4_000
MAX_OBSERVATIONS = 100
MAX_OBSERVATION_CHARS = 4_000


def _jsonl(path: Path, label: str) -> list[dict]:
    rows = []
    for number, line in enumerate(path.read_text(encoding='utf-8').splitlines(), 1):
        if not line.strip():
            continue
        row = json.loads(line)
        _require(isinstance(row, dict), f'{label} row {number} must be an object')
        rows.append(row)
    return rows


def _file_sha256(path: Path) -> str:
    _require(path.is_file() and not path.is_symlink(),
             'Evidence input is missing or symlinked: ' + str(path))
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def _snapshot_manifest(sources: Path, pins: dict[str, str]) -> list[dict]:
    """Bind the actual compressed source bytes, not only their release pins."""
    return [{'path': source.replace('/', '__') + '.text.jsonl.gz',
             'sha256': _file_sha256(
                 sources / (source.replace('/', '__') + '.text.jsonl.gz'))}
            for source in sorted(pins)]


def _review_records(reviews: Path) -> tuple[list[dict], list[dict]]:
    _require(reviews.is_dir(), 'Source-review directory is missing')
    records = []
    manifest = []
    for path in sorted(reviews.glob('*.json')):
        manifest.append({'path': path.name, 'sha256': _file_sha256(path)})
        if path.name.endswith('-claims.json'):
            continue
        document = json.loads(path.read_text(encoding='utf-8'))
        _require(isinstance(document, list),
                 'Source-review receipt file must contain an array: ' + path.name)
        records.extend(document)
    return records, manifest


def _valid_sha(value: object) -> bool:
    return isinstance(value, str) and re.fullmatch(r'[a-f0-9]{64}', value) is not None


def _validate_inputs(artifacts: list[dict], candidates: list[dict],
                     controls: list[dict], pins: dict[str, str]) -> None:
    _require(isinstance(controls, list) and isinstance(pins, dict),
             'Catalog and source pins must be structured inputs')
    control_ids = []
    for control in controls:
        _require(isinstance(control, dict) and isinstance(control.get('id'), str) and
                 bool(control['id']) and type(control.get('revision')) is int,
                 'Malformed canonical control')
        control_ids.append(control['id'])
    _require(len(control_ids) == len(set(control_ids)), 'Duplicate canonical control identity')

    artifact_ids = set()
    artifact_identities = set()
    for artifact in artifacts:
        _require(all(isinstance(artifact.get(key), str) and bool(artifact[key])
                     for key in ('artifact_id', 'source', 'commit', 'path', 'sha256')),
                 'Malformed source artifact')
        _require(_valid_sha(artifact['sha256']), 'Invalid artifact content digest')
        _require(pins.get(artifact['source']) == artifact['commit'],
                 'Artifact differs from locked source pin')
        identity = (artifact['source'], artifact['commit'], artifact['path'], artifact['sha256'])
        _require(artifact['artifact_id'] not in artifact_ids and identity not in artifact_identities,
                 'Duplicate source artifact identity')
        artifact_ids.add(artifact['artifact_id'])
        artifact_identities.add(identity)

    candidate_ids = set()
    for candidate in candidates:
        _require(isinstance(candidate.get('candidate_id'), str) and
                 bool(candidate['candidate_id']) and
                 candidate.get('artifact_id') in artifact_ids and
                 _valid_sha(candidate.get('text_sha256')),
                 'Malformed or foreign candidate')
        _require(candidate['candidate_id'] not in candidate_ids,
                 'Duplicate candidate identity')
        candidate_ids.add(candidate['candidate_id'])


def _claim_document_state(references: list[dict]) -> tuple[list[dict], object | None]:
    normalized = []
    times = []
    for reference in sorted(references, key=lambda item: item['path']):
        _require(isinstance(reference, dict) and
                 set(reference) == {'path', 'sha256'} and
                 _valid_sha(reference.get('sha256')), 'Malformed claim-document reference')
        path = Path(reference['path'])
        _require(path.is_file() and not path.is_symlink(), 'Claim document is missing or symlinked')
        raw = path.read_bytes()
        _require(hashlib.sha256(raw).hexdigest() == reference['sha256'],
                 'Claim document changed after provenance validation')
        document = json.loads(raw)
        _require(isinstance(document, dict), 'Claim document must be an object')
        times.append(_time(document.get('reviewed_at')))
        normalized.append({'path': reference['path'], 'sha256': reference['sha256']})
    return normalized, max(times) if times else None


def _bounded_evidence(document: dict) -> bool:
    method = document.get('method')
    observations = document.get('observations')
    return (isinstance(method, str) and 0 < len(method.strip()) <= MAX_METHOD_CHARS and
            _strings(observations) and len(observations) <= MAX_OBSERVATIONS and
            all(len(item) <= MAX_OBSERVATION_CHARS for item in observations))


def _validate_policy(policy: object, subject: dict) -> dict:
    _require(isinstance(policy, dict) and set(policy) == POLICY_FIELDS and
             policy.get('schema') == POLICY_SCHEMA,
             'Missing explicit source-fidelity authority policy')
    _require(isinstance(policy.get('approval_reference'), str) and
             bool(policy['approval_reference'].strip()), 'Missing authority approval reference')
    _require(digest(policy.get('subject')) == digest(subject),
             'Authority policy input digests changed')
    for role in ('authorized_fidelity_auditors',
                 'authorized_independent_omission_auditors'):
        _require(_strings(policy.get(role)), 'Invalid or absent authority role: ' + role)
    return policy


def source_fidelity_accounting(
        artifacts_path: Path, candidates_path: Path, reviews: Path,
        review_policy: dict, sources: Path, controls: list[dict],
        pins: dict[str, str], certification_receipts: list[dict] | None = None,
        certification_policy: dict | None = None, *,
        proposals: list[dict] | None = None, evidence_root: Path = ROOT) -> dict:
    """Return fail-closed artifact/claim accounting and optional audit outcomes."""
    artifacts = _jsonl(artifacts_path, 'Artifact inventory')
    candidates = _jsonl(candidates_path, 'Candidate ledger')
    proposal_records = [] if proposals is None else proposals
    _require(isinstance(proposal_records, list), 'Proposal queue must be an array')
    _validate_inputs(artifacts, candidates, [*controls, *proposal_records], pins)
    _require(isinstance(review_policy, dict) and
             _strings(review_policy.get('authorized_reviewers')),
             'Missing source-review authority policy')
    inventory_sha256 = _file_sha256(artifacts_path)
    candidate_ledger_sha256 = _file_sha256(candidates_path)
    reviews_list, source_review_documents = _review_records(reviews)
    source_snapshots = (_snapshot_manifest(sources, pins)
                        if any(reviews.glob('*-claims.json')) else [])

    with TemporaryDirectory() as temporary:
        aggregate = Path(temporary) / 'reviews.json'
        aggregate.write_text(json.dumps(reviews_list), encoding='utf-8')
        review_accounting = coverage_with_reviews(
            artifacts_path, aggregate, candidates=candidates, controls=controls,
            authorized_reviewers=review_policy['authorized_reviewers'],
            evidence_root=evidence_root)
    _require(review_accounting['errors'] == [],
             'Invalid source-review receipts: ' + repr(review_accounting['errors']))

    claim_files = sorted(reviews.glob('*-claims.json'))
    if claim_files:
        provenance = validate_provenance(
            artifacts_path, sources, reviews, review_policy['authorized_reviewers'],
            pins, {control['id'] for control in [*controls, *proposal_records]})
        claim_documents, latest_claim_review = _claim_document_state(
            provenance['review_documents'])
    else:
        provenance = {
            'valid': False,
            'reference_claims': 0,
            'source_artifacts': 0,
            'review_documents': [],
            'semantic_truth_certified': False,
            'omission_completeness_certified': False,
            'rights_cleared': False,
            'policy_adopted': False,
        }
        claim_documents, latest_claim_review = [], None

    source_review_times = [_time(record.get('reviewed_at')) for record in reviews_list]
    latest_input_review = max(
        [value for value in [latest_claim_review, *source_review_times] if value is not None],
        default=None)
    inventoried = review_accounting['inventoried']
    reviewed = review_accounting['reviewed']
    coverage_complete = None if inventoried == 0 else reviewed == inventoried
    subject = {
        'inventory_sha256': inventory_sha256,
        'inventory_digest': digest(artifacts),
        'candidate_ledger_sha256': candidate_ledger_sha256,
        'candidate_ledger_digest': digest(candidates),
        'source_review_documents_digest': digest(source_review_documents),
        'source_review_document_count': len(source_review_documents),
        'source_review_receipts_digest': digest(reviews_list),
        'source_review_accounting_digest': digest(review_accounting),
        'source_review_policy_digest': digest(review_policy),
        'source_pins_digest': digest(pins),
        'source_snapshots_digest': digest(source_snapshots),
        'catalog_digest': digest(controls),
        'proposal_digest': digest(proposal_records),
        'claim_documents_digest': digest(claim_documents),
        'claim_provenance_digest': digest(provenance),
        'inventory_count': inventoried,
        'candidate_count': len(candidates),
        'reviewed_count': reviewed,
        'coverage_complete': coverage_complete,
        'claim_document_count': len(claim_documents),
        'reference_claim_count': provenance['reference_claims'],
    }
    _require((certification_receipts is None) == (certification_policy is None),
             'Certification receipts and authority policy must be supplied together')
    receipts = [] if certification_receipts is None else certification_receipts
    policy = {} if certification_policy is None else certification_policy
    _require(isinstance(receipts, list), 'Certification receipts must be an array')
    result = {
        'schema': 'ges.source-fidelity-accounting.v1',
        'reviewed': reviewed,
        'inventoried': inventoried,
        'remaining': inventoried - reviewed,
        'coverage_complete': coverage_complete,
        'candidate_count': len(candidates),
        'reference_claims': provenance['reference_claims'],
        'claim_provenance_validated': provenance['valid'],
        'reviewed_claim_documents': claim_documents,
        'subject': subject,
        'atomic_claim_fidelity_audit': None,
        'independent_source_to_claim_omission_audit': None,
        'validated_evidence': {},
        'validated_evidence_digest': digest({}),
        'certification_receipts_digest': digest(receipts),
        'certification_policy_digest': digest(policy),
        'semantic_truth_automatically_certified': False,
        'rights_cleared': False,
        'policy_adopted': False,
        'evaluation': ('INCOMPLETE' if coverage_complete is False else 'UNVERIFIED'),
        'scope': ('Validated gate-prerequisite attestations only; counts and machine '
                  'validation do not prove semantic truth or omission-free review.'),
    }
    if certification_policy is not None:
        policy = _validate_policy(policy, subject)
    if not receipts:
        return result

    _require(len(receipts) == 1, 'Exactly one corpus certification receipt is required')
    _require(coverage_complete is True and inventoried > 0,
             'Certification cannot pass incomplete or zero artifact coverage')
    _require(provenance['valid'] is True and bool(claim_documents),
             'Certification requires validated reviewed claim documents')
    receipt = receipts[0]
    _require(isinstance(receipt, dict) and set(receipt) == RECEIPT_FIELDS and
             receipt.get('schema') == RECEIPT_SCHEMA,
             'Malformed source-fidelity certification receipt')
    _require(digest(receipt.get('subject')) == digest(subject),
             'Certification subject or count changed')
    fidelity = receipt.get('fidelity_auditor')
    omission = receipt.get('independent_omission_auditor')
    _require(fidelity in policy['authorized_fidelity_auditors'] and
             omission in policy['authorized_independent_omission_auditors'],
             'Unauthorized source-fidelity certification role')
    _require(fidelity != omission, 'Fidelity and omission auditors must be distinct')
    certified_at = _time(receipt.get('certified_at'))
    current_time = _time(now())
    _require(certified_at <= current_time and
             (latest_input_review is None or latest_input_review <= certified_at),
             'Certification timestamp is future or predates reviewed inputs')
    references = receipt.get('evidence')
    _require(isinstance(references, dict) and set(references) == set(KINDS),
             'Missing or unsupported source-fidelity evidence kinds')
    validated = {}
    for kind in KINDS:
        reference = references[kind]
        document = _evidence(evidence_root, reference)
        expected_identity = fidelity if kind == KINDS[0] else omission
        _require(set(document) == EVIDENCE_FIELDS and
                 document.get('schema') == EVIDENCE_SCHEMA and
                 document.get('kind') == kind and
                 document.get('identity') == expected_identity and
                 digest(document.get('subject')) == digest(subject),
                 'Source-fidelity evidence identity or subject mismatch')
        reviewed_at = _time(document.get('reviewed_at'))
        _require((latest_input_review is None or latest_input_review <= reviewed_at) and
                 reviewed_at <= certified_at,
                 'Audit evidence timestamp is outside reviewed input scope')
        _require(document.get('outcome') == 'PASS' and
                 document.get('unresolved') == [] and
                 _bounded_evidence(document),
                 'Audit evidence is incomplete, unbounded or unverified')
        validated[kind] = {'path': reference['path'], 'sha256': reference['sha256']}

    # Re-read all advertised evidence and claims to detect substitution during validation.
    for kind in KINDS:
        _evidence(evidence_root, validated[kind])
    final_claim_documents, _ = _claim_document_state(claim_documents)
    _require(final_claim_documents == claim_documents,
             'Claim document changed during certification validation')
    _require(_file_sha256(artifacts_path) == inventory_sha256 and
             _file_sha256(candidates_path) == candidate_ledger_sha256 and
             _review_records(reviews)[1] == source_review_documents and
             _snapshot_manifest(sources, pins) == source_snapshots,
             'Certification input changed during validation')
    result.update({
        'atomic_claim_fidelity_audit': True,
        'independent_source_to_claim_omission_audit': True,
        'validated_evidence': validated,
        'validated_evidence_digest': digest(validated),
        'fidelity_auditor': fidelity,
        'independent_omission_auditor': omission,
        'certified_at': receipt['certified_at'],
        'evaluation': 'PREREQUISITES_VALIDATED',
    })
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--artifacts', type=Path, required=True)
    parser.add_argument('--candidates', type=Path, required=True)
    parser.add_argument('--reviews', type=Path, required=True)
    parser.add_argument('--review-policy', type=Path, required=True)
    parser.add_argument('--sources', type=Path, required=True)
    parser.add_argument('--catalog', type=Path, required=True)
    parser.add_argument('--proposals', type=Path,
                        default=ROOT / 'controls/review_queue.json')
    parser.add_argument('--pins', type=Path, default=ROOT / 'sources/sources.lock.json')
    parser.add_argument('--certification-receipts', type=Path)
    parser.add_argument('--certification-policy', type=Path)
    parser.add_argument('--evidence-root', type=Path, default=ROOT)
    args = parser.parse_args()
    try:
        _require((args.certification_receipts is None) ==
                 (args.certification_policy is None),
                 'Certification receipts and authority policy must be supplied together')
        pin_document = json.loads(args.pins.read_text(encoding='utf-8'))
        pins = {item['repository']: item['commit'] for item in pin_document['sources']}
        result = source_fidelity_accounting(
            args.artifacts, args.candidates, args.reviews,
            json.loads(args.review_policy.read_text(encoding='utf-8')),
            args.sources, json.loads(args.catalog.read_text(encoding='utf-8')), pins,
            (json.loads(args.certification_receipts.read_text(encoding='utf-8'))
             if args.certification_receipts else None),
            (json.loads(args.certification_policy.read_text(encoding='utf-8'))
             if args.certification_policy else None),
            proposals=json.loads(args.proposals.read_text(encoding='utf-8')),
            evidence_root=args.evidence_root)
    except (ValueError, KeyError, TypeError, OSError, UnicodeError, RuntimeError) as exc:
        print(json.dumps({'valid': False, 'error': str(exc)}))
        return 2
    print(json.dumps({'valid': True, **result}))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
