import urllib.request
import json
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
            if len(content) > 5000:
                with open(target_path, 'wb') as f:
                    f.write(content)
                print(f" Successfully saved {os.path.basename(target_path)} ({len(content)} bytes)")
                return True
            else:
                print(f" File too small or html redirect ({len(content)} bytes)")
                return False
    except Exception as e:
        print(f" Failed to download {url}: {e}")
        return False

extra_papers = [
    {
        'title': 'An Analysis of Land Use and Land Cover Changes in Wenje, Tana River County, Kenya',
        'pdf_url': 'https://journals.eanso.org/index.php/eajenr/article/download/5506/5861',
        'file_name': 'papers/Kiprop_2026_Tana_River_Basin_Land_Use.pdf'
    },
    {
        'title': 'Spatial assessment of soil erosion using GIS-integrated RUSLE in the Wolaita zone, Ethiopia',
        'pdf_url': 'https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0350986&type=printable',
        'file_name': 'papers/Fakana_2026_Soil_Erosion_Hydrology_Ethiopian_Basins.pdf'
    },
    {
        'title': 'Research progress in online monitoring of suspended sediment concentration',
        'pdf_url': 'https://www.frontiersin.org/journals/earth-science/articles/10.3389/feart.2026.1867548/pdf',
        'file_name': 'papers/Zhang_2026_Suspended_Sediment_Monitoring_Basins.pdf'
    }
]

for p in extra_papers:
    download_file(p['pdf_url'], p['file_name'])
