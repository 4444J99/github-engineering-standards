"""Read-only checks. Passing file existence is never a semantic quality claim."""
from __future__ import annotations
import re
from .core import MISSING, lookup


def endpoint(snapshot: dict, name: str):
    value=snapshot.get('observations',{}).get(name)
    if value is None: return None,('NOT_ASSESSED',f'No observation for {name}')
    if value.get('status')!='OK':
        return None,('ERROR',f'{name}: {value.get("status","UNKNOWN")} (HTTP {value.get("http_status","unknown")})')
    if 'data' not in value: return None,('ERROR',f'{name}: missing data')
    return value['data'],None


def file_exists(snapshot: dict, paths: list[str]):
    files,err=endpoint(snapshot,'files')
    if err: return err
    for path in paths:
        if path in files:
            value=files[path]
            if isinstance(value,dict) and value.get('kind')=='symlink':
                return 'MANUAL_REVIEW',f'{path} is a symlink; target not established'
            text=value.get('content') if isinstance(value,dict) else value
            if isinstance(text,str) and text.strip(): return 'PASS',f'Nonempty file verified: {path}'
    if not snapshot.get('observations',{}).get('files',{}).get('complete',False):
        return 'NOT_VERIFIABLE','File inventory incomplete; absence cannot be established'
    return 'FAIL','No nonempty file at an accepted location: '+', '.join(paths)


def workflows(snapshot: dict):
    files,err=endpoint(snapshot,'files')
    if err: return [],err
    result=[]
    try:
        import yaml
        from .yamlutil import parse
    except ImportError:
        return [],('ERROR','PyYAML is required for workflow checks')
    for path,value in files.items():
        if path.startswith('.github/workflows/') and path.endswith(('.yml','.yaml')):
            if path.count('/') != 2:
                continue
            text=value.get('content') if isinstance(value,dict) else value
            if not isinstance(text,str): return [],('ERROR',f'Missing workflow content: {path}')
            try: data=parse(text)
            except yaml.YAMLError: return [],('FAIL',f'Invalid YAML: {path}')
            if not isinstance(data,dict): return [],('FAIL',f'Workflow is not an object: {path}')
            result.append((path,data))
    if not snapshot.get('observations',{}).get('files',{}).get('complete',False):
        return [],('NOT_VERIFIABLE','Workflow inventory incomplete')
    if not result: return [],('FAIL','Actions-enabled profile has no workflow files')
    return result,None


