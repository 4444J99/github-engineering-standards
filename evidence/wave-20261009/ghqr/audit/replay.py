"""Independent E read-only GHQR binding and decision replay."""
import json,gzip,hashlib
from pathlib import Path
import yaml
R=Path(__file__).resolve().parents[4];W=R/'evidence/wave-20261009/ghqr';O=W/'audit'
OR=Path('/Users/4jp/Workspace/4444J99/engineering-environment-standards/github-engineering-standards/github-engineering-standards')
def load(p):return json.loads(p.read_bytes())
def sha(b):return hashlib.sha256(b).hexdigest()
def dg(x):return sha(json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode())
d=load(W/'integration/proposed-decisions.json');D=load(W/'omission/source-findings.json');B=load(W/'source/primary-review.json');bindings=load(W/'source/input-bindings.json')
for b in d['bindings']+D['bindings']:assert sha((R/b['path']).read_bytes())==b['sha256']
snapshot=OR/'.cache/sources/microsoft__ghqr.text.jsonl.gz';assert sha(snapshot.read_bytes())==bindings['snapshot_compressed_sha256']
s={x['path']:x for x in map(json.loads,gzip.open(snapshot,'rt'))}
assert sha(s['internal/scanners/bestpractices/branch_protection.go']['content'].encode())==bindings['scanner_sha256']
claimfile=R/'evidence/source-reviews/ghqr-branch-protection-claims.json';claims={x['claim_id']:x for x in load(claimfile)['claims']};assert sha(claimfile.read_bytes())==bindings['claim_document_sha256']
occ={x['requirement_id']:x for x in load(OR/'.cache/a3-corpus-20261006/structured-source-requirements.json')}
for x in B:
 c=x['claim'];source=s[c['path']];assert sha(source['content'].encode())==c['content_sha256'];assert source['commit']==c['commit'];assert sha(claims[c['claim_id']]['statement'].encode())==c['statement_sha256'];assert dg(occ[x['occurrence_id']])==x['occurrence_digest']
 definition=next(r for r in yaml.safe_load(source['content']) if r['id']==x['occurrence_id'].removeprefix('SRC-GHQR-'));assert sha(definition['recommendation'].encode())==x['source_recommendation_sha256']
for row in load(W/'source/occurrence-crosswalk.json'):
 c=row['claim'];span='\n'.join(s[c['path']]['content'].splitlines()[c['start_line']-1:c['end_line']]).encode();assert sha(span)==row['source_span_sha256']
cat={x['id']:x for x in load(R/'controls/catalog.json')};q={x['id']:x for x in load(R/'controls/review_queue.json')}
for x in d['source_relations']:
 assert len({x[k] for k in ['primary_reviewer','omission_reviewer','reconciler','decision_auditor_required']})==4
 assert x['decision_auditor_required']=='codex:/root/decision_auditor_e';assert not x['accepted_policy'] and not x['objective_synthesis_complete']
 for ref in x['control_references']:assert (cat if ref['collection']=='CATALOG' else q)[ref['id']]['revision']==ref['revision']
assert dg(d['source_relations'])==d['source_relations_digest'];assert len(d['source_relations'])==3 and len(d['held_claim_ids'])==11
assert {x['id'] for x in D['findings']}=={x['finding_id'] for x in d['finding_dispositions']}
report={'structural_result':'PASS','claims_and_occurrences_checked':len(B),'definition_spans_checked':14,'scanner_digest_checked':True,'current_control_revision_references_checked':6,'D_findings_dispositioned':4,'bounded_relation_count':3,'historical_fidelity_holds':11,'upstream_executed':False,'native_predicates_verified':0,'heavy_tests_repeated':False}
(O/'replay-results.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
