"""Adversarial exact-revision observations and bounded collector integration."""
import copy
import json
import subprocess
import sys
import tempfile
import unittest
from datetime import UTC, datetime
from pathlib import Path
from urllib.parse import parse_qs

import test_collector_contracts as collector_fixtures

from ges.branch_checks import assess

Response = collector_fixtures.Response
SHA = collector_fixtures.SHA

NOW = datetime(2026, 10, 7, 0, 35, tzinfo=UTC)


def fixture():
    profile = {'target': 'o/r', 'max_age_hours': 1,
               'required_checks': [{'context': 'ci', 'app_id': 15368, 'provider': 'actions'}]}
    def obs(rows):
        return {'status': 'OK', 'complete': True, 'truncated': False, 'revision': SHA, 'data': rows}
    snapshot = {'target': 'o/r', 'target_revision': SHA, 'check_revision': SHA,
                'observed_at': NOW.isoformat(), 'observations': {
                    'check_runs': obs([{'id': 4, 'name': 'ci', 'head_sha': SHA, 'status': 'completed', 'conclusion': 'success', 'app': {'id': 15368}, 'check_suite': {'id': 6}}]),
                    'commit_statuses': obs([]),
                    'workflow_runs': obs([{'id': 3, 'head_sha': SHA, 'check_suite_id': 6, 'event': 'pull_request'}])}}
    return snapshot, profile


class BranchChecks(unittest.TestCase):
    def assess(self, snapshot, profile, kind='head'):
        return assess(snapshot, profile, SHA, kind, observed_now=NOW)

    def test_success_remains_an_observation_not_enforcement(self):
        result = self.assess(*fixture())
        self.assertTrue(result['observed_checks_pass'])
        for field in ('policy_adopted', 'native_enforcement_verified', 'workflow_execution_proved', 'integration_revision_selection_verified'):
            self.assertFalse(result[field])

    def test_missing_target_cannot_pass(self):
        snapshot, profile = fixture()
        del snapshot['target']; del profile['target']
        with self.assertRaises(ValueError):
            self.assess(snapshot, profile)

    def test_target_mismatch_and_wrong_head_fail_closed(self):
        for key in ('target', 'target_revision', 'check_revision'):
            snapshot, profile = fixture(); snapshot[key] = 'other'
            self.assertFalse(self.assess(snapshot, profile)['observed_checks_pass'])

    def test_same_name_status_failure_cannot_be_hidden_by_check_success(self):
        snapshot, profile = fixture()
        snapshot['observations']['commit_statuses']['data'] = [{'context': 'ci', 'state': 'failure'}, {'context': 'ci', 'state': 'success'}]
        result = self.assess(snapshot, profile)
        self.assertEqual(result['checks'][0]['status'], 'FAIL')

    def test_latest_success_status_and_check_both_pass(self):
        snapshot, profile = fixture()
        snapshot['observations']['commit_statuses']['data'] = [{'context': 'ci', 'state': 'success'}, {'context': 'ci', 'state': 'failure'}]
        self.assertTrue(self.assess(snapshot, profile)['observed_checks_pass'])

    def test_wrong_publisher_and_duplicate_checks_are_unknown(self):
        for mode in ('wrong_app', 'duplicates', 'missing'):
            snapshot, profile = fixture(); rows = snapshot['observations']['check_runs']['data']
            if mode == 'wrong_app': rows[0]['app']['id'] = 8
            elif mode == 'duplicates': rows.append(copy.deepcopy(rows[0]))
            else: rows.clear()
            self.assertEqual(self.assess(snapshot, profile)['checks'][0]['status'], 'NOT_VERIFIABLE')

    def test_wrong_check_sha_is_unknown(self):
        snapshot, profile = fixture(); snapshot['observations']['check_runs']['data'][0]['head_sha'] = 'b' * 40
        self.assertEqual(self.assess(snapshot, profile)['checks'][0]['status'], 'NOT_VERIFIABLE')

    def test_malformed_check_and_app_id_are_not_selected(self):
        for app_id in (15368.0, True, None):
            snapshot, profile = fixture(); snapshot['observations']['check_runs']['data'][0]['app']['id'] = app_id
            self.assertFalse(self.assess(snapshot, profile)['observed_checks_pass'])
        snapshot, profile = fixture(); del snapshot['observations']['check_runs']['data'][0]['id']
        self.assertFalse(self.assess(snapshot, profile)['observed_checks_pass'])

    def test_non_success_conclusions_and_pending_do_not_pass(self):
        for conclusion in ('skipped', 'neutral', 'failure', 'cancelled', None):
            snapshot, profile = fixture(); snapshot['observations']['check_runs']['data'][0]['conclusion'] = conclusion
            self.assertEqual(self.assess(snapshot, profile)['checks'][0]['status'], 'FAIL')
        snapshot, profile = fixture(); snapshot['observations']['check_runs']['data'][0]['status'] = 'queued'
        self.assertFalse(self.assess(snapshot, profile)['observed_checks_pass'])

    def test_manual_event_and_queue_wrong_event_do_not_pass(self):
        for event, kind, expected in (('workflow_dispatch', 'head', False), ('pull_request', 'merge_group', False), ('merge_group', 'merge_group', True)):
            snapshot, profile = fixture(); snapshot['observations']['workflow_runs']['data'][0]['event'] = event
            self.assertEqual(self.assess(snapshot, profile, kind)['observed_checks_pass'], expected)

    def test_missing_workflow_suite_binding_is_unknown(self):
        snapshot, profile = fixture(); snapshot['observations']['workflow_runs']['data'][0]['check_suite_id'] = 7
        self.assertEqual(self.assess(snapshot, profile)['checks'][0]['status'], 'NOT_VERIFIABLE')

    def test_external_app_has_no_actions_event_requirement(self):
        snapshot, profile = fixture(); profile['required_checks'][0]['provider'] = 'external'
        del snapshot['observations']['workflow_runs']
        self.assertTrue(self.assess(snapshot, profile)['observed_checks_pass'])

    def test_incomplete_or_wrong_revision_observations_never_pass(self):
        for name in ('check_runs', 'commit_statuses', 'workflow_runs'):
            for key, value in (('complete', False), ('truncated', True), ('revision', 'b' * 40), ('data', None), ('status', 'HTTP_ERROR')):
                snapshot, profile = fixture(); snapshot['observations'][name][key] = value
                self.assertFalse(self.assess(snapshot, profile)['observed_checks_pass'])

    def test_stale_future_and_invalid_observation_times(self):
        for stamp in ('2026-10-06T00:00:00+00:00', '2026-10-08T00:00:00+00:00', 'invalid', None):
            snapshot, profile = fixture(); snapshot['observed_at'] = stamp
            self.assertFalse(self.assess(snapshot, profile)['observed_checks_pass'])

    def test_invalid_profile_and_revision_rejected(self):
        for mutation in ({'required_checks': []}, {'target': None}, {'max_age_hours': 0}, {'max_age_hours': True}):
            snapshot, profile = fixture(); profile.update(mutation)
            with self.assertRaises(ValueError): self.assess(snapshot, profile)
        with self.assertRaises(ValueError): assess(*fixture(), 'main', 'head')

    def test_cli_failure_exit_is_not_success(self):
        snapshot, profile = fixture(); snapshot['observations']['check_runs']['data'] = []
        # Use a present-day timestamp: this subprocess does not use our injected clock.
        snapshot['observed_at'] = datetime.now(UTC).isoformat()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name, value in (('snapshot', snapshot), ('profile', profile)):
                (root / (name + '.json')).write_text(json.dumps(value))
            process = subprocess.run([sys.executable, '-m', 'ges', 'branch-checks', '--snapshot', str(root/'snapshot.json'), '--profile', str(root/'profile.json'), '--revision', SHA, '--revision-kind', 'head', '--output', str(root/'report.json')], capture_output=True, text=True, check=False)
            self.assertEqual(process.returncode, 1, process.stderr)
            self.assertFalse(json.loads((root/'report.json').read_text())['observed_checks_pass'])


