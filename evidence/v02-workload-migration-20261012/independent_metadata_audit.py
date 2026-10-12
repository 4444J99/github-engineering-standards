"""Independent metadata review by /root/accounting_review; no source authentication."""
if not __debug__:
 raise RuntimeError('Independent audit requires assertions enabled')
import collections, gzip, hashlib, json, pathlib, signal, time
from datetime import datetime, timezone
def audit_timeout(signum, frame):
 raise TimeoutError('Independent metadata audit exceeded 30 seconds')
signal.signal(signal.SIGALRM,audit_timeout)
signal.alarm(30)
started=time.monotonic()
root=pathlib.Path(__file__).resolve().parents[2]
reviews=root/'evidence/source-reviews'
sha=lambda b:hashlib.sha256(b).hexdigest()
canonical=lambda o:json.dumps(o,sort_keys=True,separators=(',',':'))
digest=lambda o:sha(canonical(o).encode())
read={}
def data(rel, expected=None):
 p=root/rel
 assert not p.is_symlink(), rel
 raw=p.read_bytes()
 read[rel]=sha(raw)
 if expected: assert read[rel]==expected, rel+' hash differs'
 return raw
old=json.loads(data('evidence/claim-workload-inventory.json','6151dcc71dda756610f371337bebe9981c0f9656cc6f7b252ad60e007701f5ec'))
baseline=json.loads(data('evidence/claim-workload-current-inventory.json','2e718486119b29cf286f4b21f067d67dc3bea17f2559a45fbc01105931a22658'))
current=json.loads(data('evidence/claim-workload-v02-inventory.json','ed4ee7e8be9a5369d4651769dc8717456473063d2db21010544349a9848b8a00'))
provenance=json.loads(data('evidence/claim-workload-current-provenance.json'))
data('evidence/a3-six-source-capsule-repair.json','05dab95bfbc88c2401a97da702339f4f1be89545c8f8c9f48198194aac07bb15')
artifact_raw=gzip.decompress(data('evidence/claim-workload-inputs/artifacts.jsonl.gz','9bf57e2bdf62d37026d5c06981c34e2c9db593e44bf03f39c7e441c9751358ac'))
assert sha(artifact_raw)=='86225491fb70197b893a0bfb1fa96ebfc1f5a6e33c21c86ab874d9d34f5db9a2'
artifacts=[json.loads(line) for line in artifact_raw.splitlines() if line.strip()]
index={(x['source'],x['commit'],x['path']):x for x in artifacts}
assert len(index)==len(artifacts)==13657
receipt_raw=data('evidence/provider-oidc-reconciliation.json','91f52141398c7670bd4e3335b5dad89c88815c3141c75d6007fc52a674e54485')
receipts=json.loads(receipt_raw)
assert len(receipts)==474
assert provenance['bindings']=={
'historical_report_sha256':read['evidence/claim-workload-inventory.json'],
'current_report_sha256':read['evidence/claim-workload-current-inventory.json'],
'artifact_inventory_sha256':sha(artifact_raw),
'compressed_artifact_inventory_sha256':read['evidence/claim-workload-inputs/artifacts.jsonl.gz']}
oldcopy=json.loads(json.dumps(old));basecopy=json.loads(json.dumps(baseline))
oldcopy['inputs'].pop('artifacts_sha256');basecopy['inputs'].pop('artifacts_sha256')
assert canonical(oldcopy)==canonical(basecopy)
historical_docs={x['path']:x for x in baseline['inputs']['claim_documents']}
assert len(historical_docs)==654
paths=sorted(reviews.glob('*-claims.json'))
added_name='wa-application-security-correction-01-claims.json'
assert len(paths)==655 and {p.name for p in paths}==set(historical_docs)|{added_name}
claims={};docs=[];groups={};text_count=collections.Counter();span_count=collections.Counter()
by_source=collections.Counter();strength=collections.Counter();kinds=collections.Counter()
provider_fields=collections.Counter();provider_rows=set();query_rows=set();pairs={}
provider_keys={'provider','raw_credential_identifier','source_field','entry_ordinal','definition_start_line','definition_end_line'}
for p in paths:
 rel='evidence/source-reviews/'+p.name
 raw=data(rel)
 document_sha=sha(raw)
 doc=json.loads(raw)
 if p.name in historical_docs:
  assert document_sha==historical_docs[p.name]['sha256'], p.name
  assert len(doc['claims'])==historical_docs[p.name]['claims'], p.name
 else:
  assert document_sha=='3830522db4425a0e7e267479fff32b00cc12541b36bfacd01033faa009df2589'
  assert len(doc['claims'])==5
 docs.append({'path':p.name,'sha256':document_sha,'claims':len(doc['claims'])})
 for c in doc['claims']:
  cid=c['claim_id']
  assert cid not in claims
  ident=tuple(c.get(k,doc.get(k)) for k in ('source','commit','path'))
  artifact=index[ident]
  assert c.get('content_sha256',doc.get('content_sha256',artifact['sha256']))==artifact['sha256']
  assert c.get('artifact_id',doc.get('artifact_id',artifact['artifact_id']))==artifact['artifact_id']
  a,b=c['start_line'],c['end_line']
  context=c.get('context') if isinstance(c.get('context'),dict) else {}
  is_provider=provider_keys<=context.keys()
  assert not(provider_keys&context.keys()) or is_provider
  is_query='query_occurrence' in c or 'query_help_identity' in c
  assert not(is_provider and is_query)
  if is_provider:
   kind='PROVIDER_CAPABILITY_MATRIX'
   key=[ident[0],ident[1],context['provider'],context['raw_credential_identifier']]
   provider_fields[context['source_field']]+=1
   provider_rows.add((*ident,context['entry_ordinal']))
  elif is_query:
   assert c['query_occurrence']==ident[2]+'#L'+str(a)
   kind='QUERY_TABLE_ROW'
   key=[ident[0],ident[1],c['query_occurrence'],c['query_help_identity']]
   query_rows.add(tuple(key))
  else:
   kind='SOURCE_ARTIFACT_CONTEXT';key=list(ident)
  fid=digest([kind,key])
  group=groups.setdefault(fid,{'family_id':fid,'kind':kind,'key':key,'claim_ids':[],'reconciled_claim_ids':[],'semantic_equivalence_verified':False})
  group['claim_ids'].append(cid)
  claims[cid]={'claim_id':cid,'source':ident[0],'commit':ident[1],'path':ident[2],
   'start_line':a,'end_line':b,'artifact_id':artifact['artifact_id'],'content_sha256':artifact['sha256'],
   'statement_sha256':sha(c['statement'].encode()),'claim_document':p.name,'claim_document_sha256':document_sha,'family_id':fid}
  by_source[ident[0]]+=1;strength[str(c.get('source_strength','UNSPECIFIED'))]+=1
  text_count[sha(c['statement'].encode())]+=1;span_count[(*ident,a,b)]+=1;kinds[kind]+=1
  if p.name==added_name:pairs[cid]=c['supersedes_claim_id']
