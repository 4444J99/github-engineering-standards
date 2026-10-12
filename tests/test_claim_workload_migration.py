"""The approved successor addition must preserve, not replace, old accounting."""
import hashlib
import json
import subprocess
import sys
import unittest
from unittest.mock import patch

import test_claim_workload as fixtures
from ges import claim_workload_migration as migration
from ges.claim_workload import check_historical_equivalence, check_inventory, inventory
from ges.core import ROOT


class WorkloadMigrationIntegrity(unittest.TestCase):
    def setUp(self):
        self.fixture = fixtures.ClaimWorkload()
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        fixture = self.fixture
        predecessors = ['old-a', 'old-b', 'old-c', 'old-d', 'old-e']
        fixture.add('source.md', [fixture.claim(cid) for cid in [*predecessors, 'unrelated']])
        historical, baseline, artifacts, provenance = fixture.forward_baseline()
        self.old_document = fixture.reviews / 'source.md-claims.json'
        self.successor = fixture.reviews / migration.SUCCESSOR_DOCUMENT
        successor = json.loads(self.old_document.read_text())
        successor['claims'] = [fixture.claim(cid + '-new', supersedes_claim_id=cid)
                               for cid in predecessors]
        self.successor.write_text(json.dumps(successor))
        approval = fixture.root / 'approval.json'
        approval.write_text(json.dumps({
            'successor_document_sha256': hashlib.sha256(self.successor.read_bytes()).hexdigest(),
            'proposed_decisions': [{'predecessor': cid, 'successor': cid + '-new'}
                                   for cid in predecessors],
        }))
        self.current = fixture.root / 'expanded.json'
        self.arguments = dict(reviews=fixture.reviews, artifacts=artifacts,
                              reconciliation=fixture.receipts, baseline=baseline,
                              current=self.current, historical=historical,
                              provenance=provenance, approval=approval)
        # Fixture authority is fixed before mutations; mutable reports cannot repin it.
        pinned = {key: hashlib.sha256(self.arguments[key].read_bytes()).hexdigest()
                  for key in migration.FROZEN_SHA256}
        anchor = patch.object(migration, 'FROZEN_SHA256', pinned)
        anchor.start()
        self.addCleanup(anchor.stop)
        self.regenerate_current()

    def regenerate_current(self):
        result = inventory(self.arguments['reviews'], self.arguments['artifacts'],
                           self.arguments['reconciliation'])
        self.current.write_text(json.dumps(result, indent=2) + '\n')

    def test_complete_addition_preserves_all_predecessors_and_zero_credit(self):
        result = migration.check_migration(**self.arguments)
        self.assertEqual(result['baseline_recorded_claims'], 6)
        self.assertEqual(result['current_recorded_claims'], 11)
        self.assertEqual(result['baseline_claim_documents'], 1)
        self.assertEqual(result['current_claim_documents'], 2)
        self.assertEqual(result['families'], 1)
        self.assertEqual(result['reconciliation_records_present'], 0)
        self.assertEqual(result['recorded_claims_without_reconciliation'], 11)
        self.assertEqual(result['new_reconciliation_credit'], 0)

    def test_full_inventory_and_strict_historical_equivalence_still_reject_added_claims(self):
        args = self.arguments
        with self.assertRaisesRegex(ValueError, 'Committed workload inventory differs'):
            check_inventory(args['reviews'], args['artifacts'], args['reconciliation'], args['baseline'])
        with self.assertRaisesRegex(ValueError, 'Historical workload accounting differs'):
            check_historical_equivalence(json.loads(self.current.read_text()), args['historical'])

    def test_unrelated_document_cannot_be_hidden_by_regenerating_current_report(self):
        doc = json.loads(self.old_document.read_text())
        doc['claims'] = [self.fixture.claim('unexpected')]
        (self.fixture.reviews / 'extra-claims.json').write_text(json.dumps(doc))
        self.regenerate_current()
        with self.assertRaisesRegex(ValueError, 'exactly the baseline plus approved document'):
            migration.check_migration(**self.arguments)

    def test_missing_or_renamed_historical_document_is_rejected(self):
        self.old_document.rename(self.old_document.with_name('renamed-claims.json'))
        self.regenerate_current()
        with self.assertRaises(ValueError):
            migration.check_migration(**self.arguments)

    def test_historical_claim_swap_with_unchanged_count_is_rejected(self):
        doc = json.loads(self.old_document.read_text())
        doc['claims'][-1]['claim_id'] = 'replacement-unrelated'
        self.old_document.write_text(json.dumps(doc))
        self.regenerate_current()
        with self.assertRaisesRegex(ValueError, 'Preserved claim document bytes or counts differ'):
            migration.check_migration(**self.arguments)

    def test_successor_mutations_cannot_be_authenticated_by_regenerating_new_report(self):
        original = self.successor.read_bytes()
        for mutation in ('statement', 'predecessor', 'missing', 'sixth'):
            with self.subTest(mutation=mutation):
                doc = json.loads(original)
                if mutation == 'statement':
                    doc['claims'][0]['statement'] = 'Changed source meaning.'
                elif mutation == 'predecessor':
                    doc['claims'][0]['supersedes_claim_id'] = 'unrelated'
                elif mutation == 'missing':
                    doc['claims'].pop()
                else:
                    doc['claims'].append(self.fixture.claim('sixth-new', supersedes_claim_id='unrelated'))
                self.successor.write_text(json.dumps(doc))
                self.regenerate_current()
                with self.assertRaisesRegex(ValueError, 'independently reviewed bytes'):
                    migration.check_migration(**self.arguments)
        self.successor.write_bytes(original)

    def test_mutable_approval_cannot_reauthorize_changed_successor(self):
        doc = json.loads(self.successor.read_text())
        doc['claims'][0]['supersedes_claim_id'] = 'unrelated'
        self.successor.write_text(json.dumps(doc))
        approval = json.loads(self.arguments['approval'].read_text())
        approval['successor_document_sha256'] = hashlib.sha256(self.successor.read_bytes()).hexdigest()
        approval['proposed_decisions'][0]['predecessor'] = 'unrelated'
        self.arguments['approval'].write_text(json.dumps(approval))
        self.regenerate_current()
        with self.assertRaisesRegex(ValueError, 'independently pinned approval'):
            migration.check_migration(**self.arguments)

    def test_historical_reports_and_provenance_cannot_be_rebound(self):
        for key in ('historical', 'baseline', 'provenance'):
            with self.subTest(input=key):
                path = self.arguments[key]
                original = path.read_bytes()
                path.write_bytes(original + b'\n')
                with self.assertRaisesRegex(ValueError, 'independently pinned ' + key):
                    migration.check_migration(**self.arguments)
                path.write_bytes(original)

    def test_changed_frozen_reconciliation_input_is_rejected(self):
        self.arguments['reconciliation'].write_text('[ ]')
        self.regenerate_current()
        with self.assertRaisesRegex(ValueError, 'Committed workload inventory differs'):
            migration.check_migration(**self.arguments)

    def test_changed_compressed_artifacts_are_rejected_before_decompression_or_replay(self):
        path = self.arguments['artifacts']
        path.write_bytes(path.read_bytes() + b'changed-transport')
        with patch.object(migration, 'check_inventory', side_effect=AssertionError('replay started')):
            with self.assertRaisesRegex(ValueError, 'compressed artifact fingerprint'):
                migration.check_migration(**self.arguments)

    def test_forged_current_counts_credit_and_json_types_are_rejected(self):
        original = self.current.read_bytes()
        for field, value in (('recorded_claims', 10), ('new_review_credit', 1),
                             ('new_reconciliation_credit', False)):
            with self.subTest(field=field):
                report = json.loads(original)
                report['counts'][field] = value
                self.current.write_text(json.dumps(report, indent=2) + '\n')
                with self.assertRaisesRegex(ValueError, 'Committed workload inventory differs'):
                    migration.check_migration(**self.arguments)
        self.current.write_bytes(original)

    def test_membership_and_input_mutations_between_replays_are_rejected(self):
        real_check = migration.check_inventory
        old_raw = self.old_document.read_bytes()
        for target in ('membership', 'document', 'baseline', 'reference'):
            with self.subTest(target=target):
                calls = []
                changed = []

                def modify_after_current(*args, **kwargs):
                    result = real_check(*args, **kwargs)
                    calls.append(None)
                    if len(calls) == 2:
                        if target == 'membership':
                            path = self.fixture.reviews / 'late-claims.json'
                        elif target == 'document':
                            path = self.old_document
                        elif target == 'baseline':
                            path = self.arguments['baseline']
                        else:
                            path = self.fixture.root / 'pinned-identities.json'
                        changed.append((path, path.read_bytes() if path.exists() else None))
                        path.write_bytes(old_raw + b'\n')
                    return result

                with patch.object(migration, 'check_inventory', side_effect=modify_after_current):
                    with self.assertRaisesRegex(ValueError, 'inputs changed during combined check'):
                        migration.check_migration(**self.arguments)
                for path, original in changed:
                    if original is None:
                        path.unlink()
                    else:
                        path.write_bytes(original)

    def test_preserved_membership_rejects_noncanonical_duplicate_and_incorrect_entries(self):
        manifest = json.loads(self.arguments['baseline'].read_text())['inputs']['claim_documents']
        invalid = [[{**manifest[0], 'path': name}] for name in
                   ('../outside-claims.json', '/outside-claims.json', 'a\\b-claims.json')]
        invalid += [manifest * 2, [{**manifest[0], 'claims': 5}],
                    [{**manifest[0], 'claims': True}], []]
        for entries in invalid:
            with self.subTest(entries=entries):
                with self.assertRaises(ValueError):
                    inventory(self.arguments['reviews'], self.arguments['artifacts'],
                              self.arguments['reconciliation'], document_membership=entries)

    def test_symlinked_claim_or_bound_reference_is_rejected(self):
        for path in (self.old_document, self.arguments['approval']):
            with self.subTest(path=path.name):
                original = path.read_bytes()
                other = self.fixture.root / 'symlink-target.json'
                other.write_bytes(original)
                path.unlink()
                path.symlink_to(other)
                with self.assertRaisesRegex(ValueError, 'Symlink'):
                    migration.check_migration(**self.arguments)
                path.unlink()
                path.write_bytes(original)


