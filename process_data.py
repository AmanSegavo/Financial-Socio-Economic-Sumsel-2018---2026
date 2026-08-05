import os
import glob
import sys
import pandas as pd
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')
pd.set_option('display.max_columns', 20)
pd.set_option('display.max_rows', 100)
pd.set_option('display.width', 1000)

dataset_dir = r'd:\Analisis data Financial Sumatera Selatan\Dataset'

print("=== 1. PROCESSING POPULATION DATA (2019-2026) ===")
pop_files = sorted(glob.glob(os.path.join(dataset_dir, 'Jumlah Penduduk Menurut Kelompok Umur*.csv')))

all_pop = []
for f in pop_files:
    fname = os.path.basename(f)
    year = int(''.join(filter(str.isdigit, fname)))
    df = pd.read_csv(f, encoding='utf-8-sig', sep=None, engine='python')
    df.columns = [c.strip().replace('\ufeff', '') for c in df.columns]
    
    # Identify key columns
    age_col = [c for c in df.columns if 'Kelompok Umur' in c or 'Umur' in c][0]
    male_col = [c for c in df.columns if 'Laki' in c and 'Perempuan' not in c][0]
    female_col = [c for c in df.columns if 'Perempuan' in c and 'Laki' not in c][0]
    total_col = [c for c in df.columns if ('Laki' in c and 'Perempuan' in c) or 'Jumlah' in c or 'Total' in c][0]
    
    sub = df[[age_col, male_col, female_col, total_col]].copy()
    sub.columns = ['Kelompok_Umur', 'Laki_Laki', 'Perempuan', 'Total']
    
    # Clean values (strip spaces, convert to float)
    for col in ['Laki_Laki', 'Perempuan', 'Total']:
        sub[col] = sub[col].astype(str).str.replace(',', '.').str.replace('-', '0').str.strip()
        sub[col] = pd.to_numeric(sub[col], errors='coerce')
        
    sub['Kelompok_Umur'] = sub['Kelompok_Umur'].astype(str).str.strip()
    sub = sub[sub['Kelompok_Umur'].notna() & ~sub['Kelompok_Umur'].str.contains('Keterangan|Catatan|NaN|nan', case=False)]
    sub['Tahun'] = year
    
    # Check if numbers are in Ribu or exact
    # In 2026 filename says (ribu jiwa), let's see values magnitude
    all_pop.append(sub)

pop_df = pd.concat(all_pop, ignore_index=True)
print(pop_df.head(20))
print("Years in Pop DF:", pop_df['Tahun'].unique())

print("\n=== 2. PROCESSING LABOR FORCE DATA (2019-2025) ===")
tk_files = sorted(glob.glob(os.path.join(dataset_dir, 'Keadaan Tenaga Kerja*.csv')))
all_tk = []
for f in tk_files:
    fname = os.path.basename(f)
    year = int(''.join(filter(str.isdigit, fname)))
    df = pd.read_csv(f, encoding='utf-8-sig', sep=None, engine='python')
    df.columns = [c.strip().replace('\ufeff', '') for c in df.columns]
    df['Tahun'] = year
    all_tk.append(df)

tk_df = pd.concat(all_tk, ignore_index=True)
print(tk_df.to_string())

print("\n=== 3. PROCESSING UNEMPLOYMENT RATE DATA (2019-2025) ===")
tpt_files = sorted(glob.glob(os.path.join(dataset_dir, 'Tingkat Pengangguran*.csv')))
all_tpt = []
for f in tpt_files:
    fname = os.path.basename(f)
    year = int(''.join(filter(str.isdigit, fname)))
    df = pd.read_csv(f, encoding='utf-8-sig', sep=None, engine='python')
    df.columns = [c.strip().replace('\ufeff', '') for c in df.columns]
    df['Tahun'] = year
    all_tpt.append(df)

tpt_df = pd.concat(all_tpt, ignore_index=True)
print(tpt_df.to_string())

print("\n=== 4. PROCESSING MARRIAGE AND DIVORCE DATA (2019-2025) ===")
nc_files = sorted(glob.glob(os.path.join(dataset_dir, 'Nikah dan Cerai*.csv')))
all_nc = []
for f in nc_files:
    fname = os.path.basename(f)
    year = int(''.join(filter(str.isdigit, fname)))
    df = pd.read_csv(f, encoding='utf-8-sig', sep=None, engine='python')
    df.columns = [c.strip().replace('\ufeff', '') for c in df.columns]
    df['Tahun'] = year
    print(f"Year {year} Columns:", list(df.columns))
    all_nc.append((year, df))

