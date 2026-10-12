if not __debug__:
 raise SystemExit('Independent review requires assertions enabled')
import collections as C, datetime, gzip, hashlib, json, signal, subprocess, time
from pathlib import Path
signal.alarm(30)
t=time.perf_counter(); e=Path('evidence'); S=lambda b:hashlib.sha256(b).hexdigest(); D=lambda x:S(json.dumps(x,sort_keys=True,separators=(',',':')).encode())
report_paths={k:e/p for k,p in {'historical':'claim-workload-inventory.json','baseline':'claim-workload-current-inventory.json','current':'v02-workload-migration-20261012/current-inventory.json'}.items()}
report_raw={k:p.read_bytes() for k,p in report_paths.items()}; reports={k:json.loads(v) for k,v in report_raw.items()}
expected={'historical':'6151dcc71dda756610f371337bebe9981c0f9656cc6f7b252ad60e007701f5ec','baseline':'2e718486119b29cf286f4b21f067d67dc3bea17f2559a45fbc01105931a22658','current':'ed4ee7e8be9a5369d4651769dc8717456473063d2db21010544349a9848b8a00'}
assert {k:S(v) for k,v in report_raw.items()}==expected
h,b,c=(reports[k] for k in ('historical','baseline','current'))
assert D({**h,'inputs':{**h['inputs'],'artifacts_sha256':b['inputs']['artifacts_sha256']}})==D(b)
files={'artifacts':e/'claim-workload-inputs/artifacts.jsonl.gz','receipts':e/'provider-oidc-reconciliation.json','authority':e/'a3-six-source-capsule-repair.json'}
raw={k:p.read_bytes() for k,p in files.items()}
assert S(raw['artifacts'])=='9bf57e2bdf62d37026d5c06981c34e2c9db593e44bf03f39c7e441c9751358ac'
artifact_raw=gzip.decompress(raw['artifacts']); assert S(artifact_raw)=='86225491fb70197b893a0bfb1fa96ebfc1f5a6e33c21c86ab874d9d34f5db9a2'
assert S(raw['receipts'])=='91f52141398c7670bd4e3335b5dad89c88815c3141c75d6007fc52a674e54485'
assert S(raw['authority'])=='05dab95bfbc88c2401a97da702339f4f1be89545c8f8c9f48198194aac07bb15'
artifacts=[json.loads(line) for line in artifact_raw.splitlines() if line.strip()]; assert len(artifacts)==13657
index={(r['source'],r['commit'],r['path']):r for r in artifacts}; assert len(index)==len(artifacts)
source_rows=C.defaultdict(list)
for r in artifacts:source_rows[r['source']].append(r)
fields=('source','commit','path','kind','sha256','git_blob_sha','size','link_target'); authority=json.loads(raw['authority'])
source_digests={s:D([{f:r.get(f) for f in fields} for r in sorted(rows,key=lambda r:r['path'])]) for s,rows in source_rows.items()}
assert source_digests==authority['inventory_identity_digests']
for s,rows in source_rows.items():
 tree=authority['source_trees'][s]; assert len(rows)==tree['artifacts'] and {r['commit'] for r in rows}=={tree['commit']}
