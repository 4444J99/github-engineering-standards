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
