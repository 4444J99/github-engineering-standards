import copy,gzip,hashlib,json,tempfile,unittest
from pathlib import Path
from ges.core import ROOT,applicable,digest,dump,load,safe_path,timestamp,validate_controls
from ges.checks import execute
from ges.corpus import blocks,build_corpus,coverage_with_reviews,impact
from ges.evaluate import audit,gate
from ges.render import generate,render_template
from ges.yamlutil import parse

CAT=load(ROOT/'controls/catalog.json')
AT='2026-10-01T19:00:00+00:00'
def control(kind='manual'):
    c=copy.deepcopy(CAT[0]); c['verification']={'kind':kind};return c

def snapshot(files=None,complete=True):
    return {'target':'owner/repo','target_revision':'a'*40,'observed_at':AT,'observations':{'repository':{'status':'OK','data':{'name':'valid-repository','description':'Purpose','topics':['engineering']}},'files':{'status':'OK','complete':complete,'data':files or {}}}}
PROFILE={'context':{},'authorized_reviewers':['owner'],'max_age_hours':24}

def snap_with_extra(extra=None, files=None, complete=True):
    base=snapshot(files, complete)
    if extra:
        for observation in extra.values():
            if isinstance(observation,dict) and isinstance(observation.get('data'),list):
                observation.setdefault('complete',True)
        base['observations'].update(extra)
    return base

class Contracts(unittest.TestCase):
    def test_catalog_valid(self): self.assertEqual(validate_controls(CAT),[])
    def test_duplicate_id_invalid(self): self.assertTrue(validate_controls([CAT[0],CAT[0]]))
    def test_unpinned_source_invalid(self):
        c=copy.deepcopy(CAT[0]); c['sources'][0]['commit']='main'; self.assertTrue(validate_controls([c]))
    def test_missing_acceptance_invalid(self):
        c=copy.deepcopy(CAT[0]); c['implementation']['acceptance']=[]; self.assertTrue(validate_controls([c]))
    def test_unknown_applicability(self): self.assertEqual(applicable({'applicability':{'actions':True}},{} )[0],'UNKNOWN')
    def test_false_is_not_unknown(self): self.assertEqual(applicable({'applicability':{'actions':True}},{'actions':False})[0],'NOT_APPLICABLE_WITH_REASON')
    def test_no_truthy_conversion(self): self.assertEqual(applicable({'applicability':{'actions':True}},{'actions':'true'})[0],'NOT_APPLICABLE_WITH_REASON')
    def test_timezone_required(self):
        with self.assertRaises(ValueError): timestamp('2026-10-01T00:00:00')
    def test_path_escape_rejected(self):
        with self.assertRaises(ValueError): safe_path(ROOT,'../outside')
    def test_absolute_path_rejected(self):
        with self.assertRaises(ValueError): safe_path(ROOT,'/tmp/outside')
    def test_yaml_duplicates_rejected(self):
        with self.assertRaises(Exception): parse('permissions: read-all\npermissions: write-all\n')
    def test_symlink_escape_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); (root/'escape').symlink_to('/tmp');
            with self.assertRaises(ValueError): safe_path(root,'escape/unsafe')

