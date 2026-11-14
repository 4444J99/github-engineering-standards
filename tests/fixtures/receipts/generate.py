"""Regenerate receipt fixtures: `python tests/fixtures/receipts/generate.py`.

Valid fixtures are sealed receipts. Invalid fixtures mutate a valid one and are
re-sealed so each fails only the invariant named in expected-errors.json (except
identity cases, which are deliberately left unsealed).
"""
import copy
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2]))
from ges.receipts import seal  # noqa: E402

SHA_A = 'a' * 40
SHA_B = 'b' * 40
SHA_C = 'c' * 40
DIGEST = 'd' * 64
RUN = 'https://github.com/4444J99/guide-github-standard/actions/runs/123456789'


def check(name, command, status='PASS', exit_code=0, **extra):
    base = {
        'name': name, 'command': command, 'status': status, 'exit_code': exit_code,
        'github_conclusion': None, 'started_at': '2026-11-14T10:00:00Z',
        'finished_at': '2026-11-14T10:00:30Z', 'output_sha256': DIGEST,
        'observation': 'observed locally',
    }
    base.update(extra)
    return base


def staged():
    return {
        'generated_at': '2026-11-14T10:05:00Z',
        'agent': {'name': 'claude-code', 'kind': 'claude', 'session_ref': 'session-0001'},
        'subject': {'repository': '4444J99/guide-github-standard', 'pull_request': 521,
                    'head_sha': SHA_A, 'base_ref': 'main', 'base_sha': SHA_B},
        'claim': 'STAGED',
        'required_checks': ['unit tests', 'ges validate'],
        'checks': [
            check('unit tests', 'python -m unittest discover -s tests -v'),
            check('ges validate', 'python -m ges validate'),
        ],
        'overall_status': 'PASS', 'merge_evidence': None, 'acceptance': None,
        'limitations': ['Branch-only evidence; not merged to main.'],
    }


def merged():
    receipt = staged()
    for item in receipt['checks']:
        item['started_at'], item['finished_at'] = '2026-11-14T10:31:00Z', '2026-11-14T10:32:00Z'

    receipt['claim'] = 'MERGED'
    receipt['generated_at'] = '2026-11-14T11:00:00Z'
    receipt['merge_evidence'] = {'main_sha': SHA_C, 'merged_at': '2026-11-14T10:30:00Z',
                                 'ci_run_url': RUN, 'ci_conclusion': 'success'}
    return receipt


def verified():
    receipt = merged()
    receipt['claim'] = 'VERIFIED'
    receipt['generated_at'] = '2026-11-14T12:00:00Z'
    receipt['acceptance'] = {'accepted_by': 'designated-owner', 'accepted_at': '2026-11-14T11:30:00Z',
                             'reference': 'https://github.com/4444J99/guide-github-standard/pull/521#issuecomment-1'}
    receipt['limitations'] = []
    return receipt


def incomplete():
    receipt = staged()
    receipt['checks'].append(check('remote CI', 'gh pr checks 521', status='NOT_RUN', exit_code=None,
                                   started_at=None, finished_at=None, output_sha256=None,
                                   observation='CI had not started'))
    receipt['checks'].append(check('security review', 'human review', status='NOT_VERIFIABLE', exit_code=None,
                                   output_sha256=None, observation='requires a human reviewer'))
    receipt['overall_status'] = 'INCOMPLETE'
    return receipt


def failing():
    receipt = staged()
    receipt['checks'][1] = check('ges validate', 'python -m ges validate', status='FAIL', exit_code=2,
                                 observation='validation errors reported')
    receipt['overall_status'] = 'FAIL'
    return receipt


def github_checks():
    receipt = staged()
    receipt['checks'] = [
        check('validate (3.13)', 'GitHub check run: validate (3.13)', exit_code=None, github_conclusion='success'),
        check('lint', 'GitHub check run: lint', status='NOT_VERIFIABLE', exit_code=None,
              github_conclusion='skipped', output_sha256=None, observation='provider skipped the job'),
    ]
    receipt['required_checks'] = ['validate (3.13)']
    receipt['overall_status'] = 'INCOMPLETE'
    return receipt


def mutate(base, fn, reseal=True):
    receipt = copy.deepcopy(seal(base()))
    fn(receipt)
    return seal(receipt) if reseal else receipt


