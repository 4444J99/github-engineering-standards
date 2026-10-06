import copy
import hashlib
import io
import json
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from tempfile import TemporaryDirectory

from ges.__main__ import main
from ges.core import ROOT
from ges.semantics import KINDS, canonical_bytes, stable_id, validate_record


def fixture(schema):
    if 'const' in schema:
        return schema['const']
    if 'enum' in schema:
        return schema['enum'][0]
    kind = schema.get('type')
    if isinstance(kind, list):
        return None
    if kind == 'object':
        return {key: fixture(value) for key, value in schema['properties'].items()}
    if kind == 'array':
        return [fixture(schema['items'])] if schema.get('minItems') else []
    if kind == 'integer':
        return 1
    pattern = schema.get('pattern', '')
    if pattern == '^[a-f0-9]{64}$':
        return 'a' * 64
    if pattern == '^[a-f0-9]{40}$':
        return 'a' * 40
    if pattern == '^[\\w.-]+/[\\w.-]+$':
        return 'example/source'
    return 'synthetic'


def record(kind):
    schema = json.loads((ROOT / 'schemas/semantics' / (kind + '.v1.json')).read_text())
    value = fixture(schema)
    value['id'] = stable_id(value)
    return value


class SemanticContracts(unittest.TestCase):
    def test_all_contracts_round_trip_and_reject_missing_unknown_fields(self):
        for kind in KINDS:
            with self.subTest(kind=kind):
                value = record(kind)
                validate_record(json.loads(canonical_bytes(value)))
                self.assertEqual(value['id'], stable_id(dict(reversed(list(value.items())))))
                changed = {**value, 'unexpected': True}
                with self.assertRaisesRegex(ValueError, 'unknown fields'):
                    validate_record(changed)
                del changed['schema']
                with self.assertRaises(ValueError):
                    validate_record(changed)
                changed = copy.deepcopy(value)
                del changed[next(key for key in changed if key not in ('schema', 'id'))]
                with self.assertRaisesRegex(ValueError, 'missing required fields'):
                    validate_record(changed)
                changed = {**value, 'id': kind + ':' + '0' * 64}
                with self.assertRaisesRegex(ValueError, 'identity differs'):
                    validate_record(changed)

    def test_occurrence_identity_binds_source_and_span(self):
        value = record('semantic-occurrence')
        original = value['id']
        value['formalization'] = 'Different proposed interpretation'
        self.assertEqual(original, stable_id(value))
        for field in ('commit', 'content_sha256', 'span_sha256'):
            changed = copy.deepcopy(value)
            changed['source'][field] = 'b' * len(changed['source'][field])
            self.assertNotEqual(original, stable_id(changed))

    def test_proposition_identity_preserves_qualifiers_and_array_order(self):
        value = record('semantic-proposition')
        original = value['id']
        value['semantic_ast']['exceptions'] = ['Only for private repositories']
        self.assertNotEqual(original, stable_id(value))
        value['semantic_ast']['preconditions'] = ['first', 'second']
        first = stable_id(value)
        value['semantic_ast']['preconditions'].reverse()
        self.assertNotEqual(first, stable_id(value))

    def test_canonical_encoding_golden_and_nonfinite_rejection(self):
        self.assertEqual(canonical_bytes({'b': 2, 'a': 1}), b'{"a":1,"b":2}')
        value = record('semantic-proposition')
        expected = hashlib.sha256(canonical_bytes(value['semantic_ast'])).hexdigest()
        self.assertEqual(value['id'], 'semantic-proposition:' + expected)
        with self.assertRaises(ValueError):
            canonical_bytes(float('nan'))

    def test_invalid_spans_digests_paths_and_review_evidence_rejected(self):
        for field, bad in (('start_line', True), ('end_line', 0),
                           ('commit', 'main'), ('content_sha256', 'bad'),
                           ('path', '../secret'), ('path', '/absolute')):
            with self.subTest(field=field, bad=bad):
                value = record('semantic-occurrence')
                value['source'][field] = bad
                value['id'] = stable_id(value)
                with self.assertRaises(ValueError):
                    validate_record(value)
        value = record('semantic-occurrence')
        value['source']['start_line'] = 2
        value['id'] = stable_id(value)
        with self.assertRaisesRegex(ValueError, 'Reversed'):
            validate_record(value)
        value = record('semantic-occurrence')
        value['review']['status'] = 'REVIEWED'
        with self.assertRaisesRegex(ValueError, 'requires identity'):
            validate_record(value)

    def test_cli_validates_jsonl_without_loading_control_catalog(self):
        with TemporaryDirectory() as temporary:
            path = Path(temporary) / 'records.jsonl'
            path.write_text('\n'.join(json.dumps(record(kind)) for kind in KINDS))
            with redirect_stdout(io.StringIO()) as output:
                self.assertEqual(main(['--catalog', 'missing', 'semantics',
                                       'validate', '--input', str(path)]), 0)
            report = json.loads(output.getvalue())
            self.assertEqual(report['records'], 5)
            self.assertFalse(report['semantic_truth_certified'])
            path.write_text(json.dumps(record('semantic-occurrence')) + '\n')
            path.write_text(path.read_text() * 2)
            with self.assertRaisesRegex(ValueError, 'Duplicate'):
                main(['semantics', 'validate', '--input', str(path)])
            path.write_text('')
            with self.assertRaisesRegex(ValueError, 'No semantic records'):
                main(['semantics', 'validate', '--input', str(path)])

    def test_reserved_commands_do_not_claim_success(self):
        for command in ('extract', 'reconcile', 'audit'):
            with self.subTest(command=command), redirect_stdout(io.StringIO()) as output:
                self.assertEqual(main(['semantics', command]), 2)
                self.assertEqual(json.loads(output.getvalue())['status'], 'UNAVAILABLE')
