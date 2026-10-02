import gzip
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
import urllib.request

from ges.core import digest
from ges.pages import acquire, cached_pages, validate_body, validate_pages, DocsRedirect


class PageAcquisitionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.ledger = self.root / 'ledger.json'
        self.cache = self.root / 'cache'
        self.pages = [{'path': path, 'version': 'free-pro-team@latest',
                       'page_id': digest(['free-pro-team@latest', path])[:24]}
                      for path in ('/en', '/en/actions')]
        self.ledger.write_text(json.dumps(self.pages))

    def fetch(self, page, timeout):
        return ('# Article\n'+page['path']).encode()

    def test_resume_does_not_fetch_verified_bodies(self):
        first = acquire(self.ledger, self.cache, workers=1, limit=1, fetcher=self.fetch)
        self.assertEqual(first['denominator'], 2)
        self.assertFalse(first['complete'])
        calls = []
        def fetch(page, timeout):
            calls.append(page['page_id'])
            return self.fetch(page, timeout)
        second = acquire(self.ledger, self.cache, workers=1, fetcher=fetch)
        self.assertTrue(second['complete'])
        self.assertEqual(len(calls), 1)
        for key in ('source_revision_verified', 'semantic_review_complete', 'rights_cleared', 'credentials_sent'):
            self.assertFalse(second[key])

    def test_corruption_cannot_count(self):
        acquire(self.ledger, self.cache, workers=1, limit=1, fetcher=self.fetch)
        row = json.loads((self.cache / 'index.jsonl').read_text().splitlines()[0])
        with gzip.open(self.cache / row['body_file'], 'wb') as out:
            out.write(b'wrong body')
        with self.assertRaises(ValueError):
            acquire(self.ledger, self.cache, fetcher=self.fetch)

    def test_changed_ledger_cannot_reuse_index(self):
        acquire(self.ledger, self.cache, workers=1, limit=1, fetcher=self.fetch)
        self.ledger.write_text(json.dumps(self.pages, indent=2))
        with self.assertRaises(ValueError):
            acquire(self.ledger, self.cache, fetcher=self.fetch)

    def test_failure_kill_switch_preserves_denominator(self):
        def fail(page, timeout):
            raise TimeoutError('not a receipt')
        report = acquire(self.ledger, self.cache, workers=1, failure_limit=1, fetcher=fail)
        self.assertTrue(report['kill_switch'])
        self.assertEqual(report['remaining'], 2)
        self.assertEqual(len(report['errors_this_attempt']), 1)
        self.assertFalse(report['complete'])

    def test_bad_bodies_rejected(self):
        for body in (b'', b' ', b'<html>error', b'<!DOCTYPE html>', b'\xff', b'x'*5_000_001):
            with self.subTest(body_length=len(body)), self.assertRaises((ValueError, UnicodeError)):
                validate_body(body)

    def test_invalid_identity_rejected(self):
        self.pages[0]['page_id'] = 'fake'
        with self.assertRaises(ValueError):
            validate_pages(self.pages)

    def test_duplicate_identity_rejected(self):
        with self.assertRaises(ValueError):
            validate_pages([self.pages[0], self.pages[0]])

    def test_root_english_path_is_valid(self):
        validate_pages(self.pages)

    def test_acquisition_bounds(self):
        for kwargs in ({'workers': 0}, {'workers': 5}, {'timeout': 31}, {'limit': -1}, {'failure_limit': 0}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                acquire(self.ledger, self.cache, **kwargs)

    def test_cross_origin_redirect_rejected(self):
        handler = DocsRedirect()
        request = urllib.request.Request('https://docs.github.com/api/article/body')
        for target in ('http://docs.github.com/en', 'https://example.com/en',
                       'https://user@docs.github.com/en', 'https://docs.github.com:444/en'):
            with self.subTest(target=target), self.assertRaises(ValueError):
                handler.redirect_request(request, None, 302, '', {}, target)

    def test_cached_body_path_cannot_escape(self):
        acquire(self.ledger, self.cache, workers=1, limit=1, fetcher=self.fetch)
        index = self.cache / 'index.jsonl'
        row = json.loads(index.read_text())
        row['body_file'] = '../outside.md.gz'
        index.write_text(json.dumps(row)+'\n')
        with self.assertRaises(ValueError):
            cached_pages(self.cache, self.pages, hashlib.sha256(self.ledger.read_bytes()).hexdigest())
