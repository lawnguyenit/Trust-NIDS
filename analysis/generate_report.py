#!/usr/bin/env python3
"""
analysis/generate_report.py
Generates a comprehensive Markdown audit report and a rich standalone HTML dashboard
for any Trust-NIDS Parquet dataset.
"""

import json
import sys
from pathlib import Path

# Force UTF-8 stdout
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import duckdb
import pandas as pd


def generate_audit_reports(parquet_path: Path, output_dir: Path):
    if not parquet_path.exists():
        raise FileNotFoundError(f"Parquet file not found: {parquet_path}")

    output_dir.mkdir(parents=True, exist_ok=True)
    dict_path = Path("analysis/feature_dictionary.json")
    with open(dict_path, "r", encoding="utf-8") as f:
        feature_dict = json.load(f)

    con = duckdb.connect(database=":memory:")
    con.execute(f"CREATE VIEW dataset AS SELECT * FROM read_parquet('{parquet_path.as_posix()}');")

    # 1. High-level KPIs
    kpi_query = """
    SELECT 
        COUNT(*) AS total_flows,
        COUNT(DISTINCT IPV4_SRC_ADDR) AS src_ips,
        COUNT(DISTINCT IPV4_DST_ADDR) AS dst_ips,
        COUNT(DISTINCT L4_DST_PORT) AS dst_ports,
        SUM(CASE WHEN Label = 1 THEN 1 ELSE 0 END) AS attack_flows,
        SUM(CASE WHEN Label = 0 THEN 1 ELSE 0 END) AS benign_flows,
        ROUND(SUM(CASE WHEN Label = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS attack_pct,
        ROUND(AVG(FLOW_DURATION_MILLISECONDS), 1) AS avg_duration_ms,
        ROUND(AVG(IN_BYTES), 1) AS avg_in_bytes,
        ROUND(AVG(OUT_BYTES), 1) AS avg_out_bytes
    FROM dataset;
    """
    kpis = con.execute(kpi_query).df().iloc[0].to_dict()

    # 2. Attack Breakdown
    attack_query = """
    SELECT 
        Attack,
        COUNT(*) AS count,
        ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM dataset), 2) AS pct,
        ROUND(AVG(IN_BYTES), 1) AS avg_in_bytes,
        ROUND(AVG(OUT_BYTES), 1) AS avg_out_bytes,
        ROUND(AVG(IN_PKTS), 1) AS avg_in_pkts,
        ROUND(AVG(OUT_PKTS), 1) AS avg_out_pkts,
        ROUND(AVG(FLOW_DURATION_MILLISECONDS), 1) AS avg_dur_ms
    FROM dataset
    GROUP BY Attack
    ORDER BY count DESC;
    """
    attacks_df = con.execute(attack_query).df()

    # 3. Top Talkers
    talkers_query = """
    SELECT 
        IPV4_SRC_ADDR,
        COUNT(*) AS flows,
        ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM dataset), 2) AS pct,
        SUM(CASE WHEN Label = 1 THEN 1 ELSE 0 END) AS attacks,
        SUM(CASE WHEN Label = 0 THEN 1 ELSE 0 END) AS benign,
        COUNT(DISTINCT IPV4_DST_ADDR) AS distinct_targets
    FROM dataset
    GROUP BY IPV4_SRC_ADDR
    ORDER BY flows DESC
    LIMIT 10;
    """
    talkers_df = con.execute(talkers_query).df()

    # 4. Protocols
    proto_query = """
    SELECT 
        CASE 
            WHEN PROTOCOL = 6 THEN 'TCP (6)'
            WHEN PROTOCOL = 17 THEN 'UDP (17)'
            WHEN PROTOCOL = 1 THEN 'ICMP (1)'
            ELSE 'Proto-' || CAST(PROTOCOL AS VARCHAR)
        END AS protocol_name,
        COUNT(*) AS flows,
        ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM dataset), 2) AS pct,
        SUM(CASE WHEN Label = 1 THEN 1 ELSE 0 END) AS attacks
    FROM dataset
    GROUP BY PROTOCOL
    ORDER BY flows DESC;
    """
    proto_df = con.execute(proto_query).df()

    # ==========================
    # GENERATE MARKDOWN REPORT
    # ==========================
    md_lines = [
        f"# Trust-NIDS Data Audit Report: `{parquet_path.stem}`\n",
        f"> **Tự động sinh bởi DuckDB OLAP Engine vào lúc {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}**\n",
        "## 1. Chỉ số Tổng quan (High-Level KPIs)\n",
        f"- **Tổng số flows**: `{int(kpis['total_flows']):,}`",
        f"- **Lưu lượng sạch (Benign)**: `{int(kpis['benign_flows']):,}` ({100 - kpis['attack_pct']:.2f}%)",
        f"- **Lưu lượng tấn công (Attack)**: `{int(kpis['attack_flows']):,}` ({kpis['attack_pct']:.2f}%)",
        f"- **Tổng số IP Nguồn duy nhất**: `{int(kpis['src_ips'])}`",
        f"- **Tổng số IP Đích duy nhất**: `{int(kpis['dst_ips'])}`",
        f"- **Thời lượng flow trung bình**: `{kpis['avg_duration_ms']:.1f} ms`",
        f"- **Bytes vào / ra trung bình**: `{kpis['avg_in_bytes']} B / {kpis['avg_out_bytes']} B`\n",
        "## 2. Phân bố các Loại Tấn công (Attack Behavior Matrix)\n",
        attacks_df.to_markdown(index=False),
        "\n## 3. Top Talkers (10 IP Nguồn Chiếm Lưu Lượng Lớn Nhất)\n",
        talkers_df.to_markdown(index=False),
        "\n## 4. Phân bố Giao thức Mạng (Protocols)\n",
        proto_df.to_markdown(index=False),
        "\n## 5. Từ điển 45 Đặc trưng NetFlow v9 & Cảnh báo Rò rỉ (Data Leakage Risk)\n",
        "| Tên Cột | Phân loại | Ý nghĩa mạng | Mức độ rủi ro rò rỉ (Leakage Risk) |",
        "| :--- | :--- | :--- | :--- |"
    ]
    for col, meta in feature_dict.items():
        md_lines.append(f"| `{col}` | {meta['category']} | {meta['description']} | **{meta['leakage_risk']}** |")

    md_report_path = output_dir / f"AUDIT_{parquet_path.stem}.md"
    with open(md_report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))
    print(f"[*] Generated Markdown report: {md_report_path}")

    # ==========================
    # GENERATE HTML DASHBOARD
    # ==========================
    html_content = f"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Trust-NIDS Audit Report - {parquet_path.stem}</title>
