# AI SPEC — VLearn Recall · CP4

Track A2 · Tìm lại nội dung đã học khi chỉ nhớ mang máng · Tính năng mới.

**Kết luận hiện tại: HOLD — chưa đạt quality bar tổng thể, nhưng đã đạt cả 2 hard gate an toàn.** Kết quả chạy golden set lượt 2 (18/09/2026, sau khi sửa prompt và giao diện): 14/20 case đạt = 70%, tăng từ 60% ở lượt 1. Vẫn dưới ngưỡng ≥80%, nhưng cả 2 điều kiện cứng (từ chối an toàn 100%, trích dẫn đúng nguồn 100%) đã đạt — phần còn thiếu là độ phủ (recall) của retrieval, không phải rủi ro an toàn. Bản spec này ghi nhận đúng hiện trạng, không chỉnh số liệu để "đạt cho đẹp".

## §1. User & Job

- **Job executor + workflow:** Học viên đang ôn lại bài hoặc chuẩn bị quiz, chỉ nhớ một phần đã học. Workflow hiện tại: nhớ mang máng nội dung → đoán tài liệu/buổi học → mở từng slide/transcript hoặc tua video → tìm từ khoá → đọc ngữ cảnh xác nhận → quay lại ôn tập. Điểm nghẽn nằm giữa "nhớ chủ đề" và "định vị đúng nguồn".
- **Core JTBD (không tên sản phẩm/AI):** Khi ôn bài và chỉ nhớ một phần nội dung, tìm lại đúng đoạn mình từng học để kiểm tra kiến thức và tiếp tục ôn mà không phải dò toàn bộ tài liệu.
- **Problem statement (không chữ AI):** Học viên khi ôn bài nhớ từ khoá mơ hồ nên phải lục lại slide/transcript thủ công, mất thời gian và dễ ôn sai phần quan trọng hoặc bỏ cuộc giữa chừng.
- **Evidence (Chuẩn A — khảo sát 20 học viên trong lớp):**
  - 17/20 (85%) không nhớ chính xác vị trí nội dung khi cần tìm lại (10/20 "nhớ bài nhưng không nhớ trang/đoạn", 7/20 "không nhớ nội dung nằm ở bài nào").
  - 17/20 (85%) mất từ 3 phút trở lên để tìm lại, trong đó 2 người bỏ cuộc hoàn toàn.
  - 18/20 (90%) sẵn sàng dùng thử công cụ AI hỗ trợ.
  - **Giới hạn kiểm chứng:** log khảo sát gốc (từng câu trả lời, danh sách 20 người) lưu ngoài repo theo quy định bảo mật, không đính kèm ở đây — số liệu trên là bản tổng hợp đã tính từ log đó.
  - ≥5 quote nguyên văn (ẩn danh theo mã người trả lời):
    - P02: "Không nhớ bài đó nằm ở file nào"
    - P07: "Nhiều lúc không thấy và không biết tìm ở đâu"
    - P11: "Việc không nhớ rõ được kiến thức đang nằm ở đâu gây tốn thời gian"
    - P06: "Không biết nội dung nằm ở đâu"
    - P08: "Tôi có học nhưng lúc cần tìm lại thì không biết mình nên tìm ở đâu"

## §2. Impact & quyết định chọn

| Ứng viên | Bao nhiêu người | Tần suất | Tốn gì mỗi lần | Khả thi trong 3 buổi |
|---|---|---|---|---|
| A2: tìm lại nội dung nhớ mang máng | 17/20 (85%) | Mỗi lần ôn bài/trước quiz | 3–10+ phút, có ca bỏ cuộc | Cao — transcript đã có mã đoạn `[Txx-NNN]` sẵn để trích dẫn |
| A1: tutor trả lời thiếu nguồn trích dẫn | ~28% lượt (theo data dictionary, không phải khảo sát riêng của nhóm) | Mỗi lượt hỏi tutor | Mất niềm tin, không biết đúng/sai | Trung bình — cần sửa hệ thống tutor có sẵn, phạm vi rộng hơn |
| Learning Trace (bản đồ lỗ hổng sau buổi học) | Chưa khảo sát riêng | Cuối mỗi buổi học | Ôn sai trọng tâm | Thấp — cần giảng viên tham gia, khó demo trong 5 phút |

- **Loại:** A1 (phạm vi rộng hơn lát cắt hẹp) và Learning Trace (thiếu evidence trực tiếp, cần lịch sử học tập vượt phạm vi demo).
- **Chọn A2 vì:** 85% xác nhận gặp đúng pain, 90% sẵn sàng dùng thử, có sẵn corpus phân đoạn để xây lát cắt nhỏ trong 39 giờ.

