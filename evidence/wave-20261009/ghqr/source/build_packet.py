"""B's bounded GHQR definitions/scanner review. Inputs read only; no upstream execution."""
import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from ges.core import digest

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
CACHE = Path(sys.argv[1])
sha = lambda b: hashlib.sha256(b).hexdigest()
assignment_bytes = subprocess.check_output(['git', 'show', '18abc10:evidence/wave-20261009/ghqr/assignment.json'], cwd=ROOT)
a = json.loads(assignment_bytes)
docpath = ROOT / a['claim_document']
assert sha(docpath.read_bytes()) == a['claim_document_sha256']
d = json.loads(docpath.read_bytes())
snapshot = CACHE / 'sources/microsoft__ghqr.text.jsonl.gz'
rows = {r['path']:r for r in map(json.loads,gzip.open(snapshot,'rt'))}
source = rows[d['path']]
scanner = rows[a['dependencies'][0]['path']]
assert sha(source['content'].encode()) == d['content_sha256']
assert sha(scanner['content'].encode()) == a['dependencies'][0]['sha256']
occurrence_path = CACHE / 'corpus/structured-source-requirements.json'
occ = {r['requirement_id']:r for r in json.loads(occurrence_path.read_bytes())}
catalog = json.loads((ROOT/'controls/catalog.json').read_bytes())
proposals = json.loads((ROOT/'controls/review_queue.json').read_bytes())
ci = {r['id']:r for r in catalog}
pi = {r['id']:r for r in proposals}

# Individually authored: scanner lines, proposed catalog/proposal refs, judgment, fidelity hold.
judgments = [
 ([16,18],['GES-RULE-003','GES-RULE-004','GES-RULE-008','GES-RULE-007'],[], 'Critical source recommendation covers production-branch protection, direct-push prevention, review and CI. The scanner emits001 and returns when detail is nil or not Protected; it cannot distinguish inaccessible data from absent protection here. Production scope is broader than the input-default-branch description. Composite catalog references preserve components but need exact branch coverage and bypass testing.', 'Original claim omits explicit prevention of direct pushes; source all-component scope requires preservation.'),
 ([54,59],['GES-RULE-004'],['GES-RULE-010'], 'Critical recommendation requires at least1 approving review. Scanner emits002 for count<1 only when reviews exists; count1 instead emits003. Quorum and actual independent review are distinct from configuring a number. Source threshold remains upstream; solo exceptions need explicit local policy.', 'Original claim adds when selected policy requires peer review, weakening the unconditional upstream recommendation; preserve numeric1 and local exception separately.'),
 ([54,59],['GES-RULE-004'],[], 'Medium recommendation considers2 or more approvals for production branches, especially high-risk changes. Scanner emits003 for count1, independently of production risk. This is advisory consideration, not universally mandatory2.', 'Original claim loses numeric2-or-more and narrows production guidance to high-risk changes.'),
 ([61,63],['GES-RULE-005'],['GES-RULE-011'], 'High recommendation enables stale approval dismissal on new commits. Scanner tests the DismissStaleReviews flag; it does not push changes or prove runtime invalidation. Catalog narrows to commits affecting reviewed diff, which needs explicit platform interpretation.', 'Original claim and catalog condition on changed reviewed proposal; source wording says new commits. Preserve source versus platform/local qualification.'),
 ([65,67],['GES-GOV-004'],['GES-RULE-012'], 'Medium recommendation requires designated-owner approval for CODEOWNERS paths. Scanner checks RequireCodeOwnerReviews only. CODEOWNERS existence, valid routing and actual required owner approval are separate; conversation resolution cannot substitute.', 'Original claim says review instead of approval and lacks explicit enabled requirement.'),
 ([54,70],['GES-RULE-003','GES-RULE-004','GES-RULE-005','GES-GOV-004'],['GES-RULE-013'], 'Critical composite requires approval-count configuration, stale dismissal and code-owner reviews. Scanner emits006 only for nil reviews; when present it separately evaluates002-005. PR existence alone cannot cover all components.', None),
 ([72,75],['GES-RULE-008'],[], 'High recommendation enables strict checks so branch is up to date before merge. Scanner emits007 for nonnil statusChecks with Strict false; nil emits009 instead. General right-revision analysis does not implement strict mode.', 'Original claim inserts when strict policy applies, making the upstream strict-mode recommendation conditional; preserve source and local choice separately.'),
 ([76,78],['GES-RULE-008'],[], 'High recommendation configures specific checks that must pass before merge. Scanner tests nonempty Contexts, not successful execution or trusted publisher identity. Names, run revision, actual success gating and bypass all need distinct evidence.', 'Original claim names checks but omits that they must pass before merge.'),
 ([79,81],['GES-RULE-008'],['GES-RULE-014'], 'High recommendation requires CI checks to pass before any PR merge. Scanner emits009 only for nil statusChecks; a configured object does not prove actual successful runs or native rejection. Catalog execution revision alone does not fully state success enforcement.', None),
 ([83,85],['GES-RULE-002'],['GES-RULE-015'], 'Critical recommendation disables force pushes on all protected branches. Scanner checks AllowForcePushes on supplied detail only; false does not prove effective denial for bypass principals or every branch. Canonical per-instance rejection supports meaning but full branch denominator remains explicit.', None),
 ([87,89],['GES-RULE-001'],['GES-RULE-016'], 'High recommendation disables deletion on all protected branches. Scanner checks AllowDeletions for supplied detail only. Keep topic-branch cleanup separate and verify bypass/target coverage; a false flag is not an exercised native denial.', None),
 ([91,93],['GES-RULE-009'],[], 'Medium recommendation enables signed commits for every commit merged into default. Scanner checks RequiredSignatures, not cryptographic verification. Source attribution claim overstates human authorship assurance; preserve that disputed assertion and explicit trust assumptions as an unresolved source/platform conflict.', 'Original claim changes enable required signatures into evaluate; legitimate local policy choice must not erase upstream recommendation or authorship overclaim.'),
 ([95,97],['GES-RULE-009','GES-BR-003'],[], 'Low recommendation considers squash or rebase for linear history. Scanner tests RequiredLinearHistory, not selected merge methods or readability/bisect outcomes. Preserve advisory modality, alternatives and local delivery/audit decision; no external tmcw conflict certified in this bounded read.', 'Original claim omits squash/rebase alternatives; its delivery/audit condition is local interpretation.'),
 ([26,40],['GES-RULE-007'],[], 'Informational014 is emitted only for nonnil ruleset detail marked Protected; shared settings are then evaluated and may still fail. Nil/unprotected ruleset detail returns nil, not PASS. Source no-action statement and optional migration advice do not prove active enforcement, inheritance or bypass coverage.', 'Original claim omits optional migration consideration; preserve it as source context without making redundant legacy rules mandatory.'),
]
primary, drafts, crosswalk = [], [], []
assert len(judgments)==14
for claim,(span,cids,pids,meaning,hold) in zip(a['claims'],judgments):
    oid='SRC-GHQR-'+claim['source_id']
    o=occ[oid]
    assert o['content_sha256']==d['content_sha256'] and o['start_line']==claim['start_line']
    subject={k:claim[k] for k in ('claim_id','start_line','end_line')}
    subject.update(source=d['source'],commit=d['commit'],path=d['path'],artifact_id=o['artifact_id'],content_sha256=d['content_sha256'],statement_sha256=sha(claim['statement'].encode()),claim_document=docpath.name,claim_document_sha256=sha(docpath.read_bytes()))
    refs=[{'id':i,'revision':ci[i]['revision'],'collection':'CATALOG'} for i in cids]+[{'id':i,'revision':pi[i]['revision'],'collection':'PROPOSAL'} for i in pids]
    source_definition=o['source_definition']
    primary.append({'claim':subject,'occurrence_id':oid,'occurrence_digest':digest(o),'scanner_span':{'start_line':span[0],'end_line':span[1],'content_sha256':scanner['sha256']},'source_severity':source_definition['severity'],'source_recommendation_sha256':sha(source_definition['recommendation'].encode()),'interpretation':meaning,'source_fidelity_hold':hold,'control_references':refs,'primary_identity':'codex:/root/source_worker_b','status':'PROPOSED_PENDING_D_A_E'})
    # Only records supported by an existing proposal can project SPECIALIZE.
    # Others stay explicit bounded unresolved needs, never fake REFERENCE receipts.
    drafts.append({'claim':subject,'proposed_disposition':'SPECIALIZE' if pids else None,'control_references':refs,'details':{'scope':'Source recommendation and supplied detail; all-protected/production/default branch scopes remain distinct.','distinction':meaning},'rationale':meaning,'status':'PROPOSED_NOT_RECEIPT' if pids else 'UNRESOLVED_CANONICAL_OR_PROPOSAL_DECISION_REQUIRED','primary_reviewer':'codex:/root/source_worker_b','accepted_policy':False,'adopted_obligation':None,'hold_for_fidelity_repair':bool(hold)})
    crosswalk.append({'claim':subject,'occurrence_id':oid,'occurrence_digest':digest(o),'source_span_sha256':o['span_sha256']})
