import os
import json
import pandas as pd

output_dir = r'd:\Analisis data Financial Sumatera Selatan\processed_data'
html_file = r'd:\Analisis data Financial Sumatera Selatan\dashboard.html'

df_pop = pd.read_csv(os.path.join(output_dir, 'populasi_bersih_2019_2026.csv'))
df_labor = pd.read_csv(os.path.join(output_dir, 'ketenagakerjaan_bersih_2019_2025.csv'))
df_nc = pd.read_csv(os.path.join(output_dir, 'nikah_cerai_bersih_2019_2025.csv'))

df_inf = pd.read_csv(os.path.join(output_dir, 'pendapatan_informal_2019_2025.csv'))
df_imk = pd.read_csv(os.path.join(output_dir, 'perusahaan_imk_2019_2022.csv'))
df_murid = pd.read_csv(os.path.join(output_dir, 'jumlah_murid_2019_2024.csv'))
df_inv = pd.read_csv(os.path.join(output_dir, 'investasi_perusahaan_sumsel.csv'))

pop_json = df_pop.to_dict(orient='records')
labor_json = df_labor.to_dict(orient='records')
nc_json = df_nc.to_dict(orient='records')
inf_json = df_inf.to_dict(orient='records')
imk_json = df_imk.to_dict(orient='records')
murid_json = df_murid.to_dict(orient='records')
inv_json = df_inv.to_dict(orient='records')

