"""
run_golden_set.py — Chạy toàn bộ eval/golden_set.json qua ai_recall.recall(),
đối chiếu kết quả với expected_state/expected_citation_contains, rồi ghi
bảng thống kê + phân tích vào eval/run_results.md.

Chạy: python eval/run_golden_set.py
"""

import json
import sys
import os
import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "codebase"))
from ai_recall import recall  # noqa: E402


def evaluate_case(case: dict, result: dict) -> bool:
    if result.get("state") != case["expected_state"]:
        return False
    needle = case.get("expected_citation_contains")
    if needle:
        citation = result.get("citation") or ""
        if needle.strip("[]") in citation:
            return True
        # nếu needle là placeholder chưa thay (chứa "THAY" hoặc "mã đoạn"), coi là chưa kiểm được
        return False
    return True


def main():
    with open("eval/golden_set.json", encoding="utf-8") as f:
        data = json.load(f)

    rows = []
    passed = 0
    for case in data["cases"]:
        if "THAY" in case["query"]:
            rows.append((case["id"], "BỎ QUA", "-", "-", "Case chưa được thay bằng dữ liệu thật"))
            continue
        result = recall(case["query"])
        ok = evaluate_case(case, result)
        passed += int(ok)
        rows.append((
            case["id"],
            "ĐẠT" if ok else "KHÔNG ĐẠT",
            case["expected_state"],
            result.get("state"),
            "" if ok else f"Nhận '{result.get('state')}', trích dẫn '{result.get('citation')}'"
        ))

    total_run = len([r for r in rows if r[1] != "BỎ QUA"])
    rate = (passed / total_run * 100) if total_run else 0

    lines = []
    lines.append(f"# Kết quả chạy golden set — lượt {datetime.date.today().isoformat()}\n")
    lines.append(f"**Tổng số case:** {len(rows)} · **Đã chạy:** {total_run} · **Đạt:** {passed} · **Tỷ lệ đạt:** {rate:.0f}%\n")
    lines.append("| ID | Kết quả | Mong đợi | Thực tế | Ghi chú |")
    lines.append("|---|---|---|---|---|")
    for r in rows:
        lines.append(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} |")

    lines.append("\n## Phân tích nguyên nhân sai lệch\n")
    fails = [r for r in rows if r[1] == "KHÔNG ĐẠT"]
    if fails:
        for r in fails:
            lines.append(f"- **{r[0]}**: {r[4]}")
    else:
        lines.append("_Điền phân tích cụ thể tại đây sau khi chạy đủ 20 case thật._")

    with open("eval/run_results.md", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Đã ghi eval/run_results.md — {passed}/{total_run} đạt ({rate:.0f}%)")


if __name__ == "__main__":
    main()
