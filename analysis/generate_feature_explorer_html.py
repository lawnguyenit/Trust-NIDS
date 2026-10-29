#!/usr/bin/env python3
"""
analysis/generate_feature_explorer_html.py
Builds the standalone interactive Feature Explorer HTML application.
"""

import json
from pathlib import Path
import yaml
import duckdb


def build_explorer_html(config_path: Path, parquet_path: Path, output_path: Path):
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    bundles = config.get("bundles", {})

    con = duckdb.connect(":memory:")
    # Pull stats from parquet
    all_f_names = []
    for b in bundles.values():
        all_f_names.extend([f["name"] for f in b["features"]])

    query_parts = []
    for f in all_f_names:
        if f in ("IPV4_SRC_ADDR", "IPV4_DST_ADDR", "Attack"):
            query_parts.append(f"COUNT(DISTINCT {f}) AS {f}__distinct")
        else:
            query_parts.append(f"MIN({f}) AS {f}__min, ROUND(AVG({f}), 1) AS {f}__avg, MAX({f}) AS {f}__max")
    
    q = f"SELECT {', '.join(query_parts)} FROM read_parquet('{parquet_path.as_posix()}');"
    stats_dict = con.execute(q).df().iloc[0].to_dict()

    # Enrich bundles with live stats
    bundles_enriched = []
    for b_key, b in bundles.items():
        enriched_features = []
        for f in b["features"]:
            name = f["name"]
            stat_info = {}
            if name in ("IPV4_SRC_ADDR", "IPV4_DST_ADDR", "Attack"):
                stat_info["type"] = "categorical"
                stat_info["distinct"] = int(stats_dict.get(f"{name}__distinct", 0))
            else:
                stat_info["type"] = "numeric"
                stat_info["min"] = float(stats_dict.get(f"{name}__min", 0))
                stat_info["avg"] = float(stats_dict.get(f"{name}__avg", 0))
                stat_info["max"] = float(stats_dict.get(f"{name}__max", 0))
            
            enriched_features.append({
                "name": name,
                "type": f.get("type", "int"),
                "description": f.get("description", ""),
                "leakage_risk": f.get("leakage_risk", "SAFE"),
                "stats": stat_info
            })

        bundles_enriched.append({
            "id": b["id"],
            "code": b["code"],
            "name": b["name"],
            "description": b["description"],
            "leakage_risk": b["leakage_risk"],
            "action": b.get("recommended_action", ""),
            "features": enriched_features
        })

    bundles_json = json.dumps(bundles_enriched, ensure_ascii=False)

    html_content = f"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Trust-NIDS: 8 Bộ Thuộc Tính NetFlow (Feature Explorer)</title>
