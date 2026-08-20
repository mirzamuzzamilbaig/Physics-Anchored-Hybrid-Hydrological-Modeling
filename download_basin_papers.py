import urllib.request
import urllib.parse
import json
import xml.etree.ElementTree as ET
import os

os.makedirs('papers', exist_ok=True)

def download_file(url, target_path):
    print(f"Downloading from {url} -> {target_path}")
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    })
    try:
        with urllib.request.urlopen(req) as resp:
            content = resp.read()
            # Verify it looks like a PDF or valid file
            if len(content) > 1000:
                with open(target_path, 'wb') as f:
                    f.write(content)
                print(f" Successfully saved {os.path.basename(target_path)} ({len(content)} bytes)")
                return True
            else:
                print(f" Warning: File too small ({len(content)} bytes)")
                return False
    except Exception as e:
        print(f" Error downloading {url}: {e}")
        return False

# Target 1: ArXiv paper on Subbasin-scale Streamflow Alteration & Waterpower/Dam Management in Large River Networks
arxiv_paper_1 = {
    'id': '2608.02363v1',
    'title': 'Network-Based Subbasin-Scale Mapping of Streamflow Alteration in Ontario, Canada',
    'authors': ['Hongren Shen', 'Bryan A. Tolson', 'James R. Craig', 'Robert A. Metcalfe', 'Jonathan Romero-Cuellar', 'James J. Luce'],
    'published': '2026-08-03',
    'pdf_url': 'https://arxiv.org/pdf/2608.02363v1',
    'file_name': 'papers/Shen_2026_Streamflow_Alteration_Ontario_Subbasins.pdf'
}

# Target 2: ArXiv paper on Multi-Source Dynamic Graph Learning for Compound-Flood Forecasting in Managed Coastal/River Basins
arxiv_paper_2 = {
    'id': '2608.01775v1',
    'title': 'Multi-Source Dynamic Graph Learning for Compound-Flood Forecasting in Managed Coastal Systems',
    'authors': ['Liangjun You', 'Min Wu', 'Orlando Woods', 'Dongsheng Luo'],
    'published': '2026-08-03',
    'pdf_url': 'https://arxiv.org/pdf/2608.01775v1',
    'file_name': 'papers/You_2026_Compound_Flood_Forecasting_Managed_Basins.pdf'
}

# Target 3: ArXiv paper on Hydrological Extremes & Vegetation Stress in Large Basins
arxiv_paper_3 = {
    'id': '2608.03037v1',
    'title': 'Recent Sharp Rise in Inhomogeneous Hydrological Extremes Stress Vegetation Growth in China',
    'authors': ['Shengyuan Liu', 'Jeremy Cheuk-Hin Leung', 'Jianjun Xu', 'et al.'],
    'published': '2026-08-04',
    'pdf_url': 'https://arxiv.org/pdf/2608.03037v1',
    'file_name': 'papers/Liu_2026_Hydrological_Extremes_China_Basins.pdf'
}

# Target 4: Open Access Remote Sensing Remote Sensing of Wetland Dynamics & Water Environment in Chaohu Lake Basin (MDPI Open Access PDF)
mdpi_paper_4 = {
    'title': 'Use of Multi-Source Remote Sensing Data to Understand Long-Term Wetland Dynamics and Water Environment Responses in the Chaohu Lake Basin',
    'authors': ['Ni Wang', 'Kaili Zhang', 'Juhua Luo', 'Omar Ali Eweys', 'Hongtao Duan', 'Jadunandan Dash'],
    'published': '2026-08-07',
    'pdf_url': 'https://www.mdpi.com/2072-4292/18/16/2646/pdf?version=1786098000', # MDPI RS direct pdf pattern or doi redirect
    'fallback_url': 'https://doi.org/10.3390/rs18162646',
    'file_name': 'papers/Wang_2026_Chaohu_Lake_Basin_Water_Environment.pdf'
}

# Target 5: ArXiv paper on Conceptual Hydrologic Models across 513 Basins
arxiv_paper_5 = {
    'id': '2607.26492v1',
    'title': 'From Conceptual Hydrologic Models to Conceptually Interpretable Neural Networks',
    'authors': ['Yuan-Heng Wang', 'Hoshin V. Gupta'],
    'published': '2026-07-29',
    'pdf_url': 'https://arxiv.org/pdf/2607.26492v1',
    'file_name': 'papers/Wang_2026_Mass_Conserving_Perceptron_Basin_Hydrology.pdf'
}

download_list = [arxiv_paper_1, arxiv_paper_2, arxiv_paper_3, arxiv_paper_5]

downloaded_summary = []

for item in download_list:
    success = download_file(item['pdf_url'], item['file_name'])
    if success:
        downloaded_summary.append(item)

print(f"\nSuccessfully downloaded {len(downloaded_summary)} hydrological and water management papers!")
