# Reflection cá nhân — Vũ Đình Thư (2A202602652)

## Vai trò
Member — tổng hợp số liệu khảo sát, xây golden set, chạy eval; người quan sát phiên validation R6 của Trương Việt Anh.

## Phần mình làm
- Xây `eval/golden_set.json` (20 case G01-G20, đủ 4 lớp độ khó).
- Chạy `eval/run_golden_set.py` nhiều lượt, ghi kết quả trung thực vào `eval/run_results.md` (kể cả lượt fail, không sửa golden set để "cứu" số).
- Tổng hợp số liệu khảo sát thành bảng đánh giá case theo trạng thái FOUND/CLARIFY/NOT_FOUND + citation.
- Quan sát phiên validation R6 với Trương Việt Anh — ghi nhận quote thật về nhánh CLARIFY chưa đủ cụ thể.

## AI hỗ trợ thế nào
*(Tự điền: dùng AI để làm gì trong phần xây golden set/eval — ví dụ sinh case nháp rồi mình tự kiểm tra lại theo 4 lớp khó, hay viết script eval — và chỗ nào mình tự đối chiếu số liệu thủ công để đảm bảo đúng.)*

## Một bài học từ case fail của chính nhóm
Golden set giữ nguyên 70% (14/20) qua các lượt chạy sau khi sửa nhánh CLARIFY — vì patch chỉ đổi phần `answer` (text gợi ý), không đổi `state`/`citation` là 2 trường được `evaluate_case()` chấm điểm. Ban đầu có thể hiểu nhầm là "sửa mà không cải thiện được gì", nhưng đây là kết quả đúng như kỳ vọng: sửa UX của nhánh CLARIFY và sửa retrieval là hai vấn đề khác nhau, không nên lẫn lộn khi đọc số liệu eval.

*(Tự điền thêm: bài học cá nhân về cách đọc/diễn giải số liệu eval, phân biệt "cải thiện trải nghiệm" và "cải thiện độ chính xác", hoặc điều mình muốn làm khác nếu có thêm thời gian cho golden set.)*
