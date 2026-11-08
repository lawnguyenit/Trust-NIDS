# Ca thử GraphFlow 01 — từ Q01 đến kiểm chứng lại khoảng trống

**Vòng thử đã chạy được bằng thao tác có ghi vết, và đã chặn một suy luận quá rộng về tính mới. Chưa đủ để gọi cơ chế ổn định hoặc RAG đã được kiểm chứng.** Q01 vẫn là câu hỏi tổ chức tri thức hữu ích; chưa được nâng thành khoảng trống nghiên cứu đã xác nhận.

Ngày: **08/11/2026**. Người thực hiện: AI; người dùng chưa duyệt kết quả. Đây là thử cơ chế nghiên cứu trên tài liệu, chưa là thí nghiệm detector hay đánh giá triển khai Cloud. Vault gốc được giữ nguyên.

## Đọc hồ sơ

- [Trạng thái, ý định và phạm vi](PROJECT_STATE.md).
- [Bằng chứng, quan hệ và lịch sử quyết định ở dạng JSON](evidence.json): nguồn chuẩn cho ID E/L/PR/G của ca thử, không nhập vào export chính.
- [Truy vấn, nguồn đã mở, lỗi và điểm mù](SEARCH_LOG.md).
- [Protocol đóng băng](protocol.json), [kết quả truy xuất](retrieval_results.json), [hash nền](baseline_snapshot.json).
- [Kế hoạch lượt tiếp theo](NEXT_ITERATION.md).

## 1. Tri thức cũ đã đóng vai trò gì?

| Nguyên liệu trong vault | Có thể dùng để làm gì? | Không suy ra được gì? |
|---|---|---|
| K13 → D03 → L01 | Nêu tình huống cụ thể về data events chưa được thu mặc định | Không chứng minh mọi Cloud đều thiếu log hoặc chưa có giải pháp |
| K05 → P22 → L02 | Biết đã có dựng lại đường/giai đoạn với POI | Không suy ra chất lượng khi mất sự kiện |
| K07 → P11 → L03 | Ghi đúng biên tin cậy kernel/audit | Không suy ra log đầy đủ, cũng không suy ra hệ thống đã thất bại |
| C09 và SYS_GATE | Đòi đầu vào, baseline, ground truth và điều kiện bác bỏ | Không tự cung cấp bằng chứng thực nghiệm |
| K08 → P12 → L10 | Nhắc kiểm ràng buộc triển khai replica | Không phải bằng chứng trực tiếp cho Q01 |

**Suy luận hợp lệ ban đầu:** có lý do hỏi khả năng tái dựng thay đổi thế nào khi nguồn quan sát thay đổi. **Bước chưa được phép:** biến câu hỏi ấy thành “chưa ai làm”.

## 2. Chuyển câu hỏi thành đối tượng khảo sát

Q01 được tách thành các thuộc tính để tìm công trình cùng vấn đề: loại sự kiện thiếu; thiếu context hay mất hẳn record; trễ alert hay trễ ingestion; khả năng truy vấn trạng thái host; bằng chứng còn sống; nhiệm vụ phát hiện hay điều tra; đầu ra là bằng chứng quan sát hay suy luận.

Thử tiếp bằng nguồn ngoài và đọc sâu nguồn cũ cho ba thay đổi cụ thể:

