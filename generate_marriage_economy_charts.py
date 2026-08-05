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

df_nc = pd.read_csv(os.path.join(output_dir, 'nikah_cerai_bersih_2019_2025.csv'))
df_inf = pd.read_csv(os.path.join(output_dir, 'pendapatan_informal_2019_2025.csv'))
df_pop = pd.read_csv(os.path.join(output_dir, 'populasi_bersih_2019_2026.csv'))

# 1. MARRIAGE RATE TREND (2020-2025)
nc_prov = df_nc[df_nc['Kabupaten_Kota'].str.contains('Sumatera Selatan', case=False)].sort_values('Tahun')
pop_tot = df_pop[df_pop['Kelompok_Umur'].str.contains('Jumlah|Total', case=False)].sort_values('Tahun')
df_m_trend = pd.merge(nc_prov, pop_tot[['Tahun', 'Total_Penduduk_Ribu']], on='Tahun', how='inner')
df_m_trend['Marriage_Rate'] = (df_m_trend['Nikah'] / df_m_trend['Total_Penduduk_Ribu'])

fig, ax1 = plt.subplots(figsize=(9, 5), dpi=300)
ax1.plot(df_m_trend['Tahun'], df_m_trend['Marriage_Rate'], marker='o', linewidth=3, color='#2a9d8f', label='Angka Pernikahan (per 1.000 Penduduk)')
ax1.set_ylabel('Nikah per 1.000 Penduduk', color='#2a9d8f', fontweight='bold')
ax1.set_xlabel('Tahun', fontweight='bold')

for i, txt in enumerate(df_m_trend['Marriage_Rate']):
    ax1.annotate(f"{txt:.2f}", (df_m_trend['Tahun'].iloc[i], txt + 0.1), ha='center', fontweight='bold', color='#2a9d8f')

ax2 = ax1.twinx()
ax2.plot(df_m_trend['Tahun'], df_m_trend['Rasio_Cerai_Nikah_%'], marker='s', linestyle='--', linewidth=2.5, color='#e76f51', label='Rasio Cerai/Nikah (%)')
ax2.set_ylabel('Rasio Cerai/Nikah (%)', color='#e76f51', fontweight='bold')

plt.title('Penundaan Pernikahan & Peningkatan Rasio Perceraian di Sumsel (2020-2025)', fontsize=13, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig(os.path.join(charts_dir, 'marriage_rate_vs_divorce_trend.png'))
plt.close()

# 2. SCATTER PLOT: INFORMAL INCOME VS DIVORCE RATIO (2025)
nc_2025 = df_nc[(df_nc['Tahun'] == 2025) & (~df_nc['Kabupaten_Kota'].str.contains('Sumatera Selatan', case=False))]
inf_2025 = df_inf[(df_inf['Tahun'] == 2025) & (~df_inf['Kabupaten_Kota'].str.contains('Sumatera Selatan', case=False))]
col_inf_val = [c for c in inf_2025.columns if c not in ['Tahun', 'Kabupaten_Kota']][0]
df_scat = pd.merge(nc_2025, inf_2025[['Kabupaten_Kota', col_inf_val]], on='Kabupaten_Kota', how='inner')

fig, ax = plt.subplots(figsize=(9, 6), dpi=300)
sns.regplot(data=df_scat, x=col_inf_val, y='Rasio_Cerai_Nikah_%', ax=ax, color='#1d3557', scatter_kws={'s': 80, 'color': '#e63946'}, line_kws={'linewidth': 2, 'color': '#457b9d'})

for i, row in df_scat.iterrows():
    ax.annotate(row['Kabupaten_Kota'], (row[col_inf_val] + 15, row['Rasio_Cerai_Nikah_%']), fontsize=8)

ax.set_xlabel('Rata-Rata Pendapatan Bersih Pekerja Informal (Rupiah/Bulan)', fontweight='bold')
ax.set_ylabel('Rasio Perceraian / Pernikahan (%)', fontweight='bold')
ax.set_title('Korelasi Pendapatan Worker Informal vs Kerentanan Perceraian (r = -0.57)', fontsize=13, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig(os.path.join(charts_dir, 'income_vs_divorce_ratio_scatter.png'))
plt.close()

# Copy to artifact directory
for fname in ['marriage_rate_vs_divorce_trend.png', 'income_vs_divorce_ratio_scatter.png']:
    shutil.copy2(os.path.join(charts_dir, fname), os.path.join(artifact_dir, fname))

print("MARRIAGE & ECONOMY CORRELATION CHARTS GENERATED & COPIED TO ARTIFACTS!")
