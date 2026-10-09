"""Serialize explicitly authored judgments 060-162 without granting approvals."""
import gzip
import hashlib
import json
import sys
from pathlib import Path
from ges.core import digest
from ges.semantics import stable_id, validate_record

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[3]
CACHE = Path(sys.argv[1])
sha = lambda b: hashlib.sha256(b).hexdigest()
a_path = ROOT / 'evidence/wave-20261009/assignment.json'
a = json.loads(a_path.read_bytes())
catalog = json.loads((ROOT / 'controls/catalog.json').read_bytes())
proposals = json.loads((ROOT / 'controls/review_queue.json').read_bytes())
ci, pi = {r['id']: r for r in catalog}, {r['id']: r for r in proposals}
crosswalk_path = OUT.parent / 'occurrence-crosswalk.json'
cw = {r['claim']['claim_id']: r for r in json.loads(crosswalk_path.read_bytes())}
snapshot = CACHE / 'sources/github__github-well-architected.text.jsonl.gz'
rows = {r['path']: r for r in map(json.loads, gzip.open(snapshot, 'rt'))}
source = rows['content/library/application-security/checklist.md']
assert sha(source['content'].encode()) == 'd460c2c2daf45d6914cc15b908f1e487d0e4afe8e28632706b58ccddaab27773'
authored = [line.split('|') for line in (OUT / 'judgments.txt').read_text().splitlines() if line.strip()]
assert len(authored) == 103 and all(len(r) == 4 for r in authored)
decisions, primary, drafts, crosswalk = [], [], [], []
for claim, (number, catalog_id, rationale, defect) in zip(a['B']['claims'][59:], authored):
    n = int(number)
    assert claim['claim_id'] == f'WA-APPSEC-{n:03d}'
    subject = cw[claim['claim_id']]['claim']
    proposal_id = f'GES-OPS-{n + 36:03d}'
    proposal = pi[proposal_id]
    assert proposal['sources'][0]['start_line'] == claim['start_line']
    refs = [{'id': proposal_id, 'revision': proposal['revision']}]
    if catalog_id:
        refs.insert(0, {'id': catalog_id, 'revision': ci[catalog_id]['revision']})
    scope = ('General security-awareness and communication practice.' if n < 66 else 'Additional checklist items for GitHub Enterprise deployments; distinguish Cloud, Server, relevant workload and capability before local adoption.')
    record = {'schema': 'ges.reconciliation-decision.v1', 'proposition_ids': [claim['claim_id']], 'disposition': 'SPECIALIZATION', 'source_treatment': 'RETAINED', 'control_references': refs, 'rationale': rationale, 'preserved_fields': [], 'lost_fields': [], 'conflicts': [], 'review': {'status': 'PROPOSED', 'reviewer': None, 'evidence_reference': None}}
    record['id'] = stable_id(record)
    validate_record(record)
    decisions.append(record)
    primary.append({'claim': subject, 'decision_id': record['id'], 'primary_identity': 'codex:/root/source_worker_b', 'source_scope': scope, 'interpretation': rationale, 'source_fidelity_defect': defect or None, 'source_span_sha256': sha('\n'.join(source['content'].splitlines()[claim['start_line']-1:claim['end_line']]).encode()), 'proposal_record_digest': digest(proposal), 'related_catalog_record_digest': digest(ci[catalog_id]) if catalog_id else None, 'status': 'PROPOSED_PENDING_D_A_E', 'original_claim_unchanged': True})
    drafts.append({'claim': subject, 'proposed_disposition': 'SPECIALIZE', 'control_references': [{'id': r['id'], 'revision': r['revision'], 'collection': 'CATALOG' if r['id'] in ci else 'PROPOSAL'} for r in refs], 'details': {'scope': scope, 'distinction': rationale}, 'rationale': rationale, 'primary_reviewer': 'codex:/root/source_worker_b', 'accepted_policy': False, 'adopted_obligation': None, 'status': 'PROPOSED_NOT_RECONCILIATION_RECEIPT', 'hold_for_source_fidelity_repair': bool(defect)})
    crosswalk.append({**cw[claim['claim_id']], 'primary_review_status': 'REVIEWED_PROPOSED_TRANCHE_03'})

