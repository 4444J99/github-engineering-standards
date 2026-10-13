"""Preserved membership and exact additions cannot hide unrelated workload drift."""
import hashlib
import json
import unittest
from pathlib import Path
from unittest.mock import patch

import test_claim_workload as fixtures
from ges.claim_workload import check_inventory, inventory
from ges.claim_workload_migration import check_transition


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class WorkloadMigration(unittest.TestCase):
    def setUp(self):
        self.fixture = fixtures.ClaimWorkload()
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        f = self.fixture
        f.add('first.md', [f.claim('old')])
        self.historical, self.baseline, self.artifacts, self.provenance = f.forward_baseline()
        self.added = f.reviews / 'successor-claims.json'
        self.added.write_text(json.dumps({
            'source': 'owner/source', 'commit': 'a' * 40, 'path': 'first.md',
            'claims': [f.claim('new', supersedes_claim_id='old')]}))
        self.current = f.root / 'new-current.json'
        self.current.write_text(json.dumps(f.run_inventory(), indent=2) + '\n')
        self.transition = f.root / 'transition.json'
        self.inputs = {'historical': self.historical, 'baseline': self.baseline,
                       'provenance': self.provenance, 'artifacts': self.artifacts,
                       'reconciliation': f.receipts, 'current': self.current}
        self.contract = {
            'schema': 'ges.claim-workload-transition.v1', 'transition_id': 'synthetic',
            'bindings': {key: sha(path) for key, path in self.inputs.items()},
            'added_document': {'path': self.added.name, 'sha256': sha(self.added), 'claims': 1},
            'successor_pairs': [{'predecessor': 'old', 'successor': 'new'}],
            'family_id': json.loads(self.baseline.read_text())['families'][0]['family_id'],
            'new_review_credit': 0, 'new_reconciliation_credit': 0}
        self.transition.write_text(json.dumps(self.contract))
        authority = patch('ges.claim_workload_migration.DEFAULT_TRANSITION_SHA256', sha(self.transition))
        authority.start()
        self.addCleanup(authority.stop)

    def check(self):
        f = self.fixture
        return check_transition(f.reviews, self.artifacts, f.receipts, self.baseline,
                                self.historical, self.provenance, self.transition, self.current)

    def test_preserved_and_current_reports_both_reproduce_without_writing(self):
        before = {path: path.read_bytes() for path in self.fixture.root.rglob('*') if path.is_file()}
        result = self.check()
        self.assertEqual(result['historical_recorded_claims'], 1)
        self.assertEqual(result['current_recorded_claims'], 2)
        self.assertEqual(result['added_claims'], 1)
        self.assertEqual(result['preserved_families'], 1)
        self.assertEqual(result['new_review_credit'], 0)
        self.assertEqual(result['new_reconciliation_credit'], 0)
        self.assertFalse(result['full_source_provenance_replayed'])
        self.assertFalse(result['replacement_receipt_envelopes_issued'])
        self.assertEqual(before, {path: path.read_bytes() for path in before})

    def test_historical_selection_is_explicit_and_does_not_weaken_default_check(self):
        f = self.fixture
        with self.assertRaisesRegex(ValueError, 'Committed workload inventory differs'):
            check_inventory(f.reviews, self.artifacts, f.receipts, self.baseline)
        result = check_inventory(f.reviews, self.artifacts, f.receipts, self.baseline,
                                 historical=self.historical, provenance=self.provenance,
                                 recorded_membership=True)
        self.assertEqual(result['counts']['recorded_claims'], 1)
        self.assertEqual(inventory(f.reviews, self.artifacts, f.receipts)['counts']['recorded_claims'], 2)

    def test_same_count_historical_claim_or_document_byte_changes_are_rejected(self):
        path = self.fixture.reviews / 'first.md-claims.json'
        original = path.read_bytes()
        for kind in ('statement', 'claim_id', 'metadata', 'whitespace'):
            with self.subTest(kind=kind):
                document = json.loads(original)
                if kind == 'statement':
                    document['claims'][0]['statement'] = 'Different meaning.'
                elif kind == 'claim_id':
                    document['claims'][0]['claim_id'] = 'replacement-old'
                elif kind == 'metadata':
                    document['arbitrary'] = 'changed'
                path.write_bytes(original + b'\n' if kind == 'whitespace' else json.dumps(document).encode())
                try:
                    with self.assertRaisesRegex(ValueError, 'Preserved claim document bytes or count'):
                        self.check()
                finally:
                    path.write_bytes(original)

    def test_missing_old_document_is_rejected(self):
        (self.fixture.reviews / 'first.md-claims.json').unlink()
        with self.assertRaisesRegex(ValueError, 'missing'):
            self.check()

    def test_unrelated_extra_document_is_not_hidden_by_historical_selection(self):
        document = json.loads(self.added.read_text())
        document['claims'][0]['claim_id'] = 'unrelated'
        (self.fixture.reviews / 'unrelated-claims.json').write_text(json.dumps(document))
        with self.assertRaisesRegex(ValueError, 'Committed workload inventory differs'):
            self.check()

    def test_altered_successor_cannot_rebind_its_own_report_and_transition(self):
        original_doc, original_report = self.added.read_bytes(), self.current.read_bytes()
        original_contract = self.transition.read_bytes()
        for field, value in (('statement', 'changed'), ('source_strength', 'ACCEPTED'),
                             ('start_line', 5), ('supersedes_claim_id', 'not-old')):
            with self.subTest(field=field):
                document = json.loads(original_doc)
                document['claims'][0][field] = value
                if field == 'start_line':
                    document['claims'][0]['end_line'] = value
                self.added.write_text(json.dumps(document))
                self.current.write_text(json.dumps(self.fixture.run_inventory(), indent=2) + '\n')
                forged = json.loads(original_contract)
                forged['bindings']['current'] = sha(self.current)
                forged['added_document']['sha256'] = sha(self.added)
                self.transition.write_text(json.dumps(forged))
                try:
                    with self.assertRaisesRegex(ValueError, 'independently pinned contract'):
                        self.check()
                finally:
                    self.added.write_bytes(original_doc)
                    self.current.write_bytes(original_report)
                    self.transition.write_bytes(original_contract)

    def test_omitted_or_duplicate_successor_is_rejected(self):
        original = self.added.read_bytes()
        for claims in ([], [self.fixture.claim('old')], [self.fixture.claim('unapproved')]):
            with self.subTest(claims=claims):
                document = json.loads(original)
                document['claims'] = claims
                self.added.write_text(json.dumps(document))
                try:
                    with self.assertRaises(ValueError):
                        self.check()
                finally:
                    self.added.write_bytes(original)

    def test_changed_frozen_receipt_or_baseline_cannot_be_used(self):
        for path in self.inputs.values():
            with self.subTest(input=path.name):
                original = path.read_bytes()
                path.write_bytes(original + b'\n')
                try:
                    with self.assertRaisesRegex(ValueError, 'Pinned workload transition input differs'):
                        self.check()
                finally:
                    path.write_bytes(original)

    def test_preserved_membership_requires_safe_unique_direct_child_names_and_types(self):
        f = self.fixture
        member = json.loads(self.baseline.read_text())['inputs']['claim_documents'][0]
        invalid = [None, [], [None], [{**member, 'extra': 'data'}], [member, member]]
        invalid.extend([[{**member, 'path': path}] for path in
                        ('../x-claims.json', '/x-claims.json', 'nested/x-claims.json',
                         'x\\y-claims.json', 'x\n-claims.json', 'wrong.json')])
        invalid.extend([[{**member, 'claims': value}] for value in (True, 0, -1, 1.0)])
        invalid.extend([[{**member, 'sha256': value}] for value in ('A' * 64, '0' * 63, None)])
        for membership in invalid:
            with self.subTest(membership=membership):
                # None means current-directory mode; malformed explicit report
                # membership must fail at the public preserved-check boundary.
                if membership is None:
                    report = json.loads(self.baseline.read_text())
                    report['inputs']['claim_documents'] = None
                    temp = f.root / 'bad-membership-report.json'
                    temp.write_text(json.dumps(report))
                    with self.assertRaises(ValueError):
                        check_inventory(f.reviews, self.artifacts, f.receipts, temp,
                                        recorded_membership=True)
                else:
                    with self.assertRaises(ValueError):
                        inventory(f.reviews, self.artifacts, f.receipts, claim_documents=membership)

    def test_symlinked_claim_and_transition_inputs_are_rejected(self):
        f = self.fixture
        link = f.reviews / 'link-claims.json'
        original = f.reviews / 'first.md-claims.json'
        link.symlink_to(original)
        with self.assertRaisesRegex(ValueError, 'Symlink'):
            inventory(f.reviews, self.artifacts, f.receipts,
                      claim_documents=[{'path': link.name, 'sha256': sha(original), 'claims': 1}])
        link.unlink()
        saved = f.root / 'saved-current.json'
        saved.write_bytes(self.current.read_bytes())
        self.current.unlink()
        self.current.symlink_to(saved)
        with self.assertRaisesRegex(ValueError, 'Symlink'):
            self.check()

    def test_outer_transaction_rejects_an_extra_document_after_current_replay(self):
        def add_after_check(*args, **kwargs):
            result = check_inventory(*args, **kwargs)
            if args[3] == self.current:
                (self.fixture.reviews / 'late-claims.json').write_bytes(self.added.read_bytes())
            return result
        with patch('ges.claim_workload_migration.check_inventory', side_effect=add_after_check):
            with self.assertRaisesRegex(ValueError, 'membership changed during transition check'):
                self.check()

    def test_source_identity_reference_changes_after_either_replay_are_rejected(self):
        identity = json.loads(self.provenance.read_text())['source_identity_reference']
        reference = self.provenance.parent / identity['path']
        original = reference.read_bytes()
        for replay in (self.baseline, self.current):
            with self.subTest(after=replay.name):
                def change_after_check(*args, **kwargs):
                    result = check_inventory(*args, **kwargs)
                    if args[3] == replay:
                        reference.write_bytes(original + b'\n')
                    return result
                try:
                    with patch('ges.claim_workload_migration.check_inventory',
                               side_effect=change_after_check):
                        with self.assertRaisesRegex(ValueError,
                                                    'Source identity reference changed'):
                            self.check()
                finally:
                    reference.write_bytes(original)

    def test_source_identity_reference_symlinks_after_either_replay_are_rejected(self):
        identity = json.loads(self.provenance.read_text())['source_identity_reference']
        reference = self.provenance.parent / identity['path']
        original = reference.read_bytes()
        target = self.fixture.root / 'identical-reference.json'
        target.write_bytes(original)
        for replay in (self.baseline, self.current):
            with self.subTest(after=replay.name):
                def link_after_check(*args, **kwargs):
                    result = check_inventory(*args, **kwargs)
                    if args[3] == replay:
                        reference.unlink()
                        reference.symlink_to(target)
                    return result
                try:
                    with patch('ges.claim_workload_migration.check_inventory',
                               side_effect=link_after_check):
                        with self.assertRaisesRegex(ValueError,
                                                    'Symlink source identity reference'):
                            self.check()
                finally:
                    reference.unlink(missing_ok=True)
                    reference.write_bytes(original)

    def test_transition_and_bound_input_changes_during_check_are_rejected(self):
        real_read = Path.read_bytes
        for target in (self.transition, *self.inputs.values()):
            with self.subTest(target=target.name):
                calls = 0
                def change_on_later_read(path):
                    nonlocal calls
                    raw = real_read(path)
                    if path == target:
                        calls += 1
                        if calls > 1:
                            return raw + b' '
                    return raw
                with patch.object(Path, 'read_bytes', change_on_later_read):
                    with self.assertRaises((ValueError, OSError, EOFError)):
                        self.check()


if __name__ == '__main__':
    unittest.main()
