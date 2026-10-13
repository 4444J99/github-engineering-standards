"""Per-page/function and structured-source review queues.
These are extraction work items, not accepted canonical controls.
"""
from __future__ import annotations
from collections import Counter,defaultdict
import gzip,hashlib,json,re
from pathlib import Path
from .core import digest,dump,load
from .yamlutil import parse


def structured_rows(record: dict, artifact: dict) -> list[dict]:
    """Reproduce source-defined occurrences without accepting their policy."""
    text, path, repo = record['content'], record['path'], record['source']
    if hashlib.sha256(text.encode()).hexdigest() != artifact['sha256']:
        raise ValueError('Ledger source content hash mismatch: ' + path)
    rows = []
    base = dict(artifact_id=artifact['artifact_id'], source=repo,
                commit=record['commit'], path=path, review_status='UNREVIEWED',
                adopted_obligation=None, canonical_control_ids=[],
                verification_binding='manual_source_disposition', license='MIT')
    lines = text.splitlines()
    if repo == 'microsoft/ghqr' and path.startswith('internal/recommendations/definitions/') and path.endswith('.yaml'):
        definitions = parse(text)
        if not isinstance(definitions, list):
            raise ValueError('Unexpected GHQR definition format')
        starts = [i for i, line in enumerate(lines, 1) if re.match(r'^-\s*id:', line)]
        for definition in definitions:
            start = next((i for i, line in enumerate(lines, 1)
                          if re.match(r'\s*-\s*id:\s*' + re.escape(definition['id']) + r'\s*$', line)), 1)
            end = next((n - 1 for n in starts if n > start), len(lines))
            rows.append({**base, 'requirement_id': 'SRC-GHQR-' + definition['id'],
                         'line': start, 'source_definition': definition,
                         'start_line': start, 'end_line': end,
                         'content_sha256': artifact['sha256'],
                         'span_sha256': hashlib.sha256('\n'.join(lines[start-1:end]).encode()).hexdigest()})
    if repo == 'github/github-well-architected' and path.startswith('content/library/') and path.endswith('/checklist.md'):
        heading = []
        for number, line in enumerate(lines, 1):
            title = re.match(r'^(#{1,6})\s+(.+)', line)
            if title and not title[2].startswith('SPDX-License-Identifier:'):
                heading = heading[:len(title[1])-1] + [title[2]]
            match = re.match(r'^\s*-\s+(.+)', line)
            if not match or match[1].endswith((':', ':**')):
                continue
            rows.append({**base, 'requirement_id': 'SRC-WA-' + digest([path, number, match[1]])[:16],
                         'line': number, 'function': ' / '.join(heading),
                         'source_statement': match[1], 'start_line': number, 'end_line': number,
                         'content_sha256': artifact['sha256'],
                         'span_sha256': hashlib.sha256(line.encode()).hexdigest()})
    return rows


