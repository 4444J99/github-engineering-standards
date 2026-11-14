"""Project only E-audited A decisions, preserving the original receipt prefix."""
import copy
import hashlib
import json
from pathlib import Path

from ges.core import digest

ROOT = Path(__file__).resolve().parents[2]
WAVE = ROOT / 'evidence/wave-20261009'
OUT = WAVE / 'integration'


def read(path):
    return json.loads((ROOT / path).read_text())


packages = read('evidence/wave-20261009/integration/packages.json')
old_path = 'evidence/secret-context-continuation-20261008-reconciliation.json'
policy_path = 'evidence/secret-context-continuation-20261008-policy.json'
original = read(old_path)
policy = read(policy_path)
new = []
observations = []
for package in packages:
    decisions = read(package['decisions'])
    audit = read(package['audit'])
    assert audit['verdict'] == 'PASS'
    expected = {row['claim']['claim_id'] for row in decisions['source_relations']}
    assert set(audit['approved_claim_ids']) == expected
    roles = {'codex:/root/source_worker_b', 'codex:/root/omission_reviewer_d',
             'codex:/root', 'codex:/root/decision_auditor_e'}
    for path, expected_sha in package['bindings'].items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == expected_sha
    for row in decisions['source_relations']:
        actual_roles = {row['primary_reviewer'], row['omission_reviewer'],
                        row['reconciler'], row['decision_auditor_required']}
        assert actual_roles == roles and len(actual_roles) == 4
        receipt = {key: copy.deepcopy(row[key]) for key in
                   ('claim', 'disposition', 'control_references', 'details', 'rationale')}
        receipt.update({
            'schema': 'ges.claim-reconciliation-receipt.v1',
            **{key: policy[key] for key in
               ('claim_input_digest', 'catalog_digest', 'proposal_digest')},
            'reconciler': 'codex:/root',
            'independent_reviewer': 'codex:/root/decision_auditor_e',
            'reconciled_at': decisions['reconciled_at'],
            'reviewed_at': audit['reviewed_at'],
            'accepted_policy': False, 'adopted_obligation': None})
        new.append(receipt)
    observations.append({'decisions': package['decisions'], 'audit': package['audit'],
                         'new_receipts': len(expected),
                         'held_claim_ids': decisions['held_claim_ids']})
all_ids = [row['claim']['claim_id'] for row in original + new]
assert len(set(all_ids)) == len(all_ids)
policy['authorized_reconcilers'].append('codex:/root')
policy['authorized_independent_reviewers'].append('codex:/root/decision_auditor_e')
policy['approval_reference'] += (
    ' User instruction 2026-10-09, Next: parallel reviews, serialized integration, '
    'explicitly authorizes B primary, D omission reviewer, A reconciler and E '
    'decision auditor as distinct automated runtime roles for the frozen bounded '
    'assignment. The packages.json bindings identify their actual reviewed scope. '
    'This extension grants no human review, policy adoption, publication clearance, '
    'distribution authorization, native execution or organization acceptance.')
for name, value in [('new-receipts.json', new),
                    ('combined-reconciliation.json', original + new),
                    ('combined-policy.json', policy),
                    ('receipt-projection.json', {
                        'schema': 'ges.bounded-receipt-projection.v1',
                        'original_receipts': len(original), 'new_receipts': len(new),
                        'combined_receipts': len(original) + len(new),
                        'original_prefix_unchanged': True,
                        'original_receipts_digest': digest(original),
                        'new_receipts_digest': digest(new),
                        'packages': observations,
                        'completed_objective_synthesis_credit': 0,
                        'accepted_controls': 0})]:
    (OUT / name).write_text(json.dumps(value, indent=2) + '\n')
print(json.dumps({'old': len(original), 'new': len(new), 'total': len(original) + len(new)}))
