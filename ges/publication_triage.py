"""Produce source-bound publication review work without granting clearance.

Read every blob in an immutable Git tree. Structural source associations and
exact byte matches are review leads, never judgments of authorship or licensing.
No upstream text, authorization policy, approval receipt or accepted use is emitted.
"""
from __future__ import annotations

import argparse
from collections import Counter
import gzip
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote
import zlib

from .core import ROOT, digest, now
from .pinned_sources import verify_snapshot
from .publication_use import (DEFAULT_SOURCE_INVENTORY_REFERENCE,
                              DEFAULT_SOURCE_INVENTORY_SHA256, IDENTITY,
                              _artifacts, _file, _inventory_authority, _relative, _root)
from .published_assurance import _require, _time
from .source_fidelity import _file_sha256

EXPRESSION_FIELDS = {'statement', 'source_statement', 'objective', 'title',
                     'description', 'excerpt', 'quote', 'acceptance'}
MIN_EXPRESSION_BYTES = 40
MIN_EXPRESSION_WORDS = 6
URL = re.compile(rb'https://github\.com/([\w.-]+/[\w.-]+)/(blob|tree)/([a-f0-9]{40})/([^\s"\'<>`)\]}]+)')
TOKEN = re.compile(rb'"(?:[^"\\]|\\.)*"|[{}\[\],:]|[^\s{}\[\],:]+')
REQUIREMENTS = {
    'CLASSIFICATION': 'Review every output and classify each actual upstream use; the machine category is not a semantic disposition.',
    'OMISSION_AUDIT': 'An independent reviewer must assess omitted, transformed, inherited and uncited expression beyond the detector rules.',
    'AUTHORSHIP_AND_AUTHORITY': 'Identify the output author or rights holder and verify authority for the intended distribution; Git authorship and repository ownership are not grants.',
    'SOURCE_BODY_COMPARISON': 'Compare the exact proposed output with authenticated pinned source bytes; no match is not evidence of independent creation.',
    'EXPRESSION_GRANT_AND_ATTRIBUTION': 'For actual copied or adapted expression, determine component-specific grants, restrictions, attribution and modification notices, and bind exact source/output spans.',
    'LOCATOR_REPAIR': 'Resolve missing or mismatched source commits and paths without inventing membership in the pinned corpus.',
    'TEMPLATE_OR_CODE_ORIGIN': 'Inspect template, implementation, fixture and prompt ancestry, including inherited examples and dependencies not identifiable by six-source locators.',
    'CONTAINER_CONTENTS': 'Review decoded container contents and any rendering or redistribution form; the compressed file hash alone does not classify its content.',
    'MANUAL_FORMAT_REVIEW': 'The declared file format could not be fully parsed; inspect the exact bytes and identify all source uses manually or repair the format in a new candidate.',
    'EXACT_SCOPE_APPROVALS': 'Supply the separately authorized inventory review, independent audit, human acceptance and distribution decision; this triage supplies none.',
}


def _git(repository: Path, *args: str) -> bytes:
    return subprocess.check_output(['git', '-C', str(repository), *args], stderr=subprocess.PIPE)


