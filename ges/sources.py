"""Pinned source acquisition. Imported code is never run; raw material is private cache.
Archives are streamed in memory with size limits, never extracted onto the filesystem.
Only public sources in the locked manifest are allowed. No credential is sent to Docs.
"""
from __future__ import annotations
import concurrent.futures as cf
import gzip,hashlib,io,json,os,re,tarfile,time
from pathlib import Path,PurePosixPath
import urllib.error,urllib.parse,urllib.request
from .core import ROOT,dump,load,now

class NoAuthRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl):
        new=super().redirect_request(req,fp,code,msg,headers,newurl)
        if new is not None:
            orig_host=urllib.parse.urlparse(req.full_url).netloc
            new_host=urllib.parse.urlparse(newurl).netloc
            if new_host!=orig_host:
                new.remove_header('Authorization')
        return new

OPENER=urllib.request.build_opener(NoAuthRedirect())

def fetch(url: str, *, limit: int=600_000_000, attempts: int=4, expected_sha256: str | None=None) -> bytes:
    host=urllib.parse.urlparse(url).netloc
    if host not in {'api.github.com','codeload.github.com','docs.github.com'}:raise ValueError('Source host outside allowlist')
    headers={'User-Agent':'github-engineering-standards/0.1.0'}
    token=os.environ.get('GH_TOKEN') or os.environ.get('GITHUB_TOKEN')
    if host=='api.github.com' and token:headers['Authorization']='Bearer '+token
    for attempt in range(attempts):
        try:
            with OPENER.open(urllib.request.Request(url,headers=headers),timeout=120) as response:
                body=response.read(limit+1)
                if len(body)>limit:raise ValueError('Source response exceeds size limit')
                if expected_sha256:
                    actual=hashlib.sha256(body).hexdigest()
                    if actual!=expected_sha256:
                        raise ValueError(f'Archive digest mismatch: expected {expected_sha256}, got {actual}')
                return body
        except urllib.error.HTTPError as exc:
            if exc.code not in {429,500,502,503,504} or attempt+1==attempts:raise
            try:delay=float(exc.headers.get('Retry-After','0'))
            except ValueError:delay=0
            time.sleep(min(60,max(delay,2**attempt)))
        except (urllib.error.URLError,TimeoutError):
            if attempt+1==attempts:raise
            time.sleep(2**attempt)
    raise RuntimeError('Unreachable acquisition state')