1. **Nguồn đã có nhưng trích xuất chưa đủ:** P11/KnowHow có thí nghiệm loại bớt bước tấn công tại VI.F, trang 14, Table XI. Note cũ chỉ ghi phần đầu và threat model. Thí nghiệm này đo detection trên chuỗi đã chỉnh sửa; chưa được đánh đồng với mất log tự nhiên hoặc phục hồi sự kiện thực. Xem E02/L04.
2. **Nguồn chưa có trong kho:** [Minding the Gap / Improv](https://www.ndss-symposium.org/ndss-paper/auto-draft-661/) xử lý thiếu context và ordering bằng trạng thái kernel đang sống. Đây là paper **workshop PRISM 2026**; phạm vi đó khác khôi phục lịch sử bất kỳ sau khi trạng thái đã mất. Xem E05/L05.
3. **Cách thu hẹp cũng cần phản chứng:** [HunterAgent v1](https://arxiv.org/html/2605.29269v1) đã bàn về trace thiếu log, grounding, phân biệt inferred leads và dừng khi thiếu bằng chứng. Nó là **preprint**, với giả định còn telemetry độc lập; chưa tái lập trong ca này. Xem E06/L06.

Điểm phân biệt bổ sung từ MotifTrace: trễ báo POI khi vẫn giữ lịch sử audit khác với sự kiện đến trễ, sai thứ tự hoặc mất vĩnh viễn. Không gom các trường hợp này thành một biến “delay”. Xem E03/L07.

## 3. Quyết định sau vòng phản chứng

| Đối tượng | Kết quả | Hành động |
|---|---|---|
| G0: tái dựng dưới thiếu/trễ provenance là vùng trắng | Bác cách suy novelty quá rộng | Giữ Q01 làm câu hỏi; thêm prior art và ranh giới |
| G1: thêm grounding và dừng khi thiếu bằng chứng tạo nét mới | Có overlap trực tiếp với E06 | Không đổi tên ý tưởng rồi coi là gap mới |
| G2: so sánh trong điều kiện Cloud xác định, không có live host state | Chưa xác minh | Khảo sát tiếp E09/ALASTOR và các miền lân cận trước khi chọn thí nghiệm |

G0/G1 là cách diễn giải chẩn đoán của AI trong ca thử, **không phải phát biểu đã được người dùng hay Q01 gốc khẳng định**. G2 là câu hỏi tiếp theo, chưa là đề tài được chọn. Không đổi `novelty_status` của vault gốc.

## 4. Kiểm nghi vấn truy xuất/RAG

Đã chạy cùng một BM25 trên **85 note** gốc, với **6 câu hỏi phát triển**, so truy vấn tiếng Anh nguyên bản với truy vấn thêm từ vựng song ngữ. Đóng băng protocol và hash vault trước lần probe đầu; pilot và nguồn mới không vào tập truy xuất.

| Phép đo | Truy vấn gốc | Thêm từ vựng |
|---|---:|---:|
| Câu có ít nhất một note gán nhãn liên quan trong top 5 | 6/6 | 6/6 |
| Top 1 là note được gán nhãn liên quan, xem thêm sau chạy | 5/6 | 4/6 |

Ví dụ T01: thêm từ vựng đẩy C07 lên đầu, trong khi bằng chứng trực tiếp D03/K13 nằm sau. T03 xếp K08/P12 tốt hơn nhưng top 1 vẫn là Q05. Vì vậy chưa có lợi ích top-5 trong bộ này và không có lý do thay mặc định bằng mở rộng truy vấn mù.

**Giới hạn:** cùng AI đặt câu hỏi, glossary và nhãn; không có tập giữ lại hoặc người chấm độc lập. Đây là tìm note bằng từ khóa, chưa có embedding/chunking/generator/reranker. T05 tìm đúng Q01 vẫn không có nghĩa Q01 đủ bằng chứng để trả lời. Không dùng 6/6 để tuyên bố chất lượng RAG.

Hai câu kiểm câu trả lời được xử lý **thủ công**: A01 không có kết quả thí nghiệm Kubernetes để báo; A02 không đủ căn cứ nói chưa ai giải Q01. Đây là quyết định đọc bằng chứng, chưa phải bài kiểm một generator tự động.

## 5. Cơ chế đã học được gì và sửa ở đâu?

| Loại vấn đề | Bằng chứng trong ca này | Điều chỉnh được ghi trong hồ sơ pilot |
|---|---|---|
| Thiếu độ sâu trích xuất | Thí nghiệm relevant ở P11 chưa vào note | Lưu source version + section + điều đo thật + giới hạn |
| Thiếu độ bao phủ nguồn | E05/E06 chưa có trong kho | Gap phải có lượt tìm theo vấn đề và tìm lời giải đã có |
| Lẫn ý nghĩa bài toán | Missing context/record, ordering, POI delay khác nhau | Chốt observation mechanism và task trước so sánh |
| Tìm thấy chưa đồng nghĩa trả lời được | T05 tìm Q01 nhưng Q01 còn unknowns | Tách relevance khỏi answer sufficiency |
| Không có truy vết quyết định | Q01 thiếu chuỗi claim → gap → phản chứng | Có L01–L10, PR01–PR08, G0–G2 và lý do giữ/sửa |
| Định danh nguồn yếu | Một lượt locator tạm trả nhầm tài liệu | Dùng URL + tiêu đề + phiên bản; loại kết quả sai trước trích xuất |

Chưa có bằng chứng ca này thất bại vì lexical retrieval; cũng chưa loại trừ lỗi truy xuất trên câu hỏi khác. Phần đã cải thiện nằm trong hồ sơ thử, chưa áp thành schema hay sửa cả kho.

## 6. Tái chạy và kiểm toàn vẹn

Từ thư mục `GraphFlow_Research`:

```powershell
python pilot_runs/2026-11-08_Q01/retrieval_probe.py
python GraphFlow_Research_Vault/13_Tools/validate_vault.py GraphFlow_Research_Vault
```

Script đầu từ chối chạy nếu vault hoặc protocol khác baseline; không chạy lại `--freeze` để che thay đổi. Nếu nội dung Obsidian thật sự đổi, mở run mới. Baseline vault chưa được đưa vào Git trong ca này, nên bản clone chỉ chứa hồ sơ pilot chưa đủ tái chạy nếu không có đúng snapshot vault; `baseline_snapshot.json` xác định phiên bản cần có.

Validator gốc chỉ kiểm vault, không kiểm schema của pilot; JSON pilot và liên kết/ID được kiểm riêng. Các lệnh, kết quả và giới hạn cuối cùng nằm trong [VERIFICATION.md](VERIFICATION.md). Chưa có sự chấp nhận của người dùng hay chứng nhận tính mới khoa học.
