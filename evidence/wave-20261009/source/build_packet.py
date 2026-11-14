"""Serialize B's authored 18-claim review; never creates reconciliation receipts."""
import gzip
import hashlib
import json
from pathlib import Path
import sys

from ges.core import digest
from ges.semantics import stable_id, validate_record

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
CACHE = Path(sys.argv[1])
sha = lambda b: hashlib.sha256(b).hexdigest()
assignment_path = ROOT / 'evidence/wave-20261009/assignment.json'
assignment = json.loads(assignment_path.read_bytes())
claims = assignment['B']['claims']
document_path = ROOT / 'evidence/source-reviews/wa-application-security-checklist-claims.json'
document = json.loads(document_path.read_bytes())
catalog = json.loads((ROOT / 'controls/catalog.json').read_bytes())
proposals = json.loads((ROOT / 'controls/review_queue.json').read_bytes())
ci = {c['id']: c for c in catalog}
pi = {c['id']: c for c in proposals}
snapshot_path = CACHE / 'sources/github__github-well-architected.text.jsonl.gz'
source_rows = {r['path']: r for r in map(json.loads, gzip.open(snapshot_path, 'rt'))}
source = source_rows[document['path']]
assert sha(source['content'].encode()) == document['content_sha256']
occurrence_path = CACHE / 'corpus/structured-source-requirements.json'
occurrences = {r['requirement_id']: r for r in json.loads(occurrence_path.read_bytes())}
assert len(claims) == 162

# Explicitly authored judgments in claim order, after direct source/catalog reading.
# Related catalog IDs do not imply complete semantic coverage.
judgments = [
 ('GES-SEC-002', 'Automated dependency scanning is stronger than an unspecified scan. Preserve automation and dependencies; do not equate manual review or configuration existence with execution.', 'automation must be explicit in the objective and evidence'),
 ('GES-SEC-002', 'Tool maintenance is distinct from reviewing dependency findings. Retain recurring scanner update responsibility and evidence of current supported tooling.', 'recurring scanner-tool updates are absent from the canonical acceptance'),
 ('GES-SEC-002', 'Dependency triage is covered in the broad draft objective, but prompt handling must retain a target-defined risk-based response cadence; no numeric SLA is supplied by the source.', 'prompt remediation requires explicit target cadence'),
 ('GES-SEC-003', 'The draft objective requires supported code security analysis and evidence of completed analysis on relevant revisions; this preserves using detection tools for potential code security defects.', None),
 ('GES-SEC-003', 'Pipeline integration is covered by the canonical delivery-workflow objective. The original claim introduces static analysis although the source says code scanning without that restriction; correct or explicitly qualify that narrowing before treating source consolidation as resolved.', 'original claim must not narrow code scanning to static analysis'),
 ('GES-SEC-003', 'Maintaining scan rules does not fully record periodic review of rules and configuration. Preserve both review and updates, including configurations, with profile-defined recurrence.', 'periodic review and configuration maintenance must remain explicit'),
 ('GES-SEC-004', 'Assess secret and sensitive-information management practices. An exposed-credential response control is a related safeguard and cannot replace assessment of routine handling.', 'routine assessment of secrets and sensitive information is a separate objective'),
 ('GES-SEC-004', 'Use a tool for storing and managing secrets. Incident response and prevention do not establish that an appropriate management system exists and is used.', 'secret storage and management tooling requires its own evidence'),
 ('GES-SEC-004', 'The source calls for regular rotation of secrets and credentials regardless of confirmed exposure. The original claim only maintains a reviewed rotation practice; actual recurring rotation and both object classes must be restored.', 'proactive recurring rotation differs from reactive exposed-credential revocation'),
 ('GES-GOV-010', 'Review both presence and enforcement of security policy and guidelines. Training and feedback alone cannot demonstrate effective operation of the security policy.', 'security-policy existence and effective enforcement need separate checks'),
 ('GES-GOV-010', 'Policy accessibility extends to all team members, not merely a subset deemed relevant. Preserve this audience in the assessment and distinguish access from having been trained.', 'all-team accessibility is a retained audience requirement'),
 ('GES-GOV-010', 'Update policies regularly for new threats and best practices. Governance feedback is related, but does not itself specify security-policy updates and their cadence.', 'recurring security-policy refresh and change triggers are required'),
 ('GES-SEC-009', 'Establish and enforce secure coding guidelines across all development teams. Providing education does not establish guideline adoption or enforcement; preserve cross-team scope.', 'guideline establishment and enforcement are distinct from training'),
 ('GES-SEC-009', 'Secure-development guidance and training applicability are addressed by the draft education objective. Preserve secure coding as training content, and verify the training actually occurs rather than the mere presence of guidance.', 'training delivery in secure coding must be explicit'),
 ('GES-GOV-005', 'Conduct code reviews to assess adherence to secure coding guidance. Reviewer threshold and staffing policy do not establish security-guideline adherence in an actual review.', 'review content and adherence evidence are distinct from reviewer-count policy'),
 ('GES-GOV-007', 'Implement strict access controls and regularly review permissions. Periodic access review supports the latter, but effective control implementation and strictness remain separate; define strictness through a target policy rather than a fabricated universal threshold.', 'implemented access restrictions and recurring entitlement review must both remain'),
 ('GES-GOV-003', 'Use RBAC to limit access in GitHub and other business systems. Explicit role assignments do not prove role-based enforcement; do not narrow business-system scope to connected systems only.', 'role-based enforcement spans GitHub and other business systems'),
 ('GES-GOV-008', 'Regularly audit access logs for suspicious activity across GitHub and other business systems. General audit retention and anomaly investigation do not prove recurring access-log examination or full system coverage.', 'periodic access-log audit and both system scopes must remain'),
]

