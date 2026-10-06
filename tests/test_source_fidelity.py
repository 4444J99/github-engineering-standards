import copy
import gzip
import hashlib
import io
import json
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from ges.core import digest
from ges.source_fidelity import main, source_fidelity_accounting

DEFAULT = object()


class SourceFidelity(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.evidence = self.root / 'evidence'
        self.reviews = self.evidence / 'source-reviews'
        self.sources = self.root / 'sources'
        self.evidence.mkdir()
        self.reviews.mkdir()
        self.sources.mkdir()

        self.commit = 'a' * 40
        self.content = '# Test\nMust test.\n'
        self.artifact = {
            'artifact_id': 'artifact-1',
            'source': 'example/source',
            'commit': self.commit,
            'path': 'README.md',
            'sha256': hashlib.sha256(self.content.encode()).hexdigest(),
        }
        self.candidate = {
            'candidate_id': 'candidate-1',
            'artifact_id': self.artifact['artifact_id'],
            'text_sha256': hashlib.sha256(b'Must test.').hexdigest(),
        }
        self.control = {
            'id': 'GES-TEST-001',
            'revision': 1,
            'sources': [{
                'repository': self.artifact['source'],
                'commit': self.commit,
                'path': self.artifact['path'],
            }],
        }
        self.artifacts = self.root / 'artifacts.jsonl'
        self.candidates = self.root / 'candidates.jsonl'
        self.artifacts.write_text(json.dumps(self.artifact) + '\n')
        self.candidates.write_text(json.dumps(self.candidate) + '\n')
        self.controls = [self.control]
        self.proposals = []
        self.pins = {'example/source': self.commit}
        self.review_policy = {
            'schema_version': 'ges.source_review_policy.v1',
            'authorized_reviewers': ['source-reviewer'],
            'control_adoption_authority': False,
            'manual_target_attestation_authority': False,
            'independent_omission_audit_complete': False,
        }
        self.source_review = {
            'artifact_id': self.artifact['artifact_id'],
            'commit': self.commit,
            'content_sha256': self.artifact['sha256'],
            'reviewer': 'source-reviewer',
            'reviewed_at': '2026-01-01T00:00:00Z',
            'disposition': 'CONTROL_SOURCE',
            'rationale': 'Synthetic full-file disposition.',
            'all_claims_accounted_for': True,
            'claim_mappings': [{
                'candidate_id': self.candidate['candidate_id'],
                'text_sha256': self.candidate['text_sha256'],
                'disposition': 'CONTROL',
                'control_id': self.control['id'],
                'control_revision': self.control['revision'],
            }],
        }
        self.write_source_review()
        with gzip.open(self.sources / 'example__source.text.jsonl.gz', 'wt') as stream:
            stream.write(json.dumps({
                'source': self.artifact['source'],
                'commit': self.commit,
                'path': self.artifact['path'],
                'content': self.content,
            }) + '\n')
        span = 'Must test.'
        self.claim_document = {
            'schema_version': 'ges.reference_claims.v1',
            'reviewer': 'source-reviewer',
            'reviewed_at': '2026-01-02T00:00:00Z',
            'source': self.artifact['source'],
            'commit': self.commit,
            'path': self.artifact['path'],
            'claims': [{
                'claim_id': 'claim-1',
                'artifact_id': self.artifact['artifact_id'],
                'statement': 'The source contains a synthetic requirement.',
                'start_line': 2,
                'end_line': 2,
                'content_sha256': self.artifact['sha256'],
                'span_sha256': hashlib.sha256(span.encode()).hexdigest(),
                'proposed_control_ids': [self.control['id']],
                'accepted_policy': False,
                'adopted_obligation': None,
            }],
        }
        self.write_claim_document()
        baseline = self.account(receipts=None, policy=None)
        self.build_certification(baseline['subject'])

    def write_source_review(self):
        (self.reviews / 'artifact.json').write_text(json.dumps([self.source_review]))

    def test_snapshot_replacement_after_provenance_rejected(self):
        from ges.claim_review import validate_provenance

        def replace_snapshot(*args, **kwargs):
            result = validate_provenance(*args, **kwargs)
            with gzip.open(self.sources / 'example__source.text.jsonl.gz', 'wt') as stream:
                stream.write(json.dumps({
                    'source': 'example/source', 'commit': self.commit,
                    'path': 'README.md', 'content': 'Unrelated replacement.',
                }) + '\n')
            return result

        with patch('ges.source_fidelity.validate_provenance', replace_snapshot):
            with self.assertRaisesRegex(ValueError, 'input changed'):
                self.account()

    def test_claim_document_added_after_provenance_rejected(self):
        from ges.claim_review import validate_provenance

        def add_claim(*args, **kwargs):
            result = validate_provenance(*args, **kwargs)
            document = copy.deepcopy(self.claim_document)
            document['claims'][0]['claim_id'] = 'claim-2'
            (self.reviews / 'new-claims.json').write_text(json.dumps(document))
            return result

        with patch('ges.source_fidelity.validate_provenance', add_claim):
            with self.assertRaisesRegex(ValueError, 'input changed'):
                self.account()

    def test_boolean_count_cannot_inherit_integer_subject(self):
        self.receipt['subject']['reference_claim_count'] = True
        with self.assertRaisesRegex(ValueError, 'subject or count changed'):
            self.account()

    def write_claim_document(self):
        (self.reviews / 'artifact-claims.json').write_text(json.dumps(self.claim_document))

    def account(self, receipts=DEFAULT, policy=DEFAULT):
        return source_fidelity_accounting(
            self.artifacts, self.candidates, self.reviews, self.review_policy,
            self.sources, self.controls, self.pins,
            [self.receipt] if receipts is DEFAULT else receipts,
            self.certification_policy if policy is DEFAULT else policy,
            proposals=self.proposals,
            evidence_root=self.root)

    def build_certification(self, subject):
        self.certification_policy = {
            'schema': 'ges.source-fidelity-authority-policy.v1',
            'approval_reference': 'synthetic fixture; not real authority',
            'subject': copy.deepcopy(subject),
            'authorized_fidelity_auditors': ['fidelity-auditor'],
            'authorized_independent_omission_auditors': ['omission-auditor'],
        }
        self.receipt = {
            'schema': 'ges.source-fidelity-certification-receipt.v1',
            'subject': copy.deepcopy(subject),
            'fidelity_auditor': 'fidelity-auditor',
            'independent_omission_auditor': 'omission-auditor',
            'certified_at': '2026-01-04T00:00:00Z',
            'evidence': {},
        }
        for kind, identity in (
                ('atomic_claim_fidelity_audit', 'fidelity-auditor'),
                ('independent_source_to_claim_omission_audit', 'omission-auditor')):
            document = {
                'schema': 'ges.source-fidelity-evidence.v1',
                'kind': kind,
                'identity': identity,
                'subject': copy.deepcopy(subject),
                'reviewed_at': '2026-01-03T00:00:00Z',
                'outcome': 'PASS',
                'unresolved': [],
                'method': 'Synthetic bounded audit method.',
                'observations': ['Synthetic fixture observation.'],
            }
            path = self.evidence / (kind + '.json')
            path.write_text(json.dumps(document))
            self.receipt['evidence'][kind] = {
                'path': 'evidence/' + path.name,
                'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            }

    def mutate_evidence(self, kind, changes):
        reference = self.receipt['evidence'][kind]
        path = self.root / reference['path']
        document = json.loads(path.read_text())
        document.update(changes)
        path.write_text(json.dumps(document))
        reference['sha256'] = hashlib.sha256(path.read_bytes()).hexdigest()

    def assert_evidence_change_rejected(self, kind, changes):
        original_reference = copy.deepcopy(self.receipt['evidence'][kind])
        path = self.root / original_reference['path']
        original_bytes = path.read_bytes()
        try:
            self.mutate_evidence(kind, changes)
            with self.assertRaises(ValueError):
                self.account()
        finally:
            path.write_bytes(original_bytes)
            self.receipt['evidence'][kind] = original_reference

    def test_complete_certificate_validates_only_gate_prerequisites(self):
        result = self.account()
        self.assertEqual(result['reviewed'], 1)
        self.assertEqual(result['inventoried'], 1)
        self.assertTrue(result['coverage_complete'])
        self.assertTrue(result['atomic_claim_fidelity_audit'])
        self.assertTrue(result['independent_source_to_claim_omission_audit'])
        self.assertFalse(result['semantic_truth_automatically_certified'])
        self.assertFalse(result['rights_cleared'])
        self.assertFalse(result['policy_adopted'])

    def test_missing_certification_receipts_leave_audits_unknown(self):
        result = self.account(receipts=None, policy=None)
        self.assertTrue(result['coverage_complete'])
        self.assertIsNone(result['atomic_claim_fidelity_audit'])
        self.assertIsNone(result['independent_source_to_claim_omission_audit'])
        self.assertEqual(result['evaluation'], 'UNVERIFIED')

    def test_empty_receipts_still_require_a_valid_supplied_policy(self):
        with self.assertRaisesRegex(ValueError, 'authority policy'):
            self.account(receipts=[], policy={})

    def test_partial_review_is_incomplete_and_cannot_be_certified(self):
        other = dict(self.artifact, artifact_id='artifact-2', path='OTHER.md')
        self.artifacts.write_text(json.dumps(self.artifact) + '\n' + json.dumps(other) + '\n')
        partial = self.account(receipts=None, policy=None)
        self.assertEqual(partial['reviewed'], 1)
        self.assertEqual(partial['inventoried'], 2)
        self.assertFalse(partial['coverage_complete'])
        self.assertEqual(partial['evaluation'], 'INCOMPLETE')
        self.build_certification(partial['subject'])
        with self.assertRaisesRegex(ValueError, 'incomplete or zero'):
            self.account()

    def test_zero_denominator_never_closes(self):
        artifacts = self.root / 'empty-artifacts.jsonl'
        candidates = self.root / 'empty-candidates.jsonl'
        reviews = self.root / 'empty-reviews'
        artifacts.write_text('')
        candidates.write_text('')
        reviews.mkdir()
        result = source_fidelity_accounting(
            artifacts, candidates, reviews, {'authorized_reviewers': ['reviewer']},
            self.sources, [], {}, None, None, evidence_root=self.root)
        self.assertIsNone(result['coverage_complete'])
        self.assertIsNone(result['atomic_claim_fidelity_audit'])
        self.assertIsNone(result['independent_source_to_claim_omission_audit'])

    def test_forged_subject_count_rejected(self):
        receipt = copy.deepcopy(self.receipt)
        receipt['subject']['reviewed_count'] = 2
        with self.assertRaises(ValueError):
            self.account(receipts=[receipt])

    def test_changed_inventory_candidate_review_or_claim_digest_rejected(self):
        paths = [self.artifacts, self.candidates, self.reviews / 'artifact.json',
                 self.reviews / 'artifact-claims.json']
        original_bytes = {path: path.read_bytes() for path in paths}
        original_review = copy.deepcopy(self.source_review)
        original_claims = copy.deepcopy(self.claim_document)
        mutations = ('inventory', 'candidate', 'review', 'claim')
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                try:
                    if mutation == 'inventory':
                        row = dict(self.artifact, note='changed')
                        self.artifacts.write_text(json.dumps(row) + '\n')
                    elif mutation == 'candidate':
                        row = dict(self.candidate, note='changed')
                        self.candidates.write_text(json.dumps(row) + '\n')
                    elif mutation == 'review':
                        self.source_review['rationale'] = (
                            'Changed but structurally valid rationale.')
                        self.write_source_review()
                    else:
                        self.claim_document['claims'][0]['statement'] = (
                            'Changed reference statement.')
                        self.write_claim_document()
                    with self.assertRaises(ValueError):
                        self.account()
                finally:
                    for path, content in original_bytes.items():
                        path.write_bytes(content)
                    self.source_review = copy.deepcopy(original_review)
                    self.claim_document = copy.deepcopy(original_claims)

    def test_raw_inventory_bytes_are_bound_when_parsed_rows_match(self):
        original = self.artifacts.read_bytes()
        try:
            self.artifacts.write_text('  ' + original.decode())
            with self.assertRaisesRegex(ValueError, 'input digests'):
                self.account()
        finally:
            self.artifacts.write_bytes(original)

    def test_same_auditor_rejected(self):
        self.certification_policy['authorized_independent_omission_auditors'] = [
            'fidelity-auditor']
        self.receipt['independent_omission_auditor'] = 'fidelity-auditor'
        self.mutate_evidence('independent_source_to_claim_omission_audit',
                             {'identity': 'fidelity-auditor'})
        with self.assertRaisesRegex(ValueError, 'must be distinct'):
            self.account()

    def test_unauthorized_auditor_rejected(self):
        self.receipt['fidelity_auditor'] = 'intruder'
        with self.assertRaisesRegex(ValueError, 'Unauthorized'):
            self.account()

    def test_source_review_policy_cannot_grant_certification_authority(self):
        with self.assertRaisesRegex(ValueError, 'authority policy'):
            self.account(policy=self.review_policy)

    def test_unknown_or_contradictory_certification_fields_are_rejected(self):
        policy = copy.deepcopy(self.certification_policy)
        policy['revoked'] = True
        with self.assertRaisesRegex(ValueError, 'authority policy'):
            self.account(policy=policy)

        receipt = copy.deepcopy(self.receipt)
        receipt['failed_checks'] = ['semantic review was not performed']
        with self.assertRaisesRegex(ValueError, 'Malformed'):
            self.account(receipts=[receipt])

        self.assert_evidence_change_rejected(
            'atomic_claim_fidelity_audit',
            {'failed_checks': ['semantic review was not performed']})

    def test_proposal_identity_is_valid_for_claim_provenance(self):
        proposal = {'id': 'GES-PROP-001', 'revision': 1}
        self.proposals = [proposal]
        self.claim_document['claims'][0]['proposed_control_ids'] = [proposal['id']]
        self.write_claim_document()
        result = self.account(receipts=None, policy=None)
        self.assertTrue(result['claim_provenance_validated'])
        self.assertEqual(result['subject']['proposal_digest'], digest([proposal]))

    def test_string_booleans_and_unresolved_findings_rejected(self):
        for changes in ({'outcome': True}, {'unresolved': '[]'},
                        {'unresolved': ['unreviewed source span']}):
            with self.subTest(changes=changes):
                self.assert_evidence_change_rejected(
                    'atomic_claim_fidelity_audit', changes)

    def test_missing_evidence_kind_or_file_rejected(self):
        kind = 'atomic_claim_fidelity_audit'
        reference = self.receipt['evidence'].pop(kind)
        with self.assertRaisesRegex(ValueError, 'Missing or unsupported'):
            self.account()
        self.receipt['evidence'][kind] = reference
        self.receipt['evidence'][kind]['path'] = 'evidence/missing.json'
        with self.assertRaises(ValueError):
            self.account()

    def test_evidence_path_traversal_symlink_and_oversize_rejected(self):
        kind = 'atomic_claim_fidelity_audit'
        original_reference = copy.deepcopy(self.receipt['evidence'][kind])
        self.receipt['evidence'][kind]['path'] = '../escape.json'
        with self.assertRaises(ValueError):
            self.account()

        self.receipt['evidence'][kind] = copy.deepcopy(original_reference)
        target = self.root / self.receipt['evidence'][kind]['path']
        alias = self.evidence / 'alias.json'
        alias.symlink_to(target)
        self.receipt['evidence'][kind] = {
            'path': 'evidence/alias.json',
            'sha256': hashlib.sha256(target.read_bytes()).hexdigest(),
        }
        with self.assertRaises(ValueError):
            self.account()

        self.receipt['evidence'][kind] = copy.deepcopy(original_reference)
        oversized = self.evidence / 'oversized.json'
        oversized.write_bytes(b' ' * 1_000_001)
        self.receipt['evidence'][kind] = {
            'path': 'evidence/oversized.json',
            'sha256': hashlib.sha256(oversized.read_bytes()).hexdigest(),
        }
        with self.assertRaisesRegex(ValueError, 'size bound'):
            self.account()

    def test_future_evidence_or_certificate_timestamp_rejected(self):
        self.assert_evidence_change_rejected(
            'atomic_claim_fidelity_audit',
            {'reviewed_at': '2999-01-01T00:00:00Z'})
        self.receipt['certified_at'] = '2999-01-01T00:00:00Z'
        with self.assertRaisesRegex(ValueError, 'future'):
            self.account()

    def test_cli_invalid_input_exits_two(self):
        pins = self.root / 'pins.json'
        catalog = self.root / 'catalog.json'
        review_policy = self.root / 'review-policy.json'
        pins.write_text(json.dumps({'sources': [
            {'repository': 'example/source', 'commit': self.commit}]}))
        catalog.write_text(json.dumps(self.controls))
        review_policy.write_text(json.dumps(self.review_policy))
        self.candidates.write_text('{not json}\n')
        arguments = [
            'ges.source_fidelity', '--artifacts', str(self.artifacts),
            '--candidates', str(self.candidates), '--reviews', str(self.reviews),
            '--review-policy', str(review_policy), '--sources', str(self.sources),
            '--catalog', str(catalog), '--pins', str(pins),
            '--evidence-root', str(self.root),
        ]
        with patch.object(sys, 'argv', arguments), redirect_stdout(io.StringIO()):
            self.assertEqual(main(), 2)


if __name__ == '__main__':
    unittest.main()
