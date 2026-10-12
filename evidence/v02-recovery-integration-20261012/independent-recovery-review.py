"""Independent metadata audit of the executed recovery; no receipt issuance.

Run from the repository root with --execution-directory and a new --output path.
This reads authenticated private inputs but writes only metadata and boundaries.
It does not repeat semantic decisions or replace source-to-claim omission review.
"""
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import time


TRUSTED_A3_SHA256 = '05dab95bfbc88c2401a97da702339f4f1be89545c8f8c9f48198194aac07bb15'
TRUSTED_REPLAY_SHA256 = 'da51b1279a8a7bd6b671193774180e2eab406049b9b6af1729b9f2ef83840937'
TRUSTED_LEDGER_SHA256 = 'b4147bf94b13d18188b7acc775c1f7508f1653f2737bcecc7f27920afe58b73f'
TRUSTED_POLICY_SHA256 = '06e34189c0d9a30d3d7a592e3e229ded0c22452a47f656e5bcae1e5bdb994f98'
TRUSTED_PRIOR_ACCOUNTING_SHA256 = '9c8f4ac148a22e67ee537999251987c13daeede88b11f751dd0988d825696dd5'
TRUSTED_OCT7_ARTIFACTS_SHA256 = '86225491fb70197b893a0bfb1fa96ebfc1f5a6e33c21c86ab874d9d34f5db9a2'
CHECKS = 0


def check(condition, message):
    global CHECKS
    CHECKS += 1
    if not condition:
        raise ValueError(message)


def sha(path):
    check(path.is_file() and not any(p.is_symlink() for p in (path, *path.parents)),
          'Missing, nonregular or symlinked audit input: ' + str(path))
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def load(path):
    return json.loads(path.read_text(encoding='utf-8'))


def canonical(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'),
                                     ensure_ascii=True).encode()).hexdigest()


def jsonl(path):
    with path.open(encoding='utf-8') as stream:
        return [json.loads(line) for line in stream if line.strip()]


def command_path(command, flag, root):
    check(command.count(flag) == 1, 'Ambiguous recorded argument: ' + flag)
    path = Path(command[command.index(flag) + 1])
    return path if path.is_absolute() else root / path


def references(document):
    pending = [document]
    while pending:
        item = pending.pop()
        if isinstance(item, dict):
            pending.extend(item.values())
        elif isinstance(item, list):
            pending.extend(item)
        elif isinstance(item, str) and item.startswith('evidence/') and item.endswith('.json'):
            yield item


