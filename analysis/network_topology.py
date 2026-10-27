#!/usr/bin/env python3
"""
analysis/network_topology.py
Deep Network Topology & Attack-Defense Interaction Profiler for Trust-NIDS.

Extracts:
1. IP Personas & Roles: Attackers, Victim Servers, Benign Clients, Infrastructure.
2. Bipartite Directed Interaction Matrix (Source IP -> Destination IP).
3. Attack Distribution Graph with Per-Attack Flow Counts & Payload Volumes.
4. Network Testbed Routing Topology (WAN -> Edge Router -> DMZ Server Farm).
5. Interactive Web Dashboard (HTML + SVG/Canvas) for visual graph inspection.
"""

import json
import sys
from pathlib import Path

# Force UTF-8 stdout
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import duckdb
import pandas as pd


def analyze_topology(parquet_path: Path, output_dir: Path):
    if not parquet_path.exists():
        raise FileNotFoundError(f"Parquet file not found: {parquet_path}")

    output_dir.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect(database=":memory:")
    con.execute(f"CREATE VIEW dataset AS SELECT * FROM read_parquet('{parquet_path.as_posix()}');")

    # 1. Profile All Unique IPs
    ip_query = """
    WITH src_stats AS (
        SELECT 
            IPV4_SRC_ADDR AS ip,
            COUNT(*) AS flows_as_src,
            SUM(CASE WHEN Label = 1 THEN 1 ELSE 0 END) AS attacks_sent,
            SUM(CASE WHEN Label = 0 THEN 1 ELSE 0 END) AS benign_sent,
            COUNT(DISTINCT IPV4_DST_ADDR) AS targets_contacted
        FROM dataset
        GROUP BY 1
    ),
    dst_stats AS (
        SELECT 
            IPV4_DST_ADDR AS ip,
            COUNT(*) AS flows_as_dst,
            SUM(CASE WHEN Label = 1 THEN 1 ELSE 0 END) AS attacks_received,
            SUM(CASE WHEN Label = 0 THEN 1 ELSE 0 END) AS benign_received,
            COUNT(DISTINCT IPV4_SRC_ADDR) AS sources_received_from
        FROM dataset
        GROUP BY 1
    )
    SELECT 
        COALESCE(s.ip, d.ip) AS ip,
        COALESCE(s.flows_as_src, 0) AS flows_as_src,
        COALESCE(s.attacks_sent, 0) AS attacks_sent,
        COALESCE(s.benign_sent, 0) AS benign_sent,
        COALESCE(s.targets_contacted, 0) AS targets_contacted,
        COALESCE(d.flows_as_dst, 0) AS flows_as_dst,
        COALESCE(d.attacks_received, 0) AS attacks_received,
        COALESCE(d.benign_received, 0) AS benign_received,
        COALESCE(d.sources_received_from, 0) AS sources_received_from,
        CASE
            WHEN COALESCE(s.attacks_sent, 0) > 0 THEN 'ATTACKER'
            WHEN COALESCE(d.attacks_received, 0) > 0 THEN 'VICTIM_SERVER'
            WHEN s.ip LIKE '59.166.%' THEN 'BENIGN_CLIENT'
            ELSE 'INFRASTRUCTURE'
        END AS role
    FROM src_stats s
    FULL OUTER JOIN dst_stats d ON s.ip = d.ip
    ORDER BY attacks_sent DESC, attacks_received DESC, flows_as_src DESC;
    """
    ip_profile_df = con.execute(ip_query).df()

    # 2. Extract Bipartite Traffic & Attack Edges
    edge_query = """
    SELECT 
        IPV4_SRC_ADDR AS source,
        IPV4_DST_ADDR AS target,
        COUNT(*) AS total_flows,
        SUM(CASE WHEN Label = 1 THEN 1 ELSE 0 END) AS attack_flows,
        SUM(CASE WHEN Label = 0 THEN 1 ELSE 0 END) AS benign_flows,
        ROUND(SUM(IN_BYTES) / (1024.0 * 1024.0), 2) AS total_in_mb,
        ROUND(SUM(OUT_BYTES) / (1024.0 * 1024.0), 2) AS total_out_mb,
        STRING_AGG(DISTINCT CASE WHEN Label = 1 THEN Attack ELSE NULL END, ', ') AS attack_types
    FROM dataset
    GROUP BY 1, 2
    ORDER BY attack_flows DESC, total_flows DESC;
    """
    edges_df = con.execute(edge_query).df()

    # 3. Attack types breakdown per (Source, Target)
    attack_details_query = """
    SELECT 
        IPV4_SRC_ADDR AS source,
        IPV4_DST_ADDR AS target,
        Attack,
        COUNT(*) AS count,
        ROUND(AVG(IN_BYTES), 1) AS avg_in_bytes,
        ROUND(AVG(FLOW_DURATION_MILLISECONDS), 1) AS avg_dur_ms
    FROM dataset
    WHERE Label = 1
    GROUP BY 1, 2, 3
    ORDER BY source, target, count DESC;
    """
    attack_details_df = con.execute(attack_details_query).df()

    # Save CSVs / JSON for downstream graph construction
    ip_profile_df.to_csv(output_dir / "ip_inventory.csv", index=False)
    edges_df.to_csv(output_dir / "traffic_edges.csv", index=False)

    # 4. Generate Markdown Topology Report
    md_report_path = output_dir / "NETWORK_TOPOLOGY_AUDIT.md"
    with open(md_report_path, "w", encoding="utf-8") as f:
        f.write("# Báo Cáo Phân Tích Cấu Trúc Đồ Thị & Tô-pô Mạng (Network Topology Audit)\n\n")
        f.write("> **Dự án**: Trust-NIDS Benchmark | **Bộ dữ liệu**: `NF-UNSW-NB15-v2`\n\n")
        
        f.write("## 1. Mô Hình Kiến Trúc Mạng Vật Lý & Định Tuyến (Reconstructed Network Architecture)\n\n")
        f.write("Dựa trên phân tích các dải mạng IPv4 (/24 Prefix) trong 2.39 triệu flows, kiến trúc testbed phòng thí nghiệm được phác họa như sau:\n\n")
        f.write("```text\n")
        f.write("+-----------------------------------------------------------------------------------------+\n")
        f.write("|                                  MÔ HÌNH MẠNG TESTBED                                   |\n")
        f.write("+-----------------------------------------------------------------------------------------+\n")
        f.write("                                                                                           \n")
        f.write("  [1] NGUỒN TẤN CÔNG (WAN/Internet)           [2] LƯU LƯỢNG SẠCH MÔ PHỎNG (IXIA Clients) \n")
        f.write("      Subnet: 175.45.176.0/24                     Subnet: 59.166.0.0/24                   \n")
        f.write("      - 175.45.176.0 (25.7k attacks)              - 59.166.0.0 (230k flows)               \n")
        f.write("      - 175.45.176.1 (27.5k attacks)              - 59.166.0.1 (230k flows)               \n")
        f.write("      - 175.45.176.2 (18.8k attacks)              - 59.166.0.2 (230k flows)               \n")
        f.write("      - 175.45.176.3 (23.0k attacks)              - 59.166.0.3 (228k flows)               \n")
        f.write("                                                  - 59.166.0.4 (230k flows)               \n")
        f.write("             \\                                            /                               \n")
        f.write("              \\                                          /                                \n")
        f.write("               +--------------------+-------------------+                                 \n")
        f.write("                                    |                                                     \n")
        f.write("                                    v                                                     \n")
        f.write("                      [EDGE ROUTER & FIREWALL GATEWAY]                                    \n")
        f.write("                       (Quản lý định tuyến WAN -> DMZ)                                    \n")
        f.write("                                    |                                                     \n")
        f.write("                                    v                                                     \n")
        f.write("                    [VÙNG MẠNG CHỦ NẠN NHÂN - DMZ SERVER FARM]                            \n")
        f.write("                            Subnet: 149.171.126.0/24                                      \n")
        f.write("                      (10 Máy chủ: 149.171.126.10 -> .19)                                 \n")
        f.write("               - Hứng chịu toàn bộ 95,053 cuộc tấn công (100%)                            \n")
        f.write("               - Đồng thời phục vụ 2.27 triệu kết nối người dùng sạch                     \n")
        f.write("+-----------------------------------------------------------------------------------------+\n")
        f.write("```\n\n")

        f.write("## 2. Thống Kê Phân Vai Địa Chỉ IP (IP Persona Inventory)\n\n")
        f.write(ip_profile_df.to_markdown(index=False))
        f.write("\n\n")

        f.write("## 3. Ma Trận Cạnh Tấn Công Chính (Top Malicious Traffic Edges)\n\n")
        attack_edges = edges_df[edges_df["attack_flows"] > 0].head(20)
        f.write(attack_edges.to_markdown(index=False))
        f.write("\n\n")

    print(f"[*] Generated Markdown topology report: {md_report_path}")

    # 5. Generate Standalone Interactive Bipartite Graph Visualization (HTML + JS)
    generate_interactive_html(
        ip_profile_df=ip_profile_df,
        edges_df=edges_df,
        attack_details_df=attack_details_df,
        output_file=output_dir / "topology_graph.html"
    )
    print(f"[*] Generated Interactive Visual Graph: {output_dir / 'topology_graph.html'}")


