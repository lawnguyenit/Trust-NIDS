# GraphFlow — kiểm câu trả lời có đủ bằng chứng không

**Lượt thử đã đi trọn từ truy xuất → trả lời có phạm vi → nhận diện phần thiếu → tìm bổ sung có giới hạn → cập nhật câu trả lời có lịch sử.** Có tiến triển cụ thể ở việc giữ và sử dụng tri thức đã đọc; chưa đủ để gọi một RAG/LLM riêng đã được đánh giá độc lập.

Ngày **08/11/2026**. Cùng AI tạo câu, gán nhãn, viết và tự rà câu trả lời. Các chủ đề đã biết từ lượt trước; đây là câu mới trên chủ đề quen, không phải kiểm mù. Ngữ cảnh hội thoại chưa được cô lập kỹ thuật; kỷ luật chỉ dùng packet được thể hiện bằng ID/đoạn trích và việc giữ câu thiếu bằng chứng, không phải bảo đảm mô hình không nhớ tri thức ngoài packet.

## Đã chạy những gì?

1. Chốt **12 câu hỏi mới**, rubric và mảnh bằng chứng cần có trước khi truy xuất. Protocol/hash được lưu; không sửa nhãn sau khi xem kết quả.
2. Dùng nguyên BM25 cũ, top 5. So 46 note P/K/D với cùng 46 note cộng **toàn bộ 26 claim** của hai pilot trước, đóng gói thành card có nguồn/phiên bản/vị trí/loại nhận định/giới hạn. Không chọn riêng card có lợi cho từng câu.
3. Lưu top-5 packet; viết **12 câu trả lời thực tế** từ packet augmented và policy context. Các ca thiếu không được tự lấp từ kiến thức đã biết.
4. Thử một lượt bổ sung cho đúng **hai ca còn thiếu**, dùng corpus cũ, một vòng và ngân sách truy vấn cố định. Lưu câu trả lời sau bổ sung riêng; không thay kết quả đầu.
5. Kiểm lineage, ID, đoạn trích, replay, corpus cũ; cố ý chèn lỗi để thấy bộ kiểm máy bắt được gì và bỏ sót gì.

## Kết quả truy xuất: đo sự hiện diện của bằng chứng đã gán nhãn

| Điều kiện | Hồ sơ đủ mọi mảnh tham chiếu trong top 5 |
|---|---:|
| 46 note nguồn/nhận định gốc | **3/10 câu** |
| Thêm 26 card từ các lượt đọc trước | **8/10 câu** |

N09 (số đo lab riêng) và N10 (khẳng định toàn thế giới chưa có lời giải) không nằm trong mẫu số này; chúng có yêu cầu từ chối kết luận không đủ bằng chứng. N11 được tính là có đủ record để **báo khác biệt phiên bản**, không là đã xác định số liệu đúng cuối cùng.

Đây là **reference-facet coverage**, không phải accuracy của câu trả lời hoặc bằng chứng khoa học chắc đúng. Nhãn do AI gán có thể chưa bao hết các cách hỗ trợ tương đương. Bộ câu cố ý kiểm các phần từng bị bỏ sót/khác phạm vi, không đại diện mọi câu người dùng sẽ hỏi.

Việc thêm card đồng thời thêm nội dung đã đọc, chia nhỏ đơn vị, đổi cách diễn đạt/ngôn ngữ và gắn metadata. Vì vậy kết quả không chứng minh riêng định dạng chuẩn hóa gây ra cải thiện. Nó cho thấy một cách giữ tri thức đã đọc có thể được sử dụng trong ca thử này.

## Những câu trả lời đã được kiểm

Xem [12 câu trả lời lượt đầu](ANSWERS.md) và dữ liệu chủ sở hữu [answers.json](answers.json).

| Nhóm | Cách xử lý thực tế |
|---|---|
| N01/N03/N04/N05/N06/N08/N12 | 7 câu trả lời có phạm vi, giữ điều kiện/đơn vị đo/trạng thái nguồn |
| N02 — KnowHow | Đúng paper được trả về nhưng thiếu đoạn đánh giá cần dùng; ghi **chưa đủ từ packet** |
| N07 — thiết kế rollout kết hợp evaluation | Có điều kiện quan sát nhưng thiếu mảnh hợp đồng đánh giá; chỉ trả lời **một phần** |
| N09 — tỷ lệ false positive của lab người dùng | Không bịa số hoặc dùng benchmark paper thay lab riêng |
| N10 — novelty của Q02 | Không suy global absence từ số bài, vẫn giữ giá trị câu hỏi |
| N11 — 5/7 hay 8/9 | Báo khác biệt manifestation, chưa chọn một số khi lịch sử nguồn chưa được đối chiếu |

