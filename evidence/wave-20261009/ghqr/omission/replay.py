"""Read-only GHQR source/predicate evidence binding replay; upstream is data only."""
import argparse,gzip,hashlib,json,subprocess
from pathlib import Path
import yaml
p=argparse.ArgumentParser()
p.add_argument("--repository",type=Path,required=True)
p.add_argument("--packet",type=Path,required=True)
p.add_argument("--cache",type=Path,required=True)
a=p.parse_args()
sha=lambda b:hashlib.sha256(b).hexdigest()
load=lambda p:json.loads(p.read_bytes())
digest=lambda x:sha(json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode())
assignment=json.loads(subprocess.check_output(["git","show","18abc10:evidence/wave-20261009/ghqr/assignment.json"],cwd=a.repository))
source={x["path"]:x for x in map(json.loads,gzip.open(a.cache/"sources/microsoft__ghqr.text.jsonl.gz","rt"))}
claims={x["claim_id"]:x for x in assignment["claims"]}
occ={x["requirement_id"]:x for x in load(a.cache/"corpus/structured-source-requirements.json")}
primary=load(a.packet/"primary-review.json")
assert len(primary)==14
for row in primary:
    subject=row["claim"]
    claim=claims[subject["claim_id"]]
    text=source[subject["path"]]["content"]
    assert sha(text.encode())==subject["content_sha256"]
    assert sha(claim["statement"].encode())==subject["statement_sha256"]
    assert digest(occ[row["occurrence_id"]])==row["occurrence_digest"]
    definitions={r["id"]:r for r in yaml.safe_load(text)}
    assert sha(definitions[claim["source_id"]]["recommendation"].encode())==row["source_recommendation_sha256"]
for row in load(a.packet/"occurrence-crosswalk.json"):
    s=row["claim"]
    text=source[s["path"]]["content"]
    assert sha("\n".join(text.splitlines()[s["start_line"]-1:s["end_line"]]).encode())==row["source_span_sha256"]
for dep in assignment["dependencies"]:
    assert sha(source[dep["path"]]["content"].encode())==dep["sha256"]
for item in load(a.packet/"packet-manifest.json")["files"]:
    assert sha((a.packet/item["path"]).read_bytes())==item["sha256"]
    exact=subprocess.check_output(["git","show","2ad83ba6a3029eebadfd9c97e80cf6def8e98234:evidence/wave-20261009/ghqr/source/"+item["path"]],cwd=a.repository)
    assert sha(exact)==item["sha256"]
print(json.dumps({"result":"PASS","source_claims_and_occurrences_bound":14,"scanner_bindings":1,"upstream_executed":False,"native_predicates_verified":0}))
