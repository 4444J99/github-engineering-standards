"""Validate exact candidate publication-use attestations without granting rights.

The authority policy is a separately approved, trusted input. A manifest cannot
certify its own completeness, and JSON identities cannot authenticate a human.
Candidate files and pinned source evidence are read locally; nothing is published.
The legacy whole-corpus rights_accounting contract is deliberately unchanged.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys

from .core import ROOT, digest, dump, load, now
from .published_assurance import _evidence, _require, _strings, _time
from .source_fidelity import _file_sha256

IDENTITY = {'artifact_id', 'source', 'commit', 'path', 'sha256'}
KINDS = {'REFERENCES_ONLY', 'INDEPENDENT_PARAPHRASE', 'LICENSED_COPY', 'ADAPTATION'}
EXPRESSION_KINDS = {'LICENSED_COPY', 'ADAPTATION'}
ROLES = {'reviewer': 'authorized_use_reviewers',
         'independent_auditor': 'authorized_independent_auditors',
         'human_acceptor': 'authorized_human_acceptors',
         'distribution_approver': 'authorized_distribution_approvers'}
SCOPE_FIELDS = {'candidate_id', 'candidate_revision', 'distribution_scope', 'release_scope',
                'manifest_digest', 'register_digest', 'output_inventory_digest',
                'inventory_digest', 'pins_digest', 'source_evidence_digest'}
MAX_SOURCE_RECORD_BYTES = 200_000_000


def _text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _sha(value: object) -> bool:
    return isinstance(value, str) and re.fullmatch('[a-f0-9]{64}', value) is not None


def _object(value: object, fields: set[str], message: str) -> dict:
    _require(isinstance(value, dict) and set(value) == fields, message)
    return value


def _relative(value: object) -> Path:
    _require(_text(value) and '\\' not in value and '\x00' not in value,
             'Invalid candidate/source relative path')
    path = Path(value)
    _require(path.parts and not path.is_absolute() and '..' not in path.parts and
             path.as_posix() == value and path.as_posix() != '.',
             'Noncanonical or escaping candidate/source path')
    return path


def _root(root: Path | None, label: str) -> Path:
    _require(isinstance(root, Path), 'Missing ' + label + ' root')
    absolute = root.absolute()
    _require(not any(p.is_symlink() for p in (absolute, *absolute.parents)),
             'Symlink ' + label + ' root is not permitted')
    _require(absolute.is_dir(), 'Missing ' + label + ' directory')
    return absolute.resolve()


def _file(root: Path, path: str) -> Path:
    target = root / _relative(path)
    _require(not any(p.is_symlink() for p in (target, *target.parents)
                     if p.is_relative_to(root)), 'Symlink candidate/source path is not permitted')
    _require(target.resolve().is_relative_to(root) and target.is_file(),
             'Missing or escaping candidate/source file')
    return target


def output_inventory(output_root: Path) -> list[dict]:
    """Observe every regular file beneath a dedicated candidate directory."""
    root = _root(output_root, 'output')
    rows = []
    def enumeration_failed(error: OSError) -> None:
        raise ValueError('Cannot completely enumerate candidate outputs') from error
    for current, directories, files in os.walk(root, followlinks=False, onerror=enumeration_failed):
        for name in directories + files:
            path = Path(current) / name
            mode = path.lstat().st_mode
            _require(stat.S_ISDIR(mode) or stat.S_ISREG(mode),
                     'Nonregular or symlink output is not permitted')
        for name in files:
            path = Path(current) / name
            relative = path.relative_to(root).as_posix()
            _relative(relative)
            rows.append({'path': relative, 'sha256': _file_sha256(path),
                         'size_bytes': path.stat().st_size})
    return sorted(rows, key=lambda row: row['path'])


def prepare_draft(output_root: Path, candidate_id: str, candidate_revision: str,
                  distribution_scope: str, *, release_scope: str = 'BOUNDED_PACKAGE',
                  prepared_at: str | None = None) -> dict:
    """Inventory actual bytes and explicitly leave every use classification open."""
    _require(_text(candidate_id) and _text(distribution_scope) and
             isinstance(candidate_revision, str) and re.fullmatch('[a-f0-9]{40}', candidate_revision) and
             release_scope in {'GES_V0_2', 'BOUNDED_PACKAGE'}, 'Invalid draft candidate identity/scope')
    stamp = prepared_at if prepared_at is not None else now()
    _require(_time(stamp) <= _time(now()), 'Draft preparation is future')
    outputs = output_inventory(output_root)
    _require(bool(outputs), 'Empty candidate output inventory')
    manifest = {'schema': 'ges.publication-output-manifest.v1', 'candidate_id': candidate_id,
                'candidate_revision': candidate_revision, 'distribution_scope': distribution_scope,
                'release_scope': release_scope, 'prepared_at': stamp, 'outputs': outputs}
    register = {'schema': 'ges.publication-use-register.v1', 'candidate_id': candidate_id,
                'manifest_digest': digest(manifest), 'prepared_at': stamp,
                'outputs': [{'path': row['path'], 'disposition': 'UNREVIEWED', 'use_ids': [],
                             'rationale': 'Output bytes inventoried; upstream-expression use and attribution remain unreviewed.'}
                            for row in outputs], 'uses': [], 'source_evidence': []}
    return {'manifest': manifest, 'register': register, 'receipts': [], 'policy': {}}


def _span(value: object, raw: bytes, label: str) -> None:
    span = _object(value, {'start_byte', 'end_byte', 'sha256'}, 'Malformed ' + label + ' span')
    start, end = span['start_byte'], span['end_byte']
    _require(type(start) is int and type(end) is int and 0 <= start < end <= len(raw),
             'Invalid ' + label + ' byte range')
    _require(_sha(span['sha256']) and
             hashlib.sha256(raw[start:end]).hexdigest() == span['sha256'],
             label + ' expression bytes changed')


def _artifacts(artifacts: list[dict], pins: dict[str, str], current) -> dict[str, dict]:
    _require(isinstance(artifacts, list) and isinstance(pins, dict),
             'Malformed source inventory or pins')
    _require(all(isinstance(k, str) and re.fullmatch(r'[\w.-]+/[\w.-]+', k) and
                 isinstance(v, str) and re.fullmatch('[a-f0-9]{40}', v)
                 for k, v in pins.items()), 'Malformed source pin')
    index, identities = {}, set()
    for row in artifacts:
        _require(isinstance(row, dict) and all(_text(row.get(k)) for k in IDENTITY) and
                 _sha(row['sha256']), 'Malformed source artifact identity')
        _relative(row['path'])
        _require(pins.get(row['source']) == row['commit'], 'Source differs from locked pin')
        _require(_time(row.get('retrieved_at')) <= current, 'Future source acquisition')
        identity = (row['source'], row['commit'], row['path'])
        _require(row['artifact_id'] not in index and identity not in identities,
                 'Duplicate source artifact identity')
        index[row['artifact_id']] = row
        identities.add(identity)
    return index


def _source_content(records: list[dict], needed: set[str], index: dict,
                    source_root: Path | None) -> tuple[dict[str, bytes], list[tuple[Path, str]]]:
    _require(isinstance(records, list), 'Source evidence must be an array')
    seen, grouped, content, bound = set(), {}, {}, []
    root = _root(source_root, 'source') if records else None
    for ref in records:
        _object(ref, {'artifact_id', 'format', 'path', 'sha256'}, 'Malformed source evidence')
        identity = ref['artifact_id']
        _require(_text(identity) and identity in needed and identity not in seen and
                 _sha(ref['sha256']), 'Foreign, duplicate or unhashed source evidence')
        _require(ref['format'] in {'RAW', 'SNAPSHOT_TEXT'}, 'Unsupported source evidence format')
        target = _file(root, ref['path'])
        _require(_file_sha256(target) == ref['sha256'], 'Source evidence bytes changed')
        bound.append((target, ref['sha256']))
        if ref['format'] == 'RAW':
            raw = target.read_bytes()
            _require(hashlib.sha256(raw).hexdigest() == index[identity]['sha256'],
                     'Pinned source bytes changed')
            content[identity] = raw
        else:
            _require(ref['path'] == index[identity]['source'].replace('/', '__') + '.text.jsonl.gz',
                     'Source snapshot path differs from source identity')
            if target in grouped:
                _require(grouped[target][0] == ref['sha256'], 'Conflicting source snapshot digests')
                grouped[target][1].add(identity)
            else:
                grouped[target] = (ref['sha256'], {identity})
        seen.add(identity)
    _require(seen == needed, 'Missing pinned source evidence for registered uses')
    for target, (_, assigned) in grouped.items():
        expected = {(index[i]['source'], index[i]['commit'], index[i]['path']): i for i in assigned}
        with gzip.open(target, 'rb') as stream:
            while line := stream.readline(MAX_SOURCE_RECORD_BYTES + 1):
                _require(len(line) <= MAX_SOURCE_RECORD_BYTES, 'Source record exceeds size bound')
                row = json.loads(line)
                _require(isinstance(row, dict), 'Malformed pinned source snapshot row')
                identity = expected.get((row.get('source'), row.get('commit'), row.get('path')))
                if identity is None:
                    continue
                _require(identity not in content and isinstance(row.get('content'), str),
                         'Duplicate or malformed pinned source content')
                raw = row['content'].encode('utf-8')
                _require(hashlib.sha256(raw).hexdigest() == index[identity]['sha256'],
                         'Pinned source bytes changed')
                content[identity] = raw
    _require(set(content) == needed, 'Missing pinned source content')
    return content, bound


def _policy(policy: dict, subject: dict, earliest, current) -> tuple[object, object]:
    _object(policy, {'schema', 'approval_reference', 'subject', 'issued_at', 'valid_until',
                     'authorized_inventory_reviewers', *ROLES.values()},
            'Missing explicit publication-use authority policy')
    _require(policy['schema'] == 'ges.publication-use-authority-policy.v1' and
             _text(policy['approval_reference']), 'Missing external authority approval reference')
    _require(policy['subject'] == subject, 'Approved publication scope or input digests changed')
    for role in {'authorized_inventory_reviewers', *ROLES.values()}:
        _require(_strings(policy[role]), 'Missing explicit publication authority role: ' + role)
    issued, expires = _time(policy['issued_at']), _time(policy['valid_until'])
    _require(earliest <= issued <= current < expires, 'Publication authority is premature, future or expired')
    return issued, expires


def _receipt(receipt: dict, scope: dict, policy: dict, uses: dict,
             earliest, current, policy_expiry, evidence_root: Path,
             references: dict, zero: bool) -> tuple[str | None, bool]:
    inventory = receipt.get('kind') == 'OUTPUT_INVENTORY'
    fields = {'schema', 'kind', 'subject', 'valid_until', 'obligations', 'evidence', *ROLES}
    fields |= {'disposition'} if inventory else {'use_id', 'attribution_disposition', 'attribution_rationale'}
    _object(receipt, fields, 'Malformed publication-use receipt')
    _require(receipt['schema'] == 'ges.publication-use-receipt.v1' and
             receipt['kind'] in {'OUTPUT_INVENTORY', 'EXPRESSION_USE'}, 'Unsupported publication receipt')
    _require(receipt['subject'] == scope, 'Publication receipt scope changed')
    _require(_strings(receipt['obligations']), 'Missing explicit use obligations')
    expires = _time(receipt['valid_until'])
    _require(current < expires <= policy_expiry, 'Publication receipt expired or exceeds authority validity')
    for field, role in ROLES.items():
        if inventory and field == 'reviewer':
            role = 'authorized_inventory_reviewers'
        _require(_text(receipt[field]) and receipt[field] in policy[role],
                 'Unauthorized publication role: ' + field)
    _require(len({receipt['reviewer'], receipt['independent_auditor'], receipt['human_acceptor']}) == 3 and
             receipt['distribution_approver'] not in {receipt['reviewer'], receipt['independent_auditor']},
             'Publication review, independent audit and acceptance must be independent')
    subject = {'scope': scope, 'obligations': receipt['obligations'], 'valid_until': receipt['valid_until']}
    if inventory:
        disposition = 'NO_UPSTREAM_EXPRESSION' if zero else 'REGISTER_COMPLETE'
        _require(receipt['disposition'] == disposition, 'Contradictory inventory disposition')
        subject['disposition'] = disposition
        assurances = {'all_candidate_outputs_accounted_for': True,
                      'all_upstream_uses_accounted_for': True,
                      'source_use_classifications_reviewed': True,
                      'no_upstream_expression_confirmed': zero}
        first, audit = 'inventory_review', 'independent_omission_audit'
        use_id = None
    else:
        use_id = receipt['use_id']
        _require(_text(use_id) and use_id in uses and uses[use_id]['kind'] in EXPRESSION_KINDS,
                 'Foreign use or unnecessary blanket source-grant receipt')
        use = uses[use_id]
        subject.update(use=use, attribution_disposition=receipt['attribution_disposition'],
                       attribution_rationale=receipt['attribution_rationale'])
        _require(_text(receipt['attribution_rationale']) and
                 receipt['attribution_disposition'] in {'REQUIRED_PROVIDED', 'NOT_REQUIRED_WITH_REASON'},
                 'Missing accountable attribution decision')
        _require(receipt['attribution_disposition'] != 'REQUIRED_PROVIDED' or bool(use['attributions']),
                 'Required attribution is absent from candidate outputs')
        assurances = {'exact_expression_and_grant_reviewed': True,
                      'restrictions_accounted_for': True, 'attribution_accounted_for': True}
        first, audit = 'expression_rights_review', 'independent_exception_audit'
    roles = {first: 'reviewer', audit: 'independent_auditor',
             'human_acceptance': 'human_acceptor', 'distribution_approval': 'distribution_approver'}
    _require(isinstance(receipt['evidence'], dict) and set(receipt['evidence']) == set(roles),
             'Missing review, audit, human acceptance or distribution evidence')
    times = []
    for kind, field in roles.items():
        reference = receipt['evidence'][kind]
        _object(reference, {'path', 'sha256'}, 'Malformed publication evidence reference')
        doc = _evidence(evidence_root, reference)
        _object(doc, {'schema', 'kind', 'identity', 'subject', 'reviewed_at', 'decision',
                      'assurances', 'unresolved', 'rationale'}, 'Malformed publication-use attestation')
        _require(doc['schema'] == 'ges.publication-use-attestation.v1' and doc['kind'] == kind and
                 doc['identity'] == receipt[field] and doc['subject'] == subject,
                 'Wrong publication attestation identity or exact scope')
        _require(doc['decision'] == 'APPROVED_FOR_SPECIFIED_USE' and
                 isinstance(doc['assurances'], dict) and set(doc['assurances']) == set(assurances) and
                 all(doc['assurances'][k] is v for k, v in assurances.items()) and
                 doc['unresolved'] == [] and _text(doc['rationale']),
                 'Unsupported, unresolved or nonboolean publication attestation')
        reviewed = _time(doc['reviewed_at'])
        _require(earliest <= reviewed <= current and reviewed < expires,
                 'Publication evidence is future, premature or outside validity')
        times.append(reviewed)
        path = reference['path']
        _require(path not in references or references[path] == reference,
                 'Conflicting publication evidence identity')
        references[path] = reference
    _require(times == sorted(times), 'Publication review decision order is invalid')
    return use_id, inventory


def validate_accounting_result(result: dict) -> dict:
    """Validate a computed result's internal consistency, never its authority.

    Consumers must call publication_accounting on actual inputs; this function
    does not turn a supplied sidecar report into trustworthy release evidence.
    """
    _require(isinstance(result, dict) and result.get('schema') == 'ges.publication-use-accounting.v1',
             'Malformed publication-use accounting result')
    for key in ('completed', 'denominator', 'output_count', 'copied_or_adapted_count',
                'reference_only_count', 'independent_paraphrase_count', 'validated_expression_count',
                'unreviewed_output_count'):
        _require(type(result.get(key)) is int and result[key] >= 0, 'Invalid publication count: ' + key)
    _require(result['denominator'] == result['copied_or_adapted_count'] + result['reference_only_count'] +
             result['independent_paraphrase_count'], 'Publication use denominator disagrees with kinds')
    identities = result.get('validated_use_ids')
    _require(isinstance(identities, list) and all(_text(v) for v in identities) and
             len(set(identities)) == len(identities) == result['completed'] <= result['denominator'],
             'Publication completed count disagrees with exact use identities')
    _require(result['validated_expression_count'] <= result['copied_or_adapted_count'],
             'Publication expression acceptance count exceeds scope')
    _require(result['unreviewed_output_count'] <= result['output_count'],
             'Publication unreviewed output count exceeds inventory')
    flags = ('complete_output_inventory', 'use_register_complete', 'exact_use_clearance',
             'authorized_distribution_decision')
    for key in flags:
        _require(result.get(key) is None or type(result[key]) is bool, 'Invalid publication condition: ' + key)
    _require(type(result.get('zero_use_clearance')) is bool and
             type(result.get('inventory_receipt_validated')) is bool,
             'Invalid publication zero-use or inventory condition')
    for key in ('manifest_digest', 'register_digest', 'policy_digest', 'receipts_digest',
                'output_inventory_digest', 'source_evidence_digest', 'inventory_digest', 'pins_digest'):
        _require(result.get(key) is None or _sha(result[key]), 'Invalid publication binding: ' + key)
    _require(isinstance(result.get('diagnostics'), list) and
             all(_text(item) for item in result['diagnostics']), 'Invalid publication diagnostics')
    for key in ('legal_truth_automatically_certified', 'authority_authenticity_automatically_certified',
                'publication_performed', 'legacy_rights_reinterpreted'):
        _require(result.get(key) is False, 'Publication result exceeds attestation scope')
    accepted = result['inventory_receipt_validated']
    expected_completed = (result['reference_only_count'] + result['independent_paraphrase_count'] +
                          result['validated_expression_count']) if accepted else result['validated_expression_count']
    _require(result['completed'] == expected_completed, 'Publication accounting omitted or invented use acceptance')
    if accepted:
        _require(result['output_count'] > 0 and result['unreviewed_output_count'] == 0 and
                 result['complete_output_inventory'] is True and
                 result['use_register_complete'] is True and
                 all(_sha(result[k]) for k in ('manifest_digest', 'register_digest', 'policy_digest',
                                               'receipts_digest', 'output_inventory_digest',
                                               'source_evidence_digest', 'inventory_digest', 'pins_digest')),
                 'Accepted publication inventory lacks bound nonempty output evidence')
    else:
        _require(result['use_register_complete'] is None, 'Unreviewed use register cannot be certified')
    zero = accepted and result['denominator'] == 0
    _require(result['zero_use_clearance'] is zero, 'Empty use denominator is not approved clearance')
    complete = accepted and result['completed'] == result['denominator']
    expected = complete if accepted or result['validated_expression_count'] else None
    _require(result['exact_use_clearance'] is expected and
             result['authorized_distribution_decision'] is expected,
             'Publication clearance disagrees with validated scope')
    if 'subject' in result:
        subject = _object(result['subject'], SCOPE_FIELDS, 'Malformed publication accounting subject')
        _require(subject['release_scope'] in {'GES_V0_2', 'BOUNDED_PACKAGE'} and
                 _text(subject['candidate_id']) and _text(subject['distribution_scope']) and
                 isinstance(subject['candidate_revision'], str) and
                 re.fullmatch('[a-f0-9]{40}', subject['candidate_revision']) and
                 all(subject[k] == result[k] for k in SCOPE_FIELDS if k.endswith('_digest')),
                 'Publication accounting subject disagrees with exact bindings')
    else:
        _require(result['output_count'] == 0 and not accepted, 'Publication output scope is absent')
    _require(result.get('release_scope') == (result['subject']['release_scope'] if 'subject' in result else None),
             'Publication release boundary disagrees with approved subject')
    return result


def publication_accounting(manifest: dict | None, register: dict | None,
                           receipts: list[dict], policy: dict, artifacts: list[dict],
                           pins: dict[str, str], *, output_root: Path | None = None,
                           source_root: Path | None = None, evidence_root: Path = ROOT) -> dict:
    """Bind actual outputs/uses to separately authorized exact-scope evidence.

    Invalid data/evidence raises ValueError. Missing approval stays unknown;
    valid partial approvals retain the entire registered-use denominator.
    """
    _require(isinstance(receipts, list) and isinstance(policy, dict), 'Malformed publication approval inputs')
    result = {'schema': 'ges.publication-use-accounting.v1',
              'completed': 0, 'denominator': 0, 'output_count': 0,
              'copied_or_adapted_count': 0, 'reference_only_count': 0,
              'independent_paraphrase_count': 0, 'validated_expression_count': 0,
              'unreviewed_output_count': 0,
              'validated_use_ids': [], 'complete_output_inventory': None,
              'use_register_complete': None, 'exact_use_clearance': None,
              'authorized_distribution_decision': None, 'zero_use_clearance': False,
              'inventory_receipt_validated': False, 'manifest_digest': None,
              'release_scope': None,
              'register_digest': None, 'output_inventory_digest': None,
              'source_evidence_digest': None, 'inventory_digest': digest(artifacts),
              'pins_digest': digest(pins), 'policy_digest': digest(policy),
              'receipts_digest': digest(receipts), 'diagnostics': [],
              'legal_truth_automatically_certified': False,
              'authority_authenticity_automatically_certified': False,
              'publication_performed': False, 'legacy_rights_reinterpreted': False}
    if manifest is None or register is None:
        _require(not receipts and not policy, 'Publication approval requires manifest and actual-use register')
        result['diagnostics'] = ['Missing candidate output manifest or actual-use register; clearance unknown.']
        return validate_accounting_result(result)
    _object(manifest, {'schema', 'candidate_id', 'candidate_revision', 'distribution_scope', 'release_scope',
                       'prepared_at', 'outputs'}, 'Malformed publication output manifest')
    _require(manifest['schema'] == 'ges.publication-output-manifest.v1' and
             _text(manifest['candidate_id']) and _text(manifest['distribution_scope']) and
             manifest['release_scope'] in {'GES_V0_2', 'BOUNDED_PACKAGE'} and
             isinstance(manifest['candidate_revision'], str) and
             re.fullmatch('[a-f0-9]{40}', manifest['candidate_revision']),
             'Invalid candidate identity, revision or distribution scope')
    current = _time(now())
    prepared = _time(manifest['prepared_at'])
    _require(prepared <= current, 'Candidate preparation is future')
    declared = manifest['outputs']
    _require(isinstance(declared, list) and bool(declared), 'Empty candidate output inventory')
    paths = set()
    for output in declared:
        _object(output, {'path', 'sha256', 'size_bytes'}, 'Malformed declared candidate output')
        _relative(output['path'])
        _require(output['path'] not in paths and _sha(output['sha256']) and
                 type(output['size_bytes']) is int and output['size_bytes'] >= 0,
                 'Duplicate, unhashed or invalid candidate output')
        paths.add(output['path'])
    observed = output_inventory(output_root)
    _require(sorted(declared, key=lambda row: row['path']) == observed,
             'Candidate output set or bytes changed: missing, extra or mismatched files')
    root = _root(output_root, 'output')
    output_bytes = {row['path']: _file(root, row['path']).read_bytes() for row in observed}
    _require(all(hashlib.sha256(output_bytes[row['path']]).hexdigest() == row['sha256'] for row in observed),
             'Candidate output changed during read')
    _object(register, {'schema', 'candidate_id', 'manifest_digest', 'prepared_at',
                       'outputs', 'uses', 'source_evidence'}, 'Malformed publication-use register')
    _require(register['schema'] == 'ges.publication-use-register.v1' and
             register['candidate_id'] == manifest['candidate_id'] and
             register['manifest_digest'] == digest(manifest), 'Register refers to a different candidate')
    registered = _time(register['prepared_at'])
    _require(prepared <= registered <= current, 'Use register is premature or future')
    index = _artifacts(artifacts, pins, current)
    _require(isinstance(register['uses'], list) and isinstance(register['outputs'], list),
             'Register uses/output dispositions must be arrays')
    uses, needed, spans = {}, set(), {}
    for use in register['uses']:
        _object(use, {'use_id', 'kind', 'source', 'source_range', 'output_path',
                      'output_range', 'attributions', 'rationale'}, 'Malformed actual-use row')
        uid = use['use_id']
        _require(_text(uid) and uid not in uses and isinstance(use['kind'], str) and
                 use['kind'] in KINDS and _text(use['rationale']), 'Duplicate or invalid actual-use identity')
        source = _object(use['source'], IDENTITY, 'Malformed pinned actual-use source')
        aid = source['artifact_id']
        _require(_text(aid) and aid in index and all(source[k] == index[aid][k] for k in IDENTITY),
                 'Actual-use source differs from pinned inventory')
        _require(use['output_path'] in output_bytes, 'Actual use references an undeclared output')
        _span(use['output_range'], output_bytes[use['output_path']], 'Output')
        span_key = (use['output_path'], use['output_range']['start_byte'], use['output_range']['end_byte'])
        _require(span_key not in spans or spans[span_key] == use['kind'],
                 'Contradictory use classifications for one output expression')
        _require(not any(prior['output_path'] == use['output_path'] and
                         prior['kind'] != use['kind'] and
                         max(prior['output_range']['start_byte'], use['output_range']['start_byte']) <
                         min(prior['output_range']['end_byte'], use['output_range']['end_byte'])
                         for prior in uses.values()),
                 'Contradictory classifications for overlapping output expressions')
        _require(not any(prior['source'] == source and prior['output_path'] == use['output_path'] and
                         prior['output_range'] == use['output_range'] for prior in uses.values()),
                 'Duplicate source/output expression under another use ID')
        spans[span_key] = use['kind']
        _require(isinstance(use['attributions'], list), 'Attributions must be an array')
        attribution_ids = set()
        for attribution in use['attributions']:
            _object(attribution, {'output_path', 'output_range'}, 'Malformed attribution output reference')
            _require(attribution['output_path'] in output_bytes, 'Attribution is absent from output inventory')
            _span(attribution['output_range'], output_bytes[attribution['output_path']], 'Attribution')
            identity = digest(attribution)
            _require(identity not in attribution_ids, 'Duplicate attribution reference')
            attribution_ids.add(identity)
        uses[uid] = use
        needed.add(aid)
    source_bytes, source_files = _source_content(register['source_evidence'], needed, index, source_root)
    for use in uses.values():
        if use['kind'] == 'REFERENCES_ONLY':
            _require(use['source_range'] is None, 'Reference-only rows must not claim copied source expression')
        else:
            _span(use['source_range'], source_bytes[use['source']['artifact_id']], 'Source')
            if use['kind'] == 'LICENSED_COPY':
                source_span, output_span = use['source_range'], use['output_range']
                _require(source_bytes[use['source']['artifact_id']][source_span['start_byte']:source_span['end_byte']] ==
                         output_bytes[use['output_path']][output_span['start_byte']:output_span['end_byte']],
                         'LICENSED_COPY spans are not identical source/output bytes; review the actual use kind')
    dispositions = set()
    unreviewed = 0
    assigned = set()
    for entry in register['outputs']:
        _object(entry, {'path', 'disposition', 'use_ids', 'rationale'}, 'Malformed output disposition')
        _require(_text(entry['path']) and entry['path'] in paths and entry['path'] not in dispositions and
                 _text(entry['rationale']), 'Foreign or duplicate output disposition')
        expected = {uid for uid, use in uses.items() if use['output_path'] == entry['path']}
        ids = entry['use_ids']
        _require(isinstance(ids, list) and all(_text(uid) for uid in ids) and
                 len(set(ids)) == len(ids) and set(ids) == expected,
                 'Output disposition has dropped, foreign or duplicate use rows')
        _require(entry['disposition'] in {'UNREVIEWED',
                 'USES_RECORDED' if expected else 'NO_UPSTREAM_EXPRESSION'},
                 'Contradictory output disposition')
        unreviewed += entry['disposition'] == 'UNREVIEWED'
        dispositions.add(entry['path'])
        assigned.update(ids)
    _require(dispositions == paths and assigned == set(uses), 'Missing complete output/use disposition accounting')
    result.update(manifest_digest=digest(manifest), register_digest=digest(register),
                  output_inventory_digest=digest(observed), source_evidence_digest=digest(register['source_evidence']),
                  output_count=len(observed), denominator=len(uses), complete_output_inventory=True,
                  unreviewed_output_count=unreviewed,
                  copied_or_adapted_count=sum(u['kind'] in EXPRESSION_KINDS for u in uses.values()),
                  reference_only_count=sum(u['kind'] == 'REFERENCES_ONLY' for u in uses.values()),
                  independent_paraphrase_count=sum(u['kind'] == 'INDEPENDENT_PARAPHRASE' for u in uses.values()))
    subject = {k: manifest[k] if k in manifest else result[k] for k in SCOPE_FIELDS}
    result['subject'] = subject
    result['release_scope'] = manifest['release_scope']
    if not receipts:
        if policy:
            _policy(policy, subject, registered, current)
        result['diagnostics'] = ['No approved complete output/use inventory receipt; clearance unknown.']
    else:
        earliest = max([registered, *(_time(index[aid]['retrieved_at']) for aid in needed)])
        issued, policy_expiry = _policy(policy, subject, earliest, current)
        seen, references, inventory_seen = set(), {}, False
        for receipt in receipts:
            _require(isinstance(receipt, dict), 'Publication receipt must be an object')
            _require(receipt.get('kind') != 'OUTPUT_INVENTORY' or unreviewed == 0,
                     'Unreviewed output dispositions cannot receive inventory clearance')
            uid, inventory = _receipt(receipt, subject, policy, uses, issued, current,
                                      policy_expiry, evidence_root, references, not bool(uses))
            if inventory:
                _require(not inventory_seen, 'Duplicate output inventory receipt')
                inventory_seen = True
            else:
                _require(uid not in seen, 'Duplicate expression-use receipt')
                seen.add(uid)
        expression_count = len(seen)
        if inventory_seen:
            seen.update(uid for uid, use in uses.items() if use['kind'] not in EXPRESSION_KINDS)
        result.update(inventory_receipt_validated=inventory_seen,
                      use_register_complete=True if inventory_seen else None,
                      validated_expression_count=expression_count,
                      validated_use_ids=sorted(seen), completed=len(seen),
                      zero_use_clearance=inventory_seen and not bool(uses))
        complete = inventory_seen and len(seen) == len(uses)
        result['exact_use_clearance'] = complete if inventory_seen or expression_count else None
        result['authorized_distribution_decision'] = result['exact_use_clearance']
        if not inventory_seen:
            result['diagnostics'].append('Complete inventory review/audit/acceptance/distribution receipt is missing.')
        missing = sorted(uid for uid, use in uses.items() if use['kind'] in EXPRESSION_KINDS and uid not in seen)
        if missing:
            result['diagnostics'].append('Expression-use approvals missing for: ' + ', '.join(missing))
        for reference in references.values():
            _evidence(evidence_root, reference)
    if unreviewed:
        result['diagnostics'].append(f'{unreviewed} output use classifications remain unreviewed; use denominator is uncertified.')
    _require(output_inventory(output_root) == observed, 'Candidate output changed during validation')
    for path, sha in source_files:
        source_base = _root(source_root, 'source')
        _require(_file_sha256(_file(source_base, path.relative_to(source_base).as_posix())) == sha,
                 'Source evidence changed during validation')
    return validate_accounting_result(result)


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if argv and argv[0] == 'prepare-draft':
        parser = argparse.ArgumentParser(description='Inventory a candidate with explicit UNREVIEWED use dispositions.')
        parser.add_argument('--output-root', type=Path, required=True)
        parser.add_argument('--draft-directory', type=Path, required=True)
        for name in ('candidate-id', 'candidate-revision', 'distribution-scope'):
            parser.add_argument('--' + name, required=True)
        parser.add_argument('--release-scope', choices=['GES_V0_2', 'BOUNDED_PACKAGE'], default='BOUNDED_PACKAGE')
        args = parser.parse_args(argv[1:])
        try:
            _require(not args.draft_directory.exists(), 'Draft directory already exists; refusing overwrite')
            draft = prepare_draft(args.output_root, args.candidate_id, args.candidate_revision,
                                  args.distribution_scope, release_scope=args.release_scope)
            args.draft_directory.mkdir(parents=True)
            for key, value in draft.items():
                dump(args.draft_directory / (key + '.json'), value)
        except (ValueError, TypeError, KeyError, OSError) as exc:
            print(json.dumps({'valid': False, 'error': str(exc)}))
            return 2
        print(json.dumps({'draft_prepared': True, 'output_count': len(draft['manifest']['outputs']),
                          'all_use_classifications': 'UNREVIEWED', 'clearance': None}))
        return 0
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('manifest', 'register', 'receipts', 'policy', 'artifacts', 'output-root', 'source-root'):
        parser.add_argument('--' + name, type=Path, required=True)
    parser.add_argument('--pins', type=Path, default=ROOT / 'sources/sources.lock.json')
    parser.add_argument('--evidence-root', type=Path, default=ROOT)
    args = parser.parse_args(argv)
    try:
        artifacts = [json.loads(line) for line in args.artifacts.read_text().splitlines() if line.strip()]
        pins = {s['repository']: s['commit'] for s in load(args.pins)['sources']}
        result = publication_accounting(load(args.manifest), load(args.register), load(args.receipts),
                                         load(args.policy), artifacts, pins, output_root=args.output_root,
                                         source_root=args.source_root, evidence_root=args.evidence_root)
    except (ValueError, TypeError, KeyError, OSError, UnicodeError, RuntimeError, EOFError) as exc:
        print(json.dumps({'valid': False, 'error': str(exc)}))
        return 2
    print(json.dumps({'valid': True, **result}, indent=2))
    return 0 if result['exact_use_clearance'] is True else 1


if __name__ == '__main__':
    raise SystemExit(main())