class Checks(unittest.TestCase):
    def test_present_file_passes_only_presence(self):
        c=control('file_present'); c['verification']['paths']=['README.md']; self.assertEqual(execute(c,snapshot({'README.md':'# Real'}),{})[0],'PASS')
    def test_empty_file_fails(self):
        c=control('file_present'); c['verification']['paths']=['README.md']; self.assertEqual(execute(c,snapshot({'README.md':'   '}),{})[0],'FAIL')
    def test_incomplete_inventory_not_missing(self):
        c=control('file_present'); c['verification']['paths']=['README.md']; self.assertEqual(execute(c,snapshot(complete=False),{})[0],'NOT_VERIFIABLE')
    def test_symlink_requires_review(self):
        c=control('file_present'); c['verification']['paths']=['README.md']; self.assertEqual(execute(c,snapshot({'README.md':{'kind':'symlink'}}),{})[0],'MANUAL_REVIEW')
    def test_403_not_a_pass(self):
        s=snapshot(); s['observations']['repository']={'status':'HTTP_ERROR','http_status':403}; self.assertEqual(execute(CAT[0],s,{})[0],'ERROR')
    def test_missing_endpoint_not_a_pass(self): self.assertEqual(execute(CAT[0],{'observations':{}},{})[0],'NOT_ASSESSED')
    def test_missing_field_unknown(self):
        s=snapshot(); s['observations']['repository']['data'].pop('description'); self.assertEqual(execute(CAT[0],s,{})[0],'NOT_VERIFIABLE')
    def test_name_policy(self): self.assertEqual(execute(control('repo_name'),snapshot(),{})[0],'PASS')
    def test_name_rejects_underscores(self):
        s=snapshot(); s['observations']['repository']['data']['name']='bad_name'; self.assertEqual(execute(control('repo_name'),s,{})[0],'FAIL')
    def workflow(self,body): return snapshot({'.github/workflows/ci.yml':body})
    def test_pinned_workflow(self): self.assertEqual(execute(control('workflow_pinning'),self.workflow('jobs:\n  test:\n    steps:\n      - uses: actions/checkout@'+'a'*40),{})[0],'PASS')
    def test_pinning_syntax_is_not_provenance(self):
        ctrl = control('workflow_pinning')
        ctrl['verification']['require_provenance_review'] = True
        report = execute(ctrl, self.workflow('jobs:\n  test:\n    steps:\n      - uses: actions/checkout@'+'a'*40), {})
        self.assertEqual(report[0], 'MANUAL_REVIEW')

    def test_provenance_requirement_does_not_hide_floating_reference(self):
        ctrl = control('workflow_pinning')
        ctrl['verification']['require_provenance_review'] = True
        self.assertEqual(execute(ctrl, self.workflow('jobs:\n  test:\n    steps:\n      - uses: actions/checkout@v4'), {})[0], 'FAIL')
    def test_floating_action_fails(self): self.assertEqual(execute(control('workflow_pinning'),self.workflow('jobs:\n  test:\n    steps:\n      - uses: actions/checkout@v4'),{})[0],'FAIL')
    def test_floating_reusable_workflow_fails(self): self.assertEqual(execute(control('workflow_pinning'),self.workflow('jobs:\n  test:\n    uses: org/repo/.github/workflows/test.yml@main'),{})[0],'FAIL')
    def test_container_digest(self): self.assertEqual(execute(control('workflow_pinning'),self.workflow('jobs:\n  test:\n    steps:\n      - uses: docker://alpine@sha256:'+'a'*64),{})[0],'PASS')
    def test_workflow_permission_missing(self): self.assertEqual(execute(control('workflow_permissions'),self.workflow('jobs: {}'),{})[0],'FAIL')
    def test_read_only_permissions(self): self.assertEqual(execute(control('workflow_permissions'),self.workflow('permissions:\n  contents: read\njobs: {}'),{})[0],'PASS')
    def test_write_permissions_fail(self): self.assertEqual(execute(control('workflow_permissions'),self.workflow('permissions: write-all\njobs: {}'),{})[0],'FAIL')
    def test_invalid_yaml_fails(self): self.assertEqual(execute(control('workflow_permissions'),self.workflow('jobs: ['),{})[0],'FAIL')
    def test_absent_workflows_not_vacuous_pass(self): self.assertEqual(execute(control('workflow_pinning'),snapshot(),{})[0],'FAIL')
    def test_no_rulesets_does_not_ignore_legacy(self):
        c=control('effective_rule'); c['verification']['rule_type']='pull_request'; s=snapshot(); s['observations']['effective_branch_rules']={'status':'OK','data':[]}; self.assertEqual(execute(c,s,{})[0],'NOT_VERIFIABLE')
    def test_rules_threshold(self):
        c=control('effective_rule'); c['verification'].update(rule_type='pull_request',parameter='required_approving_review_count',operator='at_least',profile_parameter='required_reviews'); s=snapshot(); s['observations']['effective_branch_rules']={'status':'OK','data':[{'type':'pull_request','parameters':{'required_approving_review_count':1}}]}; self.assertEqual(execute(c,s,{'required_reviews':2})[0],'FAIL'); self.assertEqual(execute(c,s,{'required_reviews':1})[0],'PASS')
    def test_dependabot_config_present(self):
        c=control('dependabot_config')
        s=snap_with_extra({'dependabot_config':{'status':'OK','data':{'content':'version: 2\nupdates:\n  - package-ecosystem: pip\n    directory: /\n    schedule:\n      interval: weekly\n','encoding':'utf-8'}}})
        self.assertEqual(execute(c,s,{})[0],'PASS')
    def test_dependabot_config_missing(self):
        c=control('dependabot_config')
        s=snap_with_extra({'dependabot_config':{'status':'HTTP_ERROR','http_status':404}})
        self.assertEqual(execute(c,s,{})[0],'FAIL')
    def test_dependabot_config_error(self):
        c=control('dependabot_config')
        s=snap_with_extra({'dependabot_config':{'status':'ERROR','reason':'Transport failure'}})
        self.assertEqual(execute(c,s,{})[0],'ERROR')
    def test_actions_permissions_read_only(self):
        c=control('actions_permissions')
        s=snap_with_extra({'actions_permissions':{'status':'OK','data':{'enabled':True,'allowed_actions':'selected'}}})
        self.assertEqual(execute(c,s,{})[0],'PASS')
    def test_actions_permissions_all_allowed(self):
        c=control('actions_permissions')
        s=snap_with_extra({'actions_permissions':{'status':'OK','data':{'enabled':True,'allowed_actions':'all'}}})
        self.assertEqual(execute(c,s,{})[0],'FAIL')
    def test_actions_permissions_disabled(self):
        c=control('actions_permissions')
        s=snap_with_extra({'actions_permissions':{'status':'OK','data':{'enabled':False}}})
        self.assertEqual(execute(c,s,{})[0],'FAIL')
    def test_deploy_keys_none(self):
        c=control('deploy_keys')
        s=snap_with_extra({'deploy_keys':{'status':'OK','data':[]}})
        self.assertEqual(execute(c,s,{})[0],'PASS')
    def test_deploy_keys_write_access(self):
        c=control('deploy_keys')
        s=snap_with_extra({'deploy_keys':{'status':'OK','data':[{'key':'ssh-rsa AAAA...','read_only':False,'verified':True}]}})
        self.assertEqual(execute(c,s,{})[0],'FAIL')
    def test_deploy_keys_unverified(self):
        c=control('deploy_keys')
        s=snap_with_extra({'deploy_keys':{'status':'OK','data':[{'key':'ssh-rsa AAAA...','read_only':True,'verified':False}]}})
        self.assertEqual(execute(c,s,{})[0],'FAIL')
    def test_deploy_keys_valid(self):
        c=control('deploy_keys')
        s=snap_with_extra({'deploy_keys':{'status':'OK','data':[{'key':'ssh-rsa AAAA...','read_only':True,'verified':True}]}})
        self.assertEqual(execute(c,s,{})[0],'PASS')
    def test_codeowners_validation_missing(self):
        c=control('codeowners_validation')
        s=snap_with_extra({'codeowners':{'status':'HTTP_ERROR','http_status':404}})
        self.assertEqual(execute(c,s,{})[0],'FAIL')
    def test_codeowners_validation_empty(self):
        c=control('codeowners_validation')
        s=snap_with_extra({'codeowners':{'status':'OK','data':{'content':'','encoding':'base64'}}})
        self.assertEqual(execute(c,s,{})[0],'FAIL')
    def test_codeowners_validation_invalid(self):
        c=control('codeowners_validation')
        s=snap_with_extra({'codeowners':{'status':'OK','data':{'content':'IyBDb21tZW50IG9ubHk=','encoding':'base64'}}})
        self.assertEqual(execute(c,s,{})[0],'FAIL')
    def test_codeowners_validation_valid(self):
        c=control('codeowners_validation')
        content='*.py @team/backend\n*.md @team/docs\n'
        import base64
        encoded=base64.b64encode(content.encode()).decode()
        s=snap_with_extra({'codeowners':{'status':'OK','data':{'content':encoded,'encoding':'base64'}}})
        self.assertEqual(execute(c,s,{})[0],'PASS')
    def test_code_scanning_alerts_none(self):
        c=control('code_scanning_alerts')
        s=snap_with_extra({'code_scanning_alerts':{'status':'OK','data':[]}})
        self.assertEqual(execute(c,s,{})[0],'PASS')
    def test_code_scanning_alerts_with_critical(self):
        c=control('code_scanning_alerts')
        s=snap_with_extra({'code_scanning_alerts':{'status':'OK','data':[{'rule':{'severity':'critical'}},{'rule':{'severity':'high'}}]}})
        self.assertEqual(execute(c,s,{})[0],'FAIL')
    def test_secret_scanning_alerts_none(self):
        c=control('secret_scanning_alerts')
        s=snap_with_extra({'secret_scanning_alerts':{'status':'OK','data':[]}})
        self.assertEqual(execute(c,s,{})[0],'PASS')
    def test_secret_scanning_alerts_present(self):
        c=control('secret_scanning_alerts')
        s=snap_with_extra({'secret_scanning_alerts':{'status':'OK','data':[{'secret':'ghp_xxx'}]}})
        self.assertEqual(execute(c,s,{})[0],'FAIL')
    def test_dependabot_alerts_none(self):
        c=control('dependabot_alerts')
        s=snap_with_extra({'dependabot_alerts':{'status':'OK','data':[]}})
        self.assertEqual(execute(c,s,{})[0],'PASS')
    def test_dependabot_alerts_critical_high(self):
        c=control('dependabot_alerts')
        s=snap_with_extra({'dependabot_alerts':{'status':'OK','data':[{'security_advisory':{'severity':'critical'}},{'security_advisory':{'severity':'high'}}]}})
        self.assertEqual(execute(c,s,{})[0],'FAIL')
    def test_403_manual_review(self):
        c=control('code_scanning_alerts')
        s=snap_with_extra({'code_scanning_alerts':{'status':'HTTP_ERROR','http_status':403}})
        self.assertEqual(execute(c,s,{})[0],'MANUAL_REVIEW')

