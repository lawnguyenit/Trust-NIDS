#!/usr/bin/env python3
"""
analysis/feature_bundles.py
Interactive CLI Tool for Exploring the 45 NetFlow Features in 8 Structured Bundles.
"""

import argparse
import sys
from pathlib import Path

# Force UTF-8 stdout
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import duckdb
import yaml


def load_bundles_config(config_path: Path = Path("configs/feature_bundles.yaml")):
    if not config_path.exists():
        raise FileNotFoundError(f"Config not found: {config_path}")
    with open(config_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data.get("bundles", {})


def get_real_sample(parquet_path: Path, feature_names: list):
    """Pulls min, max, median, sample from the parquet file."""
    if not parquet_path.exists():
        return {}
    con = duckdb.connect(":memory:")
    # Filter features that exist in parquet
    query_parts = []
    for f in feature_names:
        if f in ("IPV4_SRC_ADDR", "IPV4_DST_ADDR", "Attack"):
            query_parts.append(f"COUNT(DISTINCT {f}) AS {f}__distinct")
        else:
            query_parts.append(f"MIN({f}) AS {f}__min, ROUND(AVG({f}), 1) AS {f}__avg, MAX({f}) AS {f}__max")
    
    q = f"SELECT {', '.join(query_parts)} FROM read_parquet('{parquet_path.as_posix()}');"
    df = con.execute(q).df()
    return df.iloc[0].to_dict()


def show_summary(bundles: dict):
    print("\n" + "=" * 80)
    print("📦 BẢNG TỔNG QUAN 8 BỘ THUỘC TÍNH (45 TRƯỜNG NETFLOW v9)")
    print("=" * 80)
    print(f"{'Mã':<4} | {'Tên Bộ Thuộc Tính':<46} | {'Số trường':<10} | {'Rủi ro Rò rỉ'}")
    print("-" * 80)
    total_f = 0
    for key, b in bundles.items():
        b_id = b.get("id", "-")
        b_name = b.get("name", key)
        count = len(b.get("features", []))
        total_f += count
        risk = b.get("leakage_risk", "SAFE")
        print(f"[{b_id:<2}] | {b_name:<46} | {count:>4} trường | {risk}")
    print("-" * 80)
    print(f"TỔNG CỘNG: 8 BỘ | 45 THUỘC TÍNH NETFLOW ĐƯỢC CHUẨN HÓA TOÀN DIỆN")
    print("=" * 80)
    print("\n💡 Gợi ý lệnh xem chi tiết từng bộ:")
    print("   python analysis/feature_bundles.py --bundle 1   (Xem Bộ 1: Định danh)")
    print("   python analysis/feature_bundles.py --bundle 4   (Xem Bộ 4: Thời gian)")
    print("   python analysis/feature_bundles.py --search tcp (Tìm các thuộc tính liên quan TCP)\n")


def show_bundle_detail(bundle_key: str, bundle: dict, parquet_path: Path):
    b_id = bundle.get("id", "-")
    b_name = bundle.get("name", bundle_key)
    desc = bundle.get("description", "")
    risk = bundle.get("leakage_risk", "SAFE")
    action = bundle.get("recommended_action", "")
    features = bundle.get("features", [])

    print("\n" + "=" * 80)
    print(f"🔍 BỘ [{b_id}]: {b_name.upper()}")
    print("=" * 80)
    print(f"• Mô tả chung:          {desc}")
    print(f"• Đánh giá Rò rỉ:       {risk}")
    print(f"• Khuyến nghị Xử lý:    {action}")
    print(f"• Tổng số trường:       {len(features)} thuộc tính\n")

    f_names = [f["name"] for f in features]
    stats = {}
    if parquet_path.exists():
        try:
            stats = get_real_sample(parquet_path, f_names)
        except Exception:
            pass

    print(f"{'STT':<4} | {'Tên Thuộc Tính':<28} | {'Kiểu':<7} | {'Rủi ro':<9} | {'Mô tả & Dữ liệu thực tế'}")
    print("-" * 80)
    for i, f in enumerate(features, 1):
        name = f["name"]
        f_type = f.get("type", "int")
        f_risk = f.get("leakage_risk", "SAFE")
        f_desc = f.get("description", "")

        stat_str = ""
        if name in ("IPV4_SRC_ADDR", "IPV4_DST_ADDR", "Attack"):
            if f"{name}__distinct" in stats:
                stat_str = f" [Có {int(stats[f'{name}__distinct'])} giá trị duy nhất trong tập]"
        else:
            if f"{name}__min" in stats and f"{name}__max" in stats:
                stat_str = f" [Min={stats[f'{name}__min']}, Avg={stats[f'{name}__avg']}, Max={stats[f'{name}__max']}]"

        print(f" {i:<3} | {name:<28} | {f_type:<7} | {f_risk:<9} | {f_desc}")
        if stat_str:
            print(f"     {' ':<28}   {' ':<7}   {' ':<9}   └─> Thực tế: {stat_str}")
    print("=" * 80 + "\n")


def search_features(bundles: dict, keyword: str):
    kw = keyword.lower()
    print("\n" + "=" * 80)
    print(f"🔎 KẾT QUẢ TÌM KIẾM CHO TỪ KHÓA: '{keyword}'")
    print("=" * 80)
    found = 0
    for key, b in bundles.items():
        b_name = b.get("name", key)
        for f in b.get("features", []):
            if kw in f["name"].lower() or kw in f.get("description", "").lower():
                found += 1
                print(f"• [{b.get('id', '-')}] {f['name']:<28} ({b_name})")
                print(f"    - Mô tả:   {f.get('description')}")
                print(f"    - Rủi ro:  {f.get('leakage_risk')}")
    print("-" * 80)
    print(f"Tìm thấy {found} thuộc tính phù hợp.")
    print("=" * 80 + "\n")


def main():
    parser = argparse.ArgumentParser(description="Trust-NIDS Feature Bundles CLI Explorer")
    parser.add_argument(
        "--bundle",
        type=str,
        help="Mã số bộ (1-8) hoặc mã tên (identity, volumetrics, temporal_rate, tcp_state, packet_geometry,...)"
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Hiển thị bảng tổng quan 8 bộ"
    )
    parser.add_argument(
        "--search",
        type=str,
        help="Tìm kiếm thuộc tính theo tên hoặc mô tả"
    )
    parser.add_argument(
        "--data-path",
        type=Path,
        default=Path("data/processed/nf-unsw-nb15-v2/NF-UNSW-NB15-v2.parquet"),
        help="Đường dẫn file parquet để trích xuất thống kê thực tế"
    )

    args = parser.parse_args()
    bundles = load_bundles_config()

    if args.search:
        search_features(bundles, args.search)
    elif args.bundle:
        target = args.bundle.strip().lower()
        found_key = None
        for key, b in bundles.items():
            if str(b.get("id")) == target or b.get("code", "").lower() == target or key.lower() == target:
                found_key = key
                break
        if found_key:
            show_bundle_detail(found_key, bundles[found_key], args.data_path)
        else:
            print(f"\n❌ Không tìm thấy bộ '{args.bundle}'. Vui lòng chọn số từ 1 đến 8 hoặc chạy --summary để xem mã.\n")
    else:
        show_summary(bundles)


if __name__ == "__main__":
    main()
