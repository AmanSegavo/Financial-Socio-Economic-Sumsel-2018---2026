import os
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set stylish theme
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 11

output_dir = r'd:\Analisis data Financial Sumatera Selatan\processed_data'
charts_dir = r'd:\Analisis data Financial Sumatera Selatan\charts'
os.makedirs(charts_dir, exist_ok=True)

df_pop = pd.read_csv(os.path.join(output_dir, 'populasi_bersih_2019_2026.csv'))
df_labor = pd.read_csv(os.path.join(output_dir, 'ketenagakerjaan_bersih_2019_2025.csv'))
df_nc = pd.read_csv(os.path.join(output_dir, 'nikah_cerai_bersih_2019_2025.csv'))

palette_primary = '#1e3d59'
palette_secondary = '#ff6e40'
palette_accent = '#ffc13b'
palette_muted = '#f5f0e1'
color_male = '#2b580c'
color_female = '#d9534f'

# ---------------------------------------------------------
# 1. DEMOGRAPHIC PYRAMID (2026)
# ---------------------------------------------------------
pop_2026 = df_pop[(df_pop['Tahun'] == 2026) & (~df_pop['Kelompok_Umur'].str.contains('Jumlah|Total', case=False))].copy()
# Order age groups
age_order = ['0-4', '5-9', '10-14', '15-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64', '65-69', '70-74', '75+']
pop_2026['Kelompok_Umur'] = pd.Categorical(pop_2026['Kelompok_Umur'], categories=age_order, ordered=True)
pop_2026 = pop_2026.sort_values('Kelompok_Umur')

fig, ax = plt.subplots(figsize=(10, 7), dpi=300)
y = np.arange(len(pop_2026))
height = 0.4

ax.barh(y - height/2, -pop_2026['Penduduk_Laki_Laki_Ribu'], height, label='Laki-Laki (Ribu)', color='#2b7bba')
ax.barh(y + height/2, pop_2026['Penduduk_Perempuan_Ribu'], height, label='Perempuan (Ribu)', color='#e85a71')

ax.set_yticks(y)
ax.set_yticklabels(pop_2026['Kelompok_Umur'])
ax.set_xlabel('Jumlah Penduduk (Ribu Jiwa)')
ax.set_title('Piramida Penduduk Provinsi Sumatera Selatan (Proyeksi 2026)', fontsize=14, fontweight='bold', pad=15)
ax.axvline(0, color='black', linewidth=0.8)

# Custom ticks on x axis
xticks = np.arange(-500, 501, 100)
ax.set_xticks(xticks)
ax.set_xticklabels([str(abs(x)) for x in xticks])

ax.legend(loc='upper right', frameon=True)
plt.tight_layout()
plt.savefig(os.path.join(charts_dir, 'demographic_pyramid_2026.png'))
plt.close()

# ---------------------------------------------------------
# 2. POPULATION TREND (2020-2026)
# ---------------------------------------------------------
pop_tot = df_pop[df_pop['Kelompok_Umur'].str.contains('Jumlah|Total', case=False)].sort_values('Tahun')

fig, ax1 = plt.subplots(figsize=(10, 5), dpi=300)
ax1.plot(pop_tot['Tahun'], pop_tot['Total_Penduduk_Ribu']/1000, marker='o', linewidth=3, color='#1b4965', label='Total Penduduk (Juta)')
ax1.set_ylabel('Total Penduduk (Juta Jiwa)', color='#1b4965', fontweight='bold')
ax1.set_xlabel('Tahun', fontweight='bold')
ax1.set_ylim(8.0, 9.5)

for i, txt in enumerate(pop_tot['Total_Penduduk_Ribu']/1000):
    ax1.annotate(f"{txt:.3f}M", (pop_tot['Tahun'].iloc[i], txt + 0.03), ha='center', fontweight='bold', color='#1b4965')

