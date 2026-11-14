import copy
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from ges import receipts, token_semantics as ts  # noqa: E402
from ges.semantics import validate_record  # noqa: E402

CONFORMANCE = json.loads(ts.CONFORMANCE.read_text(encoding='utf-8'))
ANNOTATIONS = json.loads(ts.ANNOTATIONS.read_text(encoding='utf-8'))
RESTRICTED = {'contents': 'read', 'packages': 'read'}


class Conformance(unittest.TestCase):
    def test_committed_cases_all_pass_and_cover_every_supported_rule(self):
        self.assertEqual(ts.check_conformance(ANNOTATIONS, CONFORMANCE), [])

    def test_changed_expectation_is_reported(self):
        broken = copy.deepcopy(CONFORMANCE)
        broken['cases'][0]['expect'] = {'allowed': not broken['cases'][0]['expect']['allowed']}
        problems = ts.check_conformance(ANNOTATIONS, broken)
        self.assertEqual(len(problems), 1)
        self.assertIn(broken['cases'][0]['id'], problems[0])

    def test_uncited_source_rule_and_unsupported_cited_rule_are_reported(self):
        trimmed = copy.deepcopy(CONFORMANCE)
        trimmed['cases'] = [c for c in trimmed['cases'] if 'T12' not in c['rules']]
        self.assertTrue(any('rule T12' in p for p in ts.check_conformance(ANNOTATIONS, trimmed)))
        extra = copy.deepcopy(CONFORMANCE)
        extra['cases'][0]['rules'] = ['T99']
        self.assertTrue(any('T99' in p for p in ts.check_conformance(ANNOTATIONS, extra)))

    def test_schema_is_checked(self):
        self.assertEqual(ts.check_conformance(ANNOTATIONS, {'schema': 'x', 'cases': []}),
                         ['conformance: unsupported schema'])


class Model(unittest.TestCase):
    def resolve(self, **kwargs):
        defaults = {'default': RESTRICTED, 'event': 'push', 'from_fork': False}
        return ts.resolve_token_permissions(**{**defaults, **kwargs})

    def test_fork_downgrade_applies_only_to_pull_request_events_not_target(self):
        for event in ('pull_request', 'pull_request_review', 'pull_request_review_comment'):
            self.assertEqual(self.resolve(event=event, from_fork=True, workflow={'issues': 'write'})['issues'], 'read')
        self.assertEqual(self.resolve(event='pull_request_target', from_fork=True,
                                      workflow={'issues': 'write'})['issues'], 'write')

    def test_job_key_replaces_not_merges_with_workflow_key(self):
        result = self.resolve(workflow={'contents': 'write', 'issues': 'write'}, job={'checks': 'read'})
        self.assertEqual({k: v for k, v in result.items() if v != 'none'}, {'checks': 'read'})

    def test_unknown_scope_and_bad_default_raise(self):
        with self.assertRaises(ValueError):
            ts.apply_permissions_key({'contentz': 'read'})
        with self.assertRaises(ValueError):
            ts.apply_permissions_key('admin-all')
        with self.assertRaises(ValueError):
            self.resolve(default={'contents': 'admin'})

    def test_read_all_is_clipped_to_scope_levels(self):
        flags = frozenset({'fpt-or-ghec', 'vulnerability-alerts-permission'})
        read_all = ts.apply_permissions_key('read-all', flags)
        self.assertEqual(read_all['id-token'], 'none')
        self.assertEqual(read_all['vulnerability-alerts'], 'read')
        self.assertEqual(ts.apply_permissions_key('write-all', flags)['vulnerability-alerts'], 'read')

    def test_pull_request_target_fork_run_can_reach_secrets_pull_request_cannot(self):
        self.assertFalse(ts.secrets_reach_runner('DEPLOY_KEY', from_fork=True, event='pull_request'))
        self.assertTrue(ts.secrets_reach_runner('DEPLOY_KEY', from_fork=True, event='pull_request_target'))

    def test_merged_closure_ref_is_the_destination_branch(self):
        merged = ts.pull_request_event_context('pull_request', closed_by_merge=True)['ref']
        self.assertNotIn('refs/pull', merged)
        self.assertIn('refs/pull', ts.pull_request_event_context('pull_request')['ref'])

    def test_version_split_statements_do_not_restrict_applicability_to_old_ghes(self):
        for line in (ts.PROPOSITIONS.read_text(encoding='utf-8').splitlines()):
            record = json.loads(line)
            if record['semantic_ast']['subject'] == 'pull_request_target event':
                self.assertTrue(any('GitHub.com and later GHES' in item for item in record['applicability']),
                                record['semantic_ast']['object'])
                self.assertFalse(any(item == 'ifversion ghes < 3.20' for item in record['applicability']))

    def test_unknown_runner_rejected(self):
        with self.assertRaises(ValueError):
            ts.token_is_valid('hosted', 1.0, job_finished=False)