Các trạng thái ở bảng là **tự rà của cùng AI**, chưa là kết quả chấm semantic độc lập. Có 22 mệnh đề được nối tới đoạn packet cụ thể; bộ kiểm chỉ xác minh đoạn đó tồn tại và được cung cấp cho câu tương ứng.

## Một lượt tìm bổ sung đã giải quyết được gì?

[repair_protocol.json](repair_protocol.json) được viết sau khi thấy ca thiếu, trước khi chạy lượt bổ sung. Cùng AI biết nhãn và corpus; đây là **adaptive repair có hướng dẫn**, không là query generator tự động đã được kiểm.

- **N02:** đổi cách diễn đạt câu về paper được nêu tên sang ngôn ngữ của bản trích; thu được A_L04. Sau đó mới trả lời phần thí nghiệm bỏ bước và giới hạn của phép thử.
- **N07:** tách yêu cầu thành điều kiện đánh giá và điều kiện đủ quan sát; thu được B_Q02C4 cùng B_Q05C4. Sau đó mới nối hai phần, giữ nhãn suy luận thiết kế.

Cả hai ca tìm lại được mảnh tham chiếu cần thiết trong **một vòng**. [Hai câu trả lời sau bổ sung](REPAIRED_ANSWERS.md) được lưu riêng. Kết quả đầu vẫn là **3/10 và 8/10**; không viết lại thành 10/10, không dùng sự phục hồi này để ước lượng generalization.

## Bộ kiểm citation đã bị thử ngược như thế nào?

Bốn lỗi cấu trúc được chèn có chủ đích: trích một ID chưa có trong packet; bịa đoạn trích; gắn nhãn đủ khi mới có một phần; âm thầm giải quyết conflict. Bộ kiểm từ chối cả bốn.

Một lỗi ngữ nghĩa khác cũng được chèn: giữ citation/đoạn K13 hợp lệ nhưng thay mệnh đề bằng câu nói ngược rằng CloudTrail ghi sẵn đầy đủ data events. **Bộ kiểm cấu trúc vẫn cho qua.** Cùng AI đọc đối chiếu thấy mệnh đề trái đoạn dẫn và loại về mặt ngữ nghĩa.

Các lỗi này là **control được dựng**, không phải hallucination quan sát từ một generator. Chúng cho thấy giới hạn cụ thể: **có ID và trích dẫn thật chưa bảo đảm diễn giải đúng**. Kết quả control được giữ trong [verification.json](verification.json), bao gồm lỗi mà bộ kiểm máy bỏ sót.

## Quyết định sau lượt này

Giữ ba phần đã có ích để thử tiếp: card có lineage/giới hạn; câu trả lời nêu rõ phần đủ/phần thiếu; một lượt tìm bổ sung có ngân sách và lưu lịch sử. Giữ thêm kiểm nghĩa ở cấp mệnh đề; chưa thay nó bằng kiểm substring/citation.

Chưa nhập 26 card vào schema hoặc thống kê chuẩn của vault, chưa đánh dấu người dùng duyệt, chưa công bố gap mới. Bước tiếp phù hợp là lấy một nhóm câu do người khác đặt hoặc một phiên generator được cô lập khỏi nhãn để kiểm lại support/sufficiency, rồi mới cân nhắc hợp nhất phần tri thức đã kiểm. Không cần bỏ nền cũ để làm bước đó.

## Hồ sơ và tái chạy

- [protocol.json](protocol.json), [baseline_snapshot.json](baseline_snapshot.json): câu/nhãn/rubric và input đã đóng băng.
- [cards.json](cards.json), [packets.json](packets.json), [retrieval_results.json](retrieval_results.json): bằng chứng dẫn xuất và kết quả lượt đầu.
- [repair_results.json](repair_results.json), [repair_answers.json](repair_answers.json): lượt bổ sung tách riêng.
- [PROJECT_STATE.md](PROJECT_STATE.md), [VERIFICATION.md](VERIFICATION.md), [verification.json](verification.json): trạng thái và kiểm chứng.

```powershell
python -B pilot_runs/2026-11-08_answer-sufficiency/run_probe.py
python -B pilot_runs/2026-11-08_answer-sufficiency/repair_probe.py
python -B pilot_runs/2026-11-08_answer-sufficiency/render_answers.py --check
python -B pilot_runs/2026-11-08_answer-sufficiency/review_run.py
```

Không có truy vấn web mới, model API, code paper hay lab ở lượt này: các kết luận chỉ dùng snapshot đã đọc trước. Corpus gốc chưa nằm trong Git; cần đúng snapshot được hash để tái chạy từ clone. Push chỉ chứa hồ sơ thử và không là deployment.
