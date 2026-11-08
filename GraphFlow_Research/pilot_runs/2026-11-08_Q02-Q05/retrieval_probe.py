"""Reuse Q01 ranker on fixed Vietnamese development queries; stdlib only."""
import argparse
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
VAULT = PROJECT / "GraphFlow_Research_Vault"
PREVIOUS = HERE.parent / "2026-11-08_Q01"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def hashes(root):
    return {p.relative_to(root).as_posix(): sha(p) for p in sorted(root.rglob("*")) if p.is_file()}


def write(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--freeze", action="store_true")
    args = parser.parse_args()
    protocol_file = HERE / "protocol.json"
    baseline_file = HERE / "baseline_snapshot.json"
    current = {"vault_files": hashes(VAULT), "q01_files": hashes(PREVIOUS),
               "protocol_sha256": sha(protocol_file)}
    if args.freeze:
        if baseline_file.exists():
            raise SystemExit("Do not overwrite frozen baseline; create another run.")
        write(baseline_file, current)
        print("Frozen vault, prior pilot, and protocol.")
        return
    if json.loads(baseline_file.read_text(encoding="utf-8")) != current:
        raise SystemExit("Frozen inputs changed; open a new run instead of silently replacing the baseline.")
    spec = importlib.util.spec_from_file_location("q01_probe", PREVIOUS / "retrieval_probe.py")
    ranker = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ranker)
    docs = ranker.corpus()
    protocol = json.loads(protocol_file.read_text(encoding="utf-8"))
    rows = []
    for query in protocol["queries"]:
        top = ranker.rank(query["query"], docs, protocol["k"])
        found = sorted(set(query["relevant"]) & {hit["id"] for hit in top})
        rows.append({**query, "top_k": top, "relevant_found": found, "hit": bool(found)})
    result = {"run_id": protocol["run_id"], "protocol_sha256": sha(protocol_file),
              "script_sha256": sha(Path(__file__)), "ranker_sha256": sha(PREVIOUS / "retrieval_probe.py"),
              "baseline_unchanged": True, "corpus_notes": len(docs), "k": protocol["k"],
              "queries_with_hit": sum(row["hit"] for row in rows), "total_queries": len(rows),
              "rows": rows, "generator_tested": False,
              "limitations": ["Development queries and relevance labels authored by the same agent.",
                              "A retrieved question note is not sufficient scientific evidence.",
                              "Different query set from Q01; do not interpret the difference as an improvement rate."]}
    write(HERE / "retrieval_results.json", result)
    print(json.dumps({"corpus_notes": len(docs), "hits": result["queries_with_hit"], "of": len(rows),
                      "top5": {row["id"]: [hit["id"] for hit in row["top_k"]] for row in rows}}, indent=2))


if __name__ == "__main__":
    main()
