# Nhật ký tìm/đọc — Q02–Q05

Ngày **08/11/2026**, Asia/Saigon. Khảo sát định hướng có giới hạn để thử cơ chế; không là systematic review, không ước lượng recall hay bao phủ toàn thế giới.

## Trước khi tìm ngoài kho

Đọc nguyên Q02–Q05 và nearest-paper notes P01/P08/P09/P21, P10/P13/P14, P11/P15/P16/P17, P12/P18; đọc K01/K03/K04/K06/K08–K12/K15–K18 theo quan hệ. Mức đọc ghi trong các note chỉ là AS-IS của vault, không tự nâng thành đã đọc toàn văn hoặc người dùng duyệt.

Đóng băng vault, hồ sơ Q01 và protocol trước probe retrieval. Nguồn mới và các bản tổng hợp của run không đi vào corpus truy xuất.

## Các truy vấn web nguyên văn

| ID | Truy vấn | Mục đích |
|---|---|---|
| S01 | `"provenance" "intrusion detection" "evaluation" "Theseus"` | Q02: đọc sâu protocol liên quan |
| S02 | `"Cutting the Fuse" ProvX blocking evaluation model level` | Q03: định nghĩa tác động được đo |
| S03 | `SOC agents prompt injection evidence grounding benchmark security 2026` | Q04: nguồn đúng miền SOC |
| S04 | `"REPLICAWATCHER" "load" "version"` | Q05: assumption và thiết kế thực nghiệm |
| S05 | `"Sometimes Simpler is Better" Bilot pdf` | Q02: tìm bản tác giả khi publisher bị chặn |
| S06 | `"CaMeL" "Defeating Prompt Injections" paper` | Q04: đối chiếu control/data-flow defense |
| S07 | `microservice replica anomaly detection version skew load imbalance rolling update` | Q05: kiểm miền vận hành và từ khóa khác |
| S08 | `"What We Talk About When We Talk About Logs" dataset quality pdf` | Q02: backward snowball từ E02 reference 10 |
| S09 | `"REPLICAWATCHER" rolling updates load imbalance replica anomaly detection follow up` | Q05: kiểm tác giả đã xử lý gì |
| S10 | `"Large Language Models are Autonomous Cyber Defenders" service availability evaluation` | Q03: đối chiếu tác động dịch vụ và security |
| S11 | `"REPLICAWATCHER" "rolling updates" benchmark` | Q05: xác minh rollout được bàn ở đâu |
| S12 | `"PIDSMaker" "Building and Evaluating" 2026 arxiv` | Q02: tách framework mới khỏi bài phân tích 2025 |

Không lấy snippet hoặc các trang tổng hợp AI làm căn cứ kỹ thuật. Nguồn có ngày vượt ngày chốt, tài liệu không rõ phiên bản hoặc chủ đề không cần cho bốn ca không được nhận vào chuỗi claim. Không dùng các kết quả tin tức để suy cơ chế bảo mật.

## Tuyến nguồn và phần thực sự được dùng

| Nhóm | Tuyến và giới hạn |
|---|---|
| Q02 | P09 → author landing/PDF E01; P21 → arXiv v4 E02; E02 reference 10 → author-lab/IEEE abstract E03. Tìm riêng E04 PIDSMaker, chỉ đọc abstract/metadata, không chạy artifact. |
| Q03 | P10 → arXiv v2 E05 vì publisher 403; kiểm MER/Discussion. P14 → NDSS conference PDF E06, kiểm recovery-time units và scope. E06 reference về cyber defenders → E07 arXiv v2, kiểm reward/side effects/limitations. |
| Q04 | P16/P17 → proceedings E08/E09. E10 CaMeL arXiv v2 → control/data flows, explicit non-goals, design overview và scope discussion. E11 Watchtower v1 → threat model, method, results và limitations. Không so phần trăm giữa benchmark khác task. |
| Q05 | P12 → NDSS PDF E12, kiểm IV, VI.A/C và VIII.A/B. E13 Kubernetes/E14 Azure cung cấp lifecycle context. E15 được xác định đúng là thesis, chỉ đọc abstract/metadata và danh mục related outputs. |

P01/P08/P11/P13/P15/P18 được đọc ở mức note gốc để xác định vai trò. Không ghi nhận đã tái kiểm toàn văn chúng trong run này. E01–E15 có metadata, phiên bản và locators chính thức trong `sources.json`.

## Các khác biệt làm đổi cách hiểu

