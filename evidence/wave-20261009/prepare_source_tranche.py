"""Serialize explicitly reviewed source-only decisions after D, before E."""
import copy
import hashlib
import json
from pathlib import Path
import sys

from ges.core import now, digest

ROOT = Path(__file__).resolve().parents[2]
tranche = sys.argv[1]
assert tranche in ('tranche-02', 'tranche-03')
base = 'evidence/wave-20261009/'
source = base + 'source/' + tranche + '/'
omission = base + 'omission/' + tranche + '/'
output = ROOT / (base + 'integration/' + tranche)
output.mkdir(exist_ok=True)
read = lambda path: json.loads((ROOT / path).read_text())
drafts = read(source + 'draft-dispositions.json')
findings = read(omission + 'source-findings.json')
approved = {row['claim_id'] for row in findings['claim_findings']
            if row['verdict'] == 'SUPPORTED_BOUNDED_RELATION'}
held = {row['claim_id'] for row in findings['claim_findings'] if row['verdict'] == 'HOLD'}
assert approved.isdisjoint(held)
assert approved | held == {row['claim']['claim_id'] for row in drafts}
relations = []
for draft in drafts:
    if draft['claim']['claim_id'] not in approved:
        continue
    row = {key: copy.deepcopy(draft[key]) for key in
           ('claim', 'control_references', 'details', 'rationale')}
    row.update({'disposition': draft['proposed_disposition'],
                'primary_reviewer': 'codex:/root/source_worker_b',
                'omission_reviewer': 'codex:/root/omission_reviewer_d',
                'reconciler': 'codex:/root',
                'decision_auditor_required': 'codex:/root/decision_auditor_e',
                'objective_synthesis_complete': False,
                'accepted_policy': False, 'adopted_obligation': None})
    relations.append(row)
paths = [source + name for name in ('draft-dispositions.json', 'primary-review.json',
                                    'input-bindings.json', 'residuals.json',
                                    'packet-manifest.json')]
paths += [omission + 'source-findings.json', 'controls/catalog.json',
          'controls/review_queue.json', base + 'assignment.json']
bindings = [{'path': path, 'sha256': hashlib.sha256((ROOT / path).read_bytes()).hexdigest()}
            for path in paths]
decisions = {
    'schema': 'ges.bounded-integration-proposed-decisions.v1',
    'state': 'PROPOSED_PENDING_E_AUDIT', 'tranche': tranche,
    'baseline': '7af46c827565d4746daed9ed1a9206524c944f70',
    'reconciler': 'codex:/root', 'reconciled_at': now(), 'bindings': bindings,
    'source_relations': relations, 'source_relations_digest': digest(relations),
    'held_claim_ids': sorted(held),
    'finding_dispositions': [
        {'finding_id': row['id'], 'claim_id': row.get('claim_id'),
         'action': ('HOLD_NO_RECEIPT_OR_FIDELITY_CREDIT' if row.get('claim_id') else
                    'KEEP_MISSING_OBJECTIVES_AND_OPERATIONAL_BINDINGS_UNRESOLVED'),
         'required_action': row['required_action']} for row in findings['findings']],
    'source_coverage': {'assigned_claims': 162, 'reviewed_in_tranche': len(drafts),
                        'proposed_relation_receipts': len(relations), 'held': len(held),
                        'completed_objective_synthesis_credit': 0},
    'scope_boundaries': [
        'These are source relations to exact existing draft proposal revisions, not completed control objectives or implementation.',
        'Every historical fidelity defect remains held, with original claims and primary packet preserved.',
        'Source recommendation strength, actor, cadence and applicability remain source context; no adopted policy.',
        'Four actual automated runtime roles are authorized by the user; human review and acceptance are not asserted.',
        'Other tranches, publication clearance, cross-source synthesis and native execution remain outside this subject.'
    ]}
(output / 'proposed-decisions.json').write_text(json.dumps(decisions, indent=2) + '\n')
print(json.dumps({'tranche': tranche, 'relations': len(relations), 'held': len(held)}))