def set_path(receipt, dotted, value):
    node = receipt
    parts = dotted.split('.')
    for part in parts[:-1]:
        node = node[int(part)] if isinstance(node, list) else node[part]
    last = parts[-1]
    if isinstance(node, list):
        node[int(last)] = value
    else:
        node[last] = value


def cases():
    out = {}
    def add(name, base, dotted, value, expect, reseal=True):
        out[name] = (mutate(base, lambda r: set_path(r, dotted, value), reseal), expect)
    add('short-sha', staged, 'subject.head_sha', 'abc1234', 'head_sha')
    add('unknown-claim', staged, 'claim', 'DONE', '$.claim')
    add('bad-timestamp', staged, 'generated_at', '2026-11-14 10:05:00', 'generated_at')
    add('pass-with-nonzero-exit', staged, 'checks.0.exit_code', 1, 'PASS requires exit_code 0')
    add('pass-without-output-digest', staged, 'checks.0.output_sha256', None, 'PASS requires output_sha256')
    add('fail-with-zero-exit', failing, 'checks.1.exit_code', 0, 'FAIL requires a nonzero exit_code')
    add('overall-pass-despite-fail', failing, 'overall_status', 'PASS', 'derived status is FAIL')
    add('overall-pass-despite-not-run', incomplete, 'overall_status', 'PASS', 'derived status is INCOMPLETE')
    add('not-run-with-exit-code', incomplete, 'checks.2.exit_code', 0, 'NOT_RUN cannot carry')
    add('not-verifiable-with-output', incomplete, 'checks.3.output_sha256', DIGEST, 'NOT_VERIFIABLE cannot carry')
    add('skipped-conclusion-as-pass', github_checks, 'checks.1.status', 'PASS', 'requires status NOT_VERIFIABLE')
    add('duplicate-check-names', staged, 'checks.1.name', 'unit tests', 'duplicate check names')
    add('finish-before-start', staged, 'checks.0.finished_at', '2026-11-14T09:00:00Z', 'precedes started_at')
    add('generated-before-finish', staged, 'generated_at', '2026-11-14T10:00:10Z', 'precedes the last check')
    add('staged-with-merge-evidence', merged, 'claim', 'STAGED', 'STAGED cannot carry')
    add('merged-without-evidence', merged, 'merge_evidence', None, 'MERGED requires merge_evidence')
    add('merged-with-acceptance', verified, 'claim', 'MERGED', 'MERGED cannot carry acceptance')
    add('verified-without-acceptance', verified, 'acceptance', None, 'VERIFIED requires human acceptance')
    add('verified-with-failing-ci', verified, 'merge_evidence.ci_conclusion', 'failure', 'ci_conclusion success')
    add('verified-with-incomplete-checks', verified, 'overall_status', 'INCOMPLETE', 'derived status is PASS')
    add('verified-empty-required-checks', verified, 'required_checks', [], 'non-empty required check set')
    add('required-check-missing', staged, 'required_checks', ['unit tests', 'ges compile'], 'has no recorded result')
    add('verified-evidence-predates-merge', verified, 'checks.0.started_at', '2026-11-14T10:00:00Z', 'merged commit, not the branch')
    add('acceptance-before-merge', verified, 'acceptance.accepted_at', '2026-11-14T10:10:00Z', 'precedes merged_at')
    add('ci-run-other-repository', merged, 'merge_evidence.ci_run_url',
        'https://github.com/someone/else/actions/runs/1', 'does not belong to the subject repository')
    add('unknown-field', staged, 'extra', 'x', 'unknown field')
    out['missing-field'] = (seal({k: v for k, v in staged().items() if k != 'limitations'}), 'limitations')
    add('tampered-content', staged, 'agent.name', 'someone-else', 'identity differs', reseal=False)
    stale = seal(staged())
    stale['claim'] = 'MERGED'
    out['tampered-claim-keeps-old-id'] = (stale, 'MERGED requires merge_evidence')
    return out


def write(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n', encoding='utf-8')


def main():
    valid = {'staged-pass': staged, 'merged': merged, 'verified': verified, 'incomplete': incomplete,
             'staged-fail': failing, 'github-checks': github_checks}
    for name, build in valid.items():
        write(HERE / 'valid' / (name + '.json'), seal(build()))
    expected = {}
    for name, (receipt, expect) in cases().items():
        write(HERE / 'invalid' / (name + '.json'), receipt)
        expected[name] = expect
    write(HERE / 'expected-errors.json', expected)


if __name__ == '__main__':
    main()
