# Validation Log — Phiên 01

**Ngày:** 18/09/2026 · **Người quan sát:** Ngô Thế Khanh

---

## Người thử 3

- **Tên · Vai trò:** Nguyễn Đình Mạnh — 2A202602306 — học viên
- **Task đã giao:**
  1. Đặt một câu hỏi liên quan đến nội dung đã học.
  2. Thử diễn đạt câu hỏi theo cách khác với từ ngữ trong tài liệu.
  3. Kiểm tra các nguồn được hệ thống xếp hạng cao và so sánh mức độ liên quan của chúng.
- **Quan sát:**
  - Khi nhập câu hỏi, hệ thống tìm các đoạn trong dữ liệu có chứa từ khóa tương đồng.
  - Một số đoạn được xếp điểm cao vì chứa nhiều từ trùng với câu hỏi, nhưng **nội dung thực tế không trả lời đúng trọng tâm câu hỏi**.
  - Ngược lại, có đoạn chứa ít từ khóa giống câu hỏi hơn nhưng nội dung lại phù hợp về mặt ý nghĩa.
  - Vì vậy, thứ tự kết quả hiện tại chưa phản ánh chính xác mức độ liên quan về ngữ nghĩa.
- **Quote nguyên văn:**
  > “Đoạn có nhiều từ giống câu hỏi chưa chắc là đoạn trả lời đúng nhất.”
- **Mức nghiêm trọng:** **Cao**
- **Thay đổi đề xuất:**
  Thay cơ chế chấm điểm chủ yếu dựa trên **keyword matching** bằng **semantic search/embedding** để đánh giá mức độ tương đồng về ý nghĩa giữa câu hỏi và tài liệu. Có thể bổ sung **reranking** để sắp xếp lại các đoạn trước khi gửi Top-K context cho GPT.

---

## Tổng hợp & quyết định

- **Kết luận tạm thời từ Người thử 3:** Cơ chế keyword matching có thể xếp hạng cao các đoạn nhiều từ trùng nhưng chưa chắc phù hợp về mặt ý nghĩa. Đây là vấn đề liên quan đến độ chính xác của retrieval và được đánh giá ở mức **Cao**.
- **Quyết định hiện tại:** Chưa thay thế ngay cơ chế keyword matching trong phiên này; giữ nó làm baseline để có kết quả so sánh khi thử semantic search/reranking.
- **Đã ghi nhận:** Đưa vấn đề và đề xuất semantic search/embedding vào backlog; cần đo lại độ chính xác của Top-K context sau khi cải thiện.
- **Bổ sung sau:** Khi có phản ánh của Người thử 1 và Người thử 2, cập nhật phần này để xác định vấn đề có lặp lại giữa nhiều người hay không và điều chỉnh mức ưu tiên nếu cần.
