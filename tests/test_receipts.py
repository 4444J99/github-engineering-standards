import copy
import json
import os
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from ges import receipts  # noqa: E402

FX = ROOT / 'tests' / 'fixtures' / 'receipts'
ACTION = ROOT / '.github' / 'actions' / 'inject-agent-receipt' / 'action.yml'


def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


class SchemaContract(unittest.TestCase):
    def test_schema_uses_only_keywords_the_validator_enforces(self):
        def walk(node, path='$'):
            if isinstance(node, dict):
                for key, value in node.items():
                    if key in ('properties', '$defs'):
                        for name, sub in value.items():
                            walk(sub, f'{path}.{key}.{name}')
                    elif key in ('items',):
                        walk(value, path + '.items')
                    elif key == 'anyOf':
                        for index, sub in enumerate(value):
                            walk(sub, f'{path}.anyOf[{index}]')
                    else:
                        self.assertIn(key, receipts.SUPPORTED_KEYWORDS, f'{path}: unenforced keyword {key}')
        walk(receipts.load_schema())

    def test_every_object_schema_is_closed_and_requires_all_properties(self):
        def walk(node, path='$'):
            if isinstance(node, dict):
                if node.get('type') == 'object':
                    self.assertIs(node.get('additionalProperties'), False, path)
                    self.assertEqual(set(node['required']), set(node['properties']), path)
                for key, value in node.items():
                    walk(value, f'{path}.{key}')
            elif isinstance(node, list):
                for index, value in enumerate(node):
                    walk(value, f'{path}[{index}]')
        walk(receipts.load_schema())

    def test_conclusion_mapping_covers_the_schema_enum(self):
        schema = receipts.load_schema()
        self.assertEqual(set(schema['$defs']['githubConclusion']['enum']), set(receipts.GITHUB_CONCLUSION_STATUS))
        self.assertEqual([k for k, v in receipts.GITHUB_CONCLUSION_STATUS.items() if v == 'PASS'], ['success'])


