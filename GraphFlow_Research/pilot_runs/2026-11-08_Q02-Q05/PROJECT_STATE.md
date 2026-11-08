# Các ca thử Q02–Q05 — 08/11/2026

## Ý định và quyết định

- `requested`: tiếp tục với các phần khác sau ca Q01. Hiểu trong phạm vi hiện tại là Q02–Q05, đã thông báo giả định này trước khi làm.
- `approved`: thử cơ chế bằng tri thức đang có và nguồn ngoài, tối dần rồi mới tái tổ hợp vault.
- `correction_from_user_context`: không coi tìm thấy prior art là câu hỏi “không ổn”. Q là đối tượng học/tổng hợp; novelty chỉ được đánh giá khi đã hình thành một đóng góp cụ thể.
- `proposed_by_agent`: mỗi Q có một vòng đọc và đối chiếu có giới hạn, một câu trả lời có nguồn, điều kiện áp dụng, phần thiếu và bước khảo sát/thí nghiệm kế tiếp. Không tự chọn đề tài cho người dùng.
- `unknown`: môi trường triển khai, dữ liệu và kinh nghiệm riêng ngoài vault chưa được cung cấp.

## AS-IS và tác động

- Giữ nguyên vault và hồ sơ ca Q01. Bốn Q đều đang `candidate`, novelty `unverified`, `human_decision: not_yet_selected`.
- Q02 có P09/P21 về khung đánh giá nhưng note chưa đọc kỹ nội dung; Q03 phân biệt đổi dự đoán với hành động; Q04 có benchmark agent tổng quát; Q05 có giả định replica trong P12.
- Chủ sở hữu dữ liệu mới là thư mục run này; không thêm ID chuẩn P/K/R, không sửa JSON export/manifest gốc.
- Không thay UI/API/database/model; không triển khai Cloud, chạy mã từ paper hoặc gọi mô hình trả phí. Tác động mã chỉ là công cụ kiểm hồ sơ nếu cần.
- Git: tiếp tục nhánh `codex/graphflow-q01-pilot`, stage riêng file run. Vault, `.obsidian` và canvas chưa đặt tên đang untracked trước lượt này; bảo toàn chúng.

## Trạng thái kiểm chứng

- `verified_before`: đã đọc Q02–Q05, nearest-paper notes và claim liên quan; dùng nguồn gốc như metadata về mức đã đọc, không tự coi là người dùng duyệt.
- `implemented`: `sources.json` quản lý 15 nguồn (7 nguồn có sẵn, 8 nguồn ngoài; 10 đọc chọn phần, 5 abstract); `casebook.json` quản lý 4 ca, 16 claim và 7 quan hệ. Mọi câu trả lời có scope/claim/source/locator/limitation và phần chưa biết.
- `implemented`: A02–A05 lưu câu trả lời tổng hợp thủ công thực tế; không ghi chúng như benchmark generator hoặc kết quả model độc lập.
- `verified`: raw lexical probe 85 note/8 câu tiếng Việt tìm topic note 7/8. Trong 7 câu có nhãn P/K/D trước chạy, lọc candidate về 46 note P/K/D tăng evidence hit top-5 từ 4/7 lên 6/7; đây là adaptive development check, không giữ lại, không đủ chốt retriever chuẩn.
- `implemented`: `render_casebook.py` sinh Q02–Q05 Markdown từ hai JSON owners; `MECHANISM_REVIEW.md` tổ chức các vai trò tương hỗ và bước tối tiếp; chưa đổi schema/vault gốc.
- `verified_after`: hash 135 file vault và 12 file hồ sơ Q01 khớp nền; protocol không đổi; hai probe replay giống byte; source/claim/answer/relation/link và bản đọc sinh từ JSON được kiểm bằng `verify_run.py`. Kết quả cuối ở `verification.json`.
- `not_accepted`: người dùng chưa duyệt kết quả mới. Không có câu hỏi nào được chọn làm đề tài trong run này.

## Điều kiện hoàn tất lượt này

Q02–Q05 đều có chuỗi nguồn → claim → câu trả lời có phạm vi → nội dung cần kiểm tiếp, cùng ít nhất một đối chiếu có thể thay đổi cách hiểu. Không đòi mỗi Q phải sinh một gap mới. Ghi rõ phần chỉ có metadata/abstract, phần đọc chọn mục và phần chưa tái lập.

## Checkpoint và phát hành

- `ebf446e`: hồ sơ nguồn/casebook và hai probe đã commit/push lên `origin/codex/graphflow-q01-pilot`.
- Bản đọc, log tìm kiếm và kiểm cuối được commit tiếp sau đó; xem Git history để tra hash cuối.
- Chỉ file trong run được stage. Corpus và canvas/configuration của người dùng giữ nguyên, không được nhập ngầm vào upstream. Push hồ sơ không phải deployment hoặc backup toàn bộ vault.
