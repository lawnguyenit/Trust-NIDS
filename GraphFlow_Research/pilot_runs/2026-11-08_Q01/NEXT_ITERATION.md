# Lượt tiếp theo — đề xuất sau ca thử, chưa thực hiện

**Giữ Q01 làm hồ sơ thử; chưa tái tổ hợp vault.** Thay đổi kế tiếp nên nhắm vào chất lượng đường dẫn bằng chứng và kiểm câu trả lời, vì mở rộng từ khóa chưa cho lợi ích top-5 ở ca đầu.

## Thứ tự thử

1. **So ca dễ và ca khó:** lấy câu hỏi tiếng Việt tự nhiên của người dùng, câu hỏi nhiều bước nối claim, câu có tiền đề sai và câu chưa đủ bằng chứng. Tách một nhóm phát triển khỏi nhóm chỉ mở sau khi chốt cách truy xuất. Không chép lại tên paper vào mọi câu để làm bài thử quá dễ.
2. **Kiểm truy xuất trước generator:** chấm relevance và độ đủ bằng chứng riêng. Ghi note/đoạn chứa kết quả, phiên bản và giới hạn; so lexical baseline với điều chỉnh nhỏ, chỉ giữ điều chỉnh có bằng chứng cải thiện trên nhóm giữ lại.
3. **Thử trả lời có ràng buộc:** mỗi nhận định phải có source/locator, loại `author_reported` hoặc `reviewer_inference`, điều kiện áp dụng và lý do đủ/chưa đủ bằng chứng. Ghi câu trả lời thực tế rồi mới chấm; không lấy đáp án mong đợi làm kết quả đã chạy.
4. **Đối chiếu Cloud có giới hạn:** đọc E09 và xác minh/đọc ALASTOR; kiểm thêm prior art cùng task của G2. Không mặc định việc bỏ quyền truy cập host làm ý tưởng mới. Tách permanent omission, delayed arrival, ordering và alert delay.
5. **Thêm tri thức riêng khi đã có dữ liệu thật:** ghi nguồn, chủ sở hữu, ngày, phạm vi được sử dụng và điểm mâu thuẫn với paper. Chưa có nội dung thì đánh dấu thiếu đầu vào; không tự gán kinh nghiệm của người dùng.

## Khi nào mới xem xét tái tổ hợp?

Tiêu chí vận hành đề xuất, chưa được người dùng chốt:

- Một ca dương có bằng chứng đủ và một ca thiếu bằng chứng đều cho quyết định đúng trên nhóm giữ lại.
- Mọi kết luận quyết định có thể đi ngược từ tổng hợp → claim → đúng nguồn/phiên bản/vị trí; các giới hạn vẫn xuất hiện trong câu trả lời.
- Có ít nhất một lần sửa/bác bỏ nhận định do phản chứng và lưu nguyên lịch sử, thay vì chỉ cộng nguồn ủng hộ.
- Phân biệt được lỗi thiếu nguồn, thiếu trích xuất, truy xuất, suy luận và chấm đánh giá; không sửa RAG để che thiếu nguyên liệu.
- Chạy lặp ở các ca khác vẫn giữ được các thuộc tính trên. Một ca Q01 chưa chứng minh độ ổn định.

Khi đủ căn cứ, đưa **phần tri thức đã kiểm và lịch sử thay đổi** vào vault theo ID bền; tạo bản export/manifest mới có log delta, rồi kiểm lại. Nguồn chỉ đọc abstract, suy luận chưa kiểm và câu hỏi bị prior art trả lời vẫn giữ đúng trạng thái của chúng.
