"""Execute the workflow's actual producer against isolated Git fixtures."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from ges.yamlutil import parse

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = parse((ROOT / '.github/workflows/warning-pilot.yml').read_text())
STEPS = WORKFLOW['jobs']['inspect']['steps']
SCRIPT = next(s['run'] for s in STEPS if s.get('id') == 'inspect').split("<<'PY'\n", 1)[1].rsplit('\nPY', 1)[0]
VALID = 'on: push\npermissions: {contents: read}\njobs: {test: {runs-on: ubuntu-24.04, steps: [{run: "true"}]}}\n'


class WarningWorkflowTests(unittest.TestCase):
    def run_fixture(self, files=None, checks='["test"]', event='pull_request', mismatch=False):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            candidate = root / 'candidate'
            candidate.mkdir()
            for args in (('init', '-q'), ('config', 'user.name', 'Fixture'),
                         ('config', 'user.email', 'fixture@example.invalid')):
                subprocess.run(['git', '-C', str(candidate), *args], check=True, capture_output=True)
            for name, content in (files if files is not None else {'ci.yml': VALID}).items():
                p = candidate / '.github/workflows' / name
                p.parent.mkdir(parents=True, exist_ok=True)
                if isinstance(content, tuple):
                    p.symlink_to(content[0])
                else:
                    p.write_bytes(content if isinstance(content, bytes) else content.encode())
            # A consumer-side Python module must never be imported/executed.
            (candidate / 'json.py').write_text('raise RuntimeError("consumer code executed")')
            subprocess.run(['git', '-C', str(candidate), 'add', '.'], check=True, capture_output=True)
            subprocess.run(['git', '-C', str(candidate), 'commit', '-qm', 'fixture'], check=True, capture_output=True)
            sha = subprocess.check_output(['git', '-C', str(candidate), 'rev-parse', 'HEAD'], text=True).strip()
            env = dict(os.environ, CANDIDATE=str(candidate), REVISION='a'*40 if mismatch else sha,
                       REPOSITORY_ID='1', EXPECTED_CHECKS=checks, EVIDENCE=str(root/'evidence'),
                       GITHUB_EVENT_NAME=event, GITHUB_REPOSITORY_OWNER='fixture',
                       GITHUB_REPOSITORY='fixture/repo', GITHUB_RUN_ID='123', GITHUB_RUN_ATTEMPT='1',
                       GITHUB_STEP_SUMMARY=str(root/'summary'))
            result = subprocess.run([sys.executable, '-c', SCRIPT], cwd=ROOT, env=env,
                                    capture_output=True, text=True, timeout=30)
            data = {p.name: json.loads(p.read_text()) for p in (root/'evidence').glob('*.json')}
            return result, data

    def test_read_only_pins_and_narrow_artifact_boundary(self):
        self.assertEqual(WORKFLOW['permissions'], {'contents': 'read'})
        self.assertEqual(set(WORKFLOW.get('on', WORKFLOW.get(True))), {'workflow_call'})
        job = WORKFLOW['jobs']['inspect']
        self.assertLessEqual(job['timeout-minutes'], 3)
        self.assertNotIn('continue-on-error', job)
        for step in STEPS:
            self.assertNotIn('continue-on-error', step)
            if 'uses' in step:
                self.assertRegex(step['uses'], r'@[0-9a-f]{40}$')
            if 'run' in step:
                self.assertNotIn('${{', step['run'])
        checkouts = [s for s in STEPS if s.get('uses', '').startswith('actions/checkout@')]
        self.assertTrue(all(s['with']['persist-credentials'] is False for s in checkouts))
        self.assertEqual(checkouts[1]['with']['ref'], 'a5cdf48e9f255cb407a1ae69be62397f1151847d')
        self.assertEqual(checkouts[0]['with']['sparse-checkout'], '!/*')
        upload = STEPS[-1]['with']
        self.assertNotIn('snapshot', upload['path'])
        self.assertNotIn('*', upload['path'])
        self.assertEqual(upload['if-no-files-found'], 'error')
        self.assertEqual(upload['retention-days'], 30)

    def test_positive_configuration_unknown_execution_and_manifest(self):
        result, data = self.run_fixture()
        self.assertEqual(result.returncode, 0, result.stderr)
        report = data['report.json']
        self.assertEqual([f['status'] for f in report['findings']], ['OBSERVED', 'OBSERVED', 'NOT_VERIFIABLE'])
        self.assertFalse(report['compliance_certified'])
        manifest = data['manifest.json']
        self.assertFalse(manifest['retrieval_verified'])
        self.assertFalse(manifest['restoration_verified'])
        for name, expected in manifest['files'].items():
            raw = (json.dumps(data[name], indent=2) + '\n').encode()
            self.assertEqual(hashlib.sha256(raw).hexdigest(), expected['sha256'])
            self.assertEqual(len(raw), expected['bytes'])

    def test_warnings_are_visible_and_advisory_exit_zero(self):
        result, data = self.run_fixture({'ci.yml': VALID.replace('contents: read', 'contents: write').replace('run: "true"', 'uses: actions/checkout@main')})
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual([f['status'] for f in data['report.json']['findings'][:2]], ['WARN', 'WARN'])

    def test_symlink_duplicate_yaml_and_missing_workflows_never_positive(self):
        for files in ({'ci.yml': ('../../json.py',)}, {'ci.yml': 'jobs: {}\njobs: {}'}, {}):
            with self.subTest(files=files):
                result, data = self.run_fixture(files)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertTrue(all(f['status'] != 'OBSERVED' for f in data['report.json']['findings'][:2]))

    def test_binary_oversized_and_excessive_inventory_never_positive(self):
        for files in ({'ci.yml': b'\xff'}, {'ci.yml': b'x' * (1024*1024+1)},
                      {f'{i}.yml': VALID for i in range(129)}):
            with self.subTest(count=len(files)):
                result, data = self.run_fixture(files)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertFalse(data['snapshot.json']['observations']['files']['complete'])
                self.assertTrue(all(f['status'] != 'OBSERVED' for f in data['report.json']['findings'][:2]))

    def test_bad_plan_revision_and_privileged_event_fail_visibly(self):
        for options in ({'checks': '[]'}, {'checks': '["test", "test"]'}, {'checks': 'not-json'},
                        {'mismatch': True}, {'event': 'pull_request_target'}, {'event': 'workflow_run'}):
            with self.subTest(options=options):
                result, data = self.run_fixture(**options)
                self.assertNotEqual(result.returncode, 0)
                self.assertNotIn('report.json', data)