- **E01:** abstract trang tác giả nói 5/7, PDF liên kết nói 8/9. Đã xem nguyên trang đầu PDF; chưa xác định lịch sử phiên bản hoặc đối chiếu bytes với proceedings. Không âm thầm sửa K03.
- **E02:** validation-only selection không có nghĩa train và validation luôn theo lịch ngày đơn điệu; final test mới là phần cần giữ tách. Không đơn giản hóa quá quy trình tác giả.
- **E05/E06:** MER model-level và action-cost recovery là các đối tượng khác thực thi containment/downtime thật. Đã đọc định nghĩa, không suy từ tên metric.
- **E10/E11:** tool-flow authorization và misleading content cần đánh giá riêng. Watchtower không có tool execution; CaMeL có text-to-text non-goals. Không xem hai bài mâu thuẫn.
- **E12:** Discussion đã nêu rolling updates/readiness handling; chỉ đọc assumption sẽ bỏ sót phần đó. Chưa nhận đây là bảo đảm thực nghiệm với mọi tải lệch hoặc version skew.

## Lỗi truy cập/công cụ và cách xử lý

- Publisher USENIX trả 403 cho P09/P10. E01 dùng bản tác giả; E05 dùng arXiv v2, giữ rõ manifestation thay thế. Không giả nhận đã đọc proceedings đầy đủ.
- Connector click với URL tuyệt đối báo invalid arguments. Đọc HTML trang NDSS qua request read-only để lấy link PDF; phát hiện cả paper lẫn slides, chưa tải khi chưa phân biệt. Sau đó chọn đúng link `2026-f358-paper.pdf` đã quan sát được.
- `pdftotext` không có trong Poppler bundle. Dùng Python bundled `pypdf` để trích trang; một lượt stdout cp1252 lỗi Unicode, đã sửa xuất UTF-8. Không xem lỗi hiển thị là nguồn khoa học thất bại.
- Parser cảnh báo một số font Type1 thiếu hỗ trợ. Những trang quyết định được render bằng `pdftoppm` và xem ảnh: E01 trang 1, E06 trang 10, E12 trang 12. SHA-256 ba PDF nằm trong `sources.json`. Không commit PDF/ảnh/toàn văn.
- Adaptive retrieval diagnostic lần đầu lưu JSON thành công nhưng lỗi stdout Unicode sau khi lưu; đã thay bằng script có output ASCII, kiểm lại dữ liệu và tái chạy. Không lấy lần exit lỗi làm bằng chứng pass.

## Truy xuất trong kho: lần thử và lần chỉnh

Lần raw: 8 câu tiếng Việt và relevance labels được cố định trong `protocol.json` trước probe. Chạy đúng BM25 của Q01 trên 85 note; hit topic 7/8. T02B bỏ lỡ nhãn; T04A/T04B/T05B tìm được Q nhưng chưa tìm được source/claim được gán nhãn.

Sau khi thấy điều này, thử **một** thay đổi: hạn candidate về 46 note P/K/D. Không thay truy vấn hoặc thêm relevance labels. Trong 7 câu có nhãn P/K/D ban đầu, source/claim hit top-5 tăng 4→6; T05B vẫn miss. T04B bị loại khỏi phép đo này vì protocol chỉ có nhãn Q04; không lén thêm nhãn để tính điểm đẹp.

Đây là phép chẩn đoán trên development set, chưa có kiểm giữ lại. Cả hai điều kiện còn trả nhiều kết quả nhiễu; không coi hit là answer sufficiency hoặc giá trị của nguồn. Script không tạo câu trả lời, không gọi API model hay tool thực thi.

## Điểm mù và dừng lượt

- Chưa forward snowballing có hệ thống, chưa đọc mọi related work, chưa đủ căn cứ novelty.
- Chưa chạy code từ paper; license, dataset rights, tài nguyên và oracle chưa được xác minh cho việc tái lập.
- Lead Q05 WebNorm và các hướng single-instance/ConLock/ProCatch có xuất hiện qua tra cứu, chưa đọc full text/so task nên chưa dùng làm lời giải.
- Không có thêm tài liệu/kinh nghiệm riêng ngoài vault do người dùng cung cấp; phần ngoài ở đây là nguồn công khai đã mở.
- Dừng sau khi mỗi Q có scoped answer và một thay đổi cách hiểu có nguồn, để đánh giá cơ chế trước khi tái tổ hợp. Dừng không có nghĩa đã hoàn tất literature review cho từng miền.