def acquire_source(spec: dict, output: Path) -> dict:
    repo=spec['repository'];sha=spec['commit'];stamp=now()
    if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+',repo) or not re.fullmatch('[a-f0-9]{40}',sha):raise ValueError('Unpinned or invalid source')
    slug=repo.replace('/','__');url=f'https://codeload.github.com/{repo}/tar.gz/{sha}'
    expected_sha256=spec.get('archive_sha256')
    body=fetch(url,expected_sha256=expected_sha256);inventory=[]
    if spec.get('archive_bytes') is not None and len(body) != spec['archive_bytes']:
        raise ValueError('Archive size does not match locked snapshot')
    textpath=output/(slug+'.text.jsonl.gz');temp=textpath.with_suffix('.tmp')
    with gzip.open(temp,'wt',encoding='utf-8') as texts,tarfile.open(fileobj=io.BytesIO(body),mode='r:gz') as archive:
        for m in archive:
            parts=PurePosixPath(m.name).parts
            if len(parts)<2 or m.isdir():continue
            if '..' in parts or m.name.startswith('/'):raise ValueError('Unsafe source path')
            path='/'.join(parts[1:]);row={'source':repo,'commit':sha,'path':path,'size':m.size,'retrieved_at':stamp,'review_status':'UNREVIEWED','url':f'https://github.com/{repo}/blob/{sha}/{urllib.parse.quote(path)}'}
            if not m.isfile():
                row.update(kind='nonregular',retrieval_status='METADATA_ONLY',link_target=m.linkname);inventory.append(row);continue
            if m.size>200_000_000:raise ValueError('Source member exceeds size limit')
            stream=archive.extractfile(m);raw=stream.read(m.size+1)
            if len(raw)!=m.size:raise ValueError('Archive member size mismatch')
            row.update(sha256=hashlib.sha256(raw).hexdigest(),git_blob_sha=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest(),retrieval_status='RETRIEVED')
            try:
                text=raw.decode('utf-8')
                if '\0' in text:raise ValueError('Binary content')
                row['kind']='text';texts.write(json.dumps({**row,'content':text},ensure_ascii=False)+'\n')
            except (UnicodeDecodeError,ValueError):row['kind']='binary'
            inventory.append(row)
    temp.replace(textpath);dump(output/(slug+'.inventory.json'),inventory)
    notices=[]
    for row in inventory:
        if row.get('kind')=='text' and PurePosixPath(row['path']).name.lower() in {
                'license','license.md','license.txt','license.rst','notice','notice.md','notice.txt',
                'copying','copying.md','copying.txt','copyright','copyright.md','copyright.txt'}:
            text_path=output/(slug+'.text.jsonl.gz')
            with gzip.open(text_path,'rt',encoding='utf-8') as f:
                for line in f:
                    raw=json.loads(line)
                    if raw['path']==row['path']:
                        notices.append({'source':repo,'path':row['path'],'content':raw.get('content','')[:5000]})
                        break
    if notices:
        dump(output/(slug+'.notices.json'),notices)
    reconciliation={'status':'PENDING'}
    try:
        tree=json.loads(fetch(f'https://api.github.com/repos/{repo}/git/trees/{sha}?recursive=1',limit=25_000_000))
        if tree.get('truncated'):reconciliation={'status':'BLOCKED','reason':'Recursive tree truncated; subtree traversal required'}
        else:
            treefiles={x['path']:x for x in tree['tree'] if x['type'] in {'blob','commit'}}
            seen={x['path']:x for x in inventory}
            mismatches=[p for p in seen.keys()&treefiles.keys() if seen[p].get('git_blob_sha') and seen[p]['git_blob_sha']!=treefiles[p]['sha']]
            missing=sorted(treefiles.keys()-seen.keys());extra=sorted(seen.keys()-treefiles.keys())
            reconciliation={'status':'MATCH' if not missing and not extra and not mismatches else 'DIFFERENCE','git_tree_artifacts':len(treefiles),'archive_artifacts':len(inventory),'missing_from_archive':missing,'extra_in_archive':extra,'blob_mismatches':mismatches}
        dump(output/(slug+'.tree-reconciliation.json'),reconciliation)
    except (urllib.error.URLError,ValueError,KeyError,TimeoutError) as exc:
        reconciliation={'status':'ERROR','error_type':type(exc).__name__,'http_status':getattr(exc,'code',None)}
        dump(output/(slug+'.tree-reconciliation.json'),reconciliation)
    return {'repository':repo,'commit':sha,'archive_url':url,'archive_sha256':hashlib.sha256(body).hexdigest(),'artifacts':len(inventory),'text_artifacts':sum(x['kind']=='text' for x in inventory),'binary_artifacts':sum(x['kind']=='binary' for x in inventory),'retrieved_at':stamp,'reviewed_artifacts':0,'status':'SNAPSHOT_RETRIEVED','git_tree_reconciliation':reconciliation}

