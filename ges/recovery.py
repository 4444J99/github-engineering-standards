"""Reproducible construction accounting. Inventory never closes review gates."""
from collections import Counter
from pathlib import Path
import gzip
import hashlib
import json

from .core import ROOT, digest, dump, load, now
from .corpus import coverage_with_reviews


def evaluate_gate(name: str, completed: int, denominator: int | None,
                  condition: str, prerequisites: dict[str, bool | None]) -> dict:
    """Separate observed incompleteness from absent certification evidence."""
    if type(completed) is not int or completed < 0:
        raise ValueError('Invalid completed count')
    if denominator is not None and (type(denominator) is not int or denominator < completed):
        raise ValueError('Invalid or reduced denominator')
    if (not prerequisites or 'coverage_complete' in prerequisites or
            any(v is not None and type(v) is not bool for v in prerequisites.values())):
        raise ValueError('Gate prerequisites must be explicit boolean/unknown observations')
    coverage = None if denominator is None or denominator == 0 else completed == denominator
    observations = {'coverage_complete': coverage, **prerequisites}
    failed = [key for key, value in observations.items() if value is False]
    unknown = [key for key, value in observations.items() if value is None]
    closed = not failed and not unknown
    return {'gate': name, 'status': 'CLOSED' if closed else 'OPEN',
            'evaluation': 'PROVEN' if closed else ('INCOMPLETE' if failed else 'UNVERIFIED'),
            'completed': completed, 'denominator': denominator,
            'remaining': denominator-completed if denominator is not None else None,
            'closure_condition': condition, 'conditions': observations,
            'incomplete_conditions': failed, 'unverified_conditions': unknown,
            'evidence': 'evidence/recovery-status.json'}


