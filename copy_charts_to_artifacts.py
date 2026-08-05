import os
import shutil
import glob

source_dir = r'd:\Analisis data Financial Sumatera Selatan\charts'
artifact_dir = r'C:\Users\amans\.gemini\antigravity-ide\brain\7ee1e145-1b1f-4bfe-9b7a-287781fe4dd8'
target_charts_dir = os.path.join(artifact_dir, 'charts')

os.makedirs(target_charts_dir, exist_ok=True)

png_files = glob.glob(os.path.join(source_dir, '*.png'))
for f in png_files:
    fname = os.path.basename(f)
    dest = os.path.join(target_charts_dir, fname)
    shutil.copy2(f, dest)
    print(f"Copied {fname} -> {dest}")

print("All charts copied to artifact directory!")
