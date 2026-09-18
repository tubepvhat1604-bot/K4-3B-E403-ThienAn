# Reflection cá nhân — Ngô Thế Khanh

- **MSSV:** 2A202602503
- **GitHub:** [@khanhken159](https://github.com/khanhken159)
- **Dự án:** VLearn Recall — Track A2

## Vai trò và phần việc

Trong dự án VLearn Recall, tôi phụ trách thiết kế system prompt, phần truy xuất học liệu (retrieval), tích hợp AI thật và ghép giao diện. Tôi xây dựng luồng xử lý câu hỏi nhớ mang máng của học viên theo ba trạng thái: `FOUND` khi có nguồn phù hợp, `CLARIFY` khi cần hỏi rõ thêm và `NOT_FOUND` khi không tìm thấy căn cứ trong học liệu. Phần việc của tôi còn gồm kết nối kết quả từ backend với giao diện để học viên xem câu trả lời và mở đoạn nguồn liên quan.

## AI đã hỗ trợ tôi như thế nào

Tôi dùng AI để gợi ý cấu trúc prompt, rà soát các trường hợp biên và hỗ trợ chỉnh sửa code prototype. AI giúp tôi thử nhanh các cách xử lý câu hỏi, nhưng tôi vẫn phải quyết định tiêu chí định tuyến và đối chiếu kết quả với transcript/slide. Qua kết quả kiểm thử của nhóm, tôi nhận ra việc có prompt yêu cầu không đoán hoặc có trích dẫn trên giao diện chưa đủ để chứng minh hệ thống hoạt động đúng; cần kiểm tra cả phản hồi thực tế và đoạn nguồn mà người dùng mở được.

## Bài học từ các case thất bại của nhóm

Theo bản tổng hợp nhóm chia sẻ, kết quả hiện tại đạt 60% và vẫn ở trạng thái **HOLD**, chưa đạt ngưỡng hard gate ≥80% cùng hai điều kiện cứng. Tôi xem đây là kết quả cần phản ánh trung thực, không thể coi việc đã nối AI thật và chạy được giao diện là sản phẩm đã đạt yêu cầu.

Case **G06** là bài học rõ nhất đối với phần tôi phụ trách: hệ thống chưa từ chối rõ ràng yêu cầu ngoài phạm vi, vi phạm hard gate an toàn. Đây là lỗi hệ thống cần ưu tiên sửa. Tôi nhận ra prompt phải quy định rõ cách xử lý yêu cầu ngoài phạm vi, và hành vi từ chối phải được kiểm chứng bằng case cụ thể thay vì chỉ dựa vào nội dung hướng dẫn trong prompt.

Một lỗi khác nằm ở nút **“Mở nguồn”**: giao diện cần mở đúng chunk theo `citation` thật mà backend trả về, thay vì tự xếp hạng nguồn riêng ở frontend. Nếu câu trả lời dẫn một đoạn nhưng nút lại mở đoạn khác, học viên vẫn có thể ôn sai nội dung. Vì vậy, tôi cần kiểm tra toàn bộ luồng từ truy xuất, sinh câu trả lời đến thao tác mở nguồn.

Tôi cũng học được cách phân biệt nguyên nhân khi đọc kết quả eval. Trong 8 case fail, nhóm xác định G01, G13 và G16 là lỗi nhãn; G06 là lỗi hệ thống thật; còn G08, G10, G12 và G15 cần thêm log để điều tra retrieval. Không nên sửa prompt theo mọi case fail khi chưa xác định lỗi nằm ở nhãn đánh giá hay ở hệ thống.

## Điều tôi sẽ cải thiện

Trước CP5, tôi ưu tiên hai việc theo phân công của nhóm:

1. Sửa system prompt để từ chối rõ ràng yêu cầu ngoài phạm vi, tập trung vào G06, rồi chạy kiểm thử lại để xác nhận hành vi thực tế.
2. Sửa nút “Mở nguồn” để hiển thị đúng chunk theo `citation` từ backend, đồng thời kiểm tra sự khớp nhau giữa câu trả lời, mã trích dẫn và nội dung được mở.

Tôi sẽ phối hợp với Thư đọc thêm log context của G08, G10, G12 và G15 để xác định nguyên nhân trước khi điều chỉnh retrieval. Việc sửa placeholder G13/G16 và bổ sung log thuộc phần Thư phụ trách; tôi dùng kết quả đó để rà lại phần tích hợp của mình.

Các việc trên là kế hoạch cần hoàn thành và kiểm chứng, chưa phải kết quả đã sửa xong. Nếu lần chạy lại chưa đáp ứng đầy đủ điều kiện, tôi sẽ cùng nhóm giữ trạng thái HOLD và ghi rõ phần còn thiếu. Bài học lớn nhất của tôi là phải chịu trách nhiệm về hành vi thực tế của phần mình làm, từ quyết định trả lời hay từ chối đến việc đưa người dùng tới đúng nguồn.
