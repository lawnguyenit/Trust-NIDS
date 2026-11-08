# Mười hai câu trả lời từ packet đã lưu

<!-- Generated from answers.json, protocol.json and saved packets. -->

**Tác giả và người tự rà là cùng AI.** Đây là câu trả lời tổng hợp thủ công chỉ dùng top-5 của điều kiện augmented và policy context cố định. Không phải đầu ra của một generator riêng hoặc điểm semantic accuracy được chấm độc lập.

Đoạn trích dưới đây là từ **note/card dẫn xuất trong packet**, không được trình bày như trích nguyên văn paper. Metadata nguồn/phiên bản/vị trí và lineage nằm trong [cards.json](cards.json); packet gốc nằm trong [packets.json](packets.json).

[Tổng quan kết quả](README.md) · [Protocol đã đóng băng](protocol.json)

## N01 — `scoped_supported`

Trong snapshot này, CloudTrail trail vừa tạo có ghi sẵn data events hay phải bật thêm?

**Trả lời:** Trong snapshot này, CloudTrail trails và event data stores không ghi data events mặc định; cần cấu hình ghi loại sự kiện đó. Điều này không có nghĩa CloudTrail không ghi gì.

**ID top-5 được cung cấp:** K13, D03, A_L01, A_L09, B_Q05C4.

### Nhận định và đoạn hỗ trợ

- `official_documentation_in_snapshot` — CloudTrail trails và event data stores không ghi data events mặc định; cần cấu hình thu thập loại này.
  - **K13:** “AWS CloudTrail trails và event data stores mặc định không ghi data events.”
  - **D03:** “cần cấu hình thu thập loại sự kiện này.”
- `scope_limit` — Không suy thành CloudTrail không ghi gì.
  - **K13:** “không nói CloudTrail không ghi gì.”

**Phần thiếu/giới hạn:** Không kiểm tra cấu hình của tài khoản thật hoặc độ mới của tài liệu ngoài snapshot.

**Bước bổ sung riêng:** Khi chuyển sang lab, đọc cấu hình trail/event selectors thực tế; không lấy default làm trạng thái tài khoản.

**Tự rà:** Các mệnh đề giữ đúng loại tài nguyên và giới hạn của K13; chưa phải kiểm độc lập tài liệu AWS.

## N02 — `insufficient_retrieval`

KnowHow đã thử bỏ bớt bước tấn công chưa, và việc đó có chứng minh khôi phục được record audit bị mất không?

**Trả lời:** Packet này chưa đủ để trả lời phần thí nghiệm bỏ bước hoặc khôi phục record. Note P11 được trả về mới ghi đã xem trang 1–2 và các mục mở đầu; tao không suy rằng toàn bài không có thí nghiệm chỉ vì note chưa chứa nó.

**ID top-5 được cung cấp:** B_Q02C1, P11, B_Q03C2, B_Q05C3, B_Q05C4.

### Nhận định và đoạn hỗ trợ

- `metadata_observation` — Note P11 trong packet ghi mức đọc giới hạn ở phần đầu và chưa đọc trọn bài.
  - **P11:** “PDF NDSS 2026: trang 1–2, abstract, I, II và chú thích về bản mở rộng; chưa đọc trọn 18 trang.”

**Phần thiếu/giới hạn:** Facet step_removal_evaluation_and_boundary không có trong top 5, dù bộ card có một bằng chứng đã gán nhãn cho nó.

**Bước bổ sung riêng:** Truy xuất lại theo danh tính nguồn/locator hoặc mở bằng chứng A_L04 ở bước bổ sung riêng; chưa đưa nội dung nhớ từ card đó vào câu trả lời hiện tại.

**Tự rà:** Đã giữ câu trả lời thiếu bằng chứng thay vì dùng kiến thức đã biết ngoài packet. Đây là miss của đường truy xuất, không là bằng chứng KnowHow thiếu thí nghiệm.

## N03 — `scoped_supported`

Kết quả báo động tốt có đủ cho thấy đã tìm lại được các process tấn công để điều tra không?