class Assessment(unittest.TestCase):
    def test_manual_is_not_pass(self): self.assertEqual(audit([control()],snapshot(),PROFILE,at=AT)['results'][0]['outcome'],'MANUAL_REVIEW')
    def test_stale_not_pass(self):
        s=snapshot(); s['observed_at']='2026-09-01T00:00:00Z'; self.assertEqual(audit([CAT[0]],s,PROFILE,at=AT)['results'][0]['outcome'],'STALE')
    def test_future_not_pass(self):
        s=snapshot(); s['observed_at']='2027-01-01T00:00:00Z'; self.assertEqual(audit([CAT[0]],s,PROFILE,at=AT)['results'][0]['outcome'],'ERROR')
    def test_no_revision_error(self):
        s=snapshot(); s.pop('target_revision'); self.assertEqual(audit([CAT[0]],s,PROFILE,at=AT)['results'][0]['outcome'],'ERROR')
    def attestation(self): return {'control_id':CAT[0]['id'],'control_revision':1,'target':'owner/repo','target_revision':'a'*40,'reviewer':'owner','reviewed_at':AT,'expires_at':'2026-10-02T00:00:00Z','rationale':'Inspected relevant artifact','evidence_ref':'evidence/receipt.json','outcome':'PASS'}
    def test_authorized_attestation(self): self.assertEqual(audit([control()],snapshot(),PROFILE,at=AT,attestations=[self.attestation()])['results'][0]['outcome'],'PASS')
    def test_foreign_reviewer_rejected(self):
        a=self.attestation(); a['reviewer']='outsider'; self.assertEqual(audit([control()],snapshot(),PROFILE,at=AT,attestations=[a])['results'][0]['outcome'],'MANUAL_REVIEW')
    def test_wrong_revision_attestation_rejected(self):
        a=self.attestation(); a['target_revision']='b'*40; self.assertEqual(audit([control()],snapshot(),PROFILE,at=AT,attestations=[a])['results'][0]['outcome'],'MANUAL_REVIEW')
    def test_expired_attestation_rejected(self):
        a=self.attestation(); a['expires_at']=AT; self.assertEqual(audit([control()],snapshot(),PROFILE,at=AT,attestations=[a])['results'][0]['outcome'],'MANUAL_REVIEW')
    def test_unknown_denominator(self):
        c=control(); c['applicability']={'x':True}; r=audit([c],snapshot(),PROFILE,at=AT); self.assertEqual(r['summary']['unknown_applicability'],1); self.assertIsNone(r['summary']['pass_rate']); self.assertFalse(gate(r)[0])
    def test_empty_gate_fails(self): self.assertFalse(gate({'results':[]})[0])
    def test_draft_release_gate_fails(self): self.assertFalse(gate(audit([CAT[0]],snapshot(),PROFILE,at=AT),require_accepted=True)[0])
    def test_missing_control_result_fails(self):
        r=audit(CAT[:2],snapshot(),PROFILE,at=AT); r['results'].pop(); self.assertFalse(gate(r,expected_controls=CAT[:2])[0])
    def test_catalog_tamper_fails(self):
        r=audit([CAT[0]],snapshot(),PROFILE,at=AT); r['catalog_digest']='bad'; self.assertFalse(gate(r,expected_controls=[CAT[0]])[0])
    def test_exception_does_not_rewrite_failure(self):
        s=snapshot(); s['observations']['repository']['data']['description']=''; e={'control_id':CAT[0]['id'],'control_revision':1,'target':'owner/repo','approved_by':'owner','approved_at':AT,'expires_at':'2026-10-02T00:00:00Z','reason':'Planned repair','compensating_control':'Documented purpose elsewhere'}; r=audit([CAT[0]],s,PROFILE,at=AT,exceptions=[e]); self.assertEqual(r['results'][0]['outcome'],'FAIL'); self.assertFalse(gate(r)[0]); self.assertTrue(gate(r,allow_exceptions=True)[0])
    def test_exception_cannot_hide_missing_observation(self):
        e={'control_id':CAT[0]['id'],'control_revision':1,'target':'owner/repo','approved_by':'owner','approved_at':AT,'expires_at':'2026-10-02T00:00:00Z','reason':'test','compensating_control':'test'}; s=snapshot(); s['observations']={}; self.assertFalse(gate(audit([CAT[0]],s,PROFILE,at=AT,exceptions=[e]),allow_exceptions=True)[0])

