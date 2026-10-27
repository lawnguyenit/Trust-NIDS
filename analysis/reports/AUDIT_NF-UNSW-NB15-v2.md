# Trust-NIDS Data Audit Report: `NF-UNSW-NB15-v2`

> **Tự động sinh bởi DuckDB OLAP Engine vào lúc 2026-10-27 18:20:19**

## 1. Chỉ số Tổng quan (High-Level KPIs)

- **Tổng số flows**: `2,390,275`
- **Lưu lượng sạch (Benign)**: `2,295,222` (96.02%)
- **Lưu lượng tấn công (Attack)**: `95,053` (3.98%)
- **Tổng số IP Nguồn duy nhất**: `40`
- **Tổng số IP Đích duy nhất**: `40`
- **Thời lượng flow trung bình**: `259111.7 ms`
- **Bytes vào / ra trung bình**: `4621.7 B / 35265.7 B`

## 2. Phân bố các Loại Tấn công (Attack Behavior Matrix)

| Attack         |   count |   pct |   avg_in_bytes |   avg_out_bytes |   avg_in_pkts |   avg_out_pkts |   avg_dur_ms |
|:---------------|--------:|------:|---------------:|----------------:|--------------:|---------------:|-------------:|
| Benign         | 2295222 | 96.02 |         4159.1 |         36203.6 |          36.7 |           46.9 |       251113 |
| Exploits       |   31551 |  1.32 |        34233.2 |         21891.3 |          38.4 |           29   |       697651 |
| Fuzzers        |   22310 |  0.93 |         6722.3 |           502.2 |          12.5 |            5.9 |       437578 |
| Generic        |   16560 |  0.69 |         1783.5 |         12459.7 |           6.5 |           10.9 |       178956 |
| Reconnaissance |   12779 |  0.53 |          530.3 |           231.4 |           6.5 |            3.9 |       302820 |
| DoS            |    5794 |  0.24 |        39717.6 |         47395.6 |          47.1 |           47.2 |       513701 |
| Analysis       |    2299 |  0.1  |          621.6 |           215.3 |           4.8 |            1.6 |       216706 |
| Backdoor       |    2169 |  0.09 |          926.8 |           272.3 |           6   |            1.3 |       257416 |
| Shellcode      |    1427 |  0.06 |          524.6 |           139.6 |           6   |            3.3 |       159518 |
| Worms          |     164 |  0.01 |         2256.1 |         74949.8 |          17.9 |           61.4 |       733284 |

## 3. Top Talkers (10 IP Nguồn Chiếm Lưu Lượng Lớn Nhất)

| IPV4_SRC_ADDR   |   flows |   pct |   attacks |   benign |   distinct_targets |
|:----------------|--------:|------:|----------:|---------:|-------------------:|
| 59.166.0.1      |  230357 |  9.64 |         0 |   230357 |                 10 |
| 59.166.0.2      |  230214 |  9.63 |         0 |   230214 |                 10 |
| 59.166.0.4      |  230209 |  9.63 |         0 |   230209 |                 10 |
| 59.166.0.0      |  230068 |  9.63 |         0 |   230068 |                 10 |
| 59.166.0.3      |  228573 |  9.56 |         0 |   228573 |                 10 |
| 59.166.0.5      |  228093 |  9.54 |         0 |   228093 |                 10 |
| 59.166.0.9      |  221404 |  9.26 |         0 |   221404 |                 10 |
| 59.166.0.8      |  220524 |  9.23 |         0 |   220524 |                 10 |
| 59.166.0.6      |  219536 |  9.18 |         0 |   219536 |                 10 |
| 59.166.0.7      |  219433 |  9.18 |         0 |   219433 |                 10 |

## 4. Phân bố Giao thức Mạng (Protocols)

