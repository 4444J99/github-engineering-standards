from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path
from .core import ROOT,dump,load,validate_controls
from .corpus import build_corpus,coverage_with_reviews,impact
from .evaluate import audit,gate
from .render import generate,render_template


def main(argv=None):
    p=argparse.ArgumentParser(description='GitHub Engineering Standards — no implicit writes to GitHub')
    p.add_argument('--catalog',type=Path,default=ROOT/'controls/catalog.json')
    sub=p.add_subparsers(dest='command',required=True)
    sub.add_parser('validate')
    c=sub.add_parser('sync'); c.add_argument('--output',type=Path,required=True); c.add_argument('--rendered',action='store_true'); c.add_argument('--rendered-limit',type=int,default=0); c.add_argument('--workers',type=int,default=4)
    c=sub.add_parser('compile'); c.add_argument('--output',type=Path,default=ROOT/'generated')
    c=sub.add_parser('corpus'); c.add_argument('--snapshots',type=Path,required=True); c.add_argument('--output',type=Path,required=True)
    c=sub.add_parser('ledger'); c.add_argument('--snapshots',type=Path,required=True); c.add_argument('--corpus',type=Path,required=True)
    c=sub.add_parser('coverage'); c.add_argument('--artifacts',type=Path,required=True); c.add_argument('--reviews',type=Path,required=True)
    c.add_argument('--candidates',type=Path,required=True); c.add_argument('--review-policy',type=Path,required=True)
    c=sub.add_parser('audit'); c.add_argument('--snapshot',type=Path,required=True); c.add_argument('--profile',type=Path,required=True)
    c.add_argument('--attestations',type=Path); c.add_argument('--exceptions',type=Path); c.add_argument('--output',type=Path,required=True)
    c=sub.add_parser('gate'); c.add_argument('--report',type=Path,required=True); c.add_argument('--allow-exceptions',action='store_true')
    c.add_argument('--require-accepted',action='store_true'); c.add_argument('--enforce-should',action='store_true')
    c=sub.add_parser('render'); c.add_argument('--template',required=True); c.add_argument('--parameters',type=Path,required=True); c.add_argument('--output',type=Path,required=True)
    c=sub.add_parser('impact'); c.add_argument('--old',type=Path,required=True); c.add_argument('--new',type=Path,required=True); c.add_argument('--output',type=Path,required=True)
    c=sub.add_parser('collect'); c.add_argument('--repository',required=True); c.add_argument('--output',type=Path,required=True); c.add_argument('--max-files',type=int,default=2000)
    c.add_argument('--include-org',action='store_true'); c.add_argument('--include-enterprise',action='store_true')
    c.add_argument('--enterprise-slug'); c.add_argument('--max-pages',type=int,default=100)
    c.add_argument('--ref',help='Repository branch to inspect; defaults to the default branch')
    args=p.parse_args(argv); controls=load(args.catalog)
    errors=validate_controls(controls)
    if errors: print(json.dumps({'validation_errors':errors},indent=2)); return 2
    if args.command=='validate': print(json.dumps({'valid':True,'controls':len(controls)})); return 0
    if args.command=='sync':
        from .sources import sync
        if args.rendered_limit<0 or not 1<=args.workers<=8: raise ValueError('Invalid acquisition bounds')
        report=sync(args.output,rendered=args.rendered,rendered_limit=args.rendered_limit,workers=args.workers)
        print(json.dumps(report,indent=2))
        docs=report.get('published_docs',{})
        failed=any(s.get('status')=='ERROR' or s.get('git_tree_reconciliation',{}).get('status')!='MATCH' for s in report['sources'])
        failed=failed or docs.get('status')=='ERROR' or not docs.get('versions')
        failed=failed or any(v.get('status')!='INVENTORIED' for v in docs.get('versions',[])) or bool(docs.get('rendered_errors'))
        return 2 if failed else 0
    if args.command=='compile': generate(controls,args.output)
    elif args.command=='corpus': print(json.dumps(build_corpus(args.snapshots,args.output),indent=2))
    elif args.command=='ledger':
        from .ledger import enrich
        print(json.dumps(enrich(args.snapshots,args.corpus,controls),indent=2))
    elif args.command=='coverage':
        candidates=[json.loads(line) for line in args.candidates.read_text().splitlines() if line.strip()]
        report=coverage_with_reviews(args.artifacts,args.reviews,candidates=candidates,controls=controls,
                                     authorized_reviewers=load(args.review_policy).get('authorized_reviewers',[]))
        print(json.dumps(report,indent=2)); return 2 if report['errors'] else 0
    elif args.command=='audit':
        report=audit(controls,load(args.snapshot),load(args.profile),attestations=load(args.attestations) if args.attestations else [],exceptions=load(args.exceptions) if args.exceptions else [])
        dump(args.output,report); print(json.dumps(report['summary'],indent=2))
    elif args.command=='gate':
        ok,reasons=gate(load(args.report),allow_exceptions=args.allow_exceptions,require_accepted=args.require_accepted,enforce_should=args.enforce_should,expected_controls=controls)
        print(json.dumps({'pass':ok,'blockers':reasons},indent=2)); return 0 if ok else 1
    elif args.command=='render': render_template(ROOT,args.template,load(args.parameters),args.output)
    elif args.command=='impact': dump(args.output,impact(args.old,args.new,controls))
    elif args.command=='collect':
        from .collect import collect
        if args.max_files<1 or args.max_files>10000: raise ValueError('max-files must be 1..10000')
        if not 1 <= args.max_pages <= 1000: raise ValueError('max-pages must be 1..1000')
        if args.enterprise_slug and not args.include_enterprise: raise ValueError('--enterprise-slug requires --include-enterprise')
        dump(args.output,collect(args.repository,max_files=args.max_files,include_org=args.include_org,
                                include_enterprise=args.include_enterprise,enterprise_slug=args.enterprise_slug,max_pages=args.max_pages,ref=args.ref))
    return 0

if __name__=='__main__':
    try: raise SystemExit(main())
    except (ValueError,OSError,KeyError,TypeError) as exc:
        print(json.dumps({'error':str(exc),'type':type(exc).__name__}),file=sys.stderr); raise SystemExit(2)
