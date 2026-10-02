"""Resumable, credential-free article acquisition into a private ignored cache.

Acquisition is not semantic review or a source-commit/rendering certificate.
"""
from __future__ import annotations

import concurrent.futures as cf
import fcntl
import gzip
import hashlib
import json
from pathlib import Path
import re
import urllib.error
import urllib.parse
import urllib.request

from .core import ROOT, digest, dump, now, safe_path, timestamp

MAX_BYTES = 5_000_000


class DocsRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        parsed = urllib.parse.urlsplit(newurl)
        if (parsed.scheme != 'https' or parsed.hostname != 'docs.github.com' or
                parsed.port not in (None, 443) or parsed.username or parsed.password):
            raise ValueError('Article redirect escaped credential-free Docs origin')
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def validate_pages(pages: list[dict]) -> None:
    if not isinstance(pages, list) or not pages:
        raise ValueError('Page ledger must be a nonempty array')
    ids, keys = set(), set()
    for page in pages:
        path, version, identity = page['path'], page['version'], page['page_id']
        if (not isinstance(path, str) or not (path == '/en' or path.startswith('/en/')) or
                any(c in path for c in ('?', '#', '\\', '\r', '\n')) or
                not re.fullmatch(r'[a-z0-9.@-]+', version)):
            raise ValueError('Invalid English article pathname/version')
        if identity != digest([version, path])[:24] or identity in ids or (version, path) in keys:
            raise ValueError('Invalid or duplicate page identity')
        ids.add(identity)
        keys.add((version, path))


def fetch_article(page: dict, timeout: int) -> bytes:
    url = 'https://docs.github.com/api/article/body?pathname='+urllib.parse.quote(page['path'], safe='')
    request = urllib.request.Request(url, headers={
        'User-Agent': 'github-engineering-standards/0.1.0', 'Accept': 'text/markdown'})
    opener = urllib.request.build_opener(DocsRedirect())
    with opener.open(request, timeout=timeout) as response:
        if response.status != 200 or response.headers.get_content_type() != 'text/markdown':
            raise ValueError('Response is not a successful Markdown article')
        body = response.read(MAX_BYTES+1)
    validate_body(body)
    return body


def validate_body(body: bytes) -> None:
    if not isinstance(body, bytes) or not body.strip() or len(body) > MAX_BYTES:
        raise ValueError('Empty or oversized article body')
    body.decode('utf-8')
    if body.lstrip().lower().startswith((b'<!doctype', b'<html')):
        raise ValueError('HTML is not a Markdown article body')


def cached_pages(cache: Path, pages: list[dict], ledger_sha256: str) -> dict[str, dict]:
    """Only durable, digest-matching records from this exact ledger count."""
    validate_pages(pages)
    wanted = {p['page_id']: p for p in pages}
    indexed = {}
    index = safe_path(cache, 'index.jsonl')
    if not index.exists():
        return indexed
    # A writer may be appending during read-only recovery reporting. An
    # unterminated tail is not a committed receipt and never counts.
    index_text = index.read_text()
    lines = index_text.splitlines()
    if index_text and not index_text.endswith('\n'):
        lines = lines[:-1]
    for line in lines:
        if not line.strip():
            continue
        row = json.loads(line)
        if row.get('ledger_sha256') != ledger_sha256:
            raise ValueError('Acquisition index belongs to a different page ledger')
        identity = row['page_id']
        if identity not in wanted or any(row[k] != wanted[identity][k] for k in ('version', 'path')):
            raise ValueError('Acquisition record does not match declared page identity')
        if row.get('status') != 'RETRIEVED':
            continue
        sha = row['sha256']
        if not isinstance(sha, str) or not re.fullmatch('[a-f0-9]{64}', sha):
            raise ValueError('Invalid cached body digest')
        expected_name = identity+'.'+sha+'.md.gz'
        if row['body_file'] != expected_name:
            raise ValueError('Unsafe or mismatched body file identity')
        if timestamp(row['retrieved_at']) > timestamp(now()):
            raise ValueError('Future acquisition timestamp')
        with gzip.open(safe_path(cache, expected_name), 'rb') as stream:
            body = stream.read(MAX_BYTES+1)
        validate_body(body)
        if hashlib.sha256(body).hexdigest() != sha or len(body) != row['bytes']:
            raise ValueError('Cached article body digest/size mismatch')
        indexed[identity] = row
    return indexed


