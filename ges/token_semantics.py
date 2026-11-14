"""GITHUB_TOKEN permission and pull-request event semantics from pinned GitHub Docs.

Two halves that must agree:

* an executable model (`resolve_token_permissions`, `pull_request_event_context`,
  `workflow_run_for_token_event`) whose every rule has an id (`T*` for token,
  `E*` for event semantics);
* a source-bound ledger (`evidence/semantics/github-token-permissions/`) of
  `ges.semantic-occurrence.v1` / `ges.semantic-proposition.v1` records, each bound to an
  exact line span of a file at the pinned `github/docs` commit, naming the rules it
  supports.

`build_ledger` compiles authored annotations against the pinned source bytes and fails
on any drift (content digest, anchor text, line range). `check_conformance` proves the
model reproduces every case in `conformance.json`, that every rule has a case and a
supporting source span, and that no case cites an unknown rule.

Everything is PROPOSED: the records carry no reviewer. Structural validity and model
conformance do not certify that the documentation was interpreted correctly, and the
documentation is not a specification of GitHub's server behaviour.
Standard library only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

from .semantics import canonical_bytes, stable_id, validate_record

ROOT = Path(__file__).resolve().parents[1]
LEDGER_DIR = ROOT / 'evidence' / 'semantics' / 'github-token-permissions'
ANNOTATIONS = LEDGER_DIR / 'annotations.json'
CONFORMANCE = LEDGER_DIR / 'conformance.json'
OCCURRENCES = LEDGER_DIR / 'occurrences.jsonl'
PROPOSITIONS = LEDGER_DIR / 'propositions.jsonl'
ACCOUNTING = LEDGER_DIR / 'accounting.json'
ANNOTATIONS_SCHEMA = 'ges.token-semantics-annotations.v1'
CONFORMANCE_SCHEMA = 'ges.token-semantics-conformance.v1'

LEVELS = ('none', 'read', 'write')

# Scope -> (levels the docs allow, version flag that gates it or None).
# Source: data/reusables/actions/github-token-available-permissions.md lines 3-22 and
# github-token-scope-descriptions.md. `id-token` allows write|none and only on fpt/ghec;
# `vulnerability-alerts` allows read|none. Flags are the docs' own `ifversion` names.
SCOPES: dict[str, tuple[tuple[str, ...], str | None]] = {
    'actions': (('none', 'read', 'write'), None),
    'artifact-metadata': (('none', 'read', 'write'), 'artifact-metadata'),
    'attestations': (('none', 'read', 'write'), 'artifact-attestations'),
    'checks': (('none', 'read', 'write'), None),
    'code-quality': (('none', 'read', 'write'), 'code-quality'),
    'contents': (('none', 'read', 'write'), None),
    'deployments': (('none', 'read', 'write'), None),
    'discussions': (('none', 'read', 'write'), None),
    'id-token': (('none', 'write'), 'fpt-or-ghec'),
    'issues': (('none', 'read', 'write'), None),
    'packages': (('none', 'read', 'write'), None),
    'pages': (('none', 'read', 'write'), None),
    'pull-requests': (('none', 'read', 'write'), None),
    'security-events': (('none', 'read', 'write'), None),
    'statuses': (('none', 'read', 'write'), None),
    'vulnerability-alerts': (('none', 'read'), 'vulnerability-alerts-permission'),
}

# Rule T8: events the docs call "pull request events" (event headings in
# events-that-trigger-workflows.md other than the deprecated pull_request_comment alias
# and pull_request_target, which the calculation exempts by name).
FORK_DOWNGRADED_EVENTS = frozenset({'pull_request', 'pull_request_review',
                                    'pull_request_review_comment'})
PULL_REQUEST_TARGET = 'pull_request_target'
DEFAULT_PULL_REQUEST_ACTIVITY_TYPES = ('opened', 'synchronize', 'reopened')


def available_scopes(flags: frozenset[str] = frozenset()) -> dict[str, tuple[str, ...]]:
    """Scopes (and their allowed levels) available given the docs' version flags."""
    return {name: levels for name, (levels, flag) in SCOPES.items()
            if flag is None or flag in flags}


