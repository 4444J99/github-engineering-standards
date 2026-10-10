"""Serialize A's explicit bounded decisions; never infer mappings or approvals."""
import copy
import hashlib
import json
from pathlib import Path

from ges.core import now, digest

ROOT = Path(__file__).resolve().parents[2]
WAVE = ROOT / 'evidence/wave-20261009'
OUT = WAVE / 'integration'
OUT.mkdir(exist_ok=True)


def read(path):
    return json.loads((ROOT / path).read_text())


def write(name, value):
    (OUT / name).write_text(json.dumps(value, indent=2) + '\n')


def binding(path):
    raw = (ROOT / path).read_bytes()
    return {'path': path, 'sha256': hashlib.sha256(raw).hexdigest()}


source_d = read('evidence/wave-20261009/omission/source-findings.json')
pub_d = read('evidence/wave-20261009/omission/publication-findings.json')
drafts = read('evidence/wave-20261009/source/draft-dispositions.json')
pub = read('evidence/wave-20261009/publication/primary-review.json')
approved = {row['claim_id'] for row in source_d['claim_findings']
            if row['verdict'] == 'SUPPORTED_BOUNDED_RELATION'}
held = {row['claim_id'] for row in source_d['claim_findings']
        if row['verdict'] == 'HOLD'}
assert len(approved) == 13 and len(held) == 5
assert approved.isdisjoint(held)
relations = []
for draft in drafts:
    if draft['claim']['claim_id'] not in approved:
        continue
    row = {key: copy.deepcopy(draft[key]) for key in
           ('claim', 'control_references', 'details', 'rationale')}
    row['disposition'] = draft['proposed_disposition']
    row['primary_reviewer'] = 'codex:/root/source_worker_b'
    row['omission_reviewer'] = 'codex:/root/omission_reviewer_d'
    row['reconciler'] = 'codex:/root'
    row['decision_auditor_required'] = 'codex:/root/decision_auditor_e'
    row['objective_synthesis_complete'] = False
    row['accepted_policy'] = False
    row['adopted_obligation'] = None
    relations.append(row)

fields = ('use_id', 'kind', 'source', 'source_range', 'output_path',
          'output_range', 'attributions', 'rationale')
uses = [{key: copy.deepcopy(row[key]) for key in fields}
        for row in pub['uses'] if row['kind'] in ('LICENSED_COPY', 'REFERENCES_ONLY')]
assert len(uses) == 198
packet = 'evidence/publication-candidates/ges-v0.2-merged-f628db26-20261008/'
register = read(packet + 'register.json')
register['prepared_at'] = now()
register['uses'] = uses
source_ids = sorted({row['source']['artifact_id'] for row in uses})
register['source_evidence'] = [
    {'artifact_id': aid, 'format': 'SNAPSHOT_TEXT',
     'path': pub['source_snapshot']['path'],
     'sha256': pub['source_snapshot']['sha256']} for aid in source_ids]
for output in register['outputs']:
    output['use_ids'] = [row['use_id'] for row in uses
                         if row['output_path'] == output['path']]
    if output['use_ids']:
        output['rationale'] = (
            'Partial review of 50 selected proposal objects; 198 bounded classified '
            'uses recorded. Two escaped fields and all remaining expression review '
            'remain unresolved. This output remains UNREVIEWED; no clearance.')
    assert output['disposition'] == 'UNREVIEWED'
write('publication-register.json', register)
write('publication-policy.json', {})
write('publication-receipts.json', [])

finding_dispositions = []
for finding in source_d['findings']:
    action = ('HOLD_NO_RECEIPT_OR_FIDELITY_CREDIT' if finding.get('claim_id')
              else 'RETAIN_UNRESOLVED_OBJECTIVE_AND_BINDING_WORK')
    finding_dispositions.append({'finding_id': finding['id'], 'action': action,
                                 'claim_id': finding.get('claim_id'),
                                 'required_action': finding['required_action']})
for finding in pub_d['findings']:
    finding_dispositions.append({
        'finding_id': finding['id'],
        'action': ('KEEP_TWO_USE_CLASSIFICATIONS_UNRESOLVED' if
                   finding['id'] == 'D-PUBLICATION-ESCAPING' else
                   'KEEP_ALL_OUTPUTS_UNREVIEWED_AND_APPROVALS_EMPTY'),
        'required_action': finding['required_action']})
paths = [
    'evidence/wave-20261009/assignment.json',
    'evidence/wave-20261009/cache-validation.json',
    'evidence/wave-20261009/source/packet-manifest.json',
    'evidence/wave-20261009/source/primary-review.json',
    'evidence/wave-20261009/source/draft-dispositions.json',
    'evidence/wave-20261009/source/residuals.json',
    'evidence/wave-20261009/publication/primary-review.json',
    'evidence/wave-20261009/omission/source-findings.json',
    'evidence/wave-20261009/omission/publication-findings.json',
    'evidence/wave-20261009/integration/publication-register.json',
    'controls/catalog.json', 'controls/review_queue.json']
decisions = {
    'schema': 'ges.bounded-integration-proposed-decisions.v1',
    'state': 'PROPOSED_PENDING_E_AUDIT', 'reconciler': 'codex:/root',
    'reconciled_at': now(), 'baseline': '7af46c827565d4746daed9ed1a9206524c944f70',
    'bindings': [binding(path) for path in paths],
    'source_relations': relations, 'source_relations_digest': digest(relations),
    'held_claim_ids': sorted(held),
    'source_unit': 'Existing claim identity; occurrences are a parallel crosswalk, not additive propositions.',
    'source_coverage': {'assigned_claims': 162, 'primary_and_omission_reviewed': 18,
                        'proposed_relation_receipts': 13, 'held': 5,
                        'remaining_primary_scope': 144,
                        'completed_objective_synthesis_credit': 0},
    'publication': {'candidate_revision': pub['candidate_revision'],
                    'selected_proposals': 50, 'complete_proposal_denominator': 593,
                    'classified_uses': 198, 'unresolved_uses': pub['unresolved_findings'],
                    'all_output_denominator': 2396, 'outputs_unreviewed': 2396,
                    'policy': {}, 'receipts': [], 'clearance': None},
    'finding_dispositions': finding_dispositions,
    'scope_boundaries': [
        'SPECIALIZE records a source relation to an existing quarantined proposal; missing objectives, applicability, source-hash repair and operational bindings remain unresolved.',
        'Primary preserved_fields/lost_fields are proposed treatment, not proof of retention in the canonical catalog.',
        'Five historical fidelity defects remain unchanged and receive no new reconciliation receipts.',
        'The automated roles are distinct actual collaborating runtime tasks authorized by the user; no independent human identity is asserted.',
        'No owner acceptance, adoption, distribution approval, publication, or native execution. Later tranches need separate digest-bound D/A/E review.'
    ]}
write('proposed-decisions.json', decisions)
print(json.dumps({'relations': len(relations), 'uses': len(uses),
                  'decision_file': binding('evidence/wave-20261009/integration/proposed-decisions.json')}))
