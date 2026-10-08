"""Synthetic approval fixtures exercise validation; they are not real clearance."""
import copy
import gzip
import hashlib
import json
import os
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from ges.core import digest
from ges.publication_use import (EXPRESSION_KINDS, SCOPE_FIELDS, main, output_inventory,
                                 prepare_draft, publication_accounting, validate_accounting_result)


def byte_range(raw, start=0, end=None):
    end = len(raw) if end is None else end
    return {'start_byte': start, 'end_byte': end,
            'sha256': hashlib.sha256(raw[start:end]).hexdigest()}


def bind_approvals(fixture):
    """Write explicitly synthetic exact-scope attestations for this test input."""
    manifest, register = fixture['manifest'], fixture['register']
    register['manifest_digest'] = digest(manifest)
    subject = {key: manifest[key] for key in ('candidate_id', 'candidate_revision',
                                              'distribution_scope', 'release_scope')}
    subject.update(manifest_digest=digest(manifest), register_digest=digest(register),
                   output_inventory_digest=digest(output_inventory(fixture['output_root'])),
                   inventory_digest=digest(fixture['artifacts']), pins_digest=digest(fixture['pins']),
                   source_evidence_digest=digest(register['source_evidence']))
    fixture['policy'] = {'schema': 'ges.publication-use-authority-policy.v1',
                         'approval_reference': 'SYNTHETIC TEST ONLY; externally trusted in this fixture',
                         'subject': subject, 'issued_at': '2026-01-04T00:00:00Z',
                         'valid_until': '2098-01-01T00:00:00Z',
                         'authorized_inventory_reviewers': ['synthetic:inventory-reviewer'],
                         'authorized_use_reviewers': ['synthetic:use-reviewer'],
                         'authorized_independent_auditors': ['synthetic:auditor'],
                         'authorized_human_acceptors': ['synthetic:human'],
                         'authorized_distribution_approvers': ['synthetic:publisher']}
    inventory = {'schema': 'ges.publication-use-receipt.v1', 'kind': 'OUTPUT_INVENTORY',
                 'subject': subject, 'disposition': 'REGISTER_COMPLETE' if register['uses'] else 'NO_UPSTREAM_EXPRESSION',
                 'valid_until': '2097-01-01T00:00:00Z', 'obligations': ['Synthetic exact-scope duty'],
                 'reviewer': 'synthetic:inventory-reviewer', 'independent_auditor': 'synthetic:auditor',
                 'human_acceptor': 'synthetic:human', 'distribution_approver': 'synthetic:publisher',
                 'evidence': {}}
    receipts = [inventory]
    receipts.extend({**copy.deepcopy(inventory), 'kind': 'EXPRESSION_USE',
                     'use_id': use['use_id'], 'reviewer': 'synthetic:use-reviewer',
                     'attribution_disposition': 'REQUIRED_PROVIDED',
                     'attribution_rationale': 'Synthetic notice appears in exact output bytes.'}
                    for use in register['uses'] if use['kind'] in EXPRESSION_KINDS)
    for number, receipt in enumerate(receipts):
        is_inventory = receipt['kind'] == 'OUTPUT_INVENTORY'
        bound = {'scope': subject, 'obligations': receipt['obligations'], 'valid_until': receipt['valid_until']}
        if is_inventory:
            bound['disposition'] = receipt['disposition']
            kinds = [('inventory_review', 'reviewer'), ('independent_omission_audit', 'independent_auditor')]
            assurances = {'all_candidate_outputs_accounted_for': True,
                          'all_upstream_uses_accounted_for': True,
                          'source_use_classifications_reviewed': True,
                          'no_upstream_expression_confirmed': not bool(register['uses'])}
        else:
            receipt.pop('disposition')
            use = next(row for row in register['uses'] if row['use_id'] == receipt['use_id'])
            bound.update(use=use, attribution_disposition=receipt['attribution_disposition'],
                         attribution_rationale=receipt['attribution_rationale'])
            kinds = [('expression_rights_review', 'reviewer'), ('independent_exception_audit', 'independent_auditor')]
            assurances = {'exact_expression_and_grant_reviewed': True,
                          'restrictions_accounted_for': True, 'attribution_accounted_for': True}
        kinds += [('human_acceptance', 'human_acceptor'), ('distribution_approval', 'distribution_approver')]
        for step, (kind, field) in enumerate(kinds, 5):
            doc = {'schema': 'ges.publication-use-attestation.v1', 'kind': kind,
                   'identity': receipt[field], 'subject': copy.deepcopy(bound),
                   'reviewed_at': f'2026-01-{step:02}T00:00:00Z',
                   'decision': 'APPROVED_FOR_SPECIFIED_USE', 'assurances': assurances,
                   'unresolved': [], 'rationale': 'SYNTHETIC TEST ONLY; no actual judgment or rights grant.'}
            path = fixture['evidence_root'] / 'evidence' / f'{number}-{kind}.json'
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(doc), encoding='utf-8')
            receipt['evidence'][kind] = {'path': path.relative_to(fixture['evidence_root']).as_posix(),
                                         'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
    fixture['receipts'] = receipts
    return fixture


def create_fixture(root: Path, *, kind='LICENSED_COPY', zero_use=False, release_scope='GES_V0_2'):
    """Return kwargs for a complete synthetic candidate, including trusted inputs."""
    output_root = root / 'candidate'
    source_root = root / 'sources'
    output_root.mkdir(parents=True, exist_ok=True)
    source_root.mkdir(parents=True, exist_ok=True)
    source = b'Example source expression.\nAnother clause.\n'
    output = b'Example source expression.\nCredit: synthetic source.\n'
    if zero_use:
        output = b'Original synthetic fixture output.\n'
    if kind == 'REFERENCES_ONLY':
        output = b'https://github.com/test/source/blob/' + b'a' * 40 + b'/README.md\n'
    (source_root / 'source.txt').write_bytes(source)
    (output_root / 'release.txt').write_bytes(output)
    artifact = {'artifact_id': 'source:one', 'source': 'test/source', 'commit': 'a' * 40,
                'path': 'README.md', 'sha256': hashlib.sha256(source).hexdigest(),
                'retrieved_at': '2026-01-01T00:00:00Z', 'url': 'https://example.invalid/source'}
    draft = prepare_draft(output_root, 'synthetic-v0.2-candidate', 'b' * 40,
                          'Synthetic public distribution fixture; no publication authorized',
                          release_scope=release_scope, prepared_at='2026-01-02T00:00:00Z')
    register = draft['register']
    register['prepared_at'] = '2026-01-03T00:00:00Z'
    if zero_use:
        register['outputs'][0]['disposition'] = 'NO_UPSTREAM_EXPRESSION'
    else:
        use = {'use_id': 'use:one', 'kind': kind,
               'source': {key: artifact[key] for key in ('artifact_id', 'source', 'commit', 'path', 'sha256')},
               'source_range': None if kind == 'REFERENCES_ONLY' else byte_range(source, 0, 26),
               'output_path': 'release.txt', 'output_range': byte_range(output, 0, 26) if kind != 'REFERENCES_ONLY' else byte_range(output),
               'attributions': [{'output_path': 'release.txt', 'output_range': byte_range(output, 26)}]
                               if kind in EXPRESSION_KINDS else [],
               'rationale': 'Synthetic exact expression/use fixture only.'}
        register['uses'] = [use]
        register['outputs'][0].update(disposition='USES_RECORDED', use_ids=['use:one'])
        register['source_evidence'] = [{'artifact_id': artifact['artifact_id'], 'format': 'RAW',
                                       'path': 'source.txt', 'sha256': hashlib.sha256(source).hexdigest()}]
    fixture = {**draft, 'artifacts': [artifact], 'pins': {'test/source': 'a' * 40},
               'output_root': output_root, 'source_root': source_root, 'evidence_root': root}
    return bind_approvals(fixture)


class PublicationUse(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.fixture = create_fixture(Path(self.temp.name))

    def account(self, **changes):
        return publication_accounting(**{**self.fixture, **changes})

    def document(self, receipt_index=0, kind='inventory_review'):
        ref = self.fixture['receipts'][receipt_index]['evidence'][kind]
        return json.loads((self.fixture['evidence_root'] / ref['path']).read_text())

    def write_document(self, doc, receipt_index=0, kind='inventory_review'):
        ref = self.fixture['receipts'][receipt_index]['evidence'][kind]
        path = self.fixture['evidence_root'] / ref['path']
        path.write_text(json.dumps(doc))
        ref['sha256'] = hashlib.sha256(path.read_bytes()).hexdigest()

    def test_synthetic_exact_use_requires_every_attestation_without_claiming_legal_truth(self):
        result = self.account()
        self.assertEqual((result['completed'], result['denominator']), (1, 1))
        self.assertTrue(result['exact_use_clearance'])
        self.assertTrue(result['authorized_distribution_decision'])
        self.assertFalse(result['zero_use_clearance'])
        for flag in ['legal_truth_automatically_certified', 'authority_authenticity_automatically_certified',
                     'publication_performed', 'legacy_rights_reinterpreted']:
            self.assertFalse(result[flag])

    def test_missing_manifest_register_or_approvals_remains_unknown(self):
        for changed in [{'manifest': None, 'register': None}, {'manifest': None}, {'register': None}, {}]:
            result = self.account(receipts=[], policy={}, **changed)
            self.assertIsNone(result['exact_use_clearance'])
            self.assertFalse(result['zero_use_clearance'])

    def test_draft_inventory_is_truthfully_unreviewed_and_never_cleared(self):
        draft = prepare_draft(self.fixture['output_root'], 'candidate', 'b' * 40, 'Bounded patch',
                              prepared_at='2026-01-02T00:00:00Z')
        result = self.account(**draft)
        self.assertEqual(result['unreviewed_output_count'], 1)
        self.assertEqual(result['release_scope'], 'BOUNDED_PACKAGE')
        self.assertTrue(result['complete_output_inventory'])
        self.assertIsNone(result['use_register_complete'])
        self.assertIsNone(result['exact_use_clearance'])
        self.fixture.update(draft)
        bind_approvals(self.fixture)
        with self.assertRaisesRegex(ValueError, 'Unreviewed output'):
            self.account()

    def test_explicit_zero_use_needs_reviewed_nonempty_inventory_and_distribution(self):
        self.fixture = create_fixture(Path(self.temp.name), zero_use=True)
        result = self.account()
        self.assertEqual((result['denominator'], result['completed'], result['output_count']), (0, 0, 1))
        self.assertTrue(result['zero_use_clearance'])
        self.assertTrue(result['exact_use_clearance'])
        self.assertNotIn('percent', result)
        result = self.account(receipts=[], policy={})
        self.assertIsNone(result['exact_use_clearance'])
        self.assertFalse(result['zero_use_clearance'])

    def test_references_and_paraphrases_need_no_blanket_per_artifact_grants(self):
        for kind in ['REFERENCES_ONLY', 'INDEPENDENT_PARAPHRASE']:
            with self.subTest(kind=kind):
                self.fixture = create_fixture(Path(self.temp.name), kind=kind)
                unused = {**self.fixture['artifacts'][0], 'artifact_id': 'unreferenced:two', 'path': 'unused.md'}
                self.fixture['artifacts'].append(unused)
                bind_approvals(self.fixture)
                self.assertEqual(len(self.fixture['receipts']), 1)
                result = self.account()
                self.assertTrue(result['exact_use_clearance'])
                self.assertEqual((result['denominator'], result['copied_or_adapted_count']), (1, 0))

    def test_copy_or_adaptation_missing_use_approval_is_incomplete(self):
        for kind in ['LICENSED_COPY', 'ADAPTATION']:
            self.fixture = create_fixture(Path(self.temp.name), kind=kind)
            result = self.account(receipts=self.fixture['receipts'][:1])
            self.assertFalse(result['exact_use_clearance'])
            self.assertFalse(result['authorized_distribution_decision'])
            self.assertEqual((result['completed'], result['denominator']), (0, 1))

    def test_use_receipt_alone_never_certifies_the_complete_inventory(self):
        result = self.account(receipts=self.fixture['receipts'][1:])
        self.assertEqual((result['completed'], result['denominator']), (1, 1))
        self.assertIsNone(result['use_register_complete'])
        self.assertFalse(result['exact_use_clearance'])

    def test_missing_extra_changed_and_duplicate_output_files_rejected(self):
        root = self.fixture['output_root']
        original = (root / 'release.txt').read_bytes()
        for action in ['missing', 'extra', 'changed', 'duplicate']:
            with self.subTest(action=action):
                if action == 'missing':
                    (root / 'release.txt').unlink()
                elif action == 'extra':
                    (root / 'extra.txt').write_text('Unlisted output')
                elif action == 'changed':
                    (root / 'release.txt').write_text('Changed')
                else:
                    self.fixture['manifest']['outputs'] *= 2
                with self.assertRaises(ValueError):
                    self.account()
                (root / 'release.txt').write_bytes(original)
                (root / 'extra.txt').unlink(missing_ok=True)

    def test_escape_noncanonical_and_symlink_output_paths_rejected(self):
        for value in ['../outside', '/absolute', './release.txt', 'a//b', 'x\\y', '.']:
            with self.subTest(value=value):
                manifest = copy.deepcopy(self.fixture['manifest'])
                manifest['outputs'][0]['path'] = value
                with self.assertRaises(ValueError):
                    self.account(manifest=manifest)
        target = self.fixture['output_root'] / 'release.txt'
        target.unlink()
        target.symlink_to(self.fixture['source_root'] / 'source.txt')
        with self.assertRaises(ValueError):
            self.account()

    def test_symlink_output_directory_rejected(self):
        (self.fixture['output_root'] / 'linked').symlink_to(self.fixture['source_root'], target_is_directory=True)
        with self.assertRaises(ValueError):
            self.account()

    def test_inaccessible_subtree_never_disappears_from_initial_or_final_inventory(self):
        from ges.publication_use import _evidence
        real_scandir = os.scandir
        for stage in ['initial', 'final']:
            with self.subTest(stage=stage):
                self.fixture = create_fixture(Path(self.temp.name) / stage)
                restricted = self.fixture['output_root'] / 'inaccessible'
                def add_unreviewed_file():
                    restricted.mkdir(exist_ok=True)
                    (restricted / 'unreviewed.txt').write_text('Undeclared upstream expression')
                if stage == 'initial':
                    add_unreviewed_file()
                def inaccessible(path):
                    if Path(path) == restricted:
                        raise PermissionError('Synthetic inaccessible candidate subtree')
                    return real_scandir(path)
                def add_during_review(root, reference):
                    doc = _evidence(root, reference)
                    if stage == 'final':
                        add_unreviewed_file()
                    return doc
                with patch('ges.publication_use.os.scandir', side_effect=inaccessible), \
                     patch('ges.publication_use._evidence', side_effect=add_during_review):
                    with self.assertRaisesRegex(ValueError, 'Cannot completely enumerate candidate outputs'):
                        self.account()

    def test_changed_source_bytes_or_source_pin_rejected(self):
        (self.fixture['source_root'] / 'source.txt').write_text('changed')
        with self.assertRaises(ValueError):
            self.account()
        with self.assertRaises(ValueError):
            self.account(pins={'test/source': 'c' * 40})

    def test_escaping_and_symlink_source_evidence_rejected(self):
        self.fixture['register']['source_evidence'][0]['path'] = '../outside'
        with self.assertRaises(ValueError):
            self.account()
        self.fixture['register']['source_evidence'][0]['path'] = 'source.txt'
        target = self.fixture['source_root'] / 'source.txt'
        original = target.read_bytes()
        target.unlink()
        (self.fixture['evidence_root'] / 'outside').write_bytes(original)
        target.symlink_to(self.fixture['evidence_root'] / 'outside')
        with self.assertRaises(ValueError):
            self.account()

    def test_source_snapshot_text_uses_existing_pinned_cache_format(self):
        artifact = self.fixture['artifacts'][0]
        path = self.fixture['source_root'] / 'test__source.text.jsonl.gz'
        row = {**artifact, 'content': (self.fixture['source_root'] / 'source.txt').read_text()}
        with gzip.open(path, 'wt') as stream:
            stream.write(json.dumps(row) + '\n')
        self.fixture['register']['source_evidence'] = [{'artifact_id': artifact['artifact_id'],
                                                        'format': 'SNAPSHOT_TEXT', 'path': path.name,
                                                        'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}]
        bind_approvals(self.fixture)
        self.assertTrue(self.account()['exact_use_clearance'])
        with gzip.open(path, 'wt') as stream:
            stream.write(json.dumps({**row, 'content': 'changed source'}) + '\n')
        self.fixture['register']['source_evidence'][0]['sha256'] = hashlib.sha256(path.read_bytes()).hexdigest()
        bind_approvals(self.fixture)
        with self.assertRaisesRegex(ValueError, 'Pinned source bytes changed'):
            self.account()

    def test_duplicate_use_ids_and_contradictory_classification_rejected(self):
        original = copy.deepcopy(self.fixture['register']['uses'][0])
        for changed in [original, {**original, 'use_id': 'other', 'kind': 'REFERENCES_ONLY', 'source_range': None}]:
            self.fixture['register']['uses'] = [original, changed]
            with self.assertRaises(ValueError):
                self.account()

    def test_overlapping_spans_cannot_hide_copy_inside_reference_classification(self):
        original = self.fixture['register']['uses'][0]
        output = (self.fixture['output_root'] / 'release.txt').read_bytes()
        changed = {**copy.deepcopy(original), 'use_id': 'overlapping-reference',
                   'kind': 'REFERENCES_ONLY', 'source_range': None,
                   'output_range': byte_range(output, 0, 10)}
        self.fixture['register']['uses'].append(changed)
        with self.assertRaisesRegex(ValueError, 'overlapping output expressions'):
            self.account()

    def test_licensed_copy_must_match_actual_source_and_output_span(self):
        source = (self.fixture['source_root'] / 'source.txt').read_bytes()
        self.fixture['register']['uses'][0]['source_range'] = byte_range(source, 1, 26)
        bind_approvals(self.fixture)
        with self.assertRaisesRegex(ValueError, 'LICENSED_COPY spans are not identical'):
            self.account()

    def test_dropped_use_or_output_disposition_does_not_shrink_approved_scope(self):
        for field in ['uses', 'outputs', 'source_evidence']:
            register = copy.deepcopy(self.fixture['register'])
            register[field] = []
            with self.assertRaises(ValueError):
                self.account(register=register)

    def test_rewritten_manifest_register_cannot_self_certify_completeness(self):
        self.fixture['register']['uses'] = []
        self.fixture['register']['source_evidence'] = []
        self.fixture['register']['outputs'][0].update(disposition='NO_UPSTREAM_EXPRESSION', use_ids=[])
        with self.assertRaisesRegex(ValueError, 'Approved publication scope'):
            self.account()

    def test_changed_spans_or_attribution_rejected(self):
        for key in ['source_range', 'output_range']:
            original = copy.deepcopy(self.fixture['register']['uses'][0][key])
            self.fixture['register']['uses'][0][key]['sha256'] = 'f' * 64
            with self.assertRaises(ValueError):
                self.account()
            self.fixture['register']['uses'][0][key] = original
        self.fixture['register']['uses'][0]['attributions'][0]['output_path'] = 'missing'
        with self.assertRaises(ValueError):
            self.account()

    def test_required_attribution_cannot_be_missing(self):
        self.fixture['register']['uses'][0]['attributions'] = []
        bind_approvals(self.fixture)
        with self.assertRaisesRegex(ValueError, 'Required attribution'):
            self.account()

    def test_policy_scope_and_roles_cannot_be_invented_by_receipt(self):
        for key, value in [('approval_reference', ''), ('authorized_human_acceptors', ['agent']),
                           ('authorized_use_reviewers', 'not-an-array'),
                           ('authorized_inventory_reviewers', ['automated:semantic-review-v0.2.0'])]:
            with self.subTest(key=key):
                policy = {**self.fixture['policy'], key: value}
                with self.assertRaises(ValueError):
                    self.account(policy=policy)
        with self.assertRaises(ValueError):
            self.account(policy={})

    def test_self_audit_and_duplicate_receipts_rejected(self):
        with self.assertRaises(ValueError):
            self.account(receipts=self.fixture['receipts'] * 2)
        self.fixture['policy']['authorized_independent_auditors'].append('synthetic:inventory-reviewer')
        self.fixture['receipts'][0]['independent_auditor'] = 'synthetic:inventory-reviewer'
        with self.assertRaises(ValueError):
            self.account()

    def test_fake_approval_unknown_fields_missing_proof_and_unresolved_findings_rejected(self):
        original = self.document()
        cases = [dict(original, approved=True), dict(original, decision='PASS'),
                 dict(original, unresolved=['Unresolved component']), dict(original, rationale='')]
        for doc in cases:
            self.write_document(doc)
            with self.assertRaises(ValueError):
                self.account()
        self.write_document(original)
        self.fixture['receipts'][0]['evidence'].pop('human_acceptance')
        with self.assertRaises(ValueError):
            self.account()

    def test_attestation_truth_requires_literal_boolean(self):
        original = self.document()
        for value in [1, 'true', None]:
            doc = copy.deepcopy(original)
            doc['assurances']['all_upstream_uses_accounted_for'] = value
            self.write_document(doc)
            with self.assertRaises(ValueError):
                self.account()

    def test_expired_future_prepared_before_authority_and_naive_evidence_rejected(self):
        for stamp in ['2099-01-01T00:00:00Z', '2025-01-01T00:00:00Z', '2026-01-05T00:00:00']:
            doc = self.document()
            doc['reviewed_at'] = stamp
            self.write_document(doc)
            with self.assertRaises(ValueError):
                self.account()
        for field, stamp in [('issued_at', '2099-01-01T00:00:00Z'), ('valid_until', '2026-01-01T00:00:00Z')]:
            with self.assertRaises(ValueError):
                self.account(policy={**self.fixture['policy'], field: stamp})

    def test_wrong_evidence_subject_identity_decision_order_or_bytes_rejected(self):
        original = self.document()
        for doc in [dict(original, identity='unauthorized'), dict(original, subject={}),
                    dict(original, reviewed_at='2026-01-09T00:00:00Z')]:
            self.write_document(doc)
            with self.assertRaises(ValueError):
                self.account()
        self.write_document(original)
        path = self.fixture['evidence_root'] / self.fixture['receipts'][0]['evidence']['inventory_review']['path']
        path.write_text('{}')
        with self.assertRaises(ValueError):
            self.account()

    def test_escaping_or_symlink_attestation_rejected(self):
        reference = self.fixture['receipts'][0]['evidence']['inventory_review']
        original_path = reference['path']
        reference['path'] = '../outside.json'
        with self.assertRaises(ValueError):
            self.account()
        reference['path'] = original_path
        path = self.fixture['evidence_root'] / original_path
        path.unlink()
        path.symlink_to(self.fixture['source_root'] / 'source.txt')
        with self.assertRaises(ValueError):
            self.account()

    def test_changed_evidence_or_output_after_initial_read_rejected(self):
        from ges.publication_use import _evidence
        calls = []
        def replace(root, reference):
            doc = _evidence(root, reference)
            calls.append(reference)
            if len(calls) == 8:
                (root / calls[0]['path']).write_text('{}')
            return doc
        with patch('ges.publication_use._evidence', side_effect=replace):
            with self.assertRaises(ValueError):
                self.account()
        bind_approvals(self.fixture)
        calls.clear()
        def mutate_output(root, reference):
            doc = _evidence(root, reference)
            if not calls:
                (self.fixture['output_root'] / 'release.txt').write_text('changed mid-validation')
            calls.append(reference)
            return doc
        with patch('ges.publication_use._evidence', side_effect=mutate_output):
            with self.assertRaises(ValueError):
                self.account()

    def test_strict_accounting_rejects_boolean_sidecars_and_count_or_scope_tampering(self):
        with self.assertRaises(ValueError):
            validate_accounting_result({'schema': 'ges.publication-use-accounting.v1', 'exact_use_clearance': True})
        result = self.account()
        for changed in [dict(result, denominator=0), dict(result, completed=0),
                        dict(result, inventory_receipt_validated=False), dict(result, unreviewed_output_count=1),
                        dict(result, zero_use_clearance=True), dict(result, release_scope='BOUNDED_PACKAGE'),
                        dict(result, policy_digest=None), dict(result, legal_truth_automatically_certified=True)]:
            with self.assertRaises(ValueError):
                validate_accounting_result(changed)

    def test_draft_cli_emits_no_approval_and_refuses_overwrite(self):
        root = Path(self.temp.name) / 'draft'
        args = ['prepare-draft', '--output-root', str(self.fixture['output_root']),
                '--draft-directory', str(root), '--candidate-id', 'draft-test',
                '--candidate-revision', 'b' * 40, '--distribution-scope', 'Bounded test patch']
        with patch('builtins.print'):
            self.assertEqual(main(args), 0)
            self.assertEqual(main(args), 2)
        self.assertEqual(json.loads((root / 'policy.json').read_text()), {})
        self.assertEqual(json.loads((root / 'receipts.json').read_text()), [])
        self.assertEqual(json.loads((root / 'register.json').read_text())['outputs'][0]['disposition'], 'UNREVIEWED')


if __name__ == '__main__':
    unittest.main()
