# Kiểm chứng ca thử Q01

Môi trường: Windows PowerShell, Python 3 standard library, Poppler có sẵn. Ngày: 08/11/2026.

## Đã chạy

| Kiểm tra | Lệnh/cách thực hiện | Kết quả |
|---|---|---|
| Vault trước thử | `python GraphFlow_Research_Vault/13_Tools/validate_vault.py GraphFlow_Research_Vault` | Pass: 120 Markdown, 117 identified notes, 0 lỗi |
| Đóng băng | `python pilot_runs/2026-11-08_Q01/retrieval_probe.py --freeze` | Tạo snapshot hash tất cả file vault và protocol; không ghi lại đè |
| Lexical probe | `python pilot_runs/2026-11-08_Q01/retrieval_probe.py` | Pass; 85 note, 6 development queries; top-5 hit 6/6 ở cả hai điều kiện |
| Nguồn quyết định | Mở nguồn chính bằng URL; kiểm section/version; hai trang PDF được render bằng Poppler | Kiểm được venue PRISM của E05 và ngữ cảnh Table XI của E02; không nâng read depth toàn văn |
| Milestone đầu | Commit `3f11dd1`, normal push | Push thành công, tracking `origin/codex/graphflow-q01-pilot` |

## Kiểm cuối bằng lệnh Python/validator

`verification.json` lưu kết quả máy đọc được: so byte-hash vault với baseline, kiểm protocol, tính tái chạy probe, JSON/link/ID/reference của pilot và chạy lại validator gốc. File được sinh từ kiểm thực tế, không phải bảng kết quả kỳ vọng. Những kiểm này chứng minh toàn vẹn hồ sơ, không chứng minh kết luận khoa học.

**Kết quả cuối: PASS.** Cả 135 file vault khớp snapshot; protocol không đổi; replay probe giống byte; 9 source, 10 claim, 8 relation và 3 hypothesis có reference hợp lệ; không có link Markdown local bị thiếu. Validator gốc vẫn báo 0 lỗi. Top-1 được tính bổ sung từ output cố định, không dùng để chỉnh glossary rồi chạy lại.

## Chưa kiểm / điều kiện đóng

- **Novelty chuyên ngành:** chưa xác nhận. Cần đọc sâu prior art cùng task, tìm trích dẫn hai chiều và các miền lân cận; không có bảo đảm bao phủ toàn thế giới.
- **Kết quả paper:** tất cả giữ `results_reproduced: false`. Cần artifact, license, môi trường và thiết kế thí nghiệm trước tái lập.
- **RAG/generator:** chưa triển khai hay thử. Hai answer probes là quyết định đọc bằng chứng thủ công; cần lưu câu trả lời thực tế của pipeline rồi chấm độc lập.
- **Độ ổn định:** một ca thử có giới hạn. Cần nhiều ca, nhóm giữ lại và đánh giá riêng relevance/answer sufficiency.
- **Tri thức ngoài riêng của người dùng:** chưa có đầu vào mới; chưa thể kết hợp kinh nghiệm hoặc ghi chú không được cung cấp.
- **User acceptance:** pending. Người dùng chưa xem hồ sơ và chưa chọn Q01/G2 làm đề tài.
- **Khả năng tái chạy từ clone:** vault nền vẫn untracked theo trạng thái ban đầu và không được commit trong phạm vi ca thử. Cần đúng snapshot có hash khớp; không tự công bố đây là gói độc lập chứa đủ toàn bộ corpus.

Lỗi công cụ/truy cập được giữ tại `SEARCH_LOG.md`, gồm reference tạm trả sai tài liệu, screenshot không hỗ trợ và một nguồn PDF bị 403. Đã dùng đường truy cập khác cho tài liệu quyết định; không dùng nguồn không kiểm được để điền chi tiết thiếu.
