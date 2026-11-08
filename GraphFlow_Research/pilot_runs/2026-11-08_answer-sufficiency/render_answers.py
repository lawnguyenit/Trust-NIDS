"""Render saved actual answers and their packet evidence; no answer generation."""
import argparse
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def render(document_name="answers.json"):
    document = json.loads((HERE / document_name).read_text(encoding="utf-8"))
    protocol = json.loads((HERE / "protocol.json").read_text(encoding="utf-8"))
    packets = json.loads((HERE / "packets.json").read_text(encoding="utf-8"))
    repaired = document_name == "repair_answers.json"
    if repaired:
        repair = json.loads((HERE / "repair_results.json").read_text(encoding="utf-8"))
        packets["packet_ids"]["augmented"] = {r["id"]: r["combined_packet_ids"] for r in repair["rows"]}
    questions = {q["id"]: q for q in protocol["questions"]}
    lines = ["# " + ("Hai câu trả lời sau một lượt tìm bổ sung" if repaired else "Mười hai câu trả lời từ packet đã lưu"), "",
             f'<!-- Generated from {document_name}, protocol.json and saved packets. -->', "",
             "**Tác giả và người tự rà là cùng AI.** Đây là câu trả lời tổng hợp thủ công chỉ dùng " + ("packet kết hợp sau lượt tìm bổ sung có giới hạn" if repaired else "top-5 của điều kiện augmented và policy context cố định") + ". Không phải đầu ra của một generator riêng hoặc điểm semantic accuracy được chấm độc lập.", "",
             "Đoạn trích dưới đây là từ **note/card dẫn xuất trong packet**, không được trình bày như trích nguyên văn paper. Metadata nguồn/phiên bản/vị trí và lineage nằm trong [cards.json](cards.json); " + ("packet kết hợp nằm trong [repair_results.json](repair_results.json)." if repaired else "packet gốc nằm trong [packets.json](packets.json)."), "",
             "[Tổng quan kết quả](README.md) · [Protocol đã đóng băng](protocol.json)", ""]
    if repaired:
        lines.extend(["Đây là lượt adaptive repair có giới hạn, do cùng AI viết lại truy vấn sau khi biết ca thiếu. Không thay kết quả hoặc câu trả lời lượt đầu; không tính lại thành một điểm kiểm độc lập hoàn hảo. Xem [repair_protocol.json](repair_protocol.json).", ""])
    for answer in document["answers"]:
        question = questions[answer["id"]]
        lines.extend([f'## {answer["id"]} — `{answer["status"]}`', "", question["question"], "",
                      "**Trả lời:** " + answer["answer"], "", "**ID top-5 được cung cấp:** " + ", ".join(packets["packet_ids"]["augmented"][answer["id"]]) + ".", "",
                      "### Nhận định và đoạn hỗ trợ", ""])
        for assertion in answer["assertions"]:
            lines.extend([f'- `{assertion["epistemic_type"]}` — {assertion["text"]}'])
            for citation in assertion["support"]:
                lines.extend([f'  - **{citation["evidence_id"]}:** “{citation["excerpt"]}”'])
        lines.extend(["", "**Phần thiếu/giới hạn:** " + answer["gap"], "", "**Bước bổ sung riêng:** " + answer["next_action"], "",
                      "**Tự rà:** " + answer["self_review"], ""])
    return "\n".join(lines).rstrip() + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    for filename, owner in (("ANSWERS.md", "answers.json"), ("REPAIRED_ANSWERS.md", "repair_answers.json")):
        content = render(owner)
        path = HERE / filename
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                raise SystemExit(filename + " stale or missing")
        else:
            path.write_text(content, encoding="utf-8", newline="\n")
    print("Saved answer rendering " + ("matches JSON." if args.check else "created."))


if __name__ == "__main__":
    main()
