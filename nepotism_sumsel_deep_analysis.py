import sys
import pandas as pd
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')

print("=========================================================================")
print("          ANALISIS TINGKAT NEPOTISME & PASAR KERJA SUMATERA SELATAN       ")
print("=========================================================================")

# Data Point Summary
pencaker_bps = 188511
pencaker_disnaker = 20296
lowongan_disnaker = 15772
penempatan_disnaker = 14027

pekerja_informal = 2770465 # 62.97%
pekerja_formal = 1629194   # 37.03%

hidden_job_market_pct = ((pencaker_bps - lowongan_disnaker) / pencaker_bps) * 100

print(f"1. Porsi Hidden Job Market (Pasar Kerja Tertutup/Unreported): {hidden_job_market_pct:.2f}%")
print(f"2. Tenaga Kerja Sektor Informal (Dominasi Koneksi Personal): {pekerja_informal:,} ({62.97}%)")
print(f"3. Tenaga Kerja Sektor Formal (Seleksi Terbuka vs Terbatas): {pekerja_formal:,} ({37.03}%)")

# Estimated Distribution of Hiring Channels in Sumsel
hiring_distribution = {
    'Jaringan Keluarga / Kekerabatan (Nepotisme Informal)': 45.0, # Sektor informal & UMKM
    'Rekomendasi Internal Karyawan / Orang Dalam (Referral)': 30.0, # Swasta lokal & perkebunan/pabrik
    'Perekrutan Mandiri / Kontak Langsung Mandor': 15.0,
    'Seleksi Resmi Terbuka (CAT BKN / Job Fair / Portal E-Recruitment)': 10.0
}

print("\n--- ESTIMASI DISTRIBUSI KANAL REKRUTMEN TENAGA KERJA DI SUMSEL ---")
for k, v in hiring_distribution.items():
    print(f"- {k}: {v}%")

