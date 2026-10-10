"""JSON encoding equivalence does not imply expression rights clearance."""
import copy
import hashlib
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from ges import publication_use
from ges.core import digest
from test_publication_use import (bind_approvals, bind_source_inventory, byte_range,
                                  create_fixture, output_inventory)


class JsonRepresentation(unittest.TestCase):
    def approve(self, fixture):
        bind_approvals(fixture)
        if fixture['register']['schema'].endswith('.v2'):
            fixture['policy']['schema'] = 'ges.publication-use-authority-policy.v2'
            for receipt in fixture['receipts']:
                receipt['schema'] = 'ges.publication-use-receipt.v2'
                for ref in receipt['evidence'].values():
                    path = fixture['evidence_root'] / ref['path']
                    doc = json.loads(path.read_bytes())
                    doc['schema'] = 'ges.publication-use-attestation.v2'
                    path.write_text(json.dumps(doc))
                    ref['sha256'] = hashlib.sha256(path.read_bytes()).hexdigest()
        return fixture

    def representation(self, raw, pointer, token):
        start = raw.index(token)
        decoded = json.loads(token).encode()
        return {'mode': 'JSON_STRING', 'json_pointer': pointer,
                'token_start_byte': start, 'token_end_byte': start + len(token),
                'decoded_expression_sha256': hashlib.sha256(decoded).hexdigest()}

    def decode(self, raw, representation, span=None):
        fn = getattr(publication_use, 'decoded_json_expression', None)
        self.assertTrue(callable(fn), 'Missing explicit JSON representation validation')
        if span is None:
            span = byte_range(raw, representation['token_start_byte'] + 1,
                              representation['token_end_byte'] - 1)
        return fn(raw, representation, span)

    def test_escapes_unicode_and_array_pointer_return_exact_decoded_expression(self):
        raw = '{"é":0,"a/b":["hello \\"world\\"", "\\u00e9"]}'.encode()
        for pointer, token, expected in (
                ('/a~1b/0', b'"hello \\"world\\""', b'hello "world"'),
                ('/a~1b/1', b'"\\u00e9"', 'é'.encode())):
            with self.subTest(pointer=pointer):
                self.assertEqual(self.decode(raw, self.representation(raw, pointer, token)), expected)

    def test_equal_string_at_wrong_pointer_or_token_is_rejected(self):
        raw = b'{"one":"same","two":"same"}'
        rep = self.representation(raw, '/two', b'"same"')
        with self.assertRaises(ValueError):
            self.decode(raw, rep)

    def test_duplicate_keys_invalid_json_surrogates_and_trailing_garbage_rejected(self):
        cases = [b'{"a":"x","a":"x"}', b'{"a":"x",}', b'{"a":"x"} trailing',
                 b'{"a":"x","other":NaN}', b'{"a":"x","bad":"\\ud800"}',
                 b'{"a":"x","other":01}', b'{"a":"x","bad": [1,]}']
        for raw in cases:
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                self.decode(raw, self.representation(raw, '/a', b'"x"'))

    def test_nonstring_wrong_bounds_stale_digest_and_interior_subspan_rejected(self):
        raw = b'{"a":"hello","b":3}'
        rep = self.representation(raw, '/a', b'"hello"')
        for changed in ({'json_pointer': '/b'}, {'json_pointer': '/~2'},
                        {'token_start_byte': True}, {'token_end_byte': len(raw)},
                        {'decoded_expression_sha256': '0' * 64}):
            with self.subTest(changed=changed), self.assertRaises(ValueError):
                self.decode(raw, {**rep, **changed})
        with self.assertRaises(ValueError):
            self.decode(raw, rep, byte_range(raw, rep['token_start_byte'] + 2,
                                            rep['token_end_byte'] - 1))

    def json_fixture(self, root):
        fixture = create_fixture(root)
        source = b'Example "source" expression.'
        raw = b'{"text":"Example \\"source\\" expression.","credit":"synthetic"}'
        source_path = fixture['source_root'] / 'source.txt'
        source_path.write_bytes(source)
        output_path = fixture['output_root'] / 'release.txt'
        output_path.write_bytes(raw)
        artifact = fixture['artifacts'][0]
        artifact.update(sha256=hashlib.sha256(source).hexdigest(), size=len(source),
                        git_blob_sha=hashlib.sha1(b'blob ' + str(len(source)).encode() + b'\0' + source).hexdigest())
        fixture['manifest']['outputs'] = output_inventory(fixture['output_root'])
        register = fixture['register']
        register['schema'] = 'ges.publication-use-register.v2'
        use = register['uses'][0]
        token = b'"Example \\"source\\" expression."'  # allow-secret: synthetic JSON syntax, not a credential
        rep = self.representation(raw, '/text', token)
        use.update(source={k: artifact[k] for k in use['source']},
                   source_range=byte_range(source), representation=rep,
                   output_range=byte_range(raw, rep['token_start_byte'] + 1, rep['token_end_byte'] - 1),
                   attributions=[{'output_path': 'release.txt', 'output_range': byte_range(raw, raw.index(b'"credit"'))}])
        register['source_evidence'][0]['sha256'] = artifact['sha256']
        return self.approve(bind_source_inventory(fixture))

    def test_v2_copy_compares_decoded_expression_but_keeps_rights_gates(self):
        with TemporaryDirectory() as temporary:
            fixture = self.json_fixture(Path(temporary))
            result = publication_use.publication_accounting(**fixture)
            self.assertTrue(result['exact_use_clearance'])
            self.assertEqual(result['representation_comparisons'], [
                {'use_id': 'use:one', 'mode': 'JSON_STRING',
                 'raw_equal': False, 'decoded_equal': True}])
            fixture['receipts'] = []
            fixture['policy'] = {}
            self.assertIsNone(publication_use.publication_accounting(**fixture)['exact_use_clearance'])

    def test_v1_raw_mismatch_and_v2_substantive_change_still_rejected(self):
        with TemporaryDirectory() as temporary:
            fixture = self.json_fixture(Path(temporary))
            fixture['register']['schema'] = 'ges.publication-use-register.v1'
            fixture['register']['uses'][0].pop('representation')
            self.approve(fixture)
            with self.assertRaisesRegex(ValueError, 'identical source/output'):
                publication_use.publication_accounting(**fixture)
        with TemporaryDirectory() as temporary:
            fixture = self.json_fixture(Path(temporary))
            raw = (fixture['output_root'] / 'release.txt').read_bytes().replace(b'Example', b'Changed')
            (fixture['output_root'] / 'release.txt').write_bytes(raw)
            fixture['manifest']['outputs'] = output_inventory(fixture['output_root'])
            use = fixture['register']['uses'][0]
            use['representation'] = self.representation(raw, '/text', b'"Changed \\"source\\" expression."')
            use['output_range'] = byte_range(raw, use['representation']['token_start_byte'] + 1,
                                              use['representation']['token_end_byte'] - 1)
            self.approve(fixture)
            with self.assertRaisesRegex(ValueError, 'decoded expression'):
                publication_use.publication_accounting(**fixture)

    def test_v2_raw_mode_preserves_legacy_comparison(self):
        with TemporaryDirectory() as temporary:
            fixture = create_fixture(Path(temporary))
            fixture['register']['schema'] = 'ges.publication-use-register.v2'
            fixture['register']['uses'][0]['representation'] = {'mode': 'RAW'}
            self.approve(fixture)
            self.assertTrue(publication_use.publication_accounting(**fixture)['exact_use_clearance'])

    def test_v1_authority_cannot_be_reused_for_v2_register(self):
        with TemporaryDirectory() as temporary:
            fixture = self.json_fixture(Path(temporary))
            bind_approvals(fixture)
            with self.assertRaisesRegex(ValueError, 'authority'):
                publication_use.publication_accounting(**fixture)