<style>
  :root {{
    --bg: #0b1120;
    --card: #131d33;
    --card-hover: #1c2a47;
    --border: #223455;
    --text: #f1f5f9;
    --muted: #94a3b8;
    --accent: #38bdf8;
    --critical: #ef4444;
    --high: #f97316;
    --medium: #f59e0b;
    --safe: #10b981;
    --target: #a855f7;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    background-color: var(--bg);
    color: var(--text);
    padding: 2rem;
    line-height: 1.6;
  }}
  .container {{ max-width: 1280px; margin: 0 auto; }}
  header {{
    margin-bottom: 2rem;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid var(--border);
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 1rem;
  }}
  .title-group h1 {{ font-size: 1.6rem; color: var(--accent); margin-bottom: 0.3rem; }}
  .title-group p {{ color: var(--muted); font-size: 0.95rem; }}
  .search-box {{
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 0.6rem 1rem;
    color: var(--text);
    font-size: 0.95rem;
    width: 320px;
    outline: none;
    transition: all 0.2s;
  }}
  .search-box:focus {{ border-color: var(--accent); box-shadow: 0 0 10px rgba(56, 189, 248, 0.25); }}

  /* Grid of 8 Bundles */
  .bundle-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 1.25rem;
    margin-bottom: 2.5rem;
  }}
  .bundle-card {{
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1.25rem;
    cursor: pointer;
    transition: all 0.2s ease-in-out;
    position: relative;
    overflow: hidden;
  }}
  .bundle-card:hover {{
    background: var(--card-hover);
    transform: translateY(-2px);
    border-color: var(--accent);
  }}
  .bundle-card.active {{
    border-color: var(--accent);
    background: #182846;
    box-shadow: 0 0 15px rgba(56, 189, 248, 0.2);
  }}
  .bundle-card.active::before {{
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 4px;
    background: var(--accent);
  }}
  .bundle-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.5rem;
  }}
  .bundle-id {{
    font-size: 0.8rem;
    font-weight: 700;
    background: rgba(56, 189, 248, 0.15);
    color: var(--accent);
    padding: 0.2rem 0.5rem;
    border-radius: 4px;
  }}
  .bundle-count {{
    font-size: 0.8rem;
    color: var(--muted);
  }}
  .bundle-name {{
    font-size: 1.05rem;
    font-weight: 600;
    color: #fff;
    margin-bottom: 0.5rem;
  }}
  .bundle-desc {{
    font-size: 0.85rem;
    color: var(--muted);
    line-height: 1.4;
  }}

  /* Detail Panel */
  .detail-section {{
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1.75rem;
    margin-top: 1rem;
  }}
  .detail-header {{
    margin-bottom: 1.5rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid var(--border);
  }}
  .detail-title {{ font-size: 1.3rem; color: var(--accent); margin-bottom: 0.5rem; }}
  .detail-meta {{ display: flex; gap: 1.5rem; font-size: 0.85rem; color: var(--muted); flex-wrap: wrap; }}
  .detail-meta span b {{ color: var(--text); }}

  /* Feature Table */
  table {{ width: 100%; border-collapse: collapse; margin-top: 1rem; }}
  th, td {{ padding: 0.85rem 1rem; text-align: left; border-bottom: 1px solid var(--border); font-size: 0.9rem; }}
  th {{ background: #080d1a; color: var(--muted); font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em; }}
  tr:hover {{ background: rgba(56, 189, 248, 0.04); }}
  .col-name {{ font-family: monospace; font-weight: 600; color: #38bdf8; font-size: 0.95rem; }}
  .badge {{
    display: inline-block;
    padding: 0.2rem 0.55rem;
    border-radius: 4px;
    font-size: 0.75rem;
    font-weight: 700;
  }}
  .badge-CRITICAL {{ background: rgba(239, 68, 68, 0.2); color: var(--critical); border: 1px solid rgba(239, 68, 68, 0.4); }}
  .badge-HIGH {{ background: rgba(249, 115, 22, 0.2); color: var(--high); border: 1px solid rgba(249, 115, 22, 0.4); }}
  .badge-MEDIUM {{ background: rgba(245, 158, 11, 0.2); color: var(--medium); border: 1px solid rgba(245, 158, 11, 0.4); }}
  .badge-SAFE {{ background: rgba(16, 185, 129, 0.2); color: var(--safe); border: 1px solid rgba(16, 185, 129, 0.4); }}
  .badge-TARGET {{ background: rgba(168, 85, 247, 0.2); color: var(--target); border: 1px solid rgba(168, 85, 247, 0.4); }}
  .stat-pill {{
    display: inline-block;
    background: #080d1a;
    border: 1px solid var(--border);
    padding: 0.2rem 0.6rem;
    border-radius: 4px;
    font-size: 0.8rem;
    color: var(--muted);
    margin-top: 0.3rem;
  }}
</style>
</head>
<body>
<div class="container">
  <header>
    <div class="title-group">
      <h1>🗂️ Phân Rã 45 Thuộc Tính NetFlow Thành 8 Bộ Chức Năng</h1>
      <p>Bấm chọn từng Bộ để xem chi tiết bên trong, hoặc gõ từ khóa tìm kiếm nhanh.</p>
    </div>
    <input type="text" id="searchBox" class="search-box" placeholder="🔍 Tìm tên cột, ví dụ: tcp, bytes, port..." oninput="handleSearch()">
  </header>

  <!-- 8 Cards Grid -->
  <div class="bundle-grid" id="bundleGrid"></div>

  <!-- Detail Panel -->
  <div class="detail-section" id="detailSection">
    <div class="detail-header">
      <h2 class="detail-title" id="bundleTitle">Đang nạp...</h2>
      <div class="detail-meta">
        <span>Mô tả: <b id="bundleDesc">-</b></span>
        <span>Rủi ro rò rỉ: <b id="bundleRisk">-</b></span>
        <span>Khuyến nghị xử lý: <b id="bundleAction">-</b></span>
      </div>
    </div>
    <table id="featureTable">
      <thead>
        <tr>
          <th>Tên Thuộc Tính</th>
          <th>Kiểu</th>
          <th>Rủi Ro Rò Rỉ</th>
          <th>Ý Nghĩa Vật Lý / Mạng Máy Tính</th>
          <th>Thống Kê Thực Tế (Dataset: 2.39M flows)</th>
        </tr>
      </thead>
      <tbody id="featureTbody"></tbody>
    </table>
  </div>
</div>

<script>
const bundlesData = {bundles_json};
let selectedBundleId = 1;

function renderBundleCards() {{
  const grid = document.getElementById('bundleGrid');
  grid.innerHTML = '';
  bundlesData.forEach(b => {{
    const card = document.createElement('div');
    card.className = `bundle-card ${{b.id === selectedBundleId ? 'active' : ''}}`;
    card.onclick = () => selectBundle(b.id);
    card.innerHTML = `
      <div class="bundle-header">
        <span class="bundle-id">BỘ ${{b.id}}</span>
        <span class="bundle-count">${{b.features.length}} trường</span>
      </div>
      <div class="bundle-name">${{b.name}}</div>
      <div class="bundle-desc">${{b.description}}</div>
    `;
    grid.appendChild(card);
  }});
}}

function selectBundle(id) {{
  selectedBundleId = id;
  renderBundleCards();
  renderBundleDetail();
}}

function renderBundleDetail() {{
  const bundle = bundlesData.find(b => b.id === selectedBundleId);
  if (!bundle) return;

  document.getElementById('bundleTitle').textContent = `BỘ ${{bundle.id}}: ${{bundle.name}} (${{bundle.features.length}} thuộc tính)`;
  document.getElementById('bundleDesc').textContent = bundle.description;
  document.getElementById('bundleRisk').innerHTML = `<span class="badge badge-${{bundle.leakage_risk}}">${{bundle.leakage_risk}}</span>`;
  document.getElementById('bundleAction').textContent = bundle.action;

  const tbody = document.getElementById('featureTbody');
  tbody.innerHTML = '';

  bundle.features.forEach(f => {{
    let statHtml = '';
    if (f.stats.type === 'categorical') {{
      statHtml = `<span class="stat-pill">Duy nhất: <b>${{f.stats.distinct.toLocaleString()}}</b> giá trị</span>`;
    }} else {{
      statHtml = `<span class="stat-pill">Min: <b>${{f.stats.min.toLocaleString()}}</b> | Avg: <b>${{f.stats.avg.toLocaleString()}}</b> | Max: <b>${{f.stats.max.toLocaleString()}}</b></span>`;
    }}

    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td class="col-name">${{f.name}}</td>
      <td><code>${{f.type}}</code></td>
      <td><span class="badge badge-${{f.leakage_risk}}">${{f.leakage_risk}}</span></td>
      <td>${{f.description}}</td>
      <td>${{statHtml}}</td>
    `;
    tbody.appendChild(tr);
  }});
}}

function handleSearch() {{
  const kw = document.getElementById('searchBox').value.trim().toLowerCase();
  if (!kw) {{
    renderBundleCards();
    renderBundleDetail();
    return;
  }}

  // If searching, show all matching features across all bundles
  document.getElementById('bundleTitle').textContent = `🔎 Kết Quả Tìm Kiếm Cho: "${{kw}}"`;
  document.getElementById('bundleDesc').textContent = "Tìm thấy trên toàn bộ 45 thuộc tính của 8 bộ";
  document.getElementById('bundleRisk').textContent = "Tùy thuộc tính";
  document.getElementById('bundleAction').textContent = "Lọc trực tiếp";

  const tbody = document.getElementById('featureTbody');
  tbody.innerHTML = '';
  let matchCount = 0;

  bundlesData.forEach(b => {{
    b.features.forEach(f => {{
      if (f.name.toLowerCase().includes(kw) || f.description.toLowerCase().includes(kw)) {{
        matchCount++;
        let statHtml = '';
        if (f.stats.type === 'categorical') {{
          statHtml = `<span class="stat-pill">Duy nhất: <b>${{f.stats.distinct.toLocaleString()}}</b></span>`;
        }} else {{
          statHtml = `<span class="stat-pill">Min: ${{f.stats.min}} | Avg: ${{f.stats.avg}} | Max: ${{f.stats.max}}</span>`;
        }}
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td class="col-name">${{f.name}} <span style="font-size:0.75rem; color:var(--muted); font-weight:normal;">[Bộ ${{b.id}}]</span></td>
          <td><code>${{f.type}}</code></td>
          <td><span class="badge badge-${{f.leakage_risk}}">${{f.leakage_risk}}</span></td>
          <td>${{f.description}}</td>
          <td>${{statHtml}}</td>
        `;
        tbody.appendChild(tr);
      }}
    }});
  }});

  if (matchCount === 0) {{
    tbody.innerHTML = '<tr><td colspan="5" style="text-align:center; color:var(--muted); padding:2rem;">Không tìm thấy thuộc tính nào phù hợp với từ khóa.</td></tr>';
  }}
}}

// Initial render
renderBundleCards();
renderBundleDetail();
</script>
</body>
</html>
"""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"[*] Generated interactive Feature Explorer HTML: {output_path}")


if __name__ == "__main__":
    build_explorer_html(
        config_path=Path("configs/feature_bundles.yaml"),
        parquet_path=Path("data/processed/nf-unsw-nb15-v2/NF-UNSW-NB15-v2.parquet"),
        output_path=Path("analysis/reports/feature_explorer.html")
    )
