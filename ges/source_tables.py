"""Check literal source-table facts; never adjudicate policy or live capability."""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

import yaml

from .claim_workload import PROVIDER_FIELDS, inventory
from .core import digest
from .yamlutil import UniqueLoader, parse


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def provider_facts(content: str, path: str) -> tuple[dict, dict]:
    """Preserve exact YAML identities/occurrences; absent fields are not false."""
    if not re.fullmatch(r'src/secret-scanning/data/pattern-docs/(fpt|ghec|ghes-\d+\.\d+)/public-docs.yml', path):
        raise ValueError('Unknown provider dataset path')
    try:
        rows = parse(content)
        tree = yaml.compose(content, Loader=UniqueLoader)
    except yaml.YAMLError as exc:
        raise ValueError('Invalid provider YAML') from exc
    if not isinstance(rows, list) or not isinstance(tree, yaml.SequenceNode):
        raise TypeError('Provider dataset must be a YAML sequence')
    version = path.split('/')[-2]
    if not re.fullmatch(r'fpt|ghec|ghes-\d+\.\d+', version):
        raise ValueError('Unknown provider version path')
    product = {'fpt': 'free/pro/team', 'ghec': 'Enterprise Cloud'}.get(version, version)
    context_product = version + ' pinned dataset' if version in ('fpt', 'ghec') else version
    labels = {'isPublic': 'the literal public-support flag',
              'isPrivateWithGhas': 'the literal private-with-Advanced-Security support flag',
              'hasPushProtection': 'push-protection support',
              'hasValidityCheck': 'validity-check support',
              'hasExtendedMetadata': 'extended-metadata support',
              'base64Supported': 'Base64 detection support',
              'isduplicate': 'the duplicate-entry marker'}
    facts, statistics = {}, Counter()
    for ordinal, (row, node) in enumerate(zip(rows, tree.value), 1):
        if (not isinstance(row, dict) or not isinstance(node, yaml.MappingNode) or
                any(not isinstance(row.get(k), str) or not row[k]
                    for k in ('provider', 'secretType', 'supportedSecret'))):
            raise ValueError('Malformed provider identity')
        marks = {k.value: v.start_mark.line + 1 for k, v in node.value}
        identifier = re.sub(r'</?br\s*/?>', '', row['secretType']).strip()
        for field in sorted(PROVIDER_FIELDS):
            if field not in row:
                statistics['absent_fields'] += 1
                continue
            value = row[field]
            if type(value) is bool:
                statement = (f'For {identifier}, this {product} dataset declares '
                             f'{labels[field]} {str(value).lower()}.')
                statistics['boolean_fields'] += 1
            elif field in ('hasValidityCheck', 'hasExtendedMetadata'):
                conditions = {
                    '{% ifversion ghes %}false{% else %}true{% endif %}':
                        'Enterprise Server',
                    '{% ifversion fpt or ghes %}false{% else %}true{% endif %}':
                        'free/pro/team or Enterprise Server',
                }
                if value not in conditions:
                    raise ValueError('Unknown provider conditional')
                target = conditions[value]
                if version in ('fpt', 'ghec'):
                    statement = (f'For {identifier}, this dataset declares {labels[field]} '
                                 f'false in {target} context and true otherwise; the version '
                                 'conditional is retained rather than coerced to a boolean.')
                else:
                    statement = (f'For {identifier}, this {product} dataset declares '
                                 f'{labels[field]} false in {target} context and true otherwise; '
                                 'the source version conditional is not coerced to a boolean.')
                statistics['conditional_fields'] += 1
            else:
                raise ValueError('Provider field is not a boolean')
            facts[(ordinal, field)] = {
                'statement': statement, 'value': value, 'line': marks[field],
                'definition_start_line': node.start_mark.line + 1,
                'definition_end_line': node.end_mark.line,
                'provider': row['provider'], 'raw_credential_identifier': row['secretType'],
                'credential_identifier': identifier, 'credential_label': row['supportedSecret'],
                'product_version': context_product,
            }
        statistics['rows'] += 1
        statistics['duplicate_marked_rows'] += row.get('isduplicate') is True
    return facts, dict(statistics)


