import os
import sys
import shutil
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.metrics import r2_score, mean_absolute_error

sys.stdout.reconfigure(encoding='utf-8')
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 11

output_dir = r'd:\Analisis data Financial Sumatera Selatan\processed_data'
charts_dir = r'd:\Analisis data Financial Sumatera Selatan\charts'
artifact_dir = r'C:\Users\amans\.gemini\antigravity-ide\brain\7ee1e145-1b1f-4bfe-9b7a-287781fe4dd8\charts'

# Load Clean Datasets
df_nc = pd.read_csv(os.path.join(output_dir, 'nikah_cerai_bersih_2019_2025.csv'))
df_labor = pd.read_csv(os.path.join(output_dir, 'ketenagakerjaan_bersih_2019_2025.csv'))
df_inf = pd.read_csv(os.path.join(output_dir, 'pendapatan_informal_2019_2025.csv'))
df_pop = pd.read_csv(os.path.join(output_dir, 'populasi_bersih_2019_2026.csv'))
df_kek = pd.read_csv(os.path.join(output_dir, 'kasus_kekerasan_2022_2025.csv'))

print("=========================================================================")
print("          MODEL MACHINE LEARNING PREDIKSI SUMATERA SELATAN (2026-2030)    ")
print("=========================================================================")

nc_prov = df_nc[df_nc['Kabupaten_Kota'].str.contains('Sumatera Selatan', case=False)].sort_values('Tahun').reset_index(drop=True)
inf_prov = df_inf[df_inf['Kabupaten_Kota'].str.contains('Sumatera Selatan', case=False)].sort_values('Tahun').reset_index(drop=True)
col_inf_val = [c for c in inf_prov.columns if c not in ['Tahun', 'Kabupaten_Kota']][0]
kek_prov = df_kek.groupby('Tahun')[['Korban_Perempuan', 'Total_Kasus_Kekerasan']].sum().reset_index()

future_years = np.array([2026, 2027, 2028, 2029, 2030]).reshape(-1, 1)

def train_and_forecast(X_hist, y_hist, future_years, feature_name="Metric", poly_degree=1):
    if poly_degree > 1:
        model = make_pipeline(PolynomialFeatures(poly_degree), Ridge(alpha=1.0))
    else:
        model = LinearRegression()
        
    model.fit(X_hist, y_hist)
    y_pred_hist = model.predict(X_hist)
    r2 = r2_score(y_hist, y_pred_hist)
    mae = mean_absolute_error(y_hist, y_pred_hist)
    
    y_future = model.predict(future_years)
    print(f"\n--- Model ML: {feature_name} (Degree {poly_degree}) ---")
    print(f"Metrics -> R2 Score: {r2:.4f}, MAE: {mae:.2f}")
    for yr, val in zip(future_years.flatten(), y_future):
        print(f"  Tahun {yr}: {val:,.2f}")
        
    return model, y_future, r2, mae

# 1. PERNIKAHAN SUMSEL
X_nikah = nc_prov['Tahun'].values.reshape(-1, 1)
y_nikah = nc_prov['Nikah'].values
m_nikah, f_nikah, r2_nikah, _ = train_and_forecast(X_nikah, y_nikah, future_years, "Pernikahan (Nikah) Sumsel", poly_degree=1)

# 2. PERCERAIAN SUMSEL
y_cerai = nc_prov['Jumlah_Cerai'].values
m_cerai, f_cerai, r2_cerai, _ = train_and_forecast(X_nikah, y_cerai, future_years, "Total Perceraian Sumsel", poly_degree=1)

# 3. CERAI GUGAT SUMSEL
y_gugat = nc_prov['Cerai_Gugat'].values
m_gugat, f_gugat, r2_gugat, _ = train_and_forecast(X_nikah, y_gugat, future_years, "Cerai Gugat Sumsel", poly_degree=1)

# 4. TPT SUMSEL
X_tpt = df_labor['Tahun'].values.reshape(-1, 1)
y_tpt = df_labor['TPT_Total_%'].values
m_tpt, f_tpt, r2_tpt, _ = train_and_forecast(X_tpt, y_tpt, future_years, "TPT Total (%) Sumsel", poly_degree=2)

# 5. KASUS KEKERASAN PEREMPUAN SUMSEL
X_kek = kek_prov['Tahun'].values.reshape(-1, 1)
y_kek = kek_prov['Korban_Perempuan'].values
m_kek, f_kek, r2_kek, _ = train_and_forecast(X_kek, y_kek, future_years, "Kasus Kekerasan Perempuan Sumsel", poly_degree=1)

# 6. PALEMBANG NIKAH & CERAI
nc_pal = df_nc[df_nc['Kabupaten_Kota'].str.contains('Palembang', case=False)].sort_values('Tahun').reset_index(drop=True)
X_pal = nc_pal['Tahun'].values.reshape(-1, 1)
y_pal_n = nc_pal['Nikah'].values
y_pal_c = nc_pal['Jumlah_Cerai'].values
y_pal_g = nc_pal['Cerai_Gugat'].values

