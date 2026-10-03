"""Corpus accounting, conservative candidate extraction, and review ledgers.
Discovery is not semantic review. Never execute imported source instructions.
"""
from __future__ import annotations
import gzip
import hashlib
import json
import re
from collections import Counter,defaultdict
from pathlib import Path
from .core import ROOT, dump, digest, load, timestamp, now


def classify(path: str) -> str:
    p=path.lower()
    name=Path(p).name
    if name in {'license','license.md','license.txt','license.rst','notice','notice.md','notice.txt','copying','copying.md','copying.txt','copyright','copyright.md','copyright.txt'}: return 'license'
    if name in {'citation.cff','funding.yml'} or 'template' in name: return 'template'
    if '/test/' in p or p.startswith('test/') or name.startswith('test_') or name.endswith('_test.py'): return 'test'
    if p.startswith('data/reusables/'): return 'reusable'
    if p.startswith('content/') or p.endswith(('.md','.mdx','.rst')): return 'documentation'
    if p.endswith(('.yaml','.yml','.json','.toml','.ini','.cfg')): return 'configuration'
    if p.endswith(('.py','.go','.js','.ts','.tsx','.sh','.mjs')): return 'implementation'
    return 'supporting_asset'


def blocks(text: str):
    """Inventory every nonblank prose/list/table block and each code fence.
    Markdown is not fully rendered: includes and conditionals are recorded separately.
    """
    lines=text.splitlines(); heading=[]; buffer=[]; start=0; fence=None
    def record(end):
        return {'start_line':start,'end_line':end,'section':' / '.join(heading) or '(preamble)',
                'text':'\n'.join(buffer),'kind':'code_example' if fence else 'candidate'}
    for n,line in enumerate(lines,1):
        marker=re.match(r'^\s*(`{3,}|~{3,})',line)
        if marker:
            if fence is None:
                if buffer: yield record(n-1); buffer=[]
                fence=marker.group(1)[0]; start=n; buffer=[line]
            elif marker.group(1)[0]==fence:
                buffer.append(line); yield record(n); buffer=[]; fence=None
            else: buffer.append(line)
            continue
        if fence:
            buffer.append(line); continue
        h=re.match(r'^(#{1,6})\s+(.+)',line)
        if h:
            if buffer: yield record(n-1); buffer=[]
            level=len(h.group(1)); heading=heading[:level-1]+[h.group(2)]
            continue
        boundary=not line.strip() or bool(re.match(r'^\s*(?:[-*+]\s|\d+[.)]\s|\|)',line))
        if boundary and buffer: yield record(n-1); buffer=[]
        if line.strip():
            if not buffer: start=n
            buffer.append(line)
    if buffer: yield record(len(lines))