class ReceiptActionConsequences(unittest.TestCase):
    """The receipt action's documented limits follow from the pinned documentation."""

    def test_fork_pull_request_cannot_write_the_pull_request_body(self):
        caller = {'pull-requests': 'write', 'contents': 'read'}  # the caller in docs/agent-verification-receipts.md
        same_repo = ts.resolve_token_permissions(default=RESTRICTED, workflow=caller,
                                                 event='pull_request', from_fork=False)
        fork = ts.resolve_token_permissions(default=RESTRICTED, workflow=caller,
                                            event='pull_request', from_fork=True)
        self.assertTrue(ts.allows(same_repo, 'pull-requests', 'write'))
        self.assertFalse(ts.allows(fork, 'pull-requests', 'write'))
        self.assertTrue(ts.allows(fork, 'pull-requests', 'read'))

    def test_documented_caller_permissions_match_the_modelled_requirement(self):
        text = (ROOT / 'docs' / 'agent-verification-receipts.md').read_text(encoding='utf-8')
        block = text.split('```yaml', 1)[1].split('```', 1)[0]
        permissions = yaml.safe_load(block)['permissions']
        resolved = ts.resolve_token_permissions(default=RESTRICTED, workflow=permissions,
                                                event='pull_request', from_fork=False)
        self.assertTrue(ts.allows(resolved, 'pull-requests', 'write'))

    def test_action_refuses_the_event_whose_token_stays_writable_for_forks(self):
        action = yaml.safe_load((ROOT / '.github' / 'actions' / 'inject-agent-receipt' / 'action.yml')
                                .read_text(encoding='utf-8'))
        script = action['runs']['steps'][0]['run']
        self.assertIn(ts.PULL_REQUEST_TARGET, script)
        target = ts.resolve_token_permissions(default=RESTRICTED, workflow={'pull-requests': 'write'},
                                              event=ts.PULL_REQUEST_TARGET, from_fork=True)
        self.assertTrue(ts.allows(target, 'pull-requests', 'write'))

    def test_head_sha_binding_needs_the_payload_because_github_sha_is_the_merge_commit(self):
        self.assertIn('merge commit', ts.pull_request_event_context('pull_request')['sha'])

    def test_token_edit_of_the_body_creates_no_workflow_run(self):
        self.assertEqual(ts.workflow_run_for_token_event('pull_request', 'edited'), 'NO_RUN')


