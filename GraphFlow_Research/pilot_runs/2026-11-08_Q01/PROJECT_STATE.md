# Trạng thái ca thử Q01 — 08/11/2026

## Ý định và quyết định

- `requested`: chạy thử vòng tổng hợp → khoảng trống ứng viên → khảo sát lại → sửa nhận định; tối dần rồi mới tái tổ hợp kho.
- `requested`: dùng được tri thức có sẵn và nguồn ngoài; phân biệt thiếu tri thức với lỗi truy xuất/chưa chuẩn hóa RAG.
- `approved`: thử trước khi chuẩn hóa toàn kho, theo tin nhắn người dùng ngày 08/11/2026.
- `proposed_by_agent`: dùng Q01 làm ca đầu, tách hồ sơ thử khỏi vault gốc. Không suy thành người dùng chọn Q01 làm đề tài.
- `unknown`: nguồn lực thí nghiệm, môi trường Cloud, dữ liệu riêng và các tri thức ngoài chưa được cung cấp.

## AS-IS trước thử

- Vault gồm Markdown, JSON export và hai script Python; chưa thấy pipeline embedding, vector index, retriever hay generator được triển khai trong thư mục dự án này.
- Q01 là `candidate`, novelty `unverified`, có nearest papers nhưng chưa có đường dẫn rõ từ từng claim tới câu hỏi và chưa có hồ sơ tìm phản chứng riêng.
- P04 mới ở mức abstract; P11/P12/P22 ghi đọc chọn phần. Các mức đó là metadata của snapshot, không phải xác nhận đã được người dùng duyệt.
- Validator gốc chạy thành công: 120 Markdown, 117 identified notes, 0 lỗi. Kiểm cấu trúc không kiểm độ đúng khoa học.
- Git root là `D:/Project/Trust-NIDS`; toàn bộ `GraphFlow_Research` đang untracked trước ca thử. Không đưa nguyên vault hay cấu hình Obsidian vào commit của ca thử.

## Phạm vi tác động

| Thành phần | Chủ sở hữu / tác động |
|---|---|
| Vault và export gốc | Chỉ đọc; đóng băng hash để kiểm không bị sửa |
| Hồ sơ bằng chứng mới | Chỉ nằm trong thư mục ca thử; chưa cấp ID P/K/R chính thức |
| Truy xuất | Probe lexical ở cấp note, có đối chứng mở rộng từ vựng; không gọi là RAG đã hoạt động |
| Kết luận Q01 | Quyết định thử riêng; không tự đổi novelty của note gốc |
| UI/API/database/model | Không thay đổi, không huấn luyện hay chạy mã của paper |
| Git | Chỉ stage file do ca thử tạo; push milestone theo ủy quyền thường trực |

## Kiểm chứng và chấp nhận

- `verified_before`: validator vault thành công, đã đọc Q01, nguồn gần nhất và các claim liên quan.
- `implemented`: hồ sơ bằng chứng riêng `evidence.json` gồm 9 nguồn, 10 claim, 8 quan hệ và 3 cách diễn giải/câu hỏi; ghi rõ claim của tác giả và suy luận của người đọc.
- `verified`: probe BM25 trên 85 note/6 câu hỏi cho hit top-5 6/6 ở cả hai điều kiện; chưa có lợi ích top-5 từ glossary. Không suy thành kiểm chứng RAG/generator.
- `verified`: đọc lại nguồn chính; phát hiện phần đánh giá relevant chưa được trích vào P11, prior art mới E05/E06 và giới hạn truy cập nguồn E07. Mức đọc là chọn phần/abstract như từng E ghi, chưa phải full-text audit.
- `implemented`: quyết định giữ Q01 nhưng không nâng novelty, lưu G0/G1 bị overlap và G2 chưa xác minh. `README.md` và `SEARCH_LOG.md` trình bày đường dẫn bằng chứng/lịch sử.
- `verified_after`: validator gốc vẫn pass (120 Markdown, 117 identified notes, 0 lỗi); cả 135 file vault khớp hash nền; probe tái chạy cho output giống byte; JSON/reference/ID/link của pilot hợp lệ. Kết quả máy đọc được ở `verification.json`, phạm vi/giới hạn ở `VERIFICATION.md`.
- `not_accepted`: người dùng chưa xem kết quả ca thử; sự đồng ý chạy thử không phải chấp nhận kết luận.

## Điều kiện kết thúc ca thử

Một chuỗi suy luận có nguồn và giới hạn; ít nhất một đối chiếu có khả năng làm mất tính mới; quyết định giữ/sửa/bác bỏ câu hỏi; phân loại lỗi cơ chế và bước thử tiếp theo. Không đòi kết quả phải là một gap mới.

## Milestone Git

- `3f11dd1`: đóng băng protocol/vault hash, lưu code và kết quả lexical probe; đã push lên `origin/codex/graphflow-q01-pilot`.
- Checkpoint kết luận, log nguồn và xác minh cuối được commit tiếp sau đó; Git history là nơi tra hash chính xác để tránh ghi một commit tự tham chiếu.
- Chỉ file ca thử được stage. Vault gốc và cấu hình Obsidian vẫn untracked như trước; chưa đồng nghĩa toàn bộ kho đã được backup lên upstream. Không có deployment.
