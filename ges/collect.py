"""Bounded GitHub read adapter. Tokens stay on api.github.com; no writes."""
from __future__ import annotations
import base64
import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request
from .core import now


def collect(repository: str, *, max_files: int=2000, include_org: bool=False, include_enterprise: bool=False) -> dict:
    if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+',repository): raise ValueError('Invalid repository')
    token=os.environ.get('GH_TOKEN') or os.environ.get('GITHUB_TOKEN')
    def get(path):
        headers={'Accept':'application/vnd.github+json','User-Agent':'github-engineering-standards/0.1'}
        if token: headers['Authorization']='Bearer '+token
        try:
            req=urllib.request.Request('https://api.github.com'+path,headers=headers)
            with urllib.request.urlopen(req,timeout=30) as r:
                raw=r.read(20_000_001)
                if len(raw)>20_000_000: return {'status':'ERROR','reason':'Response too large'}
                return {'status':'OK','http_status':200,'data':json.loads(raw)}
        except urllib.error.HTTPError as exc: return {'status':'HTTP_ERROR','http_status':exc.code}
        except (urllib.error.URLError,TimeoutError,ValueError): return {'status':'ERROR','reason':'Transport or decoding failure'}
    base='/repos/'+repository; observations={}; observations['repository']=get(base)
    snap={'target':repository,'target_revision':None,'target_type':'repository','observed_at':now(),'observations':observations}
    if observations['repository']['status']!='OK': return snap
    owner=observations['repository']['data']['owner']['login']
    branch=observations['repository']['data']['default_branch']
    ref=get(base+'/git/ref/heads/'+urllib.parse.quote(branch,safe=''))
    if ref['status']!='OK': observations['head']=ref; return snap
    sha=ref['data']['object']['sha']; snap['target_revision']=sha
    observations['effective_branch_rules']=get(base+'/rules/branches/'+urllib.parse.quote(branch,safe=''))
    tree=get(base+'/git/trees/'+sha+'?recursive=1')
    if tree['status']!='OK': observations['files']=tree; return snap
    files={}; complete=not tree['data'].get('truncated',False)
    candidates=[x for x in tree['data']['tree'] if x['type']=='blob' and
                (x['path'].startswith('.github/') or '/' not in x['path'] or x['path'].startswith('docs/'))]
    filtered=[e for e in candidates if e['path'].endswith(('.md','.yml','.yaml','.cff')) or e['path'] in {'LICENSE','CODEOWNERS','.github/CODEOWNERS','docs/CODEOWNERS'}]
    if len(filtered)>max_files: complete=False
    for entry in filtered[:max_files]:
        path=entry['path']
        if entry.get('mode')=='120000': files[path]={'kind':'symlink'}; continue
        b=get(base+'/git/blobs/'+entry['sha'])
        if b['status']!='OK': complete=False; continue
        try:
            files[path]={'content':base64.b64decode(b['data']['content']).decode('utf-8'),'blob_sha':entry['sha']}
        except (KeyError,UnicodeDecodeError,ValueError): complete=False
    observations['files']={'status':'OK','complete':complete,'data':files,
                           'scope':'Root files, .github, docs; sufficient only for bundled file/workflow checks'}
    
    # Repository-level security features
    observations['dependabot_alerts']=get(base+'/dependabot/alerts?state=open&per_page=1')
    observations['code_scanning_alerts']=get(base+'/code-scanning/alerts?state=open&per_page=1')
    observations['secret_scanning_alerts']=get(base+'/secret-scanning/alerts?state=open&per_page=1')
    observations['deploy_keys']=get(base+'/keys')
    observations['codeowners']=get(base+'/contents/.github/CODEOWNERS')
    if observations['codeowners']['status']=='HTTP_ERROR' and observations['codeowners']['http_status']==404:
        observations['codeowners']=get(base+'/contents/CODEOWNERS')
    if observations['codeowners']['status']=='HTTP_ERROR' and observations['codeowners']['http_status']==404:
        observations['codeowners']=get(base+'/contents/docs/CODEOWNERS')
    observations['dependabot_config']=get(base+'/contents/.github/dependabot.yml')
    if observations['dependabot_config']['status']=='HTTP_ERROR' and observations['dependabot_config']['http_status']==404:
        observations['dependabot_config']=get(base+'/contents/.github/dependabot.yaml')
    observations['actions_permissions']=get(base+'/actions/permissions')
    observations['actions_permissions_workflow']=get(base+'/actions/permissions/workflow')
    
    if include_org:
        observations['organization']=get(f'/orgs/{owner}')
        observations['org_members']=get(f'/orgs/{owner}/members?per_page=1')
        observations['org_teams']=get(f'/orgs/{owner}/teams?per_page=1')
        observations['org_actions_permissions']=get(f'/orgs/{owner}/actions/permissions')
        observations['org_actions_permissions_workflow']=get(f'/orgs/{owner}/actions/permissions/workflow')
        observations['org_actions_permissions_repositories']=get(f'/orgs/{owner}/actions/permissions/repositories')
        observations['org_dependabot_defaults']=get(f'/orgs/{owner}/dependabot/defaults')
        observations['org_secret_scanning_defaults']=get(f'/orgs/{owner}/secret-scanning/defaults')
        observations['org_ghas_defaults']=get(f'/orgs/{owner}/security-configuration/defaults')
    
    if include_enterprise:
        # Enterprise endpoints require enterprise slug; skip if not available
        pass
    
    snap['observed_at']=now()
    return snap
