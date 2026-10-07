"""Read-only checks. Passing file existence is never a semantic quality claim."""
from __future__ import annotations
import re
from .core import MISSING, lookup


def endpoint(snapshot: dict, name: str):
    value=snapshot.get('observations',{}).get(name)
    if value is None: return None,('NOT_ASSESSED',f'No observation for {name}')
    if not isinstance(value, dict): return None,('ERROR',f'{name}: observation must be an object')
    if value.get('status')!='OK':
        return None,('ERROR',f'{name}: {value.get("status","UNKNOWN")} (HTTP {value.get("http_status","unknown")})')
    if 'data' not in value: return None,('ERROR',f'{name}: missing data')
    if value.get('data') is None: return None,('ERROR',f'{name}: payload data is null')
    if value.get('complete') is False and name != 'files': return None,('NOT_VERIFIABLE',f'{name}: observation is incomplete')
    return value['data'],None


def file_exists(snapshot: dict, paths: list[str]):
    files,err=endpoint(snapshot,'files')
    if err: return err
    if not isinstance(files, dict): return 'ERROR','File inventory payload must be a dictionary'
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
    if not isinstance(files, dict): return [],('ERROR','File inventory payload must be an object')
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
            if isinstance(value, dict) and value.get('kind') == 'symlink':
                return [], ('MANUAL_REVIEW', f'{path} is a symlink; target not established')
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


def workflow_shape_error(wf: dict) -> str | None:
    """Check the job/step shapes consumed below, not the complete platform schema."""
    jobs = wf.get('jobs')
    if not isinstance(jobs, dict) or not jobs:
        return 'invalid or empty jobs'
    for name, job in jobs.items():
        if not isinstance(job, dict):
            return f'invalid job {name}'
        if 'uses' in job:
            if 'steps' in job or 'runs-on' in job or not isinstance(job['uses'], str) or not job['uses'].strip():
                return f'invalid reusable workflow job {name}'
            continue
        steps = job.get('steps')
        if not isinstance(steps, list) or not steps:
            return f'job {name} has no nonempty steps or reusable workflow'
        for step in steps:
            if not isinstance(step, dict) or ('run' in step) == ('uses' in step):
                return f'job {name} step must contain exactly one of run or uses'
            command = step.get('run', step.get('uses'))
            if not isinstance(command, str) or not command.strip():
                return f'job {name} step command must be a nonempty string'
    return None


def permission_shape(permissions) -> str:
    """Known scope syntax; unknown future scopes require review rather than a pass."""
    if isinstance(permissions, str):
        return 'VALID' if permissions in {'read-all', 'write-all'} else 'INVALID'
    if not isinstance(permissions, dict):
        return 'INVALID'
    known = {'actions', 'artifact-metadata', 'attestations', 'checks', 'code-quality',
             'contents', 'deployments', 'discussions', 'id-token', 'issues', 'packages',
             'pages', 'pull-requests', 'security-events', 'statuses', 'vulnerability-alerts'}
    for key, value in permissions.items():
        allowed = {'read', 'write', 'none'}
        if key == 'id-token':
            allowed = {'write', 'none'}
        elif key == 'vulnerability-alerts':
            allowed = {'read', 'none'}
        if not isinstance(key, str) or not isinstance(value, str) or value not in allowed:
            return 'INVALID'
    return 'UNKNOWN' if set(permissions) - known else 'VALID'