def acquire_pages(output: Path, *, rendered: bool=False, rendered_limit: int=0, workers: int=4) -> dict:
    versions=json.loads(fetch('https://docs.github.com/api/pagelist/versions',limit=2_000_000));dump(output/'docs-versions.json',versions)
    items=versions
    if isinstance(items,dict):items=items.get('versions',list(items))
    names=[]
    for item in items:
        if isinstance(item,str):names.append(item)
        elif isinstance(item,dict):names.append(item.get('version') or item.get('id') or item.get('name'))
    names=list(dict.fromkeys(['free-pro-team@latest','enterprise-cloud@latest']+[x for x in names if isinstance(x,str)]))
    pages=[];vr=[]
    for version in names:
        if not re.fullmatch('[a-z0-9.@-]+',version):raise ValueError('Unexpected version name')
        try:
            text=fetch('https://docs.github.com/api/pagelist/en/'+urllib.parse.quote(version,safe='@'),limit=30_000_000).decode()
            paths=sorted(set(l.strip() for l in text.splitlines() if re.match(r'^/en(?:/|$)',l.strip())))
            if not paths:raise ValueError('Empty page list')
            (output/('docs-pages-'+version+'.txt')).write_text('\n'.join(paths)+'\n')
            pages.extend({'path':p,'version':version,'language':'en'} for p in paths);vr.append({'version':version,'pages':len(paths),'status':'INVENTORIED'})
        except (urllib.error.URLError,ValueError,TimeoutError) as exc:vr.append({'version':version,'status':'ERROR','error_type':type(exc).__name__})
    errors=[];retrieved=0
    if rendered:
        todo=pages if not rendered_limit else pages[:rendered_limit]
        def one(page):
            url='https://docs.github.com/api/article/body?pathname='+urllib.parse.quote(page['path'],safe='')
            try:
                raw=fetch(url,limit=5_000_000);text=raw.decode()
                if not text.strip() or text.lstrip().lower().startswith(('<!doctype','<html')):raise ValueError('Not an article body')
                return {**page,'status':'RETRIEVED','retrieved_at':now(),'sha256':hashlib.sha256(raw).hexdigest(),'body':text,'endpoint':url}
            except (urllib.error.URLError,ValueError,TimeoutError) as exc:return {**page,'status':'ERROR','error_type':type(exc).__name__,'http_status':getattr(exc,'code',None)}
        with gzip.open(output/'docs-rendered.jsonl.gz','wt',encoding='utf-8') as out,cf.ThreadPoolExecutor(max_workers=min(8,max(1,workers))) as pool:
            for record in pool.map(one,todo):
                out.write(json.dumps(record,ensure_ascii=False)+'\n')
                if record['status']=='RETRIEVED':retrieved+=1
                else:errors.append(record)
    report={'language':'en','versions':vr,'page_version_instances':len(pages),'rendered_article_bodies_retrieved':retrieved,'rendered_errors':errors,'rendered_complete':rendered and retrieved==len(pages) and not errors and all(v['status']=='INVENTORIED' for v in vr)}
    dump(output/'published-docs-report.json',report);return report

def sync(output: Path, *, manifest: Path=ROOT/'sources/sources.lock.json',rendered: bool=False,rendered_limit: int=0,workers: int=4) -> dict:
    output.mkdir(parents=True,exist_ok=True);specs=load(manifest)['sources'];results=[]
    with cf.ThreadPoolExecutor(max_workers=3) as pool:
        futures={pool.submit(acquire_source,s,output):s for s in specs}
        for future in cf.as_completed(futures):
            s=futures[future]
            try:results.append(future.result())
            except Exception as exc:results.append({'repository':s['repository'],'commit':s['commit'],'status':'ERROR','error_type':type(exc).__name__,'http_status':getattr(exc,'code',None)})
    report={'schema_version':'ges.acquisition.v1','generated_at':now(),'sources':results,'semantic_review_complete':False}
    docs_result=None
    try:
        docs_result=acquire_pages(output,rendered=rendered,rendered_limit=rendered_limit,workers=workers)
        report['published_docs']=docs_result
    except Exception as exc:
        report['published_docs']={'status':'ERROR','error_type':type(exc).__name__}
    source_errors=any(r.get('status')=='ERROR' for r in results)
    doc_errors=docs_result is None or any(v.get('status')=='ERROR' for v in docs_result.get('versions',[])) if docs_result else True
    rendered_errors=docs_result and docs_result.get('rendered_errors') if docs_result else []
    report['errors']={'source_errors':source_errors,'doc_errors':doc_errors,'rendered_errors':len(rendered_errors) if rendered_errors else 0}
    dump(output/'acquisition-report.json',report);return report
