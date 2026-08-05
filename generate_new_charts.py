import os
import shutil
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 11

output_dir = r'd:\Analisis data Financial Sumatera Selatan\processed_data'
charts_dir = r'd:\Analisis data Financial Sumatera Selatan\charts'
artifact_dir = r'C:\Users\amans\.gemini\antigravity-ide\brain\7ee1e145-1b1f-4bfe-9b7a-287781fe4dd8\charts'
os.makedirs(charts_dir, exist_ok=True)
os.makedirs(artifact_dir, exist_ok=True)

df_inf = pd.read_csv(os.path.join(output_dir, 'pendapatan_informal_2019_2025.csv'))
df_imk = pd.read_csv(os.path.join(output_dir, 'perusahaan_imk_2019_2022.csv'))
df_murid = pd.read_csv(os.path.join(output_dir, 'jumlah_murid_2019_2024.csv'))
df_inv = pd.read_csv(os.path.join(output_dir, 'investasi_perusahaan_sumsel.csv'))

# 1. INFORMAL EARNINGS TREND
inf_prov = df_inf[df_inf['Kabupaten_Kota'].str.contains('Sumatera Selatan', case=False)].sort_values('Tahun')
if not inf_prov.empty:
    val_col = [c for c in inf_prov.columns if c not in ['Tahun', 'Kabupaten_Kota']][0]
    fig, ax = plt.subplots(figsize=(9, 5), dpi=300)
    ax.plot(inf_prov['Tahun'], inf_prov[val_col]/1000, marker='o', linewidth=3, color='#e63946', label='Rata-Rata Pendapatan Informal (Ribu Rp)')
    for i, txt in enumerate(inf_prov[val_col]/1000):
        ax.annotate(f"Rp {txt:,.0f}k", (inf_prov['Tahun'].iloc[i], txt + 30), ha='center', fontweight='bold', color='#e63946')
    ax.set_ylabel('Pendapatan Bersih (Ribu Rupiah)', fontweight='bold')
    ax.set_xlabel('Tahun', fontweight='bold')
    ax.set_title('Tren Rata-Rata Pendapatan Bersih Sebulan Pekerja Informal Sumsel (2019-2025)', fontsize=13, fontweight='bold', pad=15)
    plt.tight_layout()
    plt.savefig(os.path.join(charts_dir, 'informal_income_trend.png'))
    plt.close()

# 2. TOP CORPORATE INVESTMENTS
df_inv_clean = df_inv.copy()
df_inv_clean['Nilai Investasi (Rp Miliar)'] = pd.to_numeric(df_inv_clean['Nilai Investasi (Rp Miliar)'].astype(str).str.replace('-', '0'), errors='coerce')
df_inv_top = df_inv_clean[~df_inv_clean['Nama Perusahaan'].str.contains('Jumlah', case=False)].sort_values('Nilai Investasi (Rp Miliar)', ascending=False).head(10)

fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
bars = ax.barh(df_inv_top['Nama Perusahaan'], df_inv_top['Nilai Investasi (Rp Miliar)'], color='#2a9d8f')
for bar in bars:
    w = bar.get_width()
    if w > 0:
        ax.annotate(f"Rp {w:,.1f} M", (w + 100, bar.get_y() + bar.get_height()/2), va='center', fontweight='bold', fontsize=9)
ax.set_xlabel('Nilai Investasi (Miliar Rupiah)', fontweight='bold')
ax.set_title('Top 10 Perusahaan Investasi Swasta Terbesar di Sumatera Selatan', fontsize=13, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig(os.path.join(charts_dir, 'corporate_investment_top.png'))
plt.close()

# 3. STUDENT ENROLLMENT PIPELINE (2024)
murid_2024_prov = df_murid[(df_murid['Tahun'] == 2024) & (df_murid['Kabupaten_Kota'].str.contains('Sumatera Selatan', case=False))]
if not murid_2024_prov.empty:
    row = murid_2024_prov.iloc[0]
    levels = ['SD', 'SMP', 'SMA', 'SMK']
    counts = [row.get(l, 0)/1000 for l in levels]
    fig, ax = plt.subplots(figsize=(9, 5), dpi=300)
    bars = ax.bar(levels, counts, color=['#457b9d', '#1d3557', '#e63946', '#f4a261'])
    for bar in bars:
        h = bar.get_height()
        ax.annotate(f"{h:,.1f}k Jiwa", (bar.get_x() + bar.get_width()/2, h + 15), ha='center', fontweight='bold')
    ax.set_ylabel('Jumlah Murid (Ribu Jiwa)', fontweight='bold')
    ax.set_title('Pipa Pendidikan & Jumlah Murid per Jenjang di Sumsel (2024)', fontsize=13, fontweight='bold', pad=15)
    plt.tight_layout()
    plt.savefig(os.path.join(charts_dir, 'student_pipeline_2024.png'))
    plt.close()

# Copy all new charts to artifact directory
for fname in os.listdir(charts_dir):
    if fname.endswith('.png'):
        shutil.copy2(os.path.join(charts_dir, fname), os.path.join(artifact_dir, fname))

print("NEW VISUALIZATION CHARTS GENERATED & COPIED TO ARTIFACTS!")
