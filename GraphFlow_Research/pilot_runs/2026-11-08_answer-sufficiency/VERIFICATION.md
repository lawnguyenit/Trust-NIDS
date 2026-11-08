# Kiểm chứng lượt thử độ đủ bằng chứng

Ngày 08/11/2026. Môi trường Windows/PowerShell, Python standard library. Không cần model API hoặc network để tái chạy trên input đã có.

## Kiểm thực tế

- Freeze `protocol.json` và toàn bộ file của vault/hai pilot cũ trước probe. Lưu output và commit checkpoint `a8cf3bb` trước khi hoàn tất phần câu trả lời/tự rà.
- Hai điều kiện giữ cùng BM25/k=5 và câu hỏi. Toàn bộ 26 claim cũ được đóng gói nguyên statement/limitation/epistemic type/source version; không bổ sung từ vựng theo query.
- 12 câu trả lời đầu và 2 câu sau bổ sung có owner JSON riêng; Markdown được render từ dữ liệu đã lưu, không sinh câu trả lời mới khi chạy script.
- `review_run.py` kiểm hash/lineage, trích dẫn có trong đúng packet và excerpt là substring thật, trạng thái partial/conflict/abstention theo protocol, render consistency, local links và validator gốc. Replay probe/repair phải có output giống byte.
- Control có chủ đích ghi rõ một lỗi ngữ nghĩa vẫn qua bộ kiểm cơ học. Không xóa hoặc gọi đó là câu trả lời đúng vì validator pass.

Các lệnh chính nằm trong README; `verification.json` lưu argv, exit code, checks, counts và control results từ lần chạy thực. Các lần kiểm trong quá trình viết có thể báo thiếu README/link output chưa được tạo; chỉ báo pass sau khi file thật tồn tại và đã kiểm lại.

**Kiểm cấu trúc cuối: PASS.** Giữ nguyên 135 file vault, 12 file Q01 và 21 file Q02–Q05; 26 card đúng lineage; probe và repair tái chạy giống byte; 12 câu trả lời đầu có 22 mệnh đề nối excerpt, hai câu sửa có support trong packet mới; Markdown khớp owner JSON, link hợp lệ. Validator gốc 120 Markdown/117 identified notes/0 lỗi. Semantic control vẫn được ghi là máy bỏ sót; không có điểm semantic accuracy tự động.

## Giới hạn còn giữ nguyên

1. Cùng AI viết nhãn/câu/đáp án và tự rà; không có semantic accuracy độc lập.
2. Ngữ cảnh của AI không được cô lập khỏi lịch sử chủ đề; đã dùng citation/packet để hạn nội dung và giữ ca thiếu, nhưng chưa kiểm generator độc lập bằng context isolation.
3. Reference facets là nhãn của người thiết kế, không chứng minh đã liệt kê mọi bằng chứng tương đương.
4. Corpus augmented thêm cả nội dung lẫn representation; không tách được causal effect của riêng formatting/chunking/provenance.
5. Repair có hướng dẫn của cùng AI và biết nhãn; không là held-out score hay policy tự động đã chứng minh tốt.
6. Không kiểm lại live source hoặc paper results; source status, số liệu, scope vẫn gắn snapshot/mức đọc trước. Không có thí nghiệm vận hành, dữ liệu lab riêng hoặc novelty certification mới.
7. Người dùng chưa duyệt kết quả. Vault và hai pilot cũ được bảo toàn; cấu hình/canvas không được stage. Push không là backup đầy đủ vì corpus gốc vẫn untracked.

## Điểm học được đủ cụ thể để kiểm tiếp

- N02 là ví dụ corpus có claim cần thiết nhưng truy vấn tiếng Việt chưa thu hồi card tiếng Anh; một lookup theo paper/ngôn ngữ khắc phục trong ca này.
- N07 là ví dụ câu nhiều phần cần hơn một nguồn; facet đầy đủ giúp giữ câu trả lời partial trước khi có phần thứ hai.
- N11 cần version reconciliation ngoài retrieval; tìm được hai record không cho quyền chọn một con số.
- Control semantic cho thấy nguồn thật có thể bị diễn giải ngược; cần chấm quan hệ hỗ trợ từng mệnh đề, không chỉ ID/locator.
