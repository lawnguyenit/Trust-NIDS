"""Adaptive development-only comparison; preserve the original query/relevance labels."""
import importlib.util
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("pilot", HERE / "retrieval_probe.py")
pilot = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pilot)


def main():
    protocol = json.loads((HERE / "protocol.json").read_text(encoding="utf-8"))
    frozen = json.loads((HERE / "baseline_snapshot.json").read_text(encoding="utf-8"))
    if frozen["vault_files"] != pilot.hashes(pilot.VAULT) or frozen["q01_files"] != pilot.hashes(pilot.PREVIOUS):
        raise SystemExit("Original inputs changed.")
    if frozen["protocol_sha256"] != pilot.sha(HERE / "protocol.json"):
        raise SystemExit("Protocol changed.")
    spec = importlib.util.spec_from_file_location("ranker", pilot.PREVIOUS / "retrieval_probe.py")
    ranker = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ranker)
    docs = ranker.corpus()
    candidates = [d for d in docs if d["id"][0] in "PKD"]
    rows = []
    for query in protocol["queries"]:
        labels = [x for x in query["relevant"] if x[0] in "PKD"]
        raw = ranker.rank(query["query"], docs, protocol["k"])
        filtered = ranker.rank(query["query"], candidates, protocol["k"])
        rows.append({"id": query["id"], "query": query["query"],
                     "evidence_labels_in_original_protocol": labels, "evaluable": bool(labels),
                     "raw_top5": [x["id"] for x in raw], "evidence_only_top5": [x["id"] for x in filtered],
                     "raw_evidence_hit": bool(set(labels) & {x["id"] for x in raw}),
                     "filtered_evidence_hit": bool(set(labels) & {x["id"] for x in filtered})})
    result = {"run_id": protocol["run_id"], "script_sha256": pilot.sha(Path(__file__)),
              "design_timing": "Adaptive diagnostic after raw retrieval; not preregistered or held-out. No relevance labels changed.",
              "change": "Restrict candidate note types to existing P/K/D; keep BM25, queries and note text unchanged.",
              "protocol_sha256": pilot.sha(HERE / "protocol.json"),
              "raw_candidate_notes": len(docs), "evidence_candidate_notes": len(candidates),
              "evaluable_queries": sum(r["evaluable"] for r in rows),
              "raw_evidence_hits": sum(r["raw_evidence_hit"] for r in rows),
              "filtered_evidence_hits": sum(r["filtered_evidence_hit"] for r in rows), "rows": rows,
              "limitations": ["T04B has only a question note in its original labels; evidence recovery not scored.",
                              "Type filtering is not an answer-sufficiency gate or production retriever.",
                              "Same-agent development queries and labels; no blinded validation."]}
    pilot.write(HERE / "evidence_routing_results.json", result)
    print(json.dumps({k: result[k] for k in ["evaluable_queries", "raw_evidence_hits", "filtered_evidence_hits"]}))


if __name__ == "__main__":
    main()
