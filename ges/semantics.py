"""Semantic record contracts; structural validation does not certify meaning."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from .core import ROOT

KINDS = ('source-charter', 'semantic-occurrence', 'semantic-proposition',
         'reconciliation-decision', 'policy-decision')


def canonical_bytes(value: object) -> bytes:
    """Encode JSON deterministically without accepting non-finite numbers."""
    return json.dumps(value, sort_keys=True, separators=(',', ':'),
                      ensure_ascii=False, allow_nan=False).encode('utf-8')


def stable_id(record: dict) -> str:
    """Bind occurrence identity to source and proposition identity to meaning."""
    kind = record['schema'].removeprefix('ges.').removesuffix('.v1')
    if kind not in KINDS:
        raise ValueError('Unsupported semantic schema')
    if kind == 'semantic-occurrence':
        subject = record['source']
    elif kind == 'semantic-proposition':
        subject = record['semantic_ast']
    else:
        subject = {key: value for key, value in record.items() if key != 'id'}
    return kind + ':' + hashlib.sha256(canonical_bytes(subject)).hexdigest()


def _validate(value: object, schema: dict, path: str = '$') -> None:
    """Validate the closed JSON Schema vocabulary used by A5 contracts."""
    if 'const' in schema and value != schema['const']:
        raise ValueError(path + ': incorrect schema identity')
    types = schema.get('type', [])
    types = [types] if isinstance(types, str) else types
    matches = {'object': isinstance(value, dict), 'array': isinstance(value, list),
               'string': isinstance(value, str), 'integer': type(value) is int,
               'null': value is None}
    if types and not any(matches.get(kind, False) for kind in types):
        raise ValueError(path + ': incorrect type')
    if 'enum' in schema and value not in schema['enum']:
        raise ValueError(path + ': unsupported value')
    if isinstance(value, str):
        if len(value) < schema.get('minLength', 0):
            raise ValueError(path + ': empty string')
        if 'pattern' in schema and not re.search(schema['pattern'], value):
            raise ValueError(path + ': invalid string')
    if type(value) is int and value < schema.get('minimum', value):
        raise ValueError(path + ': below minimum')
    if isinstance(value, list):
        if len(value) < schema.get('minItems', 0):
            raise ValueError(path + ': empty array')
        if schema.get('uniqueItems') and len({canonical_bytes(v) for v in value}) != len(value):
            raise ValueError(path + ': duplicate items')
        for index, item in enumerate(value):
            _validate(item, schema['items'], f'{path}[{index}]')
    if isinstance(value, dict):
        properties = schema['properties']
        if set(schema['required']) - set(value):
            raise ValueError(path + ': missing required fields')
        if schema.get('additionalProperties') is False and set(value) - set(properties):
            raise ValueError(path + ': unknown fields')
        for key, item in value.items():
            _validate(item, properties[key], path + '.' + key)


def validate_record(record: dict) -> None:
    """Check record structure and identity, never reviewer authority or truth."""
    if not isinstance(record, dict) or record.get('schema') not in {
            'ges.' + kind + '.v1' for kind in KINDS}:
        raise ValueError('Unsupported semantic schema')
    kind = record['schema'][4:-3]
    schema = json.loads((ROOT / 'schemas/semantics' / (kind + '.v1.json')).read_text())
    _validate(record, schema)
    if record['id'] != stable_id(record):
        raise ValueError('Semantic record identity differs from content')
    if kind == 'semantic-occurrence':
        source = record['source']
        if source['start_line'] > source['end_line']:
            raise ValueError('Reversed source span')
        path = source['path']
        if path.startswith('/') or '\\' in path or '..' in path.split('/'):
            raise ValueError('Unsafe source path')
    for key in ('review', 'primary_review', 'omission_review', 'owner_approval'):
        if key in record:
            review = record[key]
            fields = (review['reviewer'], review['evidence_reference'])
            if review['status'] == 'REVIEWED' and not all(
                    isinstance(field, str) and field.strip() for field in fields):
                raise ValueError('Reviewed record requires identity and evidence reference')
            if review['status'] == 'PROPOSED' and fields != (None, None):
                raise ValueError('Proposal cannot assert review evidence')


def configure_parser(subparsers) -> None:
    parser = subparsers.add_parser('semantics', help=__doc__)
    commands = parser.add_subparsers(dest='semantic_command', required=True)
    command = commands.add_parser('validate', help='Validate JSONL record structure')
    command.add_argument('--input', type=Path, required=True)
    command = commands.add_parser('extract', help='Compile authored B0 community annotations')
    command.add_argument('--manifest', type=Path, required=True)
    command.add_argument('--annotations', type=Path, required=True)
    command.add_argument('--sources', type=Path, required=True)
    command.add_argument('--output', type=Path, required=True)
    command.add_argument('--check', action='store_true', help='Compare existing outputs without writing')
    for name in ('reconcile', 'audit'):
        command = commands.add_parser(name, help=(
            'Produce comparison proposals' if name == 'reconcile'
            else 'Validate authorized reconciliation and audit receipts'))
        command.add_argument('--propositions', type=Path)
        command.add_argument('--controls', type=Path)
        command.add_argument('--output', type=Path)
        if name == 'audit':
            command.add_argument('--decisions', type=Path)
            command.add_argument('--authority', type=Path)
            command.add_argument('--audits', type=Path)
            command.add_argument('--evidence-root', type=Path)


def run(args) -> int:
    if args.semantic_command == 'extract':
        from .community_extraction import extract
        report = extract(args.manifest, args.annotations, args.sources, args.output, check=args.check)
        print(json.dumps(report, sort_keys=True))
        return 0
    if args.semantic_command in ('reconcile', 'audit') and args.propositions:
        from .reconciliation import audit, propose, read_records
        required = ('controls', 'output')
        if args.semantic_command == 'audit':
            required += ('decisions', 'authority', 'audits', 'evidence_root')
        if any(getattr(args, field) is None for field in required):
            raise ValueError('Missing reconciliation inputs: ' + ', '.join(required))
        propositions = read_records(args.propositions, 'semantic-proposition')
        catalog = json.loads(args.controls.read_text(encoding='utf-8'))
        if args.semantic_command == 'reconcile':
            report = propose(propositions, catalog)
        else:
            report = audit(
                propositions, catalog,
                read_records(args.decisions, 'reconciliation-decision'),
                json.loads(args.authority.read_text(encoding='utf-8')),
                args.evidence_root,
                json.loads(args.audits.read_text(encoding='utf-8')))
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open('x', encoding='utf-8') as stream:
            stream.write(canonical_bytes(report).decode('utf-8') + '\n')
        print(json.dumps({'output': str(args.output), 'schema': report['schema'],
                          'semantic_truth_certified': False, 'policy_adopted': False}))
        return (1 if args.semantic_command == 'audit'
                and not report['decision_accounting_complete'] else 0)
    if args.semantic_command in ('reconcile', 'audit') and any(
            value is not None for key, value in vars(args).items()
            if key in ('controls', 'output', 'decisions', 'authority', 'audits', 'evidence_root')):
        raise ValueError('Missing --propositions')
    if args.semantic_command != 'validate':
        print(json.dumps({'status': 'UNAVAILABLE', 'command': args.semantic_command,
                          'reason': 'Reserved for a later implementation tranche'}))
        return 2
    seen = set()
    count = 0
    with args.input.open(encoding='utf-8') as stream:
        for number, line in enumerate(stream, 1):
            if not line.strip():
                continue
            try:
                record = json.loads(line)
                validate_record(record)
                if record['id'] in seen:
                    raise ValueError('Duplicate semantic record identity')
                seen.add(record['id'])
                count += 1
            except (ValueError, KeyError, TypeError) as exc:
                raise ValueError(f'Line {number}: {exc}') from exc
    if not count:
        raise ValueError('No semantic records to validate')
    print(json.dumps({'valid': True, 'records': count,
                      'scope': 'STRUCTURE_AND_IDENTITY_ONLY',
                      'semantic_truth_certified': False, 'policy_adopted': False}))
    return 0
