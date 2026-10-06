"""Deterministically compile authored community annotations, never infer review."""
from __future__ import annotations

import gzip
import hashlib
import json
import re
import shutil
import tempfile
from pathlib import Path
import yaml

from .semantics import canonical_bytes, stable_id, validate_record
from .core import ROOT, digest

SOURCES = {'tmcw/github-best-practices', 'jlcanovas/gh-best-practices-template',
           'atapas/model-repo'}
PROPOSED = {'status': 'PROPOSED', 'reviewer': None, 'evidence_reference': None}


def characteristic_parameters(text: str) -> list[str]:
    """Bind an authored pledge's enumeration to its complete source list."""
    normalized = ' '.join(text.split())
    match = re.search(r'regardless of (.*?)(?:\.\s|\.$)', normalized)
    if not match:
        return []
    return ['characteristic:' + item.strip().removeprefix('or ')
            for item in match[1].split(',')]


def template_parameters(record: dict) -> list[str]:
    """Validate operative frontmatter bindings, without extracting new meaning."""
    if not record['path'].startswith('.github/ISSUE_TEMPLATE/'):
        return []
    lines = record['content'].splitlines()
    if not lines or lines[0] != '---':
        return []
    require('---' in lines[1:], 'Unterminated issue-template frontmatter')
    end = lines.index('---', 1)
    fields = yaml.safe_load('\n'.join(lines[1:end]))
    require(isinstance(fields, dict), 'Invalid issue-template frontmatter')
    result = []
    for key in ('name', 'about', 'title', 'labels', 'assignees'):
        value = fields.get(key)
        if value is not None and value != '' and value != []:
            require(isinstance(value, str), 'Unsupported nonempty frontmatter binding')
            result.append('frontmatter.' + key + '=' + value)
    return result


def validate_interpretation(ast: dict, span: str) -> None:
    """B0-specific fidelity guards; these do not certify arbitrary semantics."""
    if ast['modality'] == 'PROHIBITED':
        require(ast['polarity'] == 'NEGATIVE', 'Prohibition must negate its underlying action')
        require(ast['action'].strip().lower() not in {'avoid', 'prevent', 'refrain from', 'not'},
                'Prohibited avoidance reverses or obscures the underlying action')
    if ast['action'] == 'pledge':
        expected = characteristic_parameters(span)
        actual = [p for p in ast['parameters'] if p.startswith('characteristic:')]
        require(actual == expected, 'Protected-characteristic enumeration differs from source')


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def load_sources(manifest: dict, sources: Path) -> dict:
    require(manifest.get('schema') == 'ges.b0-input-manifest.v1', 'Wrong manifest schema')
    require({s['repository'] for s in manifest['sources']} == SOURCES
            and len(manifest['sources']) == 3, 'B0 requires exactly three community sources')
    records = {}
    pins = {s['repository']: s for s in json.loads(
        (ROOT / 'sources/sources.lock.json').read_bytes())['sources']}
    for source in manifest['sources']:
        pin = pins[source['repository']]
        require(source['commit'] == pin['commit']
                and source['archive_sha256'] == pin['archive_sha256']
                and len(source['artifacts']) == pin['artifacts'], 'B0 differs from pinned source scope')
        name = source['repository'].replace('/', '__')
        snapshot = sources / (name + '.text.jsonl.gz')
        inventory_path = sources / (name + '.inventory.json')
        require(sha(snapshot.read_bytes()) == source['snapshot_sha256'], 'Stale snapshot digest')
        raw_inventory = inventory_path.read_bytes()
        require(sha(raw_inventory) == source['inventory_sha256'], 'Stale inventory digest')
        inventory = json.loads(raw_inventory)
        frozen = source['artifacts']
        require(len(frozen) == len(inventory), 'Inventory denominator differs')
        expected = {a['path']: a for a in frozen}
        require(len(expected) == len(frozen), 'Duplicate artifact path')
        for artifact in frozen:
            require(artifact['artifact_id'] == digest([
                source['repository'], source['commit'], artifact['path']])[:24],
                'Artifact identity differs')
        seen_inventory = set()
        for artifact in inventory:
            path = artifact['path']
            require(path in expected and path not in seen_inventory, 'Unknown or duplicate inventory artifact')
            seen_inventory.add(path)
            require(artifact['source'] == source['repository']
                    and artifact['commit'] == source['commit']
                    and artifact['sha256'] == expected[path]['content_sha256']
                    and artifact['git_blob_sha'] == expected[path]['git_blob_sha'],
                    'Inventory identity differs')
        seen = set()
        with gzip.open(snapshot, 'rt', encoding='utf-8') as stream:
            for line in stream:
                record = json.loads(line)
                path = record['path']
                require(path in expected and path not in seen, 'Unknown or duplicate snapshot artifact')
                seen.add(path)
                content = record['content'].encode('utf-8')
                require(record['source'] == source['repository']
                        and record['commit'] == source['commit']
                        and record['sha256'] == expected[path]['content_sha256']
                        and sha(content) == expected[path]['content_sha256'], 'Stale artifact bytes')
                blob = hashlib.sha1(b'blob ' + str(len(content)).encode() + b'\0' + content).hexdigest()
                require(blob == expected[path]['git_blob_sha'], 'Git blob differs')
                require(len(content.splitlines()) == expected[path]['line_count'], 'Line denominator differs')
                records[(source['repository'], path)] = record
        require(seen == set(expected), 'Missing snapshot artifacts')
    return records


