"""Check frozen inputs, evidence references, rendered notes and replayable probes.

Structural checks only; does not certify scientific truth, novelty or user acceptance.
"""
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]


def read(name):
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def main():
    spec = importlib.util.spec_from_file_location("pilot", HERE / "retrieval_probe.py")
    pilot = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(pilot)
    checks = {}
    frozen, protocol, registry, book = [read(x) for x in ("baseline_snapshot.json", "protocol.json", "sources.json", "casebook.json")]
    for path in HERE.glob("*.json"):
        json.loads(path.read_text(encoding="utf-8"))
    checks["json_parses"] = True
    checks["vault_unchanged"] = frozen["vault_files"] == pilot.hashes(pilot.VAULT)
    checks["q01_record_unchanged"] = frozen["q01_files"] == pilot.hashes(pilot.PREVIOUS)
    checks["protocol_unchanged"] = frozen["protocol_sha256"] == pilot.sha(HERE / "protocol.json")
    sources = {s["id"]: s for s in registry["sources"]}
    cases = {c["id"]: c for c in book["cases"]}
    claim_list = [claim for case in book["cases"] for claim in case["claims"]]
    claims = {c["id"]: c for c in claim_list}
    checks["ids_unique"] = len(sources) == len(registry["sources"]) and len(cases) == len(book["cases"]) and len(claims) == len(claim_list) and len({r["id"] for r in book["relations"]}) == len(book["relations"])
    checks["four_requested_cases"] = set(cases) == set(protocol["question_ids"]) == {"Q02", "Q03", "Q04", "Q05"}
    checks["source_identity_reading"] = all(s["title"] and s["authors"] and s["url"].startswith("https://") and s["version"] and s["locators"] and s["cautions"] and s["read_depth"] in {"abstract_primary", "sections_checked"} for s in sources.values())
    checks["claim_provenance_limits"] = all(c["source_ids"] and set(c["source_ids"]) <= set(sources) and c["locator"] and c["limitation"] and c["epistemic_type"] in {"author_reported", "reviewer_inference", "metadata_observation", "official_documentation"} and set(c.get("premise_claim_ids", [])) <= set(claims) for c in claims.values())
    checks["answers_resolve_to_claims"] = all(set(c["answer_claim_ids"]) <= {x["id"] for x in c["claims"]} and set(c["manual_probe"]["evidence_claim_ids"]) <= set(claims) and c["manual_probe"]["actual_answer"] and c["remaining_unknowns"] and c["novelty_status"] == "unverified" for c in cases.values())
    checks["relations_resolve"] = all(r["source"] in cases and r["target"] in set(cases) | {"Q01"} and set(r["claim_ids"]) <= set(claims) and r["reason"] and r["type"] for r in book["relations"])
    checks["no_false_approval_or_reproduction"] = all(x["human_review"] == "pending" and x["results_reproduced"] is False for x in (registry, book))
    checks["local_origins_exist"] = all((pilot.VAULT / "02_Papers" / (paper + ".md")).is_file() for c in cases.values() for paper in c["original_papers"]) and all((pilot.VAULT / "04_Claims" / (claim + ".md")).is_file() for c in cases.values() for claim in c["original_claims"])
    commands = []
    for script, result in (("retrieval_probe.py", "retrieval_results.json"), ("evidence_routing_probe.py", "evidence_routing_results.json")):
        before = pilot.sha(HERE / result)
        command = [sys.executable, "-B", str(HERE / script)]
        execution = subprocess.run(command, capture_output=True, text=True, encoding="utf-8")
        commands.append({"argv": command, "exit_code": execution.returncode})
        checks[script + "_replay"] = execution.returncode == 0 and before == pilot.sha(HERE / result)
        checks[script + "_hash_matches_output"] = read(result)["script_sha256"] == pilot.sha(HERE / script)
    routing = read("evidence_routing_results.json")
    checks["routing_scores_recomputed"] = routing["evaluable_queries"] == sum(row["evaluable"] for row in routing["rows"]) and routing["raw_evidence_hits"] == sum(row["raw_evidence_hit"] for row in routing["rows"]) and routing["filtered_evidence_hits"] == sum(row["filtered_evidence_hit"] for row in routing["rows"])
    render_command = [sys.executable, "-B", str(HERE / "render_casebook.py"), "--check"]
    execution = subprocess.run(render_command, capture_output=True, text=True, encoding="utf-8")
    commands.append({"argv": render_command, "exit_code": execution.returncode})
    checks["case_notes_match_json"] = execution.returncode == 0
    bad_links = []
    for note in HERE.glob("*.md"):
        for link in re.findall(r"\[[^\]]*\]\(([^)]+)\)", note.read_text(encoding="utf-8")):
            if not link.startswith(("https://", "http://", "#")) and not (note.parent / link.split("#")[0]).exists():
                bad_links.append(note.name + ": " + link)
    checks["local_links_resolve"] = not bad_links
    command = [sys.executable, str(pilot.VAULT / "13_Tools" / "validate_vault.py"), str(pilot.VAULT)]
    execution = subprocess.run(command, capture_output=True, text=True, encoding="utf-8")
    commands.append({"argv": command, "exit_code": execution.returncode})
    checks["original_vault_validator"] = execution.returncode == 0
    report = {"run_id": protocol["run_id"], "as_of": protocol["as_of"], "ok": all(checks.values()),
              "checks": checks, "commands": commands, "bad_local_links": bad_links,
              "counts": {"vault_files_preserved": len(frozen["vault_files"]), "q01_files_preserved": len(frozen["q01_files"]), "sources": len(sources), "claims": len(claims), "relations": len(book["relations"]), "cases": len(cases)},
              "vault_validator": json.loads(execution.stdout),
              "retrieval": {"raw_topic_hits": read("retrieval_results.json")["queries_with_hit"], "raw_total": read("retrieval_results.json")["total_queries"], "evidence_evaluable": routing["evaluable_queries"], "raw_evidence_hits": routing["raw_evidence_hits"], "filtered_evidence_hits": routing["filtered_evidence_hits"]},
              "limitations": ["Source references and generated-note consistency are structural, not independent scientific validation.", "Human approval pending; no paper result reproduced; no generator, detector or cloud deployment tested."]}
    pilot.write(HERE / "verification.json", report)
    print(json.dumps({"ok": report["ok"], "checks": checks, "counts": report["counts"], "retrieval": report["retrieval"]}, indent=2))
    raise SystemExit(0 if report["ok"] else 1)


if __name__ == "__main__":
    main()