| protocol_name   |   flows |   pct |   attacks |
|:----------------|--------:|------:|----------:|
| TCP (6)         | 1830978 | 76.6  |     58254 |
| UDP (17)        |  544501 | 22.78 |     22977 |
| ICMP (1)        |    1556 |  0.07 |      1209 |
| Proto-89        |    1358 |  0.06 |       811 |
| Proto-2         |     104 |  0    |       102 |
| Proto-47        |      88 |  0    |        88 |
| Proto-41        |      85 |  0    |        85 |
| Proto-103       |      81 |  0    |        81 |
| Proto-77        |      81 |  0    |        81 |
| Proto-55        |      81 |  0    |        81 |
| Proto-53        |      81 |  0    |        81 |
| Proto-33        |      81 |  0    |        81 |
| Proto-132       |      78 |  0    |         0 |
| Proto-0         |      46 |  0    |        46 |
| Proto-3         |      46 |  0    |        46 |
| Proto-9         |      46 |  0    |        46 |
| Proto-10        |      46 |  0    |        46 |
| Proto-11        |      46 |  0    |        46 |
| Proto-12        |      46 |  0    |        46 |
| Proto-13        |      46 |  0    |        46 |
| Proto-14        |      46 |  0    |        46 |
| Proto-15        |      46 |  0    |        46 |
| Proto-16        |      46 |  0    |        46 |
| Proto-18        |      46 |  0    |        46 |
| Proto-19        |      46 |  0    |        46 |
| Proto-20        |      46 |  0    |        46 |
| Proto-21        |      46 |  0    |        46 |
| Proto-22        |      46 |  0    |        46 |
| Proto-23        |      46 |  0    |        46 |
| Proto-24        |      46 |  0    |        46 |
| Proto-25        |      46 |  0    |        46 |
| Proto-26        |      46 |  0    |        46 |
| Proto-27        |      46 |  0    |        46 |
| Proto-28        |      46 |  0    |        46 |
| Proto-29        |      46 |  0    |        46 |
| Proto-30        |      46 |  0    |        46 |
| Proto-31        |      46 |  0    |        46 |
| Proto-32        |      46 |  0    |        46 |
| Proto-34        |      46 |  0    |        46 |
| Proto-35        |      46 |  0    |        46 |
| Proto-36        |      46 |  0    |        46 |
| Proto-37        |      46 |  0    |        46 |
| Proto-38        |      46 |  0    |        46 |
| Proto-8         |      46 |  0    |        46 |
| Proto-40        |      46 |  0    |        46 |
| Proto-42        |      46 |  0    |        46 |
| Proto-43        |      46 |  0    |        46 |
| Proto-44        |      46 |  0    |        46 |
| Proto-45        |      46 |  0    |        46 |
| Proto-46        |      46 |  0    |        46 |
| Proto-48        |      46 |  0    |        46 |
| Proto-49        |      46 |  0    |        46 |
| Proto-50        |      46 |  0    |        46 |
| Proto-51        |      46 |  0    |        46 |
| Proto-52        |      46 |  0    |        46 |
| Proto-4         |      46 |  0    |        46 |
| Proto-54        |      46 |  0    |        46 |
| Proto-7         |      46 |  0    |        46 |
| Proto-56        |      46 |  0    |        46 |
| Proto-57        |      46 |  0    |        46 |
| Proto-59        |      46 |  0    |        46 |
| Proto-60        |      46 |  0    |        46 |
| Proto-61        |      46 |  0    |        46 |
| Proto-62        |      46 |  0    |        46 |
| Proto-63        |      46 |  0    |        46 |
| Proto-64        |      46 |  0    |        46 |
| Proto-65        |      46 |  0    |        46 |
| Proto-66        |      46 |  0    |        46 |
| Proto-67        |      46 |  0    |        46 |
| Proto-68        |      46 |  0    |        46 |
| Proto-69        |      46 |  0    |        46 |
| Proto-70        |      46 |  0    |        46 |
| Proto-71        |      46 |  0    |        46 |
| Proto-72        |      46 |  0    |        46 |
| Proto-73        |      46 |  0    |        46 |
| Proto-74        |      46 |  0    |        46 |
| Proto-75        |      46 |  0    |        46 |
| Proto-76        |      46 |  0    |        46 |
| Proto-5         |      46 |  0    |        46 |
| Proto-78        |      46 |  0    |        46 |
| Proto-79        |      46 |  0    |        46 |
| Proto-80        |      46 |  0    |        46 |
| Proto-81        |      46 |  0    |        46 |
| Proto-82        |      46 |  0    |        46 |
| Proto-83        |      46 |  0    |        46 |
| Proto-84        |      46 |  0    |        46 |
| Proto-85        |      46 |  0    |        46 |
| Proto-86        |      46 |  0    |        46 |
| Proto-87        |      46 |  0    |        46 |
| Proto-88        |      46 |  0    |        46 |
| Proto-90        |      46 |  0    |        46 |
| Proto-91        |      46 |  0    |        46 |
| Proto-92        |      46 |  0    |        46 |
| Proto-93        |      46 |  0    |        46 |
| Proto-94        |      46 |  0    |        46 |
| Proto-95        |      46 |  0    |        46 |
| Proto-96        |      46 |  0    |        46 |
| Proto-97        |      46 |  0    |        46 |
| Proto-98        |      46 |  0    |        46 |
| Proto-99        |      46 |  0    |        46 |
| Proto-100       |      46 |  0    |        46 |
| Proto-101       |      46 |  0    |        46 |
| Proto-102       |      46 |  0    |        46 |
| Proto-131       |      46 |  0    |        46 |
| Proto-104       |      46 |  0    |        46 |
| Proto-105       |      46 |  0    |        46 |
| Proto-106       |      46 |  0    |        46 |
| Proto-107       |      46 |  0    |        46 |
| Proto-108       |      46 |  0    |        46 |
| Proto-109       |      46 |  0    |        46 |
| Proto-110       |      46 |  0    |        46 |
| Proto-111       |      46 |  0    |        46 |
| Proto-112       |      46 |  0    |        46 |
| Proto-113       |      46 |  0    |        46 |
| Proto-114       |      46 |  0    |        46 |
| Proto-115       |      46 |  0    |        46 |
| Proto-116       |      46 |  0    |        46 |
| Proto-117       |      46 |  0    |        46 |
| Proto-118       |      46 |  0    |        46 |
| Proto-119       |      46 |  0    |        46 |
| Proto-120       |      46 |  0    |        46 |
| Proto-121       |      46 |  0    |        46 |
| Proto-122       |      46 |  0    |        46 |
| Proto-123       |      46 |  0    |        46 |
| Proto-124       |      46 |  0    |        46 |
| Proto-125       |      46 |  0    |        46 |
| Proto-126       |      46 |  0    |        46 |
| Proto-127       |      46 |  0    |        46 |
| Proto-128       |      46 |  0    |        46 |
| Proto-129       |      46 |  0    |        46 |
| Proto-130       |      46 |  0    |        46 |
| Proto-39        |      46 |  0    |        46 |
| Proto-133       |      46 |  0    |        46 |
| Proto-134       |      46 |  0    |        46 |
| Proto-135       |      46 |  0    |        46 |
| Proto-136       |      46 |  0    |        46 |
| Proto-137       |      46 |  0    |        46 |
| Proto-138       |      46 |  0    |        46 |
| Proto-139       |      46 |  0    |        46 |
| Proto-140       |      46 |  0    |        46 |
| Proto-141       |      46 |  0    |        46 |
| Proto-142       |      46 |  0    |        46 |
| Proto-143       |      46 |  0    |        46 |
| Proto-144       |      46 |  0    |        46 |
| Proto-145       |      46 |  0    |        46 |
| Proto-146       |      46 |  0    |        46 |
| Proto-147       |      46 |  0    |        46 |
| Proto-148       |      46 |  0    |        46 |
| Proto-149       |      46 |  0    |        46 |
| Proto-150       |      46 |  0    |        46 |
| Proto-151       |      46 |  0    |        46 |
| Proto-152       |      46 |  0    |        46 |
| Proto-153       |      46 |  0    |        46 |
| Proto-154       |      46 |  0    |        46 |
| Proto-155       |      46 |  0    |        46 |
| Proto-156       |      46 |  0    |        46 |
| Proto-157       |      46 |  0    |        46 |
| Proto-158       |      46 |  0    |        46 |
| Proto-159       |      46 |  0    |        46 |
| Proto-160       |      46 |  0    |        46 |
| Proto-161       |      46 |  0    |        46 |
| Proto-162       |      46 |  0    |        46 |
| Proto-163       |      46 |  0    |        46 |
| Proto-164       |      46 |  0    |        46 |
| Proto-165       |      46 |  0    |        46 |
| Proto-166       |      46 |  0    |        46 |
| Proto-167       |      46 |  0    |        46 |
| Proto-168       |      46 |  0    |        46 |
| Proto-169       |      46 |  0    |        46 |
| Proto-170       |      46 |  0    |        46 |
| Proto-171       |      46 |  0    |        46 |
| Proto-172       |      46 |  0    |        46 |
| Proto-173       |      46 |  0    |        46 |
| Proto-174       |      46 |  0    |        46 |
| Proto-175       |      46 |  0    |        46 |
| Proto-176       |      46 |  0    |        46 |
| Proto-177       |      46 |  0    |        46 |
| Proto-178       |      46 |  0    |        46 |
| Proto-179       |      46 |  0    |        46 |
| Proto-180       |      46 |  0    |        46 |
| Proto-181       |      46 |  0    |        46 |
| Proto-182       |      46 |  0    |        46 |
| Proto-183       |      46 |  0    |        46 |
| Proto-184       |      46 |  0    |        46 |
| Proto-185       |      46 |  0    |        46 |
| Proto-186       |      46 |  0    |        46 |
| Proto-187       |      46 |  0    |        46 |
| Proto-188       |      46 |  0    |        46 |
| Proto-189       |      46 |  0    |        46 |
| Proto-190       |      46 |  0    |        46 |
| Proto-191       |      46 |  0    |        46 |
| Proto-192       |      46 |  0    |        46 |
| Proto-195       |      46 |  0    |        46 |
| Proto-196       |      46 |  0    |        46 |
| Proto-197       |      46 |  0    |        46 |
| Proto-198       |      46 |  0    |        46 |
| Proto-199       |      46 |  0    |        46 |
| Proto-200       |      46 |  0    |        46 |
| Proto-201       |      46 |  0    |        46 |
| Proto-202       |      46 |  0    |        46 |
| Proto-203       |      46 |  0    |        46 |
| Proto-204       |      46 |  0    |        46 |
| Proto-205       |      46 |  0    |        46 |
| Proto-206       |      46 |  0    |        46 |
| Proto-207       |      46 |  0    |        46 |
| Proto-208       |      46 |  0    |        46 |
| Proto-209       |      46 |  0    |        46 |
| Proto-210       |      46 |  0    |        46 |
| Proto-211       |      46 |  0    |        46 |
| Proto-212       |      46 |  0    |        46 |
| Proto-213       |      46 |  0    |        46 |
| Proto-214       |      46 |  0    |        46 |
| Proto-215       |      46 |  0    |        46 |
| Proto-216       |      46 |  0    |        46 |
| Proto-217       |      46 |  0    |        46 |
| Proto-218       |      46 |  0    |        46 |
| Proto-219       |      46 |  0    |        46 |
| Proto-220       |      46 |  0    |        46 |
| Proto-221       |      46 |  0    |        46 |
| Proto-222       |      46 |  0    |        46 |
| Proto-223       |      46 |  0    |        46 |
| Proto-224       |      46 |  0    |        46 |
| Proto-225       |      46 |  0    |        46 |
| Proto-226       |      46 |  0    |        46 |
| Proto-227       |      46 |  0    |        46 |
| Proto-228       |      46 |  0    |        46 |
| Proto-229       |      46 |  0    |        46 |
| Proto-230       |      46 |  0    |        46 |
| Proto-231       |      46 |  0    |        46 |
| Proto-232       |      46 |  0    |        46 |
| Proto-233       |      46 |  0    |        46 |
| Proto-234       |      46 |  0    |        46 |
| Proto-235       |      46 |  0    |        46 |
| Proto-236       |      46 |  0    |        46 |
| Proto-237       |      46 |  0    |        46 |
| Proto-238       |      46 |  0    |        46 |
| Proto-239       |      46 |  0    |        46 |
| Proto-240       |      46 |  0    |        46 |
| Proto-241       |      46 |  0    |        46 |
| Proto-242       |      46 |  0    |        46 |
| Proto-243       |      46 |  0    |        46 |
| Proto-244       |      46 |  0    |        46 |
| Proto-245       |      46 |  0    |        46 |
| Proto-246       |      46 |  0    |        46 |
| Proto-247       |      46 |  0    |        46 |
| Proto-248       |      46 |  0    |        46 |
| Proto-249       |      46 |  0    |        46 |
| Proto-250       |      46 |  0    |        46 |
| Proto-251       |      46 |  0    |        46 |
| Proto-252       |      46 |  0    |        46 |
| Proto-253       |      46 |  0    |        46 |
| Proto-254       |      46 |  0    |        46 |
| Proto-255       |      46 |  0    |        46 |
| Proto-193       |      41 |  0    |        41 |
| Proto-194       |      41 |  0    |        41 |

