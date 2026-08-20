import fitz # PyMuPDF
import glob
import os
import re
import json
import hashlib

def get_file_hash(filepath):
    hasher = hashlib.md5()
    with open(filepath, 'rb') as f:
        buf = f.read(65536)
        while len(buf) > 0:
            hasher.update(buf)
            buf = f.read(65536)
    return hasher.hexdigest()

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extract_paper_details(filepath):
    doc = fitz.open(filepath)
    num_pages = len(doc)
    text = ""
    for page in doc[:min(3, num_pages)]:
        text += page.get_text() + "\n"
    doc.close()
    
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    
    # Try finding title (usually top lines before abstract)
    title = ""
    abstract = ""
    
    # Look for Abstract marker
    abstract_idx = -1
    for i, line in enumerate(lines[:50]):
        if re.match(r'^(abstract|abstract\b|summary)', line, re.IGNORECASE):
            abstract_idx = i
            break
            
    if abstract_idx != -1:
        # Title is usually among the lines preceding Abstract
        preceding = lines[:abstract_idx]
        # Filter out headers/arXiv markers
        preceding_clean = [p for p in preceding if not re.search(r'arXiv:|preprint|doi:|http|elsevier|springer|frontiers|nature', p, re.IGNORECASE) and len(p) > 3]
        if preceding_clean:
            title = " ".join(preceding_clean[:3])
            
        # Abstract content
        abs_lines = lines[abstract_idx+1:abstract_idx+20]
        # stop if we hit introduction or keywords
        clean_abs = []
        for l in abs_lines:
            if re.match(r'^(1\s+introduction|introduction|keywords|index terms|key words)', l, re.IGNORECASE):
                break
            clean_abs.append(l)
        abstract = clean_text(" ".join(clean_abs))
    else:
        # Fallback title from filename or top lines
        title = " ".join(lines[:2])
        abstract = clean_text(" ".join(lines[2:15]))
        
    if len(abstract) < 30:
        abstract = clean_text(" ".join(lines[:10]))
        
    # Infer year if present
    year = "2026"
    year_match = re.search(r'\b(202[0-6])\b', text[:1000])
    if year_match:
        year = year_match.group(1)
        
    basename = os.path.basename(filepath)
    clean_base_title = basename.replace('.pdf', '').replace('_', ' ')
    if len(title) < 10 or len(title) > 200:
        title = clean_base_title
        
    return {
        'filename': basename,
        'filepath': filepath,
        'title': clean_text(title),
        'abstract': abstract[:1200],
        'pages': num_pages,
        'size_mb': round(os.path.getsize(filepath)/(1024*1024), 2),
        'year': year
    }

def categorize_paper(paper):
    txt = (paper['title'] + " " + paper['abstract']).lower()
    
    if any(k in txt for k in ['groundwater', 'aquifer', 'subglacial', 'poroelastic', 'salinization']):
        return "Groundwater, Hydrogeology & Aquifer Dynamics"
    elif any(k in txt for k in ['rainfall-runoff', 'streamflow', 'runoff', 'flood', 'nowcasting', 'precipitation', 'nowcast', 'drought']):
        return "Streamflow, Runoff & Hydrological Forecasting"
    elif any(k in txt for k in ['machine learning', 'neural', 'deep learning', 'transformer', 'lstm', 'graph learning', 'ai', 'emulator', 'diffusion']):
        return "AI, Physics-Informed ML & Computational Hydrology"
    elif any(k in txt for k in ['insar', 'sentinel', 'satellite', 'remote sensing', 'grace', 'altimetry', 'radar']):
        return "Satellite Remote Sensing & Earth Observation"
    elif any(k in txt for k in ['watershed', 'basin', 'erosion', 'soil', 'swat', 'land cover', 'sediment', 'wetland', 'evapotranspiration']):
        return "Watershed Management, Soil Erosion & Eco-Hydrology"
    elif any(k in txt for k in ['allocation', 'water management', 'waterpower', 'dam', 'bankruptcy', 'tourism', 'policy', 'market']):
        return "Water Resources Management, Policy & Economics"
    else:
        return "Environmental & Hydroclimatic Studies"