def _grant(allowed: tuple[str, ...], requested: str) -> str:
    """Highest allowed level not above `requested` (read-all on a write|none scope is none)."""
    best = 'none'
    for level in allowed:
        if LEVELS.index(level) <= LEVELS.index(requested) and LEVELS.index(level) >= LEVELS.index(best):
            best = level
    return best


def apply_permissions_key(spec: object, flags: frozenset[str] = frozenset()) -> dict[str, str]:
    """Rules T4-T7: the access map a `permissions` value denotes, independent of defaults.

    `spec` is a mapping scope -> level, `'read-all'`, `'write-all'` or `{}`.
    Raises ValueError for unknown scopes or levels the docs do not allow.
    """
    scopes = available_scopes(flags)
    if spec == 'read-all':
        return {name: _grant(levels, 'read') for name, levels in scopes.items()}
    if spec == 'write-all':
        return {name: _grant(levels, 'write') for name, levels in scopes.items()}
    if not isinstance(spec, dict):
        raise ValueError('permissions must be a mapping, read-all or write-all')
    result = {name: 'none' for name in scopes}
    for name, level in spec.items():
        if name not in scopes:
            raise ValueError(f'unknown or unavailable permission scope: {name}')
        if level not in scopes[name]:
            raise ValueError(f'scope {name} cannot be set to {level!r} (allowed: {"|".join(scopes[name])})')
        result[name] = level
    return result


def resolve_token_permissions(*, default: dict[str, str], workflow: object = None, job: object = None,
                              event: str, from_fork: bool, send_write_tokens: bool = False,
                              flags: frozenset[str] = frozenset()) -> dict[str, str]:
    """Rule T8: default -> workflow `permissions` -> job `permissions` -> fork adjustment.

    `default` is the enterprise/organization/repository default access map, supplied by the
    caller: the pinned pages do not enumerate the restricted/permissive presets.
    `workflow`/`job` are `permissions` values or None when the key is absent.
    """
    scopes = available_scopes(flags)
    for name, level in default.items():
        if name not in scopes or level not in scopes[name]:
            raise ValueError(f'invalid default permission {name}: {level}')
    current = {name: default.get(name, 'none') for name in scopes}
    if workflow is not None:
        current = apply_permissions_key(workflow, flags)
    if job is not None:
        current = apply_permissions_key(job, flags)
    if from_fork and event in FORK_DOWNGRADED_EVENTS and not send_write_tokens:
        current = {name: ('read' if level == 'write' and 'read' in scopes[name] else
                          'none' if level == 'write' else level)
                   for name, level in current.items()}
    return current


def allows(permissions: dict[str, str], scope: str, needed: str) -> bool:
    """Rule T4: `write` includes `read`."""
    return LEVELS.index(permissions.get(scope, 'none')) >= LEVELS.index(needed)


def pull_request_event_context(event: str, *, ghes_before_3_20: bool = False) -> dict[str, object]:
    """Rules E1, E2, E4: what GITHUB_SHA and GITHUB_REF denote for the two PR triggers."""
    if event == 'pull_request':
        return {'sha': 'last merge commit on the GITHUB_REF branch',
                'ref': 'refs/pull/PULL_REQUEST_NUMBER/merge',
                'runs_against': 'merge commit of the pull request',
                'default_activity_types': DEFAULT_PULL_REQUEST_ACTIVITY_TYPES,
                'skipped_on_merge_conflict': True}
    if event == PULL_REQUEST_TARGET:
        return {'sha': 'last commit on the pull request base branch' if ghes_before_3_20
                else 'last commit on default branch',
                'ref': 'pull request base branch' if ghes_before_3_20 else 'default branch',
                'runs_against': 'base of the pull request' if ghes_before_3_20
                else 'default branch of the base repository',
                'default_activity_types': DEFAULT_PULL_REQUEST_ACTIVITY_TYPES,
                'skipped_on_merge_conflict': False}
    raise ValueError(f'not a modelled pull request trigger: {event}')


