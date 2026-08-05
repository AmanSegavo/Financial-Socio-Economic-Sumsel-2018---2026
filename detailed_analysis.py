import os
import glob
import sys
import pandas as pd
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')

dataset_dir = r'd:\Analisis data Financial Sumatera Selatan\Dataset'

print("=========================================================================")
print("          ANALISIS DATA KOMPREHENSIF PROVINSI SUMATERA SELATAN           ")
print("=========================================================================")

# 1. ANALISIS DEMOGRAFI (JUMLAH PENDUDUK 2019 - 2026)
print("\n-------------------------------------------------------------------------")
print("1. DEMOGRAFI & POPULASI (2019 - 2026)")
print("-------------------------------------------------------------------------")

pop_files = sorted(glob.glob(os.path.join(dataset_dir, 'Jumlah Penduduk Menurut Kelompok Umur*.csv')))

pop_dfs = []
for f in pop_files:
    fname = os.path.basename(f)
    # extract year
    year = [int(s) for s in fname.replace('.csv','').split() if s.isdigit()][0]
    df = pd.read_csv(f, encoding='utf-8-sig', sep=None, engine='python')
    df.columns = [c.strip().replace('\ufeff', '') for c in df.columns]
    df['Tahun'] = year
    pop_dfs.append((year, df))

print(f"Ditemukan {len(pop_dfs)} file data penduduk (2019-2026).")
for yr, df in pop_dfs:
    print(f"\n--- Tahun {yr} --- (Columns: {list(df.columns)})")
    print(df.to_string())

# 2. ANALISIS TENAGA KERJA (KEADAAN TENAGA KERJA 2019 - 2025)
print("\n-------------------------------------------------------------------------")
print("2. KEADAAN TENAGA KERJA (2019 - 2025)")
print("-------------------------------------------------------------------------")

tk_files = sorted(glob.glob(os.path.join(dataset_dir, 'Keadaan Tenaga Kerja*.csv')))
tk_dfs = []
for f in tk_files:
    fname = os.path.basename(f)
    year = [int(s) for s in fname.replace('.csv','').split() if s.isdigit()][0]
    df = pd.read_csv(f, encoding='utf-8-sig', sep=None, engine='python')
    df.columns = [c.strip().replace('\ufeff', '') for c in df.columns]
    df['Tahun'] = year
    tk_dfs.append((year, df))

print(f"Ditemukan {len(tk_dfs)} file keadaan tenaga kerja.")
for yr, df in tk_dfs:
    print(f"\n--- Tahun {yr} ---")
    print(df.to_string())

# 3. ANALISIS TINGKAT PENGANGGURAN (2019 - 2025)
print("\n-------------------------------------------------------------------------")
print("3. TINGKAT PENGANGGURAN (2019 - 2025)")
print("-------------------------------------------------------------------------")

tpt_files = sorted(glob.glob(os.path.join(dataset_dir, 'Tingkat Pengangguran*.csv')))
tpt_dfs = []
for f in tpt_files:
    fname = os.path.basename(f)
    year = [int(s) for s in fname.replace('.csv','').split() if s.isdigit()][0]
    df = pd.read_csv(f, encoding='utf-8-sig', sep=None, engine='python')
    df.columns = [c.strip().replace('\ufeff', '') for c in df.columns]
    df['Tahun'] = year
    tpt_dfs.append((year, df))

print(f"Ditemukan {len(tpt_dfs)} file tingkat pengangguran.")
for yr, df in tpt_dfs:
    print(f"\n--- Tahun {yr} ---")
    print(df.to_string())

# 4. ANALISIS NIKAH DAN CERAI (2019 - 2025)
print("\n-------------------------------------------------------------------------")
print("4. PERNIKAHAN DAN PERCERAIAN MENURUT KABUPATEN/KOTA (2019 - 2025)")
print("-------------------------------------------------------------------------")

nc_files = sorted(glob.glob(os.path.join(dataset_dir, 'Nikah dan Cerai*.csv')))
nc_dfs = []
for f in nc_files:
    fname = os.path.basename(f)
    year = [int(s) for s in fname.replace('.csv','').split() if s.isdigit()][0]
    df = pd.read_csv(f, encoding='utf-8-sig', sep=None, engine='python')
    df.columns = [c.strip().replace('\ufeff', '') for c in df.columns]
    df['Tahun'] = year
    nc_dfs.append((year, df))

print(f"Ditemukan {len(nc_dfs)} file nikah & cerai.")
for yr, df in nc_dfs:
    print(f"\n--- Tahun {yr} --- Columns: {list(df.columns)}")
    print(df.to_string())

