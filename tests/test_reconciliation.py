import copy
import io
import json
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from tempfile import TemporaryDirectory

from ges.__main__ import main
from ges.reconciliation import AST_FIELDS, audit, fingerprint, inputs, propose
from ges.semantics import canonical_bytes, stable_id
from tests.test_semantics import record


class ReconciliationMachinery(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'evidence').mkdir()
        self.proposition = record('semantic-proposition')
        self.propositions = [self.proposition]
        self.controls = [{'id': 'GES-TEST-001', 'revision': 1}]
        for field, reviewer in (('primary_review', 'primary'), ('omission_review', 'omission')):
            self.proposition[field] = {
                'status': 'REVIEWED', 'reviewer': reviewer,
                'evidence_reference': f'evidence/{field}.json'}
        self.policy = {
            'schema': 'ges.reconciliation-authority.v1',
            'approval_reference': 'synthetic fixture only',
            'input_digest': inputs(self.propositions, self.controls)[2],
            'primary_reviewers': ['primary'], 'omission_reviewers': ['omission'],
            'reconcilers': ['reconciler'], 'auditors': ['auditor'],
        }
        self.decision = record('reconciliation-decision')
        self.decision.update({
            'proposition_ids': [self.proposition['id']], 'disposition': 'REFERENCE',
            'source_treatment': 'RETAINED', 'control_references': [],
            'preserved_fields': sorted(AST_FIELDS), 'lost_fields': [], 'conflicts': [],
            'review': {'status': 'REVIEWED', 'reviewer': 'reconciler',
                       'evidence_reference': 'evidence/decision.json'},
        })
        self.refresh()

    def evidence(self, path, kind, reviewer, subject):
        (self.root / path).write_text(json.dumps({
            'schema': 'ges.reconciliation-evidence.v1', 'kind': kind,
            'reviewer': reviewer, 'subject_digest': subject,
            'input_digest': self.policy['input_digest'], 'outcome': 'PASS'}))

    def refresh(self):
        self.decision['id'] = stable_id(self.decision)
        self.audits = [{'decision_id': self.decision['id'], 'auditor': 'auditor',
                        'evidence_reference': 'evidence/audit.json'}]
        for prop in self.propositions:
            subject = fingerprint({k: v for k, v in prop.items()
                                   if k not in ('primary_review', 'omission_review')})
            for field, kind in (('primary_review', 'PRIMARY'), ('omission_review', 'OMISSION')):
                review = prop[field]
                self.evidence(review['evidence_reference'], kind, review['reviewer'], subject)
        self.evidence('evidence/decision.json', 'RECONCILIATION', 'reconciler', fingerprint(self.decision))
        self.evidence('evidence/audit.json', 'INDEPENDENT_AUDIT', 'auditor', fingerprint(self.decision))

    def account(self):
        return audit(self.propositions, self.controls, [self.decision],
                     self.policy, self.root, self.audits)

    def add_variant(self, field, value):
        other = copy.deepcopy(self.proposition)
        other['semantic_ast'][field] = value
        other['id'] = stable_id(other)
        other['occurrence_ids'] = ['other-occurrence']
        for name in ('primary_review', 'omission_review'):
            other[name]['evidence_reference'] = f'evidence/other-{name}.json'
        self.propositions.append(other)
        return other

    def test_authorized_reference_accounting_is_deterministic_and_does_not_adopt(self):
        result = self.account()
        self.assertEqual(result, self.account())
        self.assertTrue(result['decision_accounting_complete'])
        self.assertFalse(result['semantic_truth_certified'])
        self.assertFalse(result['policy_adopted'])

    def test_comparisons_preserve_modality_qualifiers_and_input_order_independence(self):
        self.add_variant('qualifiers', ['private repositories'])
        result = propose(self.propositions, self.controls)
        self.assertEqual(result, propose(list(reversed(self.propositions)), self.controls))
        group = result['comparisons'][0]
        self.assertEqual(group['status'], 'PROPOSED')
        self.assertEqual(group['differing_fields'], ['qualifiers'])
        self.assertEqual(group['relation'], 'RELATED')
        self.propositions[1]['semantic_ast']['polarity'] = 'NEGATIVE'
        self.propositions[1]['id'] = stable_id(self.propositions[1])
        self.assertEqual(propose(self.propositions, self.controls)['comparisons'][0]['relation'],
                         'POSSIBLE_CONFLICT')

    def test_same_keywords_do_not_cluster_different_predicates(self):
        self.add_variant('action', 'synthetic but different action')
        self.assertEqual(propose(self.propositions, self.controls)['comparisons'], [])

    def test_partial_accounting_preserves_full_denominator(self):
        self.add_variant('qualifiers', ['extra qualifier'])
        self.policy['input_digest'] = inputs(self.propositions, self.controls)[2]
        self.refresh()
        result = self.account()
        self.assertEqual(result['known_proposition_count'], 2)
        self.assertEqual(result['unmapped_proposition_ids'], [self.propositions[1]['id']])
        self.assertFalse(result['decision_accounting_complete'])

    def test_stale_input_or_authority_digest_rejected(self):
        self.controls[0]['revision'] = 2
        with self.assertRaisesRegex(ValueError, 'Stale authority'):
            self.account()

    def test_changed_proposition_metadata_invalidates_authority(self):
        self.proposition['ambiguities'] = ['new uncertainty with unchanged AST identity']
        with self.assertRaisesRegex(ValueError, 'Stale authority'):
            self.account()

    def test_primary_and_omission_roles_must_be_independent(self):
        self.policy['omission_reviewers'] = ['primary']
        self.proposition['omission_review']['reviewer'] = 'primary'
        self.policy['input_digest'] = inputs(self.propositions, self.controls)[2]
        self.refresh()
        with self.assertRaises(ValueError):
            self.account()

    def test_unknown_or_stale_control_references_rejected(self):
        self.decision['disposition'] = 'EXISTING_CONTROL'
        for refs in ([], [{'id': 'unknown', 'revision': 1}],
                     [{'id': 'GES-TEST-001', 'revision': 2}]):
            self.decision['control_references'] = refs
            self.refresh()
            with self.subTest(refs=refs), self.assertRaises(ValueError):
                self.account()

    def test_proposal_cannot_be_reviewed_evidence(self):
        self.decision['review'] = {'status': 'PROPOSED', 'reviewer': None,
                                   'evidence_reference': None}
        self.refresh()
        with self.assertRaisesRegex(ValueError, 'Proposal cannot'):
            self.account()

    def test_unauthorized_reviewer_rejected(self):
        self.policy['reconcilers'] = ['someone-else']
        with self.assertRaisesRegex(ValueError, 'Unauthorized reviewer'):
            self.account()

    def test_collapsed_review_roles_rejected(self):
        self.policy['auditors'] = ['reconciler']
        self.audits[0]['auditor'] = 'reconciler'
        with self.assertRaisesRegex(ValueError, 'non-independent'):
            self.account()

    def test_missing_independent_audit_rejected(self):
        self.audits = []
        with self.assertRaisesRegex(ValueError, 'independent audit'):
            self.account()

    def test_tampered_digest_or_model_output_cannot_be_audit_evidence(self):
        path = self.root / 'evidence/audit.json'
        for changes in ({'subject_digest': '0' * 64}, {'outcome': 'PROPOSED'},
                        {'reviewer': 'model'}, {'input_digest': '0' * 64}):
            self.refresh()
            document = json.loads(path.read_text())
            document.update(changes)
            path.write_text(json.dumps(document))
            with self.subTest(changes=changes), self.assertRaisesRegex(ValueError, 'does not bind'):
                self.account()

    def test_evidence_traversal_and_symlink_rejected(self):
        self.audits[0]['evidence_reference'] = '../audit.json'
        with self.assertRaisesRegex(ValueError, 'Unsafe'):
            self.account()
        (self.root / 'evidence/link.json').symlink_to(self.root / 'evidence/audit.json')
        self.audits[0]['evidence_reference'] = 'evidence/link.json'
        with self.assertRaisesRegex(ValueError, 'Symlinked'):
            self.account()

    def test_incomplete_semantic_fields_rejected(self):
        self.decision['preserved_fields'].remove('exceptions')
        self.refresh()
        with self.assertRaisesRegex(ValueError, 'field accounting'):
            self.account()

    def test_false_duplicate_rejected(self):
        self.add_variant('exceptions', ['an exception'])
        self.decision['proposition_ids'].append(self.propositions[1]['id'])
        self.decision['disposition'] = 'DUPLICATE'
        self.policy['input_digest'] = inputs(self.propositions, self.controls)[2]
        self.refresh()
        with self.assertRaisesRegex(ValueError, 'False equivalence'):
            self.account()

    def test_duplicate_occurrences_may_share_one_exact_proposition(self):
        self.proposition['occurrence_ids'].append('another-occurrence')
        self.policy['input_digest'] = inputs(self.propositions, self.controls)[2]
        self.decision['disposition'] = 'DUPLICATE'
        self.refresh()
        self.assertTrue(self.account()['decision_accounting_complete'])

    def test_conflict_cannot_be_erased_or_counted_as_complete(self):
        other = self.add_variant('polarity', 'NEGATIVE')
        self.policy['input_digest'] = inputs(self.propositions, self.controls)[2]
        self.refresh()
        with self.assertRaisesRegex(ValueError, 'conflict would be erased'):
            self.account()
        self.decision.update({'proposition_ids': [self.proposition['id'], other['id']],
                              'disposition': 'CONFLICT', 'source_treatment': 'CONFLICTING',
                              'conflicts': [other['id']]})
        self.refresh()
        result = self.account()
        self.assertFalse(result['decision_accounting_complete'])
        self.assertEqual(result['conflict_proposition_ids'], sorted(p['id'] for p in self.propositions))

    def test_ambiguity_remains_unresolved_after_receipt_validation(self):
        self.proposition['ambiguities'] = ['Unresolved source ambiguity']
        self.policy['input_digest'] = inputs(self.propositions, self.controls)[2]
        self.refresh()
        self.assertFalse(self.account()['decision_accounting_complete'])

    def test_unknown_conflict_and_duplicate_decision_rejected(self):
        self.decision['conflicts'] = ['foreign-proposition']
        self.refresh()
        with self.assertRaisesRegex(ValueError, 'Unknown conflict'):
            self.account()
        self.decision['conflicts'] = []
        self.refresh()
        with self.assertRaisesRegex(ValueError, 'Duplicate record'):
            audit(self.propositions, self.controls, [self.decision, self.decision],
                  self.policy, self.root, self.audits)

    def test_cli_proposals_audit_and_no_overwrite(self):
        paths = {name: self.root / (name + '.json') for name in
                 ('propositions', 'controls', 'decisions', 'authority', 'audits')}
        paths['propositions'].write_bytes(canonical_bytes(self.proposition) + b'\n')
        paths['decisions'].write_bytes(canonical_bytes(self.decision) + b'\n')
        for key, value in (('controls', self.controls), ('authority', self.policy), ('audits', self.audits)):
            paths[key].write_bytes(canonical_bytes(value))
        base = ['semantics', 'reconcile', '--propositions', str(paths['propositions']),
                '--controls', str(paths['controls']), '--output', str(self.root / 'proposals.json')]
        with redirect_stdout(io.StringIO()):
            self.assertEqual(main(base), 0)
            with self.assertRaises(FileExistsError):
                main(base)
            command = ['semantics', 'audit', '--evidence-root', str(self.root)]
            for key, path in paths.items():
                command += ['--' + key, str(path)]
            command += ['--output', str(self.root / 'report.json')]
            self.assertEqual(main(command), 0)
        report = json.loads((self.root / 'report.json').read_text())
        self.assertTrue(report['decision_accounting_complete'])

    def test_empty_inputs_rejected(self):
        with self.assertRaisesRegex(ValueError, 'No propositions'):
            propose([], [])

    def test_oversized_audit_tranche_rejected(self):
        propositions = []
        for index in range(251):
            prop = copy.deepcopy(self.proposition)
            prop['semantic_ast']['object'] = f'synthetic object {index}'
            prop['id'] = stable_id(prop)
            propositions.append(prop)
        with self.assertRaisesRegex(ValueError, '250 propositions'):
            audit(propositions, self.controls, [], self.policy, self.root, [])
