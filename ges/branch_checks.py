"""Observe exact-revision check results; do not certify execution or enforcement."""
from __future__ import annotations

import re
from collections import Counter
from datetime import UTC, datetime

from .core import digest, timestamp


def assess(snapshot: dict, profile: dict, revision: str, revision_kind: str,
           *, observed_now: datetime | None = None) -> dict:
    """A stronger draft SUCCESS-only check-result policy, not GitHub equivalence.

    Skipped jobs may still return success. Separate accountable workflow review
    and negative behavior tests remain necessary regardless of this result.
    """
    if not re.fullmatch(r'[a-f0-9]{40}', revision) or revision_kind not in {'head', 'test_merge', 'merge_group'}:
        raise ValueError('Exact lowercase revision and known revision kind required')
    if not isinstance(profile, dict) or not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', str(profile.get('target', ''))):
        raise ValueError('Explicit owner/repository target required')
    if not isinstance(snapshot, dict) or not isinstance(snapshot.get('observations'), dict):
        raise TypeError('Snapshot and observation objects required')
    specs = profile.get('required_checks')
    if not isinstance(specs, list) or not specs:
        raise ValueError('Explicit nonempty required-check profile needed')
    contexts = set()
    for spec in specs:
        if (not isinstance(spec, dict) or not isinstance(spec.get('context'), str)
                or not spec['context'].strip() or spec['context'] in contexts
                or type(spec.get('app_id')) is not int or spec['app_id'] <= 0
                or spec.get('provider') not in {'actions', 'external'}):
            raise ValueError('Unique contexts, positive expected App IDs and provider required')
        contexts.add(spec['context'])
    age_limit = profile.get('max_age_hours')
    if type(age_limit) not in {int, float} or not 0 < age_limit <= 24:
        raise ValueError('Observation age must be positive and at most 24 hours')
    now = observed_now or datetime.now(UTC)
    problems = []
    try:
        age = (now - timestamp(snapshot.get('observed_at'))).total_seconds() / 3600
        if age < 0 or age > age_limit:
            problems.append('Snapshot is stale or future dated')
    except (ValueError, TypeError, AttributeError):
        problems.append('Snapshot has no valid observation timestamp')
    if snapshot.get('check_revision') != revision:
        problems.append('Check observation revision differs from requested SHA')
    if revision_kind == 'head' and snapshot.get('target_revision') != revision:
        problems.append('Requested head differs from captured branch head')
    if snapshot.get('target') != profile.get('target'):
        problems.append('Snapshot target differs from declared pilot target')
    observations = snapshot.get('observations', {})

    def rows(name):
        observation = observations.get(name, {})
        if (not isinstance(observation, dict) or observation.get('status') != 'OK'
                or observation.get('complete') is not True
                or observation.get('truncated') is not False
                or observation.get('revision') != revision
                or not isinstance(observation.get('data'), list)
                or any(not isinstance(r, dict) for r in observation['data'])):
            problems.append(name + ' is missing, incomplete, malformed or bound to another SHA')
            return []
        return observation['data']

    checks = rows('check_runs')
    statuses = rows('commit_statuses')
    workflows = rows('workflow_runs') if any(s['provider'] == 'actions' for s in specs) else []
    results = []
    for spec in specs:
        context = spec['context']
        result = {'context': context, 'expected_app_id': spec['app_id'], 'status': 'NOT_VERIFIABLE', 'reasons': []}
        matches = [c for c in checks if c.get('name') == context
                   and isinstance(c.get('app'), dict)
                   and type(c['app'].get('id')) is int
                   and c['app']['id'] == spec['app_id']]
        if problems:
            result['reasons'].extend(problems)
        elif len(matches) != 1:
            result['reasons'].append('Expected exactly one latest check run from the selected App; missing or ambiguous results')
        else:
            check = matches[0]
            failures = []
            unknowns = []
            if type(check.get('id')) is not int or check['id'] <= 0:
                unknowns.append('Malformed check-run identity')
            if check.get('head_sha') != revision:
                unknowns.append('Check run is for another SHA')
            if check.get('status') != 'completed' or check.get('conclusion') != 'success':
                failures.append('Draft profile requires completed SUCCESS; skipped/neutral/pending/cancelled/failure do not satisfy it')
            same_name = [s for s in statuses if s.get('context') == context]
            # GitHub returns statuses newest first; never credit an older success.
            if same_name and same_name[0].get('state') != 'success':
                failures.append('Same-name latest commit status is not successful')
            if spec['provider'] == 'actions':
                suite = check.get('check_suite')
                suite_id = suite.get('id') if isinstance(suite, dict) else None
                runs = [r for r in workflows if type(suite_id) is int and r.get('check_suite_id') == suite_id and r.get('head_sha') == revision]
                if len(runs) != 1:
                    unknowns.append('Cannot uniquely bind Actions workflow event to check suite and revision')
                else:
                    allowed = {'merge_group'} if revision_kind == 'merge_group' else {'push', 'pull_request', 'pull_request_review', 'pull_request_target', 'deployment', 'deployment_status'}
                    if runs[0].get('event') not in allowed:
                        failures.append('Actions event does not satisfy this PR/merge-group required-check observation')
            result['status'] = 'FAIL' if failures else 'NOT_VERIFIABLE' if unknowns else 'PASS'
            result['reasons'] = failures + unknowns
            result['check_run_id'] = check.get('id')
        results.append(result)
    summary = dict(Counter(r['status'] for r in results))
    return {'schema': 'ges.branch-check-observation.v1', 'target': snapshot.get('target'),
            'revision': revision, 'revision_kind': revision_kind,
            'profile_digest': digest(profile), 'snapshot_digest': digest(snapshot),
            'summary': summary, 'checks': results,
            'observed_checks_pass': all(r['status'] == 'PASS' for r in results),
            'workflow_execution_proved': False, 'integration_revision_selection_verified': False,
            'policy_adopted': False, 'native_enforcement_verified': False,
            'remaining_review': ['Verify head/test-merge/queue revision selection against the actual PR',
                                 'Review workflow dependency results: skipped jobs can report success',
                                 'Review classic/ruleset layering, strictness, publishers and bypass actors',
                                 'Run positive/negative behavior and rollback tests on the approved target'],
            'scope': 'Observed successful selected-App check result and any same-name latest status only; not proof of job execution, full required-check inventory, policy adoption or enforcement.'}