def query_facts(content: str, path: str) -> tuple[dict, dict]:
    """Parse literal row cells, retaining CWE spelling and query URL identity."""
    if not re.fullmatch(r'data/reusables/code-scanning/codeql-query-tables/[a-z]+\.md', path):
        raise ValueError('Unknown query table path')
    header = '| Query name | Related CWEs | Default | Extended | {% data variables.copilot.copilot_autofix_short %} |'
    lines = content.splitlines()
    if lines.count(header) != 1:
        raise ValueError('Unknown or repeated query table header')
    position = lines.index(header)
    if (position + 1 >= len(lines) or
            lines[position + 1] != '| --- | --- | --- | --- | --- |' or
            lines[0] != '{% rowheaders %}' or lines[-1] != '{% endrowheaders %}'):
        raise ValueError('Unknown query table wrapper or separator')
    facts = {}
    rows = 0
    for line_number, line in enumerate(lines, 1):
        if not line.lstrip().startswith('|') or line == header or re.fullmatch(r'\|(?:\s*---\s*\|){5}', line):
            continue
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        if len(cells) != 5:
            raise ValueError('Unknown query table row shape')
        match = re.fullmatch(r'\[(.*)\]\((https://codeql.github.com/codeql-query-help/[^\s)]+/)\)',
                             cells[0])
        if not match:
            raise ValueError('Unknown query link shape')
        label, url = match.groups()
        identity = url.rstrip('/').split('/')[-1]
        facts[(line_number, 'label')] = {
            'statement': f'The row identified by {identity} has display label {json.dumps(label, ensure_ascii=False)}.',
            'query_help_identity': url,
        }
        facts[(line_number, 'link')] = {
            'statement': f'That query row links to {url}.', 'query_help_identity': url,
        }
        if cells[1]:
            cwes = [c.strip() for c in cells[1].split(',')]
            if len(cwes) != len(set(cwes)) or any(not re.fullmatch(r'\d+', c) for c in cwes):
                raise ValueError('Unknown or repeated CWE cell')
            for cwe in cwes:
                facts[(line_number, 'cwe:' + cwe)] = {
                    'statement': f"The {identity} row associates related CWE identity {cwe}; the source's digit spelling is preserved.",
                    'query_help_identity': url, 'cwe_identity': cwe,
                }
        for column, cell in zip(('Default', 'Extended', 'Autofix'), cells[2:]):
            match = re.fullmatch(r'{% octicon "(check|x)" aria-label="(Included|Not included)" %}', cell)
            if not match or match.groups() not in (('check', 'Included'), ('x', 'Not included')):
                raise ValueError('Unknown or contradictory query icon')
            icon, label = match.groups()
            facts[(line_number, column)] = {
                'statement': f'For {identity}, the {column} column records {label}.',
                'query_help_identity': url, 'column': column, 'cell_label': label, 'cell_icon': icon,
            }
        rows += 1
    if not rows:
        raise ValueError('No query rows')
    return facts, {'rows': rows, 'facts': len(facts)}


