"""Collector contracts tested against deterministic API responses, without credentials."""
import base64
import json
import unittest
import urllib.error
import urllib.parse
import urllib.request
from unittest.mock import patch

from ges.collect import APIOnlyRedirect, collect

SHA = 'a' * 40


class Response:
    def __init__(self, data, link=''):
        self.body = json.dumps(data).encode()
        self.headers = {'Link': link} if link else {}

    def read(self, size):
        return self.body[:size]

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False


class CollectorContracts(unittest.TestCase):
    def run_repository(self, overrides=None, **kwargs):
        urls = []
        def open_request(req, timeout):
            urls.append(req.full_url)
            parsed = urllib.parse.urlparse(req.full_url)
            path = parsed.path
            default = {
                '/repos/o/r': {'owner': {'login': 'o'}, 'default_branch': 'main'},
                '/repos/o/r/git/ref/heads/main': {'object': {'sha': SHA}},
                '/repos/o/r/git/trees/' + SHA: {'tree': [], 'truncated': False},
            }
            data = (overrides or {}).get(path, default.get(path, []))
            if callable(data):
                return data(parsed)
            return Response(data)
        with patch('ges.collect.OPENER.open', side_effect=open_request):
            snapshot = collect('o/r', **kwargs)
        return snapshot, urls

    def test_contents_requests_are_revision_pinned(self):
        snapshot, urls = self.run_repository()
        contents = [url for url in urls if '/contents/' in url]
        self.assertTrue(contents)
        self.assertTrue(all(urllib.parse.parse_qs(urllib.parse.urlparse(url).query)['ref'] == [SHA] for url in contents))
        self.assertEqual(snapshot['target_revision'], SHA)

    def test_local_action_outside_documentation_is_collected(self):
        snapshot, _ = self.run_repository({
            '/repos/o/r/git/trees/' + SHA: {'tree': [{'path': 'tools/setup/action.yml', 'type': 'blob', 'sha': SHA}], 'truncated': False},
            '/repos/o/r/git/blobs/' + SHA: {'content': base64.b64encode(b'runs:\n  using: composite\n').decode()},
        })
        self.assertIn('tools/setup/action.yml', snapshot['observations']['files']['data'])

    def test_null_list_endpoint_is_error(self):
        snapshot, _ = self.run_repository({'/repos/o/r/keys': None})
        self.assertEqual(snapshot['observations']['deploy_keys']['status'], 'ERROR')
        self.assertFalse(snapshot['observations']['deploy_keys']['complete'])

    def test_empty_page_with_next_link_is_not_complete(self):
        snapshot, _ = self.run_repository({'/repos/o/r/keys': lambda parsed: Response([], '<https://api.github.com/repos/o/r/keys?page=2>; rel="next"')}, max_pages=1)
        self.assertFalse(snapshot['observations']['deploy_keys']['complete'])
        self.assertTrue(snapshot['observations']['deploy_keys']['truncated'])

    def test_second_page_is_collected(self):
        def keys(parsed):
            page = urllib.parse.parse_qs(parsed.query)['page'][0]
            return Response([{'id': int(page)}], '<https://api.github.com/repos/o/r/keys?page=2>; rel="next"' if page == '1' else '')
        snapshot, _ = self.run_repository({'/repos/o/r/keys': keys})
        self.assertEqual(snapshot['observations']['deploy_keys']['data'], [{'id': 1}, {'id': 2}])
        self.assertTrue(snapshot['observations']['deploy_keys']['complete'])

    def test_malformed_repository_does_not_crash_or_pass(self):
        snapshot, _ = self.run_repository({'/repos/o/r': {}})
        self.assertEqual(snapshot['observations']['repository']['status'], 'ERROR')

    def test_serialized_repository_omits_nested_credentials_and_auth_echo(self):
        metadata = {'owner': {'login': 'o'}, 'default_branch': 'main',
                    'temp_clone_token': 'synthetic-clone-credential',
                    'permissions': {'admin': True, 'secrets': 'read'},
                    'nested': [{'access_token': {'value': 'synthetic-nested-credential'},
                                'Authorization': 'synthetic-header-credential',
                                'message': 'echo synthetic-request-credential'}]}
        with patch.dict('os.environ', {'GH_TOKEN': 'synthetic-request-credential'}):
            snapshot, _ = self.run_repository({'/repos/o/r': metadata})
        serialized = json.dumps(snapshot)
        for credential in ('synthetic-clone-credential', 'synthetic-nested-credential',
                           'synthetic-header-credential', 'synthetic-request-credential'):
            self.assertNotIn(credential, serialized)
        repo = snapshot['observations']['repository']
        self.assertEqual(repo['data']['permissions'], {'admin': True, 'secrets': 'read'})
        self.assertEqual(snapshot['target_revision'], SHA)
        self.assertTrue(repo['complete'])
        self.assertEqual(repo['credential_fields_omitted'], 4)
        self.assertIn('temp_clone_token', metadata)  # Input fixture is not mutated.

    def test_paginated_alerts_keep_posture_without_raw_secret_values(self):
        def alerts(parsed):
            page = int(urllib.parse.parse_qs(parsed.query)['page'][0])
            row = {'number': page, 'state': 'open', 'secret_type': 'github_token',
                   'secret': 'synthetic-alert-credential-' + str(page),
                   'nested': [{'refresh_token': 'synthetic-refresh-' + str(page)}]}
            return Response([row], '<https://api.github.com/next>; rel="next"' if page == 1 else '')
        snapshot, _ = self.run_repository({'/repos/o/r/secret-scanning/alerts': alerts})
        observed = snapshot['observations']['secret_scanning_alerts']
        serialized = json.dumps(snapshot)
        self.assertNotIn('synthetic-alert-credential', serialized)
        self.assertNotIn('synthetic-refresh-', serialized)
        self.assertEqual([x['number'] for x in observed['data']], [1, 2])
        self.assertTrue(observed['complete'])
        self.assertFalse(observed['truncated'])
        from ges.checks import secret_scanning_alerts
        self.assertEqual(secret_scanning_alerts(snapshot)[0], 'FAIL')

    def test_paginated_envelope_nested_repository_is_sanitized(self):
        snapshot, _ = self.run_repository({
            '/repos/o/r/actions/runs': {'total_count': 1, 'workflow_runs': [
                {'id': 5, 'head_sha': SHA, 'repository': {
                    'temp_clone_token': 'synthetic-envelope-credential',
                    'permissions': {'secrets': 'read'}}}]}})
        observed = snapshot['observations']['workflow_runs']
        self.assertNotIn('synthetic-envelope-credential', json.dumps(snapshot))
        self.assertEqual(observed['data'][0]['id'], 5)
        self.assertEqual(observed['data'][0]['head_sha'], SHA)
        self.assertTrue(observed['complete'])

    def test_partial_page_failure_keeps_sanitized_data_and_unknown_coverage(self):
        def alerts(parsed):
            page = int(urllib.parse.parse_qs(parsed.query)['page'][0])
            if page == 2:
                raise urllib.error.HTTPError(parsed.geturl(), 403, 'Forbidden', {}, None)
            return Response([{'number': 1, 'state': 'open', 'secret': 'synthetic-partial-credential'}],
                            '<https://api.github.com/next>; rel="next"')
        snapshot, _ = self.run_repository({'/repos/o/r/secret-scanning/alerts': alerts})
        observed = snapshot['observations']['secret_scanning_alerts']
        self.assertNotIn('synthetic-partial-credential', json.dumps(snapshot))
        self.assertFalse(observed['complete'])
        self.assertTrue(observed['truncated'])
        self.assertEqual(observed['error_page'], 2)
        self.assertEqual(observed['credential_fields_omitted'], 1)

    def test_active_credential_in_json_key_is_omitted_without_collision(self):
        metadata = {'owner': {'login': 'o'}, 'default_branch': 'main',
                    'echo-synthetic-request-credential': 'value',
                    'echo-[REDACTED]': 'unrelated retained value'}
        with patch.dict('os.environ', {'GH_TOKEN': 'synthetic-request-credential'}):
            snapshot, _ = self.run_repository({'/repos/o/r': metadata})
        self.assertNotIn('synthetic-request-credential', json.dumps(snapshot))
        repo = snapshot['observations']['repository']
        self.assertEqual(repo['data']['echo-[REDACTED]'], 'unrelated retained value')
        self.assertEqual(repo['credential_fields_omitted'], 1)

    def test_decoded_blob_omits_active_credential_and_preserves_identity(self):
        body = b'example: synthetic-request-credential\n'
        with patch.dict('os.environ', {'GH_TOKEN': 'synthetic-request-credential'}):
            snapshot, _ = self.run_repository({
                '/repos/o/r/git/trees/' + SHA: {'tree': [{'path': 'README.md', 'type': 'blob', 'sha': SHA}], 'truncated': False},
                '/repos/o/r/git/blobs/' + SHA: {'content': base64.b64encode(body).decode()},
            })
        files = snapshot['observations']['files']
        self.assertNotIn('synthetic-request-credential', json.dumps(snapshot))
        self.assertEqual(files['data']['README.md']['content'], 'example: [REDACTED]\n')
        self.assertEqual(files['data']['README.md']['blob_sha'], SHA)
        self.assertEqual(files['data']['README.md']['credential_fields_omitted'], 1)
        self.assertTrue(files['complete'])

    def test_zero_bounds_are_rejected(self):
        with self.assertRaises(ValueError):
            collect('o/r', max_pages=0)

    def test_redirect_never_carries_token_to_plaintext_or_other_origin(self):
        request = urllib.request.Request('https://api.github.com/repos/o/r', headers={'Authorization': 'Bearer secret'})
        handler = APIOnlyRedirect()
        for target in ('http://api.github.com/repos/o/r', 'https://other.invalid/repos/o/r'):
            with self.subTest(target=target), self.assertRaises(urllib.error.URLError):
                handler.redirect_request(request, None, 302, 'Found', {}, target)
        redirected = handler.redirect_request(request, None, 302, 'Found', {}, 'https://api.github.com/repos/o/new')
        self.assertEqual(redirected.get_header('Authorization'), 'Bearer secret')


if __name__ == '__main__':
    unittest.main()