decisions = []
draft_dispositions = []
primary = []
crosswalk = []
for index, claim in enumerate(claims):
    subject = {k: claim[k] for k in ('claim_id', 'source', 'commit', 'path', 'content_sha256', 'start_line', 'end_line')}
    subject.update(artifact_id=document['artifact_id'], statement_sha256=sha(claim['statement'].encode()), claim_document=document_path.name, claim_document_sha256=sha(document_path.read_bytes()))
    occurrence_ids = claim['structured_requirement_ids']
    for oid in occurrence_ids:
        occurrence = occurrences[oid]
        assert occurrence['content_sha256'] == claim['content_sha256']
        assert occurrence['start_line'] == claim['start_line']
    proposal_id = f'GES-OPS-{index + 37:03d}'
    proposal = pi[proposal_id]
    assert proposal['sources'][0]['start_line'] == claim['start_line']
    crosswalk.append({'claim': subject, 'occurrences': [{'id': oid, 'digest': digest(occurrences[oid]), 'start_line': occurrences[oid]['start_line'], 'end_line': occurrences[oid]['end_line']} for oid in occurrence_ids], 'existing_proposal': {'id': proposal_id, 'revision': proposal['revision']}, 'primary_review_status': 'REVIEWED_PROPOSED' if index < 18 else 'NOT_REVIEWED_THIS_TRANCHE'})
    if index >= 18:
        continue
    catalog_id, rationale, distinction = judgments[index]
    is_map = distinction is None
    references = [{'id': catalog_id, 'revision': ci[catalog_id]['revision']}]
    if not is_map:
        references.append({'id': proposal_id, 'revision': proposal['revision']})
    decision = {'schema': 'ges.reconciliation-decision.v1', 'proposition_ids': [claim['claim_id']], 'disposition': 'EXISTING_CONTROL' if is_map else 'SPECIALIZATION', 'source_treatment': 'RETAINED', 'control_references': references, 'rationale': rationale, 'preserved_fields': ['actor', 'action', 'object', 'modality', 'scope', 'cadence', 'applicability'], 'lost_fields': [], 'conflicts': [], 'review': {'status': 'PROPOSED', 'reviewer': None, 'evidence_reference': None}}
    decision['id'] = stable_id(decision)
    validate_record(decision)
    decisions.append(decision)
    draft_dispositions.append({'claim': subject, 'proposed_disposition': 'MAP' if is_map else 'SPECIALIZE', 'control_references': [{'id': r['id'], 'revision': r['revision'], 'collection': 'CATALOG' if r['id'] in ci else 'PROPOSAL'} for r in references], 'details': {} if is_map else {'scope': claim['scope'], 'distinction': distinction}, 'rationale': rationale, 'primary_reviewer': 'codex:/root/source_worker_b', 'accepted_policy': False, 'adopted_obligation': None, 'decision_id': decision['id'], 'status': 'PROPOSED_NOT_RECONCILIATION_RECEIPT'})
    primary.append({'claim_id': claim['claim_id'], 'decision_id': decision['id'], 'source_span_sha256': sha('\n'.join(source['content'].splitlines()[claim['start_line']-1:claim['end_line']]).encode()), 'catalog_record_digest': digest(ci[catalog_id]), 'proposal_record_digest': digest(proposal), 'interpretation': rationale, 'residual': distinction, 'publication_boundary': 'Pinned spans inspected privately; no upstream text copied into this review.'})