receipts=json.loads(raw['receipts']); paths=sorted((e/'source-reviews').glob('*-claims.json')); doc_raw={p.name:p.read_bytes() for p in paths}; hashes={n:S(v) for n,v in doc_raw.items()}; docs={n:json.loads(v) for n,v in doc_raw.items()}
added='wa-application-security-correction-01-claims.json'; old_names={r['path'] for r in b['inputs']['claim_documents']}
assert set(docs)==old_names|{added}; assert hashes[added]=='3830522db4425a0e7e267479fff32b00cc12541b36bfacd01033faa009df2589'
pairs={(f'WA-APPSEC-{n}',f'WA-APPSEC-{n}-CORRECTION-01') for n in ('005','009','011','017','018')}
assert len(docs[added]['claims'])==5 and {(r['supersedes_claim_id'],r['claim_id']) for r in docs[added]['claims']}==pairs
for r in b['inputs']['claim_documents']:assert hashes[r['path']]==r['sha256'] and len(docs[r['path']]['claims'])==r['claims']
def rebuild(report,names):
 sources=C.Counter(); strengths=C.Counter(); texts=C.Counter(); spans=C.Counter(); kinds=C.Counter(); fields=C.Counter(); provider_rows=set(); query_rows=set(); members=C.defaultdict(list); keys={}; known={}; bindings={}
 for name in sorted(names):
  doc=docs[name]
  for row in doc['claims']:
   cid=row['claim_id']; assert cid not in known
   identity=tuple(row.get(k,doc.get(k)) for k in ('source','commit','path')); source,commit,path=identity; artifact=index[identity]
   assert row.get('artifact_id',doc.get('artifact_id',artifact['artifact_id']))==artifact['artifact_id']
   assert row.get('content_sha256',doc.get('content_sha256',artifact['sha256']))==artifact['sha256']
   start,end=row['start_line'],row['end_line']; text_hash=S(row['statement'].encode()); context=row.get('context',{}); context=context if isinstance(context,dict) else {}
   provider_keys={'provider','raw_credential_identifier','source_field','entry_ordinal','definition_start_line','definition_end_line'}; typed=provider_keys.intersection(context); assert not typed or typed==provider_keys
   query='query_occurrence' in row or 'query_help_identity' in row; assert not(typed and query)
   if typed:
    kind='PROVIDER_CAPABILITY_MATRIX'; key=[source,commit,context['provider'],context['raw_credential_identifier']]; fields[context['source_field']]+=1; rid=(*identity,context['entry_ordinal']); provider_rows.add(rid)
    binding=tuple(context[k] for k in ('provider','raw_credential_identifier','definition_start_line','definition_end_line')); assert rid not in bindings or bindings[rid]==binding; bindings[rid]=binding
   elif query:
    assert row['query_occurrence']==path+'#L'+str(start); kind='QUERY_TABLE_ROW'; key=[source,commit,row['query_occurrence'],row['query_help_identity']]; query_rows.add(tuple(key))
   else:kind='SOURCE_ARTIFACT_CONTEXT'; key=list(identity)
   fid=D([kind,key]); keys[fid]=(kind,key); members[fid].append(cid)
   known[cid]={'source':source,'commit':commit,'path':path,'start_line':start,'end_line':end,'artifact_id':artifact['artifact_id'],'content_sha256':artifact['sha256'],'statement_sha256':text_hash,'claim_document':name,'claim_document_sha256':hashes[name],'family_id':fid}
   sources[source]+=1; strengths[str(row.get('source_strength','UNSPECIFIED'))]+=1; texts[text_hash]+=1; spans[(*identity,start,end)]+=1; kinds[kind]+=1
 reconciled=C.defaultdict(list); seen=set()
 for receipt in receipts:
  subject=receipt['claim']; cid=subject['claim_id']; assert cid in known and cid not in seen; seen.add(cid)
  for k,v in known[cid].items():
   if k!='family_id':assert subject[k]==v,(cid,k)
  reconciled[known[cid]['family_id']].append(cid)
 families=[{'family_id':fid,'kind':keys[fid][0],'key':keys[fid][1],'claim_ids':sorted(members[fid]),'reconciled_claim_ids':sorted(reconciled[fid]),'semantic_equivalence_verified':False} for fid in sorted(keys,key=lambda fid:(keys[fid][0],fid))]
 counts={'recorded_claims':len(known),'claim_documents':len(names),'by_source':dict(sorted(sources.items())),'by_recorded_source_strength':dict(sorted(strengths.items())),'exact_statement_hashes':len(texts),'repeated_statement_occurrences':sum(v-1 for v in texts.values()),'exact_source_spans':len(spans),'repeated_source_span_occurrences':sum(v-1 for v in spans.values()),'claims_by_queue_kind':dict(sorted(kinds.items())),'families_by_queue_kind':dict(sorted(C.Counter(f['kind'] for f in families).items())),'provider_dataset_rows':len(provider_rows),'provider_field_occurrences':dict(sorted(fields.items())),'query_row_occurrences':len(query_rows),'reconciliation_records_present':len(seen),'recorded_claims_without_reconciliation':len(known)-len(seen),'new_review_credit':0,'new_reconciliation_credit':0,'unique_actionable_obligations':None}
 inputs={'claim_documents':[{'path':n,'sha256':hashes[n],'claims':len(docs[n]['claims'])} for n in sorted(names)],'artifacts_sha256':S(artifact_raw),'reconciliation_sha256':S(raw['receipts'])}
 assert D(counts)==D(report['counts']),'counts'; assert D(families)==D(report['families']),'families'; assert D(inputs)==D(report['inputs']),'inputs'; assert D(sorted(known))==report['claim_membership_digest'],'membership'
 return known
old=rebuild(b,old_names); new=rebuild(c,set(docs)); assert set(new)-set(old)=={n for _,n in pairs} and not set(old)-set(new); assert all(new[cid]==v for cid,v in old.items()); assert all(p in old for p,_ in pairs)
assert all(c[k]==b[k] for k in c if k not in ('inputs','counts','claim_membership_digest','families'))
frozen=['evidence/source-reviews','evidence/claim-workload-inventory.json','evidence/claim-workload-current-inventory.json','evidence/claim-workload-current-provenance.json','evidence/claim-workload-inputs','evidence/a3-six-source-capsule-repair.json','evidence/provider-oidc-reconciliation.json','evidence/v02-finish-20261010/claim-migration-audit.json','evidence/v02-finish-20261010/owner-authorization.json']
subprocess.run(['git','diff','--exit-code','afdd2ffe03bd840516947a9256ff9aea380335fb','--',*frozen],check=True,capture_output=True)
assert paths==sorted((e/'source-reviews').glob('*-claims.json')); assert all(p.read_bytes()==doc_raw[p.name] for p in paths); assert all(p.read_bytes()==report_raw[k] for k,p in report_paths.items()); assert all(p.read_bytes()==raw[k] for k,p in files.items())
code=['ges/claim_workload.py','ges/claim_workload_migration.py','tests/test_claim_workload_integrity.py','tests/test_claim_workload_migration.py']
print(json.dumps({'reviewer':'/root/migration_review','status':'PASS','observed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'elapsed_seconds':round(time.perf_counter()-t,6),'imports_project_code':False,'complete_counts_families_and_membership_reconstructed':True,'all_historical_document_and_claim_subject_bindings_unchanged':True,'historical_claims':len(old),'current_claims':len(new),'historical_documents':len(old_names),'current_documents':len(docs),'families':len(c['families']),'exact_statement_hashes':c['counts']['exact_statement_hashes'],'exact_source_spans':c['counts']['exact_source_spans'],'repeated_source_span_occurrences':c['counts']['repeated_source_span_occurrences'],'source_bound_receipts':len(receipts),'claims_without_frozen_receipts':len(new)-len(receipts),'artifact_rows':len(artifacts),'all_six_source_identity_digests_match_a3':True,'report_sha256':expected,'current_claim_membership_digest':c['claim_membership_digest'],'reviewed_file_sha256':{n:S(Path(n).read_bytes()) for n in code},'new_semantic_or_reconciliation_credit':0,'full_authenticated_source_replay':False,'human_approval':False},indent=2))