<style>
  :root {{
    --bg: #0f172a;
    --card: #1e293b;
    --border: #334155;
    --text: #f8fafc;
    --muted: #94a3b8;
    --accent: #38bdf8;
    --danger: #f87171;
    --success: #4ade80;
    --warning: #fbbf24;
  }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    background-color: var(--bg);
    color: var(--text);
    margin: 0;
    padding: 2rem;
    line-height: 1.6;
  }}
  .container {{ max-width: 1200px; margin: 0 auto; }}
  h1, h2, h3 {{ color: var(--accent); }}
  .header {{ border-bottom: 1px solid var(--border); padding-bottom: 1rem; margin-bottom: 2rem; }}
  .kpi-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 1.5rem;
    margin-bottom: 2.5rem;
  }}
  .kpi-card {{
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1.25rem;
  }}
  .kpi-title {{ font-size: 0.85rem; color: var(--muted); text-transform: uppercase; letter-spacing: 0.05em; }}
  .kpi-val {{ font-size: 1.75rem; font-weight: bold; margin-top: 0.5rem; }}
  .card {{
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1.5rem;
    margin-bottom: 2.5rem;
    overflow-x: auto;
  }}
  table {{ width: 100%; border-collapse: collapse; margin-top: 1rem; }}
  th, td {{ padding: 0.75rem 1rem; text-align: left; border-bottom: 1px solid var(--border); }}
  th {{ background: #0b1120; color: var(--muted); font-size: 0.85rem; }}
  tr:hover {{ background: rgba(56, 189, 248, 0.05); }}
  .badge {{ display: inline-block; padding: 0.2rem 0.5rem; border-radius: 4px; font-size: 0.8rem; font-weight: 600; }}
  .badge-danger {{ background: rgba(248, 113, 113, 0.2); color: var(--danger); }}
  .badge-safe {{ background: rgba(74, 222, 128, 0.2); color: var(--success); }}
  .badge-warning {{ background: rgba(251, 191, 36, 0.2); color: var(--warning); }}
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <h1>🛡️ Trust-NIDS Benchmark: Exploratory Data Audit</h1>
    <p style="color: var(--muted);">Báo cáo thẩm định dữ liệu mạng chuyên sâu cho tập tin <code>{parquet_path.name}</code></p>
  </div>

  <div class="kpi-grid">
    <div class="kpi-card">
      <div class="kpi-title">Tổng số Flows Mạng</div>
      <div class="kpi-val">{int(kpis['total_flows']):,}</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-title">Tỷ lệ Tấn công (Attack)</div>
      <div class="kpi-val" style="color: var(--danger);">{kpis['attack_pct']:.2f}%</div>
      <div style="font-size: 0.8rem; color: var(--muted);">{int(kpis['attack_flows']):,} flows</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-title">Số IP Nguồn (Nodes)</div>
      <div class="kpi-val" style="color: var(--warning);">{int(kpis['src_ips'])} IPs</div>
      <div style="font-size: 0.8rem; color: var(--muted);">Nguy cơ Identity Leakage cao</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-title">Thời lượng Flow TB</div>
      <div class="kpi-val">{kpis['avg_duration_ms']:.1f} ms</div>
    </div>
  </div>

  <div class="card">
    <h2>🎯 1. Phân bố Hành vi Tấn công (Attack Breakdown)</h2>
    {attacks_df.to_html(classes='table', index=False)}
  </div>

  <div class="card">
    <h2>🌐 2. Top Talkers: Phân bố Lưu lượng theo IP Nguồn</h2>
    {talkers_df.to_html(classes='table', index=False)}
  </div>

  <div class="card">
    <h2>📡 3. Phân bố Giao thức Tầng Vận chuyển</h2>
    {proto_df.to_html(classes='table', index=False)}
  </div>

  <div class="card">
    <h2>📖 4. Từ điển 45 Đặc trưng NetFlow v9 & Đánh giá Rò rỉ Dữ liệu</h2>
    <table>
      <thead>
        <tr>
          <th>Tên Đặc Trưng</th>
          <th>Phân Loại</th>
          <th>Ý Nghĩa Mạng Máy Tính</th>
          <th>Rủi Ro Rò Rỉ (Leakage Risk)</th>
        </tr>
      </thead>
      <tbody>
        {"".join([f'''<tr>
          <td><code>{col}</code></td>
          <td>{meta['category']}</td>
          <td>{meta['description']}</td>
          <td><span class="badge {'badge-danger' if 'CRITICAL' in meta['leakage_risk'] else ('badge-warning' if 'MEDIUM' in meta['leakage_risk'] or 'HIGH' in meta['leakage_risk'] else 'badge-safe')}">{meta['leakage_risk']}</span></td>
        </tr>''' for col, meta in feature_dict.items()])}
      </tbody>
    </table>
  </div>
</div>
</body>
</html>
"""
    html_report_path = output_dir / f"audit_{parquet_path.stem.lower()}.html"
    with open(html_report_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"[*] Generated HTML Dashboard: {html_report_path}")


if __name__ == "__main__":
    generate_audit_reports(
        parquet_path=Path("data/processed/nf-unsw-nb15-v2/NF-UNSW-NB15-v2.parquet"),
        output_dir=Path("analysis/reports")
    )
