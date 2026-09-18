# Validation Log — Phiên 01

**Ngày:** 18/09/2026 · **Track:** A2 — VLearn Recall

---

## Người thử 1

- **Tên · Vai trò:** Nguyễn Bá Chính — Người trải nghiệm
- **Người quan sát:** Lê Văn Sang
- **Task đã giao:**
  1. Tự nghĩ 1 câu hỏi "nhớ mang máng" về nội dung thật đã học
  2. Thử 1 câu cố tình mơ hồ
  3. Thử yêu cầu AI làm việc ngoài phạm vi

- **Quan sát:**
  - Câu hỏi 1 ("tôi có nhớ mình học LLM ở những buổi đầu nhưng khi tôi muốn ôn lại thì lại không biết tìm nó ở đâu"): người thử mô tả đúng chủ đề (LLM) và mốc thời gian (buổi đầu), hệ thống xác định được vị trí tài liệu liên quan.
  - Câu hỏi 2, cố tình mơ hồ ("phần nói về mô hình ấy nằm ở đâu nhỉ"): chưa ghi nhận đầy đủ thao tác nhập và phản hồi hệ thống trong phiên quan sát này.
  - Câu hỏi 3, ngoài phạm vi ("Viết hộ tôi một bài luận về LLM để nộp"): đã thử nhưng người quan sát chưa ghi lại chi tiết phản hồi từ chối.

- **Quote nguyên văn:**
  > "tôi có nhớ mình học LLM ở những buổi đầu nhưng khi tôi muốn ôn lại thì lại không biết tìm nó ở đâu"

- **Mức nghiêm trọng:** Trung bình — chưa đủ dữ liệu quan sát chi tiết để kết luận chắc chắn hệ thống xử lý tốt hay gặp lỗi ở case mơ hồ/ngoài phạm vi; quote chỉ xác nhận đúng "nỗi đau" ban đầu (khó tìm lại nội dung đã học).

- **Thay đổi đề xuất:** Cân nhắc cho người dùng bổ sung buổi học/chủ đề khi câu hỏi quá rộng. (Đề xuất từ tình huống quan sát được, chưa phải kết luận đã kiểm chứng đầy đủ qua toàn bộ phiên.)

---

## Người thử 2

- **Tên · Vai trò:** Trương Việt Anh — học viên
- **Người quan sát:** Vũ Đình Thư
- **Task đã giao:**
  1. Tự nghĩ 1 câu hỏi "nhớ mang máng" về nội dung thật đã học
  2. Thử 1 câu cố tình mơ hồ
  3. Thử yêu cầu AI làm việc ngoài phạm vi

- **Quan sát:**
  - Với câu hỏi rõ ràng: người thử đọc câu trả lời và kiểm tra phần nguồn hệ thống trả về, xác định được đúng đoạn transcript liên quan.
  - Với câu hỏi mơ hồ: người thử đọc các gợi ý của hệ thống trước khi tự nhập lại câu hỏi cụ thể hơn — tức là hệ thống có đưa gợi ý nhưng người thử vẫn phải tự suy luận cách viết lại.
  - Người thử mất một lúc mới nhận ra thao tác "Mở nguồn" từ kết quả trả về (vấn đề khả dụng giao diện, không phải AI).

- **Quote nguyên văn:**
  > "Em thấy kết quả tìm kiếm khá dễ hiểu và có nguồn đi kèm, nhưng với câu hỏi mơ hồ thì phần hỏi lại có thể hướng dẫn cụ thể hơn để em biết nên bổ sung thông tin gì."

- **Mức nghiêm trọng:** Trung bình

- **Thay đổi đề xuất:** Thêm gợi ý cụ thể hơn khi hệ thống rơi vào nhánh CLARIFY (ví dụ hỏi rõ buổi học / chủ đề / từ khoá còn thiếu) để người dùng dễ đặt lại câu hỏi và tìm đúng nội dung hơn.

---

## Người thử 3

- **Tên · Vai trò:** Nguyễn Đình Mạnh — 2A202602306 — học viên
- **Người quan sát:** Ngô Thế Khanh
- **Task đã giao:**
  1. Đặt một câu hỏi liên quan đến nội dung đã học
  2. Thử diễn đạt câu hỏi theo cách khác với từ ngữ trong tài liệu
  3. Kiểm tra các nguồn được hệ thống xếp hạng cao và so sánh mức độ liên quan của chúng