## 5. Từ điển 45 Đặc trưng NetFlow v9 & Cảnh báo Rò rỉ (Data Leakage Risk)

| Tên Cột | Phân loại | Ý nghĩa mạng | Mức độ rủi ro rò rỉ (Leakage Risk) |
| :--- | :--- | :--- | :--- |
| `IPV4_SRC_ADDR` | Identity (Layer 3) | Địa chỉ IPv4 của máy nguồn gửi lưu lượng. | **CRITICAL: Nếu đưa trực tiếp vào mô hình, mô hình sẽ học vẹt IP thay vì học hành vi tấn công.** |
| `L4_SRC_PORT` | Identity (Layer 4) | Cổng (Port) dịch vụ của máy nguồn (0 - 65535). | **HIGH: Có thể bị khai thác để nhớ cổng cố định của máy tấn công.** |
| `IPV4_DST_ADDR` | Identity (Layer 3) | Địa chỉ IPv4 của máy đích nhận lưu lượng. | **CRITICAL: Rò rỉ danh tính máy chủ nạn nhân.** |
| `L4_DST_PORT` | Identity (Layer 4) | Cổng (Port) dịch vụ của máy đích (VD: 80-HTTP, 443-HTTPS, 22-SSH). | **MEDIUM: Cần giữ lại ngữ cảnh dịch vụ nhưng tránh overfit vào số cổng.** |
| `PROTOCOL` | Protocol (Layer 3) | Giao thức mạng IP (6: TCP, 17: UDP, 1: ICMP). | **LOW: Đặc trưng hành vi hợp lệ.** |
| `L7_PROTO` | Protocol (Layer 7) | Giao thức tầng ứng dụng được nDPI nhận diện (VD: DNS, HTTP, SSL). | **LOW: Đặc trưng hành vi hợp lệ.** |
| `IN_BYTES` | Payload Volumetrics | Tổng số bytes gửi từ máy nguồn sang máy đích trong flow. | **SAFE: Thuộc tính hành vi cốt lõi.** |
| `OUT_BYTES` | Payload Volumetrics | Tổng số bytes phản hồi từ máy đích về máy nguồn. | **SAFE: Thuộc tính hành vi cốt lõi.** |
| `IN_PKTS` | Payload Volumetrics | Tổng số gói tin (packets) gửi từ nguồn sang đích. | **SAFE: Thuộc tính hành vi cốt lõi.** |
| `OUT_PKTS` | Payload Volumetrics | Tổng số gói tin phản hồi từ đích về nguồn. | **SAFE: Thuộc tính hành vi cốt lõi.** |
| `TCP_FLAGS` | TCP Control | Tổng hợp (tích lũy bitwise) tất cả các cờ TCP xuất hiện trong flow (SYN, ACK, FIN, RST, PSH, URG). | **SAFE: Dấu hiệu nhận diện tấn công cực mạnh.** |
| `CLIENT_TCP_FLAGS` | TCP Control | Các cờ TCP do máy khách gửi đi. | **SAFE: Dấu hiệu hành vi hợp lệ.** |
| `SERVER_TCP_FLAGS` | TCP Control | Các cờ TCP do máy chủ phản hồi. | **SAFE: Dấu hiệu hành vi hợp lệ.** |
| `FLOW_DURATION_MILLISECONDS` | Time & Duration | Thời gian tồn tại của flow mạng tính bằng mili-giây (ms). | **SAFE: Thuộc tính thời gian cốt lõi.** |
| `DURATION_IN` | Time & Duration | Thời lượng luồng gửi đi từ Client sang Server (ms). | **SAFE: Thuộc tính thời gian.** |
| `DURATION_OUT` | Time & Duration | Thời lượng luồng phản hồi từ Server về Client (ms). | **SAFE: Thuộc tính thời gian.** |
| `MIN_TTL` | Network Topology / Hop | Giá trị Time-To-Live nhỏ nhất của gói tin trong flow. | **MEDIUM: Có thể gián tiếp rò rỉ loại OS của máy trong lab.** |
| `MAX_TTL` | Network Topology / Hop | Giá trị Time-To-Live lớn nhất của gói tin trong flow. | **MEDIUM: Tương tự MIN_TTL.** |
| `LONGEST_FLOW_PKT` | Packet Geometry | Kích thước gói tin lớn nhất trong flow (bytes). | **SAFE: Phản ánh cấu trúc packet.** |
| `SHORTEST_FLOW_PKT` | Packet Geometry | Kích thước gói tin nhỏ nhất trong flow (bytes). | **SAFE: Phản ánh cấu trúc packet.** |
| `MIN_IP_PKT_LEN` | Packet Geometry | Độ dài IP packet nhỏ nhất quan sát được. | **SAFE: Thuộc tính hình học packet.** |
| `MAX_IP_PKT_LEN` | Packet Geometry | Độ dài IP packet lớn nhất quan sát được. | **SAFE: Thuộc tính hình học packet.** |
| `SRC_TO_DST_SECOND_BYTES` | Throughput Dynamics | Tốc độ truyền dữ liệu chiều đi (Bytes/giây). | **SAFE: Động lực học băng thông.** |
| `DST_TO_SRC_SECOND_BYTES` | Throughput Dynamics | Tốc độ truyền dữ liệu chiều về (Bytes/giây). | **SAFE: Động lực học băng thông.** |
| `RETRANSMITTED_IN_BYTES` | Congestion & Loss | Số bytes TCP bị truyền lại (retransmitted) chiều đi. | **SAFE: Chỉ số chất lượng truyền tin.** |
| `RETRANSMITTED_IN_PKTS` | Congestion & Loss | Số gói tin TCP bị truyền lại chiều đi. | **SAFE: Chỉ số chất lượng truyền tin.** |
| `RETRANSMITTED_OUT_BYTES` | Congestion & Loss | Số bytes TCP bị truyền lại chiều về. | **SAFE: Chỉ số chất lượng truyền tin.** |
| `RETRANSMITTED_OUT_PKTS` | Congestion & Loss | Số gói tin TCP bị truyền lại chiều về. | **SAFE: Chỉ số chất lượng truyền tin.** |
| `SRC_TO_DST_AVG_THROUGHPUT` | Throughput Dynamics | Băng thông trung bình chiều đi (bits per second - bps). | **SAFE: Động lực học lưu lượng.** |
| `DST_TO_SRC_AVG_THROUGHPUT` | Throughput Dynamics | Băng thông trung bình chiều về (bps). | **SAFE: Động lực học lưu lượng.** |
| `NUM_PKTS_UP_TO_128_BYTES` | Packet Size Bins | Số gói tin trong flow có kích thước <= 128 bytes. | **SAFE: Phân bố kích thước gói.** |
| `NUM_PKTS_128_TO_256_BYTES` | Packet Size Bins | Số gói tin có kích thước từ 129 đến 256 bytes. | **SAFE: Phân bố kích thước gói.** |
| `NUM_PKTS_256_TO_512_BYTES` | Packet Size Bins | Số gói tin có kích thước từ 257 đến 512 bytes. | **SAFE: Phân bố kích thước gói.** |
| `NUM_PKTS_512_TO_1024_BYTES` | Packet Size Bins | Số gói tin có kích thước từ 513 đến 1024 bytes. | **SAFE: Phân bố kích thước gói.** |
| `NUM_PKTS_1024_TO_1514_BYTES` | Packet Size Bins | Số gói tin kích thước tối đa chuẩn MTU Ethernet (1025 đến 1514 bytes). | **SAFE: Phân bố kích thước gói.** |
| `TCP_WIN_MAX_IN` | TCP Window Control | Kích thước TCP Window tối đa phía client gửi. | **LOW: Hành vi điều khiển luồng.** |
| `TCP_WIN_MAX_OUT` | TCP Window Control | Kích thước TCP Window tối đa phía server phản hồi. | **LOW: Hành vi điều khiển luồng.** |
| `ICMP_TYPE` | ICMP Control | Mã loại ICMP (VD: 8: Echo Request / Ping, 0: Echo Reply, 3: Destination Unreachable). | **SAFE: Dấu hiệu nhận diện ICMP Flood.** |
| `ICMP_IPV4_TYPE` | ICMP Control | Loại ICMP dành riêng cho IPv4. | **SAFE: Dấu hiệu kiểm soát mạng.** |
| `DNS_QUERY_ID` | Application Layer (DNS) | Mã định danh giao dịch của truy vấn DNS (Transaction ID). | **SAFE: Giá trị ngẫu nhiên trong DNS.** |
| `DNS_QUERY_TYPE` | Application Layer (DNS) | Loại bản ghi DNS được hỏi (VD: 1: A, 28: AAAA, 15: MX). | **SAFE: Dấu hiệu ứng dụng.** |
| `DNS_TTL_ANSWER` | Application Layer (DNS) | Thời gian tồn tại trong bộ nhớ đệm (Time To Live) của câu trả lời DNS. | **SAFE: Thuộc tính ứng dụng.** |
| `FTP_COMMAND_RET_CODE` | Application Layer (FTP) | Mã phản hồi của lệnh FTP (VD: 220: Service Ready, 530: Not logged in / Brute force). | **SAFE: Dấu hiệu ứng dụng cực kỳ giá trị.** |
| `Label` | Ground Truth | Nhãn nhị phân: 0 = Benign (Bình thường), 1 = Attack (Tấn công). | **TARGET** |
| `Attack` | Ground Truth | Tên chi tiết của lớp tấn công (Benign, Exploits, Fuzzers, DoS, Worms,...). | **TARGET** |