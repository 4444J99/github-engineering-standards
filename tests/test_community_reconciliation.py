"""Regressions for the C0 preservation and proposed-only boundary."""
import copy
import contextlib
import io
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

from ges.core import ROOT
from ges.community_reconciliation import BASE, B0, INPUT_FILES, build, main
from ges.reconciliation import AST_FIELDS, _disposition, fingerprint, inputs


class CommunityReconciliationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for name in INPUT_FILES | {str(BASE / 'annotations.json'), str(BASE / 'input-manifest.json')}:
            destination = self.root / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / name, destination)

    def alter_annotations(self, change):
        path = self.root / BASE / 'annotations.json'
        rows = json.loads(path.read_text())
        change(rows)
        path.write_text(json.dumps(rows))
        manifest_path = self.root / BASE / 'input-manifest.json'
        manifest = json.loads(manifest_path.read_text())
        manifest['annotations_digest'] = fingerprint(rows)
        manifest_path.write_text(json.dumps(manifest))

    def test_exact_denominator_and_preservation(self):
        outputs = build(self.root)
        rows = json.loads(outputs['relationships.json'])
        original = {p['id']: p for p in (json.loads(line) for line in
                    (self.root / B0 / 'ledger/propositions.jsonl').read_text().splitlines())}
        self.assertEqual({r['proposition_id'] for r in rows}, set(original))
        self.assertEqual(len(rows), 207)
        decisions = [json.loads(line) for line in outputs['decisions.jsonl'].splitlines()]
        indexed, controls, _ = inputs(list(original.values()), [])
        for row in rows:
            self.assertEqual(row['proposition'], original[row['proposition_id']])
        for d in decisions:
            _disposition(d, indexed, controls)
            self.assertEqual(set(d['preserved_fields']), AST_FIELDS)
            self.assertFalse(d['lost_fields'])
            self.assertFalse(d['control_references'])
            self.assertEqual(d['review']['status'], 'PROPOSED')
        receipt = json.loads(outputs['receipt.json'])
        self.assertEqual(receipt['approved_decisions'], 0)
        self.assertEqual(receipt['status'], 'HOLD')

    def test_deterministic(self):
        self.assertEqual(build(self.root), build(self.root))

    def test_changed_b0_bytes_fail(self):
        path = self.root / B0 / 'ledger/propositions.jsonl'
        path.write_bytes(path.read_bytes() + b'\n')
        with self.assertRaisesRegex(ValueError, 'Changed frozen input'):
            build(self.root)

    def test_missing_proposition_fails(self):
        self.alter_annotations(lambda rows: rows.pop())
        with self.assertRaisesRegex(ValueError, 'Missing proposition disposition'):
            build(self.root)

    def test_duplicate_disposition_fails(self):
        self.alter_annotations(lambda rows: rows.append(copy.deepcopy(rows[0])))
        with self.assertRaisesRegex(ValueError, 'duplicate proposition'):
            build(self.root)

    def test_unknown_counterpart_fails(self):
        def change(rows):
            row = next(r for r in rows if r['relationships'])
            row['relationships'][0]['counterpart_ids'][0] = 'unknown'
        self.alter_annotations(change)
        with self.assertRaisesRegex(ValueError, 'Invalid counterparts'):
            build(self.root)

    def test_asymmetric_relation_fails(self):
        def change(rows):
            row = next(r for r in rows if r['relationships'])
            row['relationships'][0]['rationale'] += ' altered'
        self.alter_annotations(change)
        with self.assertRaisesRegex(ValueError, 'Asymmetric'):
            build(self.root)

    def test_cannot_promote_approval(self):
        self.alter_annotations(lambda rows: rows[0]['review'].update(
            status='REVIEWED', reviewer='invented', evidence_reference='evidence/fake.json'))
        with self.assertRaisesRegex(ValueError, 'cannot confer review'):
            build(self.root)

    def test_conflicts_remain_residual(self):
        outputs = build(self.root)
        residual = json.loads(outputs['residual.json'])
        self.assertEqual(len(residual['pending_decision_reviews']), 207)
        self.assertEqual(len(residual['conflicts']), 6)
        self.assertTrue(all(r['counterpart_ids'] for r in residual['conflicts']))

    def test_cannot_erase_conflict_by_reclassification(self):
        def change(rows):
            next(r for r in rows if r['classification'] == 'CONFLICTING')['classification'] = 'REFERENTIAL'
        self.alter_annotations(change)
        with self.assertRaisesRegex(ValueError, 'Classification does not match'):
            build(self.root)

    def test_cannot_omit_frozen_inputs(self):
        path = self.root / BASE / 'input-manifest.json'
        manifest = json.loads(path.read_text())
        manifest['files'].pop(next(iter(manifest['files'])))
        path.write_text(json.dumps(manifest))
        with self.assertRaisesRegex(ValueError, 'Incomplete B0'):
            build(self.root)

    def invoke(self, output, *options):
        with patch('sys.argv', ['c0', '--root', str(self.root), '--output',
                                str(output), *options]), contextlib.redirect_stdout(io.StringIO()):
            return main()

    def test_publication_check_no_overwrite_and_tamper(self):
        output = self.root / 'output'
        self.assertEqual(self.invoke(output), 0)
        self.assertEqual(self.invoke(output, '--check'), 0)
        self.assertEqual(self.invoke(output), 2)
        path = output / 'decisions.jsonl'
        path.write_bytes(path.read_bytes() + b'\n')
        self.assertEqual(self.invoke(output, '--check'), 2)

    def test_failure_publishes_nothing(self):
        self.alter_annotations(lambda rows: rows.pop())
        output = self.root / 'output'
        self.assertEqual(self.invoke(output), 2)
        self.assertFalse(output.exists())

    def test_extra_output_is_rejected(self):
        output = self.root / 'output'
        self.assertEqual(self.invoke(output), 0)
        (output / 'extra.json').write_text('{}')
        self.assertEqual(self.invoke(output, '--check'), 2)

    def test_symlinked_input_fails(self):
        path = self.root / B0 / 'ledger/propositions.jsonl'
        target = self.root / 'outside.jsonl'
        path.rename(target)
        path.symlink_to(target)
        with self.assertRaisesRegex(ValueError, 'Symlinked input'):
            build(self.root)


if __name__ == '__main__':
    unittest.main()
