"""Applicability, evidence age, outcomes and exceptions are independent axes."""
from __future__ import annotations
from collections import Counter
from datetime import timedelta
from .core import applicable, digest, now, timestamp
from .checks import execute


def audit(controls: list[dict], snapshot: dict, profile: dict, *, at: str | None=None,
          attestations: list[dict] | None=None, exceptions: list[dict] | None=None) -> dict:
    from .evidence_integrity import validate_authority
    validate_authority(profile)
    at=at or now(); clock=timestamp(at); rows=[]
    context=profile.get('context',{})
    trusted=set(profile.get('authorized_reviewers',[]))
    target=snapshot.get('target'); target_revision=snapshot.get('target_revision')
    target_type=snapshot.get('target_type') or 'repository'
    max_age_seconds=profile.get('max_age_hours',24)*3600
    try:
        elapsed=(clock-timestamp(snapshot['observed_at'])).total_seconds()
        freshness='FUTURE' if elapsed < -60 else ('STALE' if elapsed > max_age_seconds else 'FRESH')
    except (KeyError,ValueError,TypeError): freshness='INVALID'
    for c in controls:
        app,reason=applicable(c,context)
        if app == 'APPLICABLE':
            if c['scope'] == 'organization':
                if target_type == 'organization':
                    pass
                elif target_type == 'repository':
                    has_org = ('organization' in snapshot.get('observations', {}) or
                               any(k.startswith('org_') for k in snapshot.get('observations', {})))
                    if not has_org:
                        app, reason = 'UNKNOWN', 'Organization observations not included in repository snapshot; inheritance applicability unresolved'
                else:
                    app, reason = 'NOT_APPLICABLE_WITH_REASON', f'Control scope {c["scope"]} does not match target type {target_type}'
            elif c['scope'] == 'enterprise':
                if target_type == 'enterprise':
                    pass
                else:
                    has_ent = any(k.startswith('enterprise') for k in snapshot.get('observations', {}))
                    if not has_ent:
                        app, reason = 'UNKNOWN', 'Enterprise observations absent; inheritance applicability unresolved'
            elif target_type == 'organization' and c['scope'] == 'repository':
                app, reason = 'NOT_APPLICABLE_WITH_REASON', 'Control scope repository does not match target type organization'
            elif c['scope'] != target_type and c['scope'] != 'repository':
                app, reason = 'NOT_APPLICABLE_WITH_REASON', f'Control scope {c["scope"]} does not match target type {target_type}'
        row={'control_id':c['id'],'control_revision':c['revision'],'control_status':c['status'],
             'obligation':c['obligation'],'target':target,'target_revision':target_revision,
             'applicability':app,'applicability_reason':reason,'evaluated_at':at,
             'evidence_freshness':freshness,'exception_status':'NONE','enforcement_verified':False,
             'outcome':'NOT_ASSESSED','detail':''}
        if app=='UNKNOWN': row['detail']=reason
        elif app=='NOT_APPLICABLE_WITH_REASON': row['detail']=reason
        elif c['status']=='RETIRED':
            row.update(applicability='NOT_APPLICABLE_WITH_REASON',detail='Control is retired',applicability_reason='Control is retired')
        elif not target or not target_revision:
            row.update(outcome='ERROR',detail='Evidence must identify target and exact target revision')
        elif freshness=='STALE': row.update(outcome='STALE',detail='Snapshot exceeded maximum evidence age')
        elif freshness in {'FUTURE','INVALID'}: row.update(outcome='ERROR',detail='Evidence timestamp is invalid or in the future')
        else:
            outcome,detail=execute(c,snapshot,context)
            if c['verification']['kind']=='manual' and c['scope'] in {'organization', 'enterprise'} and c['scope'] != target_type:
                outcome, detail = 'NOT_VERIFIABLE', 'Inherited manual control requires an assessment and attestation for its owning entity'
            elif c['verification']['kind']=='manual':
                best_attestation=None
                best_reviewed_at=None
                for a in attestations or []:
                    if (a.get('control_id')!=c['id'] or a.get('control_revision')!=c['revision']
                        or a.get('target')!=target or a.get('target_revision')!=target_revision): continue
                    try:
                        reviewed=timestamp(a['reviewed_at'])
                        if reviewed < clock - timedelta(seconds=max_age_seconds):
                            continue
                        valid=(a.get('reviewer') in trusted and a.get('evidence_ref') and a.get('rationale')
                               and reviewed<=clock<timestamp(a['expires_at'])
                               and a.get('outcome') in {'PASS','FAIL','PARTIAL'})
                    except (ValueError,KeyError,TypeError): valid=False
                    if valid:
                        if best_reviewed_at is None or reviewed > best_reviewed_at:
                            best_attestation=a
                            best_reviewed_at=reviewed
                        elif reviewed == best_reviewed_at and a['outcome'] != best_attestation['outcome']:
                            best_attestation=dict(a,outcome='PARTIAL',evidence_ref='Conflicting simultaneous authorized attestations')
                if best_attestation:
                    outcome,detail=best_attestation['outcome'],'Authorized attestation: '+best_attestation['evidence_ref']
            row.update(outcome=outcome,detail=detail)
            if outcome=='PASS' and c['verification']['kind']=='effective_rule':
                row['enforcement_scope']='Active ruleset presence/parameter only; actor bypass behavior unverified'
        for e in exceptions or []:
            if e.get('control_id')!=c['id'] or e.get('control_revision')!=c['revision'] or e.get('target')!=target: continue
            if e.get('approved_by') not in trusted or not all(e.get(k) for k in ('reason','compensating_control','expires_at','approved_at')):
                row['exception_status']='INVALID'; continue
            try:
                approved=timestamp(e['approved_at']); expires=timestamp(e['expires_at'])
                row['exception_status']='APPROVED_UNTIL' if approved<=clock<expires else 'EXPIRED'
                row['exception_expires_at']=e['expires_at']
            except (ValueError,TypeError): row['exception_status']='INVALID'
        rows.append(row)
    known=[r for r in rows if r['applicability']=='APPLICABLE']
    passing=[r for r in known if r['outcome']=='PASS']
    assessed=[r for r in known if r['outcome'] in {'PASS','FAIL','PARTIAL'}]
    return {'schema_version':'ges.assessment.v1','standard_version':'0.1.0',
            'catalog_digest':digest(controls),'profile_digest':digest(profile),
            'snapshot_digest':digest(snapshot),'evaluated_at':at,'target':target,
            'summary':{'expected_instances':len(rows),'known_applicable':len(known),
                       'unknown_applicability':sum(r['applicability']=='UNKNOWN' for r in rows),
                       'verified_pass':len(passing),'valid_evaluations':len(assessed),
                       'pass_rate':len(passing)/len(known) if known else None,
                       'assessment_coverage':len(assessed)/len(known) if known else None,
                       'outcomes':dict(Counter(r['outcome'] for r in known)),
                       'approved_exceptions':sum(r['exception_status']=='APPROVED_UNTIL' for r in rows)},
            'results':rows}