def execute(control: dict, snapshot: dict, context: dict) -> tuple[str,str]:
    spec=control['verification']; kind=spec['kind']
    if kind=='manual': return 'MANUAL_REVIEW','Requires a scoped, current attestation from an authorized reviewer'
    if kind=='file_present': return file_exists(snapshot,spec['paths'])
    if kind in {'metadata_nonempty','repo_name'}:
        repo,err=endpoint(snapshot,'repository')
        if err: return err
        if not isinstance(repo, dict): return 'ERROR','Repository payload must be an object'
        key=spec.get('field','name'); value=lookup(repo,key)
        if value is MISSING: return 'NOT_VERIFIABLE',f'Repository field unavailable: {key}'
        if kind=='repo_name':
            ok=isinstance(value,str) and bool(re.fullmatch('[a-z0-9]+(?:-[a-z0-9]+)*',value)) and len(value)<=100
        elif 'value' in spec:
            ok=value==spec['value']
        elif isinstance(value,bool):
            ok=(value is True)
        elif isinstance(value,str):
            ok=bool(value.strip())
        elif isinstance(value,(list,dict,set)):
            ok=len(value)>0
        elif isinstance(value,(int,float)):
            ok=value>0
        else: ok=bool(value.strip()) if isinstance(value,str) else bool(value)
        return ('PASS' if ok else 'FAIL'),f'Observed metadata field {key}: {value!r}'
    if kind=='effective_rule':
        rules,err=endpoint(snapshot,'effective_branch_rules')
        if err: return err
        if not isinstance(rules,list): return 'ERROR','Effective branch rules must be an array'
        if any(not isinstance(r, dict) for r in rules): return 'ERROR','Effective branch rule entries must be objects'
        matches=[r for r in rules if r.get('type')==spec['rule_type']]
        if not matches:
            return 'NOT_VERIFIABLE','Requested active ruleset rule not observed; legacy branch protection is not assessed by this checker'
        if any('parameters' in r and not isinstance(r['parameters'],dict) for r in matches):
            return 'ERROR','Effective branch rule parameters must be an object'
        if spec['rule_type'] == 'required_status_checks':
            check_lists=[r.get('parameters',{}).get('required_status_checks') for r in matches]
            if any(not isinstance(checks,list) for checks in check_lists):
                return 'ERROR','Required status checks must be an array'
            if any(not isinstance(c,dict) or not isinstance(c.get('context'),str)
                   for checks in check_lists for c in checks):
                return 'ERROR','Required status check entries must identify a string context'
            if any(not c['context'].strip() for checks in check_lists for c in checks):
                return 'FAIL','Required status check context is empty'
        param=spec.get('parameter')
        if not param:
            if spec['rule_type'] == 'required_status_checks':
                has_checks = any(bool(r.get('parameters',{}).get('required_status_checks')) for r in matches)
                if not has_checks:
                    return 'FAIL','Active required_status_checks rule has no status checks configured'
            return 'PASS',f'Active branch rules API returned {spec["rule_type"]}'
        expected=spec.get('value')
        if 'profile_parameter' in spec:
            prof_val=lookup(context,spec['profile_parameter'])
            if prof_val is not MISSING:
                expected=prof_val
            elif expected is None:
                return 'NOT_VERIFIABLE','Missing rule policy parameter'
        if spec.get('operator')=='at_least' and type(expected) is int and expected < 0:
            return 'ERROR','Minimum rule policy parameter cannot be negative'
        for rule in matches:
            observed=lookup(rule.get('parameters',{}),param)
            if observed is MISSING: continue
            if spec.get('operator')=='at_least':
                if type(observed) is int and type(expected) is int:
                    ok = observed >= expected
                elif isinstance(observed, list) and type(expected) is int:
                    ok = len(observed) >= expected
                else:
                    ok = False
            elif expected is not None:
                if isinstance(observed, list) and isinstance(expected, list):
                    observed_contexts = {c.get('context') if isinstance(c, dict) else c for c in observed}
                    ok = all(exp in observed_contexts for exp in expected)
                elif isinstance(expected, bool):
                    ok = type(observed) is bool and observed is expected
                else:
                    ok = type(observed) is type(expected) and observed == expected
            else:
                ok = len(observed) > 0 if isinstance(observed, list) else bool(observed)
            if ok: return 'PASS',f'Active {spec["rule_type"]}.{param} satisfies profile; bypass policy requires separate review'
        return 'FAIL',f'Observed {spec["rule_type"]} does not satisfy parameter {param}'
    if kind in {'workflow_permissions','workflow_pinning'}:
        entries,err=workflows(snapshot)
        if err: return err
        files_data=snapshot.get('observations',{}).get('files',{}).get('data',{})
        failures=[]
        reviews=[]

        def check_composite_action(action_ref: str, origin: str, visited: set[str]):
            if not isinstance(action_ref, str):
                failures.append(f'{origin}: non-string uses')
                return
            if action_ref.startswith('./'):
                parts = action_ref.split('/')
                if '..' in parts:
                    failures.append(f'{origin}: unsafe local action path {action_ref}')
                    return
                norm_rel = '/'.join(p for p in parts if p and p != '.')
                if norm_rel in visited:
                    failures.append(f'{origin}: cyclic local action/workflow dependency {action_ref}')
                    return
                visited.add(norm_rel)
                candidates = [norm_rel + '/action.yml', norm_rel + '/action.yaml', norm_rel]
                found_path = None
                for c_path in candidates:
                    if isinstance(files_data, dict) and c_path in files_data:
                        found_path = c_path
                        break
                if not found_path:
                    if not snapshot.get('observations',{}).get('files',{}).get('complete',False):
                        failures.append(f'{origin}: local action not found (file inventory incomplete): {action_ref}')
                    else:
                        failures.append(f'{origin}: local action path not found: {action_ref}')
                    return
                entry = files_data[found_path]
                if isinstance(entry, dict) and entry.get('kind') == 'symlink':
                    reviews.append(f'{origin}: local dependency {found_path} is a symlink; target not established')
                    return
                text = entry.get('content') if isinstance(entry, dict) else entry
                if not isinstance(text, str):
                    failures.append(f'{origin}: local action file missing content: {found_path}')
                    return
                try:
                    import yaml
                    from .yamlutil import parse
                    local_doc = parse(text)
                except Exception:
                    failures.append(f'{origin}: invalid YAML in local composite action: {found_path}')
                    return
                if not isinstance(local_doc, dict):
                    failures.append(f'{origin}: local composite action is not an object: {found_path}')
                    return
                if found_path.startswith('.github/workflows/'):
                    shape_error = workflow_shape_error(local_doc)
                    if shape_error:
                        failures.append(f'{origin}: {found_path}: {shape_error}')
                        return
                    nested_jobs = local_doc.get('jobs')
                    if not isinstance(nested_jobs, dict) or not nested_jobs:
                        failures.append(f'{origin}: invalid local reusable workflow jobs: {found_path}')
                        return
                    for nested_job in nested_jobs.values():
                        if not isinstance(nested_job, dict):
                            failures.append(f'{origin}: invalid local reusable workflow job: {found_path}')
                            continue
                        if 'uses' in nested_job:
                            check_composite_action(nested_job['uses'], found_path, visited.copy())
                        nested_steps = nested_job.get('steps', [])
                        if not isinstance(nested_steps, list) or (not nested_steps and 'uses' not in nested_job):
                            failures.append(f'{origin}: invalid local reusable workflow steps: {found_path}')
                            continue
                        for nested_step in nested_steps:
                            if not isinstance(nested_step, dict) or not ('uses' in nested_step or 'run' in nested_step):
                                failures.append(f'{origin}: invalid local reusable workflow step: {found_path}')
                            elif 'uses' in nested_step:
                                check_composite_action(nested_step['uses'], found_path, visited.copy())
                    return
                runs = local_doc.get('runs', {})
                if not isinstance(runs, dict) or not isinstance(runs.get('using'), str):
                    failures.append(f'{origin}: invalid local action runs manifest: {found_path}')
                    return
                if runs['using'] != 'composite':
                    if runs['using'] == 'docker':
                        image = runs.get('image')
                        if isinstance(image, str) and image.startswith('docker://'):
                            check_composite_action(image, found_path, visited)
                        elif image != 'Dockerfile':
                            failures.append(f'{origin}: invalid or unpinned Docker image: {found_path}')
                    elif not re.fullmatch(r'node\d+', runs['using']) or not isinstance(runs.get('main'), str):
                        failures.append(f'{origin}: invalid local action runtime: {found_path}')
                    return
                steps = runs.get('steps', []) if isinstance(runs, dict) else []
                if not steps and 'steps' in local_doc:
                    steps = local_doc.get('steps', [])
                if not isinstance(steps, list) or not steps:
                    failures.append(f'{origin}: composite action must have nonempty steps: {found_path}')
                    return
                if isinstance(steps, list):
                    for step in steps:
                        if not isinstance(step, dict) or ('uses' in step) == ('run' in step):
                            failures.append(f'{origin}: invalid composite step: {found_path}')
                        elif not isinstance(step.get('uses', step.get('run')), str) or not step.get('uses', step.get('run')).strip():
                            failures.append(f'{origin}: empty or non-string composite step: {found_path}')
                        if isinstance(step, dict) and 'uses' in step:
                            check_composite_action(step['uses'], f'{origin} -> {found_path}', visited.copy())
            elif action_ref.startswith('docker://'):
                if not re.fullmatch(r'docker://[^\s]+@sha256:[a-f0-9]{64}', action_ref):
                    failures.append(f'{origin}: unpinned image {action_ref}')
            elif not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.\-/]+@[a-f0-9]{40}', action_ref):
                failures.append(f'{origin}: action/workflow not pinned to a full SHA: {action_ref}')

        for path,wf in entries:
            shape_error = workflow_shape_error(wf)
            if shape_error:
                failures.append(f'{path}: {shape_error}')
                continue
            if kind=='workflow_permissions':
                p=wf.get('permissions',MISSING)
                shape = permission_shape(p)
                if shape == 'INVALID':
                    failures.append(path+': invalid or absent default permissions')
                    continue
                if shape == 'UNKNOWN':
                    reviews.append(path+': unsupported default permission scope requires review')
                ok=p=='read-all' or isinstance(p,dict) and all(v in ('read','none') for v in p.values())
                if not ok: failures.append(path+': default permissions are absent or not read-only')
                jobs=wf.get('jobs',{})
                if not isinstance(jobs,dict): return 'FAIL',path+': invalid jobs'
                for name,job in jobs.items():
                    if not isinstance(job,dict): return 'FAIL',path+': invalid job'
                    if 'permissions' in job:
                        jp=job['permissions']
                        shape = permission_shape(jp)
                        if shape == 'INVALID':
                            failures.append(f'{path}: job {name} has invalid permission syntax')
                            continue
                        if shape == 'UNKNOWN':
                            reviews.append(f'{path}: job {name} has unsupported permission scope')
                        if not (jp=='read-all' or isinstance(jp,dict) and all(v in ('read','none') for v in jp.values())):
                            reviews.append(f'{path}: job {name} elevated permissions require scoped justification; OIDC issuance is not repository write authority')
                continue
            jobs=wf.get('jobs',{})
            if not isinstance(jobs,dict) or not jobs: return 'FAIL',path+': invalid jobs'
            for name,job in jobs.items():
                if not isinstance(job,dict): return 'FAIL',path+': invalid job'
                uses=[job['uses']] if 'uses' in job else []
                steps=job.get('steps',[])
                if not isinstance(steps,list): return 'FAIL',path+': invalid steps'
                if any(not isinstance(s, dict) or not ('uses' in s or 'run' in s) for s in steps):
                    return 'FAIL',path+': invalid step'
                if not uses and not steps: return 'FAIL',path+': job has neither steps nor reusable workflow'
                uses += [s['uses'] for s in steps if isinstance(s,dict) and 'uses' in s]
                for use in uses:
                    check_composite_action(use, path, set())
        if failures: return 'FAIL','; '.join(failures)
        if reviews: return 'MANUAL_REVIEW','; '.join(reviews)
        if kind == 'workflow_pinning' and spec.get('require_provenance_review') is True:
            return 'MANUAL_REVIEW', ('Reference syntax satisfies immutability formatting, but action commit origin, '
                                     'container provenance and safe-update review have not been verified')
        return 'PASS',f'{len(entries)} workflow files satisfy the syntactic {kind} check; execution and permission adequacy are separate controls'
    if kind=='dependabot_config':
        return dependabot_config(snapshot, spec)
    if kind=='actions_permissions':
        return actions_permissions(snapshot, spec)
    if kind=='deploy_keys':
        return deploy_keys(snapshot, spec)
    if kind=='codeowners_validation':
        return codeowners_validation(snapshot)
    if kind=='code_scanning_alerts':
        return code_scanning_alerts(snapshot, spec)
    if kind=='secret_scanning_alerts':
        return secret_scanning_alerts(snapshot, spec)
    if kind=='dependabot_alerts':
        return dependabot_alerts(snapshot, spec)
    return 'ERROR','Unknown verification kind'


