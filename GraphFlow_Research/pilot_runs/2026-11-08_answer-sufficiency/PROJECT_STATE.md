# Lượt thử độ đủ bằng chứng — 08/11/2026

## Ý định và quyết định

- `requested`: người dùng nói “tiếp” sau đề xuất kiểm câu trả lời trên nhóm câu mới trước khi tái tổ hợp kho.
- `approved`: tiếp tục thử và tối dần; chưa nhập ngầm tri thức thử vào vault chuẩn, chưa chọn Q làm đề tài.
- `proposed_by_agent`: dùng 12 câu mới trên những chủ đề đã biết, đóng băng câu/nhãn/rubric trước khi truy xuất; kiểm việc tìm đủ các mảnh bằng chứng cần thiết và trả lời có phạm vi.
- `limitation_known_before`: cùng AI biết các chủ đề, tạo câu và viết/chấm câu trả lời. Đây là forward diagnostic với câu mới, không phải kiểm mù, không phải tập độc lập do người khác giữ lại.
- `proposed_by_agent`: so corpus note chuẩn với corpus thêm tất cả 26 claim từ hai pilot cũ dưới dạng card có nguồn/phiên bản/vị trí/giới hạn. Chỉ đóng gói cho thử; không sửa hay tái tổ hợp canonical vault.

## AS-IS, chủ sở hữu và phạm vi tác động

- Q01 có 10 claim; Q02–Q05 có 16 claim. Các hồ sơ có metadata provenance, câu trả lời thủ công và mức đọc, chưa có generator pipeline hay API model riêng được triển khai.
- Truy xuất hiện có là BM25 trên note; lọc P/K/D đã có tín hiệu trên tập phát triển. Giữ nguyên thuật toán và k=5, không tiếp tục chỉnh từ vựng theo bộ mới.
- `protocol.json` sở hữu câu hỏi/facet/nhãn/rubric. `cards.json` là bản sinh từ claim cũ, có lineage. `retrieval_results.json` và `packets.json` lưu kết quả/đầu vào câu trả lời. `answers.json` sẽ lưu câu trả lời thực tế và tự rà support.
- 135 file vault, hai pilot cũ, `.obsidian` và hai canvas untracked ở root được bảo toàn. Không tải/chạy code nghiên cứu, dựng Cloud/lab, gọi API trả phí hoặc gửi dữ liệu cho bên thứ ba.
- Không thay UI/API/database. Công cụ cục bộ chỉ đóng gói, truy xuất và kiểm toàn vẹn hồ sơ.

## Các tầng trạng thái

- `verified_before`: đã nạp trạng thái và code của các lượt trước; đọc lại claim/giới hạn làm cơ sở gán nhãn trước probe.
- `implemented`: protocol 12 câu/rubric/nhãn đóng băng trước probe; corpus 46 note so với 72 record (46 note + 26 card có lineage). Không chỉnh ranker/query sau khi thấy kết quả lượt đầu.
- `verified`: reference-facet coverage là 3/10 và 8/10; hai câu abstention không vào mẫu số. Hai ca augmented miss là N02 và N07. Đây là coverage theo nhãn định trước, chưa là answer accuracy.
- `implemented`: 12 câu trả lời thực tế và 22 mệnh đề nối excerpt, giữ 1 ca retrieval-insufficient, 1 partial, 1 conflict và 2 ca từ chối kết luận không đủ bằng chứng.
- `implemented`: một vòng repair cho N02/N07 có protocol/output/answer riêng; cả hai lấy lại được facet cần. Kết quả đầu và câu trả lời đầu không đổi; không nâng score thành 10/10.
- `verified`: bốn control lỗi cấu trúc bị từ chối; một control citation đúng nhưng mệnh đề ngược nghĩa vẫn qua kiểm cơ học và được đánh dấu sai khi cùng AI tự đối chiếu. Chưa có semantic judge độc lập.
- `implemented`: `README.md` tổng hợp kết quả; `ANSWERS.md`/`REPAIRED_ANSWERS.md` sinh từ owner JSON; các kiểm cuối và giới hạn ở `VERIFICATION.md`/`verification.json`.
- `verified_after`: replay và repair giống byte, cả 135 file vault + 12 file Q01 + 21 file Q02–Q05 khớp nền; trích dẫn/lineage/render/local links qua kiểm cấu trúc; validator vault vẫn 120 Markdown/117 identified notes/0 lỗi. Pass cấu trúc không che lỗi semantic control đã nêu.
- `unknown`: hiệu quả generator tự động, đánh giá độc lập, khả năng chuyển sang câu/domain chưa thấy và kết quả vận hành thực.
- `not_accepted`: người dùng chưa duyệt kết quả lượt này. Quyền tiếp tục không là chấp nhận kết luận.

## Điều kiện hoàn tất

Đủ 12 câu có packet và câu trả lời thực tế (có thể partial/insufficient/conflict); mỗi nhận định có evidence ID/locator và giới hạn; phân loại retrieval miss, content not captured, missing local experiment và unresolved version. Không điền kiến thức ngoài packet để làm đẹp điểm. Giữ riêng mechanical reference-facet coverage với semantic sufficiency do AI tự rà.

## Checkpoint

- `a8cf3bb`: protocol, frozen inputs, 26 card và packet/kết quả lượt đầu đã commit/push lên `origin/codex/graphflow-q01-pilot` trước khi chốt đáp án/tự rà.
- Checkpoint đáp án, repair và kiểm cuối theo sau; xem Git history cho hash cuối, tránh commit tự tham chiếu.
- `not_accepted` vẫn giữ nguyên; việc này chưa chứng nhận RAG ổn định hoặc quyền hợp nhất toàn kho.
