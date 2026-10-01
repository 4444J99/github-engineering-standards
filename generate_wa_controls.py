#!/usr/bin/env python3
"""Generate new canonical controls from Well-Architected structured requirements."""
import json
import re
from pathlib import Path

# Load structured requirements
with open('.cache/corpus/structured-source-requirements.json') as f:
    structured = json.load(f)

wa = [x for x in structured if x['source'] == 'github/github-well-architected']

# Load existing catalog
with open('controls/catalog.json') as f:
    catalog = json.load(f)

# Get existing max per category
import re as regex
cat_nums = {}
for c in catalog:
    m = regex.match(r'GES-([A-Z]+)-(\d+)', c['id'])
    if m:
        cat = m.group(1)
        num = int(m.group(2))
        if cat not in cat_nums or num > cat_nums[cat]:
            cat_nums[cat] = num

# Ensure all categories have a starting number
for cat in ['SEC', 'RULE', 'GOV', 'DEP', 'COM', 'ACT', 'OPS', 'IAM', 'AI', 'ARC', 'ID', 'DOC', 'BR', 'PR', 'ISSUE', 'SCH', 'REL', 'RIGHTS', 'CI', 'ART']:
    if cat not in cat_nums:
        cat_nums[cat] = 0

print("Starting category numbers:")
for cat, num in sorted(cat_nums.items()):
    print(f"  {cat}: {num}")

# Function category mapping
func_to_cat = {
    'Security': 'SEC',
    'Governance': 'GOV',
    'Architecture': 'ARC',
    'Automation': 'OPS',
    'Efficiency': 'OPS',
    'Feedback': 'COM',
    'Continuous Learning': 'OPS',
    'Scalability': 'ARC',
    'Integration': 'ARC',
    'Compliance': 'GOV',
    'Proactivity': 'OPS',
    'Auditability': 'GOV',
    'Awareness': 'COM',
    'Interoperability': 'ARC',
    'Simplicity': 'ARC',
    'Observability': 'OPS',
    'Disaster Recovery': 'OPS',
    'Additional Checklist Items for GitHub Enterprise Deployments': 'OPS',
    'Additional Checklist Items for GitHub Enterprise Deployments / GitHub Enterprise Server': 'OPS',
    'Additional Checklist Items for GitHub Enterprise Deployments / Scalability': 'ARC',
    'Additional Checklist Items for GitHub Enterprise Deployments / Interoperability': 'ARC',
    'Additional Checklist Items for GitHub Enterprise Deployments / Simplicity': 'ARC',
    'Engineering System Success': 'OPS',
}

ctl_counter = {}
for cat in cat_nums:
    ctl_counter[cat.lower()] = cat_nums[cat]

def next_id(category):
    cat_lower = category.lower()
    ctl_counter[cat_lower] += 1
    return f"GES-{category}-{ctl_counter[cat_lower]:03d}"

# Template mapping
def get_template(cat):
    templates = {
        'SEC': 'templates/SECURITY.md',
        'GOV': 'templates/GOVERNANCE.md',
        'ARC': 'templates/architecture.md',
        'OPS': 'templates/runbook.md',
        'COM': 'templates/CODE_OF_CONDUCT.md',
        'DEP': 'templates/dependabot.yml',
        'ACT': 'templates/review-checklist.md',
        'IAM': 'templates/review-checklist.md',
        'AI': 'templates/review-checklist.md',
    }
    return templates.get(cat, 'templates/review-checklist.md')

# Verification mapping
def get_verification(cat, statement):
    if cat in {'SEC', 'GOV', 'ARC'}:
        return {'kind': 'manual'}
    return {'kind': 'manual'}

# Applicability mapping
def get_applicability(cat, statement):
    app = {}
    if 'Enterprise' in cat or 'Enterprise' in statement:
        app['enterprise_server'] = True
    if cat == 'Security':
        app['software'] = True
    if cat == 'Governance' or cat == 'Compliance' or cat == 'Auditability':
        app['organization'] = True
    return app

new_controls = []
seen_statements = set()

for req in wa:
    func = req['function']
    statement = req['source_statement']
    
    # Skip if we've seen this exact statement
    stmt_key = (func, statement)
    if stmt_key in seen_statements:
        continue
    seen_statements.add(stmt_key)
    
    cat = func_to_cat.get(func, 'OPS')
    ctl_id = next_id(cat)
    
    # Determine obligation - WA recommendations are generally SHOULD
    obligation = 'SHOULD'
    
    control = {
        'id': ctl_id,
        'revision': 1,
        'title': statement[:80] + ('...' if len(statement) > 80 else ''),
        'objective': statement,
        'category': cat,
        'scope': 'repository',  # WA checklist items are generally repo-scoped
        'obligation': obligation,
        'status': 'REVIEWED_DRAFT',
        'source_strength': 'Well-Architected checklist recommendation; adopted obligation reflects local policy interpretation.',
        'applicability': get_applicability(cat, statement),
        'sources': [{
            'repository': 'github/github-well-architected',
            'commit': req['commit'],
            'path': req['path'],
            'section': func,
            'start_line': req['line'],
            'end_line': req['line'],
            'content_sha256': req.get('content_sha256', ''),
            'url': f'https://github.com/github/github-well-architected/blob/{req["commit"]}/{req["path"]}#L{req["line"]}'
        }],
        'verification': get_verification(cat, statement),
        'implementation': {
            'template': get_template(cat),
            'acceptance': [
                statement,
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

print(f"\nGenerated {len(new_controls)} new WA controls (after deduplication)")
for c in new_controls[:20]:
    print(f"  {c['id']}: {c['title'][:60]}...")

# Save to file for review
with open('.cache/new-wa-controls.json', 'w') as f:
    json.dump(new_controls, f, indent=2)

print(f"\nUnique functions covered: {len(set(req['function'] for req in wa))}")
print(f"Unique statements: {len(seen_statements)}")