def dependabot_config(snapshot: dict, spec: dict | None = None):
    data,err=endpoint(snapshot,'dependabot_config')
    if err:
        if err[0] == 'ERROR' and 'HTTP 404' in err[1]:
            return 'FAIL','No dependabot.yml or dependabot.yaml found'
        return err
    if not isinstance(data, dict):
        return 'ERROR','Dependabot config payload must be an object'
    if data.get('type') == 'dir':
        return 'FAIL','Dependabot config path is a directory, not a file'
    content = data.get('content')
    if not isinstance(content, str) or not content.strip():
        return 'FAIL','Dependabot configuration file is empty'
    encoding = data.get('encoding', 'base64')
    if encoding == 'base64':
        try:
            import base64
            decoded = base64.b64decode(content).decode('utf-8')
        except Exception:
            return 'FAIL','Dependabot configuration base64 decoding failed'
    else:
        decoded = content
    try:
        import yaml
        from .yamlutil import parse
        cfg = parse(decoded)
    except Exception:
        return 'FAIL','Invalid YAML in Dependabot configuration'
    if not isinstance(cfg, dict):
        return 'FAIL','Dependabot configuration must be a mapping'
    version = cfg.get('version')
    if version != 2 and version != '2':
        return 'FAIL',f'Dependabot configuration version must be 2, got {version!r}'
    updates = cfg.get('updates')
    if updates is not None:
        if not isinstance(updates, list):
            return 'FAIL','Dependabot updates must be an array'
        if len(updates) == 0:
            return 'FAIL','Dependabot updates array is empty'
    if updates is None:
        return 'FAIL','Dependabot configuration missing updates array'
    for update in updates:
        if not isinstance(update, dict) or not isinstance(update.get('package-ecosystem'), str) or not isinstance(update.get('directory'), str):
            return 'FAIL','Dependabot update entries require ecosystem and directory'
        schedule = update.get('schedule')
        if not isinstance(schedule, dict) or schedule.get('interval') not in {'daily', 'weekly', 'monthly', 'quarterly', 'semiannually', 'yearly'}:
            return 'FAIL','Dependabot update entries require a valid schedule'
    return 'PASS','Dependabot configuration file present'