class RealWorkloadMigration(unittest.TestCase):
    def test_cli_reproduces_both_memberships_without_changing_frozen_evidence(self):
        frozen = [ROOT / 'evidence' / name for name in (
            'claim-workload-inventory.json', 'claim-workload-current-inventory.json',
            'claim-workload-current-provenance.json',
            'claim-workload-inputs/artifacts.jsonl.gz',
            'a3-six-source-capsule-repair.json')]
        before = {path: hashlib.sha256(path.read_bytes()).hexdigest() for path in frozen}
        result = subprocess.run([
            sys.executable, '-m', 'ges.claim_workload_migration',
            '--reviews', 'evidence/source-reviews',
            '--artifacts', 'evidence/claim-workload-inputs/artifacts.jsonl.gz',
            '--reconciliation', 'evidence/provider-oidc-reconciliation.json',
            '--baseline', 'evidence/claim-workload-current-inventory.json',
            '--current', 'evidence/v02-workload-migration-20261012/current-inventory.json',
            '--historical', 'evidence/claim-workload-inventory.json',
            '--provenance', 'evidence/claim-workload-current-provenance.json',
            '--approval', 'evidence/v02-finish-20261010/claim-migration-audit.json',
        ], cwd=ROOT, capture_output=True, text=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stderr)
        observed = json.loads(result.stdout)
        self.assertEqual(observed['status'], 'MATCH')
        self.assertEqual(observed['baseline_recorded_claims'], 61936)
        self.assertEqual(observed['current_recorded_claims'], 61941)
        self.assertEqual(observed['baseline_claim_documents'], 654)
        self.assertEqual(observed['current_claim_documents'], 655)
        self.assertEqual(observed['families'], 4651)
        self.assertEqual(observed['added_claims'], 5)
        self.assertEqual(observed['reconciliation_records_present'], 474)
        self.assertEqual(observed['recorded_claims_without_reconciliation'], 61467)
        self.assertEqual(observed['new_review_credit'], 0)
        self.assertEqual(observed['new_reconciliation_credit'], 0)
        self.assertEqual(before, {path: hashlib.sha256(path.read_bytes()).hexdigest()
                                  for path in frozen})


if __name__ == '__main__':
    unittest.main()
