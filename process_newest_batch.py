import os
import glob
import sys
import pandas as pd
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')

dataset_dir = r'd:\Analisis data Financial Sumatera Selatan\Dataset'
output_dir = r'd:\Analisis data Financial Sumatera Selatan\processed_data'

# KEKERASAN CSVs
kek_files = sorted(glob.glob(os.path.join(dataset_dir, 'Jumlah Kasus Kekerasan Menurut Kabupaten Kota*.csv')))
kek_rows = []

for f in kek_files:
    fname = os.path.basename(f)
    year = int(''.join(filter(str.isdigit, fname)))
    df = pd.read_csv(f, encoding='utf-8-sig', sep=None, engine='python')
    df.columns = [c.strip().replace('\ufeff', '') for c in df.columns]
    
    # check columns
    reg_col = df.columns[0]
    
    # find male, female, total columns
    m_c = [c for c in df.columns if 'Laki' in c]
    f_c = [c for c in df.columns if 'Perempuan' in c]
    t_c = [c for c in df.columns if 'Jumlah' in c or 'Total' in c]
    
    for _, row in df.iterrows():
        reg = str(row[reg_col]).strip()
        if not reg or reg.lower() in ['nan', 'keterangan', 'catatan'] or '<sup>' in reg:
            continue
            
        def clean_n(v):
            try:
                return float(str(v).replace('.', '').replace(',', '.').replace('-', '0').strip())
            except ValueError:
                return 0.0
                
        l = clean_n(row[m_c[0]]) if m_c else 0.0
        p = clean_n(row[f_c[0]]) if f_c else 0.0
        t = clean_n(row[t_c[0]]) if t_c else (l + p)
        
        kek_rows.append({
            'Tahun': year,
            'Kabupaten_Kota': reg,
            'Korban_Laki_Laki': l,
            'Korban_Perempuan': p,
            'Total_Kasus_Kekerasan': t
        })

df_kek = pd.DataFrame(kek_rows)
df_kek.to_csv(os.path.join(output_dir, 'kasus_kekerasan_2022_2025.csv'), index=False)
print("Kasus Kekerasan Processed. Shape:", df_kek.shape)

# IMB ANEKA INVESTASI
imb_files = sorted(glob.glob(os.path.join(dataset_dir, 'IMB Aneka Investasi*.csv')))
imb_rows = []

for f in imb_files:
    fname = os.path.basename(f)
    year = int(''.join(filter(str.isdigit, fname)))
    df = pd.read_csv(f, encoding='utf-8-sig', sep=None, engine='python')
    df.columns = [c.strip().replace('\ufeff', '') for c in df.columns]
    
    reg_col = df.columns[0]
    
    # find row index where data starts
    data_start = 0
    for i in range(min(5, len(df))):
        if 'Sumatera Selatan' in str(df.iloc[i, 0]) or 'Ogan Komering Ulu' in str(df.iloc[i, 0]):
            data_start = i
            break
            
    for r_idx in range(data_start, len(df)):
        row = df.iloc[r_idx]
        reg = str(row.iloc[0]).strip()
        if not reg or reg.lower() in ['nan', 'keterangan'] or '<sup>' in reg:
            continue
            
        # value is last column
        v_raw = str(row.iloc[-1]).replace('.', '').replace(',', '.').replace('-', '0').strip()
        try:
            v = float(v_raw)
        except ValueError:
            v = 0.0
            
        imb_rows.append({'Tahun': year, 'Kabupaten_Kota': reg, 'IMB_Aneka_Investasi_Juta_Rp': v})

df_imb = pd.DataFrame(imb_rows)
df_imb.to_csv(os.path.join(output_dir, 'imb_aneka_investasi_2019_2025.csv'), index=False)
print("IMB Investasi Processed. Shape:", df_imb.shape)

print("ALL NEWEST DATASETS PROCESSED SUCCESSFULLY!")
