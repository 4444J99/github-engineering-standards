"""Agent verification receipts: strict schema, cross-field semantics, PR-body injection.

Standard library only so the reusable GitHub Action can run this file directly
(``python ges/receipts.py ...``) without installing dependencies.

A receipt records what an agent observed. Validation proves structure and internal
consistency; it does not authenticate the agent, any named human, or the commands'
real execution. See docs/agent-verification-receipts.md for the formal semantics.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / 'schemas' / 'receipts' / 'agent-verification-receipt.v1.json'
SCHEMA_ID = 'ges.agent-verification-receipt.v1'
ID_PREFIX = 'agent-verification-receipt:'

BEGIN_MARKER = '<!-- ges:agent-verification-receipt:begin -->'
END_MARKER = '<!-- ges:agent-verification-receipt:end -->'
MARKER_FRAGMENT = 'ges:agent-verification-receipt:'
PR_BODY_LIMIT = 65536

# Formal mapping from GitHub check-run conclusions (REST "conclusion" values) to
# receipt statuses. Only `success` can be PASS; skipped, neutral, cancelled, stale
# and action_required are never green (they are NOT_VERIFIABLE, not NOT_RUN: the
# provider returned a verdict that does not establish success). A check with no
# conclusion yet is NOT_RUN and carries `github_conclusion: null`.
GITHUB_CONCLUSION_STATUS = {
    'success': 'PASS',
    'failure': 'FAIL',
    'timed_out': 'FAIL',
    'cancelled': 'NOT_VERIFIABLE',
    'skipped': 'NOT_VERIFIABLE',
    'neutral': 'NOT_VERIFIABLE',
    'stale': 'NOT_VERIFIABLE',
    'action_required': 'NOT_VERIFIABLE',
}

# The closed JSON Schema vocabulary the validator implements. A test walks the
# schema and fails on any keyword outside this set, so the schema cannot silently
# carry rules that nothing enforces.
SUPPORTED_KEYWORDS = frozenset({
    '$schema', '$id', '$comment', 'title', '$defs', '$ref', 'type', 'const', 'enum',
    'pattern', 'minLength', 'maxLength', 'minimum', 'maximum', 'minItems', 'maxItems',
    'uniqueItems', 'items', 'properties', 'required', 'additionalProperties', 'anyOf',
})


def canonical_bytes(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(',', ':'),
                      ensure_ascii=False, allow_nan=False).encode('utf-8')


def receipt_id(receipt: dict) -> str:
    """Identity binds every field except `id`."""
    body = {key: value for key, value in receipt.items() if key != 'id'}
    return ID_PREFIX + hashlib.sha256(canonical_bytes(body)).hexdigest()


def seal(receipt: dict) -> dict:
    """Return a copy with `schema` set and `id` computed. Does not validate."""
    sealed = dict(receipt)
    sealed['schema'] = SCHEMA_ID
    sealed['id'] = receipt_id(sealed)
    return sealed


def load_schema() -> dict:
    return json.loads(SCHEMA_PATH.read_text(encoding='utf-8'))


def _resolve(schema: dict, root: dict) -> dict:
    ref = schema.get('$ref')
    if ref is None:
        return schema
    if not ref.startswith('#/$defs/'):
        raise ValueError('Unsupported $ref ' + ref)
    return root['$defs'][ref[len('#/$defs/'):]]


def _matches(value: object, kind: str) -> bool:
    return {
        'object': isinstance(value, dict),
        'array': isinstance(value, list),
        'string': isinstance(value, str),
        'integer': type(value) is int,
        'boolean': type(value) is bool,
        'null': value is None,
    }[kind]


def _check(value: object, schema: dict, root: dict, path: str, errors: list[str]) -> None:
    schema = _resolve(schema, root)
    if 'anyOf' in schema:
        branches = []
        for branch in schema['anyOf']:
            attempt: list[str] = []
            _check(value, branch, root, path, attempt)
            if not attempt:
                return
            branches.append(attempt)
        errors.append(path + ': matches none of the permitted forms (' + '; '.join(
            sorted({e for attempt in branches for e in attempt[:1]})) + ')')
        return
    if 'const' in schema and value != schema['const']:
        errors.append(path + ': must equal ' + json.dumps(schema['const']))
        return
    if 'type' in schema:
        kinds = [schema['type']] if isinstance(schema['type'], str) else schema['type']
        if not any(_matches(value, kind) for kind in kinds):
            errors.append(path + ': incorrect type (expected ' + '|'.join(kinds) + ')')
            return
    if 'enum' in schema and value not in schema['enum']:
        errors.append(path + ': unsupported value')
    if isinstance(value, str):
        if len(value) < schema.get('minLength', 0):
            errors.append(path + ': too short')
        if len(value) > schema.get('maxLength', len(value)):
            errors.append(path + ': too long')
        if 'pattern' in schema and not re.search(schema['pattern'], value):
            errors.append(path + ': invalid format')
    if type(value) is int:
        if value < schema.get('minimum', value):
            errors.append(path + ': below minimum')
        if value > schema.get('maximum', value):
            errors.append(path + ': above maximum')
    if isinstance(value, list):
        if len(value) < schema.get('minItems', 0):
            errors.append(path + ': too few items')
        if len(value) > schema.get('maxItems', len(value)):
            errors.append(path + ': too many items')
        if schema.get('uniqueItems') and len({canonical_bytes(v) for v in value}) != len(value):
            errors.append(path + ': duplicate items')
        for index, item in enumerate(value):
            _check(item, schema['items'], root, f'{path}[{index}]', errors)
    if isinstance(value, dict):
        properties = schema.get('properties', {})
        for key in schema.get('required', []):
            if key not in value:
                errors.append(path + '.' + key + ': required field missing')
        if schema.get('additionalProperties') is False:
            for key in value:
                if key not in properties:
                    errors.append(path + '.' + key + ': unknown field')
        for key, item in value.items():
            if key in properties:
                _check(item, properties[key], root, path + '.' + key, errors)


def validate_structure(receipt: object) -> list[str]:
    errors: list[str] = []
    schema = load_schema()
    if not isinstance(receipt, dict):
        return ['$: receipt must be a JSON object']
    _check(receipt, schema, schema, '$', errors)
    return errors


def _time(value: str) -> dt.datetime:
    return dt.datetime.fromisoformat(value.replace('Z', '+00:00'))


def validate_semantics(receipt: dict) -> list[str]:
    """Cross-field invariants. Assumes validate_structure passed."""
    errors: list[str] = []
    checks = receipt['checks']
    names = [check['name'] for check in checks]
    if len(set(names)) != len(names):
        errors.append('$.checks: duplicate check names')
    latest = None
    for index, check in enumerate(checks):
        where = f'$.checks[{index}]'
        status, exit_code = check['status'], check['exit_code']
        conclusion = check['github_conclusion']
        started, finished = check['started_at'], check['finished_at']
        if (started is None) != (finished is None):
            errors.append(where + ': started_at and finished_at must both be set or both null')
        if started and finished:
            if _time(finished) < _time(started):
                errors.append(where + ': finished_at precedes started_at')
            latest = _time(finished) if latest is None else max(latest, _time(finished))
        if conclusion is not None and GITHUB_CONCLUSION_STATUS[conclusion] != status:
            errors.append(where + f': github_conclusion {conclusion} requires status '
                          + GITHUB_CONCLUSION_STATUS[conclusion])
        if status == 'PASS':
            if exit_code != 0 and not (exit_code is None and conclusion == 'success'):
                errors.append(where + ': PASS requires exit_code 0 (or a GitHub success conclusion)')
            if check['output_sha256'] is None:
                errors.append(where + ': PASS requires output_sha256 evidence')
            if started is None:
                errors.append(where + ': PASS requires started_at and finished_at')
        elif status == 'FAIL':
            if exit_code == 0 or (exit_code is None and conclusion not in ('failure', 'timed_out')):
                errors.append(where + ': FAIL requires a nonzero exit_code (or a GitHub failure conclusion)')
            if started is None:
                errors.append(where + ': FAIL requires started_at and finished_at')
        elif status == 'NOT_RUN':
            if exit_code is not None or check['output_sha256'] is not None or started is not None:
                errors.append(where + ': NOT_RUN cannot carry exit_code, output or timestamps')
            if conclusion is not None:
                errors.append(where + ': NOT_RUN cannot carry a provider conclusion')
        else:
            if exit_code is not None or check['output_sha256'] is not None:
                errors.append(where + ': NOT_VERIFIABLE cannot carry exit_code or output evidence')
    required = receipt['required_checks']
    for name in required:
        if name not in names:
            errors.append(f'$.required_checks: required check "{name}" has no recorded result')
    statuses = {check['status'] for check in checks}
    derived = ('FAIL' if 'FAIL' in statuses
               else 'INCOMPLETE' if statuses & {'NOT_RUN', 'NOT_VERIFIABLE'} else 'PASS')
    if receipt['overall_status'] != derived:
        errors.append(f'$.overall_status: derived status is {derived}')
    generated = _time(receipt['generated_at'])
    if latest is not None and generated < latest:
        errors.append('$.generated_at: precedes the last check finish time')

    claim, merge, accept = receipt['claim'], receipt['merge_evidence'], receipt['acceptance']
    if claim == 'STAGED':
        if merge is not None or accept is not None:
            errors.append('$.claim: STAGED cannot carry merge_evidence or acceptance')
    elif claim == 'MERGED':
        if merge is None:
            errors.append('$.claim: MERGED requires merge_evidence')
        if accept is not None:
            errors.append('$.claim: MERGED cannot carry acceptance (only VERIFIED does)')
    else:
        if merge is None:
            errors.append('$.claim: VERIFIED requires merge_evidence')
        elif merge['ci_conclusion'] != 'success':
            errors.append('$.claim: VERIFIED requires merge_evidence.ci_conclusion success')
        if accept is None:
            errors.append('$.claim: VERIFIED requires human acceptance')
        if receipt['overall_status'] != 'PASS':
            errors.append('$.claim: VERIFIED requires overall_status PASS')
        if not required:
            errors.append('$.required_checks: VERIFIED requires a declared, non-empty required check set')
        if merge is not None:
            for index, check in enumerate(checks):
                if check['started_at'] is not None and _time(check['started_at']) < _time(merge['merged_at']):
                    errors.append(f'$.checks[{index}]: VERIFIED evidence must start at or after merged_at '
                                  '(observed on the merged commit, not the branch)')
        if merge is not None and accept is not None and _time(accept['accepted_at']) < _time(merge['merged_at']):
            errors.append('$.acceptance: accepted_at precedes merged_at')
    if merge is not None:
        if _time(merge['merged_at']) > generated:
            errors.append('$.merge_evidence: merged_at follows generated_at')
        repo = receipt['subject']['repository']
        if not merge['ci_run_url'].startswith('https://github.com/' + repo + '/actions/runs/'):
            errors.append('$.merge_evidence.ci_run_url: run does not belong to the subject repository')
    if accept is not None and _time(accept['accepted_at']) > generated:
        errors.append('$.acceptance: accepted_at follows generated_at')
    return errors


def validate_receipt(receipt: object) -> list[str]:
    """Return every violation found; an empty list means structurally and semantically valid."""
    errors = validate_structure(receipt)
    if errors:
        return errors
    errors = validate_semantics(receipt)
    if receipt['id'] != receipt_id(receipt):
        errors.append('$.id: identity differs from content digest')
    return errors


def _safe_text(value: str) -> str:
    return re.sub(r'[^A-Za-z0-9 _.:/=+-]', '?', value)


def render_block(receipt: dict) -> str:
    """Render the marker-delimited PR-body block (validated first)."""
    errors = validate_receipt(receipt)
    if errors:
        raise ValueError('Invalid receipt: ' + '; '.join(errors[:5]))
    dumped = json.dumps(receipt, sort_keys=True, indent=2, ensure_ascii=True, allow_nan=False)
    if MARKER_FRAGMENT in dumped:
        raise ValueError('Receipt content contains the injection marker')
    longest = max((len(run) for run in re.findall(r'`+', dumped)), default=0)
    fence = '`' * max(3, longest + 1)
    subject = receipt['subject']
    lines = [
        BEGIN_MARKER,
        '### Agent verification receipt',
        '',
        f"Claim: **{receipt['claim']}** | Overall: **{receipt['overall_status']}** | "
        f"Head: `{subject['head_sha'][:12]}` | Agent: {_safe_text(receipt['agent']['name'])}",
        '',
        '| Check | Status | Exit |',
        '| --- | --- | --- |',
    ]
    for check in receipt['checks']:
        exit_code = '-' if check['exit_code'] is None else str(check['exit_code'])
        lines.append(f"| {_safe_text(check['name'])} | {check['status']} | {exit_code} |")
    lines += [
        '',
        '<details><summary>Receipt JSON (' + html.escape(receipt['id'][:40]) + ')</summary>',
        '',
        fence + 'json',
        dumped,
        fence,
        '',
        '</details>',
        '',
        'Structural validation only: this receipt does not authenticate the agent or certify '
        'Verified status. Receipts below `VERIFIED` are Staged evidence.',
        END_MARKER,
    ]
    return '\n'.join(lines)


def _block_span(body: str) -> tuple[int, int] | None:
    begins = [m.start() for m in re.finditer(re.escape(BEGIN_MARKER), body)]
    ends = [m.end() for m in re.finditer(re.escape(END_MARKER), body)]
    if not begins and not ends:
        return None
    if len(begins) != 1 or len(ends) != 1 or ends[0] <= begins[0]:
        raise ValueError('PR body has unbalanced or repeated receipt markers')
    return begins[0], ends[0]


def inject(body: str | None, receipt: dict) -> str:
    """Insert or replace the receipt block, leaving all other body text untouched."""
    body = (body or '').replace('\r\n', '\n')
    block = render_block(receipt)
    span = _block_span(body)
    if span is None:
        result = (body.rstrip('\n') + '\n\n' if body.strip() else '') + block + '\n'
    else:
        result = body[:span[0]] + block + body[span[1]:]
    if len(result) > PR_BODY_LIMIT:
        raise ValueError(f'PR body would exceed {PR_BODY_LIMIT} characters')
    return result


def extract(body: str | None) -> dict | None:
    """Parse and validate the receipt embedded in a PR body, or None when absent."""
    body = (body or '').replace('\r\n', '\n')
    span = _block_span(body)
    if span is None:
        return None
    block = body[span[0]:span[1]]
    match = re.search(r'^(`{3,})json\n(.*?)\n\1$', block, re.S | re.M)
    if not match:
        raise ValueError('Receipt block has no JSON fence')
    receipt = json.loads(match.group(2))
    errors = validate_receipt(receipt)
    if errors:
        raise ValueError('Embedded receipt invalid: ' + '; '.join(errors[:5]))
    if block != render_block(receipt):
        raise ValueError('Embedded receipt block was altered after rendering')
    return receipt


def check_binding(receipt: dict, repository: str, pull_request: int, head_sha: str) -> None:
    """Refuse a receipt that does not describe this exact PR head (stale or foreign evidence)."""
    subject = receipt['subject']
    if subject['repository'].lower() != repository.lower():
        raise ValueError(f"Receipt repository {subject['repository']} differs from {repository}")
    if subject['pull_request'] is not None and subject['pull_request'] != pull_request:
        raise ValueError(f"Receipt pull request {subject['pull_request']} differs from {pull_request}")
    if subject['head_sha'] != head_sha:
        raise ValueError(f"Receipt head_sha {subject['head_sha']} differs from current PR head {head_sha}")


def _pr_fields(pr: object) -> tuple[str, str]:
    if not isinstance(pr, dict) or not isinstance(pr.get('head'), dict) or not isinstance(pr['head'].get('sha'), str):
        raise ValueError('Not a pull request API response')
    return pr.get('body') or '', pr['head']['sha']


def _load_json(path: str) -> object:
    return json.loads(Path(path).read_text(encoding='utf-8'))


def configure_parser(subparsers) -> None:
    parser = subparsers.add_parser('receipt', help='Agent verification receipts')
    commands = parser.add_subparsers(dest='receipt_command', required=True)
    command = commands.add_parser('validate', help='Validate receipt JSON files')
    command.add_argument('files', nargs='+')
    command = commands.add_parser('seal', help='Compute schema and id for an unsealed receipt')
    command.add_argument('--input', required=True)
    command.add_argument('--output', required=True)
    command = commands.add_parser('render', help='Print the PR-body block for a receipt')
    command.add_argument('--receipt', required=True)
    command = commands.add_parser('inject', help='Insert or replace the receipt block in a PR body file')
    command.add_argument('--receipt', required=True)
    source = command.add_mutually_exclusive_group(required=True)
    source.add_argument('--body-file')
    source.add_argument('--pr-json', help='GET /repos/{r}/pulls/{n} response; also checks the receipt binds to this PR head')
    command.add_argument('--repository', help='owner/name (required with --pr-json)')
    command.add_argument('--pull-request', type=int, help='PR number (required with --pr-json)')
    command.add_argument('--output', required=True)
    command = commands.add_parser('extract', help='Validate the receipt embedded in a PR body file')
    source = command.add_mutually_exclusive_group(required=True)
    source.add_argument('--body-file')
    source.add_argument('--pr-json')
    command.add_argument('--expect-id', help='Fail unless the embedded receipt has this id')
    command.add_argument('--repository', help='With --pr-json: also require the receipt to bind to this repository and head')
    command.add_argument('--pull-request', type=int)


def run(args) -> int:
    try:
        if args.receipt_command == 'validate':
            failed = 0
            for name in args.files:
                try:
                    errors = validate_receipt(_load_json(name))
                except (OSError, ValueError) as exc:
                    errors = ['$: ' + str(exc)]
                for error in errors:
                    print(f'{name}: {error}', file=sys.stderr)
                failed += bool(errors)
                if not errors:
                    print(f'{name}: valid')
            return 2 if failed else 0
        if args.receipt_command == 'seal':
            sealed = seal(_load_json(args.input))
            errors = validate_receipt(sealed)
            for error in errors:
                print(f'{args.input}: {error}', file=sys.stderr)
            if errors:
                return 2
            Path(args.output).write_text(json.dumps(sealed, indent=2, sort_keys=True) + '\n', encoding='utf-8')
            return 0
        if args.receipt_command == 'render':
            print(render_block(_load_json(args.receipt)))
            return 0
        if args.receipt_command == 'inject':
            receipt = _load_json(args.receipt)
            errors = validate_receipt(receipt)
            if errors:
                for error in errors:
                    print(f'{args.receipt}: {error}', file=sys.stderr)
                return 2
            if args.pr_json:
                if not args.repository or not args.pull_request:
                    raise ValueError('--pr-json requires --repository and --pull-request')
                body, head = _pr_fields(_load_json(args.pr_json))
                check_binding(receipt, args.repository, args.pull_request, head)
            else:
                body = Path(args.body_file).read_text(encoding='utf-8')
            Path(args.output).write_text(inject(body, receipt), encoding='utf-8')
            return 0
        if args.receipt_command == 'extract':
            head = None
            if args.pr_json:
                body, head = _pr_fields(_load_json(args.pr_json))
            else:
                body = Path(args.body_file).read_text(encoding='utf-8')
            receipt = extract(body)
            if receipt is not None and head is not None and args.repository and args.pull_request:
                check_binding(receipt, args.repository, args.pull_request, head)
            if receipt is None:
                print('no receipt block', file=sys.stderr)
                return 2
            if args.expect_id and receipt['id'] != args.expect_id:
                print('embedded receipt id differs from the expected id', file=sys.stderr)
                return 2
            print(receipt['id'])
            return 0
    except (OSError, ValueError, KeyError) as exc:
        print('receipt: ' + str(exc), file=sys.stderr)
        return 2
    return 2


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest='command', required=True)
    configure_parser(sub)
    arguments = list(sys.argv[1:] if argv is None else argv)
    return run(parser.parse_args(['receipt'] + arguments))


if __name__ == '__main__':
    sys.exit(main())