**Trả lời:** Chưa thể suy như vậy. Trong khung được trích, metric alerting được tách khỏi khả năng phục hồi process tấn công; cần xem đúng kết quả process-level cho mục tiêu điều tra. Nó cũng không tự đo thời gian analyst làm việc.

**ID top-5 được cung cấp:** B_Q02C1, B_Q03C1, K09, P22, P21.

### Nhận định và đoạn hỗ trợ

- `scoped_inference_from_author_report` — Khung được trích tách metric alerting khỏi phục hồi process tấn công, nên báo động tốt một mình chưa trả lời được mục tiêu điều tra.
  - **B_Q02C1:** “tách metric alerting khỏi phục hồi process tấn công.”
- `scope_limit` — Không lấy các metric này làm thời gian làm việc thực của analyst.
  - **B_Q02C1:** “không đo trực tiếp thời gian làm việc của analyst.”

**Phần thiếu/giới hạn:** Packet không có kết quả process-level của một detector triển khai trong SOC của người dùng.

**Bước bổ sung riêng:** Chọn task/process ground truth và báo riêng metric phục hồi, alert burden và thời gian người dùng nếu muốn đo nó.

**Tự rà:** Suy luận được ghi là suy luận có phạm vi, không biến metric thành bằng chứng hiệu quả người dùng.

## N04 — `scoped_supported`

Có thể lấy recovery time của bài lập kế hoạch làm số phút ứng dụng thật ngừng hoạt động không?

**Trả lời:** Không đổi trực tiếp sang phút downtime. Card của P14 ghi recovery time theo chi phí hành động rời rạc và mô phỏng; đánh giá vận hành vẫn là việc tiếp theo. Đơn vị hành động không tự là phút phục hồi ứng dụng thật.

**ID top-5 được cung cấp:** B_Q03C2, K10, P14, B_Q05C3, P17.

### Nhận định và đoạn hỗ trợ

- `author_reported_in_extraction` — P14 ở hồ sơ này dùng chi phí hành động rời rạc và mô phỏng; đánh giá vận hành chưa được trích như kết quả hoàn tất.
  - **B_Q03C2:** “P14 đánh giá recovery time bằng chi phí hành động rời rạc và thí nghiệm mô phỏng; đánh giá vận hành vẫn được nêu là việc tiếp theo.”
- `scope_limit` — Không chuyển đơn vị hành động thành phút phục hồi thật.
  - **B_Q03C2:** “không chuyển đơn vị hành động thành phút phục hồi thật.”

**Phần thiếu/giới hạn:** Chưa có ánh xạ chi phí thực thi hay số đo downtime cho ứng dụng cụ thể.

**Bước bổ sung riêng:** Nếu cần phút downtime, đo thời gian và service health trong một kịch bản vận hành xác định, lưu riêng khỏi metric mô hình.

**Tự rà:** Không phủ nhận testbed hoặc giá trị lập kế hoạch; chỉ chặn phép đổi đơn vị không có bằng chứng.

## N05 — `scoped_supported`

Nếu đã chặn mọi luồng gọi tool trái policy thì nội dung báo cáo văn bản có còn bị dẫn sai được không?

**Trả lời:** Có thể vẫn sai nội dung. Card CaMeL nêu rõ việc làm sai văn bản mà không dẫn tới flow bị cấm là non-goal. Vì vậy chặn tool-flow trái policy chưa đủ bảo đảm báo cáo đúng; điều này cũng không có nghĩa cơ chế chặn flow vô ích.

**ID top-5 được cung cấp:** B_Q04C2, K01, B_Q05C3, B_Q04C3, P24.

### Nhận định và đoạn hỗ trợ

- `author_reported_in_extraction` — Trong phạm vi CaMeL được trích, chỉnh sai nội dung text-to-text không dẫn tới flow bị cấm là non-goal.
  - **B_Q04C2:** “chỉnh sai nội dung text-to-text không dẫn tới flow bị cấm là non-goal được nêu rõ.”
- `scope_limit` — Giới hạn đó không phủ nhận giá trị biện pháp hoặc chứng nhận mọi prompt injection đã được giải.
  - **B_Q04C2:** “Không gọi biện pháp này vô ích hay khẳng định prompt injection đã giải hoàn toàn; gắn với arXiv v2 được đọc.”