class BranchCollection(unittest.TestCase):
    def run_repository(self, *args, **kwargs):
        return collector_fixtures.CollectorContracts().run_repository(*args, **kwargs)

    def test_envelope_pages_are_combined_and_sha_bound(self):
        def check_runs(parsed):
            page = int(parse_qs(parsed.query)['page'][0])
            return Response({'total_count': 2, 'check_runs': [{'id': page}]})
        snapshot, urls = self.run_repository({'/repos/o/r/commits/'+SHA+'/check-runs': check_runs})
        observation = snapshot['observations']['check_runs']
        self.assertEqual(observation['data'], [{'id': 1}, {'id': 2}])
        self.assertTrue(observation['complete'])
        self.assertEqual(observation['revision'], SHA)
        self.assertTrue(any('head_sha='+SHA in url for url in urls))

    def test_envelope_count_and_link_gaps_never_pass(self):
        for payload in ({'total_count': 2, 'check_runs': []}, {'total_count': '2', 'check_runs': []}, {'total_count': 2, 'check_runs': [{'id': 1}]}):
            snapshot, _ = self.run_repository({'/repos/o/r/commits/'+SHA+'/check-runs': lambda parsed, payload=payload: Response(payload, '<https://api.github.com/x?page=1>; rel="prev"')})
            self.assertFalse(snapshot['observations']['check_runs']['complete'])

    def test_explicit_check_revision_does_not_relabel_branch_head(self):
        other = 'b' * 40
        snapshot, urls = self.run_repository(check_revision=other)
        self.assertEqual(snapshot['target_revision'], SHA)
        self.assertEqual(snapshot['check_revision'], other)
        self.assertTrue(any('/commits/'+other+'/statuses' in url for url in urls))
        with self.assertRaises(ValueError): self.run_repository(check_revision='main')


class PilotAggregator(unittest.TestCase):
    def test_failed_skipped_and_cancelled_dependencies_fail_shell(self):
        import yaml
        template = Path(__file__).resolve().parents[1] / 'templates/branch-pilot-workflow.yml'
        workflow = yaml.safe_load(template.read_text())
        command = workflow['jobs']['pilot-required']['steps'][0]['run']
        for value in ('success', 'failure', 'skipped', 'cancelled', ''):
            result = subprocess.run(['sh', '-c', command], env={'TEST_RESULT': value}, check=False)
            self.assertEqual(result.returncode == 0, value == 'success')


if __name__ == '__main__':
    unittest.main()
