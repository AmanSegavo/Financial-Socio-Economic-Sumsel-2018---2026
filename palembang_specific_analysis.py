import os
import sys
import pandas as pd
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')

output_dir = r'd:\Analisis data Financial Sumatera Selatan\processed_data'

df_nc = pd.read_csv(os.path.join(output_dir, 'nikah_cerai_bersih_2019_2025.csv'))
df_inf = pd.read_csv(os.path.join(output_dir, 'pendapatan_informal_2019_2025.csv'))
df_murid = pd.read_csv(os.path.join(output_dir, 'jumlah_murid_2019_2024.csv'))
df_imk = pd.read_csv(os.path.join(output_dir, 'perusahaan_imk_2019_2022.csv'))

print("=========================================================================")
print("          ANALISIS SPESIFIK DATA KOTA PALEMBANG                          ")
print("=========================================================================")

# 1. PERNIKAHAN & PERCERAIAN PALEMBANG (2019 - 2025)
nc_pal = df_nc[df_nc['Kabupaten_Kota'].str.contains('Palembang', case=False)].sort_values('Tahun').reset_index(drop=True)
print("\n--- 1. NIKAH & CERAI KOTA PALEMBANG (2019 - 2025) ---")
print(nc_pal[['Tahun', 'Nikah', 'Cerai_Talak', 'Cerai_Gugat', 'Jumlah_Cerai', 'Rasio_Cerai_Nikah_%', 'Proporsi_Cerai_Gugat_%']].to_string())

# 2. PENDAPATAN PEKERJA INFORMAL PALEMBANG
inf_pal = df_inf[df_inf['Kabupaten_Kota'].str.contains('Palembang', case=False)].sort_values('Tahun').reset_index(drop=True)
print("\n--- 2. PENDAPATAN PEKERJA INFORMAL KOTA PALEMBANG (2019 - 2025) ---")
print(inf_pal.to_string())

# 3. JUMLAH MURID PALEMBANG (2020 & 2024)
murid_pal = df_murid[df_murid['Kabupaten_Kota'].str.contains('Palembang', case=False)].sort_values('Tahun').reset_index(drop=True)
print("\n--- 3. JUMLAH MURID KOTA PALEMBANG ---")
print(murid_pal.to_string())