def workflow_run_for_token_event(event: str, activity_type: str | None = None, *,
                                 approval_flag: bool = True) -> str:
    """Rule E3: does an event caused by the repository GITHUB_TOKEN create a workflow run?

    Returns RUN, APPROVAL_REQUIRED or NO_RUN. `approval_flag` is the docs'
    `actions-github-token-pull-request-approval` version flag.
    """
    if event in ('workflow_dispatch', 'repository_dispatch'):
        return 'RUN'
    if (approval_flag and event == 'pull_request'
            and activity_type in DEFAULT_PULL_REQUEST_ACTIVITY_TYPES):
        return 'APPROVAL_REQUIRED'
    return 'NO_RUN'


def token_is_valid(runner: str, elapsed_hours: float, *, job_finished: bool) -> bool:
    """Rule T3: valid until the job finishes or the runner type's effective maximum lifetime.

    `github-hosted`: 6 hours (maximum job execution time). `self-hosted`: jobs may run
    5 days but an installation token can be refreshed for at most 24 hours.
    """
    limits = {'github-hosted': 6.0, 'self-hosted': 24.0}
    if runner not in limits:
        raise ValueError(f'unknown runner type: {runner}')
    return not job_finished and elapsed_hours < limits[runner]


def secrets_reach_runner(name: str, *, from_fork: bool) -> bool:
    """Rule T13: from a forked repository only GITHUB_TOKEN reaches the runner."""
    return name == 'GITHUB_TOKEN' or not from_fork


# --- source-bound ledger ---------------------------------------------------------------

def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding='utf-8'))


def _annotations() -> dict:
    data = _load(ANNOTATIONS)
    _require(data.get('schema') == ANNOTATIONS_SCHEMA, 'Unsupported annotations schema')
    return data