def build_corpus(snapshot_dir: Path, output: Path, *, include_restricted_text: bool=False) -> dict:
    output.mkdir(parents=True,exist_ok=True)
    inventories=[]; candidates=[]; dependencies=[]; source_counts={}
    for p in sorted(snapshot_dir.glob('*.inventory.json')):
        data=load(p)
        for row in data:
            row['artifact_id']=digest([row['source'],row['commit'],row['path']])[:24]
            row['proposed_disposition']=classify(row['path'])
            row['review_status']='UNREVIEWED'; inventories.append(row)
    idx={(r['source'],r['commit'],r['path']):r for r in inventories}
    for p in sorted(snapshot_dir.glob('*.text.jsonl.gz')):
        with gzip.open(p,'rt',encoding='utf-8') as f:
            for line in f:
                raw=json.loads(line); key=(raw['source'],raw['commit'],raw['path']); row=idx.get(key)
                if row is None: raise ValueError('Text artifact absent from inventory')
                content=raw['content']
                if hashlib.sha256(content.encode()).hexdigest()!=row.get('sha256'):
                    raise ValueError('Source content hash mismatch: '+raw['path'])
                if raw['path'].endswith(('.md','.mdx','.rst')):
                    for b in blocks(content):
                        b.update(artifact_id=row['artifact_id'],source=raw['source'],commit=raw['commit'],path=raw['path'],
                                 review_status='UNREVIEWED',canonical_control_ids=[])
                        b['candidate_id']=digest([row['artifact_id'],b['start_line'],b['end_line'],b['text']])[:24]
                        b['text_sha256']=hashlib.sha256(b['text'].encode()).hexdigest()
                        b['normative_signal']=bool(re.search(r'\b(must|should|require|ensure|recommend|avoid|never)\b',b['text'],re.I))
                        b['reference']=row['url']+f'#L{b["start_line"]}-L{b["end_line"]}'
                        # Do not redistribute source expression by default; exact references
                        # and digests are sufficient to reproduce the reviewer queue locally.
                        if not include_restricted_text: b.pop('text')
                        candidates.append(b)
                    for match in re.finditer(r'data\.(reusables|variables)\.([\w.-]+)',content):
                        dependencies.append({'artifact_id':row['artifact_id'],'kind':match.group(1),'reference':match.group(2)})
    by_artifact=Counter(c['artifact_id'] for c in candidates)
    for r in inventories: r['candidate_count']=by_artifact[r['artifact_id']]
    for repo in sorted({r['source'] for r in inventories}):
        rs=[r for r in inventories if r['source']==repo]
        source_counts[repo]={'artifacts':len(rs),'retrieved':sum(r.get('retrieval_status')=='RETRIEVED' for r in rs),
                             'text':sum(r.get('kind')=='text' for r in rs),
                             'candidates':sum(by_artifact[r['artifact_id']] for r in rs),'semantically_reviewed':0}
    for name,records in [('artifacts',inventories),('candidates',candidates),('dependencies',dependencies)]:
        with (output/(name+'.jsonl')).open('w',encoding='utf-8') as f:
            for r in records: f.write(json.dumps(r,ensure_ascii=False,sort_keys=True)+'\n')
    groups=defaultdict(list)
    for c in candidates: groups[c['text_sha256']].append(c['candidate_id'])
    dump(output/'exact-duplicate-groups.json',[v for v in groups.values() if len(v)>1])
    report={'schema_version':'ges.corpus.v1','sources':source_counts,'semantic_review_complete':False,
            'source_files_are_not_rendered_pages':True,'candidate_extraction_is_not_exhaustive_claim_review':True,
            'total_artifacts':len(inventories),'total_candidates':len(candidates),
            'semantic_review_numerator':0,'semantic_review_denominator':len(inventories),
            'rendered_page_reconciliation':'PENDING','git_tree_reconciliation':'PENDING'}
    dump(output/'coverage.json',report)
    md=['# Source artifact review ledger','', 'Generated candidates are UNREVIEWED. This ledger is not a compliance certificate.','']
    for repo,stats in source_counts.items():
        md += ['## '+repo,'',f'Artifacts: {stats["artifacts"]}; candidates: {stats["candidates"]}; semantic review: 0/{stats["artifacts"]}.','',
               '| Path | Proposed disposition | Candidates | Review |','|---|---|---:|---|']
        for r in inventories:
            if r['source']==repo:
                md.append(f'| `{r["path"]}` | {r["proposed_disposition"]} | {r["candidate_count"]} | UNREVIEWED |')
        md.append('')
    (output/'source-ledger.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
    return report


def coverage_with_reviews(artifact_path: Path, review_path: Path, *, candidates: list[dict] | None=None,
                          controls: list[dict] | None=None, authorized_reviewers: list[str] | None=None,
                          evidence_root: Path | None=None) -> dict:
    artifacts=[json.loads(x) for x in artifact_path.read_text().splitlines() if x.strip()]
    reviews=load(review_path)
    by_id={a['artifact_id']:a for a in artifacts}; complete=set(); errors=[]
    candidate_index={c['candidate_id']:c for c in candidates or []}
    candidates_by_artifact = defaultdict(set)
    for candidate in candidates or []:
        candidates_by_artifact[candidate['artifact_id']].add(candidate['candidate_id'])
    control_index={c['id']:c for c in controls or []}
    reviewed_ids=set()
    evidence_base = (evidence_root or ROOT).resolve()
    checked_evidence = {}

    def valid_evidence(reference):
        # Validate advertised references only. Presence is not semantic truth.
        if not isinstance(reference, str) or not reference.strip():
            return False
        if reference in checked_evidence:
            return checked_evidence[reference]
        relative = Path(reference)
        valid = False
        if (not relative.is_absolute() and '..' not in relative.parts and
                relative.parts and relative.parts[0] == 'evidence' and
                relative.suffix == '.json'):
            target = evidence_base / relative
            try:
                symlink = any((evidence_base / Path(*relative.parts[:i])).is_symlink()
                              for i in range(1, len(relative.parts) + 1))
                if (not symlink and target.resolve().is_relative_to(evidence_base / 'evidence')
                        and target.is_file()):
                    document = json.loads(target.read_text(encoding='utf-8'))
                    valid = isinstance(document, (dict, list)) and bool(document)
            except (OSError, ValueError, UnicodeError, RuntimeError):
                valid = False
        checked_evidence[reference] = valid
        return valid
    for r in reviews:
        if not isinstance(r,dict): errors.append('Review record must be an object'); continue
        a=by_id.get(r.get('artifact_id'))
        if a is None: errors.append('Unknown reviewed artifact'); continue
        if a['artifact_id'] in reviewed_ids:
            complete.discard(a['artifact_id']); errors.append(a['path']+': duplicate review receipt'); continue
        reviewed_ids.add(a['artifact_id'])
        if r.get('commit')!=a['commit'] or r.get('content_sha256')!=a.get('sha256'):
            errors.append(a['path']+': review invalidated by content change'); continue
        if not all(r.get(k) for k in ('reviewer','reviewed_at','disposition','rationale')):
            errors.append(a['path']+': incomplete review record'); continue
        if r['reviewer'] not in (authorized_reviewers or []):
            errors.append(a['path']+': reviewer is not authorized'); continue
        try:
            if timestamp(r['reviewed_at']) > timestamp(now()): raise ValueError('Future review')
        except (ValueError,TypeError,AttributeError):
            errors.append(a['path']+': invalid review timestamp'); continue
        if r.get('all_claims_accounted_for') is not True:
            errors.append(a['path']+': claims not fully accounted for'); continue
        if r['disposition'] not in {'CONTROL_SOURCE','REFERENCE_ONLY','NO_ACTIONABLE_CONTENT','EXCLUDED_WITH_REASON','SUPERSEDED'}:
            errors.append(a['path']+': invalid disposition'); continue
        mappings=r.get('claim_mappings',[])
        if not isinstance(mappings,list) or (r['disposition']=='CONTROL_SOURCE' and not mappings):
            errors.append(a['path']+': missing claim mappings'); continue
        valid=True; mapped=set()
        for m in mappings:
            if not isinstance(m,dict):
                errors.append(a['path']+': claim mapping must identify a candidate and disposition'); valid=False; continue
            candidate=candidate_index.get(m.get('candidate_id'))
            if candidate is None or candidate['artifact_id'] != a['artifact_id'] or candidate.get('text_sha256')!=m.get('text_sha256'):
                errors.append(a['path']+': unknown or changed candidate mapping'); valid=False; continue
            if candidate['candidate_id'] in mapped:
                errors.append(a['path']+': duplicate candidate mapping'); valid=False
            mapped.add(candidate['candidate_id'])
            if m.get('disposition')=='CONTROL':
                c=control_index.get(m.get('control_id'))
                if c is None or c['revision']!=m.get('control_revision') or not any(
                        s['repository']==a['source'] and s['commit']==a['commit'] and s['path']==a['path'] for s in c['sources']):
                    errors.append(a['path']+': invalid control mapping or revision'); valid=False
            elif m.get('disposition') not in {'REFERENCE','NO_ACTIONABLE_CONTENT','EXCLUDED_WITH_REASON','SUPERSEDED'} or not m.get('rationale'):
                errors.append(a['path']+': unresolved candidate disposition'); valid=False
        expected = candidates_by_artifact.get(a['artifact_id'], set())
        if candidates is None or mapped != expected:
            errors.append(a['path']+': complete candidate accounting is required'); valid=False
        for record in [r] + [m for m in mappings if isinstance(m, dict)]:
            for field in ('supporting_evidence', 'supporting_claims', 'independent_audit', 'repair_recheck'):
                if field in record and not valid_evidence(record[field]):
                    errors.append(a['path']+': invalid advertised '+field); valid=False
        if not valid: continue
        complete.add(a['artifact_id'])
    return {'reviewed':len(complete),'inventoried':len(artifacts),
            'review_coverage':len(complete)/len(artifacts) if artifacts else None,'errors':errors,
            'coverage_unit':'artifact_disposition_receipts',
            'receipt_count':len(complete),
            'receipt_coverage':len(complete)/len(artifacts) if artifacts else None,
            'semantic_truth_certified':False,
            'independent_omission_certified':False,
            'note':'Review receipts require independent source-to-control audit before exhaustive certification.'}


def impact(old_path: Path, new_path: Path, controls: list[dict], dependency_path: Path | None=None) -> dict:
    def idx(p): 
        result={}
        for x in [json.loads(l) for l in p.read_text().splitlines() if l]:
            key=(x['source'],x['path'])
            result[key]=x
        return result
    a,b=idx(old_path),idx(new_path); changes=[]
    artifacts_by_id={r['artifact_id']:key for key,r in a.items() if r.get('artifact_id')}
    dependents=defaultdict(set); unresolved=0
    if dependency_path:
        for line in dependency_path.read_text().splitlines():
            if not line.strip(): continue
            r=json.loads(line);parent=r.get('artifact_id')
            if parent not in artifacts_by_id: raise ValueError('Dependency parent absent from old inventory')
            targets=r.get('resolved_artifact_ids',[])
            if not targets: unresolved+=1
            for child in targets:
                if child not in artifacts_by_id: raise ValueError('Dependency target absent from old inventory')
                dependents[artifacts_by_id[child]].add(artifacts_by_id[parent])
    for key in sorted(a.keys()|b.keys()):
        if key not in a: kind='ADDED'
        elif key not in b: kind='REMOVED'
        elif a[key].get('sha256')!=b[key].get('sha256'): kind='MODIFIED'
        else: continue
        # Traverse source include dependencies conservatively; rendering remains separate.
        impacted={key};pending=[key]
        while pending:
            for parent in dependents[pending.pop()]:
                if parent not in impacted:
                    impacted.add(parent);pending.append(parent)
        affected=[]
        for c in controls:
            for s in c['sources']:
                src_key=(s['repository'],s['path'])
                if src_key in impacted:
                    affected.append(c['id'])
                    break
        changes.append({'source':key[0],'path':key[1],'change':kind,'reopen_controls':affected,'review_required':True,
                        'dependent_artifacts':[{'source':k[0],'path':k[1]} for k in sorted(impacted-{key})]})
    return {'changes':changes,'automatic_policy_deletions':0,'dependencies_provided':dependency_path is not None,
            'unresolved_dependencies':unresolved,'rendered_conditionals_verified':False}
