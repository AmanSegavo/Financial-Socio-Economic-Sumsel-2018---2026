import os
import glob
import sys
import pandas as pd

sys.stdout.reconfigure(encoding='utf-8')
pd.set_option('display.max_columns', 20)
pd.set_option('display.width', 1000)

dataset_dir = r'd:\Analisis data Financial Sumatera Selatan\Dataset'

print("=========================================================")
print("          INSPECTING NEWLY ADDED DATASETS               ")
print("=========================================================")

# 1. EXCEL FILES
print("\n--- 1. UPAH HISTORIS (2018-2023) ---")
f_upah = os.path.join(dataset_dir, 'data-historis-rata---rata-upah-di-sumatera-selatan-periode-2018-2023.xlsx')
if os.path.exists(f_upah):
    xl = pd.ExcelFile(f_upah)
    print("Sheets:", xl.sheet_names)
    df_u = xl.parse(xl.sheet_names[0])
    print(df_u.to_string())

print("\n--- 2. INDEKS KESEJAHTERAAN SOSIAL 2025 ---")
f_iks = os.path.join(dataset_dir, 'indeks-kesejahteraan-sosial-2025.xlsx')
if os.path.exists(f_iks):
    xl = pd.ExcelFile(f_iks)
    print("Sheets:", xl.sheet_names)
    df_iks = xl.parse(xl.sheet_names[0])
    print(df_iks.to_string())

# 2. INFORMAL INCOME CSVs
print("\n--- 3. PENDAPATAN PEKERJA INFORMAL (2019-2025) ---")
inf_files = sorted(glob.glob(os.path.join(dataset_dir, 'Rata-rata Pendapatan Bersih Sebulan Pekerja Informal*.csv')))
for f in inf_files:
    fname = os.path.basename(f)
    print(f"\nFile: {fname}")
    df = pd.read_csv(f, encoding='utf-8-sig', sep=None, engine='python')
    df.columns = [c.strip().replace('\ufeff', '') for c in df.columns]
    print("Shape:", df.shape)
    print("Columns:", list(df.columns))
    print(df.head(5).to_string())

# 3. IMK COMPANIES
print("\n--- 4. JUMLAH PERUSAHAAN IMK (2019-2022) ---")
imk_files = sorted(glob.glob(os.path.join(dataset_dir, 'Jumlah Perusahaan IMK*.csv')))
for f in imk_files:
    fname = os.path.basename(f)
    print(f"\nFile: {fname}")
    df = pd.read_csv(f, encoding='utf-8-sig', sep=None, engine='python')
    print(df.to_string())

# 4. EDUCATION / MURID
print("\n--- 5. JUMLAH MURID (2019-2024) ---")
murid_files = sorted(glob.glob(os.path.join(dataset_dir, 'Jumlah Murid*.csv')))
for f in murid_files[:2]: # show first 2
    fname = os.path.basename(f)
    print(f"\nFile: {fname}")
    df = pd.read_csv(f, encoding='utf-8-sig', sep=None, engine='python')
    print(df.to_string())

# 5. SATU DATA PROVINSI SUMSEL CSV
print("\n--- 6. SATU DATA PROVINSI SUMATERA SELATAN CSV ---")
f_sd = os.path.join(dataset_dir, 'Satu Data Provinsi Sumatera Selatan.csv')
if os.path.exists(f_sd):
    df_sd = pd.read_csv(f_sd, encoding='utf-8-sig', sep=None, engine='python')
    print(df_sd.to_string())