html_content = f"""<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Master Analytics Dashboard Provinsi Sumatera Selatan</title>
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <!-- FontAwesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <!-- Chart.js -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {{
            --bg-body: #090d16;
            --bg-card: rgba(30, 41, 59, 0.7);
            --border-card: rgba(255, 255, 255, 0.08);
            --primary: #3b82f6;
            --secondary: #10b981;
            --accent: #f59e0b;
            --danger: #ef4444;
            --purple: #8b5cf6;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Plus Jakarta Sans', sans-serif;
        }}

        body {{
            background: var(--bg-body);
            background-image: 
                radial-gradient(at 0% 0%, rgba(59, 130, 246, 0.15) 0px, transparent 50%),
                radial-gradient(at 100% 100%, rgba(139, 92, 246, 0.1) 0px, transparent 50%);
            background-attachment: fixed;
            color: var(--text-main);
            min-height: 100vh;
            padding: 24px;
        }}

        .header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 28px;
            padding-bottom: 16px;
            border-bottom: 1px solid var(--border-card);
        }}

        .header h1 {{
            font-size: 26px;
            font-weight: 800;
            background: linear-gradient(135deg, #60a5fa 0%, #3b82f6 50%, #a855f7 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            display: flex;
            align-items: center;
            gap: 12px;
        }}

        .header .subtitle {{
            color: var(--text-muted);
            font-size: 14px;
            margin-top: 4px;
        }}

        .badge-live {{
            background: rgba(16, 185, 129, 0.15);
            color: #34d399;
            border: 1px solid rgba(16, 185, 129, 0.3);
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 13px;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .badge-live .pulse {{
            width: 8px;
            height: 8px;
            background: #34d399;
            border-radius: 50%;
            box-shadow: 0 0 8px #34d399;
            animation: pulse 2s infinite;
        }}

        @keyframes pulse {{
            0% {{ transform: scale(0.95); opacity: 0.8; }}
            50% {{ transform: scale(1.2); opacity: 1; }}
            100% {{ transform: scale(0.95); opacity: 0.8; }}
        }}

        /* Grid Metrics */
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 18px;
            margin-bottom: 28px;
        }}

        .card-kpi {{
            background: var(--bg-card);
            backdrop-filter: blur(12px);
            border: 1px solid var(--border-card);
            border-radius: 16px;
            padding: 20px;
            transition: all 0.3s ease;
        }}

        .card-kpi:hover {{
            transform: translateY(-4px);
            border-color: rgba(59, 130, 246, 0.4);
        }}

        .card-kpi .title {{
            color: var(--text-muted);
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 8px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .card-kpi .value {{
            font-size: 26px;
            font-weight: 800;
            color: #fff;
            margin-bottom: 6px;
        }}

        .card-kpi .subtext {{
            font-size: 12px;
            font-weight: 500;
            display: flex;
            align-items: center;
            gap: 6px;
        }}

        .text-green {{ color: #34d399; }}
        .text-red {{ color: #f87171; }}
        .text-blue {{ color: #60a5fa; }}
        .text-orange {{ color: #fbbf24; }}
        .text-purple {{ color: #a78bfa; }}

        /* Charts Grid */
        .charts-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 20px;
            margin-bottom: 28px;
        }}

        @media (max-width: 1024px) {{
            .charts-grid {{ grid-template-columns: 1fr; }}
        }}

        .card-chart {{
            background: var(--bg-card);
            backdrop-filter: blur(12px);
            border: 1px solid var(--border-card);
            border-radius: 16px;
            padding: 24px;
        }}

        .card-chart h3 {{
            font-size: 15px;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 10px;
            color: #f1f5f9;
            margin-bottom: 16px;
        }}

        .chart-container {{
            position: relative;
            height: 300px;
            width: 100%;
        }}

        /* Table Section */
        .card-table {{
            background: var(--bg-card);
            backdrop-filter: blur(12px);
            border: 1px solid var(--border-card);
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 28px;
        }}

        .table-responsive {{
            overflow-x: auto;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
            text-align: left;
        }}

        th {{
            background: rgba(15, 23, 42, 0.6);
            color: var(--text-muted);
            font-weight: 600;
            padding: 12px 14px;
            border-bottom: 1px solid var(--border-card);
            text-transform: uppercase;
            font-size: 11px;
        }}

        td {{
            padding: 12px 14px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.04);
            color: #e2e8f0;
        }}

        tr:hover td {{ background: rgba(255, 255, 255, 0.02); }}

        .tab-buttons {{
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }}

        .tab-btn {{
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--border-card);
            color: var(--text-muted);
            padding: 8px 16px;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 600;
            font-size: 13px;
            transition: all 0.2s;
        }}

        .tab-btn.active, .tab-btn:hover {{
            background: var(--primary);
            color: #fff;
            border-color: var(--primary);
        }}
    </style>
</head>
<body>

    <div class="header">
        <div>
            <h1><i class="fa-solid fa-chart-pie"></i> Financial & Socio-Economic Dashboard Sumsel</h1>
            <div class="subtitle">Analisis Integrasi 60 Dataset Demografi, Keuangan, Investasi, Pendapatan & Pendidikan (2018 - 2026)</div>
        </div>
        <div class="badge-live">
            <div class="pulse"></div> 60 File Dataset Terverifikasi BPS & Disnakertrans
        </div>
    </div>

    <!-- KPI CARDS -->
    <div class="metrics-grid">
        <div class="card-kpi">
            <div class="title">Total Populasi (2026) <i class="fa-solid fa-users text-blue"></i></div>
            <div class="value">9,017,100</div>
            <div class="subtext text-green"><i class="fa-solid fa-arrow-trend-up"></i> +0.99% per tahun</div>
        </div>
        <div class="card-kpi">
            <div class="title">Nilai Investasi Swasta <i class="fa-solid fa-sack-dollar text-purple"></i></div>
            <div class="value">Rp 15.04 T</div>
            <div class="subtext text-purple"><i class="fa-solid fa-building"></i> 50 Perusahaan Korporasi</div>
        </div>
        <div class="card-kpi">
            <div class="title">Pendapatan Pekerja Informal <i class="fa-solid fa-wallet text-green"></i></div>
            <div class="value">Rp 2.15 M / bln</div>
            <div class="subtext text-green"><i class="fa-solid fa-arrow-trend-up"></i> Tumbuh dari Rp 1.7M (2019)</div>
        </div>
        <div class="card-kpi">
            <div class="title">Tingkat Pengangguran (2025) <i class="fa-solid fa-user-slash text-orange"></i></div>
            <div class="value">3.69%</div>
            <div class="subtext text-green"><i class="fa-solid fa-arrow-trend-down"></i> Melandai dari 5.51%</div>
        </div>
        <div class="card-kpi">
            <div class="title">Rasio Cerai/Nikah (2025) <i class="fa-solid fa-heart-crack text-red"></i></div>
            <div class="value">22.50%</div>
            <div class="subtext text-red"><i class="fa-solid fa-venus"></i> 79.8% Cerai Gugat</div>
        </div>
    </div>

    <!-- CHARTS GRID -->
    <div class="charts-grid">
        <div class="card-chart">
            <h3><i class="fa-solid fa-chart-line text-blue"></i> Tren Angkatan Kerja & Penduduk Bekerja</h3>
            <div class="chart-container"><canvas id="chartLabor"></canvas></div>
        </div>
        <div class="card-chart">
            <h3><i class="fa-solid fa-wallet text-green"></i> Tren Rata-Rata Pendapatan Worker Informal (2019-2025)</h3>
            <div class="chart-container"><canvas id="chartInformalIncome"></canvas></div>
        </div>
        <div class="card-chart">
            <h3><i class="fa-solid fa-building-flag text-purple"></i> Top 10 Nilai Investasi Korporasi Swasta (Rp Miliar)</h3>
            <div class="chart-container"><canvas id="chartInvestment"></canvas></div>
        </div>
        <div class="card-chart">
            <h3><i class="fa-solid fa-graduation-cap text-orange"></i> Pipa Jumlah Murid Sekolah (2024)</h3>
            <div class="chart-container"><canvas id="chartEducation"></canvas></div>
        </div>
    </div>

    <!-- DATA TABLES -->
    <div class="card-table">
        <div class="tab-buttons">
            <button class="tab-btn active" onclick="showTab('inv')">Investasi Korporasi</button>
            <button class="tab-btn" onclick="showTab('inf')">Pendapatan Informal</button>
            <button class="tab-btn" onclick="showTab('labor')">Ketenagakerjaan</button>
            <button class="tab-btn" onclick="showTab('divorce')">Nikah & Cerai (2025)</button>
        </div>

        <div id="tab-inv" class="table-responsive">
            <table>
                <thead>
                    <tr>
                        <th>No</th>
                        <th>Nama Perusahaan</th>
                        <th>Nilai Investasi (Rp Miliar)</th>
                    </tr>
                </thead>
                <tbody id="inv-body"></tbody>
            </table>
        </div>

        <div id="tab-inf" class="table-responsive" style="display:none;">
            <table>
                <thead>
                    <tr>
                        <th>Tahun</th>
                        <th>Kabupaten / Kota</th>
                        <th>Rata-Rata Pendapatan Bersih (Rp)</th>
                    </tr>
                </thead>
                <tbody id="inf-body"></tbody>
            </table>
        </div>

        <div id="tab-labor" class="table-responsive" style="display:none;">
            <table>
                <thead>
                    <tr>
                        <th>Tahun</th>
                        <th>Penduduk Bekerja</th>
                        <th>Angkatan Kerja</th>
                        <th>Penganggur</th>
                        <th>TPT Total (%)</th>
                        <th>TPT Laki-Laki (%)</th>
                        <th>TPT Perempuan (%)</th>
                    </tr>
                </thead>
                <tbody id="labor-body"></tbody>
            </table>
        </div>

        <div id="tab-divorce" class="table-responsive" style="display:none;">
            <table>
                <thead>
                    <tr>
                        <th>Kabupaten / Kota</th>
                        <th>Nikah</th>
                        <th>Cerai Talak</th>
                        <th>Cerai Gugat</th>
                        <th>Total Cerai</th>
                        <th>Rasio Cerai/Nikah</th>
                        <th>% Cerai Gugat</th>
                    </tr>
                </thead>
                <tbody id="divorce-body"></tbody>
            </table>
        </div>
    </div>

    <script>
        const rawLabor = {json.dumps(labor_json)};
        const rawNC = {json.dumps(nc_json)};
        const rawInf = {json.dumps(inf_json)};
        const rawInv = {json.dumps(inv_json)};

        // 1. Labor Chart
        new Chart(document.getElementById('chartLabor'), {{
            type: 'line',
            data: {{
                labels: rawLabor.map(d => d.Tahun),
                datasets: [
                    {{ label: 'Angkatan Kerja', data: rawLabor.map(d => d.Jumlah_Angkatan_Kerja), borderColor: '#3b82f6', backgroundColor: 'rgba(59,130,246,0.1)', fill: true, tension: 0.3 }},
                    {{ label: 'Penduduk Bekerja', data: rawLabor.map(d => d.Penduduk_Bekerja), borderColor: '#10b981', backgroundColor: 'rgba(16,185,129,0.1)', fill: true, tension: 0.3 }}
                ]
            }},
            options: {{ responsive: true, maintainAspectRatio: false, plugins: {{ legend: {{ labels: {{ color: '#cbd5e1' }} }} }}, scales: {{ y: {{ grid: {{ color: 'rgba(255,255,255,0.05)' }}, ticks: {{ color: '#94a3b8' }} }}, x: {{ grid: {{ display: false }}, ticks: {{ color: '#94a3b8' }} }} }} }}
        }});

        // 2. Informal Income Chart
        const infProv = rawInf.filter(d => d.Kabupaten_Kota.includes('Sumatera Selatan')).sort((a,b) => a.Tahun - b.Tahun);
        const colValInf = Object.keys(infProv[0]||{{}}).find(k => !['Tahun', 'Kabupaten_Kota'].includes(k));
        new Chart(document.getElementById('chartInformalIncome'), {{
            type: 'line',
            data: {{
                labels: infProv.map(d => d.Tahun),
                datasets: [{{ label: 'Rata-Rata Pendapatan Bersih (Rp)', data: infProv.map(d => d[colValInf]), borderColor: '#34d399', borderWidth: 3, pointRadius: 5, fill: false }}]
            }},
            options: {{ responsive: true, maintainAspectRatio: false, plugins: {{ legend: {{ labels: {{ color: '#cbd5e1' }} }} }}, scales: {{ y: {{ grid: {{ color: 'rgba(255,255,255,0.05)' }}, ticks: {{ color: '#94a3b8' }} }}, x: {{ grid: {{ display: false }}, ticks: {{ color: '#94a3b8' }} }} }} }}
        }});

        // 3. Investment Chart
        const invClean = rawInv.filter(d => !d['Nama Perusahaan'].includes('Jumlah')).map(d => ({{
            name: d['Nama Perusahaan'],
            val: parseFloat(String(d['Nilai Investasi (Rp Miliar)']).replace('-','0')) || 0
        }})).sort((a,b) => b.val - a.val).slice(0, 10);
        new Chart(document.getElementById('chartInvestment'), {{
            type: 'bar',
            data: {{
                labels: invClean.map(d => d.name),
                datasets: [{{ label: 'Investasi (Rp Miliar)', data: invClean.map(d => d.val), backgroundColor: '#a78bfa' }}]
            }},
            options: {{ indexAxis: 'y', responsive: true, maintainAspectRatio: false, plugins: {{ legend: {{ display: false }} }}, scales: {{ x: {{ grid: {{ color: 'rgba(255,255,255,0.05)' }}, ticks: {{ color: '#94a3b8' }} }}, y: {{ grid: {{ display: false }}, ticks: {{ color: '#cbd5e1' }} }} }} }}
        }});

        // 4. Education Chart
        new Chart(document.getElementById('chartEducation'), {{
            type: 'bar',
            data: {{
                labels: ['SD (Primary)', 'SMP (Junior High)', 'SMA (Senior High)', 'SMK (Vocational)'],
                datasets: [{{ label: 'Jumlah Murid (Ribu)', data: [914.9, 360.5, 209.1, 125.1], backgroundColor: ['#60a5fa', '#34d399', '#f87171', '#fbbf24'] }}]
            }},
            options: {{ responsive: true, maintainAspectRatio: false, plugins: {{ legend: {{ display: false }} }}, scales: {{ y: {{ grid: {{ color: 'rgba(255,255,255,0.05)' }}, ticks: {{ color: '#94a3b8' }} }}, x: {{ grid: {{ display: false }}, ticks: {{ color: '#94a3b8' }} }} }} }}
        }});

        // Populate Tables
        const invBody = document.getElementById('inv-body');
        rawInv.slice(0, 20).forEach(r => {{
            invBody.innerHTML += `<tr>
                <td>${{r.No}}</td>
                <td><strong>${{r['Nama Perusahaan']}}</strong></td>
                <td><strong class="text-purple">${{r['Nilai Investasi (Rp Miliar)']}}</strong></td>
            </tr>`;
        }});

        const infBody = document.getElementById('inf-body');
        infProv.forEach(r => {{
            const val = r[colValInf];
            infBody.innerHTML += `<tr>
                <td><strong>${{r.Tahun}}</strong></td>
                <td>${{r.Kabupaten_Kota}}</td>
                <td><strong class="text-green">Rp ${{val ? val.toLocaleString() : '-'}}</strong></td>
            </tr>`;
        }});

        const laborBody = document.getElementById('labor-body');
        rawLabor.forEach(r => {{
            laborBody.innerHTML += `<tr>
                <td><strong>${{r.Tahun}}</strong></td>
                <td>${{r.Penduduk_Bekerja.toLocaleString()}}</td>
                <td>${{r.Jumlah_Angkatan_Kerja.toLocaleString()}}</td>
                <td>${{r.Penganggur_Terbuka_Orang.toLocaleString()}}</td>
                <td><span class="text-orange"><strong>${{r['TPT_Total_%']}}%</strong></span></td>
                <td>${{r['TPT_Laki_Laki_%']}}%</td>
                <td>${{r['TPT_Perempuan_%']}}%</td>
            </tr>`;
        }});

        const nc2025All = rawNC.filter(d => d.Tahun === 2025).sort((a,b) => (b.Jumlah_Cerai||0) - (a.Jumlah_Cerai||0));
        const divorceBody = document.getElementById('divorce-body');
        nc2025All.forEach(r => {{
            divorceBody.innerHTML += `<tr>
                <td><strong>${{r.Kabupaten_Kota}}</strong></td>
                <td>${{r.Nikah ? r.Nikah.toLocaleString() : '-'}}</td>
                <td>${{r.Cerai_Talak ? r.Cerai_Talak.toLocaleString() : '-'}}</td>
                <td>${{r.Cerai_Gugat ? r.Cerai_Gugat.toLocaleString() : '-'}}</td>
                <td><strong class="text-red">${{r.Jumlah_Cerai ? r.Jumlah_Cerai.toLocaleString() : '-'}}</strong></td>
                <td>${{r['Rasio_Cerai_Nikah_%'] ? r['Rasio_Cerai_Nikah_%'].toFixed(2) + '%' : '-'}}</td>
                <td>${{r['Proporsi_Cerai_Gugat_%'] ? r['Proporsi_Cerai_Gugat_%'].toFixed(1) + '%' : '-'}}</td>
            </tr>`;
        }});

        function showTab(tabName) {{
            document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
            ['inv', 'inf', 'labor', 'divorce'].forEach(id => document.getElementById('tab-' + id).style.display = 'none');
            document.getElementById('tab-' + tabName).style.display = 'block';
            event.target.classList.add('active');
        }}
    </script>
</body>
</html>
"""

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Master Dashboard HTML v2 built successfully at:", html_file)
