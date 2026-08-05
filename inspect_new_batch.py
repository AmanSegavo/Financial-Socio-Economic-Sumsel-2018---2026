import os
import glob
import sys
import pandas as pd

sys.stdout.reconfigure(encoding='utf-8')
pd.set_option('display.max_columns', 20)
pd.set_option('display.width', 1000)

dataset_dir = r'd:\Analisis data Financial Sumatera Selatan\Dataset'

print("=========================================================")
print("          INSPECTING NEWEST BATCH OF DATASETS (75 Files)  ")
print("=========================================================")

# 1. IMB ANEKA INVESTASI (2019 - 2025)
print("\n--- 1. IMB ANEKA INVESTASI (2019 - 2025) ---")
imb_files = sorted(glob.glob(os.path.join(dataset_dir, 'IMB Aneka Investasi*.csv')))
for f in imb_files:
    fname = os.path.basename(f)
    print(f"\nFile: {fname}")
    df = pd.read_csv(f, encoding='utf-8-sig', sep=None, engine='python')
    print("Columns:", list(df.columns))
    print(df.head(5).to_string())

# 2. KASUS KEKERASAN CSVs (2022 - 2025)
print("\n--- 2. KASUS KEKERASAN CSVs (2022 - 2025) ---")
kek_files = sorted(glob.glob(os.path.join(dataset_dir, 'Jumlah Kasus Kekerasan Menurut Kabupaten Kota*.csv')))
for f in kek_files:
    fname = os.path.basename(f)
    print(f"\nFile: {fname}")
    df = pd.read_csv(f, encoding='utf-8-sig', sep=None, engine='python')
    print("Columns:", list(df.columns))
    print(df.head(5).to_string())

# 3. KEKERASAN EXCEL FILES
print("\n--- 3. KASUS KEKERASAN EXCEL FILES ---")
f_kek_b = os.path.join(dataset_dir, 'jumlah-kasus-kekerasan-menurut-kabupatenkota-dan-bentuk-kekerasan-di-provinsi-sumatera-selatan-.xlsx')
if os.path.exists(f_kek_b):
    xl = pd.ExcelFile(f_kek_b)
    print("Bentuk Kekerasan Sheets:", xl.sheet_names)
    df_kb = xl.parse(xl.sheet_names[0])
    print(df_kb.head(10).to_string())

f_kek_ad = os.path.join(dataset_dir, 'jumlah-total-kasus-dan-jumlah-korban-kekerasan-kepada-anak-dan-dewasa-menurut-kabupatenkota-dan.xlsx')
if os.path.exists(f_kek_ad):
    xl = pd.ExcelFile(f_kek_ad)
    print("Anak & Dewasa Sheets:", xl.sheet_names)
    df_ad = xl.parse(xl.sheet_names[0])
    print(df_ad.head(10).to_string())

# 4. ANGGARAN RESPONSIF GENDER (ARG) 2025
print("\n--- 4. ANGGARAN RESPONSIF GENDER (ARG) 2025 ---")
f_arg = os.path.join(dataset_dir, 'persentase-arg-anggaran-responsif-gende-2025.xlsx')
if os.path.exists(f_arg):
    xl = pd.ExcelFile(f_arg)
    print("ARG Sheets:", xl.sheet_names)
    df_arg = xl.parse(xl.sheet_names[0])
    print(df_arg.to_string())

