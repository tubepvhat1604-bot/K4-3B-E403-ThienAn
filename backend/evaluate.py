"""Evaluate lecture retrieval against a user-provided golden set."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from config import MAX_TOP_K
from retrieval import SemanticRetriever


REQUIRED_COLUMNS = {"query", "expected_course_id", "expected_lecture_code"}


def evaluate(golden_set: Path) -> dict[str, float | int]:
    if not golden_set.is_file():
        raise FileNotFoundError(f"Không tìm thấy golden set: {golden_set}")
    cases = pd.read_csv(golden_set, dtype=str, keep_default_na=False, encoding="utf-8-sig")
    missing = sorted(REQUIRED_COLUMNS - set(cases.columns))
    if missing:
        raise ValueError("golden_set.csv thiếu cột: " + ", ".join(missing))
    cases = cases[cases["query"].str.strip().ne("")].copy()
    if cases.empty:
        raise ValueError("golden_set.csv không có query hợp lệ.")

    retriever = SemanticRetriever()
    retriever.initialize()
    top_1_correct = 0
    hit_at_3_correct = 0
    retrieval_size = min(MAX_TOP_K, 3)
    for _, case in cases.iterrows():
        expected = (case["expected_course_id"].strip(), case["expected_lecture_code"].strip())
        results = retriever.search(case["query"], retrieval_size)
        returned = [(hit.course_id, hit.lecture_code) for hit in results]
        top_1_correct += int(bool(returned) and returned[0] == expected)
        hit_at_3_correct += int(expected in returned[:3])

    total = len(cases)
    return {
        "cases": total,
        "top_1_accuracy": round(top_1_correct / total, 4),
        "hit_at_3": round(hit_at_3_correct / total, 4),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate VLearn semantic lecture retrieval")
    parser.add_argument("--golden-set", type=Path, required=True, help="CSV: query,expected_course_id,expected_lecture_code")
    args = parser.parse_args()
    try:
        print(json.dumps(evaluate(args.golden_set), ensure_ascii=False, indent=2))
    except (OSError, ValueError) as error:
        parser.error(str(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
