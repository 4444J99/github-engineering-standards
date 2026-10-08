"""Counterexamples for falsely closing scoped construction milestones.

Closed legacy gates in these projection tests are synthetic evaluated inputs.
They do not stand in for the unfinished native/generalization evidence adapters.
Publication positives run the actual exact-use validator on synthetic receipts.
"""
import copy
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from ges.milestones import GATE_PREREQUISITES, milestone_accounting
from ges.recovery import evaluate_gate, status


def gate_fixture():
    return [evaluate_gate(name, 1, 1, 'Synthetic fully accounted scope',
                          {key: True for key in prerequisites})
            for name, prerequisites in GATE_PREREQUISITES.items()]


def replace_gate(gates, name, *, completed=0, denominator=None, unknown=True):
    prerequisites = {key: None if unknown else True
                     for key in GATE_PREREQUISITES[name]}
    replacement = evaluate_gate(name, completed, denominator,
                                'Synthetic bounded evidence', prerequisites)
    return [replacement if gate['gate'] == name else gate for gate in gates]


class CompletionMilestones(unittest.TestCase):
    def test_closed_legacy_rights_does_not_clear_actual_publication_use(self):
        gates = gate_fixture()
        report = milestone_accounting(gates)
        milestones = report['milestones']
        self.assertEqual(milestones['six_source_synthesis']['evaluation'], 'PROVEN')
        self.assertEqual(milestones['native_pilot_acceptance']['evaluation'], 'PROVEN')
        publication = milestones['public_release_clearance']
        self.assertEqual(publication['status'], 'OPEN')
        self.assertEqual(publication['evaluation'], 'UNVERIFIED')
        self.assertIsNone(publication['denominator'])
        self.assertEqual(report['ges_v0_2']['evaluation'], 'UNVERIFIED')
        self.assertFalse(report['governance_acceptance_automatically_certified'])

    def test_incomplete_and_unknown_conditions_are_both_preserved(self):
        gates = replace_gate(gate_fixture(), 'semantic_extraction',
                             completed=1, denominator=2)
        report = milestone_accounting(gates)
        synthesis = report['milestones']['six_source_synthesis']
        self.assertEqual(synthesis['evaluation'], 'INCOMPLETE')
        self.assertIn('semantic_extraction.coverage_complete',
                      synthesis['incomplete_conditions'])
        self.assertIn('semantic_extraction.atomic_claim_fidelity_audit',
                      synthesis['unverified_conditions'])
        self.assertEqual(report['ges_v0_2']['evaluation'], 'INCOMPLETE')

    def test_complete_counts_without_audit_are_unverified(self):
        gates = replace_gate(gate_fixture(), 'semantic_extraction',
                             completed=1, denominator=1)
        result = milestone_accounting(gates)['milestones']['six_source_synthesis']
        self.assertEqual(result['evaluation'], 'UNVERIFIED')
        self.assertFalse(result['incomplete_conditions'])
        self.assertTrue(result['unverified_conditions'])

    def test_zero_legacy_denominator_never_closes_synthesis(self):
        gates = replace_gate(gate_fixture(), 'operational_completeness',
                             completed=0, denominator=0, unknown=False)
        result = milestone_accounting(gates)['milestones']['six_source_synthesis']
        self.assertEqual(result['evaluation'], 'UNVERIFIED')
        self.assertIn('operational_completeness.coverage_complete',
                      result['unverified_conditions'])

    def test_missing_unknown_duplicate_and_nonarray_gate_identities_rejected(self):
        gates = gate_fixture()
        unknown = copy.deepcopy(gates)
        unknown[0]['gate'] = 'new_approval'
        cases = ([], gates[:-1], [*gates, gates[0]], unknown, {}, None)
        for case in cases:
            with self.subTest(case=case), self.assertRaises(ValueError):
                milestone_accounting(case)

    def test_even_independent_legacy_rights_gate_cannot_be_omitted(self):
        gates = [gate for gate in gate_fixture()
                 if gate['gate'] != 'rights_and_publication']
        with self.assertRaisesRegex(ValueError, 'Missing legacy gate'):
            milestone_accounting(gates)

    def test_arbitrary_boolean_cannot_replace_required_legacy_conditions(self):
        gates = gate_fixture()
        gates[0] = evaluate_gate('exhaustive_artifact_accounting', 1, 1,
                                 'Synthetic unsupported shortcut',
                                 {'approved': True})
        with self.assertRaisesRegex(ValueError, 'conditions'):
            milestone_accounting(gates)

    def test_inconsistent_count_status_or_claimed_evidence_rejected(self):
        changes = (
            {'completed': True}, {'denominator': True}, {'remaining': False},
            {'remaining': 7}, {'status': 'OPEN'}, {'evaluation': 'INCOMPLETE'},
            {'unverified_conditions': ['imagined_audit']},
            {'incomplete_conditions': ['coverage_complete']},
            {'approved': True}, {'evidence': 'unvalidated-sidecar.json'},
        )
        for change in changes:
            with self.subTest(change=change), self.assertRaises(ValueError):
                gates = gate_fixture()
                gates[0].update(change)
                milestone_accounting(gates)

    def test_false_closure_and_string_observations_rejected(self):
        for value in (False, None, 'true', 1):
            with self.subTest(value=value), self.assertRaises(ValueError):
                gates = gate_fixture()
                gates[0]['conditions']['pinned_git_trees_match'] = value
                milestone_accounting(gates)

    def test_gate_order_does_not_change_milestone_output(self):
        gates = gate_fixture()
        before = copy.deepcopy(gates)
        self.assertEqual(milestone_accounting(gates), milestone_accounting(gates[::-1]))
        self.assertEqual(gates, before)

    def test_legacy_rights_accounting_cannot_impersonate_actual_use_accounting(self):
        from ges.publication_use import validate_accounting_result
        forged = {'schema': 'ges.rights-acceptance-accounting.v1',
                  'completed': 1, 'denominator': 1,
                  'per_file_rights_acceptance': True,
                  'authorized_distribution_decision': True}
        with self.assertRaises(ValueError):
            validate_accounting_result(forged)
        with self.assertRaises(ValueError):
            milestone_accounting(gate_fixture(), forged)

    def test_boolean_sidecar_cannot_close_publication(self):
        with self.assertRaises(ValueError):
            milestone_accounting(gate_fixture(), {
                'schema': 'ges.publication-use-accounting.v1',
                'exact_use_clearance': True,
                'authorized_distribution_decision': True,
                'complete_output_inventory': True,
                'use_register_complete': True,
            })

    def publication_fixture(self, root, *, zero_use=False, release_scope='GES_V0_2'):
        from ges.publication_use import publication_accounting
        from test_publication_use import create_fixture
        fixture = create_fixture(root, zero_use=zero_use, release_scope=release_scope)
        return fixture, publication_accounting(**fixture)

    def test_v02_can_close_with_validated_publication_and_estate_still_open(self):
        with TemporaryDirectory() as temporary:
            _, publication = self.publication_fixture(Path(temporary))
            gates = replace_gate(gate_fixture(), 'estate_rollout')
            gates = replace_gate(gates, 'rights_and_publication',
                                 completed=0, denominator=8)
            result = milestone_accounting(gates, publication)
        self.assertEqual(result['ges_v0_2']['status'], 'CLOSED')
        self.assertEqual(result['ges_v0_2']['evaluation'], 'PROVEN')
        self.assertFalse(result['ges_v0_2']['estate_rollout_required'])
        self.assertEqual(result['milestones']['estate_rollout']['evaluation'], 'UNVERIFIED')
        self.assertEqual(result['milestones']['public_release_clearance']['evaluation'], 'PROVEN')
        self.assertFalse(all(gate['status'] == 'CLOSED' for gate in gates))
        self.assertEqual(len(gates), 9)

    def test_validated_zero_use_requires_explicit_nonempty_output_review(self):
        with TemporaryDirectory() as temporary:
            _, publication = self.publication_fixture(Path(temporary), zero_use=True)
            self.assertEqual(publication['denominator'], 0)
            self.assertTrue(publication['zero_use_clearance'])
            result = milestone_accounting(gate_fixture(), publication)
            self.assertEqual(result['milestones']['public_release_clearance']['evaluation'], 'PROVEN')
            publication['zero_use_clearance'] = False
            with self.assertRaises(ValueError):
                milestone_accounting(gate_fixture(), publication)

    def test_cleared_bounded_package_cannot_clear_project_release(self):
        with TemporaryDirectory() as temporary:
            _, publication = self.publication_fixture(
                Path(temporary), release_scope='BOUNDED_PACKAGE')
            self.assertTrue(publication['exact_use_clearance'])
            result = milestone_accounting(gate_fixture(), publication)
        milestone = result['milestones']['public_release_clearance']
        self.assertEqual(milestone['release_scope'], 'BOUNDED_PACKAGE')
        self.assertEqual(milestone['status'], 'OPEN')
        self.assertIn('ges_v0_2_release_scope', milestone['incomplete_conditions'])
        self.assertEqual(result['ges_v0_2']['status'], 'OPEN')

    def test_tampered_validated_publication_count_is_rejected(self):
        with TemporaryDirectory() as temporary:
            _, publication = self.publication_fixture(Path(temporary))
            publication['completed'] += 1
            with self.assertRaises(ValueError):
                milestone_accounting(gate_fixture(), publication)

    def test_missing_use_receipts_show_observed_incomplete_coverage(self):
        from ges.publication_use import publication_accounting
        with TemporaryDirectory() as temporary:
            fixture, _ = self.publication_fixture(Path(temporary))
            fixture['receipts'] = []
            publication = publication_accounting(**fixture)
            result = milestone_accounting(gate_fixture(), publication)
        self.assertEqual(result['milestones']['public_release_clearance']['evaluation'], 'INCOMPLETE')
        self.assertEqual(result['ges_v0_2']['evaluation'], 'INCOMPLETE')


