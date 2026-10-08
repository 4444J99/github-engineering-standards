"""Rebound metadata hashes cannot authenticate payloads or a reduced source set."""
import gzip
import hashlib
import json
import unittest
from unittest.mock import patch

import test_claim_workload as fixtures
from ges.claim_workload import _metadata_records, check_inventory
from ges.core import ROOT, digest
from ges.pinned_sources import inventory_digest


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


class WorkloadMetadataIntegrity(unittest.TestCase):
    def setUp(self):
        self.fixture = fixtures.ClaimWorkload()
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.fixture.add('claimed.md', [self.fixture.claim('claim-a')])

    def rebind(self, current, compressed, provenance, *, raw=None, container=None):
        """Rebind mutable data exactly as an attacker could; never repin authority."""
        fixture = self.fixture
        raw = (''.join(json.dumps(row) + '\n' for row in fixture.records).encode()
               if raw is None else raw)
        fixture.artifacts.write_bytes(raw)
        compressed.write_bytes(gzip.compress(raw, mtime=0) if container is None else container)
        current.write_text(json.dumps(fixture.run_inventory(), indent=2) + '\n')
        record = json.loads(provenance.read_text())
        record['bindings'].update(current_report_sha256=sha(current.read_bytes()),
                                  artifact_inventory_sha256=sha(raw),
                                  compressed_artifact_inventory_sha256=sha(compressed.read_bytes()))
        record['metadata_projection'].update(
            artifact_rows=len(fixture.records), uncompressed_bytes=len(raw),
            compressed_bytes=compressed.stat().st_size,
            fields=sorted({key for row in fixture.records for key in row}))
        provenance.write_text(json.dumps(record))

    def check(self, historical, current, compressed, provenance):
        fixture = self.fixture
        return check_inventory(fixture.reviews, compressed, fixture.receipts, current,
                               historical=historical, provenance=provenance)

    def test_allowed_url_payload_is_rejected_even_after_every_mutable_hash_is_rebound(self):
        files = self.fixture.forward_baseline()
        _, current, compressed, provenance = files
        locator = self.fixture.records[0]['url']
        for payload in ('SYNTHETIC unlicensed source text',
                        locator + '?credential=SYNTHETIC_ONLY',
                        locator + '#SYNTHETIC_ONLY', {'body': 'SYNTHETIC_ONLY'}):
            with self.subTest(payload_type=type(payload).__name__):
                self.fixture.records[0]['url'] = payload
                self.rebind(current, compressed, provenance)
                with self.assertRaisesRegex(ValueError, 'canonical pinned locator'):
                    self.check(*files)

    def test_duplicate_field_cannot_hide_a_discarded_string_payload(self):
        files = self.fixture.forward_baseline()
        _, current, compressed, provenance = files
        row = json.dumps(self.fixture.records[0])
        raw = ('{"url": "SYNTHETIC discarded upstream expression", ' + row[1:] + '\n').encode()
        self.assertEqual(json.loads(raw), self.fixture.records[0])
        self.rebind(current, compressed, provenance, raw=raw)
        with self.assertRaisesRegex(ValueError, 'Duplicate metadata object field'):
            self.check(*files)

    def test_gzip_header_payloads_and_extra_members_cannot_bypass_row_checks(self):
        files = self.fixture.forward_baseline()
        _, current, compressed, provenance = files
        raw = self.fixture.artifacts.read_bytes()
        base = gzip.compress(raw, mtime=0)
        payload = b'SYNTHETIC upstream expression in transport metadata'
        transports = {
            'filename': base[:3] + b'\x08' + base[4:10] + payload + b'\0' + base[10:],
            'comment': base[:3] + b'\x10' + base[4:10] + payload + b'\0' + base[10:],
            'extra': base[:3] + b'\x04' + base[4:10] + len(payload).to_bytes(2, 'little') + payload + base[10:],
            'second_member': base + gzip.compress(b'', mtime=0),
        }
        for label, container in transports.items():
            with self.subTest(label=label):
                self.assertEqual(gzip.decompress(container), raw)
                self.rebind(current, compressed, provenance, raw=raw, container=container)
                with self.assertRaisesRegex(ValueError, 'metadata gzip'):
                    self.check(*files)

    def test_unreferenced_artifact_cannot_be_removed_or_authenticated_by_rewritten_reference(self):
        fixture = self.fixture
        unused = {**fixture.records[0], 'path': 'unreferenced.md',
                  'artifact_id': digest(['owner/source', 'a' * 40, 'unreferenced.md'])[:24],
                  'url': 'https://github.com/owner/source/blob/' + 'a' * 40 + '/unreferenced.md'}
        fixture.records.append(unused)
        fixture.artifacts.write_text(''.join(json.dumps(row) + '\n' for row in fixture.records))
        files = fixture.forward_baseline()
        _, current, compressed, provenance = files
        fixture.records.pop()
        self.rebind(current, compressed, provenance)
        with self.assertRaisesRegex(ValueError, 'complete pinned source counts'):
            self.check(*files)
        record = json.loads(provenance.read_text())
        reference = fixture.root / record['source_identity_reference']['path']
        authority = json.loads(reference.read_text())
        forged = inventory_digest(fixture.records)
        authority['inventory_identity_digests']['owner/source'] = forged
        authority['source_trees']['owner/source'].update(artifacts=1, inventory_digest=forged)
        reference.write_text(json.dumps(authority))
        record['source_identity_reference']['sha256'] = sha(reference.read_bytes())
        record['source_identity_digests']['owner/source'] = forged
        provenance.write_text(json.dumps(record))
        with self.assertRaisesRegex(ValueError, 'independently pinned A3 fingerprint'):
            self.check(*files)

    def test_metadata_values_have_closed_types_ranges_and_canonical_forms(self):
        valid = self.fixture.records[0]
        self.assertEqual(_metadata_records((json.dumps(valid) + '\n').encode()), [valid])
        invalid = [
            ('source', 'owner/source/SYNTHETIC'), ('commit', 'a' * 39),
            ('path', '../outside.md'), ('path', './claimed.md'), ('path', 'a\\b'),
            ('path', 'a\nbody.md'), ('artifact_id', 'SYNTHETIC'),
            ('sha256', 'B' * 64), ('git_blob_sha', 'SYNTHETIC'),
            ('kind', 'SYNTHETIC'), ('kind', {}),
            ('retrieval_status', 'SYNTHETIC'), ('review_status', 'ACCEPTED'),
            ('proposed_disposition', 'SYNTHETIC upstream body'),
            ('proposed_disposition', ['documentation']),
            ('size', True), ('size', -1), ('size', 200_000_001),
            ('candidate_count', True), ('candidate_count', 1.5),
            ('candidate_count', -1), ('candidate_count', valid['size'] + 1),
            ('retrieved_at', '2026-01-01'), ('retrieved_at', 'SYNTHETIC'),
            ('retrieved_at', '2026-02-30T00:00:00+00:00'),
            ('retrieved_at', '2999-01-01T00:00:00+00:00'),
        ]
        for field, value in invalid:
            with self.subTest(field=field, value_type=type(value).__name__):
                record = {**valid, field: value}
                with self.assertRaises(ValueError):
                    _metadata_records((json.dumps(record) + '\n').encode())
        for omitted in valid:
            with self.subTest(omitted=omitted):
                record = {key: value for key, value in valid.items() if key != omitted}
                with self.assertRaisesRegex(ValueError, 'missing or non-metadata fields'):
                    _metadata_records((json.dumps(record) + '\n').encode())

    def test_canonical_metadata_paths_preserve_spaces_and_url_encoding(self):
        record = {**self.fixture.records[0], 'path': 'folder/a file#1.md',
                  'artifact_id': digest(['owner/source', 'a' * 40, 'folder/a file#1.md'])[:24],
                  'url': 'https://github.com/owner/source/blob/' + 'a' * 40 + '/folder/a%20file%231.md'}
        self.assertEqual(_metadata_records((json.dumps(record) + '\n').encode()), [record])

    def test_changed_source_pin_is_rejected_against_the_unchanged_independent_anchor(self):
        files = self.fixture.forward_baseline()
        _, current, compressed, provenance = files
        fixture = self.fixture
        row = fixture.records[0]
        row['commit'] = 'e' * 40
        row['artifact_id'] = digest([row['source'], row['commit'], row['path']])[:24]
        row['url'] = 'https://github.com/owner/source/blob/' + 'e' * 40 + '/claimed.md'
        # Exercise source authority independently of the earlier claim-binding check.
        from ges.claim_workload import _check_provenance
        raw = (json.dumps(row) + '\n').encode()
        compressed.write_bytes(gzip.compress(raw, mtime=0))
        record = json.loads(provenance.read_text())
        record['bindings'].update(artifact_inventory_sha256=sha(raw),
                                  compressed_artifact_inventory_sha256=sha(compressed.read_bytes()))
        record['metadata_projection'].update(uncompressed_bytes=len(raw),
                                               compressed_bytes=compressed.stat().st_size)
        provenance.write_text(json.dumps(record))
        with self.assertRaisesRegex(ValueError, 'complete pinned source counts or commits'):
            _check_provenance(provenance, compressed, current.read_bytes(), files[0].read_bytes())

    def test_reference_symlinks_and_mid_validation_changes_are_rejected(self):
        files = self.fixture.forward_baseline()
        _, _, _, provenance = files
        record = json.loads(provenance.read_text())
        reference = self.fixture.root / record['source_identity_reference']['path']
        original = reference.read_bytes()
        other = self.fixture.root / 'other-reference.json'
        other.write_bytes(original)
        reference.unlink()
        reference.symlink_to(other)
        with self.assertRaises(ValueError):
            self.check(*files)
        reference.unlink()
        reference.write_bytes(original)

        def change_after_metadata_read(raw):
            records = _metadata_records(raw)
            reference.write_bytes(original + b'\n')
            return records

        with patch('ges.claim_workload._metadata_records', side_effect=change_after_metadata_read):
            with self.assertRaisesRegex(ValueError, 'inputs changed during check'):
                self.check(*files)

    def test_real_current_baseline_and_independent_a3_bytes_reproduce_unchanged(self):
        evidence = ROOT / 'evidence'
        artifacts = evidence / 'claim-workload-inputs/artifacts.jsonl.gz'
        current = evidence / 'claim-workload-current-inventory.json'
        historical = evidence / 'claim-workload-inventory.json'
        provenance = evidence / 'claim-workload-current-provenance.json'
        authority = evidence / 'a3-six-source-capsule-repair.json'
        before = {path: sha(path.read_bytes()) for path in
                  (artifacts, current, historical, provenance, authority)}
        result = check_inventory(evidence / 'source-reviews', artifacts,
                                 evidence / 'provider-oidc-reconciliation.json', current,
                                 historical=historical, provenance=provenance)
        self.assertEqual(result['counts']['recorded_claims'], 61936)
        self.assertEqual(result['counts']['claim_documents'], 654)
        self.assertEqual(len(result['families']), 4651)
        self.assertEqual(before, {path: sha(path.read_bytes()) for path in before})


if __name__ == '__main__':
    unittest.main()
