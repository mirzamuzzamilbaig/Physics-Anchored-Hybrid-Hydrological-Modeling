import os
import json
import glob

papers_dir = 'papers'
pdf_files = glob.glob(os.path.join(papers_dir, '*.pdf'))

summary_data = []

for pdf_path in pdf_files:
    basename = os.path.basename(pdf_path)
    size_mb = round(os.path.getsize(pdf_path) / (1024 * 1024), 2)
    summary_data.append({
        'filename': basename,
        'size_mb': size_mb,
        'path': os.path.abspath(pdf_path)
    })

print(f"=== Downloaded Hydrology Papers Catalog ({len(summary_data)} PDFs) ===")
for i, item in enumerate(summary_data, 1):
    print(f"{i}. {item['filename']} ({item['size_mb']} MB)")

with open('downloaded_catalog.json', 'w', encoding='utf-8') as f:
    json.dump(summary_data, f, indent=2)
