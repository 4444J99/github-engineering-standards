"""Read-only independent span and identity replay; emits no upstream expressions."""
import argparse, gzip, hashlib, json
from pathlib import Path

def sha(value):
    return hashlib.sha256(value).hexdigest()

def digest(value):
    return sha(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode())

parser = argparse.ArgumentParser()
parser.add_argument("--repository", type=Path, required=True)
parser.add_argument("--source-packet", type=Path, required=True)
parser.add_argument("--publication-packet", type=Path, required=True)
parser.add_argument("--cache", type=Path, required=True)
parser.add_argument("--candidate", type=Path, required=True)
a = parser.parse_args()
load = lambda p: json.loads(p.read_bytes())
assignment = load(a.repository / "evidence/wave-20261009/assignment.json")
b = load(a.source_packet / "primary-review.json")
c = load(a.publication_packet)
wa = {x["path"]: x for x in map(json.loads, gzip.open(a.cache / "sources/github__github-well-architected.text.jsonl.gz", "rt"))}
ghqr = {x["path"]: x for x in map(json.loads, gzip.open(a.cache / "sources/microsoft__ghqr.text.jsonl.gz", "rt"))}
occ = {x["requirement_id"]: x for x in load(a.cache / "corpus/structured-source-requirements.json")}
claims = {x["claim_id"]: x for x in assignment["B"]["claims"]}
crosswalk = load(a.source_packet / "occurrence-crosswalk.json")
assert len(crosswalk) == len(claims) == 162
for row in crosswalk:
    cl = claims[row["claim"]["claim_id"]]
    assert [x["id"] for x in row["occurrences"]] == cl["structured_requirement_ids"]
    for o in row["occurrences"]:
        assert o["digest"] == digest(occ[o["id"]])
        assert o["start_line"] == cl["start_line"]
        assert o["end_line"] == cl["end_line"]
for row in b:
    cl = claims[row["claim_id"]]
    source = wa[cl["path"]]
    assert sha(source["content"].encode()) == cl["content_sha256"]
    span = "\n".join(source["content"].splitlines()[cl["start_line"]-1:cl["end_line"]]).encode()
    assert sha(span) == row["source_span_sha256"]
for dep in load(a.source_packet / "input-bindings.json")["context_artifacts"]:
    assert sha(wa[dep["path"]]["content"].encode()) == dep["sha256"]
queue = load(a.candidate / "controls/review_queue.json")
selected = [x["proposal_id"] for x in assignment["C"]["selected_proposals"]]
assert [x["proposal_id"] for x in c["proposal_reviews"]] == selected
for use in c["uses"]:
    out = (a.candidate / use["output_path"]).read_bytes()
    r = use["output_range"]
    ob = out[r["start_byte"]:r["end_byte"]]
    assert sha(ob) == r["sha256"]
    value = queue
    for token in use["json_pointer"].split("/")[1:]:
        value = value[int(token)] if isinstance(value, list) else value[token]
    assert json.loads(b'"' + ob + b'"') == value
    source = ghqr[use["source"]["path"]]
    sb = source["content"].encode()
    assert sha(sb) == use["source"]["sha256"]
    assert source["commit"] == use["source"]["commit"]
    r = use["source_range"]
    if r:
        span = sb[r["start_byte"]:r["end_byte"]]
        assert sha(span) == r["sha256"]
        if use["kind"] == "LICENSED_COPY":
            assert span == ob
    for attribution in use["attributions"]:
        ab = (a.candidate / attribution["output_path"]).read_bytes()
        r = attribution["output_range"]
        assert sha(ab[r["start_byte"]:r["end_byte"]]) == r["sha256"]
print(json.dumps({"crosswalk_claims_checked": len(crosswalk), "source_semantic_span_bindings_checked": len(b), "source_context_bindings_checked": 4, "publication_proposals_checked": len(selected), "publication_uses_checked": len(c["uses"]), "license_copy_equalities_checked": sum(u["kind"] == "LICENSED_COPY" for u in c["uses"]), "structural_result": "PASS", "semantic_and_rights_approval": False}, sort_keys=True))
