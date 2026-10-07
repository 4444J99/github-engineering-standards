import gzip
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from ges.claim_workload import inventory
from ges.source_tables import provider_facts, query_facts, validate

PROVIDER = 'src/secret-scanning/data/pattern-docs/fpt/public-docs.yml'
QUERY = 'data/reusables/code-scanning/codeql-query-tables/actions.md'
YAML = '- provider: Example\n  supportedSecret: Example token\n  secretType: a<br>b</br>\n  isPublic: false\n'
HEADER = '| Query name | Related CWEs | Default | Extended | {% data variables.copilot.copilot_autofix_short %} |'
TABLE = ('{% rowheaders %}\n\n' + HEADER + '\n| --- | --- | --- | --- | --- |\n'
         '| [Example](https://codeql.github.com/codeql-query-help/actions/example/) | 021 | '
         '{% octicon "check" aria-label="Included" %} | '
         '{% octicon "x" aria-label="Not included" %} | '
         '{% octicon "x" aria-label="Not included" %} |\n\n{% endrowheaders %}\n')


class SourceTables(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.reviews = self.root / 'reviews'
        self.reviews.mkdir()
        self.artifacts = self.root / 'artifacts.jsonl'
        self.receipts = self.root / 'receipts.json'
        self.workload = self.root / 'workload.json'
        self.sources = self.root / 'sources.gz'
        self.lock = self.root / 'lock.json'
        self.commit = 'a' * 40
        self.rows = []
        self.claims = []
        self.add_source(PROVIDER, YAML)
        self.add_source(QUERY, TABLE)
        self.claims.append({
            'claim_id': 'provider', 'source': 'github/docs', 'commit': self.commit,
            'path': PROVIDER, 'start_line': 4, 'end_line': 4,
            'statement': 'For ab, this free/pro/team dataset declares the literal public-support flag false.',
            'context': {'provider': 'Example', 'raw_credential_identifier': 'a<br>b</br>',
                        'credential_identifier': 'ab', 'credential_label': 'Example token',
                        'product_version': 'fpt pinned dataset', 'entry_ordinal': 1,
                        'definition_start_line': 1, 'definition_end_line': 4,
                        'source_field': 'isPublic'},
        })
        url = 'https://codeql.github.com/codeql-query-help/actions/example/'
        base = {'source': 'github/docs', 'commit': self.commit, 'path': QUERY,
                'start_line': 5, 'end_line': 5, 'query_occurrence': QUERY + '#L5',
                'query_help_identity': url}
        self.claims += [
            dict(base, claim_id='label', statement='The row identified by example has display label "Example".'),
            dict(base, claim_id='link', statement='That query row links to ' + url + '.'),
            dict(base, claim_id='cwe', cwe_identity='021',
                 statement="The example row associates related CWE identity 021; the source's digit spelling is preserved."),
        ]
        for column, label, icon in [('Default', 'Included', 'check'),
                                    ('Extended', 'Not included', 'x'),
                                    ('Autofix', 'Not included', 'x')]:
            self.claims.append(dict(base, claim_id=column, column=column, cell_label=label,
                                    cell_icon=icon,
                                    statement=f'For example, the {column} column records {label}.'))

    def add_source(self, path, content):
        self.rows.append({'source': 'github/docs', 'commit': self.commit, 'path': path,
                          'content': content, 'sha256': hashlib.sha256(content.encode()).hexdigest(),
                          'artifact_id': path})

    def write(self):
        (self.reviews / 'one-claims.json').write_text(json.dumps({'claims': self.claims}))
        self.artifacts.write_text(''.join(json.dumps(r) + '\n' for r in self.rows))
        self.receipts.write_text('[]')
        self.lock.write_text(json.dumps({'sources': [{'repository': 'github/docs', 'commit': self.commit}]}))
        self.sources.write_bytes(gzip.compress(''.join(json.dumps(r) + '\n' for r in self.rows).encode()))
        self.workload.write_text(json.dumps(inventory(self.reviews, self.artifacts, self.receipts)))

    def check(self):
        self.write()
        return validate(self.reviews, self.artifacts, self.receipts,
                        self.workload, self.sources, self.lock)

    def test_whole_table_scope_matches_and_absence_stays_distinct(self):
        result = self.check()
        self.assertEqual(result['counts']['mechanically_matched_claims'], 7)
        self.assertEqual(result['status'], 'LITERAL_SOURCE_MATCH')
        self.assertEqual(result['counts']['reconciliation_credit'], 0)
        provider = next(r for r in result['source_tables'] if r['path'] == PROVIDER)
        self.assertEqual(provider['absent_fields'], 6)

    def test_wrong_claim_value_is_a_finding(self):
        self.claims[0]['statement'] = self.claims[0]['statement'].replace('false', 'true')
        result = self.check()
        self.assertEqual(result['status'], 'FINDINGS')
        self.assertEqual(result['findings'][0]['claim_id'], 'provider')

    def test_missing_source_fact_claim_is_not_completion(self):
        self.claims = [c for c in self.claims if c['claim_id'] != 'cwe']
        result = self.check()
        self.assertTrue(any(r['finding'] == 'SOURCE_FACT_WITHOUT_CLAIM' for r in result['findings']))

    def test_duplicate_fact_identity_is_not_extra_credit(self):
        self.claims.append(dict(self.claims[0], claim_id='duplicate'))
        result = self.check()
        self.assertTrue(any(r['finding'] == 'DUPLICATE_FACT_SUBJECT' for r in result['findings']))

    def test_cwe_leading_zero_is_required(self):
        self.claims[3]['cwe_identity'] = '21'
        self.assertEqual(self.check()['status'], 'FINDINGS')

    def test_raw_identifier_and_spans_must_match(self):
        self.claims[0]['context']['raw_credential_identifier'] = 'ab'
        self.assertEqual(self.check()['status'], 'FINDINGS')
        self.claims[0]['context']['raw_credential_identifier'] = 'a<br>b</br>'
        self.claims[0]['context']['definition_end_line'] = 5
        self.assertEqual(self.check()['status'], 'FINDINGS')

    def test_swapped_query_columns_rejected(self):
        with self.assertRaisesRegex(ValueError, 'header'):
            query_facts(TABLE.replace('Default | Extended', 'Extended | Default'), QUERY)

    def test_unknown_icon_or_data_shape_rejected(self):
        with self.assertRaises(ValueError):
            query_facts(TABLE.replace('"check"', '"x"'), QUERY)
        with self.assertRaises(ValueError):
            query_facts(TABLE.replace('| [Example]', '| malformed [Example]'), QUERY)

    def test_invalid_wrapper_separator_rejected(self):
        with self.assertRaises(ValueError):
            query_facts(TABLE.replace('{% rowheaders %}', 'changed'), QUERY)
        with self.assertRaises(ValueError):
            query_facts(TABLE.replace('| --- | --- | --- | --- | --- |', '| --- |'), QUERY)

    def test_condition_is_preserved_and_not_coerced(self):
        conditional = "'{% ifversion ghes %}false{% else %}true{% endif %}'"
        text = YAML.replace('isPublic: false', 'hasValidityCheck: ' + conditional)
        facts, stats = provider_facts(text, PROVIDER)
        self.assertEqual(stats['conditional_fields'], 1)
        self.assertEqual(facts[(1, 'hasValidityCheck')]['value'], conditional.strip("'"))
        self.assertIn('rather than coerced', facts[(1, 'hasValidityCheck')]['statement'])
        with self.assertRaises(ValueError):
            provider_facts(text.replace('ifversion ghes', 'ifversion unknown'), PROVIDER)

    def test_duplicate_yaml_keys_and_string_booleans_rejected(self):
        with self.assertRaises(ValueError):
            provider_facts(YAML + '  isPublic: true\n', PROVIDER)
        with self.assertRaises(ValueError):
            provider_facts(YAML.replace('false', '"false"'), PROVIDER)

    def test_snapshot_content_and_pin_change_rejected(self):
        self.write()
        bad = [dict(r, content=r['content'] + 'tamper') for r in self.rows]
        self.sources.write_bytes(gzip.compress(''.join(json.dumps(r) + '\n' for r in bad).encode()))
        with self.assertRaisesRegex(ValueError, 'digest'):
            validate(self.reviews, self.artifacts, self.receipts, self.workload, self.sources, self.lock)
        self.write()
        self.lock.write_text(json.dumps({'sources': [{'repository': 'github/docs', 'commit': 'b' * 40}]}))
        with self.assertRaisesRegex(ValueError, 'pin'):
            validate(self.reviews, self.artifacts, self.receipts, self.workload, self.sources, self.lock)

    def test_empty_typed_scope_rejected(self):
        self.claims = [{'claim_id': 'narrative', 'source': 'github/docs', 'commit': self.commit,
                        'path': PROVIDER, 'start_line': 1, 'end_line': 1, 'statement': 'Narrative.'}]
        self.write()
        with self.assertRaisesRegex(ValueError, 'Empty'):
            validate(self.reviews, self.artifacts, self.receipts, self.workload, self.sources, self.lock)

    def test_transient_claim_document_change_rejected(self):
        self.write()
        target = self.reviews / 'one-claims.json'
        original = Path.read_bytes
        calls = 0

        def altered(path):
            nonlocal calls
            if path == target:
                calls += 1
                if calls == 3:
                    return json.dumps({'claims': self.claims[1:]}).encode()
            return original(path)

        with patch.object(Path, 'read_bytes', altered), self.assertRaisesRegex(ValueError, 'Claim document changed'):
            validate(self.reviews, self.artifacts, self.receipts,
                     self.workload, self.sources, self.lock)

    def test_transient_artifact_inventory_change_rejected(self):
        self.write()
        original = Path.read_bytes
        calls = 0

        def altered(path):
            nonlocal calls
            if path == self.artifacts:
                calls += 1
                if calls == 3:
                    return b'{}\n'
            return original(path)

        with patch.object(Path, 'read_bytes', altered), self.assertRaisesRegex(ValueError, 'Artifact inventory changed'):
            validate(self.reviews, self.artifacts, self.receipts,
                     self.workload, self.sources, self.lock)
