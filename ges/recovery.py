"""Reproducible construction accounting. Inventory never closes review gates."""
import gzip
import hashlib
import json
from collections import Counter
from pathlib import Path

from .claim_reconciliation import reconciliation_accounting
from .core import ROOT, digest, dump, load, now
from .corpus import coverage_with_reviews
from .milestones import evaluate_gate, milestone_accounting
from .source_fidelity import source_fidelity_accounting


def status(sources: Path, corpus: Path, reviews: Path | None=None, review_policy: Path | None=None,
           rendered_directory: Path | None=None, published_assurance: Path | None=None,
           published_assurance_policy: Path | None=None, rights_acceptance: Path | None=None,
           rights_acceptance_policy: Path | None=None, source_fidelity: Path | None=None,
           source_fidelity_policy: Path | None=None,
           claim_reconciliation: Path | None=None,
           claim_reconciliation_policy: Path | None=None,
           publication_manifest: Path | None=None,
           publication_register: Path | None=None,
           publication_receipts: Path | None=None,
           publication_policy: Path | None=None,
           publication_output_root: Path | None=None) -> dict:
    publication_inputs = (
        publication_manifest, publication_register, publication_receipts,
        publication_policy, publication_output_root,
    )
    if any(value is not None for value in publication_inputs) and not all(
            value is not None for value in publication_inputs):
        raise ValueError('Publication use accounting requires manifest, register, '
                         'receipts, approved policy and candidate output root together')
    paired_inputs = (
        (reviews, review_policy, 'Source reviews'),
        (published_assurance, published_assurance_policy, 'Published assurance'),
        (rights_acceptance, rights_acceptance_policy, 'Rights acceptance'),
        (source_fidelity, source_fidelity_policy, 'Source fidelity'),
        (claim_reconciliation, claim_reconciliation_policy, 'Claim reconciliation'),
    )
    for evidence, policy, label in paired_inputs:
        if (evidence is None) != (policy is None):
            raise ValueError(label + ' requires both receipts and authority policy')
    if ((source_fidelity is not None or claim_reconciliation is not None) and
            reviews is None):
        raise ValueError('Semantic certification requires source reviews and review policy')
    controls = load(ROOT/'controls/catalog.json')
    queue = load(ROOT/'controls/review_queue.json')
    pins = load(ROOT/'sources/sources.lock.json')['sources']
    pin_map = {pin['repository']: pin['commit'] for pin in pins}
    review_policy_document = load(review_policy) if review_policy is not None else None
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
                         authorized_reviewers=(review_policy_document['authorized_reviewers']
                                               if review_policy_document else []))
    if review_result['errors']: raise ValueError('Invalid review receipts: '+str(review_result['errors']))
    reviewed_by_source=Counter()
    corpus_artifacts=[json.loads(l) for l in (corpus/'artifacts.jsonl').read_text().splitlines() if l.strip()]
    artifacts_by_id={r['artifact_id']:r for r in corpus_artifacts}
    corpus_identities={(r['source'],r['commit'],r['path'],r['sha256']) for r in corpus_artifacts}
    if len(artifacts_by_id) != len(corpus_artifacts) or len(corpus_identities) != len(corpus_artifacts):
        raise ValueError('Duplicate corpus artifact identity')
    for receipt in receipts:
        reviewed_by_source[artifacts_by_id[receipt['artifact_id']]['source']] += 1
    sources_report = []
    locked_identities=set()
    for pin in pins:
        slug = pin['repository'].replace('/', '__')
        inventory = load(sources/(slug+'.inventory.json'))
        if any(r['source'] != pin['repository'] or r['commit'] != pin['commit'] for r in inventory):
            raise ValueError('Inventory does not match release pin: '+pin['repository'])
        identities={(r['source'],r['commit'],r['path'],r['sha256']) for r in inventory}
        if len(identities) != len(inventory) or locked_identities & identities:
            raise ValueError('Duplicate locked source artifact identity')
        locked_identities.update(identities)
        tree = load(sources/(slug+'.tree-reconciliation.json'))
        sources_report.append({'repository': pin['repository'], 'commit': pin['commit'],
                               'artifacts': len(inventory), 'reviewed_artifacts': reviewed_by_source[pin['repository']],
                               'review_evidence': 'evidence/source-reviews; source review is not control adoption or independent omission certification',
                               'git_tree_reconciliation': tree})
    if corpus_identities != locked_identities:
        raise ValueError('Corpus identities/digests differ from complete locked inventories')
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
    from .published_assurance import assurance_accounting
    assurance = assurance_accounting(
        corpus/'published-page-ledger.json', rendered_directory, corpus/'artifacts.jsonl',
        load(published_assurance) if published_assurance is not None else [],
        load(published_assurance_policy) if published_assurance_policy is not None else {},
        pin_map, evidence_root=ROOT)
    from .rights_acceptance import rights_accounting
    rights = rights_accounting(
        corpus_artifacts, pin_map,
        load(ROOT/'evidence/rights-review-queue.json')['records'],
        load(rights_acceptance) if rights_acceptance is not None else [],
        load(rights_acceptance_policy) if rights_acceptance_policy is not None else {},
        evidence_root=ROOT)
    publication = None
    if publication_manifest is not None:
        from .publication_use import publication_accounting
        publication = publication_accounting(
            load(publication_manifest), load(publication_register),
            load(publication_receipts), load(publication_policy),
            corpus_artifacts, pin_map, output_root=publication_output_root,
            source_root=sources, evidence_root=ROOT)
    accepted = sum(c['status'] == 'ACCEPTED' for c in controls)
    canonical_ids = {c['id'] for c in controls}
    if canonical_ids & {c['id'] for c in queue} or len({c['id'] for c in queue}) != len(queue):
        raise ValueError('Review queue IDs duplicate canonical or proposal IDs')

    if reviews is not None:
        fidelity = source_fidelity_accounting(
            corpus/'artifacts.jsonl', corpus/'candidates.jsonl', reviews,
            review_policy_document, sources, controls, pin_map,
            load(source_fidelity) if source_fidelity is not None else None,
            load(source_fidelity_policy) if source_fidelity_policy is not None else None,
            proposals=queue,
            evidence_root=ROOT)
        if any(reviews.glob('*-claims.json')):
            reconciliation = reconciliation_accounting(
                corpus/'artifacts.jsonl', sources, reviews, review_policy_document,
                pin_map, controls, queue,
                load(claim_reconciliation) if claim_reconciliation is not None else None,
                (load(claim_reconciliation_policy)
                 if claim_reconciliation_policy is not None else None))
        else:
            if claim_reconciliation is not None:
                raise ValueError(
                    'Claim reconciliation requires reviewed claim documents')
            reconciliation = {
                'schema': 'ges.claim-reconciliation-accounting.v1',
                'known_claim_denominator': None,
                'validated_count': 0,
                'unresolved_count': None,
                'validated_claim_ids': [],
                'mapping_complete': None,
                'claim_provenance_validated': False,
            }
    else:
        fidelity = {
            'schema': 'ges.source-fidelity-accounting.v1',
            'reviewed': 0,
            'inventoried': inventories,
            'remaining': inventories,
            'coverage_complete': None if inventories == 0 else False,
            'reference_claims': 0,
            'claim_provenance_validated': None,
            'atomic_claim_fidelity_audit': None,
            'independent_source_to_claim_omission_audit': None,
            'evaluation': 'UNVERIFIED',
        }
        reconciliation = {
            'schema': 'ges.claim-reconciliation-accounting.v1',
            'known_claim_denominator': None,
            'validated_count': 0,
            'unresolved_count': None,
            'validated_claim_ids': [],
            'mapping_complete': None,
            'claim_provenance_validated': None,
        }
    reconciliation = {
        **reconciliation,
        'structured_occurrences_completed': 0,
        'structured_occurrence_denominator': len(requirements),
        'all_structured_occurrences_reconciled': None,
    }
    gates = [
        ('exhaustive_artifact_accounting',review_result['reviewed'],inventories,'Every artifact has a validated reviewed disposition and independent omission audit'),
        ('published_content_assurance',assurance['completed'],len(pages),'Every page has rendered/version/dependency review; retrieval alone is insufficient'),
        ('semantic_extraction',fidelity['reviewed'],fidelity['inventoried'],'Full-artifact omission review and atomic claims; candidate count is not a claim denominator'),
        ('consolidation',reconciliation['validated_count'],reconciliation['known_claim_denominator'],'All structured occurrences mapped with exact provenance; remaining unstructured claims also reviewed'),
        ('generalization',0,len(controls)+len(queue),'Every definition and proposal has reviewed scope, policy, parameters and conflicts'),
        ('operational_completeness',0,accepted,'Accepted controls have all required tested bindings and accountable review procedures'),
        ('native_enforcement',0,None,'Approved target inventory, positive/negative behavior tests and recovery receipts'),
        ('rights_and_publication',rights['completed'],inventories,'Per-file rights review and approved distribution; inventory notices alone insufficient'),
        ('estate_rollout',0,None,'Explicit authorized inventory and effective-policy/behavior evidence per target'),
    ]
    # Missing semantic, rights and runtime certification is UNKNOWN, not an
    # invented failed audit or a successful count-only test. These adapters must
    # be implemented and supplied validated evidence before their values change.
    prerequisites = {
        'exhaustive_artifact_accounting': {
            'pinned_git_trees_match': all(s['git_tree_reconciliation'].get('status') == 'MATCH' for s in sources_report),
            'review_receipts_valid': not review_result['errors'],
            'independent_omission_audit': fidelity['independent_source_to_claim_omission_audit']},
        'published_content_assurance': {
            'all_bodies_durably_acquired': acquired == len(pages),
            'all_source_paths_reconciled': all(p['source_matches'] for p in pages),
            'version_include_and_render_assurance': assurance['version_include_and_render_assurance']},
        'semantic_extraction': {
            'atomic_claim_fidelity_audit': fidelity['atomic_claim_fidelity_audit'],
            'independent_source_to_claim_omission_audit': fidelity['independent_source_to_claim_omission_audit'],
            'claim_document_provenance_validated': fidelity['claim_provenance_validated']},
        'consolidation': {
            'exact_claim_mapping_and_conflict_review': reconciliation['mapping_complete'],
            'unstructured_claim_denominator_certified': fidelity['independent_source_to_claim_omission_audit'],
            'all_structured_occurrences_reconciled': reconciliation['all_structured_occurrences_reconciled']},
        'generalization': {'profiles_parameters_and_templates_reviewed': None},
        'operational_completeness': {'accepted_policy_exists': accepted > 0,
                                     'all_required_bindings_verified': None},
        'native_enforcement': {'approved_target_inventory': None,
                               'positive_negative_bypass_and_recovery_evidence': None},
        'rights_and_publication': {'per_file_rights_acceptance': rights['per_file_rights_acceptance'],
                                   'authorized_distribution_decision': rights['authorized_distribution_decision']},
        'estate_rollout': {'approved_estate_inventory': None,
                           'fresh_effective_enforcement_and_drift_evidence': None},
    }
    evaluated = [evaluate_gate(name, done, total, condition, prerequisites[name])
                 for name, done, total, condition in gates]
    milestones = milestone_accounting(evaluated, publication)
    return {'schema_version':'ges.recovery.v1','generated_at':now(),
            'project_complete':all(g['status'] == 'CLOSED' for g in evaluated),
            'milestone_accounting': milestones,
            'certification_adapter_status':'INCOMPLETE_STRUCTURED_GENERALIZATION_ADOPTION_BINDING_AND_RUNTIME_ADAPTERS',
            'certification_adapters': {
                'source_fidelity_and_omission': 'IMPLEMENTED_PINNED_ARTIFACT_RECEIPTS_ONLY',
                'claim_reconciliation': 'IMPLEMENTED_PROVENANCE_BOUND_CLAIM_RECEIPTS_ONLY',
                'structured_occurrence_reconciliation': 'NOT_IMPLEMENTED',
                'generalization': 'NOT_IMPLEMENTED',
                'policy_adoption': 'NOT_IMPLEMENTED',
                'binding_verification': 'NOT_IMPLEMENTED',
                'native_and_estate_verification': 'NOT_IMPLEMENTED',
                'published_assurance': 'IMPLEMENTED_LOCKED_SOURCE_ONLY',
                'rights_acceptance': 'IMPLEMENTED_PINNED_ARTIFACTS_ONLY',
                'publication_use': 'IMPLEMENTED_EXACT_OUTPUT_USE_RECEIPTS_ONLY'},
            'historical_checkpoint':'30b1f83c5eeb3db48ea168bdd9d4cfeb8532c040',
            'owner_url':'https://github.com/4444J99/github-engineering-standards/pull/1',
            'review_accounting':review_result,'review_receipts_digest':digest(receipts),
            'sources':sources_report,'inventory_artifacts':inventories,
            'candidate_blocks':candidates,'structured_requirements':len(requirements),
            'structured_requirements_by_source':dict(Counter(r['source'] for r in requirements)),
            'published_pages':len(pages),'rendered_bodies_acquired':acquired,
            'published_assurance_accounting': assurance,
            'rights_acceptance_accounting': rights,
            'publication_use_accounting': publication,
            'source_fidelity_accounting': fidelity,
            'claim_reconciliation_accounting': reconciliation,
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
    p.add_argument('--rights-acceptance',type=Path,
                   help='Optional exact-use per-file rights acceptance receipts')
    p.add_argument('--rights-acceptance-policy',type=Path,
                   help='Separately approved rights/human/distribution authority; not triage policy')
    p.add_argument('--source-fidelity',type=Path,
                   help='Optional digest-bound source-fidelity certification receipt array')
    p.add_argument('--source-fidelity-policy',type=Path,
                   help='Separately approved fidelity and omission-audit authority')
    p.add_argument('--claim-reconciliation',type=Path,
                   help='Optional exact-claim reconciliation receipt array')
    p.add_argument('--claim-reconciliation-policy',type=Path,
                   help='Separately approved reconciliation authority')
    p.add_argument('--publication-manifest',type=Path,
                   help='Exact public release output inventory; requires all publication inputs')
    p.add_argument('--publication-register',type=Path,
                   help='Actual upstream-expression uses for the exact candidate output set')
    p.add_argument('--publication-receipts',type=Path,
                   help='Exact-use review, independent audit, human acceptance and distribution evidence')
    p.add_argument('--publication-policy',type=Path,
                   help='Separately approved publication inventory and use authority')
    p.add_argument('--publication-output-root',type=Path,
                   help='Candidate directory whose complete file set and bytes must match the manifest')
    args=p.parse_args()
    report=status(args.sources,args.corpus,args.reviews,args.review_policy,args.rendered_directory,
                  args.published_assurance,args.published_assurance_policy,
                  args.rights_acceptance,args.rights_acceptance_policy,
                  args.source_fidelity,args.source_fidelity_policy,
                  args.claim_reconciliation,args.claim_reconciliation_policy,
                  args.publication_manifest,args.publication_register,
                  args.publication_receipts,args.publication_policy,
                  args.publication_output_root)
    dump(args.output,report)
    print(json.dumps({'project_complete':report['project_complete'],
                      'gates_open':sum(g['status'] != 'CLOSED' for g in report['gates']),
                      'milestones': {name: item['evaluation'] for name, item in
                                     report['milestone_accounting']['milestones'].items()},
                      'ges_v0_2': report['milestone_accounting']['ges_v0_2']['evaluation'],
                      'inventory_artifacts':report['inventory_artifacts'],'published_pages':report['published_pages']}))
