# Financial, Socio-Economic, & Demography Analytics - Sumatera Selatan (2018 – 2026)

![GitHub repo size](https://img.shields.io/github/repo-size/AmanSegavo/Financial-Socio-Economic-Sumsel-2018---2026)
![Dataset Count](https://img.shields.io/badge/Datasets-75%20Files-blue)
![Coverage](https://img.shields.io/badge/Coverage-17%20Regencies%2FSubcities-success)

Repository ini berisi analisis data komprehensif, dataset bersih, skrip pengolahan data Python, grafik visualisasi, dan dashboard web interaktif mengenai kondisi keuangan, ekonomi makro, investasi swasta, ketenagakerjaan, nepotisme pasar kerja, pendidikan, serta ketahanan keluarga (pernikahan, perceraian, dan KDRT) di **Provinsi Sumatera Selatan (2018 – 2026)**.

---

## 📌 Struktur Repositori

```
├── Dataset/                     # 75 file raw dataset (CSV, XLSX, PDF) dari BPS & Disnakertrans
├── processed_data/              # Dataset bersih hasil olahan & agregasi (CSV)
│   ├── populasi_bersih_2019_2026.csv
│   ├── ketenagakerjaan_bersih_2019_2025.csv
│   ├── nikah_cerai_bersih_2019_2025.csv
│   ├── pendapatan_informal_2019_2025.csv
│   ├── perusahaan_imk_2019_2022.csv
│   ├── jumlah_murid_2019_2024.csv
│   ├── investasi_perusahaan_sumsel.csv
│   ├── kasus_kekerasan_2022_2025.csv
│   └── imb_aneka_investasi_2019_2025.csv
├── charts/                      # Grafik visualisasi resolusi tinggi (PNG)
├── dashboard.html               # Master Interactive Web Dashboard (Single-page App)
├── *.py                         # Skrip pengolahan & analisis data Python
└── README.md                    # Dokumentasi utama proyek
```

---

## 📊 Rangkuman Temuan Utama Analisis

### 1. Ekonomi Makro & Investasi Corporate (Rp 15,04 Triliun)
* Pertumbuhan PDRB Sumatera Selatan tumbuh pesat **5,05% (yoy) pada 2025** dan **5,02% pada Triwulan I 2026**.
* Akumulasi investasi dari 50 korporasi swasta besar mencapai **Rp 15,04 Triliun**, didominasi oleh perkebunan kelapa sawit, industri pengolahan CPO, dan energi.

### 2. Pasar Kerja & Realitas Nepotisme (91,63% Hidden Market)
* Hanya **8,37% lowongan kerja** yang diumumkan secara resmi di Disnakertrans (15.772 lowongan vs 188.511 penganggur). Lebih dari 9 dari 10 perekrutan terjadi melalui jalur tertutup (*hidden job market*) via rekomendasi internal ("orang dalam") dan kekerabatan.
* **62,97% tenaga kerja (2,77 juta orang)** terperangkap di sektor informal dengan rata-rata penghasilan **Rp 2,15 Juta/bulan**.

### 3. Penundaan Usia Nikah & Kerentanan Perceraian (Cerai Gugat 79,8%)
* Kejadian pernikahan berkurang **24,3% (dari 66,7K di 2019 menjadi 50,5K di 2024)** seiring tren penundaan pernikahan (*delayed marriage*).
* Rasio perceraian terhadap pernikahan mencapai **22,50%**, di mana **79,8% diajukan oleh pihak istri (*Cerai Gugat*)**.
* Terdapat korelasi negatif kuat ($r = -0,568$) antara rata-rata pendapatan informal daerah dengan rasio perceraian (penelantaran ekonomi & KDRT menjadi pemicu utama gugatan cerai).

---

## 🚀 Cara Menjalankan Dashboard

Cukup buka berkas [dashboard.html](dashboard.html) di browser favorit Anda (Google Chrome, Firefox, Edge, Safari). Tidak memerlukan server backend.

---

## 🛠️ Skrip Analisis Python

```bash
# Menjalankan pemrosesan dataset bersih
python clean_all_data.py
python process_all_new_data.py
python process_newest_batch.py

# Menjalankan analisis korelasi ekonometrika
python correlation_marriage_economy.py
python nepotism_sumsel_deep_analysis.py
python palembang_specific_analysis.py

# Membuat grafik visualisasi & memperbarui dashboard HTML
python generate_charts.py
python generate_new_charts.py
python generate_marriage_economy_charts.py
python generate_newest_batch_charts.py
python build_dashboard_html_v2.py
```

---

## ✒️ Pengembang / Peneliti
* **Aman Segavo** - *Data Analytics & Financial Socio-Economic Research*
* GitHub: [AmanSegavo/Financial-Socio-Economic-Sumsel-2018---2026](https://github.com/AmanSegavo/Financial-Socio-Economic-Sumsel-2018---2026)
