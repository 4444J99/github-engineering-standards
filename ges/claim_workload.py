"""Inventory recorded claims and propose review families; never award review credit."""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
from collections import Counter
from pathlib import Path

from .core import digest
from .pinned_sources import inventory_digest

PROVIDER_FIELDS = {
    'isPublic', 'isPrivateWithGhas', 'hasPushProtection', 'hasValidityCheck',
    'base64Supported', 'isduplicate', 'hasExtendedMetadata',
}
ARTIFACT_METADATA_FIELDS = {
    'artifact_id', 'candidate_count', 'commit', 'git_blob_sha', 'kind', 'path',
    'proposed_disposition', 'retrieval_status', 'retrieved_at', 'review_status',
    'sha256', 'size', 'source', 'url',
}


def _sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _artifact_bytes(path: Path) -> bytes:
    """Read the original JSONL bytes, optionally preserved in a gzip container."""
    raw = path.read_bytes()
    return gzip.decompress(raw) if path.suffix == '.gz' else raw


def _inventory_bytes(result: dict) -> bytes:
    return (json.dumps(result, indent=2) + '\n').encode('utf-8')


def inventory(reviews: Path, artifacts: Path, reconciliation: Path) -> dict:
    """Count an immutable occurrence inventory, including all family members."""
    artifact_raw = _artifact_bytes(artifacts)
    records = [json.loads(line) for line in artifact_raw.splitlines() if line.strip()]
    indexed = {(a['source'], a['commit'], a['path']): a for a in records}
    if len(indexed) != len(records):
        raise ValueError('Duplicate artifact identity')
    documents = []
    claims = {}
    groups = {}
    text_counts = Counter()
    spans = Counter()
    source_counts = Counter()
    strengths = Counter()
    provider_fields = Counter()
    provider_rows = set()
    provider_row_bindings = {}
    query_rows = set()
    counts = Counter()
    paths = sorted(reviews.glob('*-claims.json'))
    for path in paths:
        raw = path.read_bytes()
        document_sha = _sha(raw)
        doc = json.loads(raw)
        if not isinstance(doc.get('claims'), list) or not doc['claims']:
            raise ValueError('Missing claims: ' + path.name)
        documents.append({'path': path.name, 'sha256': document_sha,
                          'claims': len(doc['claims'])})
        for claim in doc['claims']:
            cid = claim.get('claim_id')
            statement = claim.get('statement')
            source, commit, source_path = (
                claim.get(k, doc.get(k)) for k in ('source', 'commit', 'path'))
            identity = (source, commit, source_path)
            start, end = claim.get('start_line'), claim.get('end_line')
            if (not isinstance(cid, str) or not cid.strip() or cid in claims or
                    not isinstance(statement, str) or not statement.strip() or
                    type(start) is not int or type(end) is not int or
                    not 1 <= start <= end or identity not in indexed):
                raise ValueError('Invalid or duplicate claim subject: ' + str(cid))
            artifact = indexed[identity]
            if (claim.get('artifact_id', doc.get('artifact_id', artifact['artifact_id'])) !=
                    artifact['artifact_id'] or
                    claim.get('content_sha256', doc.get('content_sha256', artifact['sha256'])) !=
                    artifact['sha256']):
                raise ValueError('Changed claim artifact binding: ' + cid)
            context = claim.get('context')
            context = context if isinstance(context, dict) else {}
            provider_keys = (
                'provider', 'raw_credential_identifier', 'source_field',
                'entry_ordinal', 'definition_start_line', 'definition_end_line')
            provider = all(k in context for k in provider_keys)
            if any(k in context for k in provider_keys) and not provider:
                raise ValueError('Incomplete provider field context: ' + cid)
            query = any(k in claim for k in ('query_occurrence', 'query_help_identity'))
            if query:
                if not all(k in claim for k in ('query_occurrence', 'query_help_identity')):
                    raise ValueError('Incomplete query row: ' + cid)
                occurrence = claim['query_occurrence']
                if (not isinstance(occurrence, str) or
                        occurrence != source_path + '#L' + str(start) or
                        not isinstance(claim['query_help_identity'], str) or
                        not claim['query_help_identity'].strip()):
                    raise ValueError('Malformed query row: ' + cid)
                if provider:
                    raise ValueError('Ambiguous provider and query context: ' + cid)
            if provider:
                if (not isinstance(context['source_field'], str) or
                        context['source_field'] not in PROVIDER_FIELDS or
                        any(not isinstance(context[k], str) or not context[k].strip()
                            for k in ('provider', 'raw_credential_identifier')) or
                        type(context['entry_ordinal']) is not int or
                        context['entry_ordinal'] < 1 or
                        type(context['definition_start_line']) is not int or
                        type(context['definition_end_line']) is not int or
                        not 1 <= context['definition_start_line'] <= start <= end <=
                        context['definition_end_line']):
                    raise ValueError('Malformed provider field: ' + cid)
                kind = 'PROVIDER_CAPABILITY_MATRIX'
                key = [source, commit, context['provider'],
                       context['raw_credential_identifier']]
                provider_fields[context['source_field']] += 1
                row_identity = (*identity, context['entry_ordinal'])
                row_binding = (
                    context['provider'], context['raw_credential_identifier'],
                    context['definition_start_line'], context['definition_end_line'])
                previous = provider_row_bindings.get(row_identity)
                if previous is not None and previous != row_binding:
                    raise ValueError('Conflicting provider row identity: ' + cid)
                provider_row_bindings[row_identity] = row_binding
                provider_rows.add(row_identity)
            elif query:
                kind = 'QUERY_TABLE_ROW'
                key = [source, commit, occurrence, claim['query_help_identity']]
                query_rows.add(tuple(key))
            else:
                kind = 'SOURCE_ARTIFACT_CONTEXT'
                key = list(identity)
            family_id = digest([kind, key])
            group = groups.setdefault(family_id, {
                'family_id': family_id, 'kind': kind, 'key': key,
                'claim_ids': [], 'reconciled_claim_ids': [],
                'semantic_equivalence_verified': False,
            })
            group['claim_ids'].append(cid)
            claims[cid] = {'source': source, 'commit': commit, 'path': source_path,
                           'start_line': start, 'end_line': end,
                           'artifact_id': artifact['artifact_id'],
                           'content_sha256': artifact['sha256'],
                           'statement_sha256': _sha(statement.encode()),
                           'claim_document': path.name,
                           'claim_document_sha256': document_sha,
                           'family_id': family_id}
            source_counts[source] += 1
            strengths[str(claim.get('source_strength', 'UNSPECIFIED'))] += 1
            text_counts[_sha(statement.encode())] += 1
            spans[(*identity, start, end)] += 1
            counts[kind] += 1
    if not claims:
        raise ValueError('Empty claim inventory')
    reconciliation_raw = reconciliation.read_bytes()
    receipts = json.loads(reconciliation_raw)
    reconciled = set()
    for receipt in receipts:
        subject = receipt['claim']
        cid = subject['claim_id']
        if cid not in claims or cid in reconciled:
            raise ValueError('Unknown or duplicate reconciliation subject')
        known = claims[cid]
        if any(subject[k] != known[k] for k in (
                'source', 'commit', 'path', 'start_line', 'end_line',
                'artifact_id', 'content_sha256', 'statement_sha256',
                'claim_document', 'claim_document_sha256')):
            raise ValueError('Changed reconciliation source subject: ' + cid)
        reconciled.add(cid)
        groups[known['family_id']]['reconciled_claim_ids'].append(cid)
    # Fail closed if an input changed while constructing the advisory queue.
    if sorted(reviews.glob('*-claims.json')) != paths:
        raise ValueError('Claim document membership changed during audit')
    for item in documents:
        if _sha((reviews / item['path']).read_bytes()) != item['sha256']:
            raise ValueError('Claim document changed during audit')
    if (_sha(_artifact_bytes(artifacts)) != _sha(artifact_raw) or
            _sha(reconciliation.read_bytes()) != _sha(reconciliation_raw)):
        raise ValueError('Inventory or reconciliation changed during audit')
    families = sorted(groups.values(), key=lambda x: (x['kind'], x['family_id']))
    for family in families:
        family['claim_ids'].sort()
        family['reconciled_claim_ids'].sort()
    return {
        'schema': 'ges.claim-workload-inventory.v1',
        'scope': 'Full recorded-claim inventory only; not a distinct-obligation denominator.',
        'inputs': {'claim_documents': documents,
                   'artifacts_sha256': _sha(artifact_raw),
                   'reconciliation_sha256': _sha(reconciliation_raw)},
        'counts': {
            'recorded_claims': len(claims), 'claim_documents': len(documents),
            'by_source': dict(sorted(source_counts.items())),
            'by_recorded_source_strength': dict(sorted(strengths.items())),
            'exact_statement_hashes': len(text_counts),
            'repeated_statement_occurrences': sum(n - 1 for n in text_counts.values()),
            'exact_source_spans': len(spans),
            'repeated_source_span_occurrences': sum(n - 1 for n in spans.values()),
            'claims_by_queue_kind': dict(sorted(counts.items())),
            'families_by_queue_kind': dict(sorted(Counter(
                x['kind'] for x in families).items())),
            'provider_dataset_rows': len(provider_rows),
            'provider_field_occurrences': dict(sorted(provider_fields.items())),
            'query_row_occurrences': len(query_rows),
            'reconciliation_records_present': len(reconciled),
            'recorded_claims_without_reconciliation': len(claims) - len(reconciled),
            'new_review_credit': 0, 'new_reconciliation_credit': 0,
            'unique_actionable_obligations': None,
        },
        'claim_membership_digest': digest(sorted(claims)),
        'families': families,
        'limits': [
            'Typed fields are existing authored metadata, not independently verified source values.',
            'Every member remains separately identifiable in its digest-bound claim document.',
            'Identical text or shared spans do not prove semantic equivalence across contexts.',
            'Provider versions, duplicate rows, absent keys and conflicting values must be retained.',
            'No source read, disposition, rights decision, policy adoption or gate closure is generated.',
            'Reconciliation records are counted and source-bound here; full authority/disposition validation remains in the existing reconciliation validator.',
        ],
    }