def acquire(ledger: Path, cache: Path, *, workers: int = 2, timeout: int = 15,
            limit: int = 0, failure_limit: int = 8, fetcher=fetch_article) -> dict:
    if (type(workers) is not int or not 1 <= workers <= 4 or
            type(timeout) is not int or not 1 <= timeout <= 30 or
            type(limit) is not int or limit < 0 or
            type(failure_limit) is not int or not 1 <= failure_limit <= 20):
        raise ValueError('Invalid acquisition bounds')
    ledger_bytes = ledger.read_bytes()
    pages = json.loads(ledger_bytes)
    validate_pages(pages)
    ledger_sha = hashlib.sha256(ledger_bytes).hexdigest()
    cache.mkdir(parents=True, exist_ok=True)
    with safe_path(cache, '.writer.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        index_path = safe_path(cache, 'index.jsonl')
        if index_path.exists():
            index_bytes = index_path.read_bytes()
            if index_bytes and not index_bytes.endswith(b'\n'):
                raise ValueError('Interrupted index tail requires explicit recovery; preserve before resuming')
        present = cached_pages(cache, pages, ledger_sha)
        pending = sorted((p for p in pages if p['page_id'] not in present),
                         key=lambda p: bool(p.get('source_matches')))
        selected = pending if limit == 0 else pending[:limit]
        failures, consecutive, stopped = [], 0, False
        iterator = iter(selected)

        def retrieve(page):
            try:
                body = fetcher(page, timeout)
                validate_body(body)
                sha = hashlib.sha256(body).hexdigest()
                name = page['page_id']+'.'+sha+'.md.gz'
                target = safe_path(cache, name)
                if target.exists():
                    with gzip.open(target, 'rb') as stream:
                        existing = stream.read(MAX_BYTES+1)
                    if existing != body:
                        raise ValueError('Existing content-addressed body is corrupt; preserve for recovery')
                else:
                    with gzip.open(target, 'xb') as stream:
                        stream.write(body)
                return {k: page[k] for k in ('page_id', 'path', 'version')} | {
                    'status': 'RETRIEVED', 'retrieved_at': now(), 'ledger_sha256': ledger_sha,
                    'sha256': sha, 'bytes': len(body), 'body_file': name,
                    'source_revision_verified': False, 'semantic_reviewed': False}
            except (OSError, ValueError, UnicodeError) as exc:
                return {k: page[k] for k in ('page_id', 'path', 'version')} | {
                    'status': 'ERROR', 'retrieved_at': now(), 'ledger_sha256': ledger_sha,
                    'error_type': type(exc).__name__, 'http_status': getattr(exc, 'code', None)}

        with safe_path(cache, 'index.jsonl').open('a') as out, cf.ThreadPoolExecutor(max_workers=workers) as pool:
            active = {}
            for _ in range(workers):
                page = next(iterator, None)
                if page is not None:
                    active[pool.submit(retrieve, page)] = page
            while active:
                done, _ = cf.wait(active, return_when=cf.FIRST_COMPLETED)
                for future in done:
                    active.pop(future)
                    row = future.result()
                    out.write(json.dumps(row, sort_keys=True)+'\n')
                    out.flush()
                    if row['status'] == 'RETRIEVED':
                        present[row['page_id']] = row
                        consecutive = 0
                    else:
                        failures.append(row)
                        consecutive += 1
                        if consecutive >= failure_limit:
                            stopped = True
                    if len(present) % 25 == 0 or row['status'] == 'ERROR':
                        print(json.dumps({'retrieved': len(present), 'denominator': len(pages),
                                          'errors': len(failures), 'kill_switch': stopped}), flush=True)
                    page = None if stopped else next(iterator, None)
                    if page is not None:
                        active[pool.submit(retrieve, page)] = page
        report = {'schema_version': 'ges.rendered-acquisition.v1', 'generated_at': now(),
                  'ledger_sha256': ledger_sha, 'denominator': len(pages), 'retrieved': len(present),
                  'remaining': len(pages)-len(present), 'complete': len(present) == len(pages),
                  'errors_this_attempt': failures, 'kill_switch': stopped,
                  'source_revision_verified': False, 'semantic_review_complete': False,
                  'rights_cleared': False, 'credentials_sent': False}
        dump(safe_path(cache, 'acquisition.json'), report)
        return report


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--ledger', type=Path, required=True)
    parser.add_argument('--cache', type=Path, required=True)
    parser.add_argument('--workers', type=int, default=2)
    parser.add_argument('--timeout', type=int, default=15)
    parser.add_argument('--limit', type=int, default=0)
    parser.add_argument('--failure-limit', type=int, default=8)
    args = parser.parse_args()
    try:
        if not args.cache.resolve().is_relative_to((ROOT / '.cache').resolve()):
            raise ValueError('Raw article output must stay inside the private ignored project cache')
        report = acquire(args.ledger, args.cache, workers=args.workers, timeout=args.timeout,
                         limit=args.limit, failure_limit=args.failure_limit)
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print(json.dumps({'complete': False, 'error': str(exc), 'error_type': type(exc).__name__}))
        return 2
    print(json.dumps(report), flush=True)
    return 0 if report['complete'] else 2


if __name__ == '__main__':
    raise SystemExit(main())
