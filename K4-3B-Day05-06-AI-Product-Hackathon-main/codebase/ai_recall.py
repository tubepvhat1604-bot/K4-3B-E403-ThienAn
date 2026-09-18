"""
ai_recall.py — Module quyết định trung tâm cho VLearn Recall (CP3)
Bản dùng OpenAI API.

Cần cài trước:
    pip install openai

Cần biến môi trường:
    OPENAI_API_KEY=<khoá api của bạn>   (KHÔNG commit khoá này lên repo)
"""

import os
import json
import glob
import datetime

from openai import OpenAI

MODEL = "gpt-4o-mini"  # đổi sang model khác nếu muốn, VD "gpt-4o"
LOG_PATH = "eval/call_log.jsonl"
TRANSCRIPT_DIR = "data/vlearn-pack/transcript"  # đường dẫn tới data thật đã cấp


SYSTEM_PROMPT = """Bạn là trợ lý "VLearn Recall" giúp học viên tìm lại nội dung \
đã học khi họ chỉ nhớ mang máng, không nhớ chính xác vị trí.

Bạn sẽ nhận: (1) câu hỏi mơ hồ của học viên, (2) các đoạn transcript có mã \
số [Txx-NNN] làm ngữ liệu để đối chiếu.

QUY TẮC BẮT BUỘC (không được vi phạm):
- Nếu học viên yêu cầu AI làm việc KHÁC ngoài chức năng tìm lại nội dung đã học (viết hộ bài luận, làm hộ bài tập, cho đáp án bài kiểm tra/quiz, tạo nội dung mới...) -> trạng thái NOT_FOUND. Answer phải nói rõ đây không phải chức năng của Recall (chỉ tìm lại nội dung đã học, không làm hộ việc khác) và hướng dẫn cách hỏi đúng. KHÔNG dùng CLARIFY cho trường hợp này — đây là từ chối do NGOÀI PHẠM VI, không phải do thiếu thông tin để hỏi lại.
- Nếu tìm được đúng 1 đoạn khớp rõ ràng với câu hỏi -> trạng thái FOUND. \
Phải trích dẫn đúng mã đoạn [Txx-NNN] đã cho, KHÔNG được bịa mã đoạn không \
có trong ngữ liệu.
- Nếu câu hỏi khớp với 2 đoạn trở lên có chủ đề khác nhau, hoặc quá mơ hồ \
để chọn 1 đoạn (nhưng vẫn là câu hỏi tìm nội dung, không phải yêu cầu làm việc khác) -> trạng thái CLARIFY. Liệt kê tối đa 2 lựa chọn ngữ cảnh cụ \
thể để học viên chọn lại, KHÔNG tự chọn đại một đoạn.
- Nếu không đoạn nào trong ngữ liệu được cung cấp khớp với câu hỏi (và đây đúng là câu hỏi tìm nội dung) -> trạng \
thái NOT_FOUND. KHÔNG được suy đoán hay bịa nội dung không có trong ngữ liệu.

Luôn trả lời bằng JSON đúng schema:
{
  "state": "FOUND" | "CLARIFY" | "NOT_FOUND",
  "citation": "mã đoạn, ví dụ T06-014, hoặc null nếu không phải FOUND",
  "answer": "câu trả lời ngắn cho học viên",
  "options": ["lựa chọn 1", "lựa chọn 2"]
}
Không thêm chữ nào ngoài JSON.
"""


STOPWORDS = {
    "hình", "như", "của", "về", "đến", "những", "các", "mà", "người", "không",
    "được", "làm", "thì", "và", "có", "là", "một", "này", "đó", "cho", "với",
    "khi", "nếu", "sẽ", "đã", "đang", "rất", "cũng", "nên", "phải", "ra",
    "vào", "lên", "xuống", "lại", "nữa", "chỉ", "còn", "vì", "nói", "hỏi",
    "biết", "muốn", "cái", "con", "số", "ngày", "lúc", "bạn", "mình", "tôi",
    "chúng", "họ", "gì", "sao", "nào", "đâu", "bao", "nhiêu", "thế", "vậy",
    "hay", "là", "thầy", "cô", "buổi", "học", "mấy",
}


def load_transcript_context(question: str, top_k: int = 6) -> str:
    """Tách transcript thành từng đoạn theo mã [Txx-NNN], chấm điểm mỗi đoạn
    theo số từ khoá (đã loại từ vô nghĩa) trùng với câu hỏi, rồi chỉ gửi
    top_k đoạn khớp nhất cho AI."""
    import re

    raw_words = [w for w in re.findall(r"\w+", question.lower()) if len(w) > 2]
    keywords = [w for w in raw_words if w not in STOPWORDS]
    if not keywords:  # câu hỏi toàn từ phổ biến -> dùng tạm raw_words để còn cái mà so
        keywords = raw_words

    chunks = []  # (score, path, code, text)
    for path in sorted(glob.glob(f"{TRANSCRIPT_DIR}/*.md")):
        with open(path, encoding="utf-8") as f:
            text = f.read()
        # tách theo từng đoạn bắt đầu bằng **[Txx-NNN]**
        pieces = re.split(r"(?=\*\*\[T\d{2}-\d{3}\]\*\*)", text)
        for piece in pieces:
            piece = piece.strip()
            if not piece:
                continue
            m = re.match(r"\*\*\[(T\d{2}-\d{3})\]\*\*", piece)
            code = m.group(1) if m else None
            score = sum(piece.lower().count(k) for k in keywords)
            if score > 0:
                chunks.append((score, path, code, piece))

    chunks.sort(key=lambda x: x[0], reverse=True)
    top = chunks[:top_k]

    if not top:
        return ""  # không đoạn nào khớp từ khoá -> để AI tự nói NOT_FOUND, không tự bịa

    return "\n\n".join(
        f"[{code}] (nguồn: {os.path.basename(path)})\n{piece}"
        for _, path, code, piece in top
    )


def call_model(question: str, context: str) -> dict:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    context_display = context if context else "(Không tìm thấy đoạn transcript nào khớp từ khoá với câu hỏi này.)"

    user_msg = f"""NGỮ LIỆU TRANSCRIPT (các đoạn liên quan nhất đã được lọc sẵn):
{context_display}

CÂU HỎI HỌC VIÊN:
\"{question}\"

Trả lời đúng schema JSON đã mô tả."""

    resp = client.chat.completions.create(
        model=MODEL,
        temperature=0,  # khoá kết quả ổn định — cùng câu hỏi phải ra cùng kết quả
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_msg},
        ],
    )

    raw_text = resp.choices[0].message.content

    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps({
            "timestamp": datetime.datetime.now().isoformat(),
            "question": question,
            "raw_response": raw_text,
        }, ensure_ascii=False) + "\n")

    try:
        return json.loads(raw_text)
    except json.JSONDecodeError:
        return {"state": "NOT_FOUND", "citation": None,
                "answer": "Lỗi phân tích phản hồi model — xem log.", "options": []}


def recall(question: str) -> dict:
    context = load_transcript_context(question)
    return call_model(question, context)


if __name__ == "__main__":
    import sys
    q = sys.argv[1] if len(sys.argv) > 1 else "Attention là gì nhỉ, hình như thầy nói ở buổi nào đó rồi"
    result = recall(q)
    print(json.dumps(result, ensure_ascii=False, indent=2))
