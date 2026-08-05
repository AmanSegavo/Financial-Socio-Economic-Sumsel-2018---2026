import sys
import pandas as pd
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')

# Data 2023 dari Disnakertrans & BPS Sumsel
bps_tpt_2023 = 4.11
bps_penganggur_2023 = 188511
bps_angkatan_kerja_2023 = 4588170
bps_bekerja_2023 = 4399659

informal_pct = 62.97
formal_pct = 37.03

disnaker_pencaker_2023 = 20296
disnaker_lowongan_2023 = 15772
disnaker_ditempatkan_2023 = 14027

# Ratios
pct_pencaker_registered = (disnaker_pencaker_2023 / bps_penganggur_2023) * 100
pct_vacancies_vs_unemployed = (disnaker_lowongan_2023 / bps_penganggur_2023) * 100
pct_placed_vs_vacancies = (disnaker_ditempatkan_2023 / disnaker_lowongan_2023) * 100

print("=== INDIKATOR ANALISIS PASAR KERJA & TRANSPARANSI SELEKSI (2023) ===")
print(f"Total Penganggur Terbuka (BPS): {bps_penganggur_2023:,} orang")
print(f"Pencari Kerja Terdaftar di Disnakertrans (Kartu Kuning/AK-1): {disnaker_pencaker_2023:,} orang ({pct_pencaker_registered:.2f}% dari total penganggur)")
print(f"Lowongan Kerja Terdaftar Resmi di Disnakertrans: {disnaker_lowongan_2023:,} ({pct_vacancies_vs_unemployed:.2f}% dari total penganggur)")
print(f"Penempatan Tenaga Kerja Terdaftar: {disnaker_ditempatkan_2023:,} ({pct_placed_vs_vacancies:.2f}% dari lowongan terdaftar)")

# Proporsi Pekerja Informal vs Formal
bekerja_informal = bps_bekerja_2023 * (informal_pct / 100)
bekerja_formal = bps_bekerja_2023 * (formal_pct / 100)
print(f"\nPekerja Sektor Informal: {bekerja_informal:,.0f} orang ({informal_pct}%)")
print(f"Pekerja Sektor Formal: {bekerja_formal:,.0f} orang ({formal_pct}%)")

