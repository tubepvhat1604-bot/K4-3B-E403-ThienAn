# VLearn AI Knowledge Finder — semantic backend

Backend phục vụ trực tiếp `index.html` tại `/`. Giao diện gọi `POST /api/agent`: service tìm các nguồn học liên quan trước, sau đó gửi riêng nguồn đạt ngưỡng tin cậy cho OpenAI để tạo câu trả lời có căn cứ. `POST /api/search` vẫn giữ lại cho chức năng tìm kiếm thuần túy.

## Chuẩn bị dữ liệu

Đặt `tutor_turns.csv` tại `backend/data/tutor_turns.csv`, hoặc giữ file ở vị trí khác và đặt biến môi trường `VLEARN_DATA_PATH`. File nguồn không được commit; embedding cache được tạo ở `backend/cache/` và cũng không được commit.

## Chạy local

Từ thư mục `backend`:

```powershell
pip install -r requirements.txt
$env:VLEARN_DATA_PATH = "C:\Users\FPT SHOP\Downloads\data\vlearn-pack\chatlog\tutor_turns.csv"
uvicorn app:app --reload
```

`app.py` cũng tự đọc `backend/.env`; trong máy hiện tại file này đã trỏ
`VLEARN_DATA_PATH` đến `tutor_turns.csv`. Nếu di chuyển dữ liệu sang nơi khác,
chỉ cần cập nhật biến này. Khi dùng nút **Run Python File** trong IDE, có thể
chạy thẳng `python app.py` (không có auto-reload).

Lần đầu khởi động sẽ tải model `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`, tạo embedding cho các câu hỏi K4 không preset, và lưu cache. Những lần sau chỉ tải cache nếu CSV, filter và model không đổi.

## Cấu hình OpenAI Agent

Tạo file `backend/.env` (file này đã được `.gitignore` loại trừ) và đặt API key ở backend, không bao giờ đặt trong `index.html`:

```dotenv
VLEARN_DATA_PATH=C:\duong-dan\toi\tutor_turns.csv
OPENAI_API_KEY=sk-...
# Tùy chọn
VLEARN_AGENT_MODEL=gpt-5.2
VLEARN_AGENT_MIN_SCORE=0.72
```

Agent chỉ gọi OpenAI khi tìm thấy nguồn có điểm từ `VLEARN_AGENT_MIN_SCORE` trở lên. Nếu không đủ nguồn, câu trả lời sẽ là “Không tìm thấy thông tin này trong tài liệu đã học.” Key bị thiếu hoặc không hợp lệ sẽ không làm hỏng tìm kiếm thường; lỗi được hiển thị trong khung Agent.

## API cho frontend

```http
POST http://127.0.0.1:8000/api/search
Content-Type: application/json

{
  "query": "Tool Calling là gì?",
  "top_k": 5
}
```

Ví dụ phản hồi:

```json
{
  "query": "Tool Calling là gì?",
  "results": [
    {
      "rank": 1,
      "course_id": "K4P1",
      "lecture_code": "D03",
      "lecture_title": "AI Agent",
      "score": 0.87,
      "matched_question": "...",
      "excerpt": "..."
    }
  ],
  "message": null
}
```

`lecture_code` không được dùng một mình để định danh nguồn: mỗi kết quả luôn mang cả `course_id` và `lecture_code`. Nếu không có similarity nào qua `VLEARN_SIMILARITY_THRESHOLD` (mặc định `0.60`), `results` rỗng và `message` giải thích rằng chưa đủ nguồn phù hợp. Có thể tune threshold qua biến môi trường này.

### OpenAI Agent API

```http
POST http://127.0.0.1:8000/api/agent
Content-Type: application/json

{
  "query": "Tool Calling là gì?",
  "top_k": 5
}
```

Phản hồi gồm `answer`, `grounded`, `sources` và `results`. `sources` là các nguồn thực sự đưa vào Agent; `results` là danh sách tìm kiếm thông thường. Agent được yêu cầu chỉ dùng nội dung nguồn, không dùng kiến thức bên ngoài và từ chối nếu nguồn không đủ căn cứ.

`GET /` trả giao diện `index.html`, `GET /api` mô tả các endpoint, còn `GET /api/health` trả `{ "status": "ok" }`. CORS chỉ cho phép một danh sách localhost rõ ràng; đặt `VLEARN_CORS_ORIGINS` (danh sách phân cách bằng dấu phẩy) khi cần origin khác.

## Đánh giá retrieval

```powershell
python evaluate.py --golden-set path\to\golden_set.csv
```

Golden set cần các cột `query,expected_course_id,expected_lecture_code`. Script in ra `top_1_accuracy` và `hit_at_3`, không hard-code bất kỳ lecture nào.

## Kiểm thử không cần tải model

```powershell
python -m unittest -v test_retrieval.py
```
