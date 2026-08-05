import pypdf
import sys

sys.stdout.reconfigure(encoding='utf-8')

pdf_path = r'd:\Analisis data Financial Sumatera Selatan\Dataset\6a0bbf8ccc7fb.pdf'
reader = pypdf.PdfReader(pdf_path)

print(f"Total Pages: {len(reader.pages)}")

for i in range(35, len(reader.pages)):
    text = reader.pages[i].extract_text()
    if not text:
        continue
    t_low = text.lower()
    if any(k in t_low for k in ['lowongan', 'pencari kerja', 'penempatan', 'pencaker', 'bkk', 'lptks', 'perselisihan', 'pengaduan']):
        print(f"\n==================== PAGE {i+1} ====================")
        print(text)