## §3. Giải pháp tương tự đã nghiên cứu

| Sản phẩm | Flow của họ | Điều đáng học | Điều đáng né | Mình khác gì |
|---|---|---|---|---|
| Claude Citations | Upload tài liệu, bật citations → hỏi → câu trả lời kèm vị trí trích dẫn (trang/vùng ký tự) có thể kiểm lại | Trích dẫn phải gắn vị trí nguồn kiểm được, không chỉ tên tài liệu | Một citation đúng vị trí không tự động nghĩa là toàn bộ diễn giải đúng | Giới hạn trong corpus khoá học, dùng mã `Txx-NNN`, quyết định rõ 3 trạng thái FOUND/CLARIFY/NOT_FOUND thay vì luôn cố trả lời |
| Google NotebookLM | Upload tài liệu → hỏi đáp có trích dẫn ngay trong câu trả lời → click trích dẫn nhảy tới đúng vị trí gốc | Bắt buộc trích dẫn kèm mọi câu trả lời, không trả lời khi thiếu nguồn | Nhiều tính năng ngoài phạm vi (tạo podcast, mindmap) không cần cho lát cắt hẹp | Chỉ tập trung đúng 1 việc — định vị lại nội dung khi nhớ mang máng |

*(Phân tích dựa trên tài liệu chính thức của 2 sản phẩm, nhóm chưa có ảnh/log dùng thử trực tiếp — sẽ bổ sung nếu có quyền truy cập trước CP5.)*

## §4. Thiết kế

- **Lát cắt MỘT CÂU:** Học viên đang ôn bài, chỉ nhớ mang máng nội dung · AI quyết định tìm được đúng nguồn (trả lời kèm trang/đoạn) hay chưa đủ căn cứ để hỏi lại · kết quả là học viên định vị đúng chỗ cần xem lại thay vì tự dò cả buổi.
- **Non-goals:**
  1. Không tóm tắt toàn bộ bài giảng — chỉ định vị đúng đoạn liên quan.
  2. Không sửa/tạo nội dung học liệu mới — chỉ trích dẫn nội dung đã có.
  3. Không thay thế tutor hỏi-đáp của track A1 — đây là tính năng tìm kiếm/định vị riêng.
  4. Không làm hộ quiz, bài luận hay tác vụ ngoài phạm vi recall.
- **Mức prototype:** [x] Working — flow chạy trọn với AI thật (OpenAI gpt-4o-mini) ở quyết định trung tâm. Retrieval: tách transcript thành đoạn theo mã `[Txx-NNN]`, chấm điểm khớp từ khoá (đã lọc stopword), gửi top-6 đoạn liên quan nhất cho model quyết định trạng thái. Giao diện web gọi trực tiếp qua backend Flask.
- **Automation:** [x] Conditional — lý do cost-of-error: nếu luôn tự trả lời (Automate) mà đoán sai nguồn, học viên ôn sai kiến thức, hậu quả học thuật nặng và khó tự phát hiện. Nếu chỉ gợi ý cho tự tìm (Augment) thì không giải quyết pain chính. Chọn Conditional: tự trả lời kèm trích dẫn khi đủ căn cứ, hỏi lại hoặc từ chối khi không đủ tín hiệu.
- **§4b. Nguyên tắc HAX/PAIR:**

| Nguyên tắc | Áp cụ thể vào đâu | Hiện trạng |
|---|---|---|
| G10 · Thu hẹp phạm vi khi nghi ngờ (bắt buộc) | Câu hỏi khớp nhiều đoạn/mơ hồ → chuyển CLARIFY, không tự chọn đại. Yêu cầu ngoài phạm vi → từ chối rõ (NOT_FOUND) | Đạt cả 2 trường hợp — đã sửa và xác nhận qua lượt chạy 2 (14/20), case G06 (ngoài phạm vi) nay trả đúng |
| G11 · Giải thích vì sao | Câu trả lời FOUND kèm tag nguồn `[Txx-NNN]` + mô tả vị trí trong buổi giảng | Đạt ở mức trả lời; giao diện mở nguồn còn lỗi độc lập (xem §7.5) |
| G8 · Gạt bỏ dễ dàng | Ở CLARIFY, học viên gõ lại câu khác ngay, không phải đóng modal | Đạt |
| G9 · Sửa dễ dàng | Ô "Gửi lại" ở CLARIFY cho sửa ngay tại chỗ | Đạt, nhưng backend chưa giữ ngữ cảnh câu hỏi trước |

