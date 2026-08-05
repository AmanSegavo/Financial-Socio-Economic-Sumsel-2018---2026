import pypdf
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

pdf_path = r'd:\Analisis data Financial Sumatera Selatan\Dataset\6a0bbf8ccc7fb.pdf'
reader = pypdf.PdfReader(pdf_path)

keywords = ['lowongan', 'pencari kerja', 'penempatan', 'bkk', 'lptks', 'pengaduan', 'perselisihan', 'pendidikan', 'informal', 'formal', 'kTK', 'orang dalam', 'nepotisme', 'syarat']

print(f"Total Pages in PDF: {len(reader.pages)}")

found_text = []

for i, page in enumerate(reader.pages):
    text = page.extract_text()
    if not text:
        continue
        
    text_lower = text.lower()
    matches = [kw for kw in keywords if kw in text_lower]
    if matches:
        found_text.append({
            'page': i + 1,
            'matches': matches,
            'snippet': text[:1000]
        })

print(f"Found matches on {len(found_text)} pages.")
for item in found_text[:15]:
    print(f"\n=== PAGE {item['page']} (Matches: {item['matches']}) ===")
    print(item['snippet'])

