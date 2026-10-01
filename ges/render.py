"""Generate human checklists and templates from canonical control definitions."""
from __future__ import annotations
import re
import json
from pathlib import Path
from .core import dump, digest, safe_path


def generate(controls: list[dict], output: Path) -> None:
    output.mkdir(parents=True,exist_ok=True)
    lines=['# GitHub Engineering Standards — functional checklist','',
           'Version 0.1.0 — reviewed draft controls, not an exhaustive source consolidation.',
           'Check a box only when scoped, current evidence satisfies the stated criterion.','']
    for cat in sorted({c['category'] for c in controls}):
        lines += ['## '+cat.replace('-',' ').title(),'']
        for c in controls:
            if c['category']!=cat: continue
            lines += [f'- [ ] **{c["id"]} r{c["revision"]} — {c["title"]}** ({c["obligation"]}; {c["status"]})',
                      '  '+c['objective'],
                      '  Acceptance: '+'; '.join(c['implementation']['acceptance']),
                      '  Verification: `'+c['verification']['kind']+'`; scope: '+c['scope']+'.',
                      '  Applicability: `'+str(c['applicability'])+'`.',
                      '  Evidence: target, revision, observation time, evidence reference, result, reviewer when required.','']
    (output/'functional-checklist.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    rows=['# Control-to-source crosswalk','', '| Control | Revision | Source artifact | Section |','|---|---|---|---|']
    for c in controls:
        for s in c['sources']:
            url=f'https://github.com/{s["repository"]}/blob/{s["commit"]}/{s["path"]}'
            rows.append(f'| {c["id"]} | {c["revision"]} | [{s["repository"]}:{s["path"]}]({url}) | {s["section"]} |')
    (output/'source-crosswalk.md').write_text('\n'.join(rows)+'\n',encoding='utf-8')
    dump(output/'bindings.json',{'catalog_digest':digest(controls),'controls':[
        {'id':c['id'],'revision':c['revision'],'checker':c['verification'],
         'template':c['implementation'].get('template'), 'enforcement':c['enforcement'],
         'measurement':c['measurement']} for c in controls]})


def render_template(root: Path, template: str, parameters: dict, destination: Path) -> None:
    text=safe_path(root,template).read_text(encoding='utf-8')
    keys=set(re.findall(r'\{\{([A-Z][A-Z0-9_]*)\}\}',text))
    missing=keys-parameters.keys()
    if missing: raise ValueError('Missing parameters: '+', '.join(sorted(missing)))
    for key in keys:
        value=parameters[key]
        if not isinstance(value,str) or not value.strip() or '\x00' in value: raise ValueError('Invalid parameter: '+key)
        text=text.replace('{{'+key+'}}',value)
    if re.search(r'\{\{[A-Z][A-Z0-9_]*\}\}',text): raise ValueError('Unresolved template parameters')
    if template.endswith('.json'):
        json.loads(text)
    elif template.endswith(('.yml','.yaml','.cff')):
        from .yamlutil import parse
        parse(text)
    if destination.exists(): raise FileExistsError('Refusing to overwrite '+str(destination))
    destination.parent.mkdir(parents=True,exist_ok=True)
    destination.write_text(text,encoding='utf-8')