def compile_ledger(manifest: dict, annotations: dict, sources: Path) -> dict[str, bytes]:
    """Bind each authored span and nonclaim decision to immutable source bytes."""
    records = load_sources(manifest, sources)
    require(annotations.get('schema') == 'ges.b0-annotations.v1', 'Wrong annotation schema')
    require(sha(canonical_bytes(annotations)) == manifest['annotations_sha256'], 'Stale annotations')
    require(len(annotations['artifacts']) == len(records), 'Artifact accounting incomplete')
    occurrences, propositions, accounting = [], [], []
    seen_artifacts, seen_occurrences, seen_propositions = set(), set(), set()
    for artifact in annotations['artifacts']:
        key = (artifact['repository'], artifact['path'])
        require(key in records and key not in seen_artifacts, 'Unknown or duplicate annotation artifact')
        seen_artifacts.add(key)
        record = records[key]
        lines = record['content'].encode('utf-8').splitlines(keepends=True)
        covered = set()
        occurrence_ids = []
        nonclaims = []
        authored_parameters = set()
        for entry in artifact['spans']:
            start, end = entry['start_line'], entry['end_line']
            require(type(start) is int and type(end) is int and 1 <= start <= end <= len(lines),
                    'Invalid source span')
            numbers = set(range(start, end + 1))
            require(not (numbers & covered), 'Overlapping source accounting')
            covered.update(numbers)
            span_digest = sha(b''.join(lines[start - 1:end]))
            if entry['kind'] == 'NONCLAIM':
                require(isinstance(entry.get('reason'), str) and bool(entry['reason'].strip()),
                        'Nonclaim requires a reason')
                nonclaims.append({'start_line': start, 'end_line': end, 'span_sha256': span_digest,
                                  'reason': entry['reason'], 'review_status': 'PROPOSED'})
                continue
            require(entry['kind'] == 'OCCURRENCE' and bool(entry.get('propositions')), 'Missing semantic annotation')
            heading_stack = []
            for line in record['content'].splitlines()[:start]:
                if line.startswith('#') and ' ' in line:
                    prefix, title = line.split(' ', 1)
                    if set(prefix) == {'#'}:
                        level = len(prefix)
                        heading_stack = [(n, t) for n, t in heading_stack if n < level]
                        heading_stack.append((level, title.strip()))
            occurrence = {
                'schema': 'ges.semantic-occurrence.v1',
                'source': {'repository': key[0], 'commit': record['commit'], 'path': key[1],
                           'content_sha256': record['sha256'], 'start_line': start,
                           'end_line': end, 'span_sha256': span_digest},
                'heading_ancestry': list(dict.fromkeys(t for _, t in heading_stack)),
                'include_chain': [], 'page_applications': [],
                'conditions': artifact['context'], 'products': ['GitHub'], 'versions': [],
                'authority_class': 'COMMUNITY', 'semantic_kind': entry['semantic_kind'],
                'semantic_ast': entry['propositions'][0]['semantic_ast'],
                'formalization': ' '.join(p['formalization'] for p in entry['propositions']),
                'extraction': {'method': 'authored-span-annotations', 'version': 'b0.v1'},
                'review': dict(PROPOSED),
            }
            occurrence['id'] = stable_id(occurrence)
            validate_record(occurrence)
            require(occurrence['id'] not in seen_occurrences, 'Duplicate occurrence')
            seen_occurrences.add(occurrence['id'])
            occurrences.append(occurrence)
            occurrence_ids.append(occurrence['id'])
            for authored in entry['propositions']:
                ast = authored['semantic_ast']
                validate_interpretation(ast, b''.join(lines[start - 1:end]).decode('utf-8'))
                authored_parameters.update(ast['parameters'])
                prop = {
                    'schema': 'ges.semantic-proposition.v1', 'semantic_ast': authored['semantic_ast'],
                    'occurrence_ids': [occurrence['id']], 'preserved_differences': [],
                    'authority_order': ['COMMUNITY'], 'applicability': artifact['context'],
                    'ambiguities': authored['ambiguities'],
                    'primary_review': dict(PROPOSED), 'omission_review': dict(PROPOSED),
                }
                prop['id'] = stable_id(prop)
                validate_record(prop)
                # No automatic consolidation: source-local scope differentiates propositions.
                require(prop['id'] not in seen_propositions, 'Duplicate proposition requires explicit later reconciliation')
                seen_propositions.add(prop['id'])
                propositions.append(prop)
        require(covered == set(range(1, len(lines) + 1)), 'Unaccounted source lines')
        require(set(template_parameters(record)) <= authored_parameters,
                'Operative issue-template binding is missing')
        require(occurrence_ids or nonclaims, 'Undispositioned artifact')
        accounting.append({'repository': key[0], 'path': key[1], 'commit': record['commit'],
                           'artifact_id': digest([key[0], record['commit'], key[1]])[:24],
                           'content_sha256': record['sha256'], 'line_count': len(lines),
                           'occurrence_ids': occurrence_ids, 'nonclaims': nonclaims})
    require(seen_artifacts == set(records), 'Missing artifact dispositions')
    require(0 < len(propositions) <= 250, 'B0 proposition cap exceeded or empty')
    occurrences.sort(key=lambda r: (r['source']['repository'], r['source']['path'], r['source']['start_line']))
    propositions.sort(key=lambda r: r['id'])
    accounting.sort(key=lambda r: (r['repository'], r['path']))
    files = {
        'occurrences.jsonl': b''.join(canonical_bytes(r) + b'\n' for r in occurrences),
        'propositions.jsonl': b''.join(canonical_bytes(r) + b'\n' for r in propositions),
        'artifact-accounting.json': canonical_bytes(accounting) + b'\n',
    }
    by_occurrence = {r['id']: r for r in occurrences}
    review_lines = ['# B0 semantic review queue', '',
                    'Status: HOLD. Every row is PROPOSED; no human approval, semantic certification or policy adoption.',
                    '', '| Proposition ID | Pinned source span | Interpretation | Preserved context |',
                    '| --- | --- | --- | --- |']
    def cell(value: str) -> str:
        return value.replace('|', '\\|').replace('\n', ' ')
    ordered = sorted(propositions, key=lambda r: (
        by_occurrence[r['occurrence_ids'][0]]['source']['repository'],
        by_occurrence[r['occurrence_ids'][0]]['source']['path'],
        by_occurrence[r['occurrence_ids'][0]]['source']['start_line'], r['id']))
    for prop in ordered:
        source = by_occurrence[prop['occurrence_ids'][0]]['source']
        ast = prop['semantic_ast']
        url = (f"https://github.com/{source['repository']}/blob/{source['commit']}/"
               f"{source['path']}#L{source['start_line']}-L{source['end_line']}")
        context = [field + ': ' + '; '.join(ast[field]) for field in (
            'preconditions', 'qualifiers', 'exceptions', 'consequences', 'parameters') if ast[field]]
        if prop['ambiguities']:
            context.append('Ambiguity: ' + '; '.join(prop['ambiguities']))
        review_lines.append('| ' + ' | '.join((
            '`' + prop['id'] + '`',
            f"[{cell(source['repository'] + ':' + source['path'])}:{source['start_line']}-{source['end_line']}]({url})",
            cell(f"{ast['modality']}: {ast['subject']} — {ast['action']} {ast['object']}"),
            cell('; '.join(context)))) + ' |')
    review_lines += ['', '## Nonclaim review queue', '',
                     'These source-bound line dispositions also require B0 approval. License text remains operative legal supporting evidence, excluded from project-engineering propositions; no rights clearance is asserted.', '']
    for artifact in accounting:
        review_lines.append(f"### {artifact['repository']}:{artifact['path']}")
        review_lines.append('')
        for nonclaim in artifact['nonclaims']:
            review_lines.append(f"- Lines {nonclaim['start_line']}-{nonclaim['end_line']}: "
                                + nonclaim['reason'])
        review_lines.append('')
    files['review.md'] = ('\n'.join(review_lines).rstrip() + '\n').encode('utf-8')
    residual = {
        'schema': 'ges.b0-residual.v1', 'status': 'HOLD', 'next_tranche': 'C0',
        'source_accounting_gaps': [], 'primary_review_pending': sorted(seen_propositions),
        'artifact_and_nonclaim_review_pending': [list(key) for key in sorted(records)],
        'acceptance_pending': ['A0-A6 dependency acceptance', 'exact-head human approval',
                               'exact remote-head CI', 'merge to main', 'merged-head verification'],
        'semantic_truth_certified': False, 'policy_adopted': False,
    }
    files['residual.json'] = canonical_bytes(residual) + b'\n'
    receipt = {
        'schema': 'ges.b0-extraction-receipt.v1', 'status': 'HOLD',
        'input_manifest_sha256': sha(canonical_bytes(manifest)),
        'artifact_count': len(accounting), 'occurrence_count': len(occurrences),
        'proposition_count': len(propositions), 'reviewed_proposition_count': 0,
        'outputs_sha256': {name: sha(raw) for name, raw in sorted(files.items())},
        'exclusions': manifest['exclusions'], 'semantic_truth_certified': False,
        'policy_adopted': False, 'next_tranche': 'C0',
    }
    files['receipt.json'] = canonical_bytes(receipt) + b'\n'
    return files


def extract(manifest_path: Path, annotations_path: Path, sources: Path, output: Path,
            *, check: bool = False) -> dict:
    if not check:
        require(not output.exists(), 'Output already exists')
    manifest = json.loads(manifest_path.read_bytes())
    annotations = json.loads(annotations_path.read_bytes())
    files = compile_ledger(manifest, annotations, sources)
    if check:
        require(output.is_dir() and not output.is_symlink(), 'Missing or symlinked output')
        require({p.name for p in output.iterdir()} == set(files), 'Output membership differs')
        for name, raw in files.items():
            path = output / name
            require(path.is_file() and not path.is_symlink() and path.read_bytes() == raw,
                    'Output bytes differ: ' + name)
        return json.loads(files['receipt.json'])
    output.parent.mkdir(parents=True, exist_ok=True)
    staged = Path(tempfile.mkdtemp(prefix='.b0-', dir=output.parent))
    try:
        for name, raw in files.items():
            (staged / name).write_bytes(raw)
        require(not output.exists(), 'Output already exists')
        staged.rename(output)
    finally:
        if staged.exists():
            shutil.rmtree(staged)
    return json.loads(files['receipt.json'])