def actions_permissions(snapshot: dict, spec: dict | None = None):
    spec = spec or {}
    param = spec.get('parameter') or spec.get('check')
    if param == 'default_workflow_permissions' or spec.get('endpoint') == 'actions_permissions_workflow' or spec.get('require_read_permissions'):
        data, err = endpoint(snapshot, 'actions_permissions_workflow')
        if err:
            data, err = endpoint(snapshot, 'org_actions_permissions_workflow')
            if err:
                return err
        if not isinstance(data, dict):
            return 'ERROR', 'actions_permissions_workflow payload must be an object'
        perm = data.get('default_workflow_permissions')
        if not perm:
            return 'FAIL', 'default_workflow_permissions not configured'
        expected_perm = spec.get('value', 'read')
        if perm != expected_perm:
            return 'FAIL', f'Default workflow permission is {perm!r}, expected {expected_perm!r}'
        can_approve = data.get('can_approve_pull_request_reviews')
        if type(can_approve) is not bool:
            return 'NOT_VERIFIABLE', 'Workflow review approval permission is unavailable or malformed'
        if can_approve is True and spec.get('disallow_can_approve', True):
            return 'FAIL', 'GitHub Actions workflows can approve pull request reviews'
        return 'PASS', f'Default workflow permissions restricted to {perm}'

    data,err=endpoint(snapshot,'actions_permissions')
    if err:
        data,err=endpoint(snapshot,'org_actions_permissions')
        if err: return err
    if not isinstance(data, dict):
        return 'ERROR', 'actions_permissions payload must be an object'
    enabled=data.get('enabled',False)
    allowed=data.get('allowed_actions','all')
    if enabled is not True:
        return 'FAIL','GitHub Actions is disabled'
    if spec.get('policy') == 'selected_only':
        if allowed != 'selected':
            return 'FAIL', f'Allowed actions is {allowed!r}, expected selected'
        return 'PASS', 'GitHub Actions restricted to selected actions'
    if allowed=='all':
        return 'FAIL','All third-party actions are allowed'
    if allowed not in {'local_only', 'selected'}:
        return 'ERROR', 'Allowed actions policy is absent or malformed'
    expected_allowed = spec.get('value')
    if expected_allowed and allowed != expected_allowed:
        return 'FAIL', f'Allowed actions is {allowed!r}, expected {expected_allowed!r}'
    return 'PASS',f'GitHub Actions enabled with allowed_actions={allowed}'


