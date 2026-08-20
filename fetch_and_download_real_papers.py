import urllib.request
import urllib.parse
import json
import xml.etree.ElementTree as ET
import os
import re
import glob

os.makedirs('papers', exist_ok=True)
existing_files = set(os.listdir('papers'))

def clean_filename(title):
    clean = re.sub(r'[^a-zA-Z0-9\s_]', '', title)
    words = clean.split()[:7]
    return "_".join(words) + ".pdf"

def download_file(url, filepath):
    basename = os.path.basename(filepath)
    if basename in existing_files:
        print(f"[EXISTS] {basename}", flush=True)
        return True

    # Force HTTPS
    if url.startswith('http://'):
        url = 'https://' + url[7:]

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }
    req = urllib.request.Request(url, headers=headers)
    try:
        print(f"Downloading {url} -> {basename}...", flush=True)
        with urllib.request.urlopen(req, timeout=12) as resp:
            content = resp.read()
            if len(content) > 10000 and (content.startswith(b'%PDF') or b'PDF' in content[:50]):
                with open(filepath, 'wb') as f:
                    f.write(content)
                existing_files.add(basename)
                print(f" [SUCCESS] Saved {basename} ({len(content)//1024} KB)", flush=True)
                return True
            else:
                print(f" [WARN] Invalid PDF or small content ({len(content)} bytes)", flush=True)
                return False
    except Exception as e:
        print(f" [FAIL] Error downloading {url}: {e}", flush=True)
        return False

# 1. Search arXiv for hydrology & water resources
print("\n--- Searching arXiv ---", flush=True)
arxiv_queries = [
    'all:"hydrology"',
    'all:"water management"',
    'all:"streamflow"',
    'all:"river basin"',
    'all:"groundwater"'
]

arxiv_papers = []
for q in arxiv_queries:
    url = f'https://export.arxiv.org/api/query?search_query={urllib.parse.quote(q)}&start=0&max_results=4&sortBy=submittedDate&sortOrder=descending'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            xml_data = resp.read()
        root = ET.fromstring(xml_data)
        ns = {'atom': 'http://www.w3.org/2005/Atom'}
        for entry in root.findall('atom:entry', ns):
            title = entry.find('atom:title', ns).text.strip().replace('\n', ' ')
            paper_id = entry.find('atom:id', ns).text
            pub_date = entry.find('atom:published', ns).text
            pdf_url = paper_id.replace('http://', 'https://').replace('/abs/', '/pdf/')
            if not pdf_url.endswith('.pdf'):
                pdf_url += '.pdf'
            
            fname = os.path.join('papers', clean_filename(title))
            arxiv_papers.append({
                'title': title,
                'published': pub_date,
                'pdf_url': pdf_url,
                'filename': fname
            })
    except Exception as e:
        print(f"arXiv query '{q}' error: {e}", flush=True)

# 2. Search OpenAlex for Open Access 2026 Hydrology papers with direct PDFs
print("\n--- Searching OpenAlex ---", flush=True)
openalex_papers = []
try:
    oa_url = 'https://api.openalex.org/works?search=hydrology+river+basin+water+management&filter=is_oa:true,type:article,from_publication_date:2026-01-01&sort=publication_date:desc&per-page=10'
    req = urllib.request.Request(oa_url, headers={'User-Agent': 'mailto:researcher@example.com'})
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode('utf-8'))
    for item in data.get('results', []):
        title = item.get('display_name', '')
        pub_date = item.get('publication_date', '')
        oa_loc = item.get('best_oa_location') or {}
        pdf_url = oa_loc.get('pdf_url')
        if pdf_url and title:
            fname = os.path.join('papers', clean_filename(title))
            openalex_papers.append({
                'title': title,
                'published': pub_date,
                'pdf_url': pdf_url,
                'filename': fname
            })
except Exception as e:
    print(f"OpenAlex error: {e}", flush=True)

all_papers = arxiv_papers + openalex_papers
print(f"\nTotal candidate papers list: {len(all_papers)}", flush=True)

downloaded_count = 0
for p in all_papers:
    if download_file(p['pdf_url'], p['filename']):
        downloaded_count += 1

# Generate summary catalog
pdf_files = glob.glob('papers/*.pdf')
catalog = []
for pdf in pdf_files:
    catalog.append({
        'filename': os.path.basename(pdf),
        'size_mb': round(os.path.getsize(pdf) / (1024 * 1024), 2),
        'path': os.path.abspath(pdf)
    })

with open('downloaded_catalog.json', 'w', encoding='utf-8') as f:
    json.dump(catalog, f, indent=2)

print(f"\n=== SUMMARY ===", flush=True)
print(f"Total PDFs stored in papers/ directory: {len(catalog)}", flush=True)
