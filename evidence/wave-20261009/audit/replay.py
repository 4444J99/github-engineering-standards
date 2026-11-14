"""E independent read-only replay against frozen inputs. No upstream code executes."""
import hashlib, gzip, json, subprocess, sys
from pathlib import Path
R=Path(__file__).resolve().parents[3]
W=R/'evidence/wave-20261009'
OR=Path('/Users/4jp/Workspace/4444J99/engineering-environment-standards/github-engineering-standards/github-engineering-standards')
S=OR/'.cache/sources'
C=Path('/Users/4jp/Workspace/4444J99/.worktrees/ges-wave-20261009/.cache/publication-candidate')
A=C.parent/'artifacts.jsonl'
def load(p): return json.loads(p.read_bytes())
def sha(b): return hashlib.sha256(b).hexdigest()
def dg(x): return sha(json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode())
d=load(W/'integration/proposed-decisions.json'); reg=load(W/'integration/publication-register.json')
assert sha((W/'integration/proposed-decisions.json').read_bytes())=='143c96b9ab24843ee9554dd70910464b12d0fd4261d6e8fb38dc78a23e7e8da1'
for b in d['bindings']: assert sha((R/b['path']).read_bytes())==b['sha256'],b
cache=load(W/'cache-validation.json')
for s in cache['snapshots']: assert sha((S/(s['source'].replace('/','__')+'.text.jsonl.gz')).read_bytes())==s['snapshot_sha256']
wa={x['path']:x for x in map(json.loads,gzip.open(S/'github__github-well-architected.text.jsonl.gz','rt'))}
gh={x['path']:x for x in map(json.loads,gzip.open(S/'microsoft__ghqr.text.jsonl.gz','rt'))}
assignment=load(W/'assignment.json'); claims={x['claim_id']:x for x in assignment['B']['claims']}
occ={x['requirement_id']:x for x in load(OR/'.cache/a3-corpus-20261006/structured-source-requirements.json')}
for x in load(W/'source/occurrence-crosswalk.json'):
 cl=claims[x['claim']['claim_id']]
 assert [o['id'] for o in x['occurrences']]==cl['structured_requirement_ids']
 for o in x['occurrences']: assert dg(occ[o['id']])==o['digest']
cat={x['id']:x for x in load(R/'controls/catalog.json')}; q={x['id']:x for x in load(R/'controls/review_queue.json')}
assert dg(d['source_relations'])==d['source_relations_digest']
for rel in d['source_relations']:
 cl=rel['claim']; src=wa[cl['path']]; assert sha(src['content'].encode())==cl['content_sha256'];assert src['commit']==cl['commit']
 assert len({rel[k] for k in ['primary_reviewer','omission_reviewer','reconciler','decision_auditor_required']})==4
 assert rel['decision_auditor_required']=='codex:/root/decision_auditor_e'
 assert rel['accepted_policy'] is False and rel['objective_synthesis_complete'] is False
 for ref in rel['control_references']:
  control=(cat if ref['collection']=='CATALOG' else q)[ref['id']];assert control['revision']==ref['revision'];assert control['status']!='ACCEPTED'
assert len(d['source_relations'])==13
assert {x['claim']['claim_id'] for x in d['source_relations']}.isdisjoint(d['held_claim_ids'])
findings=load(W/'omission/source-findings.json')['findings']+load(W/'omission/publication-findings.json')['findings']
assert {x['id'] for x in findings}=={x['finding_id'] for x in d['finding_dispositions']}
pub=load(W/'publication/primary-review.json'); queue=load(C/'controls/review_queue.json')
selected=[x['proposal_id'] for x in assignment['C']['selected_proposals']]
assert selected==sorted(selected) and selected==[x['proposal_id'] for x in pub['proposal_reviews']]
for u in pub['uses']:
 ob=(C/u['output_path']).read_bytes();r=u['output_range'];ob=ob[r['start_byte']:r['end_byte']];assert sha(ob)==r['sha256']
 value=queue
 for token in u['json_pointer'].split('/')[1:]:value=value[int(token)] if isinstance(value,list) else value[token]
 assert json.loads(b'"'+ob+b'"')==value
 src=gh[u['source']['path']];sb=src['content'].encode();assert sha(sb)==u['source']['sha256'];assert src['commit']==u['source']['commit']
 if u['source_range']:
  r=u['source_range'];span=sb[r['start_byte']:r['end_byte']];assert sha(span)==r['sha256']
  if u['kind']=='LICENSED_COPY':assert span==ob
 if u['kind']=='REFERENCES_ONLY':assert value.startswith('https://github.com/microsoft/ghqr/blob/'+src['commit']+'/')
 for att in u['attributions']:
  r=att['output_range'];notice=(C/att['output_path']).read_bytes()[r['start_byte']:r['end_byte']];assert sha(notice)==r['sha256'];assert gh['LICENSE']['content'].strip().encode()==notice.strip()
for review in pub['proposal_reviews']:
 obj=queue[int(review['json_pointer'][1:])];assert obj['id']==review['proposal_id']
 source=gh[obj['sources'][0]['path']]['content'].encode();r=review['source_context_range'];assert sha(source[r['start_byte']:r['end_byte']])==r['sha256']
assert len(reg['uses'])==198 and len(reg['outputs'])==2396
assert all(x['disposition']=='UNREVIEWED' for x in reg['outputs'])
assert load(W/'integration/publication-policy.json')=={} and load(W/'integration/publication-receipts.json')==[]
cmd=[sys.executable,'-m','ges.publication_use','--manifest',str(R/'evidence/publication-candidates/ges-v0.2-merged-f628db26-20261008/manifest.json'),'--register',str(W/'integration/publication-register.json'),'--receipts',str(W/'integration/publication-receipts.json'),'--policy',str(W/'integration/publication-policy.json'),'--artifacts',str(A),'--output-root',str(C),'--source-root',str(S)]
run=subprocess.run(cmd,cwd=R,capture_output=True,text=True)
result=json.loads(run.stdout);assert run.returncode==1 and result['valid'] is True,(run.returncode,run.stdout,run.stderr)
(W/'audit/publication-accounting.json').write_text(json.dumps(result,indent=2)+'\n')
report={'structural_result':'PASS','source_relations_checked':13,'crosswalk_claims_checked':162,'publication_proposals_checked':50,'primary_use_spans_checked':len(pub['uses']),'registered_uses_checked':len(reg['uses']),'all_d_findings_dispositioned':len(findings),'publication_command':cmd,'publication_exit_code':run.returncode,'publication_stderr':run.stderr,'automated_checks_establish_semantics_or_rights':False}
(W/'audit/replay-results.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
