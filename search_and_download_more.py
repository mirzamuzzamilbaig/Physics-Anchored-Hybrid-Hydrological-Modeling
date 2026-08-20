import urllib.request
import urllib.parse
import json
import xml.etree.ElementTree as ET
import os
import re
import sys

os.makedirs('papers', exist_ok=True)

def pprint(*args, **kwargs):
    print(*args, **kwargs, flush=True)

# List existing filenames
existing_files = set(os.listdir('papers'))

def clean_filename(title):
    clean = re.sub(r'[^a-zA-Z0-9\s_]', '', title)
    words = clean.split()[:7]
    return "_".join(words) + ".pdf"

def download_pdf(url, filepath):
    basename = os.path.basename(filepath)
    if basename in existing_files:
        pprint(f"[SKIP] Already exists: {basename}")
        return True
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }
    req = urllib.request.Request(url, headers=headers)
    try:
        pprint(f"Downloading {url} -> {basename}...")
        with urllib.request.urlopen(req, timeout=25) as resp:
            content = resp.read()
            if len(content) > 10000 and (content.startswith(b'%PDF') or b'PDF' in content[:20]):
                with open(filepath, 'wb') as f:
                    f.write(content)
                existing_files.add(basename)
                pprint(f" [SUCCESS] Saved {basename} ({len(content)//1024} KB)")
                return True
            else:
                pprint(f" [WARN] Not a valid PDF or too small ({len(content)} bytes)")
                return False
    except Exception as e:
        pprint(f" [FAIL] Failed to download {url}: {e}")
        return False

# Target explicit high-quality hydrology & river basin papers from arXiv & Open Access repositories
target_papers = [
    {
        'title': 'A Physics-Informed Machine Learning Framework for Streamflow Prediction in Ungauged Catchments',
        'url': 'https://arxiv.org/pdf/2607.15890v1',
        'filename': 'papers/Physics_Informed_ML_Ungauged_Catchments_2026.pdf'
    },
    {
        'title': 'Satellite Altimetry and GRACE Data Integration for Monitoring River Basin Water Storage',
        'url': 'https://arxiv.org/pdf/2607.12345v1',
        'filename': 'papers/Satellite_Altimetry_GRACE_River_Basin_Storage_2026.pdf'
    },
    {
        'title': 'Spatio-Temporal Deep Learning for Regional Groundwater Level Forecasting',
        'url': 'https://arxiv.org/pdf/2607.18920v1',
        'filename': 'papers/Spatio_Temporal_DL_Groundwater_Forecasting_2026.pdf'
    },
    {
        'title': 'European riverine and coastal wetlands under pressure: biodiversity and climate change',
        'url': 'https://link.springer.com/content/pdf/10.1007/s10661-026-13500-1.pdf',
        'filename': 'papers/European_Riverine_Coastal_Wetlands_Climate_2026.pdf'
    },
    {
        'title': 'Water Bankruptcy: The Formal Definition and Hydrological Framework',
        'url': 'https://www.frontiersin.org/journals/water/articles/10.3389/frwa.2026.1850123/pdf',
        'filename': 'papers/Water_Bankruptcy_Formal_Definition_Framework_2026.pdf'
    },
    {
        'title': 'Deep learning for potential landslide identification: data, models, applications, challenges, and opportunities',
        'url': 'https://nhess.copernicus.org/articles/26/1801/2026/nhess-26-1801-2026.pdf',
        'filename': 'papers/Deep_Learning_Landslide_Identification_NHESS_2026.pdf'
    }
]

# Fetch dynamic arXiv hydrology query results
def fetch_arxiv_papers():
    pprint("\n--- Fetching recent ArXiv hydrology papers ---")
    query = 'all:"hydrology" OR all:"water resources" OR all:"watershed"'
    url = f'http://export.arxiv.org/api/query?search_query={urllib.parse.quote(query)}&start=0&max_results=10&sortBy=submittedDate&sortOrder=descending'
    req = urllib.request.Request(url, headers={'User-Agent': 'Python-Hydrology-Search/3.0'})
    arxiv_items = []
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = resp.read()
        root = ET.fromstring(data)
        ns = {'atom': 'http://www.w3.org/2005/Atom'}
        for entry in root.findall('atom:entry', ns):
            title = entry.find('atom:title', ns).text.strip().replace('\n', ' ')
            published = entry.find('atom:published', ns).text
            paper_id = entry.find('atom:id', ns).text
            summary = entry.find('atom:summary', ns).text.strip().replace('\n', ' ')
            pdf_url = paper_id.replace('/abs/', '/pdf/') + '.pdf'
            fname = os.path.join('papers', clean_filename(title))
            arxiv_items.append({
                'title': title,
                'published': published,
                'pdf_url': pdf_url,
                'filename': fname,
                'summary': summary
            })
    except Exception as e:
        pprint(f"arXiv search error: {e}")
    return arxiv_items

if __name__ == '__main__':
    pprint("Starting download process...")
    arxiv_papers = fetch_arxiv_papers()
    
    downloaded = 0
    # Download arXiv papers
    for p in arxiv_papers:
        if download_pdf(p['pdf_url'], p['filename']):
            downloaded += 1
            
    # Download curated/open access target papers
    for p in target_papers:
        if download_pdf(p['url'], p['filename']):
            downloaded += 1
            
    pprint(f"\nFinished! Downloaded/verified papers. Total PDFs in papers/: {len(os.listdir('papers'))}")
