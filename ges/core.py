"""Strict data contracts. No executable expressions or source-code evaluation."""
from __future__ import annotations
import datetime as dt
import hashlib
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUTCOMES = {'PASS','FAIL','PARTIAL','NOT_ASSESSED','MANUAL_REVIEW','NOT_VERIFIABLE','ERROR','STALE'}
MISSING = object()


def load(path: str | Path) -> Any:
    return json.loads(Path(path).read_text(encoding='utf-8'))


def dump(path: str | Path, data: Any) -> None:
    p = Path(path); p.parent.mkdir(parents=True, exist_ok=True)
    temp = p.with_suffix(p.suffix+'.tmp')
    temp.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True)+'\n', encoding='utf-8')
    temp.replace(p)


def now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def timestamp(value: str) -> dt.datetime:
    value = dt.datetime.fromisoformat(value.replace('Z','+00:00'))
    if value.tzinfo is None: raise ValueError('Timestamp must have an explicit timezone')
    return value.astimezone(dt.timezone.utc)


def digest(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',',':')).encode()).hexdigest()


def lookup(data: Any, path: str) -> Any:
    for key in path.split('.'):
        if not isinstance(data, dict) or key not in data: return MISSING
        data = data[key]
    return data


def safe_path(root: Path, relative: str) -> Path:
    if not isinstance(relative,str) or not relative or '\\' in relative:
        raise ValueError('Invalid relative path')
    p = Path(relative)
    if p.is_absolute() or '..' in p.parts: raise ValueError('Unsafe relative path')
    target=(root/p).resolve()
    if not target.is_relative_to(root.resolve()): raise ValueError('Path escapes root')
    return target


def validate_controls(controls: list[dict], root: Path = ROOT) -> list[str]:
    errors=[]; seen=set()
    supported={'file_present','metadata_nonempty','repo_name','workflow_permissions',
               'workflow_pinning','effective_rule','manual','dependabot_config',
               'actions_permissions','deploy_keys','codeowners_validation',
               'code_scanning_alerts','secret_scanning_alerts','dependabot_alerts'}
    checker_fields={
        'file_present': {'paths'},
        'metadata_nonempty': {'field'},
        'repo_name': set(),
        'workflow_permissions': set(),
        'workflow_pinning': set(),
        'effective_rule': {'rule_type'},
        'manual': set(),
        'dependabot_config': set(),
        'actions_permissions': set(),
        'deploy_keys': set(),
        'codeowners_validation': set(),
        'code_scanning_alerts': set(),
        'secret_scanning_alerts': set(),
        'dependabot_alerts': set(),
    }
    for c in controls:
        cid=c.get('id','<missing>')
        if cid in seen: errors.append(f'{cid}: duplicate ID')
        seen.add(cid)
        if not re.fullmatch(r'GES-[A-Z]{2,8}-[0-9]{3}',cid): errors.append(f'{cid}: invalid ID')
        for key in ('revision','title','objective','category','scope','obligation','applicability',
                    'sources','verification','implementation','enforcement','measurement','remediation','status'):
            if key not in c: errors.append(f'{cid}: missing {key}')
        if type(c.get('revision')) is not int or c.get('revision',0)<1: errors.append(f'{cid}: bad revision')
        if c.get('obligation') not in {'MUST','SHOULD','MAY'}: errors.append(f'{cid}: bad obligation')
        if c.get('status') not in {'PROPOSED','REVIEWED_DRAFT','ACCEPTED','RETIRED'}: errors.append(f'{cid}: bad status')
        vkind=c.get('verification',{}).get('kind')
        if vkind not in supported: errors.append(f'{cid}: unsupported checker')
        else:
            required=checker_fields.get(vkind,set())
            for rf in required:
                if rf not in c.get('verification',{}): errors.append(f'{cid}: verification missing required field {rf}')
        if c.get('scope') not in {'repository','organization','enterprise','workflow','release','person'}: errors.append(f'{cid}: invalid scope')
        for src in c.get('sources',[]):
            if not all(src.get(k) for k in ('repository','commit','path','section')): errors.append(f'{cid}: incomplete provenance')
            if not re.fullmatch('[a-f0-9]{40}',src.get('commit','')): errors.append(f'{cid}: unpinned source')
        if not c.get('sources'): errors.append(f'{cid}: no source provenance')
        if not c.get('implementation',{}).get('acceptance'): errors.append(f'{cid}: no acceptance criteria')
        t=c.get('implementation',{}).get('template')
        if t:
            try:
                if not safe_path(root,t).is_file(): errors.append(f'{cid}: missing template {t}')
            except ValueError: errors.append(f'{cid}: unsafe template path')
    return errors


def applicable(control: dict, context: dict) -> tuple[str,str]:
    """Missing profile dimensions stay UNKNOWN; no truthiness conversion."""
    conditions=control.get('applicability',{})
    for key, expected in conditions.items():
        actual=lookup(context,key)
        if actual is MISSING: return 'UNKNOWN',f'Missing applicability dimension: {key}'
        if isinstance(expected,list): matches=actual in expected
        else: matches=type(actual) is type(expected) and actual==expected
        if not matches: return 'NOT_APPLICABLE_WITH_REASON',f'{key}={actual!r} does not match {expected!r}'
    return 'APPLICABLE','All declared applicability predicates satisfied'