class LedgerBuild(unittest.TestCase):
    def committed(self):
        return [json.loads(line) for name in ('occurrences.jsonl', 'propositions.jsonl')
                for line in (ts.LEDGER_DIR / name).read_text(encoding='utf-8').splitlines()]

    def test_committed_records_are_valid_proposed_and_account_for_annotations(self):
        records = self.committed()
        for record in records:
            validate_record(record)
        occurrences = [r for r in records if r['schema'] == 'ges.semantic-occurrence.v1']
        propositions = [r for r in records if r['schema'] == 'ges.semantic-proposition.v1']
        self.assertEqual(len(occurrences), len(ANNOTATIONS['entries']))
        self.assertEqual(len(propositions), sum(len(e['propositions']) for e in ANNOTATIONS['entries']))
        for record in occurrences:
            self.assertEqual(record['review'], {'status': 'PROPOSED', 'reviewer': None, 'evidence_reference': None})
            self.assertEqual(record['source']['commit'], ANNOTATIONS['commit'])
        for record in propositions:
            self.assertEqual(record['primary_review']['status'], 'PROPOSED')
            self.assertEqual(record['omission_review']['status'], 'PROPOSED')
        accounting = json.loads(ts.ACCOUNTING.read_text(encoding='utf-8'))
        self.assertFalse(accounting['semantic_truth_certified'])
        self.assertFalse(accounting['policy_adopted'])
        self.assertEqual(accounting['occurrences'], len(occurrences))
        self.assertEqual(accounting['propositions'], len(propositions))

    def synthetic(self, text='alpha\nbeta rule here\ngamma\n'):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        (Path(directory.name) / 'a.md').write_bytes(text.encode())
        annotations = {
            'schema': ts.ANNOTATIONS_SCHEMA, 'repository': 'github/docs', 'commit': 'a' * 40,
            'entries': [{
                'path': 'a.md', 'start_line': 2, 'end_line': 2, 'expect': 'rule here',
                'content_sha256': hashlib.sha256('alpha\nbeta rule here\ngamma\n'.encode()).hexdigest(),
                'heading_ancestry': [], 'include_chain': [], 'conditions': [], 'versions': [],
                'semantic_kind': 'FACT',
                'propositions': [{'semantic_ast': {
                    'subject': 's', 'action': 'a', 'object': 'o', 'modality': 'DESCRIPTIVE', 'polarity': 'POSITIVE',
                    'scope': [], 'preconditions': [], 'qualifiers': [], 'exceptions': [], 'consequences': [],
                    'parameters': []}, 'formalization': 'f', 'rules': ['T4']}]}]}
        return Path(directory.name), annotations

    def test_synthetic_build_binds_exact_span_bytes(self):
        sources, annotations = self.synthetic()
        built = ts.build_ledger(annotations, sources)
        occurrence = json.loads(built['occurrences.jsonl'])
        self.assertEqual(occurrence['source']['span_sha256'], hashlib.sha256(b'beta rule here\n').hexdigest())
        self.assertEqual(built, ts.build_ledger(annotations, sources), 'build must be deterministic')

    def test_source_drift_is_rejected(self):
        sources, annotations = self.synthetic()
        (sources / 'a.md').write_bytes(b'alpha\nbeta rule here\ngamma changed\n')
        with self.assertRaisesRegex(ValueError, 'content digest differs'):
            ts.build_ledger(annotations, sources)

    def test_anchor_and_range_drift_are_rejected(self):
        sources, annotations = self.synthetic()
        moved = copy.deepcopy(annotations)
        moved['entries'][0]['start_line'] = moved['entries'][0]['end_line'] = 3
        with self.assertRaisesRegex(ValueError, 'anchor text not found'):
            ts.build_ledger(moved, sources)
        outside = copy.deepcopy(annotations)
        outside['entries'][0]['end_line'] = 9
        with self.assertRaisesRegex(ValueError, 'outside file'):
            ts.build_ledger(outside, sources)

    def test_unsafe_path_and_duplicate_statement_are_rejected(self):
        sources, annotations = self.synthetic()
        unsafe = copy.deepcopy(annotations)
        unsafe['entries'][0]['path'] = '../a.md'
        with self.assertRaisesRegex(ValueError, 'Unsafe source path'):
            ts.build_ledger(unsafe, sources)
        duplicate = copy.deepcopy(annotations)
        duplicate['entries'].append(copy.deepcopy(duplicate['entries'][0]))
        with self.assertRaisesRegex(ValueError, 'identical semantic AST'):
            ts.build_ledger(duplicate, sources)

    def test_ledger_carries_no_template_markup(self):
        # Statements are formalized ASTs bound to the source by hashes, not copied template text.
        for record in self.committed():
            self.assertNotIn('{%', json.dumps(record))


class Cli(unittest.TestCase):
    def test_conformance_and_validate_commands_exit_zero(self):
        for command in ('conformance', 'validate'):
            result = subprocess.run([sys.executable, '-m', 'ges', 'token-semantics', command],
                                    cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_verify_with_missing_sources_fails_visibly(self):
        with tempfile.TemporaryDirectory() as empty:
            result = subprocess.run([sys.executable, '-m', 'ges', 'token-semantics', 'verify', '--sources', empty],
                                    cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)


if __name__ == '__main__':
    unittest.main()