def write(name, obj):
    (OUT / name).write_text(json.dumps(obj, indent=2, sort_keys=True) + '\n')

write('proposed-decisions.json', decisions)
write('primary-review.json', primary)
write('draft-dispositions.json', drafts)
write('occurrence-crosswalk.json', crosswalk)
write('residuals.json', {'tranche_primary_claim_count': 103, 'tranche_occurrence_count': 103, 'proposed_specializations': 103, 'proposed_maps': 0, 'source_fidelity_holds': [r['claim']['claim_id'] for r in primary if r['source_fidelity_defect']], 'primary_reviewed_claims_after_three_tranches': 162, 'primary_reviewed_occurrences_after_three_tranches': 162, 'primary_unreviewed_claim_ids': [], 'validated_reconciliation_receipts_added': 0, 'reported_additional_tranche02_holds': ['WA-APPSEC-020: parent reports E found deployment scope narrows organization obligations; original packet preserved, A must bind revised decision and new audit.', 'WA-APPSEC-035: D reports original paraphrase omits threat-modeling exercises and potential-vulnerability identification; original packet preserved.'], 'remaining_scope': ['D must independently review tranche03 and may add omissions or fidelity holds.', 'A must reconcile proposed dispositions and all D findings; E must independently audit decisions.', 'Original claim wording needs repair or explicit residual treatment where source fields differ.', 'All quarantined proposals retain unresolved applicability, source-hash and evaluator-binding fields; no canonical controls are changed.', 'No duplicate disposition is asserted for repeated checklist sections.', 'Dependencies beyond explicitly read context, outbound platform links, and source-to-claim omission completeness remain uncertified.', 'No owner policy adoption, publication clearance or native pilot acceptance.']})
contexts = [('content/library/application-security/_index.md', 1, 7), ('content/library/application-security/overview.md', 1, 18), ('content/library/application-security/design-principles.md', 132, 181), ('content/library/architecture/design-principles.md', 1, 90)]
write('input-bindings.json', {'primary_identity': 'codex:/root/source_worker_b', 'baseline': a['baseline'], 'assignment_sha256': sha(a_path.read_bytes()), 'original_crosswalk_sha256': sha(crosswalk_path.read_bytes()), 'authored_judgments_sha256': sha((OUT / 'judgments.txt').read_bytes()), 'catalog_digest': digest(catalog), 'proposal_digest': digest(proposals), 'source_snapshot_compressed_sha256': sha(snapshot.read_bytes()), 'source_artifact_sha256': sha(source['content'].encode()), 'context_read_spans': [{'path': p, 'content_sha256': rows[p]['sha256'], 'start_line': start, 'end_line': end} for p, start, end in contexts], 'checklist_primary_scope': {'start_line': 118, 'end_line': 291}, 'context_boundary': 'Direct pinned checklist interpretation only. Architecture principle context is partial; dependencies not listed, diagrams, live linked product behavior and source omission completeness are not certified.'})
write('packet-manifest.json', {'files': [{'path': p.name, 'sha256': sha(p.read_bytes())} for p in sorted(OUT.glob('*.json')) if p.name != 'packet-manifest.json'], 'decision_projection_digest': digest(decisions), 'primary_identity': 'codex:/root/source_worker_b', 'state': 'STAGED_PRIMARY_REVIEW_PENDING_D_A_E'})
print(json.dumps({'schema_valid_decisions': len(decisions), 'source_fidelity_holds': sum(bool(r['source_fidelity_defect']) for r in primary), 'decision_projection_digest': digest(decisions)}))
