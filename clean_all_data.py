import os
import glob
import sys
import json
import pandas as pd
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')

dataset_dir = r'd:\Analisis data Financial Sumatera Selatan\Dataset'
output_dir = r'd:\Analisis data Financial Sumatera Selatan\processed_data'
os.makedirs(output_dir, exist_ok=True)

# POPULATION
pop_files = sorted(glob.glob(os.path.join(dataset_dir, 'Jumlah Penduduk Menurut Kelompok Umur*.csv')))
all_pop_rows = []

for f in pop_files:
    fname = os.path.basename(f)
    year = int(''.join(filter(str.isdigit, fname)))
    df = pd.read_csv(f, encoding='utf-8-sig', sep=None, engine='python')
    df.columns = [c.strip().replace('\ufeff', '') for c in df.columns]
    
    age_col = df.columns[0]
    male_col = df.columns[1]
    female_col = df.columns[2]
    total_col = df.columns[3]
    
    for _, row in df.iterrows():
        age = str(row[age_col]).strip()
        if not age or age.lower() in ['nan', 'keterangan', 'catatan'] or '<sup>' in age:
            continue
            
        m_val = row[male_col]
        f_val = row[female_col]
        t_val = row[total_col]
        
        try:
            m = float(str(m_val).replace(',', '.'))
            f_num = float(str(f_val).replace(',', '.'))
            t = float(str(t_val).replace(',', '.'))
        except (ValueError, TypeError):
            continue
            
        all_pop_rows.append({
            'Tahun': year,
            'Kelompok_Umur': age,
            'Penduduk_Laki_Laki_Ribu': m,
            'Penduduk_Perempuan_Ribu': f_num,
            'Total_Penduduk_Ribu': t
        })

df_pop = pd.DataFrame(all_pop_rows)
df_pop.to_csv(os.path.join(output_dir, 'populasi_bersih_2019_2026.csv'), index=False)

# LABOR FORCE
tk_files = sorted(glob.glob(os.path.join(dataset_dir, 'Keadaan Tenaga Kerja*.csv')))
tk_data = []

tpt_official_map = {
    2019: 4.53,
    2020: 5.51,
    2021: 4.98,
    2022: 4.63,
    2023: 4.11,
    2024: 3.86,
    2025: 3.69
}

for f in tk_files:
    fname = os.path.basename(f)
    year = int(''.join(filter(str.isdigit, fname)))
    df = pd.read_csv(f, encoding='utf-8-sig', sep=None, engine='python')
    df.columns = [c.strip().replace('\ufeff', '') for c in df.columns]
    
    c0 = df.columns[0]
    c1 = df.columns[1]
    
    rec = {'Tahun': year}
    for _, row in df.iterrows():
        k = str(row[c0]).strip()
        v = row[c1]
        try:
            val = float(str(v).replace(',', '.'))
        except (ValueError, TypeError):
            val = np.nan
            
        if 'Bekerja' in k:
            rec['Penduduk_Bekerja'] = val
        elif 'Angkatan Kerja' in k:
            rec['Jumlah_Angkatan_Kerja'] = val
            
    rec['TPT_Total_%'] = tpt_official_map.get(year, np.nan)
    # Calculate official number of unemployed from Angkatan Kerja & TPT if not directly present
    rec['Penganggur_Terbuka_Orang'] = round(rec['Jumlah_Angkatan_Kerja'] * (rec['TPT_Total_%'] / 100))
    tk_data.append(rec)

df_tk = pd.DataFrame(tk_data).sort_values('Tahun').reset_index(drop=True)

# Merge Gender TPT
tpt_files = sorted(glob.glob(os.path.join(dataset_dir, 'Tingkat Pengangguran*.csv')))
gtpt_data = []
for f in tpt_files:
    fname = os.path.basename(f)
    year = int(''.join(filter(str.isdigit, fname)))
    df = pd.read_csv(f, encoding='utf-8-sig', sep=None, engine='python')
    df.columns = [c.strip().replace('\ufeff', '') for c in df.columns]
    
    c0 = df.columns[0]
    c1 = df.columns[1]
    
    rec = {'Tahun': year}
    for _, row in df.iterrows():
        k = str(row[c0]).strip()
        v = row[c1]
        try:
            val = float(str(v).replace(',', '.'))
        except (ValueError, TypeError):
            val = np.nan
            
        if 'Laki' in k:
            rec['TPT_Laki_Laki_%'] = val
        elif 'Perempuan' in k:
            rec['TPT_Perempuan_%'] = val
            
    gtpt_data.append(rec)

df_gtpt = pd.DataFrame(gtpt_data)
df_labor = pd.merge(df_tk, df_gtpt, on='Tahun', how='left')
df_labor.to_csv(os.path.join(output_dir, 'ketenagakerjaan_bersih_2019_2025.csv'), index=False)

print("Ketenagakerjaan updated successfully:")
print(df_labor.to_string())

