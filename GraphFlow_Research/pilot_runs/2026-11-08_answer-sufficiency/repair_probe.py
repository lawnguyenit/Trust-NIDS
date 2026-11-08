"""One adaptive, bounded evidence lookup; does not change parent questions or answers."""
import collections
import importlib.util
from pathlib import Path
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("probe", HERE / "run_probe.py")
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)


def main():
    if probe.read(HERE / "baseline_snapshot.json") != probe.frozen_inputs():
        raise SystemExit("Frozen inputs changed.")
    protocol = probe.read(HERE / "repair_protocol.json")
    parent = probe.read(HERE / "protocol.json")
    first = probe.read(HERE / "retrieval_results.json")
    first_packets = probe.read(HERE / "packets.json")
    engine = probe.ranker()
    originals = [d for d in engine.corpus() if d["id"][0] in "PKD"]
    cards = probe.package_cards()
    docs = originals + [{"id": c["id"], "path": "cards.json#" + c["id"], "body": probe.card_text(c),
                         "counts": collections.Counter(engine.tokens(probe.card_text(c)))} for c in cards]
    lookup = {d["id"]: d for d in docs}
    questions = {q["id"]: q for q in parent["questions"]}
    first_rows = {r["id"]: r for r in first["conditions"]["augmented"]["questions"]}
    rows, pool = [], {}
    for case in protocol["cases"]:
        key = case["id"]
        searches = [{"query": query, "top_k": engine.rank(query, docs, protocol["top_k_per_subquery"])} for query in case["subqueries"]]
        ids = list(first_packets["packet_ids"]["augmented"][key])
        for search in searches:
            for item in search["top_k"]:
                if item["id"] not in ids:
                    ids.append(item["id"])
        ids = ids[:protocol["max_combined_ids"]]
        facets = [{"id": f["id"], "matched_ids": sorted(set(ids) & set(f["alternatives"]))} for f in questions[key]["facets"]]
        rows.append({"id": key, "original_missing_facets": first_rows[key]["missing_reference_facets"],
                     "searches": searches, "combined_packet_ids": ids, "reference_facets": facets,
                     "all_reference_facets_retrieved": all(f["matched_ids"] for f in facets)})
        for evidence_id in ids:
            d = lookup[evidence_id]
            pool[evidence_id] = {"id": evidence_id, "path": d["path"], "text": d["body"]}
    result = {"run_id": protocol["run_id"], "repair_protocol_sha256": probe.sha(HERE / "repair_protocol.json"),
              "parent_results_sha256": probe.sha(HERE / "retrieval_results.json"),
              "parent_answers_sha256": probe.sha(HERE / "answers.json"), "script_sha256": probe.sha(Path(__file__)),
              "rows": rows, "evidence_pool": pool,
              "limits": ["Adaptive, label-informed query rewrites by the same assistant.",
                         "Fixed first-pass result retained; no independent performance claim."]}
    probe.write(HERE / "repair_results.json", result)
    print(__import__("json").dumps({"cases": [{"id": r["id"], "ids": r["combined_packet_ids"],
                                             "complete_reference_facets": r["all_reference_facets_retrieved"]} for r in rows]}, indent=2))


if __name__ == "__main__":
    main()