def build_ledger(annotations: dict, sources: Path) -> dict[str, bytes]:
    """Compile occurrences, propositions and accounting from annotations and pinned bytes."""
    repository, commit = annotations['repository'], annotations['commit']
    occurrences, propositions = [], []
    modelled: set[str] = set()
    contents: dict[str, tuple[str, list[bytes]]] = {}
    for entry in annotations['entries']:
        path = entry['path']
        _require(not path.startswith('/') and '..' not in path.split('/') and '\\' not in path,
                 'Unsafe source path')
        if path not in contents:
            raw = (sources / path).read_bytes()
            contents[path] = (sha(raw), raw.splitlines(keepends=True))
        content_digest, lines = contents[path]
        start, end = entry['start_line'], entry['end_line']
        _require(1 <= start <= end <= len(lines), f'{path}: span {start}-{end} outside file')
        span = b''.join(lines[start - 1:end])
        _require(entry['expect'] in span.decode('utf-8'),
                 f'{path}:{start}-{end}: anchor text not found in span (source drift)')
        _require(entry['content_sha256'] == content_digest,
                 f'{path}: pinned content digest differs from annotation')
        occurrence = {
            'schema': 'ges.semantic-occurrence.v1',
            'source': {'repository': repository, 'commit': commit, 'path': path,
                       'content_sha256': content_digest, 'start_line': start, 'end_line': end,
                       'span_sha256': sha(span)},
            'heading_ancestry': entry['heading_ancestry'],
            'include_chain': entry['include_chain'],
            'page_applications': [],
            'conditions': entry['conditions'],
            'products': ['GitHub Actions'],
            'versions': entry['versions'],
            'authority_class': 'PLATFORM',
            'semantic_kind': entry['semantic_kind'],
            'semantic_ast': entry['propositions'][0]['semantic_ast'],
            'formalization': ' '.join(p['formalization'] for p in entry['propositions']),
            'extraction': {'method': 'authored-span-annotations', 'version': 'token-semantics.v1'},
            'review': {'status': 'PROPOSED', 'reviewer': None, 'evidence_reference': None},
        }
        occurrence['id'] = stable_id(occurrence)
        validate_record(occurrence)
        occurrences.append(occurrence)
        for item in entry['propositions']:
            proposition = {
                'schema': 'ges.semantic-proposition.v1',
                'semantic_ast': item['semantic_ast'],
                'occurrence_ids': [occurrence['id']],
                'preserved_differences': item.get('preserved_differences', []),
                'authority_order': ['PLATFORM'],
                'applicability': entry['conditions'] + entry['versions'],
                'ambiguities': item.get('ambiguities', []),
                'primary_review': {'status': 'PROPOSED', 'reviewer': None, 'evidence_reference': None},
                'omission_review': {'status': 'PROPOSED', 'reviewer': None, 'evidence_reference': None},
            }
            proposition['id'] = stable_id(proposition)
            validate_record(proposition)
            propositions.append(proposition)
            modelled.update(item.get('rules', []))
    _require(len({p['id'] for p in propositions}) == len(propositions),
             'Two annotated statements have an identical semantic AST')
    accounting = {
        'schema': 'ges.token-semantics-accounting.v1',
        'repository': repository,
        'commit': commit,
        'files': len(contents),
        'occurrences': len(occurrences),
        'propositions': len(propositions),
        'propositions_with_model_rule': sum(
            1 for entry in annotations['entries'] for p in entry['propositions'] if p.get('rules')),
        'propositions_preserved_without_model_rule': sum(
            1 for entry in annotations['entries'] for p in entry['propositions'] if not p.get('rules')),
        'rules_supported': sorted(modelled),
        'review_status': 'PROPOSED',
        'semantic_truth_certified': False,
        'policy_adopted': False,
        'scope': ('Selected GITHUB_TOKEN permission and pull-request trigger passages only; '
                  'not a review of the GitHub Docs corpus.'),
    }

    def jsonl(records: list[dict]) -> bytes:
        return b''.join(canonical_bytes(r) + b'\n' for r in records)

    return {'occurrences.jsonl': jsonl(occurrences), 'propositions.jsonl': jsonl(propositions),
            'accounting.json': json.dumps(accounting, indent=2, sort_keys=True).encode('utf-8') + b'\n'}


def check_conformance(annotations: dict, conformance: dict) -> list[str]:
    """Run every conformance case through the model; return all problems found."""
    problems: list[str] = []
    supported = {rule for entry in annotations['entries']
                 for p in entry['propositions'] for rule in p.get('rules', [])}
    if conformance.get('schema') != CONFORMANCE_SCHEMA:
        return ['conformance: unsupported schema']
    covered: set[str] = set()
    for case in conformance['cases']:
        name = case['id']
        rules = set(case['rules'])
        covered |= rules
        for rule in sorted(rules - supported):
            problems.append(f'{name}: cites rule {rule} that no annotated source statement supports')
        actual = run_case(case)
        if actual != case['expect']:
            problems.append(f'{name}: expected {case["expect"]!r}, model produced {actual!r}')
    for rule in sorted(supported - covered):
        problems.append(f'rule {rule} is supported by source statements but has no conformance case')
    return problems


def run_case(case: dict) -> dict:
    """Run one conformance case; a ValueError from the model is the observable result."""
    try:
        return _run_case(case)
    except ValueError as exc:
        return {'error': str(exc)}