expected_pairs={'WA-APPSEC-'+n+'-CORRECTION-01':'WA-APPSEC-'+n for n in ('005','009','011','017','018')}
assert pairs==expected_pairs and set(pairs.values())<=claims.keys()
old_ids=[cid for fam in baseline['families'] for cid in fam['claim_ids']]
assert len(old_ids)==len(set(old_ids))==61936
assert set(claims)==set(old_ids)|set(pairs)
reconciled=set()
for r in receipts:
 subject=r['claim'];cid=subject['claim_id']
 assert cid not in reconciled
 known=claims[cid]
 assert set(subject)==set(known)-{'family_id'}
 for k,v in subject.items():
  assert v==known[k],cid+' '+k
 reconciled.add(cid)
 groups[known['family_id']]['reconciled_claim_ids'].append(cid)
for g in groups.values():
 g['claim_ids'].sort();g['reconciled_claim_ids'].sort()
families=sorted(groups.values(),key=lambda x:(x['kind'],x['family_id']))
assert canonical(families)==canonical(current['families'])
reduced=json.loads(json.dumps(current['families']))
for f in reduced:f['claim_ids']=[x for x in f['claim_ids'] if x not in pairs]
assert canonical(reduced)==canonical(baseline['families'])
counts={
'recorded_claims':len(claims),'claim_documents':len(docs),'by_source':dict(sorted(by_source.items())),
'by_recorded_source_strength':dict(sorted(strength.items())),'exact_statement_hashes':len(text_count),
'repeated_statement_occurrences':sum(n-1 for n in text_count.values()),'exact_source_spans':len(span_count),
'repeated_source_span_occurrences':sum(n-1 for n in span_count.values()),'claims_by_queue_kind':dict(sorted(kinds.items())),
'families_by_queue_kind':dict(sorted(collections.Counter(g['kind'] for g in families).items())),
'provider_dataset_rows':len(provider_rows),'provider_field_occurrences':dict(sorted(provider_fields.items())),
'query_row_occurrences':len(query_rows),'reconciliation_records_present':len(reconciled),
'recorded_claims_without_reconciliation':len(claims)-len(reconciled),'new_review_credit':0,
'new_reconciliation_credit':0,'unique_actionable_obligations':None}
assert canonical(counts)==canonical(current['counts'])
assert current['inputs']=={'claim_documents':docs,'artifacts_sha256':sha(artifact_raw),'reconciliation_sha256':sha(receipt_raw)}
assert current['claim_membership_digest']==digest(sorted(claims))
for k in ('schema','scope','limits'):assert canonical(current[k])==canonical(baseline[k])
assert len(set(current)|set(baseline))==len(current)==len(baseline)
assert sorted(reviews.glob('*-claims.json'))==paths
for rel,s in read.items():assert sha((root/rel).read_bytes())==s,rel+' changed during audit'
changed={}
for k,v in counts.items():
 prior=baseline['counts'][k]
 if canonical(v)==canonical(prior):continue
 if isinstance(v,dict):changed[k]={name:{'before':prior.get(name),'after':value} for name,value in v.items() if value!=prior.get(name)}
 else:changed[k]={'before':prior,'after':v}
print(json.dumps({'status':'PASS','reviewer':'/root/accounting_review','kind':'independent software and metadata review; no source authentication or semantic authority',
'observed_at':datetime.now(timezone.utc).isoformat(),'duration_seconds':round(time.monotonic()-started,3),
'new_report_sha256':read['evidence/claim-workload-v02-inventory.json'],
'old_and_current_documents_checked':len(paths),'historical_documents_preserved':len(historical_docs),
'family_members_checked':len(claims),'families':len(families),'receipt_subjects_checked':len(reconciled),
'exact_successor_pairs':pairs,'baseline_unchanged':True,'all_inputs_stable':True,'changed_counts':changed,
'claim_membership_digest':current['claim_membership_digest']},indent=2))
signal.alarm(0)