## §5. Kiểu lỗi — 4 lớp chỗ khó + kịch bản

| Tình huống | Lớp | Hành vi mong muốn | Nguyên tắc |
|---|---|---|---|
| Hỏi nội dung hoàn toàn ngoài chương trình (VD: lương tối thiểu vùng) | ① | NOT_FOUND, không bịa | G10 |
| Hỏi từ khoá gần giống chủ đề đã học nhưng nội dung thật không có | ① | Không suy diễn liên tưởng sai | G10 |
| Câu hỏi khớp ≥2 đoạn khác chủ đề | ② | CLARIFY, đưa 2 lựa chọn cụ thể | G10, G8 |
| Câu hỏi quá ngắn, thiếu ngữ cảnh | ② | Nhận biết thiếu thông tin, hỏi lại thay vì đoán | G10 |
| Học viên xin đáp án bài quiz/kiểm tra | ③ | Từ chối, giải thích lý do | G10 |
| Học viên yêu cầu AI làm việc khác (viết hộ bài luận) | ③ | Từ chối, hướng dẫn dùng đúng chức năng | G10 — đã sửa system prompt, xác nhận đạt ở lượt chạy 2 |
| Câu hỏi có khái niệm dễ nhầm với khái niệm gần giống | ④ | Trích đúng khái niệm, không lẫn | G11 |
| Câu hỏi chi tiết kỹ thuật chính xác (công thức, số liệu) | ④ | Trích nguyên văn, không diễn giải sai | G11 |

**Kịch bản đáng sợ nhất khi demo:** trường hợp câu trả lời có vẻ đúng (có citation, có % khớp) nhưng nút "Mở nguồn" trên giao diện lại mở nhầm đoạn khác — người học dễ tin sai vì giao diện trông có căn cứ. Đây là lỗi đã phát hiện ở §7.5, chưa sửa xong tính đến thời điểm khoá spec.

## §6. Bốn đường đi của trải nghiệm

- **Happy path:** Câu hỏi đủ rõ ("Attention là gì nhỉ, hình như thầy nói ở buổi nào đó rồi") → tìm đúng đoạn nguồn → trả lời kèm trích dẫn (FOUND). *Lưu ý: case này lúc đầu bị golden set gắn nhãn sai là FOUND — kiểm tra trực tiếp qua giao diện cho thấy hệ thống trả CLARIFY đúng vì câu hỏi thực sự khớp 2 đoạn khác nhau (T06-086, T06-027).*
- **Low-confidence (②):** Câu hỏi khớp nhiều đoạn ("LLM hay bịa thông tin") → đưa lựa chọn ngữ cảnh cụ thể thay vì đoán (CLARIFY).
- **Failure/không căn cứ (①):** Nội dung không có trong tài liệu ("Công thức tính lương tối thiểu vùng") → nói rõ "không tìm thấy", gợi ý hỏi TA (NOT_FOUND).
- **Correction:** Sau CLARIFY, học viên nhập lại câu hỏi rõ hơn trong ô "Gửi lại" → xử lý lại với câu hỏi mới.

## §7. Kiểm thử

### 7.1 Chiều chất lượng và định nghĩa kiểm chứng được

| Chiều | Định nghĩa đạt | Cách kiểm |
|---|---|---|
| Đúng trạng thái | `state` khớp `expected_state` đã rà soát nhãn | So khớp, người ngoài nhóm chấm lại ra cùng kết quả |
| Trích dẫn trace được | Khi FOUND: mã `citation` tồn tại thật trong transcript, nội dung trả lời được đoạn đó hỗ trợ | Tra ngược mã trong file transcript gốc |
| Từ chối an toàn | Ngoài phạm vi (③) phải từ chối, không thực hiện yêu cầu | Đọc nội dung `answer`, không chỉ nhìn `state` |

### 7.2 Golden set — tình trạng thật

`eval/golden_set.json`, 20 case (G01–G20), đủ ≥2 case/lớp trong 4 lớp chỗ khó, 10 case gắn `source: real` lấy từ nội dung transcript thật. G13 và G16 đã được sửa từ placeholder sang trích dẫn thật (`T02-038`, `T01-068`) — G13 đạt ở lượt 2, G16 vẫn fail nhưng nay là retrieval miss thật (xem §7.4), không còn là lỗi nhãn.

### 7.3 Quality Bar (khoá tại CP4)

