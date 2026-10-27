# Báo Cáo Phân Tích Cấu Trúc Đồ Thị & Tô-pô Mạng (Network Topology Audit)

> **Dự án**: Trust-NIDS Benchmark | **Bộ dữ liệu**: `NF-UNSW-NB15-v2`

## 1. Mô Hình Kiến Trúc Mạng Vật Lý & Định Tuyến (Reconstructed Network Architecture)

Dựa trên phân tích các dải mạng IPv4 (/24 Prefix) trong 2.39 triệu flows, kiến trúc testbed phòng thí nghiệm được phác họa như sau:

```text
+-----------------------------------------------------------------------------------------+
|                                  MÔ HÌNH MẠNG TESTBED                                   |
+-----------------------------------------------------------------------------------------+
                                                                                           
  [1] NGUỒN TẤN CÔNG (WAN/Internet)           [2] LƯU LƯỢNG SẠCH MÔ PHỎNG (IXIA Clients) 
      Subnet: 175.45.176.0/24                     Subnet: 59.166.0.0/24                   
      - 175.45.176.0 (25.7k attacks)              - 59.166.0.0 (230k flows)               
      - 175.45.176.1 (27.5k attacks)              - 59.166.0.1 (230k flows)               
      - 175.45.176.2 (18.8k attacks)              - 59.166.0.2 (230k flows)               
      - 175.45.176.3 (23.0k attacks)              - 59.166.0.3 (228k flows)               
                                                  - 59.166.0.4 (230k flows)               
             \                                            /                               
              \                                          /                                
               +--------------------+-------------------+                                 
                                    |                                                     
                                    v                                                     
                      [EDGE ROUTER & FIREWALL GATEWAY]                                    
                       (Quản lý định tuyến WAN -> DMZ)                                    
                                    |                                                     
                                    v                                                     
                    [VÙNG MẠNG CHỦ NẠN NHÂN - DMZ SERVER FARM]                            
                            Subnet: 149.171.126.0/24                                      
                      (10 Máy chủ: 149.171.126.10 -> .19)                                 
               - Hứng chịu toàn bộ 95,053 cuộc tấn công (100%)                            
               - Đồng thời phục vụ 2.27 triệu kết nối người dùng sạch                     
+-----------------------------------------------------------------------------------------+
```

## 2. Thống Kê Phân Vai Địa Chỉ IP (IP Persona Inventory)

