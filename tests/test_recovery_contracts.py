"""Counterexamples for evidence and scope defects found during recovery."""
import copy
import json
import unittest
from pathlib import Path

from ges.checks import execute, endpoint
from ges.evaluate import audit, gate


class RecoveryContracts(unittest.TestCase):
    def setUp(self):
        self.controls = json.loads(Path('controls/catalog.json').read_text())
        if isinstance(self.controls, dict): self.controls = self.controls['controls']

    def check(self, spec, name, data, **metadata):
        return execute({'verification': spec}, {'observations': {
            name: {'status': 'OK', 'data': data, 'complete': True, **metadata}}}, {})[0]

    def test_missing_completeness_cannot_pass(self):
        for kind in ('dependabot_alerts','code_scanning_alerts','secret_scanning_alerts','deploy_keys'):
            s={'observations': {kind: {'status':'OK','data':[]}}}
            self.assertEqual(execute({'verification':{'kind':kind}},s,{})[0],'NOT_VERIFIABLE')

    def test_job_write_permission_fails(self):
        files={'.github/workflows/test.yml':'permissions: read-all\njobs:\n  test:\n    permissions: write-all\n'}
        self.assertEqual(self.check({'kind':'workflow_permissions'},'files',files),'FAIL')

    def test_boolean_is_not_review_count(self):
        spec = {'kind': 'effective_rule', 'rule_type': 'pull_request',
                'parameter': 'required_approving_review_count', 'operator': 'at_least', 'value': 1}
        self.assertEqual(self.check(spec, 'effective_branch_rules', [{
            'type': 'pull_request', 'parameters': {'required_approving_review_count': True}}]), 'FAIL')

    def test_incomplete_alerts_cannot_pass(self):
        self.assertEqual(self.check({'kind': 'dependabot_alerts'}, 'dependabot_alerts', [], complete=False), 'NOT_VERIFIABLE')

    def test_malformed_alert_is_not_ignored(self):
        for kind in ('dependabot_alerts', 'code_scanning_alerts', 'secret_scanning_alerts'):
            with self.subTest(kind=kind):
                self.assertEqual(self.check({'kind': kind, 'severity': 'critical'}, kind, [None]), 'ERROR')

    def test_code_scanning_uses_security_severity(self):
        self.assertEqual(self.check({'kind': 'code_scanning_alerts', 'severity': 'critical'},
                                   'code_scanning_alerts', [{'rule': {'severity': 'error', 'security_severity_level': 'critical'}}]), 'FAIL')

    def test_untyped_observation_is_error(self):
        self.assertEqual(endpoint({'observations': {'files': []}}, 'files')[1][0], 'ERROR')

    def test_missing_dependabot_updates_fails(self):
        self.assertEqual(self.check({'kind': 'dependabot_config'}, 'dependabot_config',
                                   {'content': 'version: 2', 'encoding': 'utf-8'}), 'FAIL')

    def test_unknown_actions_approval_permission_does_not_pass(self):
        self.assertEqual(self.check({'kind': 'actions_permissions', 'require_read_permissions': True},
                                   'actions_permissions_workflow', {'default_workflow_permissions': 'read'}), 'NOT_VERIFIABLE')

    def test_repository_attestation_cannot_prove_org_control(self):
        control = copy.deepcopy(next(c for c in self.controls if c['scope'] == 'organization'))
        control['applicability'] = {}
        control['verification'] = {'kind': 'manual'}
        snapshot = {'target': 'owner/repo', 'target_revision': 'a' * 40,
                    'observed_at': '2026-10-01T12:00:00Z', 'observations': {'organization': {'status': 'OK', 'data': {}}}}
        attestation = {'control_id': control['id'], 'control_revision': control['revision'],
                       'target': snapshot['target'], 'target_revision': snapshot['target_revision'],
                       'reviewer': 'reviewer', 'reviewed_at': '2026-10-01T11:00:00Z',
                       'expires_at': '2026-10-02T00:00:00Z', 'outcome': 'PASS', 'evidence_ref': 'review', 'rationale': 'reviewed'}
        report = audit([control], snapshot, {'context': {}, 'authorized_reviewers': ['reviewer']},
                       at='2026-10-01T12:00:00Z', attestations=[attestation])
        self.assertEqual(report['results'][0]['outcome'], 'NOT_VERIFIABLE')

    def test_missing_org_evidence_blocks_gate(self):
        control = copy.deepcopy(next(c for c in self.controls if c['scope'] == 'organization'))
        control['obligation'] = 'MUST'
        control['applicability'] = {}
        snapshot = {'target': 'owner/repo', 'target_revision': 'a' * 40,
                    'observed_at': '2026-10-01T12:00:00Z', 'observations': {}}
        report = audit([control], snapshot, {'context': {}}, at='2026-10-01T12:00:00Z')
        self.assertEqual(report['results'][0]['applicability'], 'UNKNOWN')
        self.assertFalse(gate(report)[0])

    def test_nonadopted_control_blocks_gate(self):
        row = {'control_id': 'candidate', 'control_status': 'NON_ADOPTED_DRAFT',
               'obligation': 'MAY', 'applicability': 'APPLICABLE', 'outcome': 'PASS', 'exception_status': 'NONE'}
        self.assertFalse(gate({'results': [row]})[0])

    def test_malformed_composite_cannot_pass(self):
        files = {'.github/workflows/test.yml': 'jobs:\n  test:\n    steps:\n      - uses: ./local\n',
                 'local/action.yml': 'runs:\n  using: composite\n  steps: broken\n'}
        self.assertEqual(self.check({'kind': 'workflow_pinning'}, 'files', files, complete=True), 'FAIL')

    def test_local_reusable_workflow_is_followed(self):
        files = {'.github/workflows/test.yml': 'jobs:\n  test:\n    uses: ./.github/workflows/reuse.yml\n',
                 '.github/workflows/reuse.yml': 'on: workflow_call\njobs:\n  test:\n    steps:\n      - uses: owner/action@' + 'a' * 40 + '\n'}
        self.assertEqual(self.check({'kind': 'workflow_pinning'}, 'files', files, complete=True), 'PASS')
        files['.github/workflows/reuse.yml'] = 'jobs:\n  loop:\n    uses: ./.github/workflows/test.yml\n'
        self.assertEqual(self.check({'kind': 'workflow_pinning'}, 'files', files, complete=True), 'FAIL')
