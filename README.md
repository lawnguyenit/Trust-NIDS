# Trust-NIDS Benchmark

> **An Empirical Audit Framework for Evaluating Graph vs. Tabular Intrusion Detection Systems under Realistic Distribution Shifts and Operational Constraints.**

---

## 1. Project Overview

Recent academic literature in Network Intrusion Detection Systems (NIDS) often claims near-perfect detection accuracy (>99%) using complex Graph Neural Networks (GNNs). However, in realistic operational settings:
1. **Data Leakage & Random Splits**: Random $k$-fold cross validation overfits on repetitive topological identities (IP addresses/ports) and benign flow patterns.
2. **Distribution Shift**: Networks experience chronic temporal drift (protocol evolution over time) and topological shifts (unseen host subnets and zero-day endpoints).
3. **Operational Trade-offs**: GNNs incur heavy graph construction latency ($p95$), large memory footprints (VRAM/RAM), and lower throughput (flows/sec) compared to tuned Tabular baselines (XGBoost, LightGBM).

**Trust-NIDS** provides a standardized, leakage-free empirical audit framework designed to evaluate tabular vs. graph models across three distribution regimes:
* **E1 (Stratified Random)**: Ideal upper-bound baseline.
* **E2 (Chronological Shift)**: Strict temporal cutoff ($t_{\text{train}} \to t_{\text{test}}$).
* **E3 (Subnet Disjoint Shift)**: Inductive generalization to completely disjoint IP subnets.

---

## 2. Directory Structure

```text
Trust-NIDS/
├── configs/
│   └── datasets.yaml           # Metadata & UUID registry for NetFlow datasets (UQ RDM)
├── data/
│   ├── raw/                    # Raw downloaded NetFlow CSV archives (.gitignore)
│   └── processed/              # High-speed Apache Parquet caches (.gitignore)
├── scripts/
│   └── download_data.py        # Automated multi-connection downloader (aria2c accelerated)
├── src/
│   ├── data/                   # Cleaned loaders, leak-free splitters, graph builders
│   ├── models/                 # Tabular (XGBoost, LightGBM) & Graph (E-GraphSAGE) models
│   ├── evaluation/             # Operational profiling (p95 latency, throughput, memory) & metrics
│   └── audit/                  # Distribution drift and shift quantification (Wasserstein, MMD)
├── tests/                      # Leakage tests and data integrity suites
├── .gitignore
└── README.md
```

---

## 3. Dataset Registry & Acquisition

Trust-NIDS uses standardized NetFlow datasets published by the **University of Queensland Cyber Security Group** (Sarhan et al.):

| Dataset ID | Version | Features | Compressed Size | Characteristics |
| :--- | :---: | :---: | :---: | :--- |
| `nf-cse-cic-ids2018-v2` | v2 | 43 | ~583.7 MB | Large enterprise network, clean NetFlow format |
| `nf-cse-cic-ids2018-v3` | v3 | 53 | ~744.0 MB | Extended temporal & Inter-Packet Arrival Time (IAT) stats |
| `nf-ton-iot-v2` | v2 | 43 | ~160.3 MB | Modern IoT/IIoT attack scenarios |
| `nf-unsw-nb15-v2` | v2 | 43 | ~32.3 MB | Compact dataset, ideal for smoke tests & prototyping |

### High-Speed Automated Download

Downloads query the official UQ RDM API for pre-signed AWS S3 links and leverage **`aria2c`** with up to 16 concurrent segmented connections:

```powershell
# List available datasets in registry
python scripts/download_data.py --list

# Download and convert to Parquet (Smoke test with NF-UNSW-NB15-v2)
python scripts/download_data.py --dataset nf-unsw-nb15-v2 --to-parquet

# Download the primary enterprise benchmark (NF-CSE-CIC-IDS2018-v2)
python scripts/download_data.py --dataset nf-cse-cic-ids2018-v2 --to-parquet
```
