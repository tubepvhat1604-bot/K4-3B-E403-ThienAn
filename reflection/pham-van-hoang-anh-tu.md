# Reflection cá nhân — Phạm Văn Hoàng Anh Tú (2A202602507)

## Vai trò
Leader — đội trưởng, tạo và quản lý repo, viết/chốt `spec.md`, nộp form ở tất cả 6 checkpoint.

## Phần mình làm
- Viết và chốt `spec.md` (Quality Bar §7.3, phân tích 4 lớp khó, bảng đánh giá §7.4).
- Quản lý cấu trúc repo, đảm bảo đúng yêu cầu README.md (thư mục phẳng ở gốc, không lộ `data/`).
- Tổng hợp kết quả validation R6 thật từ 3 người thử ngoài nhóm vào `validation/session-01.md`.
- Điều phối sửa nhánh CLARIFY trong `codebase/ai_recall.py` dựa trên feedback validation thật.
- Dựng `demo-slides.pdf` theo đúng cấu trúc 6 trang bắt buộc ở `02-guide.md` §5.1.
- Nộp form ở từng checkpoint đúng hạn.

## AI hỗ trợ thế nào
*(Tự điền: dùng AI để làm gì cụ thể — viết prompt, sửa lỗi git, dựng slide, phân tích log... — và chỗ nào mình tự quyết định/tự kiểm tra lại chứ không để AI làm hết.)*

## Một bài học từ case fail của chính nhóm
Golden set dừng ở 70% (14/20), 6 case fail (G01, G08, G10, G12, G15, G16) đều là retrieval miss do cơ chế keyword matching không bắt được câu hỏi diễn đạt khác từ ngữ gốc trong transcript — đúng như người thử validation thứ 3 (Nguyễn Đình Mạnh) phát hiện độc lập: "Đoạn có nhiều từ giống câu hỏi chưa chắc là đoạn trả lời đúng nhất." Nhóm quyết định **không sửa retrieval** trong CP5 vì đây là thay đổi kiến trúc lớn, rủi ro phá 2 hard gate an toàn đang đạt 100% nếu làm vội trong vài giờ cuối, và Quality Bar đã khoá từ CP4 không được đổi ngưỡng.

*(Tự điền thêm: bài học cá nhân rút ra từ việc này là gì — ví dụ về đánh đổi giữa "sửa nhanh" và "sửa đúng", về việc trung thực ghi nhận fail thay vì che giấu số liệu, v.v.)*
