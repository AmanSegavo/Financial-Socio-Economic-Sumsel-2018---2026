import os
import glob
import sys
import json
import pandas as pd

sys.stdout.reconfigure(encoding='utf-8')

dataset_dir = r'd:\Analisis data Financial Sumatera Selatan\Dataset'

print("==================================================")
print("           EXPLORING DATASET CONTENTS            ")
print("==================================================")

csv_files = sorted(glob.glob(os.path.join(dataset_dir, '*.csv')))

data_summary = {}

for f in csv_files:
    fname = os.path.basename(f)
    print(f"\nFILE: {fname}")
    try:
        df = pd.read_csv(f, encoding='utf-8-sig', sep=None, engine='python')
    except Exception as e:
        try:
            df = pd.read_csv(f, encoding='latin1', sep=None, engine='python')
        except Exception as e2:
            print(f"Error reading file: {e2}")
            continue
            
    # Clean column names (strip whitespace and BOM)
    df.columns = [c.strip().replace('\ufeff', '') for c in df.columns]
    
    print(f"Shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    print("Head:")
    print(df.to_string())
    
    data_summary[fname] = {
        'shape': df.shape,
        'columns': list(df.columns),
        'head': df.head(5).to_dict(orient='records')
    }

print("\n==================================================")
print("          CHECKING PDF FILE: 6a0bbf8ccc7fb.pdf   ")
print("==================================================")

pdf_path = os.path.join(dataset_dir, '6a0bbf8ccc7fb.pdf')
print("PDF File Size:", os.path.getsize(pdf_path), "bytes")

pdf_text_extracted = ""

# Try various libraries
try:
    import pypdf
    reader = pypdf.PdfReader(pdf_path)
    print(f"pypdf: Total pages = {len(reader.pages)}")
    for i, page in enumerate(reader.pages[:10]): # check first 10 pages
        text = page.extract_text()
        print(f"--- Page {i+1} ---")
        print(text[:300] if text else "[No text / Image page]")
except Exception as e:
    print("pypdf error / not available:", e)

try:
    import pdfplumber
    with pdfplumber.open(pdf_path) as pdf:
        print(f"pdfplumber: Total pages = {len(pdf.pages)}")
        for i, page in enumerate(pdf.pages[:5]):
            text = page.extract_text()
            print(f"--- Page {i+1} ---")
            print(text[:300] if text else "[No text / Image page]")
except Exception as e:
    print("pdfplumber error / not available:", e)

try:
    import fitz # PyMuPDF
    doc = fitz.open(pdf_path)
    print(f"fitz (PyMuPDF): Total pages = {len(doc)}")
    for i in range(min(5, len(doc))):
        print(f"--- Page {i+1} ---")
        print(doc[i].get_text()[:300])
except Exception as e:
    print("fitz error / not available:", e)

