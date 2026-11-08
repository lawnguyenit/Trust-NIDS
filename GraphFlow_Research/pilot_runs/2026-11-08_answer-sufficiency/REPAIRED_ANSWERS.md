# Hai câu trả lời sau một lượt tìm bổ sung

<!-- Generated from repair_answers.json, protocol.json and saved packets. -->

**Tác giả và người tự rà là cùng AI.** Đây là câu trả lời tổng hợp thủ công chỉ dùng packet kết hợp sau lượt tìm bổ sung có giới hạn. Không phải đầu ra của một generator riêng hoặc điểm semantic accuracy được chấm độc lập.

Đoạn trích dưới đây là từ **note/card dẫn xuất trong packet**, không được trình bày như trích nguyên văn paper. Metadata nguồn/phiên bản/vị trí và lineage nằm trong [cards.json](cards.json); packet kết hợp nằm trong [repair_results.json](repair_results.json).

[Tổng quan kết quả](README.md) · [Protocol đã đóng băng](protocol.json)

Đây là lượt adaptive repair có giới hạn, do cùng AI viết lại truy vấn sau khi biết ca thiếu. Không thay kết quả hoặc câu trả lời lượt đầu; không tính lại thành một điểm kiểm độc lập hoàn hảo. Xem [repair_protocol.json](repair_protocol.json).

## N02 — `scoped_supported_after_repair`

KnowHow đã thử bỏ bớt bước tấn công chưa, và việc đó có chứng minh khôi phục được record audit bị mất không?

**Trả lời:** Có. Bằng chứng vừa được tìm bổ sung ghi KnowHow đánh giá việc loại bớt bước tấn công theo các tỷ lệ bước còn lại và báo ảnh hưởng tới detection ở mức graph/node. Nhưng đó chưa phải bằng chứng khôi phục các sự kiện thực bị mất do cơ chế thu log; kết quả vẫn là tác giả báo cáo, chưa được tái lập ở đây.

**ID top-5 được cung cấp:** B_Q02C1, P11, B_Q03C2, B_Q05C3, B_Q05C4, A_L04, A_L08, A_L02.

### Nhận định và đoạn hỗ trợ

- `author_reported_in_extraction` — KnowHow có đánh giá loại bớt bước tấn công và báo ảnh hưởng tới graph/node detection.
  - **A_L04:** “KnowHow evaluates removal of attack steps at several retained-step ratios and reports graph/node detection effects.”
- `scope_limit` — Không đánh đồng thí nghiệm đó với dựng lại sự kiện thực bị mất dưới một cơ chế thu thập cụ thể hoặc với kết quả tái lập độc lập.
  - **A_L04:** “Detection on edited attack sequences is not equivalent to reconstructing true missing events under a real collection mechanism; no replication here.”

**Phần thiếu/giới hạn:** Chưa có phép tái lập hoặc thí nghiệm xác nhận riêng về phục hồi record bị mất.

**Bước bổ sung riêng:** Nếu chọn hướng thực nghiệm, định nghĩa cơ chế mất và oracle trước; không lấy phép bỏ bước làm thay cho mọi cơ chế missingness.

**Tự rà:** Câu trả lời này chỉ có sau khi packet sửa đã chứa A_L04; không thay câu trả lời thiếu bằng chứng của lượt đầu.

## N07 — `scoped_supported_after_repair`

Để so hai detector trong lúc rollout một cách công bằng, bản thiết kế cần ghi những điều kiện đánh giá và phần pod/thời gian đủ điều kiện giám sát nào?

**Trả lời:** Theo hai nhận định thiết kế đã tìm đủ, ghi chung task/đơn vị nhãn, dữ liệu, split, calibration, baseline và ngân sách; đồng thời ghi version group, readiness, traffic mix, phần pod/thời gian đủ điều kiện so sánh và phần thiếu bằng chứng. Đây là thiết kế tổng hợp để thử, chưa phải kết quả cho thấy một detector tốt hơn hoặc rollout chắc chắn làm mất giám sát.

**ID top-5 được cung cấp:** B_Q05C4, K10, K03, P14, P24, B_Q02C4, P10, K09, B_Q05C1.

### Nhận định và đoạn hỗ trợ

- `reviewer_inference_carried_forward` — Phần hợp đồng đánh giá đề xuất task/đơn vị nhãn, dữ liệu, split, calibration, baseline và ngân sách.
  - **B_Q02C4:** “task/đơn vị nhãn, dữ liệu, split, calibration, baseline và ngân sách.”
- `reviewer_inference_carried_forward` — Phần điều kiện giám sát đề xuất version group, readiness, traffic mix, pod/thời gian đủ điều kiện và phần không đủ bằng chứng.
  - **B_Q05C4:** “version group, readiness, traffic mix, phần thời gian/pod đủ điều kiện so sánh và phần không đủ bằng chứng”
- `scope_limit` — Các mục này là thiết kế do người đọc tổng hợp, chưa phải kết quả đo mới.
  - **B_Q02C4:** “Đây là thiết kế do người đọc tổng hợp; chưa có benchmark nội bộ hoặc kết quả hơn/kém mới.”

**Phần thiếu/giới hạn:** Chưa có dịch vụ, dữ liệu, oracle và kết quả lab cụ thể; hai mảnh được nối ở mức thiết kế.

**Bước bổ sung riêng:** Chọn một task và cấu hình đo được rồi điền hợp đồng trước khi chạy; giữ riêng các kết quả safety, utility và coverage.

**Tự rà:** Giữ cả hai mảnh và nhãn reviewer_inference; không nâng thành kết quả khoa học của riêng một paper.