| ip              |   flows_as_src |   attacks_sent |   benign_sent |   targets_contacted |   flows_as_dst |   attacks_received |   benign_received |   sources_received_from | role           |
|:----------------|---------------:|---------------:|--------------:|--------------------:|---------------:|-------------------:|------------------:|------------------------:|:---------------|
| 175.45.176.1    |          31473 |          27505 |          3968 |                  10 |           4018 |                  0 |              4018 |                      11 | ATTACKER       |
| 175.45.176.0    |          29507 |          25745 |          3762 |                  10 |           3875 |                  0 |              3875 |                      11 | ATTACKER       |
| 175.45.176.3    |          30023 |          23030 |          6993 |                  10 |           3950 |                  0 |              3950 |                      11 | ATTACKER       |
| 175.45.176.2    |          22502 |          18773 |          3729 |                  10 |            108 |                  0 |               108 |                      11 | ATTACKER       |
| 149.171.126.17  |             71 |              0 |            71 |                   4 |          14659 |              12627 |              2032 |                       4 | VICTIM_SERVER  |
| 149.171.126.10  |           1839 |              0 |          1839 |                   4 |          11960 |              11056 |               904 |                       4 | VICTIM_SERVER  |
| 149.171.126.18  |           3900 |              0 |          3900 |                   4 |          12413 |              10469 |              1944 |                       4 | VICTIM_SERVER  |
| 149.171.126.12  |           1990 |              0 |          1990 |                   4 |          10603 |               9821 |               782 |                       4 | VICTIM_SERVER  |
| 149.171.126.15  |           1986 |              0 |          1986 |                   4 |          11922 |               9489 |              2433 |                       4 | VICTIM_SERVER  |
| 149.171.126.14  |           1932 |              0 |          1932 |                   4 |          10771 |               9448 |              1323 |                       4 | VICTIM_SERVER  |
| 149.171.126.13  |             64 |              0 |            64 |                   4 |          11676 |               9431 |              2245 |                       4 | VICTIM_SERVER  |
| 149.171.126.19  |             45 |              0 |            45 |                   4 |           9988 |               7926 |              2062 |                       4 | VICTIM_SERVER  |
| 149.171.126.11  |             58 |              0 |            58 |                   5 |          10063 |               7772 |              2291 |                       5 | VICTIM_SERVER  |
| 149.171.126.16  |             47 |              0 |            47 |                   4 |           9451 |               7014 |              2437 |                       4 | VICTIM_SERVER  |
| 59.166.0.1      |         230357 |              0 |        230357 |                  10 |            602 |                  0 |               602 |                      10 | BENIGN_CLIENT  |
| 59.166.0.2      |         230214 |              0 |        230214 |                  10 |            587 |                  0 |               587 |                      10 | BENIGN_CLIENT  |
| 59.166.0.4      |         230209 |              0 |        230209 |                  10 |            550 |                  0 |               550 |                      10 | BENIGN_CLIENT  |
| 59.166.0.0      |         230068 |              0 |        230068 |                  10 |            608 |                  0 |               608 |                      10 | BENIGN_CLIENT  |
| 59.166.0.3      |         228573 |              0 |        228573 |                  10 |            530 |                  0 |               530 |                      10 | BENIGN_CLIENT  |
| 59.166.0.5      |         228093 |              0 |        228093 |                  10 |            522 |                  0 |               522 |                      10 | BENIGN_CLIENT  |
| 59.166.0.9      |         221404 |              0 |        221404 |                  10 |            574 |                  0 |               574 |                      10 | BENIGN_CLIENT  |
| 59.166.0.8      |         220524 |              0 |        220524 |                  10 |            525 |                  0 |               525 |                      10 | BENIGN_CLIENT  |
| 59.166.0.6      |         219536 |              0 |        219536 |                  10 |            532 |                  0 |               532 |                      10 | BENIGN_CLIENT  |
| 59.166.0.7      |         219433 |              0 |        219433 |                  10 |            518 |                  0 |               518 |                      10 | BENIGN_CLIENT  |
| 149.171.126.4   |            592 |              0 |           592 |                  10 |         230043 |                  0 |            230043 |                      10 | INFRASTRUCTURE |
| 149.171.126.0   |            590 |              0 |           590 |                  10 |         229472 |                  0 |            229472 |                      10 | INFRASTRUCTURE |
| 149.171.126.5   |            570 |              0 |           570 |                  10 |         228812 |                  0 |            228812 |                      10 | INFRASTRUCTURE |
| 149.171.126.8   |            565 |              0 |           565 |                  10 |         217886 |                  0 |            217886 |                      10 | INFRASTRUCTURE |
| 149.171.126.3   |            562 |              0 |           562 |                  10 |         229688 |                  0 |            229688 |                      10 | INFRASTRUCTURE |
| 149.171.126.6   |            551 |              0 |           551 |                  10 |         220567 |                  0 |            220567 |                      10 | INFRASTRUCTURE |
| 149.171.126.1   |            550 |              0 |           550 |                  10 |         229292 |                  0 |            229292 |                      10 | INFRASTRUCTURE |
| 149.171.126.2   |            548 |              0 |           548 |                  10 |         229983 |                  0 |            229983 |                      10 | INFRASTRUCTURE |
| 149.171.126.9   |            525 |              0 |           525 |                  10 |         220528 |                  0 |            220528 |                      10 | INFRASTRUCTURE |
| 149.171.126.7   |            495 |              0 |           495 |                  10 |         222140 |                  0 |            222140 |                      10 | INFRASTRUCTURE |
| 10.40.85.1      |            294 |              0 |           294 |                   5 |              0 |                  0 |                 0 |                       0 | INFRASTRUCTURE |
| 10.40.85.10     |            289 |              0 |           289 |                   2 |              0 |                  0 |                 0 |                       0 | INFRASTRUCTURE |
| 10.40.182.1     |            278 |              0 |           278 |                   2 |              0 |                  0 |                 0 |                       0 | INFRASTRUCTURE |
| 192.168.241.243 |             16 |              0 |            16 |                   1 |             16 |                  0 |                16 |                       1 | INFRASTRUCTURE |
| 10.40.182.6     |              1 |              0 |             1 |                   1 |              0 |                  0 |                 0 |                       0 | INFRASTRUCTURE |
| 127.0.0.1       |              1 |              0 |             1 |                   1 |              1 |                  0 |                 1 |                       1 | INFRASTRUCTURE |
| 192.168.241.50  |              0 |              0 |             0 |                   0 |             34 |                  0 |                34 |                       1 | INFRASTRUCTURE |
| 224.0.0.5       |              0 |              0 |             0 |                   0 |            547 |                  0 |               547 |                       2 | INFRASTRUCTURE |
| 10.40.182.255   |              0 |              0 |             0 |                   0 |              1 |                  0 |                 1 |                       1 | INFRASTRUCTURE |
| 10.40.198.10    |              0 |              0 |             0 |                   0 |            260 |                  0 |               260 |                       2 | INFRASTRUCTURE |

## 3. Ma Trận Cạnh Tấn Công Chính (Top Malicious Traffic Edges)

