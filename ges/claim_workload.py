"""Inventory recorded claims and propose review families; never award review credit."""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

from .core import digest

PROVIDER_FIELDS = {
    'isPublic', 'isPrivateWithGhas', 'hasPushProtection', 'hasValidityCheck',
    'base64Supported', 'isduplicate', 'hasExtendedMetadata',
}


def _sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def inventory(reviews: Path, artifacts: Path, reconciliation: Path) -> dict:
    """Count an immutable occurrence inventory, including all family members."""
    artifact_raw = artifacts.read_bytes()
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
                provider_rows.add((*identity, context['entry_ordinal']))
            elif 'query_occurrence' in claim:
                occurrence = claim['query_occurrence']
                if (not isinstance(occurrence, str) or
                        occurrence != source_path + '#L' + str(start) or
                        not isinstance(claim.get('query_help_identity'), str) or
                        not claim['query_help_identity'].strip()):
                    raise ValueError('Malformed query row: ' + cid)
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
    if (_sha(artifacts.read_bytes()) != _sha(artifact_raw) or
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


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reviews', type=Path, required=True)
    parser.add_argument('--artifacts', type=Path, required=True)
    parser.add_argument('--reconciliation', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = inventory(args.reviews, args.artifacts, args.reconciliation)
    with args.output.open('x') as stream:
        json.dump(result, stream, indent=2)
        stream.write('\n')
    print(json.dumps(result['counts'], sort_keys=True))


if __name__ == '__main__':
    main()