_, f_pal_n, _, _ = train_and_forecast(X_pal, y_pal_n, future_years, "Pernikahan Kota Palembang", poly_degree=1)
_, f_pal_c, _, _ = train_and_forecast(X_pal, y_pal_c, future_years, "Total Perceraian Kota Palembang", poly_degree=1)
_, f_pal_g, _, _ = train_and_forecast(X_pal, y_pal_g, future_years, "Cerai Gugat Kota Palembang", poly_degree=1)

# CONSOLIDATE PREDICTIONS TABLE
df_ml = pd.DataFrame({
    'Tahun': future_years.flatten(),
    'Prediksi_Nikah_Sumsel': np.round(f_nikah),
    'Prediksi_Cerai_Sumsel': np.round(f_cerai),
    'Prediksi_Cerai_Gugat_Sumsel': np.round(f_gugat),
    'Prediksi_Rasio_Cerai_Nikah_%': np.round((f_cerai / f_nikah) * 100, 2),
    'Prediksi_TPT_Total_%': np.round(np.clip(f_tpt, 2.5, 6.0), 2),
    'Prediksi_Kasus_Kekerasan_Perempuan': np.round(f_kek),
    'Prediksi_Nikah_Palembang': np.round(f_pal_n),
    'Prediksi_Cerai_Palembang': np.round(f_pal_c),
    'Prediksi_Cerai_Gugat_Palembang': np.round(f_pal_g),
    'Prediksi_Rasio_Cerai_Palembang_%': np.round((f_pal_c / f_pal_n) * 100, 2)
})

df_ml.to_csv(os.path.join(output_dir, 'ml_forecasts_2026_2030.csv'), index=False)
print("\n=========================================================================")
print("          TABEL PROYEKSI PREDIKSI MACHINE LEARNING (2026 - 2030)         ")
print("=========================================================================")
print(df_ml.to_string())

# GENERATE ML FORECAST CHARTS
# Chart 1: ML Forecast Pernikahan vs Perceraian Sumsel
fig, ax1 = plt.subplots(figsize=(10, 5), dpi=300)
years_hist = nc_prov['Tahun'].values

ax1.plot(years_hist, y_nikah, marker='o', linewidth=2.5, color='#2a9d8f', label='Nikah Historis (2019-2025)')
ax1.plot(future_years.flatten(), f_nikah, marker='o', linestyle='--', linewidth=3, color='#06d6a0', label='Prediksi ML Nikah (2026-2030)')
ax1.set_ylabel('Jumlah Pernikahan', color='#2a9d8f', fontweight='bold')
ax1.set_xlabel('Tahun', fontweight='bold')

ax2 = ax1.twinx()
ax2.plot(years_hist, y_cerai, marker='s', linewidth=2.5, color='#e76f51', label='Cerai Historis (2019-2025)')
ax2.plot(future_years.flatten(), f_cerai, marker='s', linestyle='--', linewidth=3, color='#d90429', label='Prediksi ML Cerai (2026-2030)')
ax2.set_ylabel('Jumlah Perceraian', color='#e76f51', fontweight='bold')

plt.title('Proyeksi Machine Learning (ML): Tren Nikah & Cerai Sumsel (2026 - 2030)', fontsize=13, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig(os.path.join(charts_dir, 'ml_forecast_marriage_divorce.png'))
plt.close()

# Chart 2: ML Forecast Palembang Divorce Ratio
pal_rasio_hist = (y_pal_c / y_pal_n) * 100
pal_rasio_future = (f_pal_c / f_pal_n) * 100

fig, ax = plt.subplots(figsize=(9, 5), dpi=300)
ax.plot(nc_pal['Tahun'], pal_rasio_hist, marker='o', linewidth=2.5, color='#1d3557', label='Rasio Cerai Palembang Historis (%)')
ax.plot(future_years.flatten(), pal_rasio_future, marker='D', linestyle='--', linewidth=3, color='#e63946', label='Prediksi ML Rasio Cerai (2026-2030)')

for i, txt in enumerate(pal_rasio_future):
    ax.annotate(f"{txt:.2f}%", (future_years.flatten()[i], txt + 0.5), ha='center', fontweight='bold', color='#e63946')

ax.set_ylabel('Rasio Cerai / Nikah (%)', fontweight='bold')
ax.set_xlabel('Tahun', fontweight='bold')
ax.set_title('Proyeksi Machine Learning: Rasio Perceraian Kota Palembang Menuju 2030', fontsize=13, fontweight='bold', pad=15)
ax.legend(loc='upper left')
plt.tight_layout()
plt.savefig(os.path.join(charts_dir, 'ml_forecast_palembang_divorce.png'))
plt.close()

# Copy to artifacts
for fn in ['ml_forecast_marriage_divorce.png', 'ml_forecast_palembang_divorce.png']:
    shutil.copy2(os.path.join(charts_dir, fn), os.path.join(artifact_dir, fn))

print("ML FORECAST CHARTS GENERATED & COPIED TO ARTIFACTS!")