ax2 = ax1.twinx()
rasio_g = (pop_tot['Penduduk_Laki_Laki_Ribu'] / pop_tot['Penduduk_Perempuan_Ribu']) * 100
ax2.plot(pop_tot['Tahun'], rasio_g, marker='s', linestyle='--', linewidth=2, color='#e63946', label='Rasio Gender (L/P %)')
ax2.set_ylabel('Rasio Gender (Laki/Perempuan x 100)', color='#e63946', fontweight='bold')
ax2.set_ylim(100, 106)

plt.title('Pertumbuhan Populasi & Rasio Gender Sumatera Selatan (2020 - 2026)', fontsize=13, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig(os.path.join(charts_dir, 'population_trend_2020_2026.png'))
plt.close()

# ---------------------------------------------------------
# 3. LABOR FORCE & UNEMPLOYMENT TREND (2019-2025)
# ---------------------------------------------------------
fig, ax1 = plt.subplots(figsize=(10, 5), dpi=300)

ax1.bar(df_labor['Tahun'] - 0.15, df_labor['Penduduk_Bekerja']/1e6, width=0.3, label='Penduduk Bekerja (Juta)', color='#2a9d8f')
ax1.bar(df_labor['Tahun'] + 0.15, df_labor['Jumlah_Angkatan_Kerja']/1e6, width=0.3, label='Jumlah Angkatan Kerja (Juta)', color='#264653', alpha=0.8)
ax1.set_ylabel('Jumlah Orang (Juta)', fontweight='bold')
ax1.set_ylim(3.5, 5.2)

ax2 = ax1.twinx()
ax2.plot(df_labor['Tahun'], df_labor['TPT_Total_%'], marker='D', linewidth=3, color='#e76f51', label='Tingkat Pengangguran Terbuka (%)')
ax2.set_ylabel('TPT (%)', color='#e76f51', fontweight='bold')
ax2.set_ylim(2.5, 6.5)

for i, txt in enumerate(df_labor['TPT_Total_%']):
    ax2.annotate(f"{txt:.2f}%", (df_labor['Tahun'].iloc[i], txt + 0.15), ha='center', fontweight='bold', color='#e76f51')

ax1.legend(loc='upper left')
ax2.legend(loc='upper right')
plt.title('Tren Ketenagakerjaan & Tingkat Pengangguran Terbuka (TPT) Sumsel (2019-2025)', fontsize=13, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig(os.path.join(charts_dir, 'labor_unemployment_trend.png'))
plt.close()

# ---------------------------------------------------------
# 4. GENDER UNEMPLOYMENT COMPARISON
# ---------------------------------------------------------
fig, ax = plt.subplots(figsize=(9, 5), dpi=300)
ax.plot(df_labor['Tahun'], df_labor['TPT_Laki_Laki_%'], marker='o', linewidth=2.5, color='#457b9d', label='TPT Laki-Laki (%)')
ax.plot(df_labor['Tahun'], df_labor['TPT_Perempuan_%'], marker='s', linewidth=2.5, color='#e63946', label='TPT Perempuan (%)')

for i in range(len(df_labor)):
    ax.annotate(f"{df_labor['TPT_Laki_Laki_%'].iloc[i]:.2f}%", (df_labor['Tahun'].iloc[i], df_labor['TPT_Laki_Laki_%'].iloc[i] - 0.15), ha='center', fontsize=9, color='#457b9d')
    ax.annotate(f"{df_labor['TPT_Perempuan_%'].iloc[i]:.2f}%", (df_labor['Tahun'].iloc[i], df_labor['TPT_Perempuan_%'].iloc[i] + 0.1), ha='center', fontsize=9, color='#e63946')

ax.set_ylabel('TPT (%)', fontweight='bold')
ax.set_xlabel('Tahun', fontweight='bold')
ax.set_title('Perbandingan Tingkat Pengangguran Terbuka Menurut Jenis Kelamin (2019-2025)', fontsize=13, fontweight='bold', pad=15)
ax.legend(loc='upper right')
plt.tight_layout()
plt.savefig(os.path.join(charts_dir, 'gender_unemployment.png'))
plt.close()

# ---------------------------------------------------------
# 5. MARRIAGE VS DIVORCE TREND (2019-2025)
# ---------------------------------------------------------
nc_prov = df_nc[df_nc['Kabupaten_Kota'].str.contains('Sumatera Selatan', case=False)].sort_values('Tahun')

fig, ax1 = plt.subplots(figsize=(10, 5), dpi=300)
ax1.plot(nc_prov['Tahun'], nc_prov['Nikah'], marker='o', linewidth=3, color='#2a9d8f', label='Kejadian Pernikahan')
ax1.set_ylabel('Jumlah Pernikahan', color='#2a9d8f', fontweight='bold')
ax1.set_xlabel('Tahun', fontweight='bold')

for i, txt in enumerate(nc_prov['Nikah']):
    ax1.annotate(f"{int(txt):,}", (nc_prov['Tahun'].iloc[i], txt + 800), ha='center', fontweight='bold', color='#2a9d8f')

ax2 = ax1.twinx()
ax2.plot(nc_prov['Tahun'], nc_prov['Jumlah_Cerai'], marker='s', linewidth=3, color='#e76f51', label='Jumlah Perceraian')
ax2.set_ylabel('Jumlah Perceraian', color='#e76f51', fontweight='bold')

for i, txt in enumerate(nc_prov['Jumlah_Cerai']):
    ax2.annotate(f"{int(txt):,}", (nc_prov['Tahun'].iloc[i], txt - 500), ha='center', fontweight='bold', color='#e76f51')

plt.title('Tren Pernikahan vs Perceraian di Provinsi Sumatera Selatan (2019-2025)', fontsize=13, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig(os.path.join(charts_dir, 'marriage_divorce_trend.png'))
plt.close()

# ---------------------------------------------------------
# 6. CERAI GUGAT VS CERAI TALAK (2019-2025)
# ---------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
width = 0.35
x = nc_prov['Tahun']

ax.bar(x - width/2, nc_prov['Cerai_Gugat'], width, label='Cerai Gugat (Inisiatif Istri)', color='#d9534f')
ax.bar(x + width/2, nc_prov['Cerai_Talak'], width, label='Cerai Talak (Inisiatif Suami)', color='#0275d8')

for i in range(len(nc_prov)):
    g_pct = nc_prov['Proporsi_Cerai_Gugat_%'].iloc[i]
    ax.annotate(f"{g_pct:.1f}% Gugat", (x.iloc[i], nc_prov['Cerai_Gugat'].iloc[i] + 200), ha='center', fontweight='bold', fontsize=9, color='#d9534f')

ax.set_ylabel('Jumlah Kejadian Perceraian', fontweight='bold')
ax.set_xlabel('Tahun', fontweight='bold')
ax.set_title('Dominasi Cerai Gugat (Istri) vs Cerai Talak (Suami) di Sumsel (2019-2025)', fontsize=13, fontweight='bold', pad=15)
ax.legend(loc='upper right')
plt.tight_layout()
plt.savefig(os.path.join(charts_dir, 'divorce_type_breakdown.png'))
plt.close()

# ---------------------------------------------------------
# 7. REGIONAL DIVORCE HOTSPOTS (2025)
# ---------------------------------------------------------
nc_2025 = df_nc[(df_nc['Tahun'] == 2025) & (~df_nc['Kabupaten_Kota'].str.contains('Sumatera Selatan', case=False))].sort_values('Jumlah_Cerai', ascending=True)

fig, ax = plt.subplots(figsize=(10, 8), dpi=300)
bars = ax.barh(nc_2025['Kabupaten_Kota'], nc_2025['Jumlah_Cerai'], color='#e76f51', alpha=0.85)

for bar in bars:
    w = bar.get_width()
    ax.annotate(f"{int(w):,} kasus", (w + 20, bar.get_y() + bar.get_height()/2), va='center', fontweight='bold', fontsize=9)

ax.set_xlabel('Jumlah Kasus Perceraian (2025)', fontweight='bold')
ax.set_title('Peringkat Kasus Perceraian Menurut Kabupaten/Kota di Sumsel (2025)', fontsize=13, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig(os.path.join(charts_dir, 'regional_divorce_2025.png'))
plt.close()

print("ALL CHARTS GENERATED SUCCESSFULLY!")

