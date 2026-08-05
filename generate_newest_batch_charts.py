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

df_kek = pd.read_csv(os.path.join(output_dir, 'kasus_kekerasan_2022_2025.csv'))
df_imb = pd.read_csv(os.path.join(output_dir, 'imb_aneka_investasi_2019_2025.csv'))

# 1. KEKERASAN GENDER TREND (2022-2025)
kek_tot = df_kek[df_kek['Kabupaten_Kota'].str.contains('Sumatera Selatan', case=False)].sort_values('Tahun')
if kek_tot.empty:
    # aggregate if no summary row
    kek_tot = df_kek[~df_kek['Kabupaten_Kota'].str.contains('Sumatera Selatan', case=False)].groupby('Tahun')[['Korban_Laki_Laki', 'Korban_Perempuan', 'Total_Kasus_Kekerasan']].sum().reset_index()

fig, ax = plt.subplots(figsize=(9, 5), dpi=300)
ax.plot(kek_tot['Tahun'], kek_tot['Korban_Perempuan'], marker='o', linewidth=3, color='#e63946', label='Korban Perempuan (KDRT & Kekerasan)')
ax.plot(kek_tot['Tahun'], kek_tot['Korban_Laki_Laki'], marker='s', linewidth=2, color='#457b9d', label='Korban Laki-Laki')

for i in range(len(kek_tot)):
    ax.annotate(f"{int(kek_tot['Korban_Perempuan'].iloc[i]):,} kasus", (kek_tot['Tahun'].iloc[i], kek_tot['Korban_Perempuan'].iloc[i] + 15), ha='center', fontweight='bold', color='#e63946')

ax.set_ylabel('Jumlah Kasus Kekerasan', fontweight='bold')
ax.set_xlabel('Tahun', fontweight='bold')
ax.set_title('Tren Kasus Kekerasan Menurut Jenis Kelamin di Sumsel (2022-2025)', fontsize=13, fontweight='bold', pad=15)
ax.legend(loc='upper right')
plt.tight_layout()
plt.savefig(os.path.join(charts_dir, 'domestic_violence_gender_trend.png'))
plt.close()

# 2. IMB ANEKA INVESTASI TOP REGENCIES (2025)
imb_2025 = df_imb[(df_imb['Tahun'] == 2025) & (~df_imb['Kabupaten_Kota'].str.contains('Sumatera Selatan', case=False))].sort_values('IMB_Aneka_Investasi_Juta_Rp', ascending=False).head(10)

fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
bars = ax.barh(imb_2025['Kabupaten_Kota'], imb_2025['IMB_Aneka_Investasi_Juta_Rp']/1000, color='#2a9d8f')

for bar in bars:
    w = bar.get_width()
    if w > 0:
        ax.annotate(f"Rp {w:,.1f} M", (w + 10, bar.get_y() + bar.get_height()/2), va='center', fontweight='bold', fontsize=9)

ax.set_xlabel('Nilai IMB Aneka Investasi (Miliar Rupiah)', fontweight='bold')
ax.set_title('Top 10 Izin Mendirikan Bangunan (IMB) Aneka Investasi per Kab/Kota (2025)', fontsize=13, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig(os.path.join(charts_dir, 'imb_investment_permits_2025.png'))
plt.close()

# Copy to artifacts
shutil.copy2(os.path.join(charts_dir, 'domestic_violence_gender_trend.png'), os.path.join(artifact_dir, 'domestic_violence_gender_trend.png'))
shutil.copy2(os.path.join(charts_dir, 'imb_investment_permits_2025.png'), os.path.join(artifact_dir, 'imb_investment_permits_2025.png'))

print("NEWEST BATCH CHARTS GENERATED & COPIED TO ARTIFACTS!")
