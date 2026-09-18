# VLearn AI Knowledge Finder

Frontend hiện có được giữ nguyên. Semantic backend FastAPI nằm trong thư mục [`backend`](backend/README.md).

Luồng Agent RAG:

```text
POST /api/agent → embedding query → cosine semantic search trên tutor_turns.csv
                → lọc nguồn đủ tin cậy → OpenAI Responses API
                → câu trả lời có dẫn nguồn + danh sách tìm kiếm thường
```

Xem [hướng dẫn chạy và hợp đồng API](backend/README.md) trước khi kết nối frontend.

## Chạy ứng dụng trên Windows

Mở PowerShell tại thư mục gốc dự án, rồi chạy lệnh dưới đây. Lệnh dùng trực tiếp Python trong `.venv`, giúp tránh lỗi `ModuleNotFoundError: No module named 'fastapi'` khi máy có nhiều bản Python.

```powershell
& ".\.venv\Scripts\python.exe" -m pip install -r .\backend\requirements.txt
& ".\.venv\Scripts\python.exe" ".\backend\app.py"
```

Khi terminal hiện `Uvicorn running on http://127.0.0.1:8000`, mở trình duyệt tại:

```text
http://127.0.0.1:8000
```

Không dùng `python backend\app.py` nếu lệnh `python` đang trỏ tới Python hệ thống thay vì `.venv`.

Nếu chạy bằng nút **Run Python File** của VS Code, chọn interpreter sau trước khi chạy:

1. Nhấn `Ctrl + Shift + P`.
2. Chọn **Python: Select Interpreter**.
3. Chọn `.venv\Scripts\python.exe`.

Để dùng Agent OpenAI, thêm `OPENAI_API_KEY=sk-...` vào `backend/.env`, rồi khởi động lại server. Xem chi tiết tại [backend/README.md](backend/README.md).

Nếu muốn kích hoạt môi trường ảo thủ công:

```powershell
.\.venv\Scripts\Activate.ps1
```