def execute(control: dict, snapshot: dict, context: dict) -> tuple[str,str]:
    spec=control['verification']; kind=spec['kind']
    if kind=='manual': return 'MANUAL_REVIEW','Requires a scoped, current attestation from an authorized reviewer'
    if kind=='file_present': return file_exists(snapshot,spec['paths'])
    if kind in {'metadata_nonempty','repo_name'}:
        repo,err=endpoint(snapshot,'repository')
        if err: return err
        key=spec.get('field','name'); value=lookup(repo,key)
        if value is MISSING: return 'NOT_VERIFIABLE',f'Repository field unavailable: {key}'
        if kind=='repo_name':
            ok=isinstance(value,str) and bool(re.fullmatch('[a-z0-9]+(?:-[a-z0-9]+)*',value)) and len(value)<=100
        else: ok=bool(value.strip()) if isinstance(value,str) else bool(value)
        return ('PASS' if ok else 'FAIL'),f'Observed metadata field {key}: {value!r}'
    if kind=='effective_rule':
        rules,err=endpoint(snapshot,'effective_branch_rules')
        if err: return err
        if not isinstance(rules,list): return 'ERROR','Effective branch rules must be an array'
        matches=[r for r in rules if r.get('type')==spec['rule_type']]
        if not matches:
            return 'NOT_VERIFIABLE','Requested active ruleset rule not observed; legacy branch protection is not assessed by this checker'
        param=spec.get('parameter')
        if not param: return 'PASS',f'Active branch rules API returned {spec["rule_type"]}'
        expected=spec.get('value')
        if 'profile_parameter' in spec:
            expected=lookup(context,spec['profile_parameter'])
            if expected is MISSING: return 'NOT_VERIFIABLE','Missing rule policy parameter'
        for rule in matches:
            observed=lookup(rule.get('parameters',{}),param)
            if observed is MISSING: continue
            if spec.get('operator')=='at_least':
                ok=type(observed) is int and type(expected) is int and observed>=expected
            else: ok=type(observed) is type(expected) and observed==expected
            if ok: return 'PASS',f'Active {spec["rule_type"]}.{param} satisfies profile; bypass policy requires separate review'
        return 'FAIL',f'Observed {spec["rule_type"]} does not satisfy parameter {param}'
    if kind in {'workflow_permissions','workflow_pinning'}:
        entries,err=workflows(snapshot)
        if err: return err
        failures=[]
        for path,wf in entries:
            if kind=='workflow_permissions':
                p=wf.get('permissions',MISSING)
                ok=p=='read-all' or isinstance(p,dict) and all(v in ('read','none') for v in p.values())
                if not ok: failures.append(path+': default permissions are absent or not read-only')
                continue
            jobs=wf.get('jobs',{})
            if not isinstance(jobs,dict): return 'FAIL',path+': invalid jobs'
            for name,job in jobs.items():
                if not isinstance(job,dict): return 'FAIL',path+': invalid job'
                uses=[job['uses']] if 'uses' in job else []
                steps=job.get('steps',[])
                if not isinstance(steps,list): return 'FAIL',path+': invalid steps'
                uses += [s['uses'] for s in steps if isinstance(s,dict) and 'uses' in s]
                for use in uses:
                    if not isinstance(use,str): failures.append(path+': non-string uses'); continue
                    if use.startswith('./'):
                        if '..' in use.split('/'): failures.append(path+': unsafe local action path')
                        continue
                        local_path=use[2:]
                        if local_path in files:
                            local_text=files[local_path].get('content') if isinstance(files[local_path],dict) else files[local_path]
                            if isinstance(local_text,str):
                                try:
                                    local_data=parse(local_text)
                                    if isinstance(local_data,dict):
                                        local_steps=local_data.get('steps') or local_data.get('jobs',{}).values()
                                        for item in local_steps:
                                            if isinstance(item,dict):
                                                luse=item.get('uses')
                                                if luse:
                                                    if not isinstance(luse,str): failures.append(path+': non-string uses in composite'); continue
                                                    if luse.startswith('./'):
                                                        if '..' in luse.split('/'): failures.append(path+': unsafe nested local action path')
                                                    elif luse.startswith('docker://'):
                                                        if not re.fullmatch(r'docker://[^\s]+@sha256:[a-f0-9]{64}',luse): failures.append(path+': unpinned image in composite '+luse)
                                                    elif not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.\-/]+@[a-f0-9]{40}',luse):
                                                        failures.append(path+': action/workflow not pinned to a full SHA in composite: '+luse)
                                except yaml.YAMLError:
                                    failures.append(path+': invalid YAML in local composite action')
                    elif use.startswith('docker://'):
                        if not re.fullmatch(r'docker://[^\s]+@sha256:[a-f0-9]{64}',use): failures.append(path+': unpinned image '+use)
                    elif not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.\-/]+@[a-f0-9]{40}',use):
                        failures.append(path+': action/workflow not pinned to a full SHA: '+use)
        if failures: return 'FAIL','; '.join(failures)
        return 'PASS',f'{len(entries)} workflow files satisfy the syntactic {kind} check; execution and permission adequacy are separate controls'
    if kind=='dependabot_config':
        return dependabot_config(snapshot)
    if kind=='actions_permissions':
        return actions_permissions(snapshot)
    if kind=='deploy_keys':
        return deploy_keys(snapshot)
    if kind=='codeowners_validation':
        return codeowners_validation(snapshot)
    if kind=='code_scanning_alerts':
        return code_scanning_alerts(snapshot)
    if kind=='secret_scanning_alerts':
        return secret_scanning_alerts(snapshot)
    if kind=='dependabot_alerts':
        return dependabot_alerts(snapshot)
    return 'ERROR','Unknown verification kind'


def dependabot_config(snapshot: dict):
    data,err=endpoint(snapshot,'dependabot_config')
    if err:
        if err[0] == 'ERROR' and 'HTTP 404' in err[1]:
            return 'FAIL','No dependabot.yml or dependabot.yaml found'
        return err
    return 'PASS','Dependabot configuration file present'