def main():
    pdf_files = glob.glob('papers/*.pdf')
    print(f"Scanning {len(pdf_files)} PDF files...")
    
    # Deduplicate based on hash or normalized title
    seen_hashes = {}
    unique_papers = []
    duplicates_count = 0
    
    for f in pdf_files:
        f_hash = get_file_hash(f)
        if f_hash in seen_hashes:
            duplicates_count += 1
            continue
        seen_hashes[f_hash] = f
        
        info = extract_paper_details(f)
        info['category'] = categorize_paper(info)
        unique_papers.append(info)
        
    print(f"Found {len(unique_papers)} unique papers (skipped {duplicates_count} duplicates).")
    
    # Sort papers by category and title
    unique_papers.sort(key=lambda x: (x['category'], x['title']))
    
    # Save structured JSON
    with open('papers_summary_data.json', 'w', encoding='utf-8') as f:
        json.dump(unique_papers, f, indent=2)
        
    # Group by category
    categories = {}
    for p in unique_papers:
        categories.setdefault(p['category'], []).append(p)
        
    # Build Master Markdown Summary
    md = []
    md.append("# Comprehensive Hydrological & Water Resources Research Papers Summary\n")
    md.append(f"> **Catalog Overview:** Consolidated synthesis of **{len(unique_papers)} unique peer-reviewed and preprint scientific research papers** (primarily **2026/2025** publications) downloaded and indexed in the local repository.\n")
    md.append("## Executive Summary & Research Landscape\n")
    md.append("The compiled collection covers state-of-the-art advances across **six primary thematic pillars** in hydrological sciences, water resources engineering, and computational hydroinformatics:\n")
    md.append("1. **Physics-Informed & Conceptually Interpretable AI:** Mass-conserving neural networks, hybrid hydrological models (combining LSTM/Transformers with conceptual models like GR4J and SAC-SMA), and graph neural networks for ungauged basins.")
    md.append("2. **Operational Streamflow, Flood & Drought Forecasting:** Global and regional forecasting frameworks using multi-source dynamic graph learning, quantile ensembles, and meteorology-informed attention mechanisms.")
    md.append("3. **Groundwater Hydrogeology & Aquifer Mechanics:** Poroelastic aquifer response driving land motion, unsupervised GRACE-based groundwater storage anomaly detection, and subglacial hydrological coupling.")
    md.append("4. **Satellite Remote Sensing & Earth Observation:** Open-source InSAR time-series processing (DefoEye), spaceborne altimetry, microwave radar soil moisture assimilation, and multi-satellite precipitation refinement.")
    md.append("5. **Catchment Morphometry, Soil Erosion & Ecohydrology:** RUSLE-GIS soil erosion mapping, morphometric vulnerability indices in arid/semi-arid watersheds, and climate impacts on macroinvertebrates.")
    md.append("6. **Water Resource Allocation, Economics & Policy:** Multi-objective allocation under economic efficiency, pro-rata mechanisms in groundwater markets, and formal mathematical definitions of water bankruptcy.\n")
    md.append("---\n")
    
    # Detailed thematic sections
    for cat_name, papers in categories.items():
        md.append(f"## {cat_name} ({len(papers)} Papers)\n")
        for i, p in enumerate(papers, 1):
            md.append(f"### {i}. {p['title']}")
            md.append(f"- **File:** [`{p['filename']}`](file:///{p['filepath'].replace('\\', '/')})")
            md.append(f"- **Year / Publication Scope:** {p['year']} | **Document Size:** {p['size_mb']} MB ({p['pages']} pages)")
            md.append(f"- **Key Focus / Abstract Summary:**\n  {p['abstract'] if p['abstract'] else 'No direct abstract extracted; see full paper for technical specifications.'}\n")
        md.append("---\n")
        
    # Statistical overview table
    md.append("## Summary Statistics by Thematic Area\n")
    md.append("| Thematic Domain | Number of Papers | Focus Areas |\n")
    md.append("| :--- | :---: | :--- |\n")
    for cat_name, papers in categories.items():
        md.append(f"| **{cat_name}** | **{len(papers)}** | Model architectures, empirical studies, and case applications |\n")
    md.append(f"| **Total Unique Papers** | **{len(unique_papers)}** | Comprehensive hydro-environmental collection |\n")
    
    with open('PAPERS_SUMMARY_MASTER.md', 'w', encoding='utf-8') as f:
        f.write("\n".join(md))
        
    print("Master summary written to PAPERS_SUMMARY_MASTER.md successfully!")

if __name__ == '__main__':
    main()
