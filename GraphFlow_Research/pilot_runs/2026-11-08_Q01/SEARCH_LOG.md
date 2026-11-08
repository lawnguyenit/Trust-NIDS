# Nhật ký khảo sát ca thử

Ngày thực hiện/chốt phạm vi: **08/11/2026**, theo ngày làm việc Asia/Saigon. Đây là log của một ca thử có giới hạn, không phải systematic review. Không thống kê tổng hit, recall tìm kiếm hay PRISMA. Thứ tự kết quả có thể thay đổi khi chạy lại.

## Tuyến truy xuất trong kho

1. Đọc Q01 và bốn nguồn được nó chỉ tới: P04, P11, P12, P22.
2. Tìm các từ `missing`, `incomplete`, `thiếu`, `trễ`, `loss`, `delay`, `partial`, `Q01` trong Claims, Relations, Syntheses và Concepts.
3. Đọc K02/K05/K06/K07/K08/K13, C07/C09 và S03_TRANSFER. Tách nguồn sinh động cơ thực tiễn khỏi nguồn chứng minh khả năng kỹ thuật.
4. Đóng băng vault/protocol; chạy BM25 trên 85 note P/C/K/R/Q/D/S, không đưa hồ sơ pilot vào tập tìm kiếm. Script và kết quả lưu riêng.

## Tám truy vấn web đã thực hiện

| Thứ tự | Truy vấn nguyên văn | Vai trò |
|---|---|---|
| S01 | `provenance attack reconstruction incomplete missing audit logs robustness investigation` | Tìm theo vấn đề thay vì chỉ tên phương pháp |
| S02 | `provenance intrusion detection delayed out of order events Kairos missing logs` | Kiểm biến thể trễ/đảo thứ tự và nguồn gốc |
| S03 | `attack investigation incomplete provenance graph uncertainty missing logs` | Tìm đối chiếu cho khoảng trống giả định |
| S04 | `"Minding the Gap" "Improv" PRISM 2026` | Xác định đúng workshop/phiên bản |
| S05 | `provenance integrity checking dropped audit records Chan ProvMark` | Kiểm nhánh đánh giá chất lượng provenance |
| S06 | `attack reconstruction missing logs uncertainty abstention provenance partial observability` | Thử phản chứng cách thu hẹp sang suy luận và từ chối kết luận |
| S07 | `cloud attack investigation reconstruction incomplete CloudTrail logs missing telemetry uncertainty` | Kiểm điểm mù chuyển sang Cloud |
| S08 | `cloud forensic attack reconstruction missing audit logs serverless partial observability` | Tìm đầu mối ngoài host provenance |

S01–S03 dẫn đến **Minding the Gap**; S06 dẫn đến **HunterAgent**; S07–S08 tạo thêm đầu mối Cloud. Đây là tuyến phát hiện quan sát được, không khẳng định truy vấn nào thu hồi đầy đủ công trình liên quan.

## Mở nguồn và sàng lọc

Chỉ dùng nguồn chính cho nhận định được nhận vào `evidence.json`.

| ID | Hành động và mức sử dụng |
|---|---|
| E01 | Mở tài liệu AWS; kiểm lại phần mặc định và ví dụ data events. |
| E02 | Mở trang NDSS và PDF hội nghị; kiểm II, V.B, VI.B, VI.F. Đọc và render nguyên trang 14 để kiểm Table XI trong ngữ cảnh. Không trộn bản arXiv mở rộng. |
| E03 | Mở HTML nhà xuất bản; kiểm threat model, preprocessing và Discussion, đặc biệt POI reporting delay. |
| E04 | Mở trang tác giả và PDF; kiểm threat model và phần chronological ingestion. Không đọc/kiểm toàn văn. |
| E05 | Mở trang NDSS rồi PDF; kiểm trang đầu để xác định đây là PRISM 2026, không phải main track NDSS. Đọc chọn phần về recovery, ordering, evaluation/trust và references. |
| E06 | Mở arXiv abstract và HTML **v1**; kiểm III.B–D, IV.A.1, IV.F/Table V và Limitations. Chỉ chấp nhận dưới nhãn tác giả báo cáo ở preprint. Không lấy headline performance làm căn cứ chọn phương pháp. |
| E07 | Backward snowballing từ reference 43 của E05; kiểm abstract/metadata chính thức USENIX. PDF bị 403 ở lần truy cập tiếp theo; không dùng kết luận chi tiết từ PDF. |
| E08 | Mở trang NDSS và PDF; kiểm IV trang 4 về điều kiện replica. Giữ vai trò đối chứng phạm vi, không coi là nearest work cho tái dựng thiếu log. |
| E09 | Mở trang NIST có tác giả, metadata và abstract. Chưa đọc full text; chỉ dùng để chỉ ra Cloud/multi-source reconstruction cần được khảo sát tiếp. |

E05 reference 40–44 còn chỉ tới broken provenance, expressiveness benchmarking và discrepancy detection. Chưa mở nguồn chính cho tất cả các mục đó; không biến lời related work của E05 thành nhận định đã kiểm độc lập về những bài ấy.

## Đầu mối chưa xử lý hết

- [ALASTOR: Reconstructing the Provenance of Serverless Intrusions](https://people.cs.umass.edu/~pdatta/publication/alastor/alastor.pdf): tìm được qua S08; **chưa đọc nội dung**, chưa dùng làm căn cứ kỹ thuật. Cần xác minh phiên bản/venue rồi đối chiếu trước khi gọi G2 là mới.
- Cloud evidence lifecycle framework và CURE xuất hiện qua tìm kiếm; chưa sàng lọc full text, không nhận vào chuỗi kết luận.
- Chưa làm forward citation search có hệ thống; chưa khảo sát đủ probabilistic reconstruction, CEP/stream processing, threat hunting, Cloud control-plane investigation và sản phẩm thương mại.
- Chưa có tri thức riêng ngoài vault do người dùng cung cấp trong lượt này. Các nguồn ngoài ở đây là tài liệu công khai đã tìm và mở.

## Lỗi truy cập và cách xử lý

- Một lượt dùng reference ID tạm của công cụ trả về **tên/URL không đúng tài liệu đích**. Không nhận các kết quả đó làm bằng chứng; mở lại bằng URL tuyệt đối và kiểm tiêu đề, phiên bản, mục đọc. Bài học cơ chế: locator tạm của công cụ không thay cho danh tính nguồn.
- Screenshot PDF qua connector báo không hỗ trợ. Đã tải hai PDF chính thức E02/E05 vào thư mục temp, render bằng Poppler và xem ảnh trang 14/trang 1. SHA-256 của PDF nằm trong `evidence.json`; không commit toàn văn hoặc ảnh trang báo.
- Không tải/chạy artifact nghiên cứu, không gọi API mô hình trả phí, không triển khai lab và không truy cập tài nguyên Cloud.

## Điều kiện dừng lượt này

Đã có đối chiếu trực tiếp đủ để chặn bước nâng câu hỏi rộng thành gap mới; đã kiểm thêm biến thể suy luận có kiểm chứng/dừng khi thiếu bằng chứng và thấy overlap. Kết thúc ở quyết định **giữ câu hỏi, chưa chứng minh novelty**, để đánh giá cơ chế. Điểm dừng này không thay cho hoàn tất khảo sát chuyên ngành.