| source       | target         |   total_flows |   attack_flows |   benign_flows |   total_in_mb |   total_out_mb | attack_types                                                                          |
|:-------------|:---------------|--------------:|---------------:|---------------:|--------------:|---------------:|:--------------------------------------------------------------------------------------|
| 175.45.176.1 | 149.171.126.18 |          4180 |           3898 |            282 |         22.3  |          30.55 | Exploits, Reconnaissance, Generic, DoS, Shellcode, Worms, Fuzzers, Backdoor           |
| 175.45.176.0 | 149.171.126.10 |          4091 |           3836 |            255 |         31.1  |          17.43 | Exploits, Generic, Reconnaissance, DoS, Shellcode, Worms, Fuzzers, Backdoor           |
| 175.45.176.0 | 149.171.126.13 |          4403 |           3827 |            576 |         55.38 |          27.2  | Backdoor, DoS, Fuzzers, Reconnaissance, Generic, Analysis, Exploits, Shellcode, Worms |
| 175.45.176.1 | 149.171.126.17 |          4628 |           3746 |            882 |         46.89 |          30.27 | Analysis, Generic, Reconnaissance, Shellcode, Worms, Backdoor, Fuzzers, Exploits, DoS |
| 175.45.176.0 | 149.171.126.17 |          3888 |           3726 |            162 |         31.75 |          30.28 | Analysis, Exploits, Generic, Reconnaissance, DoS, Worms, Shellcode, Fuzzers, Backdoor |
| 175.45.176.3 | 149.171.126.15 |          5274 |           3676 |           1598 |         36.29 |          28.89 | Backdoor, DoS, Fuzzers, Generic, Reconnaissance, Exploits, Shellcode, Worms           |
| 175.45.176.0 | 149.171.126.12 |          3889 |           3652 |            237 |         39.53 |          40.68 | Generic, Reconnaissance, Shellcode, Worms, DoS, Backdoor, Fuzzers, Exploits           |
| 175.45.176.1 | 149.171.126.14 |          3825 |           3599 |            226 |         32.35 |          20.61 | Reconnaissance, Generic, Exploits, Backdoor, DoS, Fuzzers, Worms, Shellcode           |
| 175.45.176.1 | 149.171.126.10 |          3739 |           3598 |            141 |         42.81 |          59.77 | Fuzzers, DoS, Shellcode, Worms, Exploits, Analysis, Reconnaissance, Generic, Backdoor |
| 175.45.176.3 | 149.171.126.18 |          3760 |           3413 |            347 |         33.62 |          31.91 | Reconnaissance, Generic, Shellcode, Worms, DoS, Backdoor, Fuzzers, Exploits           |
| 175.45.176.2 | 149.171.126.17 |          3519 |           3239 |            280 |         62.04 |          30.92 | Fuzzers, DoS, Shellcode, Worms, Exploits, Analysis, Reconnaissance, Generic, Backdoor |
| 175.45.176.3 | 149.171.126.19 |          4538 |           3226 |           1312 |         41.64 |          26.96 | Fuzzers, Backdoor, Exploits, Reconnaissance, Generic, Shellcode, Worms, Analysis, DoS |
| 175.45.176.1 | 149.171.126.12 |          3240 |           3038 |            202 |         34.62 |          22.13 | Analysis, Reconnaissance, Generic, Shellcode, Worms, Backdoor, Fuzzers, Exploits, DoS |
| 175.45.176.1 | 149.171.126.11 |          2893 |           2245 |            648 |         55.25 |          43.53 | DoS, Backdoor, Reconnaissance, Generic, Exploits, Fuzzers, Shellcode, Worms, Analysis |
| 175.45.176.0 | 149.171.126.15 |          2341 |           2132 |            209 |         68.66 |          35.12 | DoS, Backdoor, Reconnaissance, Generic, Exploits, Fuzzers, Shellcode, Worms, Analysis |
| 175.45.176.3 | 149.171.126.14 |          2297 |           2093 |            204 |         61.36 |          23.67 | Backdoor, DoS, Fuzzers, Analysis, Shellcode, Worms, Reconnaissance, Generic, Exploits |
| 175.45.176.1 | 149.171.126.15 |          2391 |           2080 |            311 |         78.59 |          29.63 | Shellcode, Worms, Exploits, Analysis, Reconnaissance, Generic, Fuzzers, Backdoor, DoS |
| 175.45.176.1 | 149.171.126.13 |          2771 |           2024 |            747 |         24.02 |          46.97 | Fuzzers, Backdoor, Shellcode, Worms, Analysis, DoS, Reconnaissance, Generic, Exploits |
| 175.45.176.3 | 149.171.126.10 |          2335 |           1943 |            392 |         25.36 |          23.27 | DoS, Backdoor, Analysis, Shellcode, Worms, Exploits, Reconnaissance, Generic, Fuzzers |
| 175.45.176.2 | 149.171.126.14 |          2264 |           1939 |            325 |         29.53 |          28.94 | Fuzzers, Backdoor, Shellcode, Worms, DoS, Reconnaissance, Generic, Exploits           |

