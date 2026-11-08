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
- `in_progress`: khảo sát nguồn chính, đọc chọn phần quyết định, viết câu trả lời thực tế và truy vết suy luận cho từng Q.
- `pending`: kiểm tính toàn vẹn, log delta, kết luận qua nhiều ca.
- `not_accepted`: người dùng chưa duyệt kết quả mới. Không có câu hỏi nào được chọn làm đề tài trong run này.

## Điều kiện hoàn tất lượt này

Q02–Q05 đều có chuỗi nguồn → claim → câu trả lời có phạm vi → nội dung cần kiểm tiếp, cùng ít nhất một đối chiếu có thể thay đổi cách hiểu. Không đòi mỗi Q phải sinh một gap mới. Ghi rõ phần chỉ có metadata/abstract, phần đọc chọn mục và phần chưa tái lập.