- **Quan sát:**
  - Hệ thống tìm các đoạn trong dữ liệu có chứa từ khoá tương đồng với câu hỏi.
  - Một số đoạn được xếp điểm cao vì chứa nhiều từ trùng với câu hỏi, nhưng **nội dung thực tế không trả lời đúng trọng tâm câu hỏi**.
  - Ngược lại, có đoạn chứa ít từ khoá giống câu hỏi hơn nhưng nội dung lại phù hợp về mặt ý nghĩa.
  - Thứ tự kết quả hiện tại chưa phản ánh chính xác mức độ liên quan về ngữ nghĩa khi người dùng diễn đạt khác cách dùng từ trong tài liệu gốc.

- **Quote nguyên văn:**
  > "Đoạn có nhiều từ giống câu hỏi chưa chắc là đoạn trả lời đúng nhất."

- **Mức nghiêm trọng:** Cao

- **Thay đổi đề xuất:** Thay cơ chế chấm điểm chủ yếu dựa trên keyword matching bằng semantic search/embedding để đánh giá mức độ tương đồng về ý nghĩa giữa câu hỏi và tài liệu; có thể bổ sung reranking trước khi gửi Top-K context cho GPT.

---

## Tổng hợp & quyết định

- **Chủ đề lặp lại giữa nhiều người thử:** Người thử 1 (Chính) và Người thử 2 (Việt Anh) đều gặp khó khăn giống nhau khi đặt câu hỏi mơ hồ/rộng — cả hai đều phải tự suy luận cách thu hẹp câu hỏi vì hệ thống chưa hướng dẫn đủ cụ thể ở nhánh CLARIFY. Đây là điểm chung giữa 2/3 người thử → bằng chứng mạnh hơn một nhận xét đơn lẻ.
- **Phát hiện độc lập mức nghiêm trọng cao:** Người thử 3 (Mạnh) phát hiện retrieval dựa trên keyword matching xếp hạng sai khi câu hỏi diễn đạt khác từ ngữ gốc trong tài liệu. Phát hiện này **khớp với bug đã biết trước đó** trong `run_results.md` (5 case G08, G10, G12, G15, G16 bị miss do retrieval chỉ đếm từ khoá thuần) — validation thật xác nhận đúng nguyên nhân gốc rễ đã nghi ngờ.
- **Đã sửa dựa trên feedback này:** Chưa sửa retrieval (giữ keyword matching làm baseline) — xem lý do giữ nguyên bên dưới. Đề xuất cải thiện gợi ý ở nhánh CLARIFY (từ Chính + Việt Anh) là thay đổi khả thi nhất trong thời gian còn lại; **cần đội áp dụng trực tiếp vào `codebase/ai_recall.py`** (phần system prompt nhánh CLARIFY) vì bản tóm tắt này không có quyền truy cập trực tiếp vào codebase để sửa — xem gợi ý cụ thể trong ghi chú gửi kèm.
- **Giữ nguyên, không sửa:** Cơ chế retrieval theo keyword matching được giữ nguyên trong phiên CP5 này. Lý do: (1) đây là thay đổi kiến trúc lớn (đổi sang semantic search/embedding + reranking), rủi ro phá vỡ 2 hard gate an toàn đang đạt 100% (từ chối lớp ③ và citation thật cho case FOUND) nếu làm vội trong vài giờ còn lại trước hạn nộp; (2) Quality Bar tại §7.3 đã khoá từ CP4, không được sửa ngưỡng — mọi thay đổi retrieval cần được đo lại bằng đúng golden set trước khi công nhận, việc này cần nhiều thời gian hơn khung CP5 cho phép.
- **Đưa vào backlog:** Semantic search/embedding + reranking cho retrieval (ưu tiên Cao, từ Người thử 3) — cần đo lại độ chính xác Top-K context sau khi cải thiện, dự kiến làm ở vòng sau hackathon. Cải thiện khả dụng nút "Mở nguồn" trên giao diện (từ quan sát của Người thử 2) — mức ưu tiên thấp hơn, không chặn Quality Bar.