def check_historical_equivalence(result: dict, historical: Path) -> bytes:
    """Require identical accounting while allowing a separately observed input hash."""
    original_raw = historical.read_bytes()
    original = json.loads(original_raw)
    comparable = []
    for report in (original, result):
        if (not isinstance(report, dict) or
                report.get('schema') != 'ges.claim-workload-inventory.v1' or
                not isinstance(report.get('inputs'), dict) or
                not isinstance(report['inputs'].get('artifacts_sha256'), str)):
            raise ValueError('Invalid report for historical workload equivalence')
        input_sha = report['inputs']['artifacts_sha256']
        if len(input_sha) != 64 or any(char not in '0123456789abcdef' for char in input_sha):
            raise ValueError('Invalid artifact SHA256 for historical workload equivalence')
        inputs = {key: value for key, value in report['inputs'].items()
                  if key != 'artifacts_sha256'}
        comparable.append({**report, 'inputs': inputs})
    # Canonical JSON comparison preserves JSON types (for example, false != 0).
    if digest(comparable[0]) != digest(comparable[1]):
        raise ValueError('Historical workload accounting differs beyond inputs.artifacts_sha256')
    if historical.read_bytes() != original_raw:
        raise ValueError('Historical workload inventory changed during check')
    return original_raw


def _check_provenance(path: Path, artifacts: Path, current_raw: bytes,
                      historical_raw: bytes) -> None:
    """Check preserved byte bindings and pinned identities without new acquisition."""
    raw = path.read_bytes()
    provenance = json.loads(raw)
    if (not isinstance(provenance, dict) or
            provenance.get('schema') != 'ges.claim-workload-current-provenance.v1'):
        raise ValueError('Invalid current workload provenance')
    credits = {
        'new_review_credit': 0, 'new_reconciliation_credit': 0,
        'source_body_validation': 'NOT_ASSERTED_BY_THIS_METADATA_OBSERVATION',
        'rights_clearance': 'NOT_GRANTED', 'policy_adoption': 'NOT_GRANTED',
        'native_acceptance': 'NOT_GRANTED', 'human_review': 'NOT_ASSERTED',
    }
    if (provenance.get('acquisition_kind') != 'NEW_OBSERVED_WORKFLOW_METADATA' or
            provenance.get('is_historical_cache_restoration') is not False or
            digest(provenance.get('credits')) != digest(credits)):
        raise ValueError('Current metadata cannot claim restoration, review or acceptance credit')
    if artifacts.suffix != '.gz':
        raise ValueError('Current provenance requires gzip-preserved metadata')
    compressed_raw = artifacts.read_bytes()
    artifact_raw = gzip.decompress(compressed_raw)
    bindings = {
        'historical_report_sha256': _sha(historical_raw),
        'current_report_sha256': _sha(current_raw),
        'artifact_inventory_sha256': _sha(artifact_raw),
        'compressed_artifact_inventory_sha256': _sha(compressed_raw),
    }
    if provenance.get('bindings') != bindings:
        raise ValueError('Current workload provenance byte bindings differ')
    original = json.loads(historical_raw)
    if (provenance.get('historical_original_input_replay') != {
            'status': 'UNAVAILABLE',
            'artifact_inventory_sha256': original['inputs']['artifacts_sha256']} or
            provenance.get('allowed_report_difference') != ['inputs.artifacts_sha256']):
        raise ValueError('Historical replay limitation or equivalence scope changed')
    reference = provenance.get('source_identity_reference', {})
    name = reference.get('path') if isinstance(reference, dict) else None
    if (not isinstance(name, str) or not name or
            Path(name).name != name or name in {'.', '..'}):
        raise ValueError('Source identity reference must name a sibling metadata file')
    reference_path = path.parent / name
    if reference_path.resolve().parent != path.parent.resolve():
        raise ValueError('Source identity reference leaves the provenance directory')
    reference_raw = reference_path.read_bytes()
    if _sha(reference_raw) != reference.get('sha256'):
        raise ValueError('Source identity reference digest changed')
    expected = json.loads(reference_raw).get('inventory_identity_digests')
    records = [json.loads(line) for line in artifact_raw.splitlines() if line.strip()]
    if any(not isinstance(row, dict) or set(row) - ARTIFACT_METADATA_FIELDS
           for row in records):
        raise ValueError('Current artifact input contains non-metadata fields')
    projection = {
        'artifact_rows': len(records), 'uncompressed_bytes': len(artifact_raw),
        'compressed_bytes': len(compressed_raw),
        'fields': sorted({key for row in records for key in row}),
        'raw_source_bodies_included': False, 'source_archives_included': False,
        'credentials_included': False,
    }
    if digest(provenance.get('metadata_projection')) != digest(projection):
        raise ValueError('Current metadata projection or content boundary differs')
    actual = {source: inventory_digest([row for row in records if row['source'] == source])
              for source in sorted({row['source'] for row in records})}
    if (actual != expected or actual != provenance.get('source_identity_digests')):
        raise ValueError('Current artifact identities differ from the pinned source baseline')
    if (path.read_bytes() != raw or reference_path.read_bytes() != reference_raw or
            artifacts.read_bytes() != compressed_raw):
        raise ValueError('Current workload provenance inputs changed during check')


