import urllib.request
import json
import xml.etree.ElementTree as ET
import os
import re

os.makedirs('papers', exist_ok=True)
existing_files = set(os.listdir('papers'))

def clean_filename(title):
    clean = re.sub(r'[^a-zA-Z0-9\s_]', '', title)
    words = clean.split()[:7]
    return "_".join(words) + ".pdf"

def download_pdf(url, target_filename):
    basename = os.path.basename(target_filename)
    if basename in existing_files:
        print(f"[SKIP] Already exists: {basename}", flush=True)
        return True
    
    # Ensure https
    if url.startswith('http://'):
        url = 'https://' + url[7:]

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    req = urllib.request.Request(url, headers=headers)
    try:
        print(f"Downloading: {basename} ...", flush=True)
        with urllib.request.urlopen(req, timeout=15) as resp:
            content = resp.read()
            if len(content) > 10000 and (content.startswith(b'%PDF') or b'PDF' in content[:50]):
                with open(target_filename, 'wb') as f:
                    f.write(content)
                existing_files.add(basename)
                print(f" [SUCCESS] Saved {basename} ({len(content)//1024} KB)", flush=True)
                return True
            else:
                print(f" [WARN] Not a PDF or too small ({len(content)} bytes)", flush=True)
                return False
    except Exception as e:
        print(f" [FAIL] Could not download {url}: {e}", flush=True)
        return False

# Search arXiv for hydrology papers
print("Searching arXiv for recent papers...", flush=True)
url = 'https://export.arxiv.org/api/query?search_query=all:%22hydrology%22+OR+all:%22river+basin%22+OR+all:%22water+management%22&start=0&max_results=12&sortBy=submittedDate&sortOrder=descending'
req = urllib.request.Request(url, headers={'User-Agent': 'Python-Hydrology-Search/3.0'})

papers_to_download = []
try:
    with urllib.request.urlopen(req, timeout=15) as resp:
        xml_data = resp.read()
    root = ET.fromstring(xml_data)
    ns = {'atom': 'http://www.w3.org/2005/Atom'}
    for entry in root.findall('atom:entry', ns):
        title = entry.find('atom:title', ns).text.strip().replace('\n', ' ')
        paper_id = entry.find('atom:id', ns).text
        published = entry.find('atom:published', ns).text
        pdf_url = paper_id.replace('/abs/', '/pdf/')
        if not pdf_url.endswith('.pdf'):
            pdf_url += '.pdf'
        filename = os.path.join('papers', clean_filename(title))
        papers_to_download.append({'title': title, 'pdf_url': pdf_url, 'filename': filename, 'published': published})
except Exception as e:
        print(f"Error fetching arXiv: {e}", flush=True)

# Add curated Open Access papers
papers_to_download.extend([
    {
        'title': 'Water Bankruptcy: The Formal Definition and Hydrological Framework',
        'pdf_url': 'https://www.frontiersin.org/journals/water/articles/10.3389/frwa.2026.1850123/pdf',
        'filename': 'papers/Water_Bankruptcy_Formal_Definition_2026.pdf',
        'published': '2026-01-01'
    },
    {
        'title': 'Predictability of large-scale extreme droughts from global bias-corrected seasonal forecasts',
        'pdf_url': 'https://www.frontiersin.org/journals/water/articles/10.3389/frwa.2026.1911791/pdf',
        'filename': 'papers/Weber_2026_Predictability_Extreme_Droughts.pdf',
        'published': '2026-08-10'
    },
    {
        'title': 'Comparing crop evapotranspiration estimation methods in San Joaquin Valley',
        'pdf_url': 'https://www.frontiersin.org/journals/water/articles/10.3389/frwa.2026.1879797/pdf',
        'filename': 'papers/Kandhway_2026_Evapotranspiration_San_Joaquin.pdf',
        'published': '2026-08-10'
    }
])

print(f"Total papers queued for download: {len(papers_to_download)}", flush=True)
success_count = 0
for p in papers_to_download:
    if download_pdf(p['pdf_url'], p['filename']):
        success_count += 1

print(f"\nDone! Successfully processed {success_count} papers.", flush=True)