**Phần thiếu/giới hạn:** Chưa có phép đo tính đúng của báo cáo hoặc policy cụ thể của trợ lý riêng.

**Bước bổ sung riêng:** Chấm độ đúng/support của nội dung tách khỏi quyền gọi tool; giữ phiên bản/threat model của nguồn.

**Tự rà:** Không biến non-goal của một phiên bản thành tuyên bố mọi hệ thống chắc chắn bị tấn công thành công.

## N06 — `scoped_supported`

Paper replica xử lý pod đang cập nhật như thế nào, và đề xuất đó có bảo đảm đo đủ trong lúc hai phiên bản cùng tồn tại chưa?

**Trả lời:** Theo card đã trích, REPLICAWATCHER bàn cách loại pod đang tạo/xóa bằng readiness probes khi rolling update. Nhưng đề xuất trong Discussion chưa tự thành phép đo đầy đủ cho mixed-version/load-skew hoặc bảo đảm luôn đủ peer để giám sát.

**ID top-5 được cung cấp:** B_Q05C1, K08, K18, P06, K17.

### Nhận định và đoạn hỗ trợ

- `author_reported_in_extraction` — Bài gốc có thảo luận loại pod đang tạo/xóa bằng readiness probes khi rolling update.
  - **B_Q05C1:** “thảo luận loại pod đang tạo/xóa bằng readiness probes khi rolling update.”
- `scope_limit` — Không xem riêng đề xuất đó là bảo đảm đầy đủ về mixed-version/load-skew hoặc đủ peer.
  - **B_Q05C1:** “Đề xuất trong Discussion không mặc nhiên là phép đo đầy đủ mixed-version/load-skew hoặc bảo đảm luôn có đủ peer.”

**Phần thiếu/giới hạn:** Chưa có kết quả đo coverage hoặc kiểm implementation readiness/version handling trong artifact.

**Bước bổ sung riêng:** Kiểm artifact và ghi eligible pod/time coverage cùng kết quả phát hiện trong một phép thử xác định.

**Tự rà:** Giữ đề xuất đúng tư cách đề xuất; không tuyên bố chắc chắn có blind spot hay detector thất bại.

## N07 — `partial`

Để so hai detector trong lúc rollout một cách công bằng, bản thiết kế cần ghi những điều kiện đánh giá và phần pod/thời gian đủ điều kiện giám sát nào?

**Trả lời:** Từ packet này, phần điều kiện vận hành có thể ghi là version group, readiness, traffic mix, phần pod/thời gian đủ điều kiện so sánh và phần không đủ bằng chứng. Đây là thiết kế do người đọc đề xuất. Packet chưa đủ để trình bày trọn hợp đồng đánh giá hai detector; còn thiếu mảnh về điều kiện đánh giá chung đã gán nhãn trước.

**ID top-5 được cung cấp:** B_Q05C4, K10, K03, P14, P24.

### Nhận định và đoạn hỗ trợ

- `reviewer_inference_carried_forward` — Phần thiết kế được trả về đề xuất ghi version group, readiness, traffic mix, eligibility theo pod/thời gian và phần thiếu bằng chứng.
  - **B_Q05C4:** “Phép thử hữu ích phải ghi version group, readiness, traffic mix, phần thời gian/pod đủ điều kiện so sánh và phần không đủ bằng chứng”
- `scope_limit` — Đây là thiết kế kiểm khả năng, chưa phải kết quả readiness gây blind spot hay baseline thất bại.
  - **B_Q05C4:** “Không tuyên bố readiness luôn gây blind spot hoặc baseline thất bại. Đây là thiết kế thử để kiểm các khả năng đó.”

**Phần thiếu/giới hạn:** Facet evaluation_contract không có trong top 5. Facet monitoring_eligibility có, nên chỉ trả lời phần tương ứng.

**Bước bổ sung riêng:** Lấy thêm bằng chứng B_Q02C4 qua lượt truy xuất bổ sung riêng rồi mới nối hai phần; không dùng trí nhớ để chốt bản thiết kế đầy đủ trong câu này.

