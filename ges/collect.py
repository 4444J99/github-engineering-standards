"""Bounded GitHub read adapter. Tokens stay on api.github.com; no writes."""
from __future__ import annotations
import base64
import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request
from .core import digest, now
from .sources import NoAuthRedirect


class APIOnlyRedirect(NoAuthRedirect):
    """Never forward an API credential to another origin or plaintext URL."""
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        parsed = urllib.parse.urlparse(newurl)
        if parsed.scheme != 'https' or parsed.netloc != 'api.github.com':
            raise urllib.error.URLError('API redirect outside trusted HTTPS origin')
        return super().redirect_request(req, fp, code, msg, headers, newurl)

OPENER = urllib.request.build_opener(APIOnlyRedirect())


def collect(
    target: str | None = None,
    *,
    repository: str | None = None,
    max_files: int = 2000,
    max_pages: int = 10,
    include_org: bool = False,
    include_enterprise: bool = False,
    enterprise_slug: str | None = None,
    target_type: str | None = None,
    ref: str | None = None,
) -> dict:
    """Collect snapshots from GitHub API for repositories or organizations.

    Guarantees:
    - Tokens are strictly isolated to api.github.com via NoAuthRedirect opener.
    - All collections are read-only; no POST/PUT/PATCH/DELETE calls exist.
    - Alert and deploy key endpoints use bounded pagination reporting complete and truncated flags.
    - Organization collection gathers typed organizational posture and defaults.
    """
    target = target or repository
    if not target or not isinstance(target, str):
        raise ValueError('Target repository or organization required')
    if max_pages < 1 or max_files < 1:
        raise ValueError('Collection bounds must be positive')
    if target_type not in {None, 'repository', 'organization'}:
        raise ValueError('Unsupported target type')
    if enterprise_slug and not re.fullmatch(r'[A-Za-z0-9_.-]+', enterprise_slug):
        raise ValueError('Invalid enterprise slug')

    api_credential = os.environ.get('GH_TOKEN') or os.environ.get('GITHUB_TOKEN')
    if include_enterprise:
        enterprise_slug = enterprise_slug or os.environ.get('GITHUB_ENTERPRISE')
        if enterprise_slug and not re.fullmatch(r'[A-Za-z0-9_.-]+', enterprise_slug):
            raise ValueError('Invalid enterprise slug')

    def get(path: str) -> dict:
        headers = {'Accept': 'application/vnd.github+json', 'User-Agent': 'github-engineering-standards/0.1'}
        if api_credential:
            headers['Authorization'] = 'Bearer ' + api_credential
        try:
            req = urllib.request.Request('https://api.github.com' + path, headers=headers)
            with OPENER.open(req, timeout=30) as r:
                raw = r.read(20_000_001)
                if len(raw) > 20_000_000:
                    return {'status': 'ERROR', 'reason': 'Response too large', 'data': None, 'complete': False, 'truncated': True}
                data = json.loads(raw)
                if not isinstance(data, (dict, list)):
                    return {'status': 'ERROR', 'reason': 'Unexpected API payload type', 'data': None, 'complete': False, 'truncated': False}
                return {'status': 'OK', 'http_status': 200, 'data': data, 'complete': True, 'truncated': False}
        except urllib.error.HTTPError as exc:
            return {'status': 'HTTP_ERROR', 'http_status': exc.code, 'data': None, 'complete': False, 'truncated': False}
        except (urllib.error.URLError, TimeoutError, ValueError):
            return {'status': 'ERROR', 'reason': 'Transport or decoding failure', 'data': None, 'complete': False, 'truncated': False}

    def get_paginated(path: str, *, max_pages: int = max_pages, per_page: int = 100) -> dict:
        items = []
        page = 1
        complete = True
        truncated = False
        sep = '&' if '?' in path else '?'
        headers = {'Accept': 'application/vnd.github+json', 'User-Agent': 'github-engineering-standards/0.1'}
        if api_credential:
            headers['Authorization'] = 'Bearer ' + api_credential

        while page <= max_pages:
            p_path = f"{path}{sep}per_page={per_page}&page={page}"
            try:
                req = urllib.request.Request('https://api.github.com' + p_path, headers=headers)
                with OPENER.open(req, timeout=30) as r:
                    raw = r.read(20_000_001)
                    if len(raw) > 20_000_000:
                        return {'status': 'ERROR', 'reason': 'Response too large', 'data': items, 'complete': False, 'truncated': True}
                    page_data = json.loads(raw)
                    if path.endswith('/actions/permissions/repositories') and isinstance(page_data, dict):
                        page_data = page_data.get('repositories')
                    if not isinstance(page_data, list) or any(not isinstance(item, dict) for item in page_data):
                        return {'status': 'ERROR', 'reason': 'Expected API object list', 'data': items, 'complete': False, 'truncated': False}
                    items.extend(page_data)
                    link = r.headers.get('Link', '')
                    has_next = 'rel="next"' in link if link else len(page_data) >= per_page
                    if not has_next:
                        complete = True
                        truncated = False
                        break
                    if page == max_pages:
                        complete = False
                        truncated = True
                        break
                    page += 1
            except urllib.error.HTTPError as exc:
                if page == 1:
                    return {'status': 'HTTP_ERROR', 'http_status': exc.code, 'data': None, 'complete': False, 'truncated': False}
                else:
                    return {'status': 'OK', 'http_status': 200, 'data': items, 'complete': False, 'truncated': True, 'error_page': page}
            except (urllib.error.URLError, TimeoutError, ValueError):
                if page == 1:
                    return {'status': 'ERROR', 'reason': 'Transport or decoding failure', 'data': None, 'complete': False, 'truncated': False}
                else:
                    return {'status': 'OK', 'http_status': 200, 'data': items, 'complete': False, 'truncated': True}

        return {'status': 'OK', 'http_status': 200, 'data': items, 'complete': complete, 'truncated': truncated}

    # Resolve target type
    if target_type is None:
        target_type = 'repository' if '/' in target else 'organization'

    observations: dict[str, dict] = {}

    def organization_defaults(observation: dict, fields: tuple[str, ...]) -> dict:
        data=observation.get('data')
        if observation.get('status') != 'OK' or not isinstance(data,dict):
            return {'status':'NOT_ASSESSED','reason':'Organization metadata unavailable','complete':False}
        values={field:data[field] for field in fields if field in data}
        return {'status':'OK' if len(values)==len(fields) else 'NOT_ASSESSED',
                'data':values,'complete':len(values)==len(fields),'scope':'Organization defaults for new repositories only'}

    # Organization target collection
    if target_type == 'organization':
        if not re.fullmatch(r'[A-Za-z0-9_.-]+', target):
            raise ValueError('Invalid organization')
        org_base = f'/orgs/{target}'
        org_res = get(org_base)
        observations['organization'] = org_res
        if org_res['status'] != 'OK':
            return {
                'target': target,
                'target_revision': None,
                'target_type': 'organization',
                'observed_at': now(),
                'observations': observations,
            }
        org_data = org_res.get('data', {})
        if not isinstance(org_data, dict) or not isinstance(org_data.get('login'), str):
            observations['organization'] = {'status': 'ERROR', 'reason': 'Invalid organization payload', 'data': None, 'complete': False, 'truncated': False}
            return {'target': target, 'target_revision': None, 'target_type': 'organization', 'observed_at': now(), 'observations': observations}
        org_rev = org_data.get('updated_at') or digest(org_data)
        snap = {
            'target': target,
            'target_revision': str(org_rev),
            'target_type': 'organization',
            'observed_at': now(),
            'observations': observations,
        }
        observations['org_members'] = get_paginated(f'{org_base}/members', max_pages=max_pages)
        observations['org_teams'] = get_paginated(f'{org_base}/teams', max_pages=max_pages)
        observations['org_actions_permissions'] = get(f'{org_base}/actions/permissions')
        observations['org_actions_permissions_workflow'] = get(f'{org_base}/actions/permissions/workflow')
        observations['org_actions_permissions_repositories'] = get_paginated(f'{org_base}/actions/permissions/repositories', max_pages=max_pages)
        observations['org_dependabot_defaults'] = organization_defaults(org_res,('dependabot_alerts_enabled_for_new_repositories','dependabot_security_updates_enabled_for_new_repositories'))
        observations['org_secret_scanning_defaults'] = organization_defaults(org_res,('secret_scanning_enabled_for_new_repositories','secret_scanning_push_protection_enabled_for_new_repositories'))
        observations['org_ghas_defaults'] = get(f'{org_base}/code-security/configurations/defaults')
        observations['org_rulesets'] = get_paginated(f'{org_base}/rulesets', max_pages=max_pages)

        if include_enterprise:
            ent = enterprise_slug or os.environ.get('GITHUB_ENTERPRISE')
            if ent:
                observations['enterprise'] = get(f'/enterprises/{ent}')
                observations['enterprise_actions_permissions'] = get(f'/enterprises/{ent}/actions/permissions')
            else:
                observations['enterprise'] = {'status': 'NOT_ASSESSED', 'reason': 'Enterprise slug not specified', 'data': None, 'complete': False, 'truncated': False}

        snap['observed_at'] = now()
        return snap

    # Repository target collection
    if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', target):
        raise ValueError('Invalid repository')

    base = '/repos/' + target
    observations['repository'] = get(base)
    snap = {
        'target': target,
        'target_revision': None,
        'target_type': 'repository',
        'observed_at': now(),
        'observations': observations,
    }
    if observations['repository']['status'] != 'OK':
        return snap

    repo_data = observations['repository']['data']
    if not isinstance(repo_data, dict) or not isinstance(repo_data.get('owner'), dict) or not isinstance(repo_data['owner'].get('login'), str) or not isinstance(repo_data.get('default_branch'), str):
        observations['repository'] = {'status': 'ERROR', 'reason': 'Invalid repository payload', 'data': None, 'complete': False, 'truncated': False}
        return snap
    owner = repo_data['owner']['login']
    branch = ref or repo_data['default_branch']
    head = get(base + '/git/ref/heads/' + urllib.parse.quote(branch, safe=''))
    if head['status'] != 'OK':
        observations['head'] = head
        return snap
    ref_data = head['data']
    if not isinstance(ref_data, dict) or not isinstance(ref_data.get('object'), dict) or not re.fullmatch(r'[a-fA-F0-9]{40}', str(ref_data['object'].get('sha', ''))):
        observations['head'] = {'status': 'ERROR', 'reason': 'Invalid git reference payload', 'data': None, 'complete': False, 'truncated': False}
        return snap
    sha = ref_data['object']['sha']
    snap['target_revision'] = sha
    snap['target_branch'] = branch
    observations['effective_branch_rules'] = get(base + '/rules/branches/' + urllib.parse.quote(branch, safe=''))
    tree = get(base + '/git/trees/' + sha + '?recursive=1')
    if tree['status'] != 'OK':
        observations['files'] = tree
        return snap

    files = {}
    if not isinstance(tree['data'], dict) or not isinstance(tree['data'].get('tree'), list) or any(not isinstance(x, dict) or not all(isinstance(x.get(k), str) for k in ('path', 'type', 'sha')) for x in tree['data']['tree']):
        observations['files'] = {'status': 'ERROR', 'reason': 'Invalid git tree payload', 'data': None, 'complete': False, 'truncated': False}
        return snap
    complete = not tree['data'].get('truncated', False)
    candidates = [x for x in tree['data']['tree'] if x['type'] == 'blob' and
                  (x['path'].startswith('.github/') or '/' not in x['path'] or x['path'].startswith('docs/') or x['path'].endswith(('/action.yml', '/action.yaml')))]
    filtered = [e for e in candidates if e['path'].endswith(('.md', '.yml', '.yaml', '.cff')) or e['path'] in {'LICENSE', 'CODEOWNERS', '.github/CODEOWNERS', 'docs/CODEOWNERS'}]
    if len(filtered) > max_files:
        complete = False
    for entry in filtered[:max_files]:
        path = entry['path']
        if entry.get('mode') == '120000':
            files[path] = {'kind': 'symlink'}
            continue
        b = get(base + '/git/blobs/' + entry['sha'])
        if b['status'] != 'OK':
            complete = False
            continue
        try:
            if not isinstance(b['data'], dict) or b['data'].get('encoding') not in {None, 'base64'}:
                complete = False
                continue
            files[path] = {'content': base64.b64decode(b['data']['content']).decode('utf-8'), 'blob_sha': entry['sha']}
        except (KeyError, TypeError, UnicodeDecodeError, ValueError):
            complete = False

    observations['files'] = {
        'status': 'OK',
        'complete': complete,
        'truncated': not complete,
        'data': files,
        'scope': 'Root files, .github, docs and all local action manifests; sufficient only for bundled file/workflow checks',
    }

    # Repository-level security features with full/capped pagination
    observations['dependabot_alerts'] = get_paginated(base + '/dependabot/alerts?state=open', max_pages=max_pages)
    observations['code_scanning_alerts'] = get_paginated(base + '/code-scanning/alerts?state=open', max_pages=max_pages)
    observations['secret_scanning_alerts'] = get_paginated(base + '/secret-scanning/alerts?state=open', max_pages=max_pages)
    observations['deploy_keys'] = get_paginated(base + '/keys', max_pages=max_pages)

    pinned_ref = '?ref=' + urllib.parse.quote(sha, safe='')
    observations['codeowners'] = get(base + '/contents/.github/CODEOWNERS' + pinned_ref)
    if observations['codeowners']['status'] == 'HTTP_ERROR' and observations['codeowners']['http_status'] == 404:
        observations['codeowners'] = get(base + '/contents/CODEOWNERS' + pinned_ref)
    if observations['codeowners']['status'] == 'HTTP_ERROR' and observations['codeowners']['http_status'] == 404:
        observations['codeowners'] = get(base + '/contents/docs/CODEOWNERS' + pinned_ref)

    observations['dependabot_config'] = get(base + '/contents/.github/dependabot.yml' + pinned_ref)
    if observations['dependabot_config']['status'] == 'HTTP_ERROR' and observations['dependabot_config']['http_status'] == 404:
        observations['dependabot_config'] = get(base + '/contents/.github/dependabot.yaml' + pinned_ref)

    observations['actions_permissions'] = get(base + '/actions/permissions')
    observations['actions_permissions_workflow'] = get(base + '/actions/permissions/workflow')

    if include_org:
        observations['organization'] = get(f'/orgs/{owner}')
        if observations['organization']['status'] == 'OK':
            observations['org_members'] = get_paginated(f'/orgs/{owner}/members', max_pages=max_pages)
            observations['org_teams'] = get_paginated(f'/orgs/{owner}/teams', max_pages=max_pages)
            observations['org_actions_permissions'] = get(f'/orgs/{owner}/actions/permissions')
            observations['org_actions_permissions_workflow'] = get(f'/orgs/{owner}/actions/permissions/workflow')
            observations['org_actions_permissions_repositories'] = get_paginated(f'/orgs/{owner}/actions/permissions/repositories', max_pages=max_pages)
            observations['org_dependabot_defaults'] = organization_defaults(observations['organization'],('dependabot_alerts_enabled_for_new_repositories','dependabot_security_updates_enabled_for_new_repositories'))
            observations['org_secret_scanning_defaults'] = organization_defaults(observations['organization'],('secret_scanning_enabled_for_new_repositories','secret_scanning_push_protection_enabled_for_new_repositories'))
            observations['org_ghas_defaults'] = get(f'/orgs/{owner}/code-security/configurations/defaults')
            observations['org_rulesets'] = get_paginated(f'/orgs/{owner}/rulesets', max_pages=max_pages)
        else:
            observations['org_members'] = {'status': 'NOT_ASSESSED', 'reason': f'Owner {owner} is not an organization or inaccessible', 'data': None, 'complete': False, 'truncated': False}
            observations['org_teams'] = {'status': 'NOT_ASSESSED', 'reason': f'Owner {owner} is not an organization or inaccessible', 'data': None, 'complete': False, 'truncated': False}

    if include_enterprise:
        ent = enterprise_slug or os.environ.get('GITHUB_ENTERPRISE')
        if ent:
            observations['enterprise'] = get(f'/enterprises/{ent}')
            observations['enterprise_actions_permissions'] = get(f'/enterprises/{ent}/actions/permissions')
        else:
            observations['enterprise'] = {'status': 'NOT_ASSESSED', 'reason': 'Enterprise slug not specified', 'data': None, 'complete': False, 'truncated': False}

    snap['observed_at'] = now()
    return snap