def generate_interactive_html(ip_profile_df, edges_df, attack_details_df, output_file: Path):
    """Generates a rich interactive SVG/Canvas graph visualization of bipartite network."""
    
    # Filter nodes for visual clarity:
    # Source nodes: 4 Attackers + 5 Benign clients + Top Internal
    # Target nodes: 10 DMZ Servers + Top Other
    src_nodes = ip_profile_df[ip_profile_df["flows_as_src"] > 0].copy()
    dst_nodes = ip_profile_df[ip_profile_df["flows_as_dst"] > 0].copy()

    # Build node data for frontend
    nodes_data = []
    for _, row in ip_profile_df.iterrows():
        nodes_data.append({
            "id": row["ip"],
            "role": row["role"],
            "flows_src": int(row["flows_as_src"]),
            "attacks_sent": int(row["attacks_sent"]),
            "benign_sent": int(row["benign_sent"]),
            "flows_dst": int(row["flows_as_dst"]),
            "attacks_recv": int(row["attacks_received"]),
            "benign_recv": int(row["benign_received"]),
            "targets": int(row["targets_contacted"])
        })

    # Build edges data
    edges_data = []
    for _, row in edges_df.iterrows():
        edges_data.append({
            "source": row["source"],
            "target": row["target"],
            "total_flows": int(row["total_flows"]),
            "attack_flows": int(row["attack_flows"]),
            "benign_flows": int(row["benign_flows"]),
            "in_mb": float(row["total_in_mb"]),
            "out_mb": float(row["total_out_mb"]),
            "attacks": str(row["attack_types"]) if pd.notna(row["attack_types"]) else ""
        })

    nodes_json = json.dumps(nodes_data)
    edges_json = json.dumps(edges_data)

    html_template = f"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Trust-NIDS: Sơ Đồ Đồ Thị Tấn Công & Phòng Thủ (Topology Graph)</title>
