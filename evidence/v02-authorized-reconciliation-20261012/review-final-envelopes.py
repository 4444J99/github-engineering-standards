"""Actual scoped agent review; run only by named reviewer under the owner grant."""
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from ges.claim_reconciliation import RECEIPT_FIELDS, SUBJECT_FIELDS
from ges.core import digest, timestamp

ROOT = Path('/workspace/scratch/2aefcbff59bd/ges')
EVIDENCE = ROOT / 'evidence/v02-authorized-reconciliation-20261012'
DRAFT = Path('/workspace/scratch/9f3cdabec13b/ges/.cache/cloud-replay-20261012/replacement-draft/replacement-decisions.draft.json')
PENDING = ROOT / '.cache/reconciliation-issued-20261012/issued-pending-review.json'
FINAL = PENDING.with_name('issued-reviewed.json')
ACTOR = 'chatgpt-cloud:20261012:2aefcbff59bd:/root/envelope_review'
RECONCILER = 'chatgpt-cloud:20261012:2aefcbff59bd:/root'
started = datetime.now(timezone.utc).isoformat()
inputs = {}
checks = 0

def require(value, message):
    global checks
    if not value:
        raise ValueError(message)
    checks += 1

def read(path, expected=None):
    require(path.is_file() and not any(p.is_symlink() for p in (path, *path.parents)), 'Regular unsymlinked file required')
    raw = path.read_bytes()
    sha = hashlib.sha256(raw).hexdigest()
    require(expected is None or sha == expected, 'Hash mismatch: ' + str(path))
    inputs[str(path)] = sha
    return raw

def load(path, expected=None):
    return json.loads(read(path, expected))

grant = load(EVIDENCE / 'owner-authorization.json', '72b8510137eb0de5c12095a816f48cc2f3cf21c94df5b7331c0b56e79e2c8ed0')
policy_path = EVIDENCE / 'claim-reconciliation-policy.json'
policy = load(policy_path, '06e34189c0d9a30d3d7a592e3e229ded0c22452a47f656e5bcae1e5bdb994f98')
issuance = load(EVIDENCE / 'issuance.json')
prior_path = ROOT / 'evidence/v02-cloud-replay-20261012/independent-decision-review.json'
prior = load(prior_path)
draft_raw = read(DRAFT, 'a8b9065b0a5a43e950451683badcbeaa335cc344bbce78940dac4420fb6d7185')
draft = json.loads(draft_raw)
pending = load(PENDING, '31e2b25ad9c95f62d7c839aee61c9fd44ebf07a2f6078345531daefb8407feee')
require(grant['owner_reply'] == 'Approve scoped issuance and independent review', 'Owner scope reply')
require(grant['authorized_reconciler'] == RECONCILER and grant['authorized_independent_reviewer'] == ACTOR and ACTOR != RECONCILER, 'Granted actual actors')
require(policy['authorized_reconcilers'] == [RECONCILER] and policy['authorized_independent_reviewers'] == [ACTOR], 'Policy actual actors')
require('owner-authorization.json' in policy['approval_reference'], 'Policy grant reference')
require(grant['draft_sha256'] == inputs[str(DRAFT)] == issuance['draft_sha256'] == prior['draft_sha256'], 'Exact draft grant and earlier review')
require(digest(draft) == grant['draft_canonical_digest'] == prior['draft_canonical_digest'], 'Draft canonical binding')
require(issuance['grant_sha256'] == inputs[str(EVIDENCE / 'owner-authorization.json')] and issuance['policy_sha256'] == inputs[str(policy_path)], 'Issuance grant binding')
require(issuance['pending_ledger_sha256'] == inputs[str(PENDING)] and issuance['issued_by'] == RECONCILER, 'Issuance ledger binding')
require(prior['status'] == 'PASS_EXACT_CARRYFORWARD_AND_TEN_DRAFT_DISPOSITIONS' and not prior['material_findings'], 'Prior independent review disposition')
require(prior['carried_decisions_compared'] == 2164 and prior['new_predecessor_supersessions'] == prior['new_successor_specializations'] == 5, 'Prior review scope')
require(len(draft) == len(pending) == issuance['decisions'] == 2174, 'Exact count')
index = {r['claim']['claim_id']: r for r in draft}
require(len(index) == len(draft), 'Unique draft membership')
seen = set()
fields = RECEIPT_FIELDS - {'schema', 'reconciler', 'reconciled_at', 'independent_reviewer', 'reviewed_at'}
compared = 0
subject_fields = 0
for r in pending:
    require(set(r) == RECEIPT_FIELDS and r['schema'] == 'ges.claim-reconciliation-receipt.v1', 'Issued schema')
    cid = r['claim']['claim_id']
    require(cid in index and cid not in seen, 'Exact unique membership')
    d = index[cid]
    require(d['schema'] == 'ges.claim-reconciliation-receipt.draft.v1' and all(d[k] is None for k in ('reconciler','reconciled_at','independent_reviewer','reviewed_at')), 'Nonissued draft')
    require(set(r['claim']) == set(SUBJECT_FIELDS), 'Exact subject shape')
    for key in SUBJECT_FIELDS:
        require(digest(r['claim'][key]) == digest(d['claim'][key]), 'Subject changed: '+cid+':'+key)
        subject_fields += 1
    for key in fields:
        require(digest(r[key]) == digest(d[key]), 'Decision changed: '+cid+':'+key)
        compared += 1
    for key in ('claim_input_digest','catalog_digest','proposal_digest'):
        require(r[key] == grant[key] == policy[key], 'Grant binding changed')
    require(r['accepted_policy'] is False and r['adopted_obligation'] is None, 'Nonadoption')
    require(r['reconciler'] == RECONCILER and r['reconciled_at'] == issuance['issued_at'], 'Actual issuance fields')
    require(timestamp(grant['recorded_at']) <= timestamp(r['reconciled_at']) <= datetime.now(timezone.utc), 'Actual ordered issuance')
    require(r['independent_reviewer'] is None and r['reviewed_at'] is None, 'Pending review fields must be null')
    seen.add(cid)
