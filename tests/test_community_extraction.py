import copy
import gzip
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from ges.community_extraction import (compile_ledger, extract, sha,
                                      validate_interpretation, template_parameters,
                                      characteristic_parameters)
from ges.core import ROOT, digest
from ges.semantics import canonical_bytes, validate_record


class CommunityExtraction(unittest.TestCase):
    def setUp(self):
        self.temporary = TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.manifest = {'schema': 'ges.b0-input-manifest.v1', 'sources': [],
                         'exclusions': ['controls', 'other sources']}
        self.annotations = {'schema': 'ges.b0-annotations.v1', 'artifacts': []}
        pins = json.loads((ROOT / 'sources/sources.lock.json').read_bytes())['sources']
        for pin in pins:
            repo = pin['repository']
            if repo not in {'tmcw/github-best-practices', 'jlcanovas/gh-best-practices-template',
                            'atapas/model-repo'}:
                continue
            inventory = []
            rows = []
            frozen = []
            for number in range(pin['artifacts']):
                path = f'{number}.md'
                raw = b'# Synthetic\r\nIllustrative statement.\r\n'
                import hashlib
                blob = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
                row = {'source': repo, 'commit': pin['commit'], 'path': path,
                       'sha256': sha(raw), 'git_blob_sha': blob, 'content': raw.decode()}
                rows.append(row)
                inventory.append({k: v for k, v in row.items() if k != 'content'})
                frozen.append({'path': path, 'content_sha256': sha(raw), 'git_blob_sha': blob,
                               'artifact_id': digest([repo, pin['commit'], path])[:24], 'line_count': 2})
                ast = {'subject': 'synthetic participant', 'action': 'consider', 'object': 'example',
                       'modality': 'MAY', 'polarity': 'POSITIVE', 'scope': [repo, path],
                       'preconditions': [], 'qualifiers': [], 'exceptions': [],
                       'consequences': [], 'parameters': []}
                self.annotations['artifacts'].append({'repository': repo, 'path': path,
                    'context': ['synthetic'], 'spans': [
                        {'kind': 'NONCLAIM', 'start_line': 1, 'end_line': 1, 'reason': 'Heading'},
                        {'kind': 'OCCURRENCE', 'start_line': 2, 'end_line': 2,
                         'semantic_kind': 'EXAMPLE', 'propositions': [{'semantic_ast': ast,
                         'formalization': 'Synthetic illustration.', 'ambiguities': []}]}]})
            name = repo.replace('/', '__')
            raw_inventory = canonical_bytes(inventory)
            snapshot = gzip.compress(b''.join(canonical_bytes(r) + b'\n' for r in rows), mtime=0)
            (self.root / (name + '.inventory.json')).write_bytes(raw_inventory)
            (self.root / (name + '.text.jsonl.gz')).write_bytes(snapshot)
            self.manifest['sources'].append({'repository': repo, 'commit': pin['commit'],
                'archive_sha256': pin['archive_sha256'], 'artifacts': frozen,
                'inventory_sha256': sha(raw_inventory), 'snapshot_sha256': sha(snapshot)})
        self.bind()

    def bind(self):
        self.manifest['annotations_sha256'] = sha(canonical_bytes(self.annotations))

    def compile(self):
        return compile_ledger(self.manifest, self.annotations, self.root)

    def test_deterministic_source_bound_records_never_assert_review(self):
        files = self.compile()
        self.assertEqual(files, self.compile())
        for name in ('occurrences.jsonl', 'propositions.jsonl'):
            for line in files[name].splitlines():
                record = json.loads(line)
                validate_record(record)
                review = record.get('review', record.get('primary_review'))
                self.assertEqual(review['status'], 'PROPOSED')
                self.assertIsNone(review['reviewer'])
        receipt = json.loads(files['receipt.json'])
        self.assertEqual(receipt['status'], 'HOLD')
        self.assertEqual(receipt['artifact_count'], 22)
        self.assertEqual(receipt['reviewed_proposition_count'], 0)
        self.assertFalse(receipt['semantic_truth_certified'])
        occurrence = json.loads(files['occurrences.jsonl'].splitlines()[0])
        self.assertEqual(occurrence['source']['span_sha256'], sha(b'Illustrative statement.\r\n'))
        residual = json.loads(files['residual.json'])
        self.assertEqual(len(residual['primary_review_pending']), 22)

    def test_missing_artifact_or_line_and_overlap_fail_closed(self):
        original = copy.deepcopy(self.annotations)
        for mutation in ('artifact', 'line', 'overlap', 'reason'):
            with self.subTest(mutation=mutation):
                self.annotations = copy.deepcopy(original)
                if mutation == 'artifact':
                    self.annotations['artifacts'].pop()
                elif mutation == 'line':
                    self.annotations['artifacts'][0]['spans'].pop(0)
                elif mutation == 'reason':
                    self.annotations['artifacts'][0]['spans'][0]['reason'] = ' '
                else:
                    self.annotations['artifacts'][0]['spans'].append(
                        copy.deepcopy(self.annotations['artifacts'][0]['spans'][0]))
                self.bind()
                with self.assertRaises(ValueError):
                    self.compile()

    def test_stale_annotations_and_snapshot_fail_closed(self):
        self.annotations['artifacts'][0]['context'].append('unbound edit')
        with self.assertRaisesRegex(ValueError, 'Stale annotations'):
            self.compile()
        self.bind()
        snapshot = next(self.root.glob('*.gz'))
        snapshot.write_bytes(snapshot.read_bytes() + b'changed')
        with self.assertRaisesRegex(ValueError, 'Stale snapshot'):
            self.compile()

    def test_source_refresh_or_reduced_denominator_is_rejected(self):
        self.manifest['sources'][0]['commit'] = '0' * 40
        with self.assertRaisesRegex(ValueError, 'pinned source scope'):
            self.compile()
        self.manifest['sources'][0]['commit'] = json.loads(
            (ROOT / 'sources/sources.lock.json').read_bytes())['sources'][1]['commit']
        self.manifest['sources'][0]['artifacts'].pop()
        with self.assertRaisesRegex(ValueError, 'pinned source scope'):
            self.compile()

    def test_unknown_or_duplicate_artifact_identity_is_rejected(self):
        self.manifest['sources'][0]['artifacts'][0]['artifact_id'] = '0' * 24
        with self.assertRaisesRegex(ValueError, 'Artifact identity'):
            self.compile()

    def test_invalid_ast_and_cap_are_rejected(self):
        entry = self.annotations['artifacts'][0]['spans'][1]
        original = copy.deepcopy(entry['propositions'][0])
        entry['propositions'][0]['semantic_ast']['modality'] = 'ACCEPTED'
        self.bind()
        with self.assertRaises(ValueError):
            self.compile()
        entry['propositions'] = []
        for number in range(251):
            prop = copy.deepcopy(original)
            prop['semantic_ast']['object'] = f'synthetic {number}'
            entry['propositions'].append(prop)
        self.bind()
        with self.assertRaisesRegex(ValueError, 'cap exceeded'):
            self.compile()

    def test_atomic_publication_check_and_no_overwrite(self):
        manifest = self.root / 'manifest.json'
        annotations = self.root / 'annotations.json'
        manifest.write_bytes(canonical_bytes(self.manifest))
        annotations.write_bytes(canonical_bytes(self.annotations))
        output = self.root / 'ledger'
        extract(manifest, annotations, self.root, output)
        extract(manifest, annotations, self.root, output, check=True)
        with self.assertRaisesRegex(ValueError, 'already exists'):
            extract(manifest, annotations, self.root, output)
        (output / 'propositions.jsonl').write_text('tampered\n')
        with self.assertRaisesRegex(ValueError, 'Output bytes differ'):
            extract(manifest, annotations, self.root, output, check=True)

    def test_failure_publishes_no_output(self):
        self.annotations['artifacts'].pop()
        self.bind()
        manifest = self.root / 'manifest.json'
        annotations = self.root / 'annotations.json'
        manifest.write_bytes(canonical_bytes(self.manifest))
        annotations.write_bytes(canonical_bytes(self.annotations))
        output = self.root / 'ledger'
        with self.assertRaises(ValueError):
            extract(manifest, annotations, self.root, output)
        self.assertFalse(output.exists())

    def test_committed_ledger_identities_and_pending_reviews(self):
        ledger = ROOT / 'evidence/semantics/b0/ledger'
        ids = set()
        for name in ('occurrences.jsonl', 'propositions.jsonl'):
            for line in (ledger / name).read_text().splitlines():
                record = json.loads(line)
                validate_record(record)
                self.assertNotIn(record['id'], ids)
                ids.add(record['id'])
        receipt = json.loads((ledger / 'receipt.json').read_bytes())
        for name, expected in receipt['outputs_sha256'].items():
            self.assertEqual(sha((ledger / name).read_bytes()), expected)
        manifest = json.loads((ledger.parent / 'input-manifest.v3.json').read_bytes())
        self.assertEqual(sha(canonical_bytes(manifest)), receipt['input_manifest_sha256'])

    def test_prohibition_is_on_underlying_action_not_avoidance(self):
        ast = copy.deepcopy(self.annotations['artifacts'][0]['spans'][1]['propositions'][0]['semantic_ast'])
        ast.update(modality='PROHIBITED', polarity='NEGATIVE', action='avoid', object='harassment')
        with self.assertRaisesRegex(ValueError, 'Prohibited avoidance'):
            validate_interpretation(ast, 'Harassment is unacceptable.')
        ast['action'] = 'engage in'
        validate_interpretation(ast, 'Harassment is unacceptable.')
        ast['polarity'] = 'POSITIVE'
        with self.assertRaisesRegex(ValueError, 'negate its underlying action'):
            validate_interpretation(ast, 'Harassment is unacceptable.')

    def test_nonempty_template_binding_cannot_hide_in_nonclaim_span(self):
        record = {'path': '.github/ISSUE_TEMPLATE/question.md',
                  'content': '---\nname: Question\nabout: Ask something\nlabels: question\nassignees: ""\n---\n'}
        self.assertEqual(template_parameters(record), ['frontmatter.name=Question',
                         'frontmatter.about=Ask something', 'frontmatter.labels=question'])
        art = self.annotations['artifacts'][0]
        source = self.manifest['sources'][0]
        original_path = art['path']
        inventory_path = self.root / (source['repository'].replace('/', '__') + '.inventory.json')
        snapshot_path = self.root / (source['repository'].replace('/', '__') + '.text.jsonl.gz')
        inventory = json.loads(inventory_path.read_bytes())
        rows = [json.loads(s) for s in gzip.decompress(snapshot_path.read_bytes()).splitlines()]
        import hashlib
        raw = record['content'].encode()
        blob = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
        for row in inventory + rows:
            if row['path'] == original_path:
                row.update(path=record['path'], sha256=sha(raw), git_blob_sha=blob)
                if 'content' in row:
                    row['content'] = record['content']
        art['path'] = record['path']
        source['artifacts'][0].update(path=record['path'], content_sha256=sha(raw),
            git_blob_sha=blob, line_count=len(raw.splitlines()),
            artifact_id=digest([source['repository'], source['commit'], record['path']])[:24])
        inventory_path.write_bytes(canonical_bytes(inventory))
        snapshot_path.write_bytes(gzip.compress(b''.join(canonical_bytes(r) + b'\n' for r in rows), mtime=0))
        source['inventory_sha256'] = sha(inventory_path.read_bytes())
        source['snapshot_sha256'] = sha(snapshot_path.read_bytes())
        original = copy.deepcopy(art['spans'][1]['propositions'][0])
        art['spans'] = [{'kind': 'NONCLAIM', 'start_line': 1, 'end_line': 6, 'reason': 'Metadata'}]
        self.bind()
        with self.assertRaisesRegex(ValueError, 'Operative issue-template binding'):
            self.compile()
        original['semantic_ast'].update(parameters=template_parameters(record),
            scope=[source['repository'], record['path']])
        art['spans'] = [{'kind': 'OCCURRENCE', 'start_line': 1, 'end_line': 6,
            'semantic_kind': 'IMPLEMENTATION', 'propositions': [original]}]
        self.bind()
        self.compile()

    def test_complete_characteristic_lists_are_source_bound(self):
        span = 'We pledge participation regardless of age, caste, or sexual identity and orientation.'
        ast = copy.deepcopy(self.annotations['artifacts'][0]['spans'][1]['propositions'][0]['semantic_ast'])
        ast.update(action='pledge', parameters=characteristic_parameters(span))
        self.assertEqual(ast['parameters'], ['characteristic:age', 'characteristic:caste',
                                            'characteristic:sexual identity and orientation'])
        validate_interpretation(ast, span)
        ast['parameters'].remove('characteristic:caste')
        with self.assertRaisesRegex(ValueError, 'enumeration differs'):
            validate_interpretation(ast, span)

    def test_corrected_golden_records_close_reported_fidelity_findings(self):
        root = ROOT / 'evidence/semantics/b0'
        records = [json.loads(s) for s in (root / 'ledger/propositions.jsonl').read_text().splitlines()]
        self.assertEqual(len(records), 227)
        for record in records:
            ast = record['semantic_ast']
            if ast['modality'] == 'PROHIBITED':
                self.assertNotEqual(ast['action'], 'avoid')
                self.assertEqual(ast['polarity'], 'NEGATIVE')
        bindings = [p for p in records if 'frontmatter.labels=question' in p['semantic_ast']['parameters']]
        self.assertEqual(len(bindings), 1)
        self.assertEqual(bindings[0]['semantic_ast']['modality'], 'DESCRIPTIVE')
        pledges = [p for p in records if p['semantic_ast']['action'] == 'pledge']
        self.assertEqual(len(pledges), 4)
        self.assertTrue(all(p['semantic_ast']['parameters'] for p in pledges))
        revision = json.loads((root / 'revision-v2.json').read_bytes())
        self.assertEqual(len(revision['added_proposition_ids']), 9)
        self.assertEqual(len(revision['old_to_new_proposition_ids']), 207)

    def test_review_corrections_preserve_distinct_actors_and_modalities(self):
        root = ROOT / 'evidence/semantics/b0'
        records = [json.loads(s) for s in (root / 'ledger/propositions.jsonl').read_text().splitlines()]
        asts = [p['semantic_ast'] for p in records]
        reports = [a for a in asts if a['action'] == 'report' and a['subject'] == 'participants']
        self.assertEqual(len(reports), 3)
        self.assertTrue(all(a['modality'] == 'MAY' and a['subject'] == 'participants' for a in reports))
        investigations = [a for a in asts if a['action'] == 'review and investigate']
        self.assertEqual(len(investigations), 3)
        self.assertTrue(all(a['modality'] == 'MUST' and a['preconditions'] for a in investigations))
        privacy = [a for a in asts if a['action'] == 'protect']
        self.assertEqual(len(privacy), 3)
        self.assertTrue(all(a['modality'] == 'MUST' for a in privacy))
        citation = next(a for a in asts if a['scope'][-1] == 'CITATION.cff')
        self.assertEqual(citation['subject'], 'software user')
        self.assertEqual(citation['preconditions'], ['Uses this software'])
        choices = [a for a in asts if a['action'] == 'choose corrective measures']
        self.assertEqual(len(choices), 3)
        self.assertTrue(all(a['modality'] == 'MAY' for a in choices))
        discussions = [a for a in asts if a['scope'][-1] == 'GOVERNANCE.md' and
                       a['subject'] == 'issue-discussion participants']
        self.assertEqual(len(discussions), 1)
        self.assertEqual(discussions[0]['modality'], 'MUST')

    def test_warning_trigger_is_bound_and_comment_terms_are_complete(self):
        root = ROOT / 'evidence/semantics/b0/ledger'
        props = [json.loads(s) for s in (root / 'propositions.jsonl').read_text().splitlines()]
        comments = [p['semantic_ast']['object'] for p in props if
                    p['semantic_ast']['object'].startswith('trolling,')]
        self.assertEqual(len(comments), 3)
        self.assertTrue(all('insulting' in text and 'derogatory' in text for text in comments))
        occurrences = [json.loads(s) for s in (root / 'occurrences.jsonl').read_text().splitlines()]
        warning = next(o for o in occurrences if
                       o['source']['repository'].startswith('jlcanovas/') and
                       o['source']['path'] == 'CODE_OF_CONDUCT.md' and
                       o['semantic_ast']['object'].startswith('warning with consequences'))
        self.assertEqual(warning['source']['start_line'], 84)
        self.assertEqual(warning['source']['end_line'], 86)
