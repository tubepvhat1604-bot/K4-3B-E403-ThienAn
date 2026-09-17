# Mini Hackathon AI — Batch 04 · Lớp 3B

**SPEC → Prototype → Demo.** Đây không phải cuộc thi code — đây là cuộc thi **tư duy sản phẩm AI**.

## 👥 Thành viên nhóm & Phân công vai trò

**Lớp:** 3B · **Phòng:** ____ · **Cụm:** ____ · **Track:** A2 — VLearn Recall

| Họ và Tên | Mã Học Viên | Vai trò chính | Phần việc đảm nhiệm trong dự án |
| --------- | ----------- | -------------- | -------------------------------- |
| Phạm Văn Hoàng Anh Tú | 2A202602507 | Leader | Đội trưởng · tạo & quản lý repo · viết/chốt spec.md · nộp form checkpoint |
| Lê Văn Sang | 2A202602391 | Member | Khảo sát học viên · thu thập & tổng hợp bằng chứng (evidence) |
| Ngô Thế Khanh | 2A202602503 | Member | Thiết kế prompt/logic AI · xây prototype · tích hợp lời gọi AI thật |
| Vũ Đình Thư | 2A202602652 | Member | Tổng hợp số liệu khảo sát · xây golden set · chạy eval |

> Nhóm copy nguyên file README này về repo của mình, rồi điền bảng trên. Cột **Phần việc đảm nhiệm** ghi càng cụ thể càng tốt.

- Thời lượng: **39 giờ** từ phát đề đến thuyết trình (ca 3B) — LAB 5 (phát đề + build) · LEC 6 (tiếp tục build theo ca) · LAB 6 (vòng thi)
- Nhóm: **3-4 người** · thi theo phòng (E403 / E402), chia cụm rồi chung kết phòng — xem *Thể thức thi*
- **Chia cụm theo bàn**, không cần chung đề tài. Chủ đề tự chọn trong khuôn khổ đề bài
- Nhóm nhỏ thì **chọn lát cắt nhỏ**, và phải có **khảo sát nỗi đau thật** — đây là chỗ ăn điểm nặng nhất

## Bắt đầu từ đâu?

1. Đọc **`01-challenge-brief.md`** để hiểu khung chung và 5 tiêu chí, rồi **`tracks/README.md`** để chọn track và đề.
2. Mở **`02-guide.md`** — hướng dẫn từng giai đoạn, đứng ở đâu đọc mục đó.
3. Viết spec theo **`03-ai-spec-template.md`** — deliverable trung tâm của cả sự kiện.
4. Đọc **`04-rubric.md`** ngay từ đầu — biết trước bài được chấm theo tiêu chí nào.

| File / thư mục | Nội dung |
| --- | --- |
| `01-challenge-brief.md` | Đề bài: bảng 5 track · lát cắt · ràng buộc chung · 5 tiêu chí nghiệm thu |
| `02-guide.md` | Hướng dẫn 5 giai đoạn: khám phá → spec → build → đo & validate → demo |
| `03-ai-spec-template.md` | Template AI Spec (nộp tại **hạn chốt spec** — xem Lịch) |
| `04-rubric.md` | Rubric 100 điểm (25 nộp checkpoint + 67 chấm bài + 8 điểm R6) + checklist xác minh 6 mốc |
| `tracks/` | **5 track**, mỗi đề cùng một khung mục — bắt đầu từ `tracks/README.md` |
| `data/` | Dữ liệu thật đã ẩn danh: `vlearn-pack/` và `discord-pack/` — dùng để tìm bằng chứng và xây golden set. **Đọc `data/README.md` trước** |
| `further-reading/` | Tài liệu tham khảo — bắt đầu từ `further-reading/README.md` |

## Lịch — 6 checkpoint (ca 3B · 39 giờ)

| Mốc | Cần hoàn thành | Hạn (ca 3B) |
| --- | --- | --- |
| — | Khai mạc 17:30 · phát đề 18:00 | 17/9 |
| **CP1** | Canvas 4 ô + đội trưởng + **link repo GitHub công khai** | **19:30** · 17/9 |
| **CP2** | Cho thấy **luồng hoạt động** — bấm thử được, hoặc sơ đồ luồng | **21:00** · 17/9 |
| **CP3** | **Video thao tác** 30 giây + **số đo** (thử bao nhiêu, đúng bao nhiêu) | **16:00** · 18/9 |
| **CP4** | Chốt `spec.md` — **khoá chuẩn "đạt"** · tự khai phần chưa xong | **21:00** · 18/9 |
| **CP5** | Slide PDF + **video demo dự phòng cho buổi pitch** — nộp cuối | **22:30** · 18/9 |
| **CP6** | Thuyết trình · không nộp thêm | **09:00** · 19/9 |

**CP1 đến CP5 mỗi mốc 5 điểm.** Nộp đúng hạn được đủ, nộp muộn là **0 điểm mốc đó** — không bù được bằng mốc khác.

## Nộp bài

### Tạo repo mới — không fork repo đề bài

Nhóm tạo một repo **hoàn toàn mới và trống**. Không fork, không clone repo này rồi push lên.

### Cấu trúc repo

```
repo/
├── README.md          ← copy file này, điền bảng thành viên ở đầu
├── spec.md            ← AI Spec theo 03-ai-spec-template.md
├── canvas.md           ← Canvas 7 dòng CP1
├── demo-slides.pdf    ← slide 6 trang theo 02-guide.md §5.1
├── codebase/          ← prototype (ghi rõ phần nào mock)
├── eval/              ← golden set + bảng kết quả các lượt chạy
├── validation/        ← nhật ký cho người ngoài dùng thử (R6)
└── reflection/        ← mỗi người 1 file
```

## Link nộp

| Mốc | Form nộp |
| --- | --- |
| CP1 | *(cập nhật lúc khai mạc)* |
| CP2 | *(cập nhật lúc khai mạc)* |
| CP3 | *(cập nhật lúc khai mạc)* |
| CP4 | *(cập nhật lúc khai mạc)* |
| CP5 | *(cập nhật lúc khai mạc)* |

> **Đội trưởng nộp form thay cả nhóm** — một phiếu cho cả nhóm ở mỗi mốc. **Cả 5 mốc phải nộp bằng cùng một mã học viên của đội trưởng** (2A202602507).

## Luật chung

1. Prototype có 3 mức **Sketch / Mock / Working** — mức nào cũng bắt buộc **≥1 lời gọi AI chạy thật**. Đây là thứ phải thấy được trong **video thao tác ở CP3**.
2. **Vibe-coding rule:** dùng AI để build thoải mái, nhưng không giải thích được phần có tên mình thì phần đó 0 điểm.
3. **Quality bar** chốt tại hạn chốt spec (21:00 18/9, tại CP4) và giữ nguyên sau đó.
4. Chỉ dùng dữ liệu trong `data/` hoặc dữ liệu giả tự sinh — không dùng dữ liệu thật của người thật. Không commit API key.
5. Tuân thủ quy định bảo mật dữ liệu — không commit data pack, khảo sát gốc, tên/MSSV người được hỏi.