**Tự rà:** Không gắn kết quả đủ một nửa thành câu trả lời đủ toàn bộ; giữ nhãn reviewer_inference của card.

## N08 — `scoped_supported`

Một trợ lý cứ từ chối hết mọi tác vụ có thể được xem là an toàn và hữu ích chỉ nhờ tỷ lệ tấn công thành công thấp không?

**Trả lời:** Không. Chỉ nhìn tỷ lệ tấn công thành công thấp có thể bỏ qua việc trợ lý không làm được nhiệm vụ hợp lệ. Cần đánh giá cả an toàn lẫn công dụng; đây là quy tắc đánh giá có nguồn trong kho, chưa là kết quả đo một trợ lý riêng.

**ID top-5 được cung cấp:** K11, P16, B_Q03C1, B_Q03C2, B_Q04C1.

### Nhận định và đoạn hỗ trợ

- `reviewer_inference_carried_forward` — Thất bại ở nhiệm vụ hợp lệ có thể trông an toàn, nên phải báo cả an toàn lẫn công dụng.
  - **K11:** “Agent thất bại ở nhiệm vụ hợp lệ có thể trông an toàn; cần báo cả hai mặt.”
- `scope_limit` — Quy tắc này không là một định lý bao quát mọi agent.
  - **K11:** “Đây là suy luận đánh giá; chưa là định lý bao quát agent.”

**Phần thiếu/giới hạn:** Chưa có tập tác vụ hợp lệ, input đối kháng và kết quả agent riêng để tính trade-off.

**Bước bổ sung riêng:** Lưu task completion cùng kết quả security trên cùng workflow, giữ oracle và mẫu đánh giá rõ.

**Tự rà:** Không đánh đồng tỷ lệ từ chối cao với an toàn/hữu ích; không đưa ra tỷ lệ nào chưa đo.

## N09 — `insufficient_no_local_experiment`

Trong lab của tao, rollout làm tăng false positive chính xác bao nhiêu phần trăm?

**Trả lời:** Tao chưa có bằng chứng trong gói này để báo một tỷ lệ false positive cho lab của mày. Không lấy số từ benchmark của paper thay cho lab riêng; cần dữ liệu hoặc kết quả đo của đúng cấu hình đó.

**ID top-5 được cung cấp:** P17, P18, P20, B_Q05C2, P14.

### Nhận định và đoạn hỗ trợ

- `abstention_policy` — Không thay số đo lab riêng bằng hiệu năng paper chưa được tái lập.
  - **POLICY_EVIDENCE:** “Số điểm/hiệu năng trong paper là tác giả báo cáo cho đến khi tái lập.”

**Phần thiếu/giới hạn:** Không có số đo đúng lab/cấu hình/nhãn của người dùng trong packet; không khẳng định người dùng chưa từng chạy thí nghiệm bên ngoài kho.

**Bước bổ sung riêng:** Nhận hoặc tạo dữ liệu có nhãn benign/attack và trạng thái rollout cho đúng lab trước khi tính tỷ lệ; việc chạy lab chưa nằm trong lượt kiểm tài liệu này.

**Tự rà:** Không đưa số tưởng tượng, không đồng nhất phạm vi kho với toàn bộ kinh nghiệm của người dùng.

## N10 — `insufficient_global_novelty`

Từ số bài đã đọc, mình đã đủ căn cứ tuyên bố thế giới chưa có lời giải cho Q02 chưa?

**Trả lời:** Chưa. Số bài trong kho không chứng minh toàn thế giới chưa có lời giải cho Q02. Mình có thể ghi phạm vi đã khảo sát và phần chưa biết; Q02 vẫn dùng được để học và thiết kế đánh giá.

**ID top-5 được cung cấp:** K18, P10, B_Q05C4, K12, P05.

### Nhận định và đoạn hỗ trợ

- `abstention_policy` — Không thấy lời giải trong tập đang có không cho phép viết chưa ai làm.
  - **POLICY_EVIDENCE:** “Không thấy một lời giải trong tập hiện có: viết “chưa thấy trong phạm vi đã tìm”, không viết “chưa ai làm”.”
