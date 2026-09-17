# AI SPEC — VLearn Recall · Nhóm [điền số nhóm] · Zone [điền phòng]
Hướng: [x] A — VLearn  [ ] B — Trợ lý Học viên  [ ] C — Làn mở
Loại: [ ] Tối ưu tính năng có sẵn  [x] Tính năng mới

## §1. User & Job

- **Job executor + workflow:** Học viên đang ôn lại bài hoặc chuẩn bị quiz, chỉ nhớ một phần đã học. Trước khi ôn: nhớ mang máng có một khái niệm/nội dung liên quan nhưng không nhớ nằm ở buổi nào, slide nào, hay đoạn transcript nào. Hiện tại phải dò từng slide/tài liệu hoặc tua lại video để tìm.
- **Core JTBD (không tên sản phẩm/AI trong câu):** Tìm lại đúng chỗ chứa nội dung mình từng học, khi chỉ nhớ mang máng chủ đề chứ không nhớ vị trí cụ thể.
- **Problem statement (KHÔNG chữ AI):** Học viên khi ôn bài nhớ từ khóa mơ hồ nên phải lục lại slide/transcript thủ công, mất thời gian và dễ ôn sai phần quan trọng hoặc bỏ cuộc giữa chừng.
- **Evidence (Chuẩn A — khảo sát, log đầy đủ trong `data/` khảo sát nhóm tự thu thập):**
  - Số liệu khảo sát: n = 20 học viên trong lớp. 17/20 (85%) không nhớ chính xác vị trí nội dung khi cần tìm lại (10/20 "nhớ bài nhưng không nhớ trang/đoạn", 7/20 "không nhớ nội dung nằm ở bài nào"). 17/20 (85%) mất từ 3 phút trở lên để tìm lại, trong đó 2 người bỏ cuộc hoàn toàn không tìm được. 18/20 (90%) sẵn sàng dùng thử công cụ AI hỗ trợ.
  - ≥5 quote/ví dụ nguyên văn + nguồn (ẩn danh theo mã người trả lời, log đầy đủ lưu ngoài repo):
    - P02: "Không nhớ bài đó nằm ở file nào"
    - P07: "Nhiều lúc không thấy và không biết tìm ở đâu"
    - P11: "Việc không nhớ rõ được kiến thức đang nằm ở đâu gây tốn thời gian"
    - P06: "Không biết nội dung nằm ở đâu"
    - P08: "Tôi có học nhưng lúc cần tìm lại thì không biết mình nên tìm ở đâu"

## §2. Impact & quyết định chọn

- **Bảng impact ≥3 ứng viên:**

| Ứng viên vấn đề | Bao nhiêu người | Tần suất | Tốn gì mỗi lần | Khả thi trong 3 buổi |
|---|---|---|---|---|
| Tìm lại nội dung nhớ mang máng | 17/20 (85%) | Mỗi lần ôn bài/trước quiz | 3–10+ phút, có ca bỏ cuộc | Cao — data pack đã có transcript mã đoạn sẵn |
| Câu trả lời tutor không trích dẫn nguồn (A1) | ~28% lượt (theo data dictionary) | Mỗi lần hỏi tutor | Mất niềm tin, không biết đúng/sai | Trung bình — cần chỉnh sửa hệ thống tutor có sẵn |
| Không biết mình đang hổng kiến thức nào (Learning Trace) | Chưa khảo sát riêng | Cuối mỗi buổi học | Ôn sai trọng tâm | Thấp hơn — cần thiết kế tính năng hoàn toàn mới, ít bằng chứng trực tiếp |

- **Ứng viên ĐÃ LOẠI + vì sao:** "Learning Trace" (bản đồ lỗ hổng sau buổi học) bị loại vì thiếu bằng chứng số liệu trực tiếp trong thời gian CP1, và phạm vi rộng hơn (cần giảng viên tham gia) khó demo trong 5 phút.
- **Ứng viên CHỌN + vì sao (bằng số):** VLearn Recall — 85% học viên xác nhận gặp đúng vấn đề này, 90% sẵn sàng dùng thử, và có sẵn data (transcript đã có mã đoạn `[Txx-NNN]` để trích dẫn) nên khả thi build trong 39 giờ.

## §3. Giải pháp tương tự đã nghiên cứu

*(hoàn thiện tại CP4)*

## §4. Thiết kế

- **Lát cắt MỘT CÂU:** Học viên đang ôn bài, chỉ nhớ mang máng nội dung · AI quyết định tìm được đúng nguồn (trả lời kèm trang/đoạn) hay chưa đủ căn cứ để hỏi lại · kết quả là học viên định vị đúng chỗ cần xem lại thay vì tự dò cả buổi.
- **Non-goals (≥3 thứ KHÔNG build):**
  1. Không tự tóm tắt toàn bộ bài giảng — chỉ định vị đúng đoạn liên quan.
  2. Không sửa/tạo nội dung học liệu mới — chỉ trích dẫn nội dung đã có.
  3. Không thay thế tutor hỏi-đáp hiện có của track A1 — đây là tính năng tìm kiếm/định vị riêng.