def validate(reviews: Path, artifacts: Path, reconciliation: Path,
             workload: Path, snapshots: Path, lock: Path) -> dict:
    """Recompute complete membership, verify pinned bytes, and compare exact facts."""
    workload_raw, lock_raw = workload.read_bytes(), lock.read_bytes()
    audit = json.loads(workload_raw)
    if inventory(reviews, artifacts, reconciliation) != audit:
        raise ValueError('Workload no longer reproduces from the exact inputs')
    pin_rows = json.loads(lock_raw)['sources']
    pins = {r['repository']: r['commit'] for r in pin_rows}
    if len(pins) != len(pin_rows):
        raise ValueError('Duplicate source lock repository')
    artifact_raw = artifacts.read_bytes()
    if sha(artifact_raw) != audit['inputs']['artifacts_sha256']:
        raise ValueError('Artifact inventory changed before source pass')
    artifact_rows = [json.loads(line) for line in artifact_raw.splitlines() if line.strip()]
    indexed = {(a['source'], a['commit'], a['path']): a for a in artifact_rows}
    kinds = {cid: f['kind'] for f in audit['families']
             if f['kind'] in ('PROVIDER_CAPABILITY_MATRIX', 'QUERY_TABLE_ROW')
             for cid in f['claim_ids']}
    if not kinds:
        raise ValueError('Empty source-table scope')
    subjects = {}
    for row in audit['inputs']['claim_documents']:
        document_raw = (reviews / row['path']).read_bytes()
        if sha(document_raw) != row['sha256']:
            raise ValueError('Claim document changed before source pass')
        doc = json.loads(document_raw)
        for claim in doc['claims']:
            if claim['claim_id'] in kinds:
                subjects[claim['claim_id']] = (claim, doc)
    if set(subjects) != set(kinds):
        raise ValueError('Source-table claim membership mismatch')
    selected = {(c.get('source', d.get('source')), c.get('commit', d.get('commit')),
                 c.get('path', d.get('path'))) for c, d in subjects.values()}
    source_raw = snapshots.read_bytes()
    sources = {}
    for line in gzip.decompress(source_raw).splitlines():
        row = json.loads(line)
        key = (row['source'], row['commit'], row['path'])
        if key in selected:
            if key in sources:
                raise ValueError('Duplicate selected source snapshot')
            if pins.get(row['source']) != row['commit']:
                raise ValueError('Source pin mismatch')
            content = row['content'].encode()
            if sha(content) != indexed[key]['sha256'] or row['sha256'] != sha(content):
                raise ValueError('Pinned source content digest mismatch')
            sources[key] = row
    if set(sources) != selected:
        raise ValueError('Missing selected source snapshot')
    facts, path_stats = {}, []
    for key, row in sorted(sources.items()):
        parser = provider_facts if key[2].endswith('/public-docs.yml') else query_facts
        parsed, stats = parser(row['content'], key[2])
        facts[key] = parsed
        path_stats.append({'source': key[0], 'commit': key[1], 'path': key[2],
                           'sha256': row['sha256'], **stats})
    seen, matched, findings = set(), [], []
    for cid, (claim, doc) in sorted(subjects.items()):
        key = tuple(claim.get(k, doc.get(k)) for k in ('source', 'commit', 'path'))
        line = claim['start_line']
        if kinds[cid] == 'PROVIDER_CAPABILITY_MATRIX':
            ctx = claim['context']
            slot = (ctx['entry_ordinal'], ctx['source_field'])
            fact = facts[key].get(slot)
            okay = (fact is not None and claim['statement'] == fact['statement'] and
                    line == claim['end_line'] == fact['line'] and
                    all(ctx.get(k) == fact[k] for k in (
                        'provider', 'raw_credential_identifier', 'credential_identifier',
                        'credential_label', 'product_version', 'definition_start_line',
                        'definition_end_line')))
        else:
            slot_name = (claim.get('column') or ('cwe:' + claim['cwe_identity']
                         if 'cwe_identity' in claim else
                         'link' if claim['statement'].startswith('That query row links to ') else 'label'))
            slot = (line, slot_name)
            fact = facts[key].get(slot)
            okay = (fact is not None and claim['end_line'] == line and
                    claim['query_occurrence'] == key[2] + '#L' + str(line) and
                    all(claim.get(k) == v for k, v in fact.items()))
        full_slot = (*key, *slot)
        if full_slot in seen:
            findings.append({'claim_id': cid, 'path': key[2], 'finding': 'DUPLICATE_FACT_SUBJECT'})
        elif not okay:
            findings.append({'claim_id': cid, 'path': key[2], 'finding': 'SOURCE_FACT_MISMATCH'})
        else:
            matched.append(cid)
        seen.add(full_slot)
    expected = {(*key, *slot) for key, rows in facts.items() for slot in rows}
    for missing in sorted(expected - seen):
        findings.append({'path': missing[2], 'subject': list(missing[3:]), 'finding': 'SOURCE_FACT_WITHOUT_CLAIM'})
    # Recheck every digest-bound input and complete membership after the source pass.
    if (snapshots.read_bytes() != source_raw or lock.read_bytes() != lock_raw or
            workload.read_bytes() != workload_raw or
            inventory(reviews, artifacts, reconciliation) != audit):
        raise ValueError('Inputs changed during source-table validation')
    return {
        'schema': 'ges.source-table-verification.v1',
        'scope': 'Exact literal fields in selected pinned source tables; distinct from semantic review.',
        'inputs': {'workload_sha256': sha(workload_raw), 'source_lock_sha256': sha(lock_raw),
                   'source_snapshot_sha256': sha(source_raw)},
        'counts': {'recorded_table_claims': len(subjects), 'source_facts': len(expected),
                   'mechanically_matched_claims': len(matched), 'findings': len(findings),
                   'matched_by_kind': dict(Counter(kinds[c] for c in matched)),
                   'semantic_review_credit': 0, 'reconciliation_credit': 0},
        'status': 'LITERAL_SOURCE_MATCH' if not findings else 'FINDINGS',
        'matched_claim_ids': matched, 'findings': findings, 'source_tables': path_stats,
        'source_facts_digest': digest([[list(key), list(slot), fact]
                                     for key, rows in sorted(facts.items())
                                     for slot, fact in sorted(rows.items())]),
        'limits': [
            'Provider public/private field labels are legacy claim wording, not current UI meanings.',
            'Conditional strings are preserved, not rendered or coerced to booleans.',
            'All missing provider keys and duplicate occurrences remain visible.',
            'CodeQL facts describe pinned table cells, not successful execution or complete coverage.',
            'No source-omission, rights, policy adoption, native behavior or legacy gate closure credit.',
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('reviews', 'artifacts', 'reconciliation', 'workload', 'snapshots', 'lock', 'output'):
        parser.add_argument('--' + name, type=Path, required=True)
    args = parser.parse_args()
    result = validate(args.reviews, args.artifacts, args.reconciliation,
                      args.workload, args.snapshots, args.lock)
    with args.output.open('x') as stream:
        json.dump(result, stream, indent=2)
        stream.write('\n')
    print(json.dumps(result['counts']))
    if result['findings']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