def check_inventory(reviews: Path, artifacts: Path, reconciliation: Path,
                    committed: Path, *, historical: Path | None = None,
                    provenance: Path | None = None) -> dict:
    """Reproduce the committed report exactly without writing or repairing inputs."""
    expected_raw = committed.read_bytes()
    expected = json.loads(expected_raw)
    if (not isinstance(expected, dict) or
            expected.get('schema') != 'ges.claim-workload-inventory.v1' or
            not isinstance(expected.get('inputs'), dict)):
        raise ValueError('Invalid committed workload inventory')
    if _sha(_artifact_bytes(artifacts)) != expected['inputs'].get('artifacts_sha256'):
        raise ValueError('Artifact inventory differs from the committed input SHA256')
    result = inventory(reviews, artifacts, reconciliation)
    if _inventory_bytes(result) != expected_raw:
        differences = sorted(key for key in set(result) | set(expected)
                             if result.get(key) != expected.get(key))
        raise ValueError('Committed workload inventory differs in ' +
                         ', '.join(differences or ['serialization']) +
                         '; regenerate separately and review the changed inputs and report')
    if provenance is not None and historical is None:
        raise ValueError('Current provenance requires the historical inventory')
    if historical is not None:
        historical_raw = check_historical_equivalence(result, historical)
        if provenance is not None:
            _check_provenance(provenance, artifacts, expected_raw, historical_raw)
        if historical.read_bytes() != historical_raw:
            raise ValueError('Historical workload inventory changed during check')
    if committed.read_bytes() != expected_raw:
        raise ValueError('Committed workload inventory changed during check')
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reviews', type=Path, required=True)
    parser.add_argument('--artifacts', type=Path, required=True,
                        help='Exact original artifacts.jsonl, optionally gzip-compressed')
    parser.add_argument('--reconciliation', type=Path, required=True)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--output', type=Path, help='Create a new report; never overwrite')
    mode.add_argument('--check', type=Path,
                      help='Fail unless the committed report is reproduced byte for byte')
    parser.add_argument('--historical', type=Path,
                        help='Require identical historical accounting except artifact input SHA256')
    parser.add_argument('--provenance', type=Path,
                        help='Check current/historical byte bindings and pinned source identities')
    args = parser.parse_args()
    if (args.historical is not None or args.provenance is not None) and args.check is None:
        parser.error('--historical and --provenance require --check')
    try:
        if args.check is not None:
            result = check_inventory(args.reviews, args.artifacts,
                                     args.reconciliation, args.check,
                                     historical=args.historical, provenance=args.provenance)
            print(json.dumps({'status': 'MATCH',
                              'recorded_claims': result['counts']['recorded_claims'],
                              'claim_documents': result['counts']['claim_documents'],
                              'families': len(result['families']),
                              'new_review_credit': 0, 'new_reconciliation_credit': 0}))
            return
        result = inventory(args.reviews, args.artifacts, args.reconciliation)
        with args.output.open('xb') as stream:
            stream.write(_inventory_bytes(result))
    except (OSError, EOFError, ValueError) as exc:
        parser.exit(1, 'Claim workload failed: ' + str(exc) + '\n')
    print(json.dumps(result['counts'], sort_keys=True))


if __name__ == '__main__':
    main()