- `abstention_policy` — Nhãn substantiated_in_scope cũng không bảo đảm toàn thế giới chưa ai làm.
  - **POLICY_GATE:** “Tên nhãn này vẫn không bảo đảm toàn thế giới chưa ai làm.”

**Phần thiếu/giới hạn:** Chưa có khảo sát đủ phạm vi cho một đóng góp cụ thể; global absence không thể suy từ số note.

**Bước bổ sung riêng:** Khi có ý tưởng đóng góp cụ thể mới lập hồ sơ prior art và phản chứng cho phạm vi đó; tiếp tục dùng Q02 như câu hỏi tổ chức tri thức.

**Tự rà:** Từ chối tuyên bố novelty, không từ chối hoặc loại bỏ chính câu hỏi Q02.

## N11 — `conflict`

Với bài Bilot, nên chốt kết quả mạng đơn giản là 5/7 hay 8/9 dataset để đưa vào review?

**Trả lời:** Chưa chốt một con số duy nhất. Hồ sơ ghi trang tác giả là 5/7 còn PDF được liên kết là 8/9; chưa xác định lịch sử sửa đổi và bản proceedings tương ứng. Trong review tạm, ghi khác biệt kèm từng phiên bản hoặc dùng kết luận định tính có giới hạn, rồi xác minh trước khi chốt số.

**ID top-5 được cung cấp:** K03, P09, B_Q04C2, P07, B_Q02C3.

### Nhận định và đoạn hỗ trợ

- `metadata_observation_in_extraction` — Hồ sơ đang ghi hai denominator khác nhau theo trang tác giả và PDF liên kết.
  - **B_Q02C3:** “Trang tác giả ghi năm trong bảy dataset, còn PDF được liên kết ghi tám trong chín.”
- `scope_limit` — Chưa đủ căn cứ âm thầm thay số cũ bằng số mới.
  - **B_Q02C3:** “Chưa xác định lịch sử sửa đổi hay bản proceedings byte-identical; không sửa số cũ thành số mới chỉ từ khác biệt này.”

**Phần thiếu/giới hạn:** Cần xác minh version history và bản được chọn để trích; khác biệt không tự chứng minh tác giả sai hoặc kết quả bị bác bỏ.

**Bước bổ sung riêng:** Đối chiếu bản proceedings/errata và artifact tương ứng trong một lượt kiểm nguồn riêng trước khi đưa con số cuối vào literature review.

**Tự rà:** Không chọn 8/9 vì mới nhìn thấy sau hoặc coi 5/7 là sai chỉ do hai manifestation khác nhau.

## N12 — `scoped_supported`

Theo hồ sơ ngày 08/11/2026, P21 đã là bài xuất bản NDSS 2027 được xác minh chính thức chưa?

**Trả lời:** Trong hồ sơ ngày 08/11/2026, P21 đang được ghi là preprint 2026, với acceptance NDSS 2027 do tác giả báo cáo; hồ sơ chưa có xác nhận venue chính thức. Vì vậy chưa nâng nó thành bài đã xuất bản năm 2027 được xác minh chính thức.

**ID top-5 được cung cấp:** P21, K16, P04, P19, P14.

### Nhận định và đoạn hỗ trợ

- `metadata_observation` — Kho tác giả ghi accepted NDSS 2027, còn bản công khai đang kiểm là preprint 2026.
  - **K16:** “Kho tác giả Theseus ghi accepted NDSS 2027; bản công khai đang kiểm là preprint 2026.”
- `scope_limit` — Hồ sơ này chưa ghi xác nhận venue chính thức.
  - **K16:** “Chưa có xác nhận venue chính thức trong lượt này.”

**Phần thiếu/giới hạn:** Không cập nhật trạng thái venue trực tiếp ở lượt này; câu trả lời chỉ áp dụng cho snapshot đã đóng băng.

**Bước bổ sung riêng:** Nếu cần trạng thái hiện hành để nộp review, kiểm danh sách hoặc proceedings chính thức rồi ghi một lần xác minh mới.

**Tự rà:** Giữ riêng acceptance, publication year và source verification; không biến venue tương lai thành năm xuất bản hiện tại.

