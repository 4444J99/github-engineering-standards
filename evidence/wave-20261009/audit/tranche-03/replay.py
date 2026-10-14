"""E03 read-only exact-subject replay, preserving semantic findings separately."""
import json,gzip,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[4];W=R/'evidence/wave-20261009';O=W/'audit/tranche-03'
OR=Path('/Users/4jp/Workspace/4444J99/engineering-environment-standards/github-engineering-standards/github-engineering-standards')
def load(p):return json.loads(p.read_bytes())
def sha(b):return hashlib.sha256(b).hexdigest()
def dg(x):return sha(json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode())
d=load(W/'integration/tranche-03/proposed-decisions.json');primary=load(W/'source/tranche-03/primary-review.json');D=load(W/'omission/tranche-03/source-findings.json')
for b in d['bindings']+D['bindings']:assert sha((R/b['path']).read_bytes())==b['sha256']
snapshot=OR/'.cache/sources/github__github-well-architected.text.jsonl.gz';assert sha(snapshot.read_bytes())==load(W/'source/tranche-03/input-bindings.json')['source_snapshot_compressed_sha256']
src={x['path']:x for x in map(json.loads,gzip.open(snapshot,'rt'))}
for b in load(W/'source/tranche-03/input-bindings.json')['context_read_spans']:assert sha(src[b['path']]['content'].encode())==b['content_sha256']
claimdoc=R/'evidence/source-reviews/wa-application-security-checklist-claims.json';claims={x['claim_id']:x for x in load(claimdoc)['claims']}
cat={x['id']:x for x in load(R/'controls/catalog.json')};q={x['id']:x for x in load(R/'controls/review_queue.json')}
for x in primary:
 c=x['claim'];s=src[c['path']];assert sha(s['content'].encode())==c['content_sha256'];assert s['commit']==c['commit'];assert sha(claimdoc.read_bytes())==c['claim_document_sha256'];assert sha(claims[c['claim_id']]['statement'].encode())==c['statement_sha256']
 span='\n'.join(s['content'].splitlines()[c['start_line']-1:c['end_line']]).encode();assert sha(span)==x['source_span_sha256']
for x in d['source_relations']:
 assert x['claim']['claim_id'] in claims
 assert len({x[k] for k in ['primary_reviewer','omission_reviewer','reconciler','decision_auditor_required']})==4
 assert x['decision_auditor_required']=='codex:/root/decision_auditor_e'
 assert x['accepted_policy'] is False and x['objective_synthesis_complete'] is False
 for ref in x['control_references']:assert (cat if ref['collection']=='CATALOG' else q)[ref['id']]['revision']==ref['revision']
assert dg(d['source_relations'])==d['source_relations_digest'];assert len(d['source_relations'])==31 and len(d['held_claim_ids'])==72
occ={x['requirement_id']:x for x in load(OR/'.cache/a3-corpus-20261006/structured-source-requirements.json')}
walk=load(W/'source/tranche-03/occurrence-crosswalk.json')
for x in walk:
 for o in x['occurrences']:assert dg(occ[o['id']])==o['digest']
assert {x['id'] for x in D['findings']}=={x['finding_id'] for x in d['finding_dispositions']}
report={'structural_result':'PASS','bound_primary_claims_checked':len(primary),'proposed_relations_checked':len(d['source_relations']),'historical_hold_count':len(d['held_claim_ids']),'occurrence_crosswalk_rows_checked':len(walk),'D_findings_dispositioned':len(D['findings']),'semantic_result':'CHANGE_REQUIRED','additional_fidelity_holds':['WA-APPSEC-'+str(i).zfill(3) for i in [74,110,117,120,140,145,149]],'heavy_tests_repeated':False,'reason':'Independent semantic finding; parent observed667 tests already pass. Evidence-only change invokes read-only binding replay and diff check.'}
(O/'replay-results.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
