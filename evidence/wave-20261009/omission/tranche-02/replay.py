"""Read-only tranche 02 source identity replay."""
import argparse, gzip, hashlib, json
from pathlib import Path
p=argparse.ArgumentParser()
p.add_argument("--repository",type=Path,required=True)
p.add_argument("--packet",type=Path,required=True)
p.add_argument("--cache",type=Path,required=True)
a=p.parse_args()
sha=lambda b:hashlib.sha256(b).hexdigest()
load=lambda p:json.loads(p.read_bytes())
digest=lambda x:sha(json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode())
source={x["path"]:x for x in map(json.loads,gzip.open(a.cache/"sources/github__github-well-architected.text.jsonl.gz","rt"))}
claims={x["claim_id"]:x for x in load(a.repository/"evidence/wave-20261009/assignment.json")["B"]["claims"]}
occ={x["requirement_id"]:x for x in load(a.cache/"corpus/structured-source-requirements.json")}
primary=load(a.packet/"primary-review.json")
assert len(primary)==41
for row in primary:
    subject=row["claim"]
    claim=claims[subject["claim_id"]]
    text=source[subject["path"]]["content"]
    assert sha(text.encode())==subject["content_sha256"]
    assert sha("\n".join(text.splitlines()[subject["start_line"]-1:subject["end_line"]]).encode())==row["source_span_sha256"]
    assert sha(claim["statement"].encode())==subject["statement_sha256"]
for row in load(a.packet/"occurrence-crosswalk.json"):
    claim=claims[row["claim"]["claim_id"]]
    assert [x["id"] for x in row["occurrences"]]==claim["structured_requirement_ids"]
    for item in row["occurrences"]:
        assert digest(occ[item["id"]])==item["digest"]
        assert item["start_line"]==claim["start_line"]
        assert item["end_line"]==claim["end_line"]
for context in load(a.packet/"input-bindings.json")["context_read_spans"]:
    assert sha(source[context["path"]]["content"].encode())==context["content_sha256"]
for item in load(a.packet/"packet-manifest.json")["files"]:
    assert sha((a.packet/item["path"]).read_bytes())==item["sha256"]
print(json.dumps({"result":"PASS","source_claims_and_occurrences_bound":41,"contexts_bound":2,"semantic_approval":False}))