def status(sources: Path, corpus: Path, reviews: Path | None=None, review_policy: Path | None=None,
           rendered_directory: Path | None=None, published_assurance: Path | None=None,
           published_assurance_policy: Path | None=None) -> dict:
    controls = load(ROOT/'controls/catalog.json')
    queue = load(ROOT/'controls/review_queue.json')
    pins = load(ROOT/'sources/sources.lock.json')['sources']
    receipts=[]
    if reviews:
        for p in sorted(reviews.glob('*.json')):
            if not p.name.endswith('-claims.json'):
                records=load(p)
                if not isinstance(records,list): raise ValueError('Review receipt file must contain an array')
                receipts.extend(records)
    with (corpus/'candidates.jsonl').open() as stream:
        candidate_records=[json.loads(line) for line in stream if line.strip()]
    from tempfile import TemporaryDirectory
    with TemporaryDirectory() as td:
        receipt_path=Path(td)/'reviews.json';dump(receipt_path,receipts)
        review_result=coverage_with_reviews(corpus/'artifacts.jsonl',receipt_path,
                         candidates=candidate_records,controls=controls,
                         authorized_reviewers=load(review_policy)['authorized_reviewers'] if review_policy else [])
    if review_result['errors']: raise ValueError('Invalid review receipts: '+str(review_result['errors']))
    reviewed_by_source=Counter()
    artifacts_by_id={r['artifact_id']:r for r in [json.loads(l) for l in (corpus/'artifacts.jsonl').read_text().splitlines()]}
    for receipt in receipts:
        reviewed_by_source[artifacts_by_id[receipt['artifact_id']]['source']] += 1
    sources_report = []
    for pin in pins:
        slug = pin['repository'].replace('/', '__')
        inventory = load(sources/(slug+'.inventory.json'))
        if any(r['source'] != pin['repository'] or r['commit'] != pin['commit'] for r in inventory):
            raise ValueError('Inventory does not match release pin: '+pin['repository'])
        tree = load(sources/(slug+'.tree-reconciliation.json'))
        sources_report.append({'repository': pin['repository'], 'commit': pin['commit'],
                               'artifacts': len(inventory), 'reviewed_artifacts': reviewed_by_source[pin['repository']],
                               'review_evidence': 'evidence/source-reviews; source review is not control adoption or independent omission certification',
                               'git_tree_reconciliation': tree})
    ledger = load(corpus/'ledger-summary.json')
    requirements = load(corpus/'structured-source-requirements.json')
    pages = load(corpus/'published-page-ledger.json')
    inventories = sum(s['artifacts'] for s in sources_report)
    candidates = len(candidate_records)
    rendered = []
    rendered_path = sources/'docs-rendered.jsonl.gz'
    if rendered_path.exists():
        with gzip.open(rendered_path, 'rt') as stream:
            for line in stream:
                r = json.loads(line)
                if r.get('status') == 'RETRIEVED' and hashlib.sha256(r['body'].encode()).hexdigest() == r.get('sha256'):
                    rendered.append((r['version'],r['path']))
    page_keys = {(r['version'],r['path']) for r in pages}
    if rendered_directory is not None:
        from .pages import cached_pages
        page_ledger_sha = hashlib.sha256((corpus/'published-page-ledger.json').read_bytes()).hexdigest()
        verified = cached_pages(rendered_directory, pages, page_ledger_sha)
        rendered.extend((r['version'], r['path']) for r in verified.values())
    acquired = len(page_keys & set(rendered))
    if (published_assurance is None) != (published_assurance_policy is None):
        raise ValueError('Published assurance requires both receipt and authority policy inputs')
    from .published_assurance import assurance_accounting
    assurance = assurance_accounting(
        corpus/'published-page-ledger.json', rendered_directory, corpus/'artifacts.jsonl',
        load(published_assurance) if published_assurance is not None else [],
        load(published_assurance_policy) if published_assurance_policy is not None else {},
        {p['repository']: p['commit'] for p in pins}, evidence_root=ROOT)
    accepted = sum(c['status'] == 'ACCEPTED' for c in controls)
    canonical_ids = {c['id'] for c in controls}
    if canonical_ids & {c['id'] for c in queue} or len({c['id'] for c in queue}) != len(queue):
        raise ValueError('Review queue IDs duplicate canonical or proposal IDs')
    gates = [
        ('exhaustive_artifact_accounting',review_result['reviewed'],inventories,'Every artifact has a validated reviewed disposition and independent omission audit'),
        ('published_content_assurance',assurance['completed'],len(pages),'Every page has rendered/version/dependency review; retrieval alone is insufficient'),
        ('semantic_extraction',review_result['reviewed'],inventories,'Full-artifact omission review and atomic claims; candidate count is not a claim denominator'),
        ('consolidation',0,len(requirements),'All structured occurrences mapped with exact provenance; remaining unstructured claims also reviewed'),
        ('generalization',0,len(controls)+len(queue),'Every definition and proposal has reviewed scope, policy, parameters and conflicts'),
        ('operational_completeness',0,accepted,'Accepted controls have all required tested bindings and accountable review procedures'),
        ('native_enforcement',0,None,'Approved target inventory, positive/negative behavior tests and recovery receipts'),
        ('rights_and_publication',0,inventories,'Per-file rights review and approved distribution; inventory notices alone insufficient'),
        ('estate_rollout',0,None,'Explicit authorized inventory and effective-policy/behavior evidence per target'),
    ]
    # Missing semantic, rights and runtime certification is UNKNOWN, not an
    # invented failed audit or a successful count-only test. These adapters must
    # be implemented and supplied validated evidence before their values change.
    prerequisites = {
        'exhaustive_artifact_accounting': {
            'pinned_git_trees_match': all(s['git_tree_reconciliation'].get('status') == 'MATCH' for s in sources_report),
            'review_receipts_valid': not review_result['errors'],
            'independent_omission_audit': None},
        'published_content_assurance': {
            'all_bodies_durably_acquired': acquired == len(pages),
            'all_source_paths_reconciled': all(p['source_matches'] for p in pages),
            'version_include_and_render_assurance': assurance['version_include_and_render_assurance']},
        'semantic_extraction': {'atomic_claim_fidelity_audit': None,
                                'independent_source_to_claim_omission_audit': None},
        'consolidation': {'exact_claim_mapping_and_conflict_review': None,
                          'unstructured_claim_denominator_certified': None},
        'generalization': {'profiles_parameters_and_templates_reviewed': None},
        'operational_completeness': {'accepted_policy_exists': accepted > 0,
                                     'all_required_bindings_verified': None},
        'native_enforcement': {'approved_target_inventory': None,
                               'positive_negative_bypass_and_recovery_evidence': None},
        'rights_and_publication': {'per_file_rights_acceptance': None,
                                   'authorized_distribution_decision': None},
        'estate_rollout': {'approved_estate_inventory': None,
                           'fresh_effective_enforcement_and_drift_evidence': None},
    }
    evaluated = [evaluate_gate(name, done, total, condition, prerequisites[name])
                 for name, done, total, condition in gates]
    return {'schema_version':'ges.recovery.v1','generated_at':now(),
            'project_complete':all(g['status'] == 'CLOSED' for g in evaluated),
            'certification_adapter_status':'INCOMPLETE_SEMANTIC_RIGHTS_AND_RUNTIME_ADAPTERS',
            'historical_checkpoint':'30b1f83c5eeb3db48ea168bdd9d4cfeb8532c040',
            'owner_url':'https://github.com/4444J99/github-engineering-standards/pull/1',
            'review_accounting':review_result,'review_receipts_digest':digest(receipts),
            'sources':sources_report,'inventory_artifacts':inventories,
            'candidate_blocks':candidates,'structured_requirements':len(requirements),
            'structured_requirements_by_source':dict(Counter(r['source'] for r in requirements)),
            'published_pages':len(pages),'rendered_bodies_acquired':acquired,
            'published_assurance_accounting': assurance,
            'unresolved_published_pages':[{'page_id':r['page_id'],'version':r['version'],'path':r['path']}
                                          for r in pages if not r['source_matches']],
            'ledger':ledger,'catalog_controls':len(controls),'catalog_digest':digest(controls),
            'quarantined_proposals':len(queue),'queue_digest':digest(queue),
            'accepted_controls':accepted,'justified_exclusions':0,
            'templates':len([p for p in (ROOT/'templates').iterdir() if p.is_file()]),
            'profiles':len(list((ROOT/'profiles').glob('*.json'))),
            'gates':evaluated}


if __name__ == '__main__':
    import argparse
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--sources',type=Path,required=True)
    p.add_argument('--corpus',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--reviews',type=Path)
    p.add_argument('--review-policy',type=Path)
    p.add_argument('--rendered-directory',type=Path,
                   help='Integrity-checked resumable body cache; acquisition is not semantic assurance')
    p.add_argument('--published-assurance',type=Path,
                   help='Optional digest-bound page assurance receipt array')
    p.add_argument('--published-assurance-policy',type=Path,
                   help='Separately approved certification/independent-audit authority, not source disposition policy')
    args=p.parse_args()
    report=status(args.sources,args.corpus,args.reviews,args.review_policy,args.rendered_directory,
                  args.published_assurance,args.published_assurance_policy)
    dump(args.output,report)
    print(json.dumps({'project_complete':report['project_complete'],
                      'gates_open':sum(g['status'] != 'CLOSED' for g in report['gates']),
                      'inventory_artifacts':report['inventory_artifacts'],'published_pages':report['published_pages']}))