def deploy_keys(snapshot: dict, spec: dict | None = None):
    data,err=endpoint(snapshot,'deploy_keys')
    if err: return err
    if not isinstance(data, list):
        return 'ERROR', 'Deploy keys payload must be a list'
    if snapshot['observations']['deploy_keys'].get('complete') is not True:
        return 'NOT_VERIFIABLE', 'Deploy key inventory completeness is not established'
    if not data:
        return 'PASS','No deploy keys configured'
    issues=[]
    for key in data:
        if not isinstance(key, dict):
            return 'ERROR', 'Deploy key entry must be an object'
        key_id = str(key.get('id') or key.get('key') or '?')[:20]
        if key.get('read_only') is False:
            issues.append(f'Deploy key {key_id}... has write access')
        elif key.get('read_only') is not True:
            issues.append(f'Deploy key {key_id}... is not strictly read-only')
        if key.get('verified') is not True:
            issues.append(f'Deploy key {key_id}... is not strictly verified')
    if issues:
        return 'FAIL','; '.join(issues)
    return 'PASS',f'{len(data)} deploy keys verified as read-only and verified'


def codeowners_validation(snapshot: dict):
    data,err=endpoint(snapshot,'codeowners')
    if err:
        if err[0] == 'ERROR' and 'HTTP 404' in err[1]:
            return 'FAIL','No CODEOWNERS file found'
        return err
    if not isinstance(data, dict): return 'ERROR','CODEOWNERS payload must be an object'
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