def write(name, value):
    (OUT / name).write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')

write('proposed-decisions.json', decisions)
write('draft-dispositions.json', draft_dispositions)
write('occurrence-crosswalk.json', crosswalk)
write('primary-review.json', primary)
write('residuals.json', {'assigned_claims': 162, 'assigned_occurrences': 162, 'primary_reviewed_claims': 18, 'primary_reviewed_occurrences': 18, 'proposed_map_count': 1, 'proposed_specialize_count': 17, 'independently_audited_decisions': 0, 'unreviewed_claim_ids': [c['claim_id'] for c in claims[18:]], 'all_decisions_pending_D_A_E': True, 'source_fidelity_repairs_required': ['WA-APPSEC-005: static restriction absent from original source', 'WA-APPSEC-009: reviewed practice does not establish regular actual rotation', 'WA-APPSEC-011: relevant contributors narrows all team members', 'WA-APPSEC-017: connected business systems narrows other business systems', 'WA-APPSEC-018: investigation does not establish recurring audit'], 'proposal_defects': ['Existing proposals are quarantined NON_ADOPTED_DRAFT with unspecified applicability and empty content_sha256 in their source mapping; this packet binds source bytes but does not revise or adopt those proposals.'], 'boundary': 'Claims and occurrences are two representations of one assigned source set, not 324 propositions. No human approval, publication clearance, policy adoption, operational implementation, source omission certification or whole-file reconciliation.'})
context_paths = ['content/library/application-security/design-principles.md', 'content/library/application-security/schema.json', 'content/library/application-security/index.yml', 'content/library/application-security/recommendations/managing-dependency-threats.md']
write('input-bindings.json', {'baseline': assignment['baseline'], 'primary_identity': 'codex:/root/source_worker_b', 'assignment_sha256': sha(assignment_path.read_bytes()), 'catalog_digest': digest(catalog), 'proposal_digest': digest(proposals), 'claim_document_sha256': sha(document_path.read_bytes()), 'structured_occurrence_ledger_sha256': sha(occurrence_path.read_bytes()), 'source_snapshot_compressed_sha256': sha(snapshot_path.read_bytes()), 'source_artifact_sha256': document['content_sha256'], 'context_artifacts': [{'path': p, 'sha256': source_rows[p]['sha256']} for p in context_paths], 'context_read_boundary': 'Checklist all 291 lines inspected; detailed primary semantic decisions only lines 15-42. Design for Security section and metadata/schema read; dependency-defense overview, strategies and assumptions read for context. Other recommendation content, outbound links, rendering behavior and all 83 routing dependencies are not certified.'})
write('packet-manifest.json', {'files': [{'path': p.name, 'sha256': sha(p.read_bytes())} for p in sorted(OUT.glob('*.json')) if p.name != 'packet-manifest.json'], 'decision_projection_digest': digest(decisions), 'primary_identity': 'codex:/root/source_worker_b', 'state': 'STAGED_PRIMARY_REVIEW_PENDING_INDEPENDENT_REVIEW'})
print(json.dumps({'claim_subjects_checked': len(crosswalk), 'semantic_schema_valid_decisions': len(decisions), 'decision_projection_digest': digest(decisions)}))