def _run_case(case: dict) -> dict:
    kind, given = case['kind'], case['given']
    flags = frozenset(given.get('flags', []))
    if kind == 'permissions-key':
        return {'permissions': apply_permissions_key(given['spec'], flags)}
    if kind == 'resolve':
        return {'permissions': resolve_token_permissions(
            default=given['default'], workflow=given.get('workflow'), job=given.get('job'),
            event=given['event'], from_fork=given['from_fork'],
            send_write_tokens=given.get('send_write_tokens', False), flags=flags)}
    if kind == 'can':
        permissions = resolve_token_permissions(
            default=given['default'], workflow=given.get('workflow'), job=given.get('job'),
            event=given['event'], from_fork=given['from_fork'],
            send_write_tokens=given.get('send_write_tokens', False), flags=flags)
        return {'allowed': allows(permissions, given['scope'], given['needed'])}
    if kind == 'event-context':
        context = pull_request_event_context(given['event'], ghes_before_3_20=given.get('ghes_before_3_20', False))
        return {'context': {k: list(v) if isinstance(v, tuple) else v for k, v in context.items()}}
    if kind == 'token-event':
        return {'result': workflow_run_for_token_event(
            given['event'], given.get('activity_type'), approval_flag=given.get('approval_flag', True))}
    if kind == 'token-valid':
        return {'valid': token_is_valid(given['runner'], given['elapsed_hours'], job_finished=given['job_finished'])}
    if kind == 'secret':
        return {'reaches_runner': secrets_reach_runner(given['name'], from_fork=given['from_fork'])}
    raise ValueError(f'unknown case kind {kind}')


def verify_sources(sources: Path) -> list[str]:
    """Rebuild the ledger from pinned source bytes and compare with the committed files."""
    problems = []
    try:
        built = build_ledger(_annotations(), sources)
    except (OSError, ValueError, KeyError) as exc:
        return [str(exc)]
    for name, raw in built.items():
        if (LEDGER_DIR / name).read_bytes() != raw:
            problems.append(f'{name}: differs from a rebuild against the pinned sources')
    return problems


def configure_parser(subparsers) -> None:
    parser = subparsers.add_parser('token-semantics', help=__doc__.splitlines()[0])
    commands = parser.add_subparsers(dest='token_command', required=True)
    command = commands.add_parser('build', help='Compile the ledger from pinned github/docs files')
    command.add_argument('--sources', type=Path, required=True,
                         help='Directory laid out like the github/docs checkout at the pinned commit')
    command.add_argument('--output', type=Path, default=LEDGER_DIR)
    command = commands.add_parser('verify', help='Check the committed ledger against pinned sources')
    command.add_argument('--sources', type=Path, required=True)
    commands.add_parser('conformance', help='Check the executable model against conformance cases')
    commands.add_parser('validate', help='Validate committed record structure and identity')


def run(args) -> int:
    try:
        if args.token_command == 'build':
            built = build_ledger(_annotations(), args.sources)
            args.output.mkdir(parents=True, exist_ok=True)
            for name, raw in built.items():
                (args.output / name).write_bytes(raw)
            print(json.dumps({'written': sorted(built), 'review_status': 'PROPOSED'}))
            return 0
        if args.token_command == 'verify':
            problems = verify_sources(args.sources)
        elif args.token_command == 'conformance':
            problems = check_conformance(_annotations(), _load(CONFORMANCE))
        else:
            problems = []
            for name in ('occurrences.jsonl', 'propositions.jsonl'):
                for number, line in enumerate((LEDGER_DIR / name).read_text(encoding='utf-8').splitlines(), 1):
                    try:
                        validate_record(json.loads(line))
                    except (ValueError, KeyError) as exc:
                        problems.append(f'{name}:{number}: {exc}')
        for problem in problems:
            print(problem, file=sys.stderr)
        if not problems:
            print(json.dumps({'ok': True, 'command': args.token_command,
                              'semantic_truth_certified': False}))
        return 2 if problems else 0
    except (OSError, ValueError, KeyError) as exc:
        print('token-semantics: ' + str(exc), file=sys.stderr)
        return 2


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest='command', required=True)
    configure_parser(sub)
    return run(parser.parse_args(sys.argv[1:] if argv is None else argv))


if __name__ == '__main__':
    sys.exit(main())