def gate(report: dict, *, allow_exceptions: bool=False, require_accepted: bool=False,
         enforce_should: bool=False, expected_controls: list[dict] | None=None) -> tuple[bool,list[str]]:
    """Unknowns and errors block mandatory controls; an exception never rewrites outcome."""
    reasons=[]
    if not report.get('results'): return False,['Empty or missing assessment results']
    ids=[r.get('control_id') for r in report['results']]
    if len(ids)!=len(set(ids)): return False,['Duplicate control results']
    if expected_controls is not None:
        if report.get('catalog_digest')!=digest(expected_controls): reasons.append('Catalog digest does not match selected standard')
        if set(ids)!={c['id'] for c in expected_controls}: reasons.append('Assessment omits or adds control instances')
        by_id={c['id']:c for c in expected_controls}
        for row in report['results']:
            c=by_id.get(row.get('control_id'))
            if c and (row.get('control_revision')!=c['revision'] or row.get('obligation')!=c['obligation'] or row.get('control_status')!=c['status']):
                reasons.append(row['control_id']+': result policy metadata mismatch')
    for r in report['results']:
        if r.get('control_status') in {'NON_ADOPTED_DRAFT', 'PROPOSED'}:
            reasons.append(r['control_id']+': control is not adopted policy')
        if r['obligation'] not in ({'MUST','SHOULD'} if enforce_should else {'MUST'}): continue
        if require_accepted and r['control_status']!='ACCEPTED': reasons.append(r['control_id']+': control not accepted')
        if r['applicability']=='NOT_APPLICABLE_WITH_REASON': continue
        excepted=allow_exceptions and r['exception_status']=='APPROVED_UNTIL' and r['applicability']=='APPLICABLE' and r['outcome'] in {'FAIL','PARTIAL'}
        if r['applicability']=='UNKNOWN' or r['outcome']!='PASS':
            if not excepted: reasons.append(r['control_id']+': '+r['applicability']+'/'+r['outcome'])
    return not reasons,reasons