def code_scanning_alerts(snapshot: dict, spec: dict | None = None):
    data,err=endpoint(snapshot,'code_scanning_alerts')
    if err:
        if err[0] == 'ERROR' and 'HTTP 403' in err[1]:
            return 'MANUAL_REVIEW','Code scanning alerts access requires GHAS or organization admin'
        return err
    if not isinstance(data, list):
        return 'ERROR', 'Code scanning alerts payload must be a list'
    if any(not isinstance(a, dict) or not isinstance(a.get('rule'), dict) for a in data):
        return 'ERROR', 'Code scanning alert entries require rule objects'
    if snapshot['observations']['code_scanning_alerts'].get('complete') is not True:
        return 'NOT_VERIFIABLE', 'Code scanning alert inventory completeness is not established'
    spec = spec or {}
    check = spec.get('check') or ('configuration' if spec.get('require_configured') else None)
    if check == 'configuration':
        entries, workflow_error = workflows(snapshot)
        if workflow_error: return workflow_error
        has_codeql = False
        for _, wf in entries:
            jobs = wf.get('jobs', {})
            if isinstance(jobs, dict):
                for job in jobs.values():
                    if isinstance(job, dict):
                        steps = job.get('steps', [])
                        if isinstance(steps, list):
                            for s in steps:
                                if isinstance(s, dict) and re.fullmatch(r'github/codeql-action/(?:init|analyze)@[^\s]+', str(s.get('uses', ''))):
                                    has_codeql = True
                                    break
        if not has_codeql:
            return 'FAIL', 'Code scanning (CodeQL) is not configured; no CodeQL workflow found'
        return 'NOT_VERIFIABLE', 'CodeQL workflow syntax observed; recent successful analysis and pull-request coverage are not collected'
    severity = spec.get('severity')
    if severity == 'critical':
        if any(a['rule'].get('security_severity_level') not in {'critical', 'high', 'medium', 'low'} for a in data):
            return 'NOT_VERIFIABLE', 'Code scanning security severity is unavailable'
        crit = sum(1 for a in data if a['rule'].get('security_severity_level') == 'critical')
        if crit > 0:
            return 'FAIL', f'{crit} open critical code scanning alerts'
        return 'PASS', 'No open critical code scanning alerts'
    elif severity == 'high':
        if any(a['rule'].get('security_severity_level') not in {'critical', 'high', 'medium', 'low'} for a in data):
            return 'NOT_VERIFIABLE', 'Code scanning security severity is unavailable'
        high = sum(1 for a in data if a['rule'].get('security_severity_level') in {'critical', 'high'})
        if high > 0:
            return 'FAIL', f'{high} open high code scanning alerts'
        return 'PASS', 'No open high code scanning alerts'
    alerts=data
    if not alerts:
        return 'PASS','No open code scanning alerts'
    critical=sum(1 for a in alerts if isinstance(a, dict) and a.get('rule',{}).get('severity')=='critical')
    high=sum(1 for a in alerts if isinstance(a, dict) and a.get('rule',{}).get('severity')=='high')
    return 'FAIL',f'{len(alerts)} open code scanning alerts ({critical} critical, {high} high)'


