#!/usr/bin/env python3
"""
scripts/download_data.py
Automated high-speed dataset downloader for Trust-NIDS Benchmark.

Features:
- Fetches ephemeral pre-signed AWS S3 download links directly from UQ RDM API.
- Accelerates download using multi-connection segmented transfer via aria2c (or falls back to Python streaming).
- Supports auto-extraction (.zip -> .csv) and validation.
- Optional automatic conversion to Apache Parquet for 5-10x faster I/O and lower memory usage.
"""

import argparse
import json
import logging
import os
import shutil
import subprocess
import sys
import time
import urllib.request
import zipfile
from pathlib import Path
from typing import Dict, Any, Optional

import yaml

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger("TrustNIDS-Downloader")


def load_dataset_registry(config_path: Path) -> Dict[str, Any]:
    """Loads dataset definitions and UUIDs from YAML config."""
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def get_signed_s3_url(uuid: str, api_base: str) -> str:
    """Queries the University of Queensland RDM API for a signed S3 URL."""
    api_url = f"{api_base.rstrip('/')}/{uuid}/download"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) TrustNIDS/1.0",
        "Accept": "application/json",
    }
    logger.info(f"Resolving download link for UUID: {uuid}")
    req = urllib.request.Request(api_url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            s3_url = data.get("url")
            if not s3_url:
                raise ValueError(f"API response did not contain download URL: {data}")
            return s3_url
    except Exception as e:
        logger.error(f"Failed to query UQ RDM API: {e}")
        raise


def download_with_aria2(
    s3_url: str,
    output_dir: Path,
    filename: str,
    max_connections: int = 16
) -> Path:
    """Executes aria2c with multi-connection acceleration."""
    aria2_path = shutil.which("aria2c")
    if not aria2_path:
        raise RuntimeError("aria2c executable not found on system PATH.")

    output_dir.mkdir(parents=True, exist_ok=True)
    target_file = output_dir / filename

    cmd = [
        aria2_path,
        f"-x{max_connections}",
        f"-s{max_connections}",
        "-j1",
        "-k1M",
        "--file-allocation=none",
        "--summary-interval=1",
        "--console-log-level=warn",
        "--allow-overwrite=true",
        "--auto-file-renaming=false",
        "-d", str(output_dir),
        "-o", filename,
        s3_url
    ]

    logger.info(f"Launching aria2c accelerator with {max_connections} connections...")
    start_time = time.time()
    result = subprocess.run(cmd)
    if result.returncode != 0:
        raise RuntimeError(f"aria2c exited with error code {result.returncode}")

    elapsed = time.time() - start_time
    size_mb = target_file.stat().st_size / (1024 * 1024)
    speed_mbps = (size_mb / elapsed) if elapsed > 0 else 0
    logger.info(f"Download complete: {size_mb:.2f} MB in {elapsed:.1f}s (~{speed_mbps:.2f} MB/s)")
    return target_file


def download_with_python_fallback(
    s3_url: str,
    output_dir: Path,
    filename: str,
    chunk_size: int = 4 * 1024 * 1024
) -> Path:
    """Standard chunked stream download fallback when aria2c is unavailable."""
    output_dir.mkdir(parents=True, exist_ok=True)
    target_file = output_dir / filename

    logger.info("Using Python streaming downloader fallback...")
    req = urllib.request.Request(s3_url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as resp, open(target_file, "wb") as f:
        total_size = int(resp.headers.get("Content-Length", 0))
        downloaded = 0
        start_time = time.time()
        while True:
            chunk = resp.read(chunk_size)
            if not chunk:
                break
            f.write(chunk)
            downloaded += len(chunk)
            if total_size > 0:
                percent = (downloaded / total_size) * 100
                print(f"\rProgress: {downloaded / (1024*1024):.1f}/{total_size / (1024*1024):.1f} MB ({percent:.1f}%)", end="")
    print()
    elapsed = time.time() - start_time
    logger.info(f"Python download finished in {elapsed:.1f}s.")
    return target_file


def extract_zip(zip_path: Path, extract_to: Path, remove_archive: bool = False) -> None:
    """Extracts zip archive with progress reporting."""
    logger.info(f"Extracting {zip_path.name} -> {extract_to} ...")
    extract_to.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "r") as zf:
        members = zf.namelist()
        for i, member in enumerate(members, 1):
            zf.extract(member, extract_to)
            if i % 5 == 0 or i == len(members):
                logger.info(f"Extracted {i}/{len(members)} entries...")

    if remove_archive:
        logger.info(f"Removing archive {zip_path.name} to save disk space.")
        zip_path.unlink()


def inspect_dataset_csv(extract_dir: Path) -> None:
    """Finds extracted CSV files and prints summary schema and rows."""
    csv_files = list(extract_dir.rglob("*.csv"))
    if not csv_files:
        logger.warning(f"No CSV files found in {extract_dir}")
        return

    import pandas as pd
    for csv_file in csv_files:
        size_mb = csv_file.stat().st_size / (1024 * 1024)
        logger.info(f"\n==========================================")
        logger.info(f"Inspecting file: {csv_file.name} ({size_mb:.2f} MB)")
        logger.info(f"Location: {csv_file}")
        # Read header and first 5 rows
        df_sample = pd.read_csv(csv_file, nrows=5)
        logger.info(f"Columns count: {len(df_sample.columns)}")
        logger.info(f"Columns list: {list(df_sample.columns)}")
        logger.info(f"Data types preview:\n{df_sample.dtypes.value_counts()}")
        logger.info("==========================================\n")


def convert_csv_to_parquet(extract_dir: Path, target_dir: Path) -> None:
    """Converts CSV files to Parquet for 10x faster benchmark loading."""
    csv_files = list(extract_dir.rglob("*.csv"))
    if not csv_files:
        return

    import pandas as pd
    target_dir.mkdir(parents=True, exist_ok=True)
    for csv_file in csv_files:
        parquet_file = target_dir / f"{csv_file.stem}.parquet"
        logger.info(f"Converting {csv_file.name} -> {parquet_file.name} ...")
        start = time.time()
        # Read in chunks or full if memory allows
        df = pd.read_csv(csv_file)
        df.to_parquet(parquet_file, index=False, engine="pyarrow")
        elapsed = time.time() - start
        orig_mb = csv_file.stat().st_size / (1024 * 1024)
        pq_mb = parquet_file.stat().st_size / (1024 * 1024)
        logger.info(f"Parquet conversion done: {orig_mb:.1f} MB (CSV) -> {pq_mb:.1f} MB (Parquet) in {elapsed:.1f}s.")


def main():
    parser = argparse.ArgumentParser(description="Trust-NIDS Automated High-Speed Dataset Downloader")
    parser.add_argument(
        "--dataset",
        type=str,
        default="nf-unsw-nb15-v2",
        help="Dataset identifier (e.g. nf-cse-cic-ids2018-v2, nf-cse-cic-ids2018-v3, nf-ton-iot-v2, nf-unsw-nb15-v2, all)"
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("configs/datasets.yaml"),
        help="Path to datasets registry YAML configuration"
    )
    parser.add_argument(
        "--dest-dir",
        type=Path,
        default=Path("data/raw"),
        help="Destination directory for raw files"
    )
    parser.add_argument(
        "--max-connections",
        type=int,
        default=16,
        help="Maximum concurrent aria2c connections (default: 16)"
    )
    parser.add_argument(
        "--no-extract",
        action="store_true",
        help="Do not automatically extract zip archive"
    )
    parser.add_argument(
        "--clean-zip",
        action="store_true",
        help="Delete zip archive after extraction"
    )
    parser.add_argument(
        "--to-parquet",
        action="store_true",
        help="Also convert extracted CSV to high-speed Parquet format in data/processed"
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all available datasets in registry"
    )

    args = parser.parse_args()
    registry = load_dataset_registry(args.config)
    datasets_meta = registry.get("datasets", {})
    api_base = registry.get("api_base_url", "https://api.rdm.uq.edu.au/datasets")

    if args.list:
        print("\n=== Available NetFlow Benchmark Datasets ===")
        for key, meta in datasets_meta.items():
            print(f"- {key:25} | {meta.get('approx_size_mb', 0):>6.1f} MB | {meta.get('description')}")
        print()
        return

    selected_keys = []
    if args.dataset.lower() == "all":
        selected_keys = list(datasets_meta.keys())
    elif args.dataset in datasets_meta:
        selected_keys = [args.dataset]
    else:
        logger.error(f"Unknown dataset '{args.dataset}'. Choose from: {list(datasets_meta.keys())}")
        sys.exit(1)

    has_aria2 = shutil.which("aria2c") is not None
    logger.info(f"Downloader engine: {'aria2c (Multi-connection accelerated)' if has_aria2 else 'Standard Python Stream'}")

    for key in selected_keys:
        meta = datasets_meta[key]
        name = meta.get("name", key)
        uuid = meta.get("uuid")
        size_est = meta.get("approx_size_mb", 0)

        logger.info(f"\n>>> Starting acquisition for: {name} (~{size_est} MB)")
        s3_url = get_signed_s3_url(uuid, api_base)

        zip_filename = f"{key}.zip"
        dataset_raw_dir = args.dest_dir / key

        if has_aria2:
            downloaded_zip = download_with_aria2(
                s3_url=s3_url,
                output_dir=dataset_raw_dir,
                filename=zip_filename,
                max_connections=args.max_connections
            )
        else:
            downloaded_zip = download_with_python_fallback(
                s3_url=s3_url,
                output_dir=dataset_raw_dir,
                filename=zip_filename
            )

        if not args.no_extract:
            extract_zip(downloaded_zip, dataset_raw_dir, remove_archive=args.clean_zip)
            inspect_dataset_csv(dataset_raw_dir)

            if args.to_parquet:
                processed_dir = Path("data/processed") / key
                convert_csv_to_parquet(dataset_raw_dir, processed_dir)

    logger.info("\nAll requested dataset tasks completed successfully!")


if __name__ == "__main__":
    main()
