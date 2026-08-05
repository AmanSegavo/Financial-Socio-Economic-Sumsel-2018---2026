import os
import glob
import sys
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sys.stdout.reconfigure(encoding='utf-8')
sns.set_theme(style="whitegrid")
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'

dataset_dir = r'd:\Analisis data Financial Sumatera Selatan\Dataset'
output_dir = r'd:\Analisis data Financial Sumatera Selatan\processed_data'
charts_dir = r'd:\Analisis data Financial Sumatera Selatan\charts'
os.makedirs(output_dir, exist_ok=True)
os.makedirs(charts_dir, exist_ok=True)

# ---------------------------------------------------------
# 1. PROCESS POPULATION DATA (2019-2026)
# ---------------------------------------------------------
pop_files = sorted(glob.glob(os.path.join(dataset_dir, 'Jumlah Penduduk Menurut Kelompok Umur*.csv')))
pop_records = []

for f in pop_files:
    fname = os.path.basename(f)
    year = int(''.join(filter(str.isdigit, fname)))
    df = pd.read_csv(f, encoding='utf-8-sig', sep=None, engine='python')
    df.columns = [c.strip().replace('\ufeff', '') for c in df.columns]
    
    age_col = [c for c in df.columns if 'Kelompok Umur' in c or 'Umur' in c][0]
    male_col = [c for c in df.columns if 'Laki' in c and 'Perempuan' not in c][0]
    female_col = [c for c in df.columns if 'Perempuan' in c and 'Laki' not in c][0]
    total_col = [c for c in df.columns if ('Laki' in c and 'Perempuan' in c) or 'Jumlah' in c or 'Total' in c][0]
    
    for idx, row in df.iterrows():
        age_group = str(row[age_col]).strip()
        if not age_group or age_group.lower() in ['nan', 'keterangan', 'catatan'] or '<sup>' in age_group:
            continue
        
        m_val = str(row[male_col]).replace(',', '.').replace('-', '0').strip()
        f_val = str(row[female_col]).replace(',', '.').replace('-', '0').strip()
        t_val = str(row[total_col]).replace(',', '.').replace('-', '0').strip()
        
        try:
            m = float(m_val)
            f_num = float(f_val)
            t = float(t_val)
        except ValueError:
            continue
            
        pop_records.append({
            'Tahun': year,
            'Kelompok_Umur': age_group,
            'Laki_Laki': m,
            'Perempuan': f_num,
            'Total': t
        })

df_pop = pd.DataFrame(pop_records)
df_pop.to_csv(os.path.join(output_dir, 'populasi_2019_2026.csv'), index=False)

# Summarize Population yearly totals
pop_yearly = df_pop[df_pop['Kelompok_Umur'].str.contains('Jumlah|Total', case=False)].copy()
pop_yearly = pop_yearly.sort_values('Tahun').reset_index(drop=True)
pop_yearly['Growth_%'] = pop_yearly['Total'].pct_change() * 100
pop_yearly['Rasio_Gender_L_P'] = (pop_yearly['Laki_Laki'] / pop_yearly['Perempuan']) * 100

print("\n--- RINGKASAN POPULASI TAHUNAN ---")
print(pop_yearly.to_string())

# ---------------------------------------------------------
# 2. PROCESS LABOR FORCE & UNEMPLOYMENT (2019-2025)
# ---------------------------------------------------------
tk_files = sorted(glob.glob(os.path.join(dataset_dir, 'Keadaan Tenaga Kerja*.csv')))
tk_records = []

for f in tk_files:
    fname = os.path.basename(f)
    year = int(''.join(filter(str.isdigit, fname)))
    df = pd.read_csv(f, encoding='utf-8-sig', sep=None, engine='python')
    df.columns = [c.strip().replace('\ufeff', '') for c in df.columns]
    
    col_name = df.columns[0]
    val_col = df.columns[1]
    
    record = {'Tahun': year}
    for idx, row in df.iterrows():
        k = str(row[col_name]).strip()
        v = str(row[val_col]).strip().replace(',', '.')
        try:
            val = float(v)
        except ValueError:
            val = np.nan
            
        if 'Bekerja' in k:
            record['Penduduk_Bekerja'] = int(val) if pd.notna(val) else None
        elif 'Penganggur' in k:
            record['Penganggur'] = int(val) if pd.notna(val) else None
        elif 'Angkatan Kerja' in k:
            record['Jumlah_Angkatan_Kerja'] = int(val) if pd.notna(val) else None
        elif 'Tingkat Pengangguran' in k:
            record['TPT_Total'] = val
            
    tk_records.append(record)

df_tk = pd.DataFrame(tk_records).sort_values('Tahun').reset_index(drop=True)

