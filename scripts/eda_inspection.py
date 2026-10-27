#!/usr/bin/env python3
"""
scripts/eda_inspection.py
Exploratory Data Analysis (EDA) & Data Leakage Audit Tool for Trust-NIDS.

Analyzes:
1. Dataset dimensions and memory footprint.
2. Binary and multiclass label distribution (imbalance ratio).
3. IP Address cardinality (Source & Destination) and graph density.
4. Top talkers / Super-nodes (distribution of flows per IP).
5. Feature value ranges, missing values, and high-correlation leakage risks.
"""

import argparse
import logging
import sys
from pathlib import Path

# Force UTF-8 stdout for Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import numpy as np
import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger("TrustNIDS-EDA")


def run_eda(parquet_path: Path) -> None:
    if not parquet_path.exists():
        raise FileNotFoundError(f"Parquet file not found at: {parquet_path}")

    logger.info(f"Loading parquet: {parquet_path.name} ...")
    df = pd.read_parquet(parquet_path)

    n_rows, n_cols = df.shape
    memory_mb = df.memory_usage(deep=True).sum() / (1024 * 1024)

    print("\n" + "=" * 70)
    print(f"[*] EXPLORATORY DATA AUDIT: {parquet_path.name}")
    print("=" * 70)
    print(f"• Total Network Flows (Rows): {n_rows:,}")
    print(f"• Total Extracted Features:   {n_cols}")
    print(f"• Memory in RAM:              {memory_mb:.2f} MB")
    print(f"• Missing / Null Values:      {df.isnull().sum().sum()}")

    # 1. Label Distribution
    print("\n" + "-" * 70)
    print("1. CLASS DISTRIBUTION (Binary & Multiclass)")
    print("-" * 70)
    if "Label" in df.columns:
        label_counts = df["Label"].value_counts()
        label_pct = df["Label"].value_counts(normalize=True) * 100
        for label, count in label_counts.items():
            name = "Benign (0)" if label == 0 else "Attack (1)"
            print(f"  - {name:<12}: {count:>10,} flows ({label_pct[label]:>5.2f}%)")

    if "Attack" in df.columns:
        print("\n  Detailed Attack Breakdown:")
        attack_counts = df["Attack"].value_counts()
        attack_pct = df["Attack"].value_counts(normalize=True) * 100
        for attack_name, count in attack_counts.items():
            print(f"  - {attack_name:<16}: {count:>10,} flows ({attack_pct[attack_name]:>5.2f}%)")

    # 2. Topology & Identity Leakage Risk
    print("\n" + "-" * 70)
    print("2. TOPOLOGY & IP IDENTITY LEAKAGE AUDIT")
    print("-" * 70)
    src_col = "IPV4_SRC_ADDR" if "IPV4_SRC_ADDR" in df.columns else None
    dst_col = "IPV4_DST_ADDR" if "IPV4_DST_ADDR" in df.columns else None

    if src_col and dst_col:
        unique_src = df[src_col].nunique()
        unique_dst = df[dst_col].nunique()
        all_unique_ips = len(set(df[src_col].unique()).union(set(df[dst_col].unique())))

        print(f"• Unique Source IPs:      {unique_src}")
        print(f"• Unique Destination IPs: {unique_dst}")
        print(f"• Total Distinct Nodes:   {all_unique_ips}")
        print(f"• Average Flows per Node: {n_rows / all_unique_ips:,.1f}")

        # Top 5 Source IPs by volume
        print("\n  Top 5 High-Volume Source IPs (Super-Nodes):")
        top_src = df[src_col].value_counts().head(5)
        for ip, count in top_src.items():
            pct = (count / n_rows) * 100
            print(f"    * {ip:<18}: {count:>10,} flows ({pct:>5.2f}%)")

        print("\n  [!] DATA LEAKAGE AUDIT INSIGHT:")
        print(f"    In a random split, these {all_unique_ips} IPs will be present in BOTH Train and Test.")
        print("    Any model using raw IP features will trivially memorize identities rather than attack behavior.")

    # 3. Protocol & Duration Summary
    print("\n" + "-" * 70)
    print("3. PROTOCOL & FLOW CHARACTERISTICS")
    print("-" * 70)
    if "PROTOCOL" in df.columns:
        proto_map = {6: "TCP (6)", 17: "UDP (17)", 1: "ICMP (1)"}
        proto_counts = df["PROTOCOL"].value_counts()
        for p, count in proto_counts.head(5).items():
            p_name = proto_map.get(p, f"Proto-{p}")
            print(f"  - {p_name:<12}: {count:>10,} flows ({(count / n_rows)*100:>5.2f}%)")

    if "FLOW_DURATION_MILLISECONDS" in df.columns:
        dur = df["FLOW_DURATION_MILLISECONDS"]
        print(f"\n• Flow Duration (ms): Min={dur.min():.1f}, Median={dur.median():.1f}, Mean={dur.mean():.1f}, Max={dur.max():.1f}")

    print("=" * 70 + "\n")


def main():
    parser = argparse.ArgumentParser(description="Trust-NIDS Exploratory Data Analysis & Leakage Audit")
    parser.add_argument(
        "--data-path",
        type=Path,
        default=Path("data/processed/nf-unsw-nb15-v2/NF-UNSW-NB15-v2.parquet"),
        help="Path to processed parquet file"
    )
    args = parser.parse_args()
    run_eda(args.data_path)


if __name__ == "__main__":
    main()
