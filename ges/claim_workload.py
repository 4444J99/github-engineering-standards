"""Inventory recorded claims and propose review families; never award review credit."""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import re
import zlib
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from urllib.parse import quote

from .core import digest
from .evidence_paths import canonical_path
from .pinned_sources import DEFAULT_SOURCE_INVENTORY_SHA256, inventory_digest

PROVIDER_FIELDS = {
    'isPublic', 'isPrivateWithGhas', 'hasPushProtection', 'hasValidityCheck',
    'base64Supported', 'isduplicate', 'hasExtendedMetadata',
}
ARTIFACT_METADATA_FIELDS = {
    'artifact_id', 'candidate_count', 'commit', 'git_blob_sha', 'kind', 'path',
    'proposed_disposition', 'retrieval_status', 'retrieved_at', 'review_status',
    'sha256', 'size', 'source', 'url',
}
ARTIFACT_DISPOSITIONS = {
    'license', 'template', 'test', 'reusable', 'documentation',
    'configuration', 'implementation', 'supporting_asset',
}
MAX_ARTIFACT_BYTES = 200_000_000
MAX_METADATA_BYTES = 150_000_000


def _unique_metadata_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('Duplicate metadata object field')
        result[key] = value
    return result


def _preserved_metadata_bytes(compressed: bytes) -> bytes:
    """Admit one gzip member with no optional fields that can carry arbitrary text."""
    if len(compressed) < 18 or compressed[:4] != b'\x1f\x8b\x08\x00':
        raise ValueError('Preserved metadata gzip has unsupported header payload fields')
    try:
        decoder = zlib.decompressobj(wbits=31)
        raw = decoder.decompress(compressed, MAX_METADATA_BYTES + 1)
    except zlib.error as exc:
        raise ValueError('Invalid preserved metadata gzip') from exc
    if (len(raw) > MAX_METADATA_BYTES or not decoder.eof or
            decoder.unused_data or decoder.unconsumed_tail):
        raise ValueError('Preserved metadata gzip must contain one complete bounded member')
    return raw