require(seen == set(index), 'Complete membership')
for finding in prior['source_semantic_review']['findings']:
    for prefix, field in (('predecessor','predecessor_draft_canonical_digest'),('successor','successor_draft_canonical_digest')):
        require(digest(index[finding[prefix]]) == finding[field], 'Ten decision prior review binding')
    pred, succ = index[finding['predecessor']], index[finding['successor']]
    require(pred['disposition'] == 'EXCLUDED_WITH_REASON' and pred['details']['basis'] == 'SUPERSEDED' and pred['details']['related_claim_ids'] == [finding['successor']], 'Supersession')
    require(succ['disposition'] == 'SPECIALIZE' and succ['control_references'] == [dict(collection='CATALOG', id=finding['catalog']['id'], revision=1),dict(collection='PROPOSAL', id=finding['proposal']['id'], revision=1)], 'Specialization')
for path, sha in inputs.items():
    require(hashlib.sha256(Path(path).read_bytes()).hexdigest() == sha, 'Input changed during review')
reviewed_at = datetime.now(timezone.utc).isoformat()
for row in pending:
    row['independent_reviewer'] = ACTOR
    row['reviewed_at'] = reviewed_at
with FINAL.open('x') as stream:
    json.dump(pending, stream, indent=2, sort_keys=True)
    stream.write('\n')
command = [sys.executable, '-m', 'ges.reconciliation_envelopes', '--draft', str(DRAFT), '--draft-sha256', grant['draft_sha256'], '--receipts', str(FINAL), '--policy', str(policy_path)]
result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=30)
require(result.returncode == 0, 'Final comparator failed: ' + result.stderr + result.stdout)
comparison_path = EVIDENCE / 'envelope-comparison.json'
with comparison_path.open('x') as stream:
    stream.write(result.stdout)
comparison = json.loads(result.stdout)
require(comparison['valid'] and comparison['compared_decisions'] == 2174, 'Final comparison count')
report = dict(schema='ges.independent-authorized-final-envelope-review.v1', status='PASS_EXACT_AUTHORIZED_FINAL_ENVELOPES', reviewer=ACTOR, reconciler=RECONCILER, started_at=started, reviewed_at=reviewed_at, completed_at=datetime.now(timezone.utc).isoformat(), checks_passed=checks, decisions=2174, subject_field_comparisons=subject_fields, substantive_field_comparisons=compared, input_sha256=inputs, final_ledger_sha256=hashlib.sha256(FINAL.read_bytes()).hexdigest(), final_ledger_canonical_digest=digest(pending), comparison_sha256=hashlib.sha256(comparison_path.read_bytes()).hexdigest(), script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), command=command, script_command=['timeout','60s',sys.executable,str(Path(__file__))], findings=[], source_acquisition_repeated=False, accounting_performed=False, human_approval=False, release_acceptance=False, semantic_review_reused=True, limits=['Actual scoped agent final-envelope review under the direct owner grant; this is not human approval, release acceptance, or identity-provider authentication.', 'Reuses prior independent semantic review of ten dispositions and preservation review of 2164 carried decisions; no fresh semantic adjudication of all carried decisions or source replay.', 'Actual review timestamps generated after complete comparison; issuance actor and timestamps preserved. Script runtime timestamps cover mechanical checks; manual reading of grant, prior review reasoning and ten decisions preceded this execution.'])
with (EVIDENCE / 'independent-envelope-review.json').open('x') as stream:
    json.dump(report, stream, indent=2, sort_keys=True)
    stream.write('\n')
print(json.dumps({k:v for k,v in report.items() if k != 'input_sha256'}, indent=2))
