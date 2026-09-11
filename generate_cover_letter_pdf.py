#!/usr/bin/env python3
"""
generate_cover_letter_pdf.py

Generates a publication-grade PDF of the formal Cover Letter for MDPI Geosciences
using ReportLab, ensuring zero external dependencies on Word COM.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable

def generate_pdf():
    pdf_path = "Cover_Letter_Geosciences.pdf"
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom styles
    header_style = ParagraphStyle(
        'HeaderStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=colors.HexColor('#0F172A')
    )

    sender_style = ParagraphStyle(
        'SenderStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#334155')
    )

    body_style = ParagraphStyle(
        'BodyStyle',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=10.5,
        leading=14.5,
        textColor=colors.HexColor('#1E293B'),
        spaceAfter=7
    )

    heading_style = ParagraphStyle(
        'HeadingStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14.5,
        textColor=colors.HexColor('#0F172A'),
        spaceBefore=7,
        spaceAfter=4
    )

    bullet_style = ParagraphStyle(
        'BulletStyle',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=10,
        leading=14,
        leftIndent=15,
        textColor=colors.HexColor('#1E293B'),
        spaceAfter=4
    )

    story = []

    # Sender info
    story.append(Paragraph("NED University of Engineering and Technology", header_style))
    story.append(Paragraph("Department of Computer and Information Systems Engineering (CISE)<br/>University Road, Karachi 75270, Sindh, Pakistan<br/><b>Corresponding Author:</b> Mirza Muhammad Muzzamil | <b>Email:</b> mirzamuzzamil@neduet.edu.pk | <b>ORCID:</b> 0000-0001-5258-8959", sender_style))
    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#1E3A8A'), spaceBefore=2, spaceAfter=10))

    # Date & Recipient
    story.append(Paragraph("<b>Date:</b> September 11, 2026", sender_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>To:</b><br/>Editorial Office, <i>Geosciences</i> (MDPI)<br/>St. Alban-Anlage 66, 4052 Basel, Switzerland", sender_style))
    story.append(Spacer(1, 10))

    # Subject
    story.append(Paragraph("<b>Subject: Submission of Original Research Article — Manuscript ID Consideration</b>", header_style))
    story.append(Spacer(1, 6))

    # Salutation
    story.append(Paragraph("Dear Editor-in-Chief and Editorial Board Members,", body_style))

    # Opening
    story.append(Paragraph(
        "We are pleased to submit our original research manuscript entitled <b>“Storage- and Regulation-Aware Physics-Guided Learning Reveals Nonlinear Flood Response Thresholds in Regulated River Basins”</b> for consideration as an <b>Article</b> in <i><b>Geosciences</b></i>.",
        body_style
    ))

    # Explicit Linkage to Geosciences
    story.append(Paragraph("Linkage and Explicit Alignment with <i>Geosciences</i>:", heading_style))
    story.append(Paragraph(
        "This study directly advances the core mission of <i>Geosciences</i> by linking catchment hydrology, Earth system remote sensing, and extreme geological/alluvial hazard dynamics. In response to the journal's editorial criteria, this work contributes to the geosciences discipline through three primary pillars:",
        body_style
    ))

    story.append(Paragraph("• <b>Multi-Sensor Satellite Earth Observation:</b> We integrate spaceborne gravimetry (NASA GRACE/GRACE-FO JPL Mascon RL06), vadose soil moisture (NASA SMAP L4), infrared precipitation (CHIRPS v2.0), and atmospheric reanalysis (ERA5-Land) to resolve dynamic terrestrial water storage anomalies (TWSA) across the heavily managed Lower Indus Alluvial Basin.", bullet_style))
    story.append(Paragraph("• <b>Nonlinear Hydrological Threshold Law Discovery:</b> Non-parametric bootstrap regression derives the critical catchment threshold law <i>S*(U) = 38.2 + 0.515 U<sub>t</sub></i> (mm), revealing that anthropogenic canal irrigation withdrawals expand effective storage buffering by up to +14.8 mm/month before super-critical flood surge occurs. We introduce the <b>Flood Amplification Margin</b> (<i>FAM<sub>t</sub> = S<sub>t</sub> - S*(U<sub>t</sub>)</i>) as an operational diagnostic for monsoon flood preparedness.", bullet_style))
    story.append(Paragraph("• <b>Satellite Radar Inundation Grounding & Dual-Basin Validation:</b> Modeled discharge is validated against Copernicus Sentinel-1 Synthetic Aperture Radar (SAR) flood inundation extent (<i>r = 0.94, R² = 0.88, IoU = 0.79</i>) during the historic 2022 Pakistan Mega-Flood, alongside cross-climatic transfer evaluation on the catastrophic July 2021 Ahr River flash flood in Rhineland-Palatinate, Germany.", bullet_style))

    # Scientific Highlights
    story.append(Paragraph("Key Scientific Contributions:", heading_style))
    story.append(Paragraph("• <b>Mitigates Machine Learning Peak Attenuation:</b> State-adaptive sigmoidal gating (α<sub>t</sub>) dynamically shifts weight to a mass-conservation backbone as storage pressure mounts, restricting 2022 flood peak bias to -4.0% (vs. -13.3% for unconstrained GBDT and -11.9% for conceptual GR2M).", bullet_style))
    story.append(Paragraph("• <b>Cross-Basin Structural Transferability:</b> Zero-shot direct transfer to the Ahr River achieved KGE = 0.421 (NSE = 0.518), rising to KGE = 0.607 under local calibration, confirming generalizability across contrasting morphometric regimes.", bullet_style))

    # Author Declarations
    story.append(Paragraph("Author Declarations:", heading_style))
    story.append(Paragraph("• This manuscript is original, has not been published previously, and is not under consideration for publication elsewhere.", bullet_style))
    story.append(Paragraph("• The author has reviewed and approved the manuscript and agrees with its submission to <i>Geosciences</i>.", bullet_style))
    story.append(Paragraph("• The author declares no conflicts of interest. No external grant funding was received for this study.", bullet_style))
    story.append(Paragraph("• All satellite datasets (CHIRPS, ERA5-Land, SMAP, GRACE, Sentinel-1) and modeling code are fully open-source.", bullet_style))

    # Suggested Reviewers
    story.append(Paragraph("Suggested Expert Peer Reviewers:", heading_style))
    story.append(Paragraph("1. <b>Prof. Dr. Markus Reichstein</b> — Max Planck Institute for Biogeochemistry, Germany (<i>mreichstein@bgc-jena.mpg.de</i>). Expert in Earth system science and hybrid physics-AI modeling.", bullet_style))
    story.append(Paragraph("2. <b>Dr. Frederik Kratzert</b> — Google Research / JKU Linz, Austria (<i>kratzert@google.com</i>). Expert in deep learning and hydrological sequence modeling.", bullet_style))
    story.append(Paragraph("3. <b>Prof. Dr. Vimal Mishra</b> — IIT Gandhinagar, India (<i>vmishra@iitgn.ac.in</i>). Expert in South Asian monsoons, remote sensing, and flood hazards.", bullet_style))
    story.append(Paragraph("4. <b>Dr. Grey Nearing</b> — Google Research / UC Davis, USA (<i>gs-nearing@google.com</i>). Expert in large-sample machine learning hydrology.", bullet_style))

    story.append(Spacer(1, 6))
    story.append(Paragraph("Thank you for your consideration of our work. We look forward to the editorial decision and peer review.", body_style))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Sincerely,<br/><b>Mirza Muhammad Muzzamil</b><br/>Department of Computer and Information Systems Engineering (CISE)<br/>NED University of Engineering and Technology, Karachi, Pakistan<br/>Email: <i>mirzamuzzamil@neduet.edu.pk</i>", sender_style))

    doc.build(story)
    print(f"SUCCESS: Generated {pdf_path}")

if __name__ == "__main__":
    generate_pdf()
