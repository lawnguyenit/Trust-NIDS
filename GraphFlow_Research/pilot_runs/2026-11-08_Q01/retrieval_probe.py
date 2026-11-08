"""Read-only lexical diagnostic of the original vault; Python standard library only.

Not an embedding index, RAG pipeline, or independent relevance evaluation.
Run --freeze once before the first probe, then run without flags to reproduce it.
"""
import argparse
import collections
import hashlib
import json
import math
from pathlib import Path
import re
import unicodedata

HERE = Path(__file__).resolve().parent
VAULT = HERE.parents[1] / "GraphFlow_Research_Vault"
STOP = set("a an the is are was were do does have has be been can we our of or and for from to in on by with which what that this during not all how it if as at la cua va co khong cac cho mot trong duoc khi voi da thi de nay nhung".split())


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def snapshot():
    return {p.relative_to(VAULT).as_posix(): digest(p)
            for p in sorted(VAULT.rglob("*")) if p.is_file()}


def normalize(value):
    return "".join(c for c in unicodedata.normalize("NFD", value.lower())
                   if not unicodedata.combining(c)).replace("đ", "d")


def tokens(value):
    return [t for t in re.findall(r"[a-z0-9]+", normalize(value)) if t not in STOP]


def corpus():
    docs = []
    for path in sorted(VAULT.rglob("*.md")):
        if not re.fullmatch(r"[PCKRQD]\d+|S\d+_\w+", path.stem):
            continue
        raw = path.read_text(encoding="utf-8")
        body = raw.split("---\n", 2)[2] if raw.startswith("---\n") else raw
        docs.append({"id": path.stem, "path": path.relative_to(VAULT).as_posix(),
                     "body": body, "counts": collections.Counter(tokens(body))})
    return docs


def rank(query, docs, k):
    # BM25, k1=1.2, b=0.75; identical ranker and corpus for both conditions.
    terms = sorted(set(tokens(query)))
    avg = sum(sum(d["counts"].values()) for d in docs) / len(docs)
    df = {t: sum(t in d["counts"] for d in docs) for t in terms}
    ranked = []
    for d in docs:
        length = sum(d["counts"].values())
        score = 0.0
        for t in terms:
            freq = d["counts"][t]
            idf = math.log(1 + (len(docs) - df[t] + 0.5) / (df[t] + 0.5))
            score += idf * freq * 2.2 / (freq + 1.2 * (0.25 + 0.75 * length / avg))
        if score > 0:
            ranked.append({"id": d["id"], "path": d["path"], "score": round(score, 6)})
    return sorted(ranked, key=lambda d: (-d["score"], d["id"]))[:k]


def expand(query, glossary):
    normalized = normalize(query)
    additions = [value for key, value in glossary.items() if normalize(key) in normalized]
    return query + " " + " ".join(additions)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--freeze", action="store_true")
    args = parser.parse_args()
    protocol_path = HERE / "protocol.json"
    frozen_path = HERE / "baseline_snapshot.json"
    if args.freeze:
        if frozen_path.exists():
            raise SystemExit("Refusing to overwrite frozen baseline; create a new run instead.")
        frozen_path.write_text(json.dumps({"vault_files": snapshot(), "protocol_sha256": digest(protocol_path)},
                                         ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
        print("Frozen original vault and protocol.")
        return
    frozen = json.loads(frozen_path.read_text(encoding="utf-8"))
    if frozen["vault_files"] != snapshot() or frozen["protocol_sha256"] != digest(protocol_path):
        raise SystemExit("Baseline or protocol changed; do not silently rerun against a different corpus.")
    protocol = json.loads(protocol_path.read_text(encoding="utf-8"))
    docs = corpus()
    output = {"run_id": protocol["run_id"], "protocol_sha256": digest(protocol_path),
              "script_sha256": digest(Path(__file__)), "corpus_notes": len(docs),
              "unit": "note", "k": protocol["k"], "baseline_unchanged": True,
              "limitations": ["Six development queries; same agent authored glossary and relevance labels.",
                              "Retrieval relevance does not establish answer sufficiency or novelty.",
                              "No embeddings, generated answers, chunking, reranker, or automatic abstention tested."],
              "conditions": {}}
    for method in ("raw", "glossary_expanded"):
        rows = []
        for item in protocol["queries"]:
            query = item["query"] if method == "raw" else expand(item["query"], protocol["glossary"])
            hits = rank(query, docs, protocol["k"])
            found = sorted({h["id"] for h in hits} & set(item["relevant"]))
            rows.append({"id": item["id"], "query_used": query, "relevant": item["relevant"],
                         "top_k": hits, "relevant_found": found,
                         "hit": bool(found), "relevant_recall": len(found) / len(item["relevant"])})
        output["conditions"][method] = {"queries_with_hit": sum(r["hit"] for r in rows),
                                          "total_queries": len(rows),
                                          "mean_relevant_recall": sum(r["relevant_recall"] for r in rows) / len(rows),
                                          "rows": rows}
    destination = HERE / "retrieval_results.json"
    destination.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"corpus_notes": len(docs), "baseline_unchanged": True,
                      "conditions": {m: {"hits": c["queries_with_hit"], "of": c["total_queries"],
                                          "ranks": {r["id"]: [h["id"] for h in r["top_k"]] for r in c["rows"]}}
                                     for m, c in output["conditions"].items()}}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