def secret_scanning_alerts(snapshot: dict, spec: dict | None = None):
    data,err=endpoint(snapshot,'secret_scanning_alerts')
    if err:
        if err[0] == 'ERROR' and 'HTTP 403' in err[1]:
            return 'MANUAL_REVIEW','Secret scanning alerts access requires GHAS or organization admin'
        return err
    if not isinstance(data, list):
        return 'ERROR', 'Secret scanning alerts payload must be a list'
    if any(not isinstance(a, dict) for a in data): return 'ERROR', 'Secret scanning alert entries must be objects'
    if snapshot['observations']['secret_scanning_alerts'].get('complete') is not True:
        return 'NOT_VERIFIABLE', 'Secret scanning alert inventory completeness is not established'
    alerts=data
    if not alerts:
        return 'PASS','No open secret scanning alerts'
    return 'FAIL',f'{len(alerts)} open secret scanning alerts'


def dependabot_alerts(snapshot: dict, spec: dict | None = None):
    data,err=endpoint(snapshot,'dependabot_alerts')
    if err:
        if err[0] == 'ERROR' and 'HTTP 403' in err[1]:
            return 'MANUAL_REVIEW','Dependabot alerts access requires security access'
        return err
    if not isinstance(data, list):
        return 'ERROR', 'Dependabot alerts payload must be a list'
    if any(not isinstance(a, dict) or not isinstance(a.get('security_advisory'), dict) for a in data):
        return 'ERROR', 'Dependabot alert entries require security advisory objects'
    if snapshot['observations']['dependabot_alerts'].get('complete') is not True:
        return 'NOT_VERIFIABLE', 'Dependabot alert inventory completeness is not established'
    spec = spec or {}
    check = spec.get('check') or ('enablement' if spec.get('check_enablement') else None)
    if check == 'enablement':
        repo = snapshot.get('observations', {}).get('repository', {}).get('data', {})
        sec = repo.get('security_and_analysis', {}) if isinstance(repo, dict) else {}
        dep_status = sec.get('dependabot_security_updates', {}).get('status')
        has_alerts = len(data) > 0
        obs = snapshot.get('observations', {}).get('dependabot_alerts', {})
        is_enabled = obs.get('enabled') is True or dep_status == 'enabled' or has_alerts
        if not is_enabled:
            return 'FAIL', 'Dependabot alerts enablement not verified; empty alert list does not prove feature is active'
        return 'PASS', 'Dependabot alerts verified as enabled'
    severity = spec.get('severity')
    if severity and any(a['security_advisory'].get('severity') not in {'critical', 'high', 'moderate', 'low'} for a in data):
        return 'NOT_VERIFIABLE', 'Dependabot alert severity is unavailable'
    if severity == 'critical':
        crit = sum(1 for a in data if isinstance(a, dict) and a.get('security_advisory', {}).get('severity') == 'critical')
        if crit > 0:
            return 'FAIL', f'{crit} open critical Dependabot alerts'
        return 'PASS', 'No open critical Dependabot alerts'
    elif severity == 'high':
        high = sum(1 for a in data if a['security_advisory'].get('severity') in {'critical', 'high'})
        if high > 0:
            return 'FAIL', f'{high} open high Dependabot alerts'
        return 'PASS', 'No open high Dependabot alerts'
    alerts=data
    if not alerts:
        return 'PASS','No open Dependabot alerts'
    critical=sum(1 for a in alerts if isinstance(a, dict) and a.get('security_advisory',{}).get('severity')=='critical')
    high=sum(1 for a in alerts if isinstance(a, dict) and a.get('security_advisory',{}).get('severity')=='high')
    return 'FAIL',f'{len(alerts)} open Dependabot alerts ({critical} critical, {high} high)'
