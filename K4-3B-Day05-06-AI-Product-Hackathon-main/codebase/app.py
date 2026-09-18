"""
app.py — Server cho VLearn Recall:
  1) Phục vụ giao diện (index.html + vlearn_data.json) tại http://localhost:5000/
  2) API /recall — nhận câu hỏi, gọi AI thật (ai_recall.py), trả JSON.

Cần cài thêm:
    pip install flask flask-cors

Chạy:
    python codebase/app.py
Rồi mở trình duyệt vào: http://localhost:5000/
(Không mở file index.html trực tiếp bằng cách double-click nữa — phải qua
server này thì fetch('vlearn_data.json') và fetch('/recall') mới chạy được.)
"""

import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

from ai_recall import recall  # dùng lại đúng logic đã viết, không viết lại

STATIC_DIR = os.path.dirname(os.path.abspath(__file__))  # = thư mục codebase/

app = Flask(__name__, static_folder=STATIC_DIR, static_url_path="")
CORS(app)


@app.route("/")
def home():
    return send_from_directory(STATIC_DIR, "index.html")


@app.route("/recall", methods=["POST"])
def recall_endpoint():
    body = request.get_json(force=True)
    question = (body or {}).get("question", "").strip()
    if not question:
        return jsonify({"state": "NOT_FOUND", "citation": None,
                         "answer": "Bạn chưa nhập câu hỏi.", "options": []})
    result = recall(question)
    return jsonify(result)


if __name__ == "__main__":
    app.run(port=5000, debug=False)