def write(name,obj):
    (OUT/name).write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')
write('primary-review.json',primary)
write('draft-dispositions.json',drafts)
write('occurrence-crosswalk.json',crosswalk)
write('residuals.json',{'primary_claims':14,'primary_occurrences':14,'unreviewed_assigned_claim_ids':[],'completed_reconciliation_receipts':0,'fidelity_hold_ids':[r['claim']['claim_id'] for r in primary if r['source_fidelity_hold']],'remaining_scope':['D omission review, A reconciliation, E independent audit.','Collector/default-branch acquisition and ruleset aggregation outside this scanner file not read or certified.','Boolean configuration findings do not establish native enforcement, runtime approval correctness, check success or bypass coverage.','Catalog/proposal decisions and source fidelity repairs remain unapproved; severity and numeric thresholds are upstream, not adopted policy.','No human approvals, publication clearance, native execution or corpus completeness.']})
write('input-bindings.json',{'assignment_commit':'18abc10','assignment_sha256':sha(assignment_bytes),'claim_document_sha256':sha(docpath.read_bytes()),'snapshot_compressed_sha256':sha(snapshot.read_bytes()),'source_sha256':source['sha256'],'scanner_sha256':scanner['sha256'],'scanner_read_lines':[1,98],'definitions_read_lines':[1,153],'catalog_digest':digest(catalog),'proposal_digest':digest(proposals),'structured_ledger_sha256':sha(occurrence_path.read_bytes()),'primary_identity':'codex:/root/source_worker_b'})
write('packet-manifest.json',{'files':[{'path':p.name,'sha256':sha(p.read_bytes())} for p in sorted(OUT.glob('*.json')) if p.name!='packet-manifest.json'],'primary_projection_digest':digest(primary),'draft_projection_digest':digest(drafts),'state':'STAGED_PRIMARY_PENDING_D_A_E'})
print(json.dumps({'primary_claims':len(primary),'source_fidelity_holds':sum(bool(r['source_fidelity_hold']) for r in primary),'primary_digest':digest(primary),'draft_digest':digest(drafts)}))
