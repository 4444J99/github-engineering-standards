"""Read-only metadata/decision audit; no source acquisition or receipt issuance."""
import argparse
import hashlib
import json
from pathlib import Path
from datetime import datetime, timezone
from ges.core import digest
from ges.claim_reconciliation import RECEIPT_FIELDS, _validate_disposition
from ges.reconciliation_envelopes import ENVELOPE_FIELDS, ROLE_TIME_FIELDS

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--retained-root', type=Path, required=True)
p.add_argument('--output', type=Path, required=True)
a = p.parse_args()
root = Path(__file__).resolve().parents[2]
retained = a.retained_root
work = retained / '.cache/cloud-replay-20261012/fresh-pinned'
directory = retained / '.cache/cloud-replay-20261012/replacement-draft'
started = datetime.now(timezone.utc).isoformat()
hashes = {}
checks = 0


def require(value, message):
    global checks
    if not value:
        raise ValueError(message)
    checks += 1


def read(path, expected=None):
    require(path.is_file() and not any(x.is_symlink() for x in (path, *path.parents)), 'File path type')
    raw = path.read_bytes()
    sha = hashlib.sha256(raw).hexdigest()
    require(expected is None or sha == expected, 'Byte digest: ' + str(path))
    require(str(path) not in hashes or hashes[str(path)] == sha, 'File changed')
    hashes[str(path)] = sha
    return raw


def load(path, expected=None):
    return json.loads(read(path, expected))


manifest = load(root / 'evidence/v02-cloud-replay-20261012/manifest.json')
for item in manifest['files']:
    raw = read(root / 'evidence/v02-cloud-replay-20261012' / item['path'], item['sha256'])
    require(len(raw) == item['bytes'], 'Manifest byte length')
draft_raw = read(directory / 'replacement-decisions.draft.json', 'a8b9065b0a5a43e950451683badcbeaa335cc344bbce78940dac4420fb6d7185')
draft = json.loads(draft_raw)
old = load(root / 'evidence/wave-20261009/integration/combined-reconciliation.json', '63d1b79fe2b9d58207050abdb593adbe1ebd009bbc327643e599dd4515d6ac5c')
require(digest(draft) == '010aa6e9003301d96825cb1f34b317bafb401783e9f7462c40ac1c7d05bbb8e6', 'Draft canonical digest')
artifacts = {}
for line in read(work / 'artifacts.oct7.jsonl', '86225491fb70197b893a0bfb1fa96ebfc1f5a6e33c21c86ab874d9d34f5db9a2').splitlines():
    row = json.loads(line)
    key = tuple(row[k] for k in ('source', 'commit', 'path'))
    require(key not in artifacts, 'Duplicate artifact')
    artifacts[key] = row
inventory = load(root / 'evidence/claim-workload-v02-inventory.json', 'ed4ee7e8be9a5369d4651769dc8717456473063d2db21010544349a9848b8a00')
expected = {row['path']: row for row in inventory['inputs']['claim_documents']}
paths = sorted((root / 'evidence/source-reviews').glob('*-claims.json'))
require({path.name for path in paths} == set(expected), 'Complete document membership')
subjects = {}
for path in paths:
    doc = load(path, expected[path.name]['sha256'])
    for claim in doc['claims']:
        cid = claim['claim_id']
        require(cid not in subjects, 'Duplicate subject')
        source, commit, source_path = (claim.get(k, doc.get(k)) for k in ('source', 'commit', 'path'))
        art = artifacts[(source, commit, source_path)]
        subjects[cid] = dict(claim_id=cid, source=source, commit=commit, path=source_path,
            artifact_id=art['artifact_id'], content_sha256=art['sha256'],
            start_line=claim['start_line'], end_line=claim['end_line'],
            statement_sha256=hashlib.sha256(claim['statement'].encode()).hexdigest(),
            claim_document=path.name, claim_document_sha256=expected[path.name]['sha256'])
