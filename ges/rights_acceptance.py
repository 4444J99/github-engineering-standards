"""Validate scoped, authorized rights attestations, never infer legal permission.

The separately approved policy is a trusted authority input. Names, JSON and
hashes do not authenticate a human or prove the truth of a legal judgment.
No upstream content is executed, distributed or newly licensed by this module.
"""
from __future__ import annotations

from pathlib import Path
import re

from .core import ROOT, digest, now
from .published_assurance import _evidence, _require, _strings, _time
from .rights import triage

SUBJECT = ('artifact', 'inventory_digest', 'findings_digest', 'intended_use',
           'distribution_scope', 'obligations', 'valid_until')
IDENTITY = ('artifact_id', 'source', 'commit', 'path', 'sha256')
ROLES = {'file_rights_review': ('reviewer', 'authorized_reviewers'),
         'independent_exception_audit': ('independent_auditor', 'authorized_auditors'),
         'human_acceptance': ('human_acceptor', 'authorized_human_acceptors'),
         'distribution_approval': ('distribution_approver', 'authorized_distribution_approvers')}
USES = {'REFERENCES_ONLY', 'INDEPENDENT_PARAPHRASE', 'LICENSED_COPY', 'ADAPTATION'}


def rights_accounting(artifacts: list[dict], pins: dict[str, str],
                      findings: list[dict], receipts: list[dict], policy: dict,
                      *, evidence_root: Path = ROOT) -> dict:
    _require(isinstance(artifacts, list) and bool(artifacts), 'Empty rights inventory')
    _require(isinstance(findings, list) and isinstance(pins, dict), 'Invalid rights inputs')
    for item in artifacts:
        _require(isinstance(item, dict) and all(isinstance(item.get(k), str) and
                 bool(item[k].strip()) for k in (*IDENTITY, 'url', 'retrieved_at')),
                 'Malformed rights artifact')
        _require(re.fullmatch('[a-f0-9]{64}', item['sha256']) is not None,
                 'Invalid source content digest')
        _time(item['retrieved_at'])
    for finding in findings:
        _require(isinstance(finding, dict) and all(isinstance(finding.get(k), str)
                 and bool(finding[k]) for k in ('source', 'commit', 'path', 'content_sha256')),
                 'Malformed file-specific rights finding')
    # Retain every finding and the original complete inventory; triage is not
    # promoted into an approval and cannot import redistribution_approved=True.
    triage(artifacts, pins, findings)
    _require(isinstance(receipts, list), 'Rights receipts must be an array')
    result = {'schema': 'ges.rights-acceptance-accounting.v1',
              'completed': 0, 'denominator': len(artifacts),
              'inventory_digest': digest(artifacts), 'findings_digest': digest(findings),
              'receipts_digest': digest(receipts), 'policy_digest': digest(policy),
              'validated_artifact_ids': [], 'per_file_rights_acceptance': None,
              'authorized_distribution_decision': None,
              'legal_truth_automatically_certified': False,
              'authority_authenticity_automatically_certified': False,
              'publication_performed': False,
              'published_body_rights_cleared': False,
              'scope': 'Accountable attestations for the exact specified use/distribution only; not blanket reuse or publication permission.'}
    if not receipts:
        return result
    _require(isinstance(policy, dict) and policy.get('schema') ==
             'ges.rights-authority-policy.v1', 'Missing approved rights authority policy')
    _require(isinstance(policy.get('approval_reference'), str) and
             bool(policy['approval_reference'].strip()), 'Missing policy approval reference')
    for _, role in ROLES.values():
        _require(_strings(policy.get(role)), 'Missing explicit authority role: ' + role)
    _require(policy.get('inventory_digest') == result['inventory_digest'] and
             isinstance(policy.get('intended_use'), str) and policy['intended_use'] in USES and
             isinstance(policy.get('distribution_scope'), str) and
             bool(policy['distribution_scope'].strip()),
             'Authority policy must bind the exact project inventory, use and distribution')
    indexed = {x['artifact_id']: x for x in artifacts}
    seen = set()
    evidence_references = {}
    current_time = _time(now())
    for receipt in receipts:
        _require(isinstance(receipt, dict) and receipt.get('schema') ==
                 'ges.rights-acceptance-receipt.v1', 'Malformed rights acceptance receipt')
        subject = receipt.get('artifact')
        _require(isinstance(subject, dict) and set(subject) == set(IDENTITY) and
                 all(isinstance(subject[k], str) and bool(subject[k]) for k in IDENTITY),
                 'Malformed rights subject')
        identity = subject['artifact_id']
        _require(identity in indexed and identity not in seen, 'Foreign or duplicate rights receipt')
        artifact = indexed[identity]
        _require(all(subject[k] == artifact[k] for k in IDENTITY), 'Rights artifact changed')
        _require(receipt.get('inventory_digest') == result['inventory_digest'] and
                 receipt.get('findings_digest') == result['findings_digest'],
                 'Rights inventory or findings changed')
        _require(isinstance(receipt.get('intended_use'), str) and
                 receipt['intended_use'] == policy['intended_use'], 'Wrong approved project use')
        _require(isinstance(receipt.get('distribution_scope'), str) and
                 bool(receipt['distribution_scope'].strip()) and
                 _strings(receipt.get('obligations')), 'Missing distribution scope/obligations')
        _require(receipt['distribution_scope'] == policy['distribution_scope'],
                 'Wrong approved project distribution scope')
        expires = _time(receipt.get('valid_until'))
        _require(expires > current_time, 'Rights acceptance expired')
        for field, role in ROLES.values():
            _require(isinstance(receipt.get(field), str) and receipt[field] in policy[role],
                     'Unauthorized rights role: ' + field)
        _require(len({receipt['reviewer'], receipt['independent_auditor'],
                      receipt['human_acceptor']}) == 3 and
                 receipt['distribution_approver'] not in
                 {receipt['reviewer'], receipt['independent_auditor']},
                 'Rights acceptance and audit must be independent')
        references = receipt.get('evidence')
        _require(isinstance(references, dict) and set(references) == set(ROLES),
                 'Missing file review, audit, human acceptance or distribution approval')
        expected = {k: receipt[k] for k in SUBJECT}
        times = {}
        for kind, (field, _) in ROLES.items():
            reference = references[kind]
            doc = _evidence(evidence_root, reference)
            _require(doc.get('schema') == 'ges.rights-attestation.v1' and
                     doc.get('kind') == kind and doc.get('identity') == receipt[field] and
                     doc.get('subject') == expected, 'Wrong rights attestation identity or scope')
            _require(doc.get('decision') == 'APPROVED_FOR_SPECIFIED_USE' and
                     doc.get('file_specific_grant_and_components_reviewed') is True and
                     doc.get('exceptions_and_restrictions_accounted_for') is True and
                     isinstance(doc.get('rationale'), str) and bool(doc['rationale'].strip()),
                     'Unresolved or unsupported rights decision')
            times[kind] = _time(doc.get('reviewed_at'))
            _require(_time(artifact['retrieved_at']) <= times[kind] <= current_time,
                     'Rights review predates acquisition or is future')
            _require(times[kind] < expires, 'Rights evidence postdates its validity')
            path = reference['path']
            _require(path not in evidence_references or
                     evidence_references[path] == reference, 'Conflicting evidence identity')
            evidence_references[path] = reference
        _require(times['file_rights_review'] <= times['independent_exception_audit'] <=
                 times['human_acceptance'] <= times['distribution_approval'],
                 'Rights decision order is invalid')
        seen.add(identity)
    # Detect replacement during validation rather than trusting an earlier read.
    for reference in evidence_references.values():
        _evidence(evidence_root, reference)
    result.update(completed=len(seen), validated_artifact_ids=sorted(seen),
                  per_file_rights_acceptance=len(seen) == len(artifacts),
                  authorized_distribution_decision=len(seen) == len(artifacts),
                  approved_intended_use=policy['intended_use'],
                  approved_distribution_scope=policy['distribution_scope'])
    return result