def current_closure(root, sources, corpus, ledger, policy):
    result = {}
    directories = {
        'sources': sources, 'corpus': corpus, 'code': root / 'ges',
        'reviews': root / 'evidence/source-reviews', 'controls': root / 'controls',
        'templates': root / 'templates', 'profiles': root / 'profiles',
    }
    for label, directory in directories.items():
        check(directory.is_dir(), 'Missing input directory: ' + label)
        for path in sorted(directory.rglob('*')):
            check(not any(part.is_symlink() for part in (path, *path.parents)),
                  'Symlink input in ' + label)
            if path.is_file() and '__pycache__' not in path.parts:
                result[label + '/' + path.relative_to(directory).as_posix()] = sha(path)
    for label, path in {
        'issued-receipts': ledger, 'issued-policy': policy,
        'source-lock': root / 'sources/sources.lock.json',
        'review-policy': root / 'evidence/source-review-policy.json',
        'rights-queue': root / 'evidence/rights-review-queue.json',
    }.items():
        result[label] = sha(path)
    pending = list((root / 'evidence/source-reviews').glob('*.json'))
    seen = set()
    while pending:
        path = pending.pop()
        if path in seen:
            continue
        seen.add(path)
        for reference in references(load(path)):
            relative = Path(reference)
            check(not relative.is_absolute() and '..' not in relative.parts,
                  'Unsafe supporting-evidence reference')
            target = root / relative
            if target.is_file():
                result['support/' + reference] = sha(target)
                pending.append(target)
    return dict(sorted(result.items()))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=Path.cwd())
    parser.add_argument('--execution-directory', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    started_at = datetime.now(timezone.utc).isoformat()
    clock = time.monotonic()
    root = args.repo.absolute()
    execution_directory = args.execution_directory.absolute()
    check(not args.output.exists(), 'Audit output already exists')
    script_sha256 = sha(Path(__file__).absolute())
    execution_sha256 = sha(execution_directory / 'execution.json')
    execution = load(execution_directory / 'execution.json')
    check(execution['exit_code'] == 0 and execution['timed_out'] is False,
          'Recovery did not finish successfully')
    check(execution['input_closure_unchanged'] is True and execution['driver_unchanged'] is True,
          'Execution did not retain stable inputs and driver')
    before_path = execution_directory / 'input-closure-before.json'
    after_path = execution_directory / 'input-closure-after.json'
    before, after = load(before_path), load(after_path)
    check(before == after and len(before) == execution['input_files'],
          'Recorded closure membership or bytes changed')
    check(sha(before_path) == execution['input_closure_sha256'], 'Closure digest changed')
    for name, key in (('stdout.json', 'stdout_sha256'), ('stderr.txt', 'stderr_sha256'),
                      ('recovery-current.json', 'recovery_report_sha256')):
        check(sha(execution_directory / name) == execution[key], 'Recorded output changed: ' + name)
    check((execution_directory / 'stderr.txt').stat().st_size == 0, 'Unexpected recovery stderr')
    command = execution['command']
    check(command[1:3] == ['-m', 'ges.recovery'], 'Recorded command is not recovery')
    sources = command_path(command, '--sources', root)
    corpus = command_path(command, '--corpus', root)
    ledger = command_path(command, '--claim-reconciliation', root)
    policy_path = command_path(command, '--claim-reconciliation-policy', root)
    check(command_path(command, '--output', root) == execution_directory / 'recovery-current.json',
          'Recorded output location changed')
    check(current_closure(root, sources, corpus, ledger, policy_path) == before,
          'Current source, code, corpus, reviews or supporting evidence differs from execution')
    driver = root / 'evidence/v02-recovery-integration-20261012/run-recovery.py'
    check(sha(driver) == execution['driver_sha256'] == execution['driver_sha256_after'],
          'Preserved execution driver changed')

    a3_path = root / 'evidence/a3-six-source-capsule-repair.json'
    check(sha(a3_path) == TRUSTED_A3_SHA256, 'Independent A3 reference changed')
    a3 = load(a3_path)
    exact_members = []
    for name in ('candidates.jsonl', 'dependencies.jsonl', 'published-page-ledger.json',
                 'structured-source-requirements.json', 'ledger-summary.json'):
        wanted = a3['capsule_manifest']['files'].get('corpus/' + name,
                                                   a3['supplement_files'].get(name))
        check(sha(corpus / name) == wanted['sha256'] and
              (corpus / name).stat().st_size == wanted['bytes'], 'A3 member differs: ' + name)
        exact_members.append(name)
    check(sha(corpus / 'artifacts.jsonl') == TRUSTED_OCT7_ARTIFACTS_SHA256,
          'Preserved October 7 artifact metadata changed')
    check(before['corpus/artifacts.jsonl'] != a3['capsule_manifest']['files']['corpus/artifacts.jsonl']['sha256'],
          'Unexpected artifact-byte provenance: inspect rather than assume historical restoration')
    replay_path = root / 'evidence/v02-cloud-replay-20261012/execution.v1.json'
    check(sha(replay_path) == TRUSTED_REPLAY_SHA256, 'Independent source replay reference changed')
    replay = load(replay_path)
    for name, fingerprint in replay['source_input_hashes_after_replay'].items():
        check(before.get(name) == fingerprint, 'Retained source differs from executed replay: ' + name)
    check(len([key for key in before if key.startswith('sources/')]) == 23,
          'Retained source membership changed')

    check(sha(ledger) == TRUSTED_LEDGER_SHA256, 'Approved final ledger bytes changed')
    check(sha(policy_path) == TRUSTED_POLICY_SHA256, 'Approved policy bytes changed')
    prior_path = root / 'evidence/v02-authorized-reconciliation-20261012/current-accounting.json'
    check(sha(prior_path) == TRUSTED_PRIOR_ACCOUNTING_SHA256, 'Prior accounting reference changed')
    prior = load(prior_path)
    receipts, policy = load(ledger), load(policy_path)
    report = load(execution_directory / 'recovery-current.json')
    reconciliation = report['claim_reconciliation_accounting']
    for key in ('known_claim_denominator', 'validated_count', 'unresolved_count',
                'validated_claim_ids', 'disposition_counts', 'claim_input_digest',
                'catalog_digest', 'proposal_digest', 'receipts_digest', 'policy_digest'):
        check(reconciliation[key] == prior[key], 'Prior issued accounting differs: ' + key)
    artifacts = jsonl(corpus / 'artifacts.jsonl')
    artifact_index = {(row['source'], row['commit'], row['path']): row for row in artifacts}
    check(len(artifact_index) == len(artifacts) == 13657, 'Artifact identity count changed')
    subjects = {}
    claim_documents = sorted((root / 'evidence/source-reviews').glob('*-claims.json'))
    for path in claim_documents:
        document, document_sha = load(path), sha(path)
        for claim in document['claims']:
            identity = tuple(claim.get(key, document.get(key)) for key in ('source', 'commit', 'path'))
            artifact = artifact_index[identity]
            subject = {
                'claim_id': claim['claim_id'], 'source': identity[0], 'commit': identity[1],
                'path': identity[2], 'artifact_id': artifact['artifact_id'],
                'content_sha256': artifact['sha256'], 'start_line': claim['start_line'],
                'end_line': claim['end_line'],
                'statement_sha256': hashlib.sha256(claim['statement'].encode()).hexdigest(),
                'claim_document': path.name, 'claim_document_sha256': document_sha,
            }
            check(subject['claim_id'] not in subjects, 'Duplicate current claim identity')
            subjects[subject['claim_id']] = subject
    check(len(subjects) == 61941 and len(claim_documents) == 655, 'Current claim universe changed')
    universe_digest = canonical(sorted(subjects.values(), key=lambda item: item['claim_id']))
    check(universe_digest == reconciliation['claim_input_digest'] == policy['claim_input_digest'],
          'Reconstructed current claim universe differs')
    ids = []
    for receipt in receipts:
        subject = receipt['claim']
        check(subject == subjects.get(subject['claim_id']), 'Issued claim subject changed')
        check(receipt['accepted_policy'] is False and receipt['adopted_obligation'] is None,
              'Issued receipt gained adoption authority')
        check(receipt['reconciler'] in policy['authorized_reconcilers'] and
              receipt['independent_reviewer'] in policy['authorized_independent_reviewers'] and
              receipt['reconciler'] != receipt['independent_reviewer'], 'Original role pair changed')
        ids.append(subject['claim_id'])
    check(len(ids) == len(set(ids)) == 2174 and sorted(ids) == reconciliation['validated_claim_ids'],
          'Issued receipt membership differs from final recovery')
    check(dict(Counter(row['disposition'] for row in receipts)) == reconciliation['disposition_counts'],
          'Issued disposition counts differ')
    check(canonical(receipts) == reconciliation['receipts_digest'], 'Issued receipt canonical digest differs')
    check(reconciliation['validated_count'] + reconciliation['unresolved_count'] == len(subjects),
          'Claim arithmetic differs')
    check(reconciliation['claim_provenance_validated'] is True and reconciliation['mapping_complete'] is False,
          'Reconciliation boundary changed')

    candidates = jsonl(corpus / 'candidates.jsonl')
    pages = load(corpus / 'published-page-ledger.json')
    structured = load(corpus / 'structured-source-requirements.json')
    check(len(candidates) == len({row['candidate_id'] for row in candidates}) == 150903,
          'Candidate membership differs')
    check(len(pages) == 18019 and sum(not row['source_matches'] for row in pages) == 14,
          'Original page universe or unresolved mappings changed')
    check(len(structured) == 605, 'Structured denominator changed')
    for key, expected in {'inventory_artifacts': 13657, 'candidate_blocks': 150903,
                          'structured_requirements': 605, 'published_pages': 18019,
                          'rendered_bodies_acquired': 0, 'accepted_controls': 0,
                          'catalog_controls': 95, 'quarantined_proposals': 593}.items():
        check(report[key] == expected, 'Report denominator differs: ' + key)
    check(report['review_accounting']['reviewed'] == 3590 and not report['review_accounting']['errors'],
          'Artifact review accounting changed')
    check(report['publication_use_accounting'] is None, 'Publication clearance unexpectedly supplied')
    gates = report['gates']
    check(len(gates) == len({gate['gate'] for gate in gates}) == 9, 'Gate membership changed')
    for gate in gates:
        denominator, completed = gate['denominator'], gate['completed']
        coverage = None if denominator in (None, 0) else completed == denominator
        check(gate['conditions']['coverage_complete'] is coverage, 'Gate coverage differs')
        check(gate['remaining'] == (None if denominator is None else denominator - completed),
              'Gate remaining count differs')
        incomplete = sorted(key for key, value in gate['conditions'].items() if value is False)
        unknown = sorted(key for key, value in gate['conditions'].items() if value is None)
        check(sorted(gate['incomplete_conditions']) == incomplete and
              sorted(gate['unverified_conditions']) == unknown, 'Gate observations differ')
        check(gate['status'] == 'OPEN' and (incomplete or unknown), 'A gate was improperly closed')
        check(gate['evaluation'] == ('INCOMPLETE' if incomplete else 'UNVERIFIED'),
              'Gate evaluation differs')
    milestone_states = {'six_source_synthesis': 'INCOMPLETE', 'public_release_clearance': 'UNVERIFIED',
                        'native_pilot_acceptance': 'UNVERIFIED', 'estate_rollout': 'UNVERIFIED'}
    milestones = report['milestone_accounting']
    for name, expected in milestone_states.items():
        check(milestones['milestones'][name]['evaluation'] == expected and
              milestones['milestones'][name]['status'] == 'OPEN', 'Milestone boundary differs: ' + name)
    check(milestones['ges_v0_2']['evaluation'] == 'INCOMPLETE' and
          milestones['ges_v0_2']['estate_rollout_required'] is False and
          report['project_complete'] is False and
          milestones['governance_acceptance_automatically_certified'] is False,
          'Release or acceptance boundary changed')
    check(current_closure(root, sources, corpus, ledger, policy_path) == before,
          'Inputs changed during independent audit')
    for name, key in (('stdout.json', 'stdout_sha256'), ('stderr.txt', 'stderr_sha256'),
                      ('recovery-current.json', 'recovery_report_sha256')):
        check(sha(execution_directory / name) == execution[key], 'Output changed during audit: ' + name)
    check(sha(execution_directory / 'execution.json') == execution_sha256,
          'Execution record changed during audit')
    check(sha(Path(__file__).absolute()) == script_sha256, 'Auditor script changed during execution')
    record = {
        'schema': 'ges.automated-recovery-review.v1', 'reviewer': '/root/recovery_contract',
        'started_at': started_at, 'completed_at': datetime.now(timezone.utc).isoformat(),
        'elapsed_seconds': round(time.monotonic() - clock, 6), 'status': 'PASS',
        'explicit_mechanical_checks': CHECKS, 'input_files': len(before),
        'execution_sha256': execution_sha256,
        'recovery_report_sha256': execution['recovery_report_sha256'],
        'input_closure_sha256': execution['input_closure_sha256'],
        'script_sha256': script_sha256,
        'source_files_identical_to_retained_replay': 23, 'a3_exact_corpus_members': exact_members,
        'artifacts_metadata_provenance': 'Preserved October 7 workflow metadata; not original A3 artifact bytes.',
        'original_full_a3_capsule_restored': False, 'claim_subjects_reconstructed': len(subjects),
        'claim_documents': len(claim_documents), 'issued_receipts_unchanged': len(receipts),
        'validated_claims': 2174, 'unresolved_claims': 59767, 'candidate_blocks': 150903,
        'structured_occurrences': 605, 'published_page_applications': 18019,
        'unresolved_page_source_mappings': 14, 'artifact_disposition_receipts': 3590,
        'gates_open': 9, 'milestone_states': milestone_states, 'ges_v0_2': 'INCOMPLETE',
        'new_receipts_issued': 0, 'human_review': False, 'owner_acceptance': False,
        'new_source_omission_audit': False, 'source_text_redecompressed_in_this_audit': False,
        'boundaries': [
            'Automated evidence audit: hashes, exact membership, reconstructed metadata subjects, counts and truthful open gates.',
            'All source snapshot bytes match the separately independently content-validated retained cloud replay inputs.',
            'Source-to-claim omission completeness, semantic adjudication, rights, policy adoption, pilot and human acceptance are not supplied by this audit.',
            'The execution records a base revision plus the actual modified-code hashes; it is branch evidence, not merged-main acceptance.',
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('x', encoding='utf-8') as stream:
        stream.write(json.dumps(record, indent=2) + '\n')
    print(json.dumps({'status': 'PASS', 'mechanical_checks': CHECKS,
                      'claim_subjects': len(subjects), 'input_files': len(before),
                      'elapsed_seconds': record['elapsed_seconds']}))


if __name__ == '__main__':
    main()