catalog = load(root / 'controls/catalog.json')
proposals = load(root / 'controls/review_queue.json')
bindings = (digest([subjects[k] for k in sorted(subjects)]), digest(catalog), digest(proposals))
old_index = {row['claim']['claim_id']: row for row in old}
new_index = {row['claim']['claim_id']: row for row in draft}
require(len(new_index) == len(draft) == 2174 and len(old_index) == len(old) == 2164, 'Exact unique decision counts')
audit = load(root / 'evidence/v02-finish-20261010/claim-migration-audit.json')
new_ids = {row[k] for row in audit['proposed_decisions'] for k in ('predecessor', 'successor')}
require(set(new_index) == set(old_index) | new_ids and not set(old_index) & new_ids, 'Exact decision membership')
carried_comparisons = 0
for cid, row in new_index.items():
    require(set(row) == RECEIPT_FIELDS and row['schema'] == 'ges.claim-reconciliation-receipt.draft.v1', 'Draft shape')
    require(all(row[k] is None for k in ROLE_TIME_FIELDS), 'Draft remains nonissued')
    require(row['accepted_policy'] is False and row['adopted_obligation'] is None, 'Nonadoption')
    require(digest(row['claim']) == digest(subjects[cid]), 'Exact current subject')
    require(tuple(row[k] for k in ('claim_input_digest', 'catalog_digest', 'proposal_digest')) == bindings, 'Exact bindings')
    _validate_disposition(row, set(subjects), {r['id']: r for r in catalog}, {r['id']: r for r in proposals})
    if cid in old_index:
        for field in RECEIPT_FIELDS - ENVELOPE_FIELDS - {'claim_input_digest'}:
            require(digest(row[field]) == digest(old_index[cid][field]), 'Carried decision changed')
            carried_comparisons += 1
for row in audit['proposed_decisions']:
    pred, succ = new_index[row['predecessor']], new_index[row['successor']]
    require(pred['disposition'] == 'EXCLUDED_WITH_REASON' and pred['details']['basis'] == 'SUPERSEDED' and pred['details']['related_claim_ids'] == [row['successor']], 'Supersession pair')
    require(succ['disposition'] == 'SPECIALIZE' and succ['control_references'] == [dict(collection='CATALOG', id=row['catalog'], revision=1), dict(collection='PROPOSAL', id=row['proposal'], revision=1)], 'Specialization pair')
for path, sha in list(hashes.items()):
    read(Path(path), sha)
require({p.name for p in (root / 'evidence/source-reviews').glob('*-claims.json')} == set(expected), 'Final membership')
result = dict(schema='ges.retained-draft-readiness-check.v1', status='PASS_METADATA_AND_DECISION_PRESERVATION_ONLY',
    actor='chatgpt-cloud:20261012:2aefcbff59bd:/root', started_at=started,
    completed_at=datetime.now(timezone.utc).isoformat(), checks_passed=checks,
    artifacts=len(artifacts), claim_documents=len(paths), known_claims=len(subjects),
    draft_decisions=len(draft), carried_decisions=len(old), preserved_field_comparisons=carried_comparisons,
    claim_input_digest=bindings[0], catalog_digest=bindings[1], proposal_digest=bindings[2],
    draft_sha256=hashlib.sha256(draft_raw).hexdigest(), draft_canonical_digest=digest(draft),
    file_hashes=hashes, source_acquisition_repeated=False, source_provenance_replayed=False,
    semantic_review_repeated=False, role_grant_issued=False, envelopes_issued=False,
    current_accounting_performed=False, validated_current_receipts=0,
    limits='Reuses the source replay and semantic draft review retained in PR #506. '
           'This run authenticates metadata and decision preservation only; no grant, issuance or accounting credit.')
with a.output.open('x') as stream:
    json.dump(result, stream, indent=2, sort_keys=True)
    stream.write('\n')
print(json.dumps({k: v for k, v in result.items() if k != 'file_hashes'}, indent=2))
