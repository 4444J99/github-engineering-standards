#!/usr/bin/env python3
"""Generate new canonical controls from GHQR structured requirements."""
import json
from pathlib import Path

raise SystemExit('Retired unsafe category-based generator. Use python -m ges ledger to produce UNREVIEWED source requirements; review controls individually before adoption. Historical IDs remain in controls/review_queue.json.')

# Load structured requirements
with open('.cache/corpus/structured-source-requirements.json') as f:
    structured = json.load(f)

ghqr = [x for x in structured if x['source'] == 'microsoft/ghqr']

# Load existing catalog
with open('controls/catalog.json') as f:
    catalog = json.load(f)

# Get existing IDs and max per category
existing_ids = {c['id'] for c in catalog}
existing_ghqr_sections = set()
cat_nums = {}
import re
for c in catalog:
    for s in c['sources']:
        if s['repository'] == 'microsoft/ghqr':
            existing_ghqr_sections.add(s['section'])
    m = re.match(r'GES-([A-Z]+)-(\d+)', c['id'])
    if m:
        cat = m.group(1)
        num = int(m.group(2))
        if cat not in cat_nums or num > cat_nums[cat]:
            cat_nums[cat] = num

# Ensure all categories have a starting number
for cat in ['SEC', 'RULE', 'GOV', 'DEP', 'COM', 'ACT', 'OPS', 'IAM', 'AI']:
    if cat not in cat_nums:
        cat_nums[cat] = 0

print("Starting category numbers:")
for cat, num in sorted(cat_nums.items()):
    print(f"  {cat}: {num}")

# Group by scope
repo_reqs = [x for x in ghqr if x['source_definition']['scope'] == 'repository']
org_reqs = [x for x in ghqr if x['source_definition']['scope'] == 'organization']
ent_reqs = [x for x in ghqr if x['source_definition']['scope'] == 'enterprise']
ghes_reqs = [x for x in ghqr if x['source_definition']['scope'] == 'ghes']

print(f"Repository-scoped: {len(repo_reqs)}")
print(f"Organization-scoped: {len(org_reqs)}")
print(f"Enterprise-scoped: {len(ent_reqs)}")
print(f"GHES-scoped: {len(ghes_reqs)}")

# Category mapping for GHQR to our categories
cat_map = {
    'security': 'SEC',
    'branch_protection': 'RULE',
    'access_control': 'GOV',
    'dependencies': 'DEP',
    'community': 'COM',
    'actions': 'ACT',
    'features': 'OPS',
    'maintenance': 'OPS',
    'budget': 'OPS',
    'copilot_security': 'AI',
    'copilot_cost': 'OPS',
    'copilot_features': 'AI',
    'ghes_server': 'OPS',
    'ghes_infrastructure': 'OPS',
    'ghes_networking': 'OPS',
    'ghes_authentication': 'IAM',
    'ghes_license': 'OPS',
}

# Scope mapping
scope_map = {
    'repository': 'repository',
    'organization': 'organization',
    'enterprise': 'enterprise',
    'ghes': 'enterprise',  # GHES is enterprise-level
}

# Applicability mapping
def get_applicability(req):
    cat = req['source_definition']['category']
    scope = req['source_definition']['scope']
    app = {}
    if scope == 'repository':
        app = {}
    elif scope == 'organization':
        app = {'organization': True}
    elif scope == 'enterprise':
        app = {'enterprise_server': True}
    elif scope == 'ghes':
        app = {'enterprise_server': True}
    
    if cat == 'actions':
        app['actions'] = True
    elif cat == 'dependencies':
        app['uses_dependabot'] = True
    elif cat == 'community':
        app['community'] = True
    elif cat in {'copilot_security', 'copilot_cost', 'copilot_features'}:
        app['ai_tools'] = True
    elif cat == 'security':
        app['software'] = True
    return app