<style>
  :root {{
    --bg: #090d16;
    --card: #131c2e;
    --border: #22324e;
    --text: #e2e8f0;
    --muted: #64748b;
    --attacker: #ef4444;
    --victim: #3b82f6;
    --benign: #10b981;
    --router: #8b5cf6;
    --warning: #f59e0b;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    background: var(--bg);
    color: var(--text);
    overflow-x: hidden;
  }}
  .app-container {{ display: flex; height: 100vh; flex-direction: column; }}
  header {{
    background: #0d1527;
    border-bottom: 1px solid var(--border);
    padding: 1rem 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }}
  .title-group h1 {{ font-size: 1.3rem; color: #38bdf8; }}
  .title-group p {{ font-size: 0.85rem; color: var(--muted); }}
  .controls {{ display: flex; gap: 1rem; align-items: center; }}
  .btn {{
    background: var(--card);
    border: 1px solid var(--border);
    color: var(--text);
    padding: 0.4rem 0.8rem;
    border-radius: 6px;
    font-size: 0.85rem;
    cursor: pointer;
    transition: all 0.2s;
  }}
  .btn.active, .btn:hover {{
    background: #38bdf8;
    color: #000;
    border-color: #38bdf8;
    font-weight: 600;
  }}
  .main-area {{ display: flex; flex: 1; overflow: hidden; }}
  .graph-pane {{ flex: 1; position: relative; background: radial-gradient(circle at center, #111a2e 0%, #090d16 100%); }}
  #graphCanvas {{ width: 100%; height: 100%; display: block; }}
  .side-pane {{
    width: 380px;
    background: var(--card);
    border-left: 1px solid var(--border);
    padding: 1.5rem;
    overflow-y: auto;
  }}
  .card {{
    background: #0d1527;
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1rem;
    margin-bottom: 1.25rem;
  }}
  .card h3 {{ font-size: 0.95rem; color: #38bdf8; margin-bottom: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em; }}
  .stat-row {{ display: flex; justify-content: space-between; padding: 0.35rem 0; font-size: 0.85rem; border-bottom: 1px dashed #1e293b; }}
  .stat-label {{ color: var(--muted); }}
  .stat-val {{ font-weight: 600; }}
  .legend-item {{ display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem; font-size: 0.85rem; }}
  .dot {{ width: 12px; height: 12px; border-radius: 50%; display: inline-block; }}
  .dot-attacker {{ background: var(--attacker); box-shadow: 0 0 8px var(--attacker); }}
  .dot-victim {{ background: var(--victim); box-shadow: 0 0 8px var(--victim); }}
  .dot-benign {{ background: var(--benign); }}
  .dot-router {{ background: var(--router); }}
  .tooltip {{
    position: absolute;
    display: none;
    background: rgba(13, 21, 39, 0.95);
    border: 1px solid #38bdf8;
    border-radius: 8px;
    padding: 0.75rem 1rem;
    font-size: 0.85rem;
    pointer-events: none;
    z-index: 100;
    box-shadow: 0 10px 25px rgba(0,0,0,0.5);
  }}
</style>
</head>
<body>
<div class="app-container">
  <header>
    <div class="title-group">
      <h1>🌐 Trust-NIDS: Sơ Đồ Đồ Thị Tấn Công & Phòng Thủ Hai Phía (Bipartite Graph)</h1>
      <p>Trực quan hóa luồng kết nối Nguồn (Source IP) ➔ Đích (Destination IP) qua Cổng Biên (Edge Router)</p>
    </div>
    <div class="controls">
      <span>Chế độ hiển thị:</span>
      <button class="btn active" id="btnAll" onclick="setFilter('all')">Tất cả Luồng</button>
      <button class="btn" id="btnAttacks" onclick="setFilter('attacks')">🚨 Chỉ Tấn Công</button>
      <button class="btn" id="btnBenign" onclick="setFilter('benign')">✅ Chỉ Lưu Lượng Sạch</button>
    </div>
  </header>

  <div class="main-area">
    <div class="graph-pane">
      <canvas id="graphCanvas"></canvas>
      <div class="tooltip" id="tooltip"></div>
    </div>

    <div class="side-pane">
      <div class="card">
        <h3>🔍 Thông Tin Node Được Chọn</h3>
        <div id="nodeDetails">
          <p style="color: var(--muted); font-size: 0.85rem;">Rê chuột vào một địa chỉ IP hoặc đường nối (cạnh) để xem thông số chi tiết.</p>
        </div>
      </div>

      <div class="card">
        <h3>🗺️ Chú Giải & Phân Vùng Mạng</h3>
        <div class="legend-item">
          <span class="dot dot-attacker"></span>
          <span><b>Kẻ Tấn Công (Attackers)</b>: <code>175.45.176.0/24</code></span>
        </div>
        <div class="legend-item">
          <span class="dot dot-benign"></span>
          <span><b>Người Dùng Sạch (Clients)</b>: <code>59.166.0.0/24</code></span>
        </div>
        <div class="legend-item">
          <span class="dot dot-router"></span>
          <span><b>Cổng Biên (Edge Gateway)</b>: Router/Firewall</span>
        </div>
        <div class="legend-item">
          <span class="dot dot-victim"></span>
          <span><b>Server Nạn Nhân (DMZ)</b>: <code>149.171.126.0/24</code></span>
        </div>
      </div>

      <div class="card">
        <h3>📊 Phát Hiện Chiến Lược NIDS</h3>
        <div class="stat-row">
          <span class="stat-label">Tổng số IP nguồn:</span>
          <span class="stat-val">40 IPs</span>
        </div>
        <div class="stat-row">
          <span class="stat-label">Số IP phát động tấn công:</span>
          <span class="stat-val" style="color: var(--attacker);">Chỉ 4 IPs (100% đòn đánh)</span>
        </div>
        <div class="stat-row">
          <span class="stat-label">Số Server DMZ mục tiêu:</span>
          <span class="stat-val" style="color: var(--victim);">10 Servers (.10 ➔ .19)</span>
        </div>
        <div class="stat-row">
          <span class="stat-label">Các loại tấn công:</span>
          <span class="stat-val">9 lớp (DoS, Fuzzers,...)</span>
        </div>
      </div>
    </div>
  </div>
</div>

<script>
const nodesData = {nodes_json};
const edgesData = {edges_json};

let currentFilter = 'all'; // 'all', 'attacks', 'benign'
let hoveredNode = null;
let hoveredEdge = null;

const canvas = document.getElementById('graphCanvas');
const ctx = canvas.getContext('2d');
const tooltip = document.getElementById('tooltip');
const nodeDetails = document.getElementById('nodeDetails');

function resizeCanvas() {{
  canvas.width = canvas.parentElement.clientWidth;
  canvas.height = canvas.parentElement.clientHeight;
  layoutNodes();
  draw();
}}
window.addEventListener('resize', resizeCanvas);

// Position nodes into 3 columns: Left (Sources), Center (Router), Right (DMZ Targets)
const sourceNodes = [];
const targetNodes = [];
const routerNode = {{ id: "Edge Router / Gateway", role: "ROUTER", x: 0, y: 0, r: 24 }};

function layoutNodes() {{
  sourceNodes.length = 0;
  targetNodes.length = 0;

  // Filter top representative nodes for visualization
  const attackers = nodesData.filter(n => n.attacks_sent > 0);
  const benignClients = nodesData.filter(n => n.role === 'BENIGN_CLIENT').slice(0, 5);
  const victims = nodesData.filter(n => n.role === 'VICTIM_SERVER').slice(0, 10);

  const leftNodes = [...attackers, ...benignClients];
  const rightNodes = victims;

  const w = canvas.width;
  const h = canvas.height;

  // Left column (Sources)
  const leftX = w * 0.15;
  const leftStep = h / (leftNodes.length + 1);
  leftNodes.forEach((node, i) => {{
    node.x = leftX;
    node.y = leftStep * (i + 1);
    node.r = node.attacks_sent > 0 ? 14 : 10;
    sourceNodes.push(node);
  }});

  // Center (Router Gateway)
  routerNode.x = w * 0.50;
  routerNode.y = h * 0.50;

  // Right column (DMZ Targets)
  const rightX = w * 0.85;
  const rightStep = h / (rightNodes.length + 1);
  rightNodes.forEach((node, i) => {{
    node.x = rightX;
    node.y = rightStep * (i + 1);
    node.r = 13;
    targetNodes.push(node);
  }});
}}

function setFilter(filter) {{
  currentFilter = filter;
  document.querySelectorAll('.btn').forEach(b => b.classList.remove('active'));
  if (filter === 'all') document.getElementById('btnAll').classList.add('active');
  if (filter === 'attacks') document.getElementById('btnAttacks').classList.add('active');
  if (filter === 'benign') document.getElementById('btnBenign').classList.add('active');
  draw();
}}

function draw() {{
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // 1. Draw Edges
  edgesData.forEach(edge => {{
    const src = sourceNodes.find(n => n.id === edge.source);
    const tgt = targetNodes.find(n => n.id === edge.target);
    if (!src || !tgt) return;

    const isAttack = edge.attack_flows > 0;
    if (currentFilter === 'attacks' && !isAttack) return;
    if (currentFilter === 'benign' && isAttack) return;

    // Check hover
    const isHighlighted = (hoveredNode && (hoveredNode.id === src.id || hoveredNode.id === tgt.id));
    const isDimmed = hoveredNode && !isHighlighted;

    ctx.save();
    ctx.beginPath();
    // Route from Source -> Router -> Target
    ctx.moveTo(src.x, src.y);
    ctx.quadraticCurveTo(routerNode.x, (src.y + tgt.y) / 2, tgt.x, tgt.y);

    if (isAttack) {{
      ctx.strokeStyle = isHighlighted ? '#ff2222' : (isDimmed ? 'rgba(239, 68, 68, 0.08)' : 'rgba(239, 68, 68, 0.45)');
      ctx.lineWidth = isHighlighted ? 3.5 : Math.min(3, Math.max(1, edge.attack_flows / 3000));
    }} else {{
      ctx.strokeStyle = isHighlighted ? '#10b981' : (isDimmed ? 'rgba(16, 185, 129, 0.05)' : 'rgba(16, 185, 129, 0.25)');
      ctx.lineWidth = isHighlighted ? 2.5 : 1;
    }}
    ctx.stroke();
    ctx.restore();
  }});

  // 2. Draw Center Router
  ctx.save();
  ctx.beginPath();
  ctx.arc(routerNode.x, routerNode.y, routerNode.r, 0, Math.PI * 2);
  ctx.fillStyle = '#1e1b4b';
  ctx.fill();
  ctx.lineWidth = 3;
  ctx.strokeStyle = '#8b5cf6';
  ctx.stroke();

  ctx.fillStyle = '#fff';
  ctx.font = 'bold 11px sans-serif';
  ctx.textAlign = 'center';
  ctx.fillText('FIREWALL', routerNode.x, routerNode.y - 4);
  ctx.fillText('ROUTER', routerNode.x, routerNode.y + 10);
  ctx.restore();

  // 3. Draw Nodes (Sources & Targets)
  const allNodes = [...sourceNodes, ...targetNodes];
  allNodes.forEach(node => {{
    ctx.save();
    ctx.beginPath();
    ctx.arc(node.x, node.y, node.r, 0, Math.PI * 2);

    let color = '#64748b';
    if (node.role === 'ATTACKER') color = '#ef4444';
    else if (node.role === 'BENIGN_CLIENT') color = '#10b981';
    else if (node.role === 'VICTIM_SERVER') color = '#3b82f6';

    ctx.fillStyle = color;
    ctx.fill();

    if (hoveredNode && hoveredNode.id === node.id) {{
      ctx.lineWidth = 4;
      ctx.strokeStyle = '#ffffff';
      ctx.stroke();
    }} else {{
      ctx.lineWidth = 1.5;
      ctx.strokeStyle = 'rgba(255,255,255,0.3)';
      ctx.stroke();
    }}

    // Label
    ctx.fillStyle = '#f8fafc';
    ctx.font = '12px monospace';
    if (node.x < canvas.width * 0.5) {{
      ctx.textAlign = 'right';
      ctx.fillText(node.id, node.x - node.r - 8, node.y + 4);
    }} else {{
      ctx.textAlign = 'left';
      ctx.fillText(node.id, node.x + node.r + 8, node.y + 4);
    }}
    ctx.restore();
  }});
}}

// Mouse interaction
canvas.addEventListener('mousemove', e => {{
  const rect = canvas.getBoundingClientRect();
  const mx = e.clientX - rect.left;
  const my = e.clientY - rect.top;

  let foundNode = null;
  const allNodes = [...sourceNodes, ...targetNodes];
  for (const n of allNodes) {{
    const dist = Math.hypot(n.x - mx, n.y - my);
    if (dist <= n.r + 4) {{
      foundNode = n;
      break;
    }}
  }}

  if (foundNode !== hoveredNode) {{
    hoveredNode = foundNode;
    draw();
    updateTooltip(e, foundNode);
  }}
}});

function updateTooltip(e, node) {{
  if (!node) {{
    tooltip.style.display = 'none';
    return;
  }}

  let html = `<b>IP: ${{node.id}}</b><br>`;
  html += `Vai trò: <span style="color: ${{node.role==='ATTACKER'?'#ef4444':'#38bdf8'}}">${{node.role}}</span><br>`;
  if (node.flows_src > 0) {{
    html += `Flows gửi: ${{node.flows_src.toLocaleString()}}<br>`;
    html += `🚨 Tấn công phát động: <b style="color:#ef4444">${{node.attacks_sent.toLocaleString()}}</b><br>`;
    html += `✅ Lưu lượng sạch: ${{node.benign_sent.toLocaleString()}}<br>`;
    html += `Số mục tiêu tấn công: ${{node.targets}} servers<br>`;
  }}
  if (node.flows_dst > 0) {{
    html += `Flows nhận: ${{node.flows_dst.toLocaleString()}}<br>`;
    html += `🚨 Đòn tấn công hứng chịu: <b style="color:#ef4444">${{node.attacks_recv.toLocaleString()}}</b><br>`;
    html += `✅ Request bình thường nhận: ${{node.benign_recv.toLocaleString()}}<br>`;
  }}

  tooltip.innerHTML = html;
  tooltip.style.display = 'block';
  tooltip.style.left = (e.clientX + 15) + 'px';
  tooltip.style.top = (e.clientY + 15) + 'px';

  // Update side-pane
  nodeDetails.innerHTML = html;
}}

// Initial load
setTimeout(() => {{
  resizeCanvas();
}}, 100);
</script>
</body>
</html>
"""
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_template)


if __name__ == "__main__":
    analyze_topology(
        parquet_path=Path("data/processed/nf-unsw-nb15-v2/NF-UNSW-NB15-v2.parquet"),
        output_dir=Path("analysis/reports")
    )