- **Mức prototype nhắm tới:** [x] Mock — flow bấm được trọn 3 nhánh, dữ liệu trả lời hiện đang là dữ liệu giả (hard-code); phần AI thật (đối chiếu ngữ nghĩa với transcript) sẽ nối vào lõi ở CP3.
- **Automation:** [x] Conditional — lý do theo cost-of-error: nếu AI luôn tự trả lời (Automate) mà đoán sai nguồn, học viên có thể ôn sai kiến thức — hậu quả học thuật nặng, khó tự phát hiện lỗi. Nếu AI luôn chỉ gợi ý cho người tự tìm (Augment) thì không giải quyết được pain chính (mất thời gian tự dò). Do đó chọn Conditional: AI tự trả lời kèm trích dẫn khi đủ căn cứ rõ ràng (FOUND), nhưng chuyển sang hỏi lại (CLARIFY) hoặc từ chối rõ ràng (NOT_FOUND) khi không đủ tín hiệu, thay vì đoán bừa.
- **§4b. Nguyên tắc đã áp dụng (≥4 — HAX/PAIR):**

| Nguyên tắc | Áp cụ thể vào đâu trong prototype |
|---|---|
| **G10 · Thu hẹp phạm vi khi nghi ngờ** (bắt buộc) | Khi câu hỏi khớp nhiều đoạn hoặc còn mơ hồ, hệ thống chuyển sang trạng thái CLARIFY và hỏi lại, không tự chọn đại một đoạn để trả lời. |
| **G11 · Giải thích vì sao** | Mọi câu trả lời ở trạng thái FOUND đều kèm tag nguồn dạng "Transcript-06 · đoạn [T06-014]" và mô tả vị trí trong buổi giảng (VD: "phút 32–35 buổi ngày 2"), giúp học viên hiểu vì sao AI đưa ra câu trả lời này. |
| **G8 · Gạt bỏ dễ dàng** | Ở trạng thái CLARIFY, học viên có thể bỏ qua gợi ý đưa ra và tự gõ lại câu hỏi khác ngay trong cùng màn hình, không phải đóng modal hay quay lại bước trước. |
| **G9 · Sửa dễ dàng** | Ô "Gửi lại" ở trạng thái CLARIFY cho phép học viên chỉnh/nhập lại câu hỏi ngay tại chỗ mà không mất phần đã nhập trước đó. |

## §5. Kiểu lỗi — 4 lớp chỗ khó + kịch bản

*(hoàn thiện đầy đủ ≥8 kịch bản tại CP3/CP4 — bản nháp ban đầu)*

- ① **Nguồn sự thật:** Câu hỏi không liên quan tài liệu đã học → không được bịa nguồn, phải trả lời NOT_FOUND.
- ② **Mơ hồ/thiếu thông tin:** Câu hỏi khớp nhiều đoạn/buổi khác nhau → chuyển CLARIFY, đưa ra các lựa chọn ngữ cảnh cụ thể.
- ③ **Ngoài phạm vi:** Học viên hỏi xin đáp án bài kiểm tra hoặc nội dung không liên quan chương trình → từ chối rõ ràng, hướng dẫn cách hỏi hợp lệ.
- ④ **Đặc thù domain:** Trích dẫn sai đoạn có thể khiến học viên học sai kiến thức → ưu tiên trả lời "chưa đủ căn cứ" hơn là trả lời có khả năng sai.

## §6. Bốn đường đi của trải nghiệm

- **Happy path:** Học viên nhập câu hỏi đủ rõ ("Attention là gì nhỉ, hình như thầy nói ở buổi nào đó rồi") → AI tìm thấy đúng đoạn nguồn → trả lời kèm trích dẫn trang/mã đoạn cụ thể (trạng thái FOUND).
- **Low-confidence (②):** Câu hỏi khớp nhiều đoạn khác nhau ("Cái phần nói về việc LLM hay bịa thông tin ấy") → AI đưa ra các lựa chọn ngữ cảnh cụ thể để học viên chọn đúng, thay vì tự đoán một chỗ (trạng thái CLARIFY).
- **Failure/không căn cứ (①):** Nội dung không có trong tài liệu đã học ("Công thức tính lương tối thiểu vùng") → AI nói rõ "Không tìm thấy trong tài liệu đã học", không bịa, gợi ý hỏi TA (trạng thái NOT_FOUND).
- **Correction (user sửa):** Sau khi nhận CLARIFY, học viên nhập lại câu hỏi rõ hơn trong ô "Gửi lại" → luồng xử lý lại từ đầu với câu hỏi mới, không mất ngữ cảnh đã nhập.

## §7. Kiểm thử

*(hoàn thiện tại CP3 — golden set ≥20 case)*

## §8. Phân công & kế hoạch

- **Phân công có tên:** Phạm Văn Hoàng Anh Tú — đội trưởng, repo + spec.md + nộp form · Lê Văn Sang — khảo sát, thu thập bằng chứng · Vũ Đình Thư — tổng hợp số liệu, golden set · Ngô Thế Khanh — thiết kế prompt, prototype, AI call
- **Willing users (≥2 tên):** Nguyễn Bá Chính — Học viên, từng gặp khó khi tìm lại nội dung bài giảng đã học, đồng ý thử prototype · Trương Việt Anh — Học viên, từng gặp pain này, đồng ý dùng thử

## §9. Changelog

| Thời điểm | Đổi gì | Vì sao (trỏ về feedback/case nào) |
|---|---|---|
| CP1 | Chốt canvas 7 dòng, chọn track A2 VLearn Recall | Dựa trên khảo sát 20 học viên |
| CP2 | Hoàn thiện §4 (thiết kế, automation, 4 nguyên tắc HAX) và §6 (4 đường đi trải nghiệm); dựng mock click-through 3 nhánh FOUND/CLARIFY/NOT_FOUND | Theo yêu cầu mốc CP2 trong `02-guide.md` §2 |