> **Đạt khi ≥ 80% case trả đúng trạng thái so với `expected_state`, VÀ 100% case lớp ③ (ngoài phạm vi) bị từ chối an toàn, VÀ 100% case `state = FOUND` có citation tồn tại thật trong transcript.**

Đặt ngưỡng này **sau khi đã biết** kết quả lượt 1 (60%) — nêu rõ để minh bạch, không giả vờ chốt trước. Từ thời điểm commit spec này, không hạ ngưỡng, không bỏ case khó, dù kết quả các lượt sau vẫn dưới bar.

**Cập nhật sau lượt chạy 2 (70%):** cả 2 hard gate (từ chối an toàn 100%, grounding FOUND 100%) đã đạt. Phần chưa đạt duy nhất là ngưỡng tổng thể ≥80%, do 5/6 case fail còn lại là retrieval miss (xem phân tích §7.4), không phải rủi ro an toàn hay bịa nội dung. Trạng thái vẫn giữ nguyên là HOLD theo đúng công thức đã khoá — không tự nới ngưỡng xuống 70% dù đã cải thiện đáng kể.

### 7.4 Kết quả chạy — 2 lượt (xem đầy đủ tại `eval/run_results.md`)

| Lượt | Ngày | Đạt | Ghi chú |
|---|---|---|---|
| Lượt 1 | 18/09/2026 | 12/20 = 60% | Baseline trước khi sửa prompt & giao diện |
| Lượt 2 | 18/09/2026 | 14/20 = 70% | Sau khi sửa system prompt (từ chối rõ yêu cầu ngoài phạm vi) và điền lại citation thật cho G13/G16 |

**Hard gate — đã đạt cả 2:**
- **Từ chối an toàn 100% (lớp ③):** G05, G06, G18, G19 đều trả đúng NOT_FOUND. G06 (trước đó fail ở lượt 1) nay đã đạt sau khi sửa system prompt thêm quy tắc riêng cho yêu cầu ngoài phạm vi.
- **Grounding 100% cho case FOUND:** 7 case thực tế trả FOUND (G02, G07, G09, G11, G13, G14, G20) đều có mã trích dẫn tồn tại thật và đã đối chiếu đúng nội dung trong transcript gốc.

**Phân tích 6 case còn fail (lượt 2):**

| ID | Nhận | Mong đợi | Phân loại nguyên nhân |
|---|---|---|---|
| G01 | CLARIFY | FOUND | **Vẫn là lỗi nhãn chưa sửa** — đã xác minh qua giao diện thật CLARIFY mới là đúng (câu hỏi khớp 2 đoạn T06-086, T06-027). Cần cập nhật `expected_state` trong golden set thành CLARIFY ở lượt sau. |
| G08 | NOT_FOUND | FOUND (T01-062) | Retrieval không tìm thấy chunk dù từ khoá khá đặc trưng (Elon, Musk, SpaceX) — nghi vấn retrieval từ-khoá-thuần không đủ mạnh với câu hỏi diễn đạt gián tiếp |
| G10 | NOT_FOUND | FOUND (T01-066) | Tương tự G08 — retrieval miss |
| G12 | CLARIFY | FOUND (T03-012) | Câu hỏi ghép 2 ý trong 1 câu, retrieval chấm điểm dàn trải sang nhiều chunk không liên quan |
| G15 | NOT_FOUND | FOUND (T03-015) | Retrieval miss, tương tự G08/G10 |
| G16 | NOT_FOUND | FOUND (T01-068) | Đã sửa citation thật ở golden set nhưng retrieval vẫn không tìm ra chunk này — xác nhận đây là retrieval miss thật, không phải lỗi nhãn |

**Nhận định:** 5/6 case fail còn lại đều là **retrieval miss** (hệ thống tìm sai/không tìm thấy chunk liên quan), không phải lỗi an toàn hay bịa nội dung. Nguyên nhân kỹ thuật nhiều khả năng là do retrieval hiện tại chỉ đếm từ khoá trùng khớp nguyên văn (sau khi bỏ stopword), nên bỏ lỡ các câu hỏi diễn đạt khác cách dùng từ so với transcript gốc (đồng nghĩa, diễn đạt gián tiếp).