def _blobs(repository: Path, revision: str):
    """Use Git objects, not mutable worktree files or filters, as the output scope."""
    _require(re.fullmatch('[a-f0-9]{40}', revision) is not None,
             'Candidate revision must be an exact 40-character commit SHA')
    _require(_git(repository, 'cat-file', '-t', revision).strip() == b'commit',
             'Candidate revision is not a commit')
    entries = []
    for entry in _git(repository, 'ls-tree', '-rz', '--full-tree', revision).split(b'\0'):
        if not entry:
            continue
        metadata, path_bytes = entry.split(b'\t', 1)
        mode, kind, sha = metadata.decode('ascii').split()
        path = path_bytes.decode('utf-8')
        _relative(path)
        _require(kind == 'blob' and mode in {'100644', '100755'},
                 'Nonregular candidate Git entry: ' + path)
        entries.append((path, mode, sha))
    process = subprocess.Popen(['git', '-C', str(repository), 'cat-file', '--batch'],
                               stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        for path, mode, sha in sorted(entries):
            process.stdin.write((sha + '\n').encode('ascii'))
            process.stdin.flush()
            found, kind, size = process.stdout.readline().decode('ascii').split()
            _require(found == sha and kind == 'blob', 'Unexpected Git blob response')
            raw = process.stdout.read(int(size))
            _require(len(raw) == int(size) and process.stdout.read(1) == b'\n', 'Incomplete Git blob response')
            _require(hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest() == sha,
                     'Candidate Git blob differs from its object identity')
            yield {'path': path, 'git_mode': mode, 'git_blob_sha': sha,
                   'sha256': hashlib.sha256(raw).hexdigest(), 'size_bytes': len(raw)}, raw
        process.stdin.close()
        _require(process.wait() == 0, 'Git object read failed')
    finally:
        if process.poll() is None:
            process.kill()
            process.wait()
        for stream in (process.stdin, process.stdout, process.stderr):
            stream.close()


def _pointer(value: str) -> str:
    return value.replace('~', '~0').replace('/', '~1')


def _json_spans(raw: bytes) -> dict[str, dict]:
    """Locate string values in already validated JSON, without reserializing bytes."""
    tokens = iter(TOKEN.finditer(raw))
    spans = {}

    def visit(token, pointer):
        value = token.group()
        if value == b'{':
            token = next(tokens)
            if token.group() == b'}':
                return
            while True:
                key = json.loads(token.group())
                _require(next(tokens).group() == b':', 'Malformed JSON object')
                visit(next(tokens), pointer + '/' + _pointer(key))
                token = next(tokens)
                if token.group() == b'}':
                    return
                _require(token.group() == b',', 'Malformed JSON object separator')
                token = next(tokens)
        elif value == b'[':
            token, index = next(tokens), 0
            if token.group() == b']':
                return
            while True:
                visit(token, pointer + '/' + str(index))
                token = next(tokens)
                if token.group() == b']':
                    return
                _require(token.group() == b',', 'Malformed JSON array separator')
                token, index = next(tokens), index + 1
        elif value.startswith(b'"'):
            start, end = token.start() + 1, token.end() - 1
            spans[pointer] = {'start_byte': start, 'end_byte': end,
                              'sha256': hashlib.sha256(raw[start:end]).hexdigest()}

    visit(next(tokens), '')
    return spans


def _unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        _require(key not in result, 'Duplicate JSON key: ' + key)
        result[key] = value
    return result


def _role(path: str) -> str:
    if path == 'THIRD_PARTY_NOTICES.md' or 'LICENSE' in Path(path).name:
        return 'NOTICE_OR_LICENSE_TEXT'
    prefix = path.split('/')[0]
    return {'evidence': 'EVIDENCE_RECORD', 'controls': 'CONTROL_DRAFT',
            'generated': 'GENERATED_VIEW', 'templates': 'TEMPLATE',
            'ges': 'IMPLEMENTATION', 'scripts': 'IMPLEMENTATION', 'tests': 'TEST_FIXTURE_OR_CODE',
            '.codex': 'AGENT_INSTRUCTIONS', '.github': 'REPOSITORY_AUTOMATION',
            'docs': 'PROJECT_DOCUMENTATION', 'sources': 'SOURCE_METADATA',
            'schemas': 'DATA_CONTRACT', 'profiles': 'TARGET_PROFILE'}.get(prefix, 'PROJECT_SUPPORT_FILE')


def _analyze_content(identity, raw, by_identity, source_index, derived_fields=()):
    row = {**identity, 'content_role': _role(identity['path']), 'disposition': 'UNREVIEWED',
           'source_artifact_ids': [], 'unresolved_locators': [], 'expression_candidates': [],
           'review_requirements': ['CLASSIFICATION', 'OMISSION_AUDIT', 'AUTHORSHIP_AND_AUTHORITY', 'EXACT_SCOPE_APPROVALS']}
    associated, unresolved, candidates = set(), {}, []
    source_repositories = {row['source'] for row in source_index.values()}
    payload = raw
    if identity['path'].endswith('.gz'):
        payload = gzip.decompress(raw)
        row.update(content_format='GZIP', decoded_payload_sha256=hashlib.sha256(payload).hexdigest(),
                   decoded_payload_size_bytes=len(payload))
        row['review_requirements'].append('CONTAINER_CONTENTS')
    else:
        row['content_format'] = 'UTF8_TEXT'

    def locate(source, commit, path, pointer):
        if not all(isinstance(value, str) and value for value in (source, commit, path)):
            return None
        key = (source, commit, path)
        artifact = by_identity.get(key)
        if artifact is not None:
            associated.add(artifact['artifact_id'])
            return artifact['artifact_id']
        if re.fullmatch(r'[\w.-]+/[\w.-]+', source):
            encoded = digest(list(key))
            if encoded not in unresolved:
                unresolved[encoded] = {'source': source, 'commit': commit, 'path': path,
                                       'first_locator': pointer, 'occurrences': 0,
                                       'status': 'NOT_IN_AUTHENTICATED_PINNED_INVENTORY' if source in source_repositories
                                                 else 'OUTSIDE_AUTHENTICATED_SOURCE_INVENTORY'}
            unresolved[encoded]['occurrences'] += 1
        return None

    for match in URL.finditer(payload):
        source, _, commit, path = (part.decode('utf-8') for part in match.groups())
        locate(source, commit, unquote(path.split('#', 1)[0]), 'url-byte:' + str(match.start()))

    if row['content_role'] == 'GENERATED_VIEW':
        for field in derived_fields:
            value = field['_value']
            origin = {'path': 'controls/catalog.json', 'locator': field['locator']}
            if field.get('additional_canonical_locators'):
                origin['additional_locators'] = field['additional_canonical_locators']
            start = payload.find(value)
            while start >= 0:
                associated.update(field['source_artifact_ids'])
                candidates.append({**field, 'locator': 'raw-byte:' + str(start),
                                   'derived_from': origin,
                                   'range_encoding': 'RAW_BYTES',
                                   'output_range': {'start_byte': start, 'end_byte': start + len(value),
                                                    'sha256': hashlib.sha256(value).hexdigest()}})
                start = payload.find(value, start + len(value))

    def walk(value, pointer, context, references, spans):
        if isinstance(value, dict):
            context = dict(context)
            for source_key in ('source', 'repository'):
                if isinstance(value.get(source_key), str):
                    context['source'] = value[source_key]
            for key in ('commit', 'path'):
                if isinstance(value.get(key), str):
                    context[key] = value[key]
            own = locate(context.get('source'), context.get('commit'), context.get('path'), pointer)
            local = {own} if own else set(references)
            for ref in value.get('sources', []) if isinstance(value.get('sources'), list) else []:
                if isinstance(ref, dict):
                    found = locate(ref.get('repository', ref.get('source')), ref.get('commit'), ref.get('path'), pointer + '/sources')
                    if found:
                        local.add(found)
            for key, child in value.items():
                child_pointer = pointer + '/' + _pointer(key)
                if key in EXPRESSION_FIELDS and local:
                    values = [(child_pointer, child)] if isinstance(child, str) else [
                        (child_pointer + '/' + str(index), text) for index, text in enumerate(child)
                        if isinstance(text, str)] if isinstance(child, list) else []
                    for value_pointer, text in values:
                        encoded = text.encode('utf-8')
                        if len(encoded) >= MIN_EXPRESSION_BYTES and len(text.split()) >= MIN_EXPRESSION_WORDS:
                            span = spans[value_pointer]
                            candidates.append({'locator': value_pointer, 'field': key,
                                               'decoded_text_sha256': hashlib.sha256(encoded).hexdigest(),
                                               'decoded_text_bytes': len(encoded),
                                               'range_encoding': 'DECODED_GZIP_JSON_STRING' if row['content_format'] == 'GZIP' else 'JSON_STRING_LITERAL_INTERIOR',
                                               'output_range': span, 'source_artifact_ids': sorted(local),
                                               '_value': encoded})
                walk(child, child_pointer, context, local, spans)
        elif isinstance(value, list):
            for index, child in enumerate(value):
                walk(child, pointer + '/' + str(index), context, references, spans)

    name = identity['path'].removesuffix('.gz')
    if name.endswith('.json'):
        value = json.loads(payload, object_pairs_hook=_unique_pairs)
        walk(value, '', {}, set(), _json_spans(payload))
        row['content_format'] = 'JSON' if row['content_format'] != 'GZIP' else 'GZIP_JSON'
    elif name.endswith('.jsonl'):
        offset = 0
        for index, line in enumerate(payload.splitlines(keepends=True)):
            if line.strip():
                value = json.loads(line, object_pairs_hook=_unique_pairs)
                spans = {'/lines/' + str(index) + pointer: {**span, 'start_byte': span['start_byte'] + offset,
                                                          'end_byte': span['end_byte'] + offset}
                         for pointer, span in _json_spans(line).items()}
                walk(value, '/lines/' + str(index), {}, set(), spans)
            offset += len(line)
        row['content_format'] = 'JSONL' if row['content_format'] != 'GZIP' else 'GZIP_JSONL'
    else:
        try:
            payload.decode('utf-8')
        except UnicodeError:
            row['content_format'] = 'BINARY'
        if row['content_format'] == 'UTF8_TEXT' and associated:
            for match in re.finditer(rb'(?s)(?:\A|\n\s*\n)(.+?)(?=\n\s*\n|\Z)', payload):
                text = match.group(1)
                if len(text) >= MIN_EXPRESSION_BYTES and len(text.split()) >= MIN_EXPRESSION_WORDS:
                    candidates.append({'locator': 'paragraph-byte:' + str(match.start(1)), 'field': 'paragraph',
                                       'decoded_text_sha256': hashlib.sha256(text).hexdigest(), 'decoded_text_bytes': len(text),
                                       'range_encoding': 'RAW_BYTES',
                                       'output_range': {'start_byte': match.start(1), 'end_byte': match.end(1),
                                                        'sha256': hashlib.sha256(text).hexdigest()},
                                       'source_artifact_ids': sorted(associated), '_value': text})
    row['source_artifact_ids'] = sorted(associated)
    row['unresolved_locators'] = sorted(unresolved.values(), key=lambda item: (item['source'], item['commit'], item['path']))
    row['expression_candidates'] = candidates
    if candidates:
        row['triage_category'] = 'SOURCE_ASSOCIATED_EXPRESSION_CANDIDATES'
        row['review_requirements'] += ['SOURCE_BODY_COMPARISON', 'EXPRESSION_GRANT_AND_ATTRIBUTION']
    elif associated:
        row['triage_category'] = 'SOURCE_LOCATORS_PRESENT'
    else:
        row['triage_category'] = 'NO_SOURCE_LOCATOR_DETECTED'
    if unresolved:
        row['review_requirements'].append('LOCATOR_REPAIR')
    if row['content_role'] in {'TEMPLATE', 'IMPLEMENTATION', 'TEST_FIXTURE_OR_CODE', 'AGENT_INSTRUCTIONS', 'REPOSITORY_AUTOMATION'}:
        row['review_requirements'].append('TEMPLATE_OR_CODE_ORIGIN')
    return row


def _analyze(identity, raw, by_identity, source_index, derived_fields=()):
    try:
        row = _analyze_content(identity, raw, by_identity, source_index, derived_fields)
        row['scan_status'] = 'COMPLETE_WITHIN_DECLARED_METHOD'
        return row
    except (ValueError, UnicodeError, EOFError, OSError, zlib.error) as exc:
        # A malformed candidate file still belongs to the complete Git inventory.
        return {**identity, 'content_role': _role(identity['path']), 'disposition': 'UNREVIEWED',
                'content_format': 'UNPARSED', 'scan_status': 'INCOMPLETE', 'scan_error': str(exc),
                'source_artifact_ids': [], 'unresolved_locators': [], 'expression_candidates': [],
                'triage_category': 'CONTENT_PARSE_REQUIRES_REVIEW',
                'review_requirements': ['CLASSIFICATION', 'OMISSION_AUDIT', 'AUTHORSHIP_AND_AUTHORITY',
                                        'EXACT_SCOPE_APPROVALS', 'MANUAL_FORMAT_REVIEW']}


def triage(repository: Path, revision: str, artifacts: list[dict], pins: dict[str, str], *,
           source_root: Path | None = None,
           source_inventory_reference: Path = DEFAULT_SOURCE_INVENTORY_REFERENCE,
           source_inventory_sha256: str = DEFAULT_SOURCE_INVENTORY_SHA256) -> dict:
    authority = _inventory_authority(source_inventory_reference, source_inventory_sha256)
    source_index = _artifacts(artifacts, pins, _time(now()), authority)
    by_identity = {(row['source'], row['commit'], row['path']): row for row in artifacts}
    outputs, derived_fields = [], []
    rights_raw = None
    for identity, raw in _blobs(repository, revision):
        row = _analyze(identity, raw, by_identity, source_index, derived_fields)
        outputs.append(row)
        if row['path'] == 'controls/catalog.json':
            # Git path order visits the canonical catalog before generated views.
            groups = {}
            for candidate in row['expression_candidates']:
                value = candidate['_value']
                if value not in groups:
                    groups[value] = dict(candidate)
                else:
                    previous = groups[value]
                    previous['source_artifact_ids'] = sorted(set(previous['source_artifact_ids']) |
                                                              set(candidate['source_artifact_ids']))
                    previous.setdefault('additional_canonical_locators', []).append(candidate['locator'])
            derived_fields = list(groups.values())
        if row['path'] == 'evidence/rights-review-queue.json':
            rights_raw = raw
    _require(bool(outputs), 'Empty candidate output tree')
    needed = {artifact_id for row in outputs for candidate in row['expression_candidates']
              for artifact_id in candidate['source_artifact_ids']}
    bodies, observations = {}, []
    if source_root is not None:
        source_root = _root(source_root, 'source')
        for source, commit in sorted(pins.items()):
            rows = [row for row in artifacts if row['source'] == source]
            retain = [row['path'] for row in rows if row['artifact_id'] in needed and row['kind'] == 'text']
            path = _file(source_root, source.replace('/', '__') + '.text.jsonl.gz')
            texts = verify_snapshot(path, rows, source, commit, retain=retain)
            bodies.update({by_identity[(source, commit, path)]['artifact_id']: text.encode('utf-8')
                           for path, text in texts.items()})
            observations.append({'source': source, 'commit': commit, 'snapshot_path': path.name,
                                 'snapshot_sha256': _file_sha256(path), 'status': 'COMPLETE_PINNED_TEXT_VALIDATED',
                                 'retained_for_comparison': len(texts)})
    for row in outputs:
        for candidate in row['expression_candidates']:
            value = candidate.pop('_value')
            candidate['body_comparison'] = 'NOT_SUPPLIED' if source_root is None else 'NO_EXACT_MATCH_FOUND'
            candidate['exact_matches'] = []
            candidate['compared_source_artifact_ids'] = []
            candidate['unavailable_source_artifact_ids'] = []
            for artifact_id in candidate['source_artifact_ids']:
                raw = bodies.get(artifact_id)
                if raw is None:
                    candidate['unavailable_source_artifact_ids'].append(artifact_id)
                    continue
                candidate['compared_source_artifact_ids'].append(artifact_id)
                start = raw.find(value)
                if start >= 0:
                    candidate['exact_matches'].append({'artifact_id': artifact_id,
                        'source_range': {'start_byte': start, 'end_byte': start + len(value),
                                         'sha256': hashlib.sha256(value).hexdigest()},
                        'match_kind': 'EXACT_DECODED_CONTAINER_STRING' if candidate['range_encoding'].startswith('DECODED_GZIP')
                                      else 'EXACT_RAW_BYTES' if candidate['output_range']['sha256'] == hashlib.sha256(value).hexdigest()
                                      else 'EXACT_DECODED_JSON_STRING'})
            if candidate['exact_matches']:
                candidate['body_comparison'] = 'EXACT_MATCH_FOUND'
            elif source_root is not None and candidate['unavailable_source_artifact_ids']:
                candidate['body_comparison'] = 'SOURCE_BODY_COMPARISON_INCOMPLETE'
        row['exact_match_candidate_count'] = sum(bool(item['exact_matches']) for item in row['expression_candidates'])
        if row['exact_match_candidate_count']:
            row['triage_category'] = 'EXACT_SOURCE_EXPRESSION_MATCHES'
    used = {artifact_id for row in outputs for artifact_id in row['source_artifact_ids']}
    rights_findings = []
    if rights_raw is not None:
        for index, finding in enumerate(json.loads(rights_raw)['records']):
            source = by_identity.get((finding.get('source'), finding.get('commit'), finding.get('path')))
            if source is not None and source['artifact_id'] in used:
                rights_findings.append({'artifact_id': source['artifact_id'],
                                        'evidence_path': 'evidence/rights-review-queue.json',
                                        'evidence_sha256': hashlib.sha256(rights_raw).hexdigest(),
                                        'json_pointer': '/records/' + str(index), 'record_digest': digest(finding),
                                        'source_digest_matches': finding.get('content_sha256') == source['sha256'],
                                        'recorded_status': finding.get('status'),
                                        'recorded_issue_count': len(finding.get('file_specific_issues', [])),
                                        'clearance_inferred': False})
    inventory = [{key: row[key] for key in ('path', 'sha256', 'size_bytes')} for row in outputs]
    return {'schema': 'ges.publication-output-triage.v1', 'candidate_revision': revision,
            'candidate_tree': _git(repository, 'rev-parse', revision + '^{tree}').decode().strip(),
            'scope': 'Every tracked regular file in the exact immutable candidate Git tree; no path exclusions.',
            'output_inventory_digest': digest(inventory), 'source_inventory_digest': digest(artifacts),
            'pins_digest': digest(pins), 'source_inventory_reference_digest': source_inventory_sha256,
            'method': {'implementation_sha256': _file_sha256(Path(__file__)),
                       'minimum_expression_utf8_bytes': MIN_EXPRESSION_BYTES,
                       'minimum_expression_words': MIN_EXPRESSION_WORDS,
                       'expression_field_names': sorted(EXPRESSION_FIELDS),
                       'comparison': 'Exact decoded field or paragraph bytes in associated authenticated source text; no fuzzy matching or semantic inference.'},
            'summary': {'output_count': len(outputs), 'output_bytes': sum(row['size_bytes'] for row in outputs),
                        'triage_categories': dict(sorted(Counter(row['triage_category'] for row in outputs).items())),
                        'content_roles': dict(sorted(Counter(row['content_role'] for row in outputs).items())),
                        'source_associated_outputs': sum(bool(row['source_artifact_ids']) for row in outputs),
                        'unique_source_artifacts': len(used),
                        'expression_candidate_count': sum(len(row['expression_candidates']) for row in outputs),
                        'exact_match_candidate_count': sum(row['exact_match_candidate_count'] for row in outputs),
                        'unresolved_locator_count': sum(len(row['unresolved_locators']) for row in outputs),
                        'scan_incomplete_output_count': sum(row['scan_status'] == 'INCOMPLETE' for row in outputs),
                        'unreviewed_output_count': len(outputs)},
            'source_body_observations': observations,
            'existing_rights_finding_references': rights_findings,
            'source_artifacts': [{**{key: source_index[artifact_id][key] for key in sorted(IDENTITY)},
                                  'kind': source_index[artifact_id]['kind']}
                                 for artifact_id in sorted(used)],
            'review_requirement_definitions': REQUIREMENTS,
            'authority': {'semantic_review_completed': False, 'actual_use_register_complete': False,
                          'human_approval_created': False, 'rights_clearance_granted': False,
                          'publication_performed': False, 'accepted_control_credit': 0},
            'limitations': ['Categories describe detector observations, not ownership, originality, licensing or semantic review.',
                            'Exact matches establish bytes, not historical copying direction or permission; common and legal text can match several sources.',
                            'No match and no source locator cannot establish independent creation or absence of upstream expression.',
                            'Only named fields, source associations and paragraphs are tested; transformed, short, uncited, binary and externally inherited expression require review.',
                            'Compressed-container ranges locate decoded payload bytes and are not valid publication output spans without a concrete distribution-form review.',
                            'This packet is not a publication use register, clearance result, authority policy or approval receipt.'],
            'outputs': outputs}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repository', type=Path, default=ROOT)
    parser.add_argument('--revision', required=True)
    parser.add_argument('--artifacts', type=Path, required=True)
    parser.add_argument('--pins', type=Path, default=ROOT / 'sources/sources.lock.json')
    parser.add_argument('--source-root', type=Path)
    parser.add_argument('--source-inventory-reference', type=Path, default=DEFAULT_SOURCE_INVENTORY_REFERENCE)
    parser.add_argument('--source-inventory-sha256', default=DEFAULT_SOURCE_INVENTORY_SHA256)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        _require(not args.output.exists() and not args.output.is_symlink(), 'Refusing to overwrite triage output')
        opener = gzip.open if args.artifacts.suffix == '.gz' else open
        with opener(args.artifacts, 'rt', encoding='utf-8') as stream:
            artifacts = [json.loads(line) for line in stream if line.strip()]
        pins = {row['repository']: row['commit'] for row in json.loads(args.pins.read_text())['sources']}
        report = triage(args.repository, args.revision, artifacts, pins, source_root=args.source_root,
                        source_inventory_reference=args.source_inventory_reference,
                        source_inventory_sha256=args.source_inventory_sha256)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        if args.output.suffix == '.gz':
            with args.output.open('xb') as destination:
                with gzip.GzipFile(filename='', mode='wb', fileobj=destination, mtime=0) as compressed:
                    with io.TextIOWrapper(compressed, encoding='utf-8') as stream:
                        json.dump(report, stream, ensure_ascii=False, sort_keys=True, separators=(',', ':'))
                        stream.write('\n')
        else:
            with args.output.open('x', encoding='utf-8') as stream:
                json.dump(report, stream, ensure_ascii=False, sort_keys=True, separators=(',', ':'))
                stream.write('\n')
    except (ValueError, TypeError, KeyError, OSError, UnicodeError, EOFError, subprocess.SubprocessError) as exc:
        print(json.dumps({'valid': False, 'error': str(exc)}))
        return 2
    print(json.dumps({'triage_prepared': True, **report['summary'], 'clearance': None}))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
