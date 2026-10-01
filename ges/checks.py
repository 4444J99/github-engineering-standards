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
                    elif use.startswith('docker://'):
                        if not re.fullmatch(r'docker://[^\s]+@sha256:[a-f0-9]{64}',use): failures.append(path+': unpinned image '+use)
                    elif not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.\-/]+@[a-f0-9]{40}',use):
                        failures.append(path+': action/workflow not pinned to a full SHA: '+use)
        if failures: return 'FAIL','; '.join(failures)
        return 'PASS',f'{len(entries)} workflow files satisfy the syntactic {kind} check; execution and permission adequacy are separate controls'
    return 'ERROR','Unknown verification kind'