class Fixtures(unittest.TestCase):
    def test_valid_fixtures_validate(self):
        paths = sorted((FX / 'valid').glob('*.json'))
        self.assertGreaterEqual(len(paths), 6)
        for path in paths:
            self.assertEqual(receipts.validate_receipt(load(path)), [], path.name)

    def test_each_invalid_fixture_fails_for_its_named_reason(self):
        expected = load(FX / 'expected-errors.json')
        paths = sorted((FX / 'invalid').glob('*.json'))
        self.assertEqual({p.stem for p in paths}, set(expected))
        for path in paths:
            errors = receipts.validate_receipt(load(path))
            self.assertTrue(any(expected[path.stem] in error for error in errors), (path.name, errors))

    def test_fixtures_match_generator(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location('receipt_fixture_generator', FX / 'generate.py')
        generator = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(generator)
        for name, build in {'staged-pass': generator.staged, 'merged': generator.merged,
                            'verified': generator.verified, 'incomplete': generator.incomplete,
                            'staged-fail': generator.failing, 'github-checks': generator.github_checks}.items():
            self.assertEqual(load(FX / 'valid' / (name + '.json')), receipts.seal(build()), name)
        for name, (receipt, expect) in generator.cases().items():
            self.assertEqual(load(FX / 'invalid' / (name + '.json')), receipt, name)
            self.assertEqual(load(FX / 'expected-errors.json')[name], expect, name)

    def test_non_object_and_garbage_inputs(self):
        for value in ([], 'x', 1, None):
            self.assertTrue(receipts.validate_receipt(value))


class Semantics(unittest.TestCase):
    def setUp(self):
        self.verified = load(FX / 'valid' / 'verified.json')

    def test_branch_pass_is_never_verified_by_construction(self):
        staged = load(FX / 'valid' / 'staged-pass.json')
        staged['claim'] = 'VERIFIED'
        self.assertTrue(receipts.validate_receipt(receipts.seal(staged)))

    def test_every_non_success_conclusion_is_not_green(self):
        for conclusion, status in receipts.GITHUB_CONCLUSION_STATUS.items():
            receipt = load(FX / 'valid' / 'github-checks.json')
            check = receipt['checks'][0]
            check['github_conclusion'] = conclusion
            check['status'] = status
            check['exit_code'] = None
            if status != 'PASS':
                check['output_sha256'] = None
            receipt['overall_status'] = 'PASS' if status == 'PASS' and receipt['checks'][1]['status'] == 'PASS' else (
                'FAIL' if status == 'FAIL' else 'INCOMPLETE')
            self.assertEqual(receipts.validate_receipt(receipts.seal(receipt)), [], conclusion)
            if status != 'PASS':
                receipt['checks'][0]['status'] = 'PASS'
                self.assertTrue(receipts.validate_receipt(receipts.seal(receipt)), conclusion)

    def test_identity_ignores_key_order_and_changes_with_content(self):
        reordered = dict(reversed(list(self.verified.items())))
        self.assertEqual(receipts.receipt_id(reordered), self.verified['id'])
        changed = copy.deepcopy(self.verified)
        changed['limitations'] = ['changed']
        self.assertNotEqual(receipts.receipt_id(changed), self.verified['id'])

    def test_booleans_are_not_integers(self):
        receipt = copy.deepcopy(self.verified)
        receipt['subject']['pull_request'] = True
        self.assertTrue(receipts.validate_structure(receipt))


class Injection(unittest.TestCase):
    def setUp(self):
        self.receipt = load(FX / 'valid' / 'staged-pass.json')

    def test_inject_appends_then_replaces_idempotently(self):
        body = 'Intent\n\n## Notes\nkeep this'
        once = receipts.inject(body, self.receipt)
        self.assertIn('keep this', once)
        self.assertEqual(once.count(receipts.BEGIN_MARKER), 1)
        self.assertEqual(receipts.inject(once, self.receipt), once)
        newer = receipts.seal({**self.receipt, 'limitations': ['updated']})
        twice = receipts.inject(once, newer)
        self.assertEqual(twice.count(receipts.BEGIN_MARKER), 1)
        self.assertEqual(receipts.extract(twice)['id'], newer['id'])
        self.assertTrue(twice.startswith('Intent\n\n## Notes\nkeep this'))

    def test_empty_and_missing_bodies(self):
        for body in (None, '', '\n\n'):
            self.assertEqual(receipts.extract(receipts.inject(body, self.receipt))['id'], self.receipt['id'])

    def test_crlf_bodies_are_normalised(self):
        self.assertEqual(receipts.extract(receipts.inject('a\r\nb', self.receipt))['id'], self.receipt['id'])

    def test_invalid_receipt_is_never_injected(self):
        bad = load(FX / 'invalid' / 'tampered-content.json')
        with self.assertRaises(ValueError):
            receipts.inject('body', bad)

    def test_unbalanced_or_repeated_markers_fail(self):
        for body in (receipts.BEGIN_MARKER, receipts.END_MARKER + receipts.BEGIN_MARKER,
                     receipts.BEGIN_MARKER + receipts.END_MARKER + receipts.BEGIN_MARKER + receipts.END_MARKER):
            with self.assertRaises(ValueError):
                receipts.inject(body, self.receipt)

    def test_hostile_text_cannot_break_out_of_the_block(self):
        receipt = copy.deepcopy(self.receipt)
        receipt['checks'][0]['name'] = '@octocat [click](https://evil.example) | x <script>'
        receipt['checks'][0]['observation'] = '```\n</details>\n# injected heading ```` '
        block = receipts.render_block(receipts.seal(receipt))
        self.assertNotIn('@octocat', block.split('<details>')[0])
        self.assertNotIn('<script>', block.split('<details>')[0])
        self.assertEqual(receipts.extract(receipts.inject('x', receipts.seal(receipt)))['checks'][0]['observation'],
                         receipt['checks'][0]['observation'])

    def test_marker_text_inside_receipt_is_refused(self):
        receipt = copy.deepcopy(self.receipt)
        receipt['checks'][0]['observation'] = receipts.END_MARKER
        with self.assertRaises(ValueError):
            receipts.render_block(receipts.seal(receipt))

    def test_edited_block_is_detected(self):
        text = receipts.inject('x', self.receipt).replace('STAGED', 'VERIFIED', 1)
        with self.assertRaises(ValueError):
            receipts.extract(text)

    def test_body_size_limit(self):
        with self.assertRaises(ValueError):
            receipts.inject('x' * receipts.PR_BODY_LIMIT, self.receipt)

    def test_binding_checks(self):
        subject = self.receipt['subject']
        receipts.check_binding(self.receipt, subject['repository'], 521, subject['head_sha'])
        for args in ((subject['repository'], 521, 'f' * 40), ('other/repo', 521, subject['head_sha']),
                     (subject['repository'], 999, subject['head_sha'])):
            with self.assertRaises(ValueError):
                receipts.check_binding(self.receipt, *args)


class Cli(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run([sys.executable, str(ROOT / 'ges' / 'receipts.py'), *args],
                              capture_output=True, text=True, cwd=tempfile.gettempdir())

    def test_validate_exit_codes(self):
        self.assertEqual(self.run_cli('validate', str(FX / 'valid' / 'merged.json')).returncode, 0)
        result = self.run_cli('validate', str(FX / 'valid' / 'merged.json'), str(FX / 'invalid' / 'short-sha.json'))
        self.assertEqual(result.returncode, 2)
        self.assertIn('head_sha', result.stderr)

    def test_missing_file_is_a_clean_failure(self):
        self.assertEqual(self.run_cli('validate', '/nonexistent/receipt.json').returncode, 2)

    def test_seal_roundtrip(self):
        with tempfile.TemporaryDirectory() as tmp:
            unsealed = {k: v for k, v in load(FX / 'valid' / 'staged-pass.json').items() if k not in ('id', 'schema')}
            source, target = Path(tmp) / 'in.json', Path(tmp) / 'out.json'
            source.write_text(json.dumps(unsealed))
            self.assertEqual(self.run_cli('seal', '--input', str(source), '--output', str(target)).returncode, 0)
            self.assertEqual(load(target), load(FX / 'valid' / 'staged-pass.json'))

    def test_main_cli_is_wired(self):
        result = subprocess.run([sys.executable, '-m', 'ges', 'receipt', 'validate', str(FX / 'valid' / 'staged-pass.json')],
                                capture_output=True, text=True, cwd=ROOT)
        self.assertEqual(result.returncode, 0, result.stderr)


class ActionScript(unittest.TestCase):
    """Run the composite action's shell step against a fake `gh` that records its calls."""

    def setUp(self):
        action = yaml.safe_load(ACTION.read_text(encoding='utf-8'))
        self.script = action['runs']['steps'][0]['run']
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.dir = Path(self.tmp.name)
        self.receipt = load(FX / 'valid' / 'staged-pass.json')
        (self.dir / 'receipt.json').write_text(json.dumps(self.receipt))
        self.state = self.dir / 'pr-body.txt'
        self.state.write_text('Existing description')
        fake = self.dir / 'bin' / 'gh'
        fake.parent.mkdir()
        fake.write_text('''#!/usr/bin/env python3
import json, os, sys
state = os.environ['FAKE_BODY']
args = sys.argv[1:]
if args[0] != 'api':
    sys.exit(9)
if '-X' in args:
    if os.environ.get('FAKE_DENY') == '1':
        print('HTTP 403', file=sys.stderr)
        sys.exit(1)
    spec = [a for a in args if a.startswith('body=@')][0][6:]
    if os.environ.get('FAKE_DROP') != '1':
        open(state, 'w').write(open(spec).read())
    print('{}')
else:
    print(json.dumps({'body': open(state).read(), 'head': {'sha': os.environ['FAKE_HEAD']}}))
''')
        fake.chmod(fake.stat().st_mode | stat.S_IEXEC)

    def run_action(self, head=None, event='pull_request', **extra):
        env = {
            'PATH': str(self.dir / 'bin') + os.pathsep + os.environ['PATH'],
            'RECEIPT_PATH': 'receipt.json', 'INPUT_PR': '', 'EVENT_PR': '521', 'EVENT_NAME': event,
            'REPOSITORY': '4444J99/guide-github-standard', 'GH_TOKEN': 'unused-fake',
            'ACTION_PATH': str(ROOT / '.github' / 'actions' / 'inject-agent-receipt'),
            'WORKSPACE': str(self.dir), 'RUNNER_TEMP_DIR': str(self.dir / 'tmp'),
            'GITHUB_OUTPUT': str(self.dir / 'out.txt'), 'FAKE_BODY': str(self.state),
            'FAKE_HEAD': head or self.receipt['subject']['head_sha'],
        }
        env.update(extra)
        (self.dir / 'tmp').mkdir(exist_ok=True)
        return subprocess.run(['bash', '-c', self.script], env=env, capture_output=True, text=True)

    def test_success_embeds_receipt_and_is_idempotent(self):
        first = self.run_action()
        self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
        body = self.state.read_text()
        self.assertTrue(body.startswith('Existing description'))
        self.assertEqual(receipts.extract(body)['id'], self.receipt['id'])
        self.assertIn('receipt-id=' + self.receipt['id'], (self.dir / 'out.txt').read_text())
        self.assertEqual(self.run_action().returncode, 0)
        self.assertEqual(self.state.read_text(), body)

    def test_pull_request_target_is_refused(self):
        result = self.run_action(event='pull_request_target')
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.state.read_text(), 'Existing description')

    def test_stale_head_is_refused(self):
        result = self.run_action(head='9' * 40)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('::error', result.stdout)
        self.assertEqual(self.state.read_text(), 'Existing description')

    def test_invalid_receipt_is_refused(self):
        (self.dir / 'receipt.json').write_text((FX / 'invalid' / 'tampered-content.json').read_text())
        self.assertNotEqual(self.run_action().returncode, 0)
        self.assertEqual(self.state.read_text(), 'Existing description')

    def test_missing_receipt_and_bad_pr_number_fail(self):
        self.assertNotEqual(self.run_action(RECEIPT_PATH='absent.json').returncode, 0)
        self.assertNotEqual(self.run_action(EVENT_PR='12; rm -rf').returncode, 0)

    def test_read_only_token_fails_visibly(self):
        result = self.run_action(FAKE_DENY='1')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('pull-requests: write', result.stdout)

    def test_unconfirmed_write_fails(self):
        self.assertNotEqual(self.run_action(FAKE_DROP='1').returncode, 0)

    def test_action_has_no_unpinned_uses_and_no_expression_in_script(self):
        action = yaml.safe_load(ACTION.read_text(encoding='utf-8'))
        for step in action['runs']['steps']:
            self.assertNotIn('uses', step)
            self.assertNotIn('${{', step['run'])


if __name__ == '__main__':
    unittest.main()
