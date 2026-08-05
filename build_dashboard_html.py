import os
import json
import pandas as pd

output_dir = r'd:\Analisis data Financial Sumatera Selatan\processed_data'
html_file = r'd:\Analisis data Financial Sumatera Selatan\dashboard.html'

df_pop = pd.read_csv(os.path.join(output_dir, 'populasi_bersih_2019_2026.csv'))
df_labor = pd.read_csv(os.path.join(output_dir, 'ketenagakerjaan_bersih_2019_2025.csv'))
df_nc = pd.read_csv(os.path.join(output_dir, 'nikah_cerai_bersih_2019_2025.csv'))

pop_json = df_pop.to_dict(orient='records')
labor_json = df_labor.to_dict(orient='records')
nc_json = df_nc.to_dict(orient='records')

html_content = f"""<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard Analisis Data Provinsi Sumatera Selatan</title>
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <!-- FontAwesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <!-- Chart.js -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {{
            --bg-body: #0f172a;
            --bg-card: rgba(30, 41, 59, 0.7);
            --border-card: rgba(255, 255, 255, 0.08);
            --primary: #3b82f6;
            --primary-glow: rgba(59, 130, 246, 0.3);
            --secondary: #10b981;
            --accent: #f59e0b;
            --danger: #ef4444;
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
            background: #090d16;
            background-image: 
                radial-gradient(at 0% 0%, rgba(59, 130, 246, 0.15) 0px, transparent 50%),
                radial-gradient(at 100% 100%, rgba(16, 185, 129, 0.1) 0px, transparent 50%);
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
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
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
            position: relative;
            overflow: hidden;
        }}

        .card-kpi:hover {{
            transform: translateY(-4px);
            border-color: rgba(59, 130, 246, 0.4);
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
        }}

        .card-kpi .title {{
            color: var(--text-muted);
            font-size: 13px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 8px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .card-kpi .value {{
            font-size: 28px;
            font-weight: 800;
            color: #fff;
            margin-bottom: 6px;
        }}

        .card-kpi .subtext {{
            font-size: 13px;
            font-weight: 500;
            display: flex;
            align-items: center;
            gap: 6px;
        }}

        .text-green {{ color: #34d399; }}
        .text-red {{ color: #f87171; }}
        .text-blue {{ color: #60a5fa; }}
        .text-orange {{ color: #fbbf24; }}

        /* Main Section Cards */
        .charts-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 20px;
            margin-bottom: 28px;
        }}

        @media (max-width: 1024px) {{
            .charts-grid {{
                grid-template-columns: 1fr;
            }}
        }}

        .card-chart {{
            background: var(--bg-card);
            backdrop-filter: blur(12px);
            border: 1px solid var(--border-card);
            border-radius: 16px;
            padding: 24px;
        }}

        .card-chart .chart-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }}

        .card-chart h3 {{
            font-size: 16px;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 10px;
            color: #f1f5f9;
        }}

        .chart-container {{
            position: relative;
            height: 320px;
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
            font-size: 14px;
            text-align: left;
        }}

        th {{
            background: rgba(15, 23, 42, 0.6);
            color: var(--text-muted);
            font-weight: 600;
            padding: 12px 16px;
            border-bottom: 1px solid var(--border-card);
            text-transform: uppercase;
            font-size: 12px;
        }}

        td {{
            padding: 14px 16px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.04);
            color: #e2e8f0;
        }}

        tr:hover td {{
            background: rgba(255, 255, 255, 0.02);
        }}

        .tab-buttons {{
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
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
            <h1><i class="fa-solid fa-chart-line"></i> Analytics Dashboard Sumatera Selatan</h1>
            <div class="subtitle">Analisis Data Demografi, Ketenagakerjaan, dan Pernikahan/Perceraian (2019 - 2026)</div>
        </div>
        <div class="badge-live">
            <div class="pulse"></div> Data Terverifikasi BPS & Disnakertrans
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
            <div class="title">Angkatan Kerja (2025) <i class="fa-solid fa-briefcase text-green"></i></div>
            <div class="value">4,664,935</div>
            <div class="subtext text-blue"><i class="fa-solid fa-user-check"></i> 4.49 Juta Bekerja</div>
        </div>
        <div class="card-kpi">
            <div class="title">Tingkat Pengangguran (2025) <i class="fa-solid fa-user-slash text-orange"></i></div>
            <div class="value">3.69%</div>
            <div class="subtext text-green"><i class="fa-solid fa-arrow-trend-down"></i> Turun dari 5.51% (2020)</div>
        </div>
        <div class="card-kpi">
            <div class="title">Rasio Cerai/Nikah (2025) <i class="fa-solid fa-heart-crack text-red"></i></div>
            <div class="value">22.50%</div>
            <div class="subtext text-red"><i class="fa-solid fa-venus"></i> 79.8% Cerai Gugat (Istri)</div>
        </div>
    </div>

    <!-- CHARTS GRID -->
    <div class="charts-grid">
        <div class="card-chart">
            <div class="chart-header">
                <h3><i class="fa-solid fa-chart-area text-blue"></i> Tren Angkatan Kerja & Bekerja (2019-2025)</h3>
            </div>
            <div class="chart-container">
                <canvas id="chartLabor"></canvas>
            </div>
        </div>

        <div class="card-chart">
            <div class="chart-header">
                <h3><i class="fa-solid fa-chart-line text-orange"></i> Tingkat Pengangguran Terbuka (TPT) Gender</h3>
            </div>
            <div class="chart-container">
                <canvas id="chartTPT"></canvas>
            </div>
        </div>

        <div class="card-chart">
            <div class="chart-header">
                <h3><i class="fa-solid fa-heart text-green"></i> Pernikahan vs Perceraian (2019-2025)</h3>
            </div>
            <div class="chart-container">
                <canvas id="chartMarriage"></canvas>
            </div>
        </div>

        <div class="card-chart">
            <div class="chart-header">
                <h3><i class="fa-solid fa-city text-red"></i> Top 10 Kasus Perceraian Kab/Kota (2025)</h3>
            </div>
            <div class="chart-container">
                <canvas id="chartRegional"></canvas>
            </div>
        </div>
    </div>

    <!-- DATA TABLES -->
    <div class="card-table">
        <div class="tab-buttons">
            <button class="tab-btn active" onclick="showTab('labor')">Ketenagakerjaan</button>
            <button class="tab-btn" onclick="showTab('pop')">Populasi 2026</button>
            <button class="tab-btn" onclick="showTab('divorce')">Nikah & Cerai (2025)</button>
        </div>

        <div id="tab-labor" class="table-responsive">
            <table>
                <thead>
                    <tr>
                        <th>Tahun</th>
                        <th>Penduduk Bekerja</th>
                        <th>Angkatan Kerja</th>
                        <th>Penganggur (Est)</th>
                        <th>TPT Total (%)</th>
                        <th>TPT Laki-Laki (%)</th>
                        <th>TPT Perempuan (%)</th>
                    </tr>
                </thead>
                <tbody id="labor-body"></tbody>
            </table>
        </div>

        <div id="tab-pop" class="table-responsive" style="display:none;">
            <table>
                <thead>
                    <tr>
                        <th>Kelompok Umur</th>
                        <th>Laki-Laki (Ribu)</th>
                        <th>Perempuan (Ribu)</th>
                        <th>Total (Ribu Jiwa)</th>
                        <th>Proporsi (%)</th>
                    </tr>
                </thead>
                <tbody id="pop-body"></tbody>
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
        const rawPop = {json.dumps(pop_json)};
        const rawNC = {json.dumps(nc_json)};

        // Render Charts
        // 1. Labor
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

        // 2. TPT Gender
        new Chart(document.getElementById('chartTPT'), {{
            type: 'line',
            data: {{
                labels: rawLabor.map(d => d.Tahun),
                datasets: [
                    {{ label: 'TPT Laki-Laki (%)', data: rawLabor.map(d => d['TPT_Laki_Laki_%']), borderColor: '#60a5fa', borderWidth: 3, pointRadius: 5 }},
                    {{ label: 'TPT Perempuan (%)', data: rawLabor.map(d => d['TPT_Perempuan_%']), borderColor: '#f87171', borderWidth: 3, pointRadius: 5 }}
                ]
            }},
            options: {{ responsive: true, maintainAspectRatio: false, plugins: {{ legend: {{ labels: {{ color: '#cbd5e1' }} }} }}, scales: {{ y: {{ grid: {{ color: 'rgba(255,255,255,0.05)' }}, ticks: {{ color: '#94a3b8' }} }}, x: {{ grid: {{ display: false }}, ticks: {{ color: '#94a3b8' }} }} }} }}
        }});

        // 3. Marriage vs Divorce
        const ncProv = rawNC.filter(d => d.Kabupaten_Kota.includes('Sumatera Selatan')).sort((a,b) => a.Tahun - b.Tahun);
        new Chart(document.getElementById('chartMarriage'), {{
            type: 'bar',
            data: {{
                labels: ncProv.map(d => d.Tahun),
                datasets: [
                    {{ label: 'Nikah', data: ncProv.map(d => d.Nikah), backgroundColor: '#34d399' }},
                    {{ label: 'Cerai', data: ncProv.map(d => d.Jumlah_Cerai), backgroundColor: '#f87171' }}
                ]
            }},
            options: {{ responsive: true, maintainAspectRatio: false, plugins: {{ legend: {{ labels: {{ color: '#cbd5e1' }} }} }}, scales: {{ y: {{ grid: {{ color: 'rgba(255,255,255,0.05)' }}, ticks: {{ color: '#94a3b8' }} }}, x: {{ grid: {{ display: false }}, ticks: {{ color: '#94a3b8' }} }} }} }}
        }});

        // 4. Regional Divorce 2025 Top 10
        const nc2025Reg = rawNC.filter(d => d.Tahun === 2025 && !d.Kabupaten_Kota.includes('Sumatera Selatan')).sort((a,b) => b.Jumlah_Cerai - a.Jumlah_Cerai).slice(0, 10);
        new Chart(document.getElementById('chartRegional'), {{
            type: 'bar',
            data: {{
                labels: nc2025Reg.map(d => d.Kabupaten_Kota),
                datasets: [{{ label: 'Kasus Cerai 2025', data: nc2025Reg.map(d => d.Jumlah_Cerai), backgroundColor: '#fbbf24' }}]
            }},
            options: {{ indexAxis: 'y', responsive: true, maintainAspectRatio: false, plugins: {{ legend: {{ display: false }} }}, scales: {{ x: {{ grid: {{ color: 'rgba(255,255,255,0.05)' }}, ticks: {{ color: '#94a3b8' }} }}, y: {{ grid: {{ display: false }}, ticks: {{ color: '#cbd5e1' }} }} }} }}
        }});

        // Populate Tables
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

        const pop2026 = rawPop.filter(d => d.Tahun === 2026);
        const popBody = document.getElementById('pop-body');
        const tot2026 = 9017.1;
        pop2026.forEach(r => {{
            const pct = ((r.Total_Penduduk_Ribu / tot2026) * 100).toFixed(2);
            popBody.innerHTML += `<tr>
                <td><strong>${{r.Kelompok_Umur}}</strong></td>
                <td>${{r.Penduduk_Laki_Laki_Ribu}}</td>
                <td>${{r.Penduduk_Perempuan_Ribu}}</td>
                <td><strong>${{r.Total_Penduduk_Ribu}}</strong></td>
                <td>${{pct}}%</td>
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
            document.getElementById('tab-labor').style.display = 'none';
            document.getElementById('tab-pop').style.display = 'none';
            document.getElementById('tab-divorce').style.display = 'none';

            if(tabName === 'labor') {{
                document.getElementById('tab-labor').style.display = 'block';
                event.target.classList.add('active');
            }} else if(tabName === 'pop') {{
                document.getElementById('tab-pop').style.display = 'block';
                event.target.classList.add('active');
            }} else if(tabName === 'divorce') {{
                document.getElementById('tab-divorce').style.display = 'block';
                event.target.classList.add('active');
            }}
        }}
    </script>
</body>
</html>
"""

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Dashboard HTML built successfully at:", html_file)
