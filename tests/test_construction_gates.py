import unittest

from ges.recovery import evaluate_gate


class ConstructionGates(unittest.TestCase):
    def test_all_proven_conditions_can_close(self):
        gate = evaluate_gate('test', 2, 2, 'Complete evidence', {'independent_audit': True})
        self.assertEqual(gate['status'], 'CLOSED')

    def test_partial_review_is_observed_incompleteness(self):
        gate = evaluate_gate('test', 1, 2, 'Complete evidence', {'independent_audit': None})
        self.assertEqual(gate['evaluation'], 'INCOMPLETE')
        self.assertIn('coverage_complete', gate['incomplete_conditions'])
        self.assertIn('independent_audit', gate['unverified_conditions'])

    def test_full_count_does_not_replace_independent_audit(self):
        gate = evaluate_gate('test', 2, 2, 'Complete evidence', {'independent_audit': None})
        self.assertEqual(gate['evaluation'], 'UNVERIFIED')
        self.assertEqual(gate['status'], 'OPEN')

    def test_zero_denominator_is_not_success(self):
        gate = evaluate_gate('test', 0, 0, 'Complete evidence', {'bindings': True})
        self.assertEqual(gate['status'], 'OPEN')

    def test_undeclared_native_scope_is_not_success(self):
        gate = evaluate_gate('test', 0, None, 'Complete evidence', {'behavior': True})
        self.assertIn('coverage_complete', gate['unverified_conditions'])

    def test_string_truth_is_not_a_receipt(self):
        with self.assertRaises(ValueError):
            evaluate_gate('test', 2, 2, 'Complete evidence', {'audit': 'true'})

    def test_cannot_reduce_denominator_below_completed(self):
        with self.assertRaises(ValueError):
            evaluate_gate('test', 3, 2, 'Complete evidence', {'audit': True})

    def test_empty_prerequisites_are_not_certification(self):
        with self.assertRaises(ValueError):
            evaluate_gate('test', 2, 2, 'Complete evidence', {})

    def test_prerequisites_cannot_override_incomplete_coverage(self):
        with self.assertRaises(ValueError):
            evaluate_gate('test', 1, 2, 'Complete evidence', {'coverage_complete': True})
