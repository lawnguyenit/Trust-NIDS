"""Freeze and run a same-agent forward diagnostic; no model or network calls."""
import argparse
import collections
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
VAULT = PROJECT / "GraphFlow_Research_Vault"
Q01 = HERE.parent / "2026-11-08_Q01"
BATCH = HERE.parent / "2026-11-08_Q02-Q05"


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def hashes(root):
    return {p.relative_to(root).as_posix(): sha(p) for p in sorted(root.rglob("*")) if p.is_file()}


def frozen_inputs():
    return {"vault": hashes(VAULT), "q01": hashes(Q01), "q02_q05": hashes(BATCH),
            "protocol_sha256": sha(HERE / "protocol.json")}


def ranker():
    spec = importlib.util.spec_from_file_location("fixed_ranker", Q01 / "retrieval_probe.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def package_cards():
    first = read(Q01 / "evidence.json")
    second = read(BATCH / "casebook.json")
    registry = read(BATCH / "sources.json")
    groups = [("A", first["claims"], first["sources"], Q01 / "evidence.json")]
    groups.append(("B", [claim for case in second["cases"] for claim in case["claims"]], registry["sources"], BATCH / "casebook.json"))
    cards = []
    for prefix, claims, source_rows, origin_file in groups:
        sources = {s["id"]: s for s in source_rows}
        for claim in claims:
            selected = [{"id": prefix + "_" + s, "title": sources[s]["title"], "url": sources[s]["url"],
                         "version": sources[s]["version"], "read_depth": sources[s]["read_depth"],
                         "publication_status": sources[s]["publication_status"]} for s in claim["source_ids"]]
            cards.append({"id": prefix + "_" + claim["id"], "statement": claim["statement"],
                          "epistemic_type": claim["epistemic_type"], "locator": claim["locator"],
                          "limitation": claim["limitation"], "sources": selected,
                          "origin_path": origin_file.relative_to(PROJECT).as_posix(),
                          "origin_sha256": sha(origin_file), "origin_claim_id": claim["id"],
                          "human_review": "pending", "results_reproduced": False})
    return cards


def card_text(card):
    source_text = "\n".join(s["title"] + "; " + s["version"] for s in card["sources"])
    return (f'# {card["id"]}\n\nNhận định: {card["statement"]}\n\n'
            f'Loại: {card["epistemic_type"]}\n\nVị trí: {card["locator"]}\n\n'
            f'Giới hạn: {card["limitation"]}\n\nNguồn:\n{source_text}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--freeze", action="store_true")
    args = parser.parse_args()
    baseline_path = HERE / "baseline_snapshot.json"
    current = frozen_inputs()
    if args.freeze:
        if baseline_path.exists():
            raise SystemExit("Baseline exists; do not overwrite or redefine this trial.")
        write(baseline_path, current)
        print("Frozen questions/rubric, original vault and two prior pilots before retrieval.")
        return
    if read(baseline_path) != current:
        raise SystemExit("Frozen input changed. Use a new run instead of silently changing this one.")
    protocol = read(HERE / "protocol.json")
    engine = ranker()
    originals = [d for d in engine.corpus() if d["id"][0] in "PKD"]
    cards = package_cards()
    card_docs = [{"id": card["id"], "path": "cards.json#" + card["id"], "body": card_text(card),
                  "counts": collections.Counter(engine.tokens(card_text(card)))} for card in cards]
    corpora = {"original": originals, "augmented": originals + card_docs}
    evidence_pool = {}
    results = {"run_id": protocol["run_id"], "protocol_sha256": sha(HERE / "protocol.json"),
               "script_sha256": sha(Path(__file__)), "ranker_sha256": sha(Q01 / "retrieval_probe.py"),
               "conditions": {}, "generator_tested": False, "independent_judge": False}
    for condition, docs in corpora.items():
        ids = {d["id"] for d in docs}
        lookup = {d["id"]: d for d in docs}
        rows = []
        for question in protocol["questions"]:
            ranked = engine.rank(question["question"], docs, protocol["k"])
            retrieved = {d["id"] for d in ranked}
            facets = [{"id": f["id"], "reference_in_corpus": bool(ids & set(f["alternatives"])),
                       "reference_in_topk": bool(retrieved & set(f["alternatives"])),
                       "matched_ids": sorted(retrieved & set(f["alternatives"]))} for f in question["facets"]]
            missing = [f["id"] for f in facets if not f["reference_in_topk"]]
            rows.append({"id": question["id"], "question": question["question"], "kind": question["kind"],
                         "top_k": ranked, "reference_facets": facets,
                         "all_reference_facets_retrieved": all(f["reference_in_topk"] for f in facets) if facets else None,
                         "missing_reference_facets": missing,
                         "capture_gaps": [f["id"] for f in facets if not f["reference_in_corpus"]],
                         "retrieval_misses": [f["id"] for f in facets if f["reference_in_corpus"] and not f["reference_in_topk"]]})
            for item in ranked:
                document = lookup[item["id"]]
                if item["id"] not in evidence_pool:
                    evidence_pool[item["id"]] = {"id": item["id"], "path": document["path"], "text": document["body"],
                                                 "origin_kind": "pilot_claim_card" if item["id"].startswith(("A_", "B_")) else "original_vault_note"}
        results["conditions"][condition] = {"candidate_count": len(docs), "questions": rows,
                                             "scored_questions": sum(bool(q["facets"]) for q in protocol["questions"]),
                                             "complete_reference_packets": sum(row["all_reference_facets_retrieved"] is True for row in rows)}
    policy = [{"path": path, "sha256": sha(VAULT / path), "text": (VAULT / path).read_text(encoding="utf-8")} for path in protocol["fixed_policy_context"]]
    packets = {"run_id": protocol["run_id"], "policy_context": policy, "evidence_pool": evidence_pool,
               "packet_ids": {condition: {row["id"]: [item["id"] for item in row["top_k"]] for row in data["questions"]}
                              for condition, data in results["conditions"].items()},
               "answer_condition": "augmented", "warning": "Packet text is reviewer-derived evidence, not newly read full text or proof of scientific truth."}
    write(HERE / "cards.json", {"run_id": protocol["run_id"], "cards": cards})
    write(HERE / "retrieval_results.json", results)
    write(HERE / "packets.json", packets)
    print(json.dumps({condition: {"candidate_count": data["candidate_count"], "complete_reference_packets": data["complete_reference_packets"],
                                  "scored_questions": data["scored_questions"],
                                  "rows": [{"id": row["id"], "ids": [x["id"] for x in row["top_k"]],
                                            "missing": row["missing_reference_facets"], "capture_gaps": row["capture_gaps"]} for row in data["questions"]]}
                      for condition, data in results["conditions"].items()}, indent=2))


if __name__ == "__main__":
    main()
