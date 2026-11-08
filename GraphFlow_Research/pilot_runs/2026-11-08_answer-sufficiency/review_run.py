"""Validate lineage/packet citations and expose the limits of mechanical checking.

This is not a semantic judge or a model-quality benchmark.
"""
import copy
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("probe", HERE / "run_probe.py")
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)


def validate_answers(document, protocol, packets, results):
    errors = []
    questions = {q["id"]: q for q in protocol["questions"]}
    rows = {r["id"]: r for r in results["conditions"]["augmented"]["questions"]}
    policy = {"POLICY_EVIDENCE": packets["policy_context"][0]["text"],
              "POLICY_GATE": packets["policy_context"][1]["text"]}
    if document.get("condition") != "augmented" or document.get("human_review") != "pending":
        errors.append("wrong condition or false human approval")
    ids = [answer["id"] for answer in document["answers"]]
    if len(ids) != len(set(ids)) or set(ids) != set(questions):
        errors.append("question ID coverage or uniqueness")
    for answer in document["answers"]:
        key = answer["id"]
        if key not in questions:
            continue
        allowed = set(packets["packet_ids"]["augmented"][key]) | set(policy)
        complete = rows[key]["all_reference_facets_retrieved"]
        if answer["status"] == "scoped_supported" and complete is not True:
            errors.append(key + ": claiming full support despite missing reference facets")
        if questions[key].get("required_outcome"):
            expected = {"insufficient_no_local_experiment": "insufficient_no_local_experiment",
                        "insufficient_global_novelty": "insufficient_global_novelty",
                        "conflict_no_silent_selection": "conflict"}[questions[key]["required_outcome"]]
            if answer["status"] != expected:
                errors.append(key + ": violates predeclared abstention/conflict outcome")
        if not all(answer.get(field) for field in ("answer", "assertions", "gap", "next_action", "self_review")):
            errors.append(key + ": missing answer, caveat, support or follow-up")
        for assertion in answer["assertions"]:
            if not assertion.get("text") or not assertion.get("epistemic_type") or not assertion.get("support"):
                errors.append(key + ": empty assertion/support")
            for citation in assertion.get("support", []):
                evidence_id = citation["evidence_id"]
                if evidence_id not in allowed:
                    errors.append(key + ": citation outside packet: " + evidence_id)
                    continue
                text = policy[evidence_id] if evidence_id in policy else packets["evidence_pool"][evidence_id]["text"]
                if not citation.get("excerpt") or citation["excerpt"] not in text:
                    errors.append(key + ": excerpt not found in " + evidence_id)
    return errors


