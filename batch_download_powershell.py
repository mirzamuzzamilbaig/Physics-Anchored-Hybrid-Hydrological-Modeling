import urllib.request
import json
import xml.etree.ElementTree as ET
import os
import re
import subprocess

os.makedirs('papers', exist_ok=True)
existing_files = set(os.listdir('papers'))

def clean_filename(title):
    clean = re.sub(r'[^a-zA-Z0-9\s_]', '', title)
    words = clean.split()[:7]
    return "_".join(words) + ".pdf"

# List of target papers with direct PDF links
target_papers = [
    {
        'title': 'Rainfall Sensing via Mobile Communication Signals and Environmental Modeling',
        'url': 'https://arxiv.org/pdf/2608.16088v1',
        'filename': 'papers/Rainfall_Sensing_Mobile_Communication_Signals_2026.pdf'
    },
    {
        'title': 'Graph Neural Networks for Catchment-Scale Hydrological and Runoff Forecasting',
        'url': 'https://arxiv.org/pdf/2608.14022v1',
        'filename': 'papers/Graph_Neural_Networks_Catchment_Hydrology_2026.pdf'
    },
    {
        'title': 'Machine Learning for Flash Flood Early Warning in Complex River Basins',
        'url': 'https://arxiv.org/pdf/2608.09501v1',
        'filename': 'papers/Machine_Learning_Flash_Flood_Warning_2026.pdf'
    },
    {
        'title': 'High-Resolution Satellite Soil Moisture Assimilation in SWAT Hydrological Model',
        'url': 'https://arxiv.org/pdf/2608.08210v1',
        'filename': 'papers/Satellite_Soil_Moisture_SWAT_Hydrology_2026.pdf'
    },
    {
        'title': 'Groundwater Depletion and Salinization dynamics in Managed Coastal Aquifers',
        'url': 'https://arxiv.org/pdf/2608.06543v1',
        'filename': 'papers/Groundwater_Depletion_Salinization_Coastal_Aquifers_2026.pdf'
    },
    {
        'title': 'Water Bankruptcy: The Formal Definition and Hydrological Management Framework',
        'url': 'https://www.frontiersin.org/journals/water/articles/10.3389/frwa.2026.1850123/pdf',
        'filename': 'papers/Water_Bankruptcy_Formal_Definition_2026.pdf'
    },
    {
        'title': 'Predictability of large-scale extreme droughts from global bias-corrected seasonal forecasts',
        'url': 'https://www.frontiersin.org/journals/water/articles/10.3389/frwa.2026.1911791/pdf',
        'filename': 'papers/Weber_2026_Predictability_Extreme_Droughts.pdf'
    },
    {
        'title': 'Comparing crop evapotranspiration estimation methods to evaluate water saving potential',
        'url': 'https://www.frontiersin.org/journals/water/articles/10.3389/frwa.2026.1879797/pdf',
        'filename': 'papers/Kandhway_2026_Evapotranspiration_San_Joaquin.pdf'
    }
]

# Fetch 6 more dynamic papers from arXiv
print("Searching arXiv for latest 2026 papers...", flush=True)
url = 'https://export.arxiv.org/api/query?search_query=all:%22hydrology%22+OR+all:%22water+management%22+OR+all:%22streamflow%22&start=0&max_results=8&sortBy=submittedDate&sortOrder=descending'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, timeout=15) as resp:
        xml_data = resp.read()
    root = ET.fromstring(xml_data)
    ns = {'atom': 'http://www.w3.org/2005/Atom'}
    for entry in root.findall('atom:entry', ns):
        title = entry.find('atom:title', ns).text.strip().replace('\n', ' ')
        paper_id = entry.find('atom:id', ns).text
        pdf_url = paper_id.replace('/abs/', '/pdf/')
        if not pdf_url.endswith('.pdf'):
            pdf_url += '.pdf'
        filename = os.path.join('papers', clean_filename(title))
        target_papers.append({
            'title': title,
            'url': pdf_url,
            'filename': filename
        })
except Exception as e:
    print(f"arXiv search error: {e}", flush=True)

print(f"\nProcessing {len(target_papers)} papers...", flush=True)

success_count = 0
for p in target_papers:
    fname = p['filename']
    basename = os.path.basename(fname)
    if basename in existing_files:
        print(f"[EXISTS] {basename}", flush=True)
        success_count += 1
        continue
    
    url = p['url']
    if url.startswith('http://'):
        url = 'https://' + url[7:]
        
    print(f"Downloading {basename}...", flush=True)
    cmd = f'powershell -Command "Invoke-WebRequest -Uri \'{url}\' -OutFile \'{fname}\' -UserAgent \'Mozilla/5.0\'"'
    try:
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=25)
        if os.path.exists(fname) and os.path.getsize(fname) > 10000:
            existing_files.add(basename)
            print(f" [SUCCESS] Downloaded {basename} ({os.path.getsize(fname)//1024} KB)", flush=True)
            success_count += 1
        else:
            if os.path.exists(fname):
                os.remove(fname)
            print(f" [FAIL] Download failed or invalid file for {basename}", flush=True)
    except Exception as e:
        print(f" [ERROR] Exception downloading {basename}: {e}", flush=True)

print(f"\nTotal valid PDFs now in papers/: {len(os.listdir('papers'))}", flush=True)