class RecoveryMilestoneIntegration(unittest.TestCase):
    def setUp(self):
        # Reuse the existing real recovery-input fixture without rerunning its
        # entire TestCase through inheritance or importing it into our namespace.
        import test_published_assurance
        self.fixture = test_published_assurance.PublishedAssurance()
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)

    def test_existing_recovery_inputs_preserve_nine_gates_and_add_unknown_publication(self):
        sources, corpus, _, _ = self.fixture.recovery_fixture()
        with patch('ges.recovery.ROOT', self.fixture.root):
            result = status(sources, corpus, rendered_directory=self.fixture.cache)
        self.assertEqual(len(result['gates']), 9)
        self.assertEqual(result['project_complete'],
                         all(gate['status'] == 'CLOSED' for gate in result['gates']))
        self.assertIsNone(result['publication_use_accounting'])
        milestones = result['milestone_accounting']['milestones']
        self.assertEqual(milestones['public_release_clearance']['evaluation'], 'UNVERIFIED')
        self.assertEqual(milestones['native_pilot_acceptance']['evaluation'], 'UNVERIFIED')
        self.assertEqual(milestones['estate_rollout']['evaluation'], 'UNVERIFIED')
        self.assertEqual(milestones['six_source_synthesis']['evaluation'], 'INCOMPLETE')

    def test_partial_publication_input_group_rejected_before_file_access(self):
        fields = ('publication_manifest', 'publication_register',
                  'publication_receipts', 'publication_policy',
                  'publication_output_root')
        absent = Path('/synthetic-no-source-access')
        for name in fields:
            with self.subTest(name=name), self.assertRaisesRegex(ValueError, 'requires manifest'):
                status(absent, absent, **{name: absent})
        for missing in fields:
            inputs = {name: absent for name in fields if name != missing}
            with self.subTest(missing=missing), self.assertRaisesRegex(ValueError, 'requires manifest'):
                status(absent, absent, **inputs)

    def test_recovery_rejects_actual_use_summary_in_place_of_manifest(self):
        sources, corpus, _, _ = self.fixture.recovery_fixture()
        root = self.fixture.root
        manifest, register = root / 'publication-manifest.json', root / 'publication-register.json'
        receipts, policy = root / 'publication-receipts.json', root / 'publication-policy.json'
        manifest.write_text(json.dumps({'schema': 'ges.publication-use-accounting.v1',
                                        'exact_use_clearance': True}))
        register.write_text('{}')
        receipts.write_text('[]')
        policy.write_text('{}')
        output = root / 'candidate'
        output.mkdir()
        with patch('ges.recovery.ROOT', root), self.assertRaises(ValueError):
            status(sources, corpus, publication_manifest=manifest,
                   publication_register=register, publication_receipts=receipts,
                   publication_policy=policy, publication_output_root=output)

    def test_recovery_validates_real_input_chain_without_closing_native_or_legacy_rights(self):
        from test_publication_use import create_fixture
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            fixture = create_fixture(root)
            sources, corpus = fixture['source_root'], root / 'corpus'
            for directory in (corpus, root / 'controls', root / 'templates', root / 'profiles'):
                directory.mkdir()
            for filename in ('catalog.json', 'review_queue.json'):
                (root / 'controls' / filename).write_text('[]')
            (sources / 'sources.lock.json').write_text(json.dumps({
                'sources': [{'repository': source, 'commit': commit}
                            for source, commit in fixture['pins'].items()]}))
            for source in fixture['pins']:
                slug = source.replace('/', '__')
                inventory = [item for item in fixture['artifacts'] if item['source'] == source]
                (sources / (slug + '.inventory.json')).write_text(json.dumps(inventory))
                (sources / (slug + '.tree-reconciliation.json')).write_text('{"status":"MATCH"}')
            (corpus / 'artifacts.jsonl').write_text(''.join(
                json.dumps(item) + '\n' for item in fixture['artifacts']))
            (corpus / 'candidates.jsonl').write_text('')
            (corpus / 'ledger-summary.json').write_text('{}')
            (corpus / 'structured-source-requirements.json').write_text('[]')
            (corpus / 'published-page-ledger.json').write_text(json.dumps([
                {**self.fixture.page, 'source_matches': []}]))
            (root / 'evidence' / 'rights-review-queue.json').write_text('{"records":[]}')
            inputs = {}
            for name in ('manifest', 'register', 'receipts', 'policy'):
                path = root / ('publication-' + name + '.json')
                path.write_text(json.dumps(fixture[name]))
                inputs['publication_' + name] = path
            inputs['publication_output_root'] = fixture['output_root']
            with patch('ges.recovery.ROOT', root):
                result = status(sources, corpus, **inputs)
        self.assertTrue(result['publication_use_accounting']['exact_use_clearance'])
        milestones = result['milestone_accounting']['milestones']
        self.assertEqual(milestones['public_release_clearance']['evaluation'], 'PROVEN')
        self.assertEqual(milestones['native_pilot_acceptance']['evaluation'], 'UNVERIFIED')
        self.assertEqual(milestones['estate_rollout']['evaluation'], 'UNVERIFIED')
        rights = next(gate for gate in result['gates'] if gate['gate'] == 'rights_and_publication')
        self.assertEqual(rights['status'], 'OPEN')
        self.assertEqual(rights['completed'], 0)
        self.assertFalse(result['project_complete'])


if __name__ == '__main__':
    unittest.main()
