import os
import glob
import sys
import pandas as pd
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')

dataset_dir = r'd:\Analisis data Financial Sumatera Selatan\Dataset'
output_dir = r'd:\Analisis data Financial Sumatera Selatan\processed_data'
os.makedirs(output_dir, exist_ok=True)

print("=========================================================================")
print("          PARSING & AGGREGATING ALL NEWLY ADDED DATASETS                 ")
print("=========================================================================")

# ---------------------------------------------------------
# 1. PENDAPATAN PEKERJA INFORMAL (2019 - 2025)
# ---------------------------------------------------------
inf_files = sorted(glob.glob(os.path.join(dataset_dir, 'Rata-rata Pendapatan Bersih Sebulan Pekerja Informal*.csv')))
inf_rows = []

for f in inf_files:
    fname = os.path.basename(f)
    year = int(''.join(filter(str.isdigit, fname)))
    df = pd.read_csv(f, encoding='utf-8-sig', sep=None, engine='python')
    df.columns = [c.strip().replace('\ufeff', '') for c in df.columns]
    
    # Expect regency in first column
    reg_col = df.columns[0]
    
    for _, row in df.iterrows():
        reg = str(row[reg_col]).strip()
        if not reg or reg.lower() in ['nan', 'keterangan', 'catatan'] or '<sup>' in reg:
            continue
            
        rec = {'Tahun': year, 'Kabupaten_Kota': reg}
        for col in df.columns[1:]:
            v = str(row[col]).replace('.', '').replace(',', '.').replace('-', '0').strip()
            try:
                rec[col] = float(v)
            except ValueError:
                rec[col] = np.nan
        inf_rows.append(rec)

df_inf = pd.DataFrame(inf_rows)
df_inf.to_csv(os.path.join(output_dir, 'pendapatan_informal_2019_2025.csv'), index=False)
print("Pendapatan Informal Processed. Shape:", df_inf.shape)

# ---------------------------------------------------------
# 2. JUMLAH PERUSAHAAN IMK (2019 - 2022)
# ---------------------------------------------------------
imk_files = sorted(glob.glob(os.path.join(dataset_dir, 'Jumlah Perusahaan IMK*.csv')))
imk_rows = []

for f in imk_files:
    fname = os.path.basename(f)
    year = int(''.join(filter(str.isdigit, fname)))
    df = pd.read_csv(f, encoding='utf-8-sig', sep=None, engine='python')
    df.columns = [c.strip().replace('\ufeff', '') for c in df.columns]
    
    reg_col = df.columns[0]
    val_col = df.columns[1]
    
    for _, row in df.iterrows():
        reg = str(row[reg_col]).strip()
        if not reg or reg.lower() in ['nan', 'keterangan', 'catatan'] or '<sup>' in reg:
            continue
        v = str(row[val_col]).replace('.', '').replace(',', '.').replace('-', '0').strip()
        try:
            val = float(v)
        except ValueError:
            val = np.nan
        imk_rows.append({'Tahun': year, 'Kabupaten_Kota': reg, 'Jumlah_Perusahaan_IMK': val})

df_imk = pd.DataFrame(imk_rows)
df_imk.to_csv(os.path.join(output_dir, 'perusahaan_imk_2019_2022.csv'), index=False)
print("Perusahaan IMK Processed. Shape:", df_imk.shape)

# ---------------------------------------------------------
# 3. JUMLAH MURID (2019 - 2024)
# ---------------------------------------------------------
murid_files = sorted(glob.glob(os.path.join(dataset_dir, 'Jumlah Murid*.csv')))
murid_rows = []

for f in murid_files:
    fname = os.path.basename(f)
    year = int(''.join(filter(str.isdigit, fname)))
    df = pd.read_csv(f, encoding='utf-8-sig', sep=None, engine='python')
    df.columns = [c.strip().replace('\ufeff', '') for c in df.columns]
    
    # Headers are usually at row index 1: SD, MI, SMP, MTs, SMA, MA, SMK
    if len(df) > 3:
        reg_col = df.columns[0]
        # find header row
        header_idx = None
        for i in range(min(5, len(df))):
            if 'SD' in df.iloc[i].values:
                header_idx = i
                break
                
        if header_idx is not None:
            cols = [str(c).strip() for c in df.iloc[header_idx].values]
            for r_idx in range(header_idx + 2, len(df)):
                row = df.iloc[r_idx]
                reg = str(row.iloc[0]).strip()
                if not reg or reg.lower() in ['nan', 'keterangan'] or '<sup>' in reg:
                    continue
                rec = {'Tahun': year, 'Kabupaten_Kota': reg}
                for c_idx in range(1, min(len(cols), len(row))):
                    c_name = cols[c_idx]
                    if not c_name or c_name == 'nan':
                        continue
                    v = str(row.iloc[c_idx]).replace('.', '').replace(',', '.').replace('-', '0').strip()
                    try:
                        rec[c_name] = float(v)
                    except ValueError:
                        rec[c_name] = np.nan
                murid_rows.append(rec)

df_murid = pd.DataFrame(murid_rows)
df_murid.to_csv(os.path.join(output_dir, 'jumlah_murid_2019_2024.csv'), index=False)
print("Jumlah Murid Processed. Shape:", df_murid.shape)

# ---------------------------------------------------------
# 4. INVESTASI PERUSAHAAN SATU DATA SUMSEL
# ---------------------------------------------------------
f_sd = os.path.join(dataset_dir, 'Satu Data Provinsi Sumatera Selatan.csv')
if os.path.exists(f_sd):
    df_sd = pd.read_csv(f_sd, encoding='utf-8-sig', sep=None, engine='python')
    df_sd.columns = [c.strip().replace('\ufeff', '') for c in df_sd.columns]
    df_sd.to_csv(os.path.join(output_dir, 'investasi_perusahaan_sumsel.csv'), index=False)
    print("Investasi Perusahaan Processed. Shape:", df_sd.shape)

print("\nALL NEW DATASETS PROCESSED SUCCESSFULLY!")
