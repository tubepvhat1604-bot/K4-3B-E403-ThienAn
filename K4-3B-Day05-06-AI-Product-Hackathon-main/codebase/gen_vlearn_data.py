"""
gen_vlearn_data.py — Tách transcript thật trong data/vlearn-pack/transcript/
thành từng đoạn theo mã [Txx-NNN], xuất ra codebase/vlearn_data.json để giao
diện HTML (của bạn) load vào hiển thị Kho bài học + tìm kiếm phía client.

Chạy: python codebase/gen_vlearn_data.py
"""

import re
import os
import json
import glob

TRANSCRIPT_DIR = "data/vlearn-pack/transcript"
OUT_PATH = "codebase/vlearn_data.json"


def main():
    docs = []
    for path in sorted(glob.glob(f"{TRANSCRIPT_DIR}/*.md")):
        fname = os.path.basename(path)
        with open(path, encoding="utf-8") as f:
            text = f.read()

        pieces = re.split(r"(?=\*\*\[T\d{2}-\d{3}\]\*\*)", text)
        for piece in pieces:
            piece = piece.strip()
            if not piece:
                continue
            m = re.match(r"\*\*\[(T\d{2}-\d{3})\]\*\*\s*(.*)", piece, re.S)
            if not m:
                continue
            code, body = m.group(1), m.group(2).strip()
            title = (body[:60] + "…") if len(body) > 60 else body
            docs.append({
                "id": code,
                "title": title,
                "file": fname,
                "text": body,
            })

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(docs, f, ensure_ascii=False, indent=2)

    print(f"Đã tạo {OUT_PATH} — {len(docs)} đoạn kiến thức từ {len(glob.glob(f'{TRANSCRIPT_DIR}/*.md'))} transcript.")


if __name__ == "__main__":
    main()