def actions_permissions(snapshot: dict):
    data,err=endpoint(snapshot,'actions_permissions')
    if err: return err
    enabled=data.get('enabled',False)
    allowed=data.get('allowed_actions','all')
    if not enabled:
        return 'FAIL','GitHub Actions is disabled'
    if allowed=='all':
        return 'FAIL','All third-party actions are allowed'
    return 'PASS',f'GitHub Actions enabled with allowed_actions={allowed}'


def deploy_keys(snapshot: dict):
    data,err=endpoint(snapshot,'deploy_keys')
    if err: return err
    keys=data
    if not keys:
        return 'PASS','No deploy keys configured'
    issues=[]
    for key in keys:
        if key.get('read_only') is False:
            issues.append(f'Deploy key {key.get("key","?")[:20]}... has write access')
        if not key.get('verified',True):
            issues.append(f'Deploy key {key.get("key","?")[:20]}... is unverified')
    if issues:
        return 'FAIL','; '.join(issues)
    return 'PASS',f'{len(keys)} deploy keys verified as read-only and verified'


def codeowners_validation(snapshot: dict):
    data,err=endpoint(snapshot,'codeowners')
    if err:
        if err[0] == 'ERROR' and 'HTTP 404' in err[1]:
            return 'FAIL','No CODEOWNERS file found'
        return err
    content=data.get('content','')
    if not content:
        return 'FAIL','CODEOWNERS file is empty'
    try:
        import base64
        decoded=base64.b64decode(content).decode('utf-8')
    except Exception:
        return 'FAIL','CODEOWNERS content could not be decoded'
    lines=decoded.splitlines()
    valid_lines=0
    for line in lines:
        line=line.strip()
        if not line or line.startswith('#'):
            continue
        if re.match(r'^[\w\*\-\.\/\[\]]*\s+@[\w\-/]+',line):
            valid_lines+=1
        elif re.match(r'^[\w\*\-\.\/\[\]]*\s+[\w\-]+@[\w\-]+',line):
            valid_lines+=1
    if valid_lines==0:
        return 'FAIL','CODEOWNERS has no valid ownership patterns'
    return 'PASS',f'CODEOWNERS has {valid_lines} valid ownership patterns'


def code_scanning_alerts(snapshot: dict):
    data,err=endpoint(snapshot,'code_scanning_alerts')
    if err:
        if err[0] == 'ERROR' and 'HTTP 403' in err[1]:
            return 'MANUAL_REVIEW','Code scanning alerts access requires GHAS or organization admin'
        return err
    alerts=data
    if not alerts:
        return 'PASS','No open code scanning alerts'
    critical=sum(1 for a in alerts if a.get('rule',{}).get('severity')=='critical')
    high=sum(1 for a in alerts if a.get('rule',{}).get('severity')=='high')
    return 'FAIL',f'{len(alerts)} open code scanning alerts ({critical} critical, {high} high)'


def secret_scanning_alerts(snapshot: dict):
    data,err=endpoint(snapshot,'secret_scanning_alerts')
    if err:
        if err[0] == 'ERROR' and 'HTTP 403' in err[1]:
            return 'MANUAL_REVIEW','Secret scanning alerts access requires GHAS or organization admin'
        return err
    alerts=data
    if not alerts:
        return 'PASS','No open secret scanning alerts'
    return 'FAIL',f'{len(alerts)} open secret scanning alerts'


def dependabot_alerts(snapshot: dict):
    data,err=endpoint(snapshot,'dependabot_alerts')
    if err:
        if err[0] == 'ERROR' and 'HTTP 403' in err[1]:
            return 'MANUAL_REVIEW','Dependabot alerts access requires security access'
        return err
    alerts=data
    if not alerts:
        return 'PASS','No open Dependabot alerts'
    critical=sum(1 for a in alerts if a.get('security_advisory',{}).get('severity')=='critical')
    high=sum(1 for a in alerts if a.get('security_advisory',{}).get('severity')=='high')
    return 'FAIL',f'{len(alerts)} open Dependabot alerts ({critical} critical, {high} high)'