# Verification kind mapping
def get_verification(req):
    cat = req['source_definition']['category']
    scope = req['source_definition']['scope']
    if cat == 'branch_protection':
        return {'kind': 'effective_rule', 'rule_type': 'pull_request'}
    elif cat == 'dependencies' or cat == 'budget':
        return {'kind': 'manual'}
    elif cat == 'actions':
        return {'kind': 'manual'}
    elif cat == 'copilot_security' or cat == 'copilot_features' or cat == 'copilot_cost':
        return {'kind': 'manual'}
    elif cat == 'access_control':
        return {'kind': 'manual'}
    elif cat == 'security':
        if scope == 'repository':
            return {'kind': 'file_present', 'paths': ['SECURITY.md', '.github/SECURITY.md', 'docs/SECURITY.md']}
        else:
            return {'kind': 'manual'}
    elif cat == 'community':
        return {'kind': 'file_present', 'paths': ['CODE_OF_CONDUCT.md', '.github/CODE_OF_CONDUCT.md', 'docs/CODE_OF_CONDUCT.md']}
    else:
        return {'kind': 'manual'}

# Template mapping
def get_template(req):
    cat = req['source_definition']['category']
    if cat == 'community':
        return 'templates/CODE_OF_CONDUCT.md'
    elif cat == 'security' and req['source_definition']['scope'] == 'repository':
        return 'templates/SECURITY.md'
    elif cat == 'branch_protection':
        return 'templates/ruleset.json'
    elif cat == 'dependencies':
        return 'templates/dependabot.yml'
    else:
        return 'templates/review-checklist.md'

# Generate new controls
new_controls = []
ctl_counter = {}
for cat in cat_nums:
    ctl_counter[cat.lower()] = cat_nums[cat]

def next_id(category):
    cat_lower = category.lower()
    ctl_counter[cat_lower] += 1
    return f"GES-{category}-{ctl_counter[cat_lower]:03d}"

for req in ghqr:
    ghqr_id = req['source_definition']['id']
    if ghqr_id in existing_ghqr_sections:
        continue
    
    cat = cat_map.get(req['source_definition']['category'], 'ops')
    ctl_id = next_id(cat)
    
    # Determine obligation based on severity
    sev = req['source_definition'].get('severity', 'high')
    if sev in {'critical', 'high'}:
        obligation = 'MUST'
    elif sev == 'medium':
        obligation = 'SHOULD'
    else:
        obligation = 'MAY'
    
    control = {
        'id': ctl_id,
        'revision': 1,
        'title': req['source_definition']['title'],
        'objective': req['source_definition']['recommendation'],
        'category': cat,
        'scope': scope_map.get(req['source_definition']['scope'], 'repository'),
        'obligation': obligation,
        'status': 'REVIEWED_DRAFT',
        'source_strength': 'GHQR source-defined check; adopted obligation reflects local policy interpretation of upstream recommendation.',
        'applicability': get_applicability(req),
        'sources': [{
            'repository': 'microsoft/ghqr',
            'commit': req['commit'],
            'path': req['path'],
            'section': ghqr_id,
            'start_line': req['line'],
            'end_line': req['line'],
            'content_sha256': req.get('content_sha256', ''),
            'url': f'https://github.com/microsoft/ghqr/blob/{req["commit"]}/{req["path"]}#L{req["line"]}'
        }],
        'verification': get_verification(req),
        'implementation': {
            'template': get_template(req),
            'acceptance': [
                req['source_definition']['recommendation'],
                'Evidence identifies the target, revision, responsible reviewer, observed outcome and review date.'
            ]
        },
        'enforcement': {
            'mechanism': 'CI assessment gate or authorized attestation gate; native policy requires separate enablement',
            'native_deployed': False,
            'bypass_review_required': True
        },
        'measurement': {
            'unit': 'applicable control instance',
            'numerator': 'current verified passes',
            'denominator': 'known applicable instances',
            'unknowns_reported_separately': True
        },
        'remediation': 'Resolve the stated acceptance criteria through a reviewed change, collect fresh evidence, and rerun assessment; do not erase or convert unknown outcomes.'
    }
    new_controls.append(control)

print(f"\nGenerated {len(new_controls)} new controls")
for c in new_controls:
    print(f"  {c['id']}: {c['title'][:60]}...")

# Save to file for review
with open('.cache/new-ghqr-controls.json', 'w') as f:
    json.dump(new_controls, f, indent=2)
