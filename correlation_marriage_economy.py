import os
import sys
import pandas as pd
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')

output_dir = r'd:\Analisis data Financial Sumatera Selatan\processed_data'

df_nc = pd.read_csv(os.path.join(output_dir, 'nikah_cerai_bersih_2019_2025.csv'))
df_labor = pd.read_csv(os.path.join(output_dir, 'ketenagakerjaan_bersih_2019_2025.csv'))
df_inf = pd.read_csv(os.path.join(output_dir, 'pendapatan_informal_2019_2025.csv'))
df_pop = pd.read_csv(os.path.join(output_dir, 'populasi_bersih_2019_2026.csv'))

# Sumsel Level Time Series (2019 - 2025)
nc_prov = df_nc[df_nc['Kabupaten_Kota'].str.contains('Sumatera Selatan', case=False)].sort_values('Tahun').reset_index(drop=True)
inf_prov = df_inf[df_inf['Kabupaten_Kota'].str.contains('Sumatera Selatan', case=False)].sort_values('Tahun').reset_index(drop=True)

# Merge Time Series
df_ts = pd.merge(nc_prov[['Tahun', 'Nikah', 'Jumlah_Cerai', 'Cerai_Gugat', 'Cerai_Talak', 'Rasio_Cerai_Nikah_%', 'Proporsi_Cerai_Gugat_%']], 
                 df_labor[['Tahun', 'Penduduk_Bekerja', 'Jumlah_Angkatan_Kerja', 'TPT_Total_%', 'TPT_Laki_Laki_%', 'TPT_Perempuan_%']], 
                 on='Tahun', how='inner')

col_inf_val = [c for c in inf_prov.columns if c not in ['Tahun', 'Kabupaten_Kota']][0]
df_ts = pd.merge(df_ts, inf_prov[['Tahun', col_inf_val]], on='Tahun', how='left')
df_ts.rename(columns={col_inf_val: 'Pendapatan_Informal_Bulan'}, inplace=True)

# Merge Population Totals
pop_tot = df_pop[df_pop['Kelompok_Umur'].str.contains('Jumlah|Total', case=False)].sort_values('Tahun')[['Tahun', 'Total_Penduduk_Ribu']]
df_ts = pd.merge(df_ts, pop_tot, on='Tahun', how='left')

# Calculate Marriage Rate per 1,000 population (Angka Pernikahan Kasar / Crude Marriage Rate)
df_ts['Marriage_Rate_per_1000'] = (df_ts['Nikah'] / (df_ts['Total_Penduduk_Ribu']))

print("=========================================================================")
print("          TIME SERIES DATA KORELASI PERNIKAHAN & EKONOMI SUMSEL          ")
print("=========================================================================")
print(df_ts.to_string())

print("\n--- MATRIKS KORELASI PEARSON (r) ---")
corr_cols = ['Nikah', 'Marriage_Rate_per_1000', 'Jumlah_Cerai', 'Rasio_Cerai_Nikah_%', 'TPT_Total_%', 'TPT_Laki_Laki_%', 'TPT_Perempuan_%', 'Pendapatan_Informal_Bulan', 'Total_Penduduk_Ribu']
corr_matrix = df_ts[corr_cols].corr()
print(corr_matrix[['Nikah', 'Marriage_Rate_per_1000', 'Jumlah_Cerai', 'Rasio_Cerai_Nikah_%']].to_string())

# REGIONAL CROSS-SECTIONAL CORRELATION (2025)
nc_2025 = df_nc[(df_nc['Tahun'] == 2025) & (~df_nc['Kabupaten_Kota'].str.contains('Sumatera Selatan', case=False))].copy()
inf_2025 = df_inf[(df_inf['Tahun'] == 2025) & (~df_inf['Kabupaten_Kota'].str.contains('Sumatera Selatan', case=False))].copy()
pop_2025 = df_pop[(df_pop['Tahun'] == 2025) & (df_pop['Kelompok_Umur'].str.contains('Jumlah|Total', case=False))].copy()

df_reg_2025 = pd.merge(nc_2025, inf_2025[['Kabupaten_Kota', col_inf_val]], on='Kabupaten_Kota', how='inner')
df_reg_2025.rename(columns={col_inf_val: 'Pendapatan_Informal_2025'}, inplace=True)

print("\n--- KORELASI REGIONAL PER KABUPATEN/KOTA (2025) ---")
print("Korelasi Pendapatan Informal vs Rasio Cerai/Nikah:")
print(df_reg_2025[['Nikah', 'Jumlah_Cerai', 'Rasio_Cerai_Nikah_%', 'Proporsi_Cerai_Gugat_%', 'Pendapatan_Informal_2025']].corr()['Pendapatan_Informal_2025'].to_string())

