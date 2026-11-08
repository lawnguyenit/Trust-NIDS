# Kiểm chứng và giới hạn

Ngày 08/11/2026. Windows PowerShell; Python standard library cho hồ sơ/probe; bundled Python `pypdf` và Poppler cho đọc/render trang PDF.

## Lệnh chạy được lưu cùng kết quả

```powershell
python -B pilot_runs/2026-11-08_Q02-Q05/retrieval_probe.py
python -B pilot_runs/2026-11-08_Q02-Q05/evidence_routing_probe.py
python -B pilot_runs/2026-11-08_Q02-Q05/render_casebook.py
python -B pilot_runs/2026-11-08_Q02-Q05/verify_run.py
```

`verify_run.py` kiểm JSON, nguồn/claim/answer/relation references, trạng thái chưa duyệt/chưa tái lập, link Markdown local, bản đọc sinh từ JSON, hash vault/hồ sơ Q01/protocol; tái chạy hai probe và so output byte-hash; gọi lại validator vault gốc. `verification.json` lưu lệnh cụ thể, exit code, check và counts từ việc chạy thật.

Kiểm cuối: PASS, 135 file vault và 12 file Q01 giữ nguyên; 15 nguồn/16 claim/7 quan hệ/4 ca có reference hợp lệ; hai replay giống byte; 4 bản đọc khớp JSON; validator vault gốc 120 Markdown/117 identified notes/0 lỗi. Lượt kiểm đầu ghi một link tới chính output verification chưa tồn tại; sau khi output được tạo, đã kiểm lại link thực tế, không bỏ qua mục lỗi này.

## Phạm vi chứng minh

- Nguồn: mức `sections_checked` hoặc `abstract_primary` như từng E ghi. Chỉ ba trang quyết định được render/xem nguyên trang; không gọi đó là đọc và kiểm mọi trang của mọi paper.
- Câu trả lời A02–A05: đầu ra tổng hợp thủ công đã lưu, nối tới claim. Chưa có một generator độc lập được chạy/chấm.
- Truy xuất: BM25 trên note gốc; câu hỏi và nhãn do cùng AI tạo. Thử lọc P/K/D là adaptive development check; chưa giữ lại tập kiểm độc lập.
- Toàn vẹn: hash và validator chứng minh không sửa corpus cũ và cấu trúc hồ sơ hợp lệ. Không chứng minh nguồn đúng, novelty hoặc kết luận đã được chuyên gia duyệt.
- Thực tiễn: chưa chạy artifact, tấn công, response action, lab hay Cloud. Chưa có ground truth, ngân sách hoặc quyền triển khai để đo các kết quả đó.
- Phát hành: chỉ run được commit/push trên nhánh pilot; corpus gốc đang untracked được bảo toàn, chưa thành backup đầy đủ trên upstream. Không có deployment.

## Điểm còn mở

| Điểm mở | Điều kiện đóng |
|---|---|
| T04B thiếu nhãn source/claim trong protocol | Tạo bộ kiểm mới với nhãn evidence trước chạy; không điền nhãn hậu nghiệm rồi tính lại điểm của bộ cũ |
| T05B vẫn miss bằng chứng trong top 5 | Chẩn đoán từ vựng/độ sâu note/candidate routing trên ca mới; không mặc định thêm embedding là đủ |
| E01 khác denominator giữa landing/PDF | Xác định lịch sử/version và đối chiếu bản proceedings trước sửa canonical claim |
| Source support và answer sufficiency | Một lượt chấm riêng theo từng claim, có ca thiếu bằng chứng và người đánh giá độc lập khi có thể |
| Độ ổn định qua task | Tập câu khác, rubric cố định, lặp lại; một batch thủ công chưa đủ |
| Chấp nhận của người dùng | Người dùng xem/duyệt kết quả; không suy từ quyền chạy thử |

Lỗi truy cập/encoding và hướng khắc phục có ở `SEARCH_LOG.md`. Kết quả máy của lần kiểm cuối là nguồn xác nhận trạng thái pass/fail; không xóa dấu vết của giới hạn để báo hoàn tất.