class RenderingAndCorpus(unittest.TestCase):
    def test_generation_is_deterministic(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td); generate(CAT,p); one=(p/'functional-checklist.md').read_bytes(); generate(CAT,p); self.assertEqual(one,(p/'functional-checklist.md').read_bytes())
    def test_missing_template_variable_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaises(ValueError): render_template(ROOT,'templates/README.md',{},Path(td)/'README.md')
    def test_template_no_overwrite(self):
        with tempfile.TemporaryDirectory() as td:
            dest=Path(td)/'pr.md'; dest.write_text('existing')
            with self.assertRaises(FileExistsError): render_template(ROOT,'templates/pull_request_template.md',{},dest)
    def test_bad_json_template_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            r=Path(td); (r/'t.json').write_text('{"name":"{{NAME}}"}')
            with self.assertRaises(ValueError): render_template(r,'t.json',{'NAME':'"broken'},r/'out.json')
    def test_blocks_track_line_ranges(self):
        b=list(blocks('# Heading\n\n- rule one\n- rule two\n\n```py\nx=1\n```\n')); self.assertEqual([x['start_line'] for x in b],[3,4,6]); self.assertEqual(b[-1]['kind'],'code_example')
    def test_source_import_is_not_semantic_review(self):
        with tempfile.TemporaryDirectory() as td:
            r=Path(td); s=r/'source'; s.mkdir(); text='# Heading\n\nMust test.\n'; rec={'source':'org/repo','commit':'a'*40,'path':'README.md','sha256':hashlib.sha256(text.encode()).hexdigest(),'kind':'text','retrieval_status':'RETRIEVED','url':'https://github.com/org/repo/blob/'+('a'*40)+'/README.md'}; dump(s/'r.inventory.json',[rec]);
            with gzip.open(s/'r.text.jsonl.gz','wt') as f: f.write(json.dumps({**rec,'content':text})+'\n')
            out=r/'out'; report=build_corpus(s,out); self.assertEqual(report['semantic_review_numerator'],0); self.assertNotIn('"text":',(out/'candidates.jsonl').read_text()); self.assertEqual(report['total_artifacts'],1)
    def test_hash_mismatch_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            r=Path(td); rec={'source':'org/repo','commit':'a'*40,'path':'README.md','sha256':'bad','url':'example','kind':'text'}; dump(r/'r.inventory.json',[rec]);
            with gzip.open(r/'r.text.jsonl.gz','wt') as f: f.write(json.dumps({**rec,'content':'Changed'})+'\n')
            with self.assertRaises(ValueError): build_corpus(r,r/'out')
    def test_upstream_changes_reopen_controls(self):
        with tempfile.TemporaryDirectory() as td:
            r=Path(td); s=CAT[0]['sources'][0]; a={'source':s['repository'],'path':s['path'],'sha256':'old'}; (r/'old').write_text(json.dumps(a)); a['sha256']='new'; (r/'new').write_text(json.dumps(a)); self.assertIn(CAT[0]['id'],impact(r/'old',r/'new',CAT)['changes'][0]['reopen_controls'])

if __name__=='__main__': unittest.main()
