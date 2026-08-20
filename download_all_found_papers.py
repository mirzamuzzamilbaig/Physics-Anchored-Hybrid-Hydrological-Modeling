import json
import urllib.request
import urllib.parse
import os
import re

papers_dir = 'papers'
os.makedirs(papers_dir, exist_ok=True)

with open('search_results.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

def clean_filename(title):
    # Remove non-alphanumeric characters for safe filename
    clean = re.sub(r'[^\w\s-]', '', title)
    clean = re.sub(r'[-\s]+', '_', clean).strip('_')
    return clean[:60] + '.pdf'

downloaded_count = 0
failed_count = 0

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

for source, item_list in data.items():
    print(f"\n--- Processing {source} ({len(item_list)} papers) ---")
    for item in item_list:
        pdf_url = item.get('pdf_url')
        title = item.get('title', 'paper')
        if not pdf_url:
            print(f"Skipping (No PDF URL): {title[:50]}")
            continue

        filename = clean_filename(title)
        filepath = os.path.join(papers_dir, filename)

        if os.path.exists(filepath) and os.path.getsize(filepath) > 10000:
            print(f"Already exists: {filename}")
            downloaded_count += 1
            continue

        print(f"Downloading: {title[:50]}...")
        print(f"  URL: {pdf_url}")
        
        try:
            req = urllib.request.Request(pdf_url, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as resp:
                content = resp.read()
                if len(content) > 5000 and (content.startswith(b'%PDF') or b'pdf' in resp.headers.get('Content-Type', '').lower()):
                    with open(filepath, 'wb') as out_f:
                        out_f.write(content)
                    print(f"  [SUCCESS] Saved {filename} ({len(content)} bytes)")
                    downloaded_count += 1
                else:
                    print(f"  [SKIPPED] Non-PDF or too small ({len(content)} bytes)")
                    failed_count += 1
        except Exception as e:
            print(f"  [FAILED] Error: {e}")
            failed_count += 1

print(f"\nSummary: {downloaded_count} papers ready in '{papers_dir}', {failed_count} skipped/failed.")
