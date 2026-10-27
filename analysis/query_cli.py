#!/usr/bin/env python3
"""
analysis/query_cli.py
High-speed DuckDB SQL Analytics Engine for Trust-NIDS Parquet Datasets.

Allows querying millions of network flows in milliseconds directly from disk
without loading the entire dataset into RAM.
"""

import argparse
import sys
from pathlib import Path

# Force UTF-8 stdout for Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import duckdb


def get_connection(parquet_path: Path):
    if not parquet_path.exists():
        raise FileNotFoundError(f"Parquet file not found: {parquet_path}")
    con = duckdb.connect(database=":memory:")
    # Register view pointing directly to parquet file on disk
    con.execute(f"CREATE VIEW dataset AS SELECT * FROM read_parquet('{parquet_path.as_posix()}');")
    return con


def show_summary(con):
    print("\n" + "=" * 75)
    print("🚀 INSTANT DATASET PROFILE SUMMARY (via DuckDB OLAP Engine)")
    print("=" * 75)
    query = """
    SELECT 
        COUNT(*) AS total_flows,
        COUNT(DISTINCT IPV4_SRC_ADDR) AS unique_src_ips,
        COUNT(DISTINCT IPV4_DST_ADDR) AS unique_dst_ips,
        COUNT(DISTINCT L4_DST_PORT) AS unique_dst_ports,
        SUM(CASE WHEN Label = 1 THEN 1 ELSE 0 END) AS attack_flows,
        SUM(CASE WHEN Label = 0 THEN 1 ELSE 0 END) AS benign_flows,
        ROUND(AVG(FLOW_DURATION_MILLISECONDS), 2) AS avg_duration_ms,
        ROUND(AVG(IN_BYTES), 2) AS avg_in_bytes,
        ROUND(AVG(OUT_BYTES), 2) AS avg_out_bytes
    FROM dataset;
    """
    df = con.execute(query).df()
    print(df.T.to_string(header=False))
    print("=" * 75 + "\n")


def show_attacks(con):
    print("\n" + "=" * 75)
    print("🎯 ATTACK BEHAVIOR PROFILE MATRIX")
    print("=" * 75)
    query = """
    SELECT 
        Attack,
        COUNT(*) AS flow_count,
        ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM dataset), 2) AS pct_of_total,
        ROUND(AVG(IN_BYTES), 1) AS avg_in_bytes,
        ROUND(AVG(OUT_BYTES), 1) AS avg_out_bytes,
        ROUND(AVG(IN_PKTS), 1) AS avg_in_pkts,
        ROUND(AVG(OUT_PKTS), 1) AS avg_out_pkts,
        ROUND(AVG(FLOW_DURATION_MILLISECONDS), 1) AS avg_dur_ms
    FROM dataset
    GROUP BY Attack
    ORDER BY flow_count DESC;
    """
    df = con.execute(query).df()
    print(df.to_string(index=False))
    print("=" * 75 + "\n")


def show_top_talkers(con):
    print("\n" + "=" * 75)
    print("🌐 TOP 10 IP TALKERS & MALICIOUS ACTIVITY RATIO")
    print("=" * 75)
    query = """
    SELECT 
        IPV4_SRC_ADDR,
        COUNT(*) AS total_flows,
        ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM dataset), 2) AS flow_share_pct,
        SUM(CASE WHEN Label = 1 THEN 1 ELSE 0 END) AS attacks_originated,
        SUM(CASE WHEN Label = 0 THEN 1 ELSE 0 END) AS benign_originated,
        COUNT(DISTINCT IPV4_DST_ADDR) AS distinct_targets_contacted
    FROM dataset
    GROUP BY IPV4_SRC_ADDR
    ORDER BY total_flows DESC
    LIMIT 10;
    """
    df = con.execute(query).df()
    print(df.to_string(index=False))
    print("=" * 75 + "\n")


def run_custom_sql(con, sql: str):
    print(f"\n[Executing SQL Query]: {sql}\n")
    try:
        df = con.execute(sql).df()
        print(df.to_string(index=False))
        print(f"\n({len(df)} rows returned)\n")
    except Exception as e:
        print(f"SQL Error: {e}\n")


def interactive_repl(con):
    print("\n" + "=" * 75)
    print("💡 TRUST-NIDS SQL INTERACTIVE REPL")
    print("Table name is: 'dataset'. Type SQL queries or 'exit' / 'quit' to return.")
    print("Example: SELECT Attack, count(*) FROM dataset GROUP BY 1;")
    print("=" * 75 + "\n")
    while True:
        try:
            line = input("TrustNIDS-SQL> ").strip()
            if not line:
                continue
            if line.lower() in ("exit", "quit", "q"):
                break
            run_custom_sql(con, line)
        except (KeyboardInterrupt, EOFError):
            print()
            break


def main():
    parser = argparse.ArgumentParser(description="Trust-NIDS DuckDB High-Speed Analytics Engine")
    parser.add_argument(
        "--data-path",
        type=Path,
        default=Path("data/processed/nf-unsw-nb15-v2/NF-UNSW-NB15-v2.parquet"),
        help="Path to processed parquet file"
    )
    parser.add_argument("--summary", action="store_true", help="Show instant high-level summary")
    parser.add_argument("--attacks", action="store_true", help="Show detailed attack behavior profile")
    parser.add_argument("--top-talkers", action="store_true", help="Show top talker IPs and attack ratios")
    parser.add_argument("--sql", type=str, help="Run a custom SQL query against the 'dataset' view")
    parser.add_argument("-i", "--interactive", action="store_true", help="Launch interactive SQL REPL")

    args = parser.parse_args()

    con = get_connection(args.data_path)

    if args.sql:
        run_custom_sql(con, args.sql)
    elif args.attacks:
        show_attacks(con)
    elif args.top_talkers:
        show_top_talkers(con)
    elif args.interactive:
        interactive_repl(con)
    else:
        # Default: show summary and attacks
        show_summary(con)
        show_attacks(con)


if __name__ == "__main__":
    main()
