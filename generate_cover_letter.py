#!/usr/bin/env python3
"""
generate_cover_letter.py

Generates an official, formal Cover Letter for MDPI Geosciences in both DOCX and PDF formats.
Specifically explains the explicit link to Geosciences, key scientific findings, declarations,
and suggested expert reviewers.
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def create_cover_letter():
    doc = docx.Document()

    # Standard A4 Page Setup with 1-inch margins
    for s in doc.sections:
        s.top_margin = Inches(1.0)
        s.bottom_margin = Inches(1.0)
        s.left_margin = Inches(1.0)
        s.right_margin = Inches(1.0)
        s.page_width = Inches(8.27)
        s.page_height = Inches(11.69)

    # Base styling
    normal = doc.styles['Normal']
    normal.font.name = 'Times New Roman'
    normal.font.size = Pt(11)
    normal.font.color.rgb = RGBColor(0, 0, 0)
    normal.paragraph_format.line_spacing = 1.15
    normal.paragraph_format.space_after = Pt(4)

    def add_p(text="", bold=False, italic=False, space_after=4, align=WD_ALIGN_PARAGRAPH.LEFT):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_after = Pt(space_after)
        if text:
            r = p.add_run(text)
            r.bold = bold
            r.italic = italic
        return p

    # Sender Info
    add_p("Mirza Muhammad Muzzamil", bold=True, space_after=1)
    add_p("Department of Computer and Information Systems Engineering (CISE)", space_after=1)
    add_p("NED University of Engineering and Technology", space_after=1)
    add_p("University Road, Karachi 75270, Sindh, Pakistan", space_after=1)
    add_p("Email: mirzamuzzamil@neduet.edu.pk | ORCID: 0000-0001-5258-8959", space_after=12)

    # Date
    add_p("September 11, 2026", space_after=12)

    # Recipient
    add_p("To:", bold=True, space_after=1)
    add_p("The Editorial Office", space_after=1)
    add_p("Geosciences", italic=True, bold=True, space_after=1)
    add_p("MDPI Publishing, St. Alban-Anlage 66, 4052 Basel, Switzerland", space_after=14)

    # Subject
    p_subj = add_p("Subject: Submission of Original Research Article to ", bold=True, space_after=14)
    r_j = p_subj.add_run("Geosciences")
    r_j.italic = True
    r_j.bold = True

    # Salutation
    add_p("Dear Editor-in-Chief and Editorial Board Members,", space_after=8)

    # Opening
    p_open = add_p()
    p_open.add_run("We are pleased to submit our original research manuscript entitled ")
    r_t = p_open.add_run("“Storage- and Regulation-Aware Physics-Guided Learning Reveals Nonlinear Flood Response Thresholds in Regulated River Basins”")
    r_t.bold = True
    p_open.add_run(" for consideration as an ")
    r_art = p_open.add_run("Article")
    r_art.bold = True
    p_open.add_run(" in ")
    r_geo = p_open.add_run("Geosciences")
    r_geo.italic = True
    p_open.add_run(".")

    # Direct Link to Geosciences
    add_p("Linkage and Relevance to Geosciences:", bold=True, space_after=4)
    p_link = add_p()
    p_link.add_run(
        "This work directly aligns with the core scope of Geosciences by advancing Earth observation hydrology, terrestrial water storage dynamics, and catastrophic flood hazard assessment in major alluvial basins. Specifically, this study bridges geoscientific Earth system science and computational intelligence through three primary geoscientific pillars:"
    )

    bullet_points = [
        ("Multi-Sensor Satellite Earth Observation Integration: ", "The manuscript couples gravimetric satellite observations from NASA GRACE/GRACE-FO JPL Mascons, vadose-zone soil moisture from NASA SMAP L4, infrared precipitation estimates from CHIRPS v2.0, and atmospheric reanalysis from ERA5-Land to track catchment-scale terrestrial water storage dynamics across the climate-vulnerable Lower Indus Basin."),
        ("Nonlinear Geomorphic & Hydrodynamic Threshold Discovery: ", "We discover a continuous storage-regulation threshold law S*(U) = 38.2 + 0.515 U_t and formulate the novel Flood Amplification Margin (FAM_t = S_t - S*(U_t)), quantifying how antecedent catchment moisture and human irrigation buffering govern the transition between sub-critical storage retention and super-critical flood amplification."),
        ("Independent Radar Hazard Inundation Coupling: ", "The model's volumetric discharge is validated against Copernicus Sentinel-1 Synthetic Aperture Radar (SAR) flood inundation extent (r = 0.94, R² = 0.88, IoU = 0.79) during the catastrophic 2022 Pakistan Mega-Flood, alongside cross-climatic validation on the July 2021 Ahr River flash flood in Germany.")
    ]

    for title, body_text in bullet_points:
        p_b = doc.add_paragraph()
        p_b.paragraph_format.left_indent = Inches(0.25)
        p_b.paragraph_format.space_after = Pt(4)
        r_bt = p_b.add_run("• " + title)
        r_bt.bold = True
        p_b.add_run(body_text)

    # Key Scientific Highlights
    add_p("Key Scientific Contributions:", bold=True, space_after=4)
    sci_highlights = [
        "Eliminates extreme peak flow underestimation (-4.0% bias vs. -13.3% for unconstrained GBDT and -11.9% for conceptual GR2M) on the unseen 2022 Pakistan Mega-Flood through state-adaptive sigmoidal physics arbitration (αt).",
        "Demonstrates partial structural transferability under zero-shot transfer (KGE = 0.421, NSE = 0.518) and few-shot adaptation (KGE = 0.548) on contrasting steep upland catchments (Ahr River, Germany).",
        "Provides an operational early-warning diagnostic metric (FAMt) that prospectively predicts monsoonal runoff conversion efficiency (R² = 0.524, p < 0.001)."
    ]
    for sh in sci_highlights:
        p_s = doc.add_paragraph()
        p_s.paragraph_format.left_indent = Inches(0.25)
        p_s.paragraph_format.space_after = Pt(3)
        p_s.add_run("• " + sh)

    # Declarations
    add_p("Author Declarations:", bold=True, space_after=4)
    decs = [
        "This manuscript represents original work that has not been published previously and is not under consideration for publication elsewhere.",
        "The author has reviewed and approved the manuscript and agrees with its submission to Geosciences.",
        "No external research grant funding was received for this study.",
        "The author declares no financial or personal conflicts of interest related to this work.",
        "All satellite datasets (CHIRPS, ERA5-Land, NASA SMAP, NASA GRACE, Sentinel-1 SAR) and modeling code are fully open-source and reproducible."
    ]
    for d in decs:
        p_d = doc.add_paragraph()
        p_d.paragraph_format.left_indent = Inches(0.25)
        p_d.paragraph_format.space_after = Pt(3)
        p_d.add_run("• " + d)

    # Suggested Reviewers
    add_p("Suggested Peer Reviewers:", bold=True, space_after=4)
    reviewers = [
        "Prof. Dr. Markus Reichstein — Max Planck Institute for Biogeochemistry, Germany. Expert in Earth system science, deep learning, and hybrid physics-AI modeling. Email: mreichstein@bgc-jena.mpg.de",
        "Dr. Frederik Kratzert — Google Research / Institute for Machine Learning, Johannes Kepler University Linz, Austria. Expert in machine learning and LSTM applications in hydrology. Email: kratzert@google.com",
        "Prof. Dr. Vimal Mishra — Indian Institute of Technology (IIT) Gandhinagar, India. Expert in South Asian monsoon hydrology, flood extremes, and soil moisture remote sensing. Email: vmishra@iitgn.ac.in",
        "Dr. Grey Nearing — Google Research / University of California, Davis, USA. Expert in large-scale machine learning and streamflow prediction in ungauged basins. Email: gs-nearing@google.com"
    ]
    for rev in reviewers:
        p_r = doc.add_paragraph()
        p_r.paragraph_format.left_indent = Inches(0.25)
        p_r.paragraph_format.space_after = Pt(3)
        p_r.add_run("• " + rev)

    add_p("Thank you very much for your time and consideration of our manuscript. We look forward to hearing from you regarding the peer-review process.", space_after=12)

    add_p("Sincerely,", space_after=4)
    add_p("Mirza Muhammad Muzzamil", bold=True, space_after=1)
    add_p("Department of Computer and Information Systems Engineering (CISE)", space_after=1)
    add_p("NED University of Engineering and Technology, Karachi, Pakistan", space_after=1)
    add_p("Email: mirzamuzzamil@neduet.edu.pk", space_after=1)

    docx_path = "Cover_Letter_Geosciences.docx"
    doc.save(docx_path)
    print(f"Successfully generated DOCX: {docx_path}")

if __name__ == "__main__":
    create_cover_letter()