def _metadata_records(raw: bytes) -> list[dict]:
    """Validate the closed value contract; field names alone do not exclude payloads."""
    records = [json.loads(line, object_pairs_hook=_unique_metadata_object)
               for line in raw.splitlines() if line.strip()]
    identities, artifact_ids = set(), set()
    current = datetime.now(timezone.utc)
    for row in records:
        if not isinstance(row, dict) or set(row) != ARTIFACT_METADATA_FIELDS:
            raise ValueError('Current artifact input contains missing or non-metadata fields')
        if (not isinstance(row['source'], str) or
                not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', row['source']) or
                not isinstance(row['commit'], str) or
                not re.fullmatch('[a-f0-9]{40}', row['commit']) or
                not isinstance(row['sha256'], str) or
                not re.fullmatch('[a-f0-9]{64}', row['sha256']) or
                not isinstance(row['git_blob_sha'], str) or
                not re.fullmatch('[a-f0-9]{40}', row['git_blob_sha'])):
            raise ValueError('Invalid current artifact source or content digest')
        name = row['path']
        if (not isinstance(name, str) or not 0 < len(name) <= 4096 or
                '\\' in name or any(ord(char) < 32 or ord(char) == 127 for char in name)):
            raise ValueError('Invalid current artifact relative path')
        relative = PurePosixPath(name)
        if (relative.is_absolute() or '..' in relative.parts or
                relative.as_posix() != name or name == '.'):
            raise ValueError('Noncanonical current artifact relative path')
        identity = (row['source'], row['commit'], name)
        if (row['artifact_id'] != digest(list(identity))[:24] or
                identity in identities or row['artifact_id'] in artifact_ids):
            raise ValueError('Invalid or duplicate canonical current artifact identity')
        identities.add(identity)
        artifact_ids.add(row['artifact_id'])
        canonical_url = f'https://github.com/{row["source"]}/blob/{row["commit"]}/{quote(name)}'
        if row['url'] != canonical_url:
            raise ValueError('Current artifact URL differs from its canonical pinned locator')
        if (row['kind'] not in ('text', 'binary') or
                row['retrieval_status'] != 'RETRIEVED' or row['review_status'] != 'UNREVIEWED' or
                not isinstance(row['proposed_disposition'], str) or
                row['proposed_disposition'] not in ARTIFACT_DISPOSITIONS):
            raise ValueError('Invalid current artifact metadata classification')
        if (type(row['size']) is not int or not 0 <= row['size'] <= MAX_ARTIFACT_BYTES or
                type(row['candidate_count']) is not int or
                not 0 <= row['candidate_count'] <= row['size'] or
                (row['candidate_count'] != 0 and
                 (row['kind'] != 'text' or not name.endswith(('.md', '.mdx', '.rst'))))):
            raise ValueError('Invalid bounded current artifact size or candidate count')
        stamp = row['retrieved_at']
        if (not isinstance(stamp, str) or not re.fullmatch(
                r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{6})?\+00:00', stamp)):
            raise ValueError('Invalid canonical UTC artifact acquisition timestamp')
        try:
            acquired = datetime.fromisoformat(stamp)
        except ValueError as exc:
            raise ValueError('Invalid artifact acquisition timestamp') from exc
        if acquired > current:
            raise ValueError('Future artifact acquisition timestamp')
    return records


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
    artifact_raw = _preserved_metadata_bytes(compressed_raw)
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
    if (not isinstance(reference, dict) or set(reference) != {'path', 'sha256'} or
            not isinstance(name, str) or not name or '\\' in name or
            Path(name).name != name or name in {'.', '..'}):
        raise ValueError('Source identity reference must name a sibling metadata file')
    reference_input = path.parent / name
    reference_path = canonical_path(reference_input, symlink_error='Symlink source identity reference is not permitted')
    if (not reference_path.is_file() or
            reference_path.resolve().parent != path.parent.resolve()):
        raise ValueError('Source identity reference is missing, symlinked or leaves the provenance directory')
    reference_raw = reference_path.read_bytes()
    # The mutable provenance cannot choose its own authority fingerprint.
    if (reference.get('sha256') != DEFAULT_SOURCE_INVENTORY_SHA256 or
            _sha(reference_raw) != DEFAULT_SOURCE_INVENTORY_SHA256):
        raise ValueError('Source identity reference differs from independently pinned A3 fingerprint')
    authority = json.loads(reference_raw)
    expected, trees = authority.get('inventory_identity_digests'), authority.get('source_trees')
    if (not isinstance(expected, dict) or not isinstance(trees, dict) or not expected or
            set(expected) != set(trees)):
        raise ValueError('Trusted source reference has incomplete pinned tree identities')
    records = _metadata_records(artifact_raw)
    projection = {
        'artifact_rows': len(records), 'uncompressed_bytes': len(artifact_raw),
        'compressed_bytes': len(compressed_raw),
        'fields': sorted({key for row in records for key in row}),
        'raw_source_bodies_included': False, 'source_archives_included': False,
        'credentials_included': False,
    }
    if digest(provenance.get('metadata_projection')) != digest(projection):
        raise ValueError('Current metadata projection or content boundary differs')
    groups = {}
    for row in records:
        groups.setdefault(row['source'], []).append(row)
    if set(groups) != set(expected):
        raise ValueError('Current metadata does not contain every independently pinned source')
    for source, rows in groups.items():
        tree = trees[source]
        if (not isinstance(tree, dict) or tree.get('repository') != source or
                tree.get('status') != 'MATCH' or type(tree.get('artifacts')) is not int or
                tree['artifacts'] <= 0 or len(rows) != tree['artifacts'] or
                tree.get('inventory_digest') != expected[source] or
                any(row['commit'] != tree.get('commit') for row in rows)):
            raise ValueError('Current metadata differs from complete pinned source counts or commits')
    actual = {source: inventory_digest(rows) for source, rows in sorted(groups.items())}
    if (actual != expected or actual != provenance.get('source_identity_digests')):
        raise ValueError('Current artifact identities differ from the pinned source baseline')
    if (canonical_path(reference_input, symlink_error='Symlink source identity reference is not permitted') != reference_path or
            path.read_bytes() != raw or reference_path.read_bytes() != reference_raw or
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