# Merge gender unemployment rate
tpt_files = sorted(glob.glob(os.path.join(dataset_dir, 'Tingkat Pengangguran*.csv')))
gender_tpt = []
for f in tpt_files:
    fname = os.path.basename(f)
    year = int(''.join(filter(str.isdigit, fname)))
    df = pd.read_csv(f, encoding='utf-8-sig', sep=None, engine='python')
    df.columns = [c.strip().replace('\ufeff', '') for c in df.columns]
    
    g_col = df.columns[0]
    v_col = df.columns[1]
    
    tpt_m, tpt_f = None, None
    for idx, row in df.iterrows():
        g = str(row[g_col]).strip()
        v = str(row[v_col]).strip().replace(',', '.')
        try:
            val = float(v)
        except ValueError:
            val = None
            
        if 'Laki' in g:
            tpt_m = val
        elif 'Perempuan' in g:
            tpt_f = val
            
    gender_tpt.append({'Tahun': year, 'TPT_Laki_Laki': tpt_m, 'TPT_Perempuan': tpt_f})

df_gtpt = pd.DataFrame(gender_tpt)
df_labor = pd.merge(df_tk, df_gtpt, on='Tahun', how='left')
df_labor.to_csv(os.path.join(output_dir, 'ketenagakerjaan_2019_2025.csv'), index=False)

print("\n--- RINGKASAN KETENAGAKERJAAN & TPT ---")
print(df_labor.to_string())

# ---------------------------------------------------------
# 3. PROCESS MARRIAGE AND DIVORCE DATA (2019-2025)
# ---------------------------------------------------------
nc_files = sorted(glob.glob(os.path.join(dataset_dir, 'Nikah dan Cerai*.csv')))
nc_records = []

for f in nc_files:
    fname = os.path.basename(f)
    year = int(''.join(filter(str.isdigit, fname)))
    df = pd.read_csv(f, encoding='utf-8-sig', sep=None, engine='python')
    df.columns = [c.strip().replace('\ufeff', '') for c in df.columns]
    
    reg_col = df.columns[0]
    nikah_col = df.columns[1]
    talak_col = df.columns[2]
    gugat_col = df.columns[3]
    total_cerai_col = df.columns[4]
    
    for idx, row in df.iterrows():
        reg = str(row[reg_col]).strip()
        if not reg or reg.lower() in ['nan', 'keterangan', 'catatan'] or '<sup>' in reg:
            continue
            
        n_val = str(row[nikah_col]).replace('.', '').replace(',', '.').replace('-', '0').strip()
        t_val = str(row[talak_col]).replace('.', '').replace(',', '.').replace('-', '0').strip()
        g_val = str(row[gugat_col]).replace('.', '').replace(',', '.').replace('-', '0').strip()
        tc_val = str(row[total_cerai_col]).replace('.', '').replace(',', '.').replace('-', '0').strip()
        
        try:
            nikah = float(n_val) if n_val != '...' else np.nan
            talak = float(t_val) if t_val != '...' else np.nan
            gugat = float(g_val) if g_val != '...' else np.nan
            tc = float(tc_val) if tc_val != '...' else np.nan
        except ValueError:
            continue
            
        nc_records.append({
            'Tahun': year,
            'Kabupaten_Kota': reg,
            'Nikah': nikah,
            'Cerai_Talak': talak,
            'Cerai_Gugat': gugat,
            'Jumlah_Cerai': tc
        })

df_nc = pd.DataFrame(nc_records)
df_nc['Rasio_Cerai_Nikah_%'] = (df_nc['Jumlah_Cerai'] / df_nc['Nikah']) * 100
df_nc['Proporsi_Cerai_Gugat_%'] = (df_nc['Cerai_Gugat'] / df_nc['Jumlah_Cerai']) * 100

df_nc.to_csv(os.path.join(output_dir, 'nikah_cerai_2019_2025.csv'), index=False)

print("\n--- RINGKASAN NIKAH CERAI PER TAHUN (TOTAL SUMSEL) ---")
df_nc_sumsel = df_nc[df_nc['Kabupaten_Kota'].str.contains('Sumatera Selatan', case=False)].sort_values('Tahun').reset_index(drop=True)
print(df_nc_sumsel.to_string())

print("\n--- 5 KABUPATEN/KOTA DENGAN CASING CERAI TERTINGGI (2024-2025) ---")
df_nc_reg = df_nc[~df_nc['Kabupaten_Kota'].str.contains('Sumatera Selatan', case=False)]
top_divorce = df_nc_reg[df_nc_reg['Tahun'] == 2025].sort_values('Jumlah_Cerai', ascending=False)
print(top_divorce[['Kabupaten_Kota', 'Nikah', 'Jumlah_Cerai', 'Cerai_Gugat', 'Cerai_Talak', 'Rasio_Cerai_Nikah_%', 'Proporsi_Cerai_Gugat_%']].head(10).to_string())

