# GraphFlow — tiếp tục thử Q02–Q05

**Đã hoàn tất bốn vòng đọc/đối chiếu có giới hạn. Cả bốn Q đều giúp tổ chức và phát triển tri thức; chưa Q nào được chọn làm đề tài hoặc chứng nhận tính mới.** Kết quả lần này làm rõ quan hệ giữa chúng và cho một điều chỉnh truy xuất nhỏ có tín hiệu trên tập phát triển.

Ngày **08/11/2026**. Vault và hồ sơ Q01 giữ nguyên. Các nhận định mới, phiên bản nguồn và lịch sử sửa cách hiểu nằm trong run này; chưa tái tổ hợp vào kho chuẩn. Người dùng chưa duyệt kết luận.

| Câu hỏi | Kết quả dùng được | Điều cần kiểm tiếp |
|---|---|---|
| [Q02 — Đánh giá thống nhất](Q02.md) | Kết luận hơn/kém phụ thuộc task, labels, benchmark và operating point; có khung dùng chung để tham khảo | Một hợp đồng đánh giá cụ thể cho dữ liệu/mục tiêu của mình |
| [Q03 — Giải thích → can thiệp](Q03.md) | Tách đổi dự đoán, thực thi hành động, tác hại an ninh và tác dụng lên dịch vụ | Ánh xạ cạnh→hành động và oracle độc lập trong lab xác định |
| [Q04 — Trợ lý có nguồn/biên tin cậy](Q04.md) | Tách grounding, nội dung bị thao túng, quyền gọi tool và utility | Tác vụ SOC với cặp dữ liệu sạch/đối kháng, chấm độc lập |
| [Q05 — Replica, rollout và tải lệch](Q05.md) | Bài gốc đã bàn rollout; cần xét peer group và phần bị bỏ khỏi giám sát | Kiểm artifact trước, rồi đo coverage cùng detection/false alerts |

## Vòng thử đã thực hiện

Mỗi Q có nguyên liệu gốc, câu trả lời có phạm vi, bốn claim kèm nguồn/vị trí/giới hạn, một đối chiếu có khả năng đổi cách hiểu, câu hỏi với tiền đề cần kiểm và câu trả lời thực tế, cùng phần chưa biết và bước tiếp. Các câu trả lời được tổng hợp thủ công từ lần đọc này; chưa có generator benchmark hay thí nghiệm detector/agent/Cloud.

Có **15 nguồn**, gồm **7 nguồn vốn có trong vault** được kiểm lại và **8 nguồn ngoài**; không coi mọi nguồn mới đều đã đọc toàn văn. Mức đọc của run: 10 nguồn đọc chọn phần, 5 nguồn ở mức abstract. Có **16 claim** và **7 quan hệ giữa Q**. Đây là hồ sơ pilot, không cộng thẳng vào thống kê nguồn/claim chuẩn của vault.

Ba thay đổi cách hiểu đáng chú ý:

- **Q02:** P09 có khác biệt giữa abstract trên trang tác giả và PDF liên kết (5/7 so với 8/9). Giữ từng manifestation; chưa sửa K03 hoặc gộp con số. P21 đã đọc sâu hơn bản metadata, nên có thể dùng quy trình của nó làm đối chiếu có điều kiện.
- **Q03:** tên metric “mitigation/recovery” cần đi cùng đối tượng và đơn vị đo; thay đổi detector hoặc chi phí hành động mô hình hóa chưa xác nhận hiệu quả vận hành.
- **Q04/Q05:** một lớp chặn tool-flow không bao phủ mọi sai lệch nội dung; một đề xuất xử lý rollout không mặc nhiên là bảo đảm bao phủ giám sát. Đọc Discussion/non-goals đã tạo ra tri thức hữu ích hơn việc chỉ đếm paper.

## Điều chỉnh cơ chế truy xuất đã thử

Giữ nguyên BM25 của Q01 và corpus **85 note**, dùng **8 truy vấn tiếng Việt tự nhiên do AI đặt**. Không nêu tên paper trong truy vấn và không đưa nguồn mới/case report vào corpus.

| Kiểm tra | Kết quả |
|---|---|
| Raw retrieval có ít nhất một note gán nhãn liên quan trong top 5 | 7/8 câu |
| Trong 7 câu có sẵn nhãn nguồn/claim P/K/D, raw tìm được nhãn đó trong top 5 | 4/7 câu |
| Cùng 7 câu đó, chỉ xếp hạng 46 note P/K/D | 6/7 câu |

Phép lọc theo loại note là **thử thích nghi sau khi xem kết quả raw**, dùng lại cùng truy vấn và nhãn, chưa có nhóm giữ lại/người chấm độc lập. Không so 7/8 của lần này với 6/6 của Q01 thành tốc độ cải thiện vì hai tập câu khác nhau.

T04B chỉ được gán Q04 trong protocol ban đầu, nên **không chấm evidence retrieval** cho nó. T05B vẫn tìm sai nguồn dù đã lọc loại note. Các ca được tìm đúng cũng có nhiều kết quả nhiễu; hit không đồng nghĩa đủ bằng chứng để trả lời. Cần giữ đường tìm Q/concept để điều hướng, còn đường lấy bằng chứng có thể xét bộ lọc riêng; chưa thay mặc định của vault hay triển khai RAG.

## Mạng tương hỗ sau lượt thử

Xem [bản đồ quan hệ và mức độ kiểm chứng](MECHANISM_REVIEW.md). Q02 là lớp kiểm phương pháp; Q05 có thể cung cấp điều kiện vận hành; Q01 quản lý khả năng quan sát/tái dựng; Q03 kiểm tác động; Q04 kiểm biên tin cậy của trợ lý. Đây là cách tổ chức nghiên cứu đề xuất, không phải một hệ thống tích hợp đã triển khai.

## Hồ sơ và tái chạy

- [sources.json](sources.json): chủ sở hữu metadata/phiên bản/mức đọc; [casebook.json](casebook.json): chủ sở hữu claim, câu trả lời và quan hệ. Q02–Q05 Markdown được sinh từ hai file này; sửa JSON rồi render lại.
- [SEARCH_LOG.md](SEARCH_LOG.md): truy vấn, tuyến nguồn, lỗi và điểm mù.
- [protocol.json](protocol.json), [retrieval_results.json](retrieval_results.json), [evidence_routing_results.json](evidence_routing_results.json).
- [PROJECT_STATE.md](PROJECT_STATE.md), [VERIFICATION.md](VERIFICATION.md), [verification.json](verification.json): ý định, AS-IS, kiểm chứng và giới hạn.

Từ thư mục `GraphFlow_Research`:

```powershell
python -B pilot_runs/2026-11-08_Q02-Q05/retrieval_probe.py
python -B pilot_runs/2026-11-08_Q02-Q05/evidence_routing_probe.py
python -B pilot_runs/2026-11-08_Q02-Q05/render_casebook.py --check
python -B pilot_runs/2026-11-08_Q02-Q05/verify_run.py
```

Hai probe dùng đúng vault và hồ sơ Q01 đã đóng băng; nếu input đổi thì mở run mới, không ghi lại `--freeze`. Vault gốc vẫn chưa được commit trong lượt này, nên clone chỉ có các pilot chưa đủ corpus để tái chạy; cần đúng các file được hash trong baseline. Không có deployment.
