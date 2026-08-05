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
nc_pal = df_nc[df_nc['Kabupaten_Kota'].str.contains('Palembang', case=False)].sort_values('Tahun')

fig, ax1 = plt.subplots(figsize=(9, 5), dpi=300)
ax1.plot(nc_pal['Tahun'], nc_pal['Nikah'], marker='o', linewidth=3, color='#2a9d8f', label='Pernikahan (Nikah)')
ax1.set_ylabel('Jumlah Pernikahan', color='#2a9d8f', fontweight='bold')
ax1.set_xlabel('Tahun', fontweight='bold')

for i, txt in enumerate(nc_pal['Nikah']):
    ax1.annotate(f"{int(txt):,}", (nc_pal['Tahun'].iloc[i], txt + 250), ha='center', fontweight='bold', color='#2a9d8f')

ax2 = ax1.twinx()
ax2.plot(nc_pal['Tahun'], nc_pal['Jumlah_Cerai'], marker='s', linewidth=3, color='#e76f51', label='Perceraian (Cerai)')
ax2.set_ylabel('Jumlah Perceraian', color='#e76f51', fontweight='bold')

for i, txt in enumerate(nc_pal['Jumlah_Cerai']):
    ax2.annotate(f"{int(txt):,}", (nc_pal['Tahun'].iloc[i], txt - 200), ha='center', fontweight='bold', color='#e76f51')

plt.title('Dinamika Pernikahan vs Perceraian di Kota Palembang (2019-2025)', fontsize=13, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig(os.path.join(charts_dir, 'palembang_marriage_divorce_trend.png'))
plt.close()

shutil.copy2(os.path.join(charts_dir, 'palembang_marriage_divorce_trend.png'), os.path.join(artifact_dir, 'palembang_marriage_divorce_trend.png'))
print("PALEMBANG CHART GENERATED AND COPIED TO ARTIFACTS!")