def enrich(snapshots: Path, corpus: Path, controls: list[dict]) -> dict:
    artifacts=[json.loads(l) for l in (corpus/'artifacts.jsonl').read_text().splitlines()]
    idx={(r['source'],r['commit'],r['path']):r for r in artifacts};mdpages={};dependencies=[];structured=[]
    for p in snapshots.glob('*.text.jsonl.gz'):
        with gzip.open(p,'rt',encoding='utf-8') as f:
            for line in f:
                r=json.loads(line);text=r['content'];path=r['path'];repo=r['source'];commit=r['commit'];a=idx[(repo,commit,path)]
                if hashlib.sha256(text.encode()).hexdigest() != a.get('sha256'):
                    raise ValueError('Ledger source content hash mismatch: '+path)
                if path.endswith(('.md','.mdx')):
                    for m in re.finditer(r'(?:data\s+|data\.)(reusables|variables)\.([\w.-]+)',text):
                        ref=m[2];kind=m[1];paths=[]
                        if kind=='reusables':paths=['data/reusables/'+ref.replace('.','/')+x for x in ('.md','.yml','.yaml')]
                        else:
                            parts=ref.split('.');paths=['data/variables/'+('/'.join(parts[:n]))+x for n in range(1,len(parts)) for x in ('.yml','.yaml')]
                        matches=[idx[(repo,commit,p)] for p in paths if (repo,commit,p) in idx]
                        dependencies.append({'artifact_id':a['artifact_id'],'kind':kind,'reference':ref,'source_line':text[:m.start()].count('\n')+1,'resolved_artifact_ids':[v['artifact_id'] for v in matches],'resolution':'PATH_MATCH' if matches else 'UNRESOLVED','value_or_conditional_rendering_verified':False})
                    for m in re.finditer(r'{%\s*(ifversion|elsif|include|if|unless)\s+([^%]+)%}',text):
                        dependencies.append({'artifact_id':a['artifact_id'],'kind':m[1],'reference':m[2].strip(),'source_line':text[:m.start()].count('\n')+1,'resolution':'RENDER_REQUIRED','resolved_artifact_ids':[]})
                if repo=='github/docs' and path.startswith('content/') and path.endswith('.md'):
                    meta={};error=None
                    if text.startswith('---\n'):
                        front=text[4:].split('\n---',1)[0]
                        try:meta=parse(front) or {}
                        except Exception as exc:error=type(exc).__name__
                    title=meta.get('title',Path(path).stem) if isinstance(meta,dict) else Path(path).stem
                    mdpages[path]={'artifact_id':a['artifact_id'],'source_path':path,'function':title,'versions':meta.get('versions',{}) if isinstance(meta,dict) else {},'frontmatter_error':error,'candidate_count':a['candidate_count'],'semantic_review':'UNREVIEWED','canonical_control_ids':[c['id'] for c in controls if any(s['repository']==repo and s['path']==path for s in c['sources'])]}
                structured.extend(structured_rows(r, a))
    with (corpus/'dependencies.jsonl').open('w') as f:
        for r in dependencies:f.write(json.dumps(r,sort_keys=True)+'\n')
    dump(corpus/'docs-source-pages.json',list(mdpages.values()))
    dump(corpus/'structured-source-requirements.json',structured)
    page_versions=[]
    for p in sorted(snapshots.glob('docs-pages-*.txt')):
        version=p.name[len('docs-pages-'):-len('.txt')]
        for path in p.read_text().splitlines():
            bits=path.strip('/').split('/');tail=bits[2:] if len(bits)>1 and '@' in bits[1] else bits[1:]
            stem='/'.join(tail);candidates=['content/'+stem+'.md','content/'+stem+'/index.md'] if stem else ['content/index.md']
            matches=[mdpages[k] for k in candidates if k in mdpages]
            page_versions.append({'page_id':digest([version,path])[:24],'version':version,'path':path,'source_matches':[m['artifact_id'] for m in matches],'function':matches[0]['function'] if matches else stem,'reconciliation':'SOURCE_PATH_MATCH' if matches else 'GENERATED_OR_UNRESOLVED','rendered_body_review':'UNREVIEWED','review_checklist':{'page_source_reviewed':False,'all_actionable_claims_extracted':False,'claims_mapped_or_excluded':False,'implementation_bound':False,'verification_evidence_current':False}})
    dump(corpus/'published-page-ledger.json',page_versions)
    pages=['# Per-page function review ledger','','Each row is one published English page-version instance. Unchecked stages are not complete.','', '| Version | Function | Published path | Source mapping | Extract / reconcile / verify |','|---|---|---|---|---|']
    pages += [f'| {r["version"]} | {str(r["function"]).replace("|","/")} | `{r["path"]}` | {r["reconciliation"]} | [ ] / [ ] / [ ] |' for r in page_versions]
    (corpus/'page-function-checklist.md').write_text('\n'.join(pages)+'\n')
    matrix=[]
    for a in artifacts:
        mapped=[c['id'] for c in controls if any(s['repository']==a['source'] and s['path']==a['path'] for s in c['sources'])]
        matrix.append({'artifact_id':a['artifact_id'],'source':a['source'],'path':a['path'],'canonical_controls':mapped,'all_unique_information_consolidated':False,'generalization_review':'PENDING','license_review':'PENDING' if a['source']=='tmcw/github-best-practices' else 'PER_FILE_REVIEW_REQUIRED'})
    dump(corpus/'source-consolidation-matrix.json',matrix)
    summary={'docs_source_markdown_files':len(mdpages),'published_page_version_instances':len(page_versions),'published_source_path_matches':sum(bool(x['source_matches']) for x in page_versions),'generated_or_unresolved_page_instances':sum(not x['source_matches'] for x in page_versions),'structured_source_requirements':len(structured),'structured_requirements_by_source':dict(Counter(r['source'] for r in structured)),'dependency_references':len(dependencies),'dependencies_with_path_match':sum(r['resolution']=='PATH_MATCH' for r in dependencies),'source_artifacts_referenced_by_canonical_controls':sum(bool(r['canonical_controls']) for r in matrix),'full_semantic_review_complete':False}
    dump(corpus/'ledger-summary.json',summary);return summary