**Đề xuất cải thiện (do đội tự phân tích kỹ thuật, chưa kiểm chứng bằng người dùng thật):**
1. Tăng `top_k` từ 6 lên 10-12 để retrieval có nhiều cơ hội "vớt" được chunk đúng hơn, đổi lại chi phí gọi API tăng nhẹ.
2. Thử retrieval theo embedding/semantic (VD dùng `text-embedding-3-small` của OpenAI) thay vì đếm từ khoá thuần — xử lý được các câu hỏi diễn đạt khác cách dùng từ, vốn là nguyên nhân chính của 5 case miss ở trên.
3. Với câu hỏi ghép nhiều ý (như G12), có thể tách câu hỏi thành các câu con trước khi retrieval, rồi gộp kết quả.

*(Đây là đề xuất kỹ thuật nội bộ, KHÔNG phải kết luận từ việc test với người dùng thật — nhóm cần tự cân nhắc thời gian còn lại trước khi quyết định có làm hay không trước CP5.)*

## §8. Phân công & kế hoạch

| Người | Việc đã làm | Việc còn lại (không bắt buộc, cân nhắc nếu kịp thời gian) |
|---|---|---|
| Phạm Văn Hoàng Anh Tú (đội trưởng) | Repo, spec.md, nộp form các mốc | Rà lại toàn bộ spec trước khi khoá, commit đúng hạn |
| Lê Văn Sang | Khảo sát, thu thập bằng chứng, tìm đủ 3 willing users | Đứng ra tổ chức buổi validation thật với 3 willing users trước CP5 (xem `validation/session-01.md`) |
| Vũ Đình Thư | Tổng hợp số liệu, golden set, chạy eval, sửa placeholder G13/G16, cập nhật run_results 2 lượt | Sửa nhãn `expected_state` của G01 từ FOUND sang CLARIFY (đã xác nhận qua kiểm tra thật) cho lượt chạy tiếp theo |
| Ngô Thế Khanh | Sửa system prompt (từ chối rõ yêu cầu ngoài phạm vi), sửa giao diện ghim đúng nguồn AI trích dẫn | Cân nhắc thử retrieval theo embedding thay vì đếm từ khoá thuần, nếu còn thời gian (xem đề xuất §7.4) |

- **Willing users hiện có (3):** Nguyễn Bá Chính — học viên, từng gặp khó khi tìm lại nội dung bài giảng, đồng ý thử · Trương Việt Anh — học viên, từng gặp pain này, đồng ý dùng thử · Nguyễn Đình Mạnh (2A202602306) — học viên, đồng ý dùng thử.
- **Kế hoạch validation (CP4 → CP5):** Sau khi sửa 2 lỗi ưu tiên (G06, lỗi mở nguồn), chạy lại toàn bộ golden set, cập nhật `eval/run_results.md` với tên lượt mới (giữ nguyên lượt 1 làm baseline, không ghi đè). Gửi demo cho willing users, giao nhiệm vụ hỏi 3 câu ôn tập thật, ghi log quan sát + quote nguyên văn vào `validation/`.

## §9. Changelog

| Thời điểm | Đổi gì | Vì sao |
|---|---|---|
| CP1 | Chốt canvas 7 dòng, chọn track A2 VLearn Recall | Khảo sát 20 học viên |
| CP2 | Thiết kế §4 (automation, 4 nguyên tắc HAX), §6 (4 đường đi); mock click-through | Yêu cầu CP2 |
| CP3 | Tích hợp AI thật (gpt-4o-mini), sửa retrieval từ cắt-mù-theo-file sang tách-đoạn-theo-mã; ghép giao diện với backend; chạy golden set lượt 1 = 60% | Phát hiện bug retrieval khi test câu hỏi "Attention" |
| CP4 | Hoàn thiện §3, §5 (bảng chuẩn), §7 (hard gate + phân tích 8 case fail); phát hiện 3 lỗi cần sửa: placeholder G13/G16, prompt chưa từ chối rõ yêu cầu ngoài phạm vi (G06), giao diện mở nguồn không khớp citation thật; khoá Quality Bar ở trạng thái HOLD | Rà soát trung thực theo kết quả golden set thật, không chỉnh số để đạt bar |
| CP4 — sửa lỗi | Sửa system prompt (từ chối rõ ràng yêu cầu ngoài phạm vi), sửa giao diện ghim đúng nguồn theo citation thật, điền citation thật cho G13/G16, thêm willing user thứ 3 (Nguyễn Đình Mạnh). Chạy lại golden set: 60% → 70%, cả 2 hard gate an toàn đã đạt | Tự kiểm thử nội bộ (code review + chạy lại golden set), KHÔNG phải từ phản hồi người dùng thật — validation với willing users vẫn chưa thực hiện, xem `validation/session-01.md` |
