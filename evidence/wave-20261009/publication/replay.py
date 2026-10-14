"""Replay bounded C comparisons; upstream text stays in authenticated cache."""
import collections
import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import sys

from ges.publication_triage import _json_spans

ROOT = Path(__file__).resolve().parents[3]
DEST = Path(__file__).resolve().parent
PACKET = ROOT / 'evidence/publication-candidates/ges-v0.2-merged-f628db26-20261008'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def span(data, start, end):
    return {'start_byte': start, 'end_byte': end, 'sha256': sha(data[start:end])}


def main():
    source_root = Path(sys.argv[1])
    assignment = json.loads((ROOT / 'evidence/wave-20261009/assignment.json').read_bytes())
    cache = json.loads((ROOT / 'evidence/wave-20261009/cache-validation.json').read_bytes())
    revision = assignment['publication_revision']
    raw = subprocess.check_output(['git', 'show', revision + ':controls/review_queue.json'], cwd=ROOT)
    queue = json.loads(raw)
    spans = _json_spans(raw)
    triage = json.loads(gzip.decompress((PACKET / 'output-triage.json.gz').read_bytes()))
    artifacts = {x['artifact_id']: x for x in triage['source_artifacts']}
    source_cache = source_root / 'microsoft__ghqr.text.jsonl.gz'
    expected = next(x for x in cache['snapshots'] if x['source'] == 'microsoft/ghqr')
    assert sha(source_cache.read_bytes()) == expected['snapshot_sha256']
    sources = {x['path']: x for x in map(json.loads, gzip.open(source_cache, 'rt'))}
    manifest = json.loads((PACKET / 'manifest.json').read_bytes())
    assert next(x for x in manifest['outputs'] if x['path'] == 'controls/review_queue.json')['sha256'] == sha(raw)
    notice = subprocess.check_output(['git', 'show', revision + ':THIRD_PARTY_NOTICES.md'], cwd=ROOT)
    license_raw = sources['LICENSE']['content'].encode()
    license_start = notice.index(license_raw)
    attribution = {'output_path': 'THIRD_PARTY_NOTICES.md', 'output_range': span(notice, license_start, license_start + len(license_raw))}
    license_artifact = next(x for x in artifacts.values() if x['source'] == 'microsoft/ghqr' and x['path'] == 'LICENSE')
    assert sha(license_raw) == license_artifact['sha256']
    reviews, uses, unresolved = [], [], []
    for selected in assignment['C']['selected_proposals']:
        i = selected['proposal_index']
        proposal = queue[i]
        assert proposal['id'] == selected['proposal_id']
        source = proposal['sources'][0]
        artifact = next(x for x in artifacts.values() if x['source'] == source['repository'] and x['path'] == source['path'])
        source_bytes = sources[source['path']]['content'].encode()
        assert sha(source_bytes) == artifact['sha256']
        assert sources[source['path']]['commit'] == source['commit'] == expected['commit']
        # Bound interpretation to the actual recommendation block, not any coincidental match elsewhere.
        marker = ('- id: ' + source['section']).encode()
        block_start = source_bytes.index(marker)
        next_block = source_bytes.find(b'\n- id: ', block_start + len(marker))
        block_end = next_block if next_block >= 0 else len(source_bytes)
        block = source_bytes[block_start:block_end]
        reviewed_fields = []
        for suffix, value in [('title', proposal['title']), ('objective', proposal['objective']), ('implementation/acceptance/0', proposal['implementation']['acceptance'][0])]:
            pointer = f'/{i}/{suffix}'
            encoded = value.encode()
            pos = block.find(encoded)
            output_range = spans[pointer]
            output_bytes = raw[output_range['start_byte']:output_range['end_byte']]
            assert pos >= 0, (proposal['id'], suffix)
            source_range = span(source_bytes, block_start + pos, block_start + pos + len(encoded))
            exact = output_bytes == encoded
            use = {'use_id': proposal['id'] + '-' + suffix.replace('/', '-'),
                   'kind': 'LICENSED_COPY' if exact else None,
                   'source': {k: artifact[k] for k in ('artifact_id', 'source', 'commit', 'path', 'sha256')},
                   'source_range': source_range, 'output_path': 'controls/review_queue.json',
                   'output_range': output_range, 'attributions': [attribution],
                   'rationale': 'Proposal reuses the pinned GHQR recommendation block wording as its ' + suffix + '. Microsoft MIT notice is retained at the exact candidate notice span. ' + ('Raw output bytes equal the source expression; proposed LICENSED_COPY remains subject to independent review and human/distribution approval.' if exact else 'Decoded JSON string equals source wording, but raw JSON escapes differ. Classification unresolved: LICENSED_COPY raw-byte invariant fails and no semantic adaptation is established by encoding alone.'),
                   'classification_status': 'PROPOSED_NOT_APPROVED' if exact else 'UNRESOLVED_JSON_ENCODING',
                   'json_pointer': pointer, 'decoded_text_sha256': sha(encoded),
                   'source_context_range': span(source_bytes, block_start, block_end),
                   'attribution_obligation': 'Retain Microsoft copyright and complete MIT permission/disclaimer notice with copies or substantial portions; actual-use approval outstanding.'}
            uses.append(use)
            reviewed_fields.append(pointer)
            if not exact:
                unresolved.append({'use_id': use['use_id'], 'finding': 'Raw JSON escaping prevents a LICENSED_COPY row under the current raw-range equality contract; independent judgment or encoding-aware contract change required.'})
        # Locators are factual identity references, not a substitute for expression rows.
        for j, locator in enumerate(proposal['sources']):
            pointer = f'/{i}/sources/{j}/url'
            uses.append({'use_id': proposal['id'] + f'-reference-{j}', 'kind': 'REFERENCES_ONLY',
                         'source': {k: artifact[k] for k in ('artifact_id', 'source', 'commit', 'path', 'sha256')},
                         'source_range': None, 'output_path': 'controls/review_queue.json',
                         'output_range': spans[pointer], 'attributions': [],
                         'rationale': 'Pinned URL is a provenance locator for the source block. Expressive title and recommendation wording are separately recorded, so this does not classify the whole proposal as reference-only.',
                         'classification_status': 'PROPOSED_NOT_APPROVED', 'json_pointer': pointer})
        reviews.append({'proposal_id': proposal['id'], 'json_pointer': f'/{i}',
                        'expression_fields_inspected': reviewed_fields,
                        'other_fields_inspected': [f'/{i}/' + k for k in proposal if k not in ('title', 'objective')],
                        'other_fields_judgment': 'IDs, revision, applicability, severity translation and source locators are structured metadata; generic implementation, evidence, enforcement and quarantine wording has no identified GHQR expression in the bound source block. No independent-authorship or whole-proposal clearance is certified. Source-strength local-policy wording is not itself adoption.',
                        'boilerplate_acceptance_pointer': f'/{i}/implementation/acceptance/1',
                        'source_context_range': span(source_bytes, block_start, block_end),
                        'component_notice_observation': 'No separate copyright, license or third-party notice in the selected YAML block; pinned repository LICENSE supplies Microsoft MIT terms. Linked external documentation expression is not copied in these inspected fields.',
                        'disposition': 'PARTIAL_REVIEW_ONLY'})
    result = {'schema': 'ges.bounded-publication-review.v1',
              'reviewer': 'codex:/root/publication_worker_c', 'status': 'Staged',
              'candidate_revision': revision, 'candidate_id': manifest['candidate_id'],
              'bindings': [{'path': str(p.relative_to(ROOT)), 'sha256': sha(p.read_bytes())} for p in [ROOT / 'evidence/wave-20261009/assignment.json', ROOT / 'evidence/wave-20261009/cache-validation.json', PACKET / 'manifest.json', PACKET / 'register.json', PACKET / 'output-triage.json.gz', PACKET / 'review-priorities.json']],
              'source_snapshot': {'path': source_cache.name, 'sha256': expected['snapshot_sha256'], 'source': 'microsoft/ghqr', 'commit': expected['commit']},
              'source_inventory_reference_sha256': cache['reference_sha256'],
              'license_source': license_artifact, 'license_source_range': span(license_raw, 0, len(license_raw)),
              'coverage': {'candidate_output_files': 2396, 'candidate_proposals': 593, 'matched_proposals': 543,
                           'selected_proposals_inspected': len(reviews), 'expression_fields_inspected': 150,
                           'unselected_proposals': 543, 'unselected_matched_proposals': 493,
                           'outputs_fully_cleared': 0, 'outputs_remaining_unreviewed': 2396},
              'uses': uses, 'proposal_reviews': reviews, 'unresolved_findings': unresolved,
              'classification_counts': dict(collections.Counter(x['kind'] or 'UNRESOLVED' for x in uses)),
              'remaining_scope': ['Independent omission review; reconciled classifications; independent decision audit.', 'JSON-escaped raw-span classification unresolved where recorded.', 'Complete candidate inventory/use review and all human/distribution approvals remain outstanding.', 'No original register, policy, receipts, candidate bytes or historical packets changed.'],
              'publication_clearance': None, 'human_approvals_created': False, 'distribution_approvals_created': False}
    (DEST / 'primary-review.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'coverage': result['coverage'], 'classification_counts': result['classification_counts'], 'review_sha256': sha((DEST / 'primary-review.json').read_bytes())}, indent=2))


if __name__ == '__main__':
    main()