def main():
    protocol = probe.read(HERE / "protocol.json")
    packets = probe.read(HERE / "packets.json")
    results = probe.read(HERE / "retrieval_results.json")
    answers = probe.read(HERE / "answers.json")
    checks = {}
    checks["frozen_inputs_unchanged"] = probe.read(HERE / "baseline_snapshot.json") == probe.frozen_inputs()
    checks["cards_have_exact_lineage"] = probe.read(HERE / "cards.json")["cards"] == probe.package_cards()
    checks["cards_not_user_approved_or_reproduced"] = all(c["human_review"] == "pending" and c["results_reproduced"] is False for c in probe.read(HERE / "cards.json")["cards"])
    checks["protocol_hash_matches_results"] = results["protocol_sha256"] == probe.sha(HERE / "protocol.json")
    errors = validate_answers(answers, protocol, packets, results)
    checks["answer_mechanical_checks"] = not errors
    files = [HERE / name for name in ("cards.json", "packets.json", "retrieval_results.json")]
    before = {p.name: probe.sha(p) for p in files}
    command = [sys.executable, "-B", str(HERE / "run_probe.py")]
    replay = subprocess.run(command, capture_output=True, text=True, encoding="utf-8")
    checks["replay_succeeded"] = replay.returncode == 0
    checks["replay_identical"] = before == {p.name: probe.sha(p) for p in files}
    checks["current_script_hash_matches"] = results["script_sha256"] == probe.sha(HERE / "run_probe.py")
    controls = []
    mutations = [
        ("outside_packet", "N02", lambda a: a["assertions"][0]["support"].append({"evidence_id": "A_L04", "excerpt": "KnowHow"})),
        ("fabricated_excerpt", "N03", lambda a: a["assertions"][0]["support"][0].update(excerpt="NONEXISTENT_SUPPORT_FRAGMENT")),
        ("partial_labeled_complete", "N07", lambda a: a.update(status="scoped_supported")),
        ("conflict_silently_resolved", "N11", lambda a: a.update(status="scoped_supported"))
    ]
    for name, question_id, mutate in mutations:
        changed = copy.deepcopy(answers)
        answer = next(a for a in changed["answers"] if a["id"] == question_id)
        mutate(answer)
        control_errors = validate_answers(changed, protocol, packets, results)
        controls.append({"id": name, "origin": "manually injected validator control; not observed model output",
                         "mechanically_rejected": bool(control_errors), "errors": control_errors})
    checks["structural_negative_controls_rejected"] = all(c["mechanically_rejected"] for c in controls)
    semantic = copy.deepcopy(answers)
    changed_answer = next(a for a in semantic["answers"] if a["id"] == "N01")
    changed_answer["assertions"][0]["text"] = "CloudTrail trails mặc định đã ghi đầy đủ mọi data event."
    semantic_errors = validate_answers(semantic, protocol, packets, results)
    controls.append({"id": "valid_citation_wrong_assertion", "origin": "manually injected semantic control; not observed model output",
                     "mutated_text": changed_answer["assertions"][0]["text"],
                     "mechanically_rejected": bool(semantic_errors),
                     "same_agent_semantic_review": "Contradicts the unchanged cited K13 statement. Reject semantically even though IDs and quotes remain valid.",
                     "lesson": "Exact citation checks cannot establish entailment or answer correctness."})
    repair = probe.read(HERE / "repair_results.json")
    repaired_answers = probe.read(HERE / "repair_answers.json")
    repair_rows = {r["id"]: r for r in repair["rows"]}
    repair_errors = []
    for answer in repaired_answers["answers"]:
        row = repair_rows.get(answer["id"])
        if not row or not row["all_reference_facets_retrieved"]:
            repair_errors.append(answer["id"] + ": required facets not retrieved")
            continue
        for assertion in answer["assertions"]:
            for citation in assertion["support"]:
                if citation["evidence_id"] not in row["combined_packet_ids"]:
                    repair_errors.append(answer["id"] + ": outside repair packet")
                elif citation["excerpt"] not in repair["evidence_pool"][citation["evidence_id"]]["text"]:
                    repair_errors.append(answer["id"] + ": excerpt missing")
    checks["repair_citations_resolve"] = not repair_errors
    checks["repair_did_not_overwrite_first_answers"] = repair["parent_answers_sha256"] == probe.sha(HERE / "answers.json") and repair["parent_results_sha256"] == probe.sha(HERE / "retrieval_results.json")
    checks["repair_protocol_hash_matches"] = repair["repair_protocol_sha256"] == probe.sha(HERE / "repair_protocol.json")
    repair_before = probe.sha(HERE / "repair_results.json")
    repair_command = [sys.executable, "-B", str(HERE / "repair_probe.py")]
    repair_replay = subprocess.run(repair_command, capture_output=True, text=True, encoding="utf-8")
    checks["repair_replay_identical"] = repair_replay.returncode == 0 and repair_before == probe.sha(HERE / "repair_results.json")
    validator_command = [sys.executable, str(probe.VAULT / "13_Tools" / "validate_vault.py"), str(probe.VAULT)]
    validator = subprocess.run(validator_command, capture_output=True, text=True, encoding="utf-8")
    checks["original_vault_validator"] = validator.returncode == 0
    rendered = subprocess.run([sys.executable, "-B", str(HERE / "render_answers.py"), "--check"], capture_output=True, text=True, encoding="utf-8")
    checks["render_matches_answers"] = rendered.returncode == 0
    report = {"run_id": protocol["run_id"], "as_of": protocol["as_of"], "ok": all(checks.values()),
              "mechanical_checks": checks, "answer_errors": errors, "repair_errors": repair_errors, "controls": controls,
              "counts": {"questions": len(protocol["questions"]), "cards": len(probe.read(HERE / "cards.json")["cards"]),
                         "substantive_assertions_with_excerpt_links": sum(len(a["assertions"]) for a in answers["answers"]),
                         "vault_files_preserved": len(probe.hashes(probe.VAULT)), "q01_files_preserved": len(probe.hashes(probe.Q01)),
                         "q02_q05_files_preserved": len(probe.hashes(probe.BATCH))},
              "retrieval_reference_coverage": {name: {"complete_reference_packets": condition["complete_reference_packets"],
                                                       "scored_questions": condition["scored_questions"]}
                                                for name, condition in results["conditions"].items()},
              "commands": [{"argv": command, "exit_code": replay.returncode}, {"argv": repair_command, "exit_code": repair_replay.returncode}, {"argv": validator_command, "exit_code": validator.returncode}],
              "vault_validator": json.loads(validator.stdout),
              "semantic_review": {"mode": "Same assistant manually authored and reviewed answers; not independent.",
                                  "semantic_accuracy": None, "generator_tested": False,
                                  "limits": "Subset coverage and exact substrings do not prove source truth, completeness, entailment or model performance."}}
    # Write before checking local links so the report's own link has a real target.
    probe.write(HERE / "verification.json", report)
    bad_links = []
    for path in HERE.glob("*.md"):
        for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
            if not target.startswith(("https://", "http://", "#")) and not (path.parent / target.split("#")[0]).exists():
                bad_links.append(path.name + ": " + target)
    checks["local_links_resolve"] = not bad_links
    report["bad_local_links"] = bad_links
    report["ok"] = all(checks.values())
    probe.write(HERE / "verification.json", report)
    print(json.dumps({"ok": report["ok"], "mechanical_checks": checks, "counts": report["counts"],
                      "reference_coverage": report["retrieval_reference_coverage"], "semantic_control_mechanically_rejected": bool(semantic_errors)}, indent=2))
    raise SystemExit(0 if report["ok"] else 1)


if __name__ == "__main__":
    main()
