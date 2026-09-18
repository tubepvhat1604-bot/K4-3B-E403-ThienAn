# Reflection cá nhân — Ngô Thế Khanh (2A202602503)

## Vai trò
Member — thiết kế prompt/logic AI, xây prototype, tích hợp lời gọi AI thật; người quan sát phiên validation R6 của Nguyễn Đình Mạnh.

## Phần mình làm
- Thiết kế `SYSTEM_PROMPT` và logic 3 trạng thái FOUND / CLARIFY / NOT_FOUND trong `codebase/ai_recall.py`.
- Xây prototype, tích hợp lời gọi AI thật (không hardcode) cho quyết định trung tâm.
- Áp dụng patch sửa nhánh CLARIFY sau khi có feedback validation thật (thêm gợi ý cụ thể khi 2 lựa chọn đều chưa đúng ý học viên).
- Quan sát phiên validation R6 với Nguyễn Đình Mạnh — ghi nhận phát hiện quan trọng về retrieval keyword matching.

## AI hỗ trợ thế nào
*(Tự điền: dùng AI để làm gì trong phần prompt/code — ví dụ generate code khung, debug lỗi, viết prompt nháp rồi mình tự chỉnh — và chỗ nào mình tự quyết định logic, tự test lại.)*

## Một bài học từ case fail của chính nhóm
Người thử mình quan sát (Nguyễn Đình Mạnh, mức nghiêm trọng Cao) phát hiện: "Đoạn có nhiều từ giống câu hỏi chưa chắc là đoạn trả lời đúng nhất" — đúng nguyên nhân gốc rễ của 5/6 case fail trong golden set (retrieval dựa keyword matching, không bắt được ngữ nghĩa khi diễn đạt khác từ ngữ gốc). Mình là người trực tiếp thiết kế phần logic AI nên đây là bài học rõ nhất: đo bằng máy (golden set) đúng, nhưng phải có validation người thật mới xác nhận được nguyên nhân gốc — không thể chỉ nhìn % để đoán bug nằm ở đâu.

*(Tự điền thêm: bài học cá nhân cụ thể hơn về việc thiết kế retrieval/prompt, và vì sao quyết định không sửa kiến trúc vội trong CP5 là hợp lý hay có điều mình muốn làm khác đi.)*
