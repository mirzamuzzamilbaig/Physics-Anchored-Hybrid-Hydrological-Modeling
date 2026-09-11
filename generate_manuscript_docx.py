"""
Generate complete MS-Word (.docx) manuscript for Geosciences Journal
Strictly adhering to Springer Geosciences Journal Submission Guidelines and Article Template:
1. Title Page (14pt Bold Title in Sentence Case, Authors, Affiliations, Corresponding Author block, Short title, Abstract, Keywords, End of title page)
2. Continuous Line Numbering across all pages
3. Sentence case headings (1 Introduction, 1.1 ..., 1.2 ...)
4. Figures & Captions (Fig. 1 ... no trailing period, embedded with caption on same page)
5. Tables & Captions (Table 1 ... no vertical lines, no trailing period, on single page)
6. Equations left-justified with trailing punctuation before equation number
7. Back matter (Acknowledgements, Statements and declarations, Data availability statements, References with italicized journal names and volume numbers, End of text)
"""

import os
import sys

import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn


def add_continuous_line_numbering(doc):
    """Enable continuous line numbering in Word document XML across all sections."""
    for section in doc.sections:
        sectPr = section._sectPr
        lnNumType = parse_xml(r'<w:lnNumType %s w:countBy="1" w:restart="continuous"/>' % nsdecls('w'))
        sectPr.append(lnNumType)


def set_cell_borders(cell, top=None, bottom=None, left=None, right=None):
    """Set custom borders on table cells (used for standard 3-line academic tables)."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:top w:val="{top or "none"}" w:sz="6" w:space="0" w:color="auto"/>'
        f'<w:left w:val="{left or "none"}" w:sz="0" w:space="0" w:color="auto"/>'
        f'<w:bottom w:val="{bottom or "none"}" w:sz="6" w:space="0" w:color="auto"/>'
        f'<w:right w:val="{right or "none"}" w:sz="0" w:space="0" w:color="auto"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(tcBorders)


def generate_docx(output_path="paper_latex/Research_Article_Journal_of_Hydroinformatics.docx", journal="hydroinformatics"):
    doc = docx.Document()

    # Page setup: Standard A4 with 1-inch (2.54 cm) margins
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        section.page_width = Inches(8.27)
        section.page_height = Inches(11.69)

    # Base typography: Times New Roman 11pt, 1.15 line spacing
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(11)
    font.color.rgb = RGBColor(0, 0, 0)
    doc.styles['Normal'].paragraph_format.line_spacing = 1.15
    doc.styles['Normal'].paragraph_format.space_after = Pt(4)

    # =========================================================================
    # TITLE PAGE (Template Page 1)
    # =========================================================================

    # Title (Template: max 20 words, bold, 16pt)
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r_title = p_title.add_run("Storage- and Regulation-Aware Physics-Guided Learning Reveals Nonlinear Flood Response Thresholds in Regulated River Basins")
    r_title.bold = True
    r_title.font.size = Pt(16)
    p_title.paragraph_format.space_after = Pt(14)
    p_title.paragraph_format.line_spacing = 1.15

    # Author
    p_author = doc.add_paragraph()
    r_author = p_author.add_run("Mirza Muhammad Muzzamil")
    r_author.bold = True
    r_author.font.size = Pt(11)
    p_author.paragraph_format.space_after = Pt(4)

    # Affiliation
    p_aff = doc.add_paragraph()
    p_aff.add_run("Department of Computer and Information Systems Engineering (CISE), NED University of Engineering and Technology, Karachi 75270, Sindh, Pakistan")
    p_aff.paragraph_format.space_after = Pt(8)

    # Corresponding Author
    p_corr = doc.add_paragraph()
    r_corr_lbl = p_corr.add_run("Corresponding author: ")
    r_corr_lbl.bold = True
    p_corr.add_run("Mirza Muhammad Muzzamil | E-mail: mirzamuzzamil@neduet.edu.pk | ORCID: https://orcid.org/0000-0001-5258-8959")
    p_corr.paragraph_format.space_after = Pt(14)

    # Highlights (Template Section: 3 to 5 bullet points, max 85 characters each)
    if journal == "hydroinformatics":
        p_hl_hdr = doc.add_paragraph()
        r_hl_hdr = p_hl_hdr.add_run("Highlights")
        r_hl_hdr.bold = True
        p_hl_hdr.paragraph_format.space_after = Pt(4)

        highlights = [
            "State-adaptive physics gating balances physical conservation and machine learning",
            "Tracks modeled catchment water storage state (St) constrained by GRACE gravimetry and SMAP",
            "Separates modeled natural runoff generation and unresolved agricultural regulation fluxes",
            "Discovers storage-regulation runoff threshold S*(U) and Flood Amplification Margin (FAM)",
            "Dual-basin validation across Lower Indus (Pakistan 2022) and Ahr River (Germany 2021)"
        ]
        for hl in highlights:
            p_hl = doc.add_paragraph()
            p_hl.paragraph_format.left_indent = Inches(0.25)
            p_hl.paragraph_format.space_after = Pt(2)
            r_bullet = p_hl.add_run("• ")
            r_bullet.bold = True
            p_hl.add_run(hl)

        p_space_hl = doc.add_paragraph()
        p_space_hl.paragraph_format.space_after = Pt(6)

    # Abstract
    p_abs_hdr = doc.add_paragraph()
    r_abs_hdr = p_abs_hdr.add_run("Abstract")
    r_abs_hdr.bold = True
    p_abs_hdr.paragraph_format.space_after = Pt(4)

    p_abs = doc.add_paragraph(
        "Accurate streamflow simulation and extreme flood risk estimation in large, managed alluvial basins are severely hindered by hydro-climatic non-stationarity, complex hydraulic regulation, and observational scarcity. While machine learning (ML) architectures capture non-linear hydrological interactions, unconstrained algorithms suffer from severe peak-flow attenuation and variance collapse when exposed to out-of-distribution (OOD) hydrometeorological shocks. In this study, we propose the Storage-Adaptive and Regulation-Aware Physics-Guided Multi-Sensor Catchment Hydrology framework (SA-PG-MCH). SA-PG-MCH reconstructs the dynamic hydrological state of managed basins by tracking a continuous latent catchment water storage state (St) regularized by multi-sensor Earth observations (CHIRPS precipitation, ERA5-Land reanalysis, NASA SMAP root-zone soil moisture, and NASA GRACE/GRACE-FO terrestrial water storage anomalies) and transboundary upstream boundary telemetry. The architecture explicitly separates modeled natural runoff generation from unobserved anthropogenic irrigation abstraction and groundwater recharge fluxes (Ut = Dt^irr + Gt). To reduce the tendency of tree ensembles to collapse under extreme events, a state-dependent sigmoidal gating mechanism (αt) dynamically shifts weight to a monotonic physical mass backbone as catchment storage pressure and precipitation anomalies intensify. Calibrated on a 20-year baseline (2000–2019, N = 240) and evaluated under a strict temporal holdout against the catastrophic 2022 Pakistan Mega-Flood (N = 12), SA-PG-MCH achieved KGE = 0.812 and restricted peak underestimation bias (FHV) to -4.0%, whereas unconstrained GBDT collapsed (FHV = -13.3%). Independent cross-climatic validation on the July 2021 flash flood in the Ahr River Basin, Germany (252 calibration months, 12-month event holdout) confirmed partial structural transferability under zero-shot transfer (KGE = 0.421, NSE = 0.518), rising to KGE = 0.607 under local calibration. Response surface analysis (∂Q/∂P = f(S, U)) reveals that runoff sensitivity surges nonlinearly from 0.12 under dry baseflows to >0.50 during saturated states, while human regulation expands the critical saturation threshold S*(U) from 38.2 mm to 48.5 mm, providing up to +14.8 mm/month of modeled peak flood buffering. Introducing the Flood Amplification Margin (FAMt = St - S*(Ut)) provides a continuous diagnostic that prospectively predicts observed runoff elasticity (R² = 0.52, p < 0.001). Closed-loop validation against Sentinel-1 SAR flood inundation extent confirms strong temporal agreement (r = 0.94, R² = 0.88, IoU = 0.79), while multi-threshold exceedance probabilities provide a potential decision-support indicator for seasonal flood preparedness."
    )
    p_abs.paragraph_format.space_after = Pt(10)

    # Keywords
    p_kw = doc.add_paragraph()
    r_kw_lbl = p_kw.add_run("Keywords: ")
    r_kw_lbl.bold = True
    p_kw.add_run("Physics-guided machine learning, Storage-adaptive gating, GRACE terrestrial water storage, Anthropogenic regulation, Response surface, Indus Basin, Sentinel-1 SAR, Out-of-distribution extremes")
    p_kw.paragraph_format.space_after = Pt(14)

    if journal != "hydroinformatics":
        # End of title page
        p_end_tp = doc.add_paragraph()
        p_end_tp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_end_tp = p_end_tp.add_run("— End of title page —")
        r_end_tp.italic = True
        p_end_tp.paragraph_format.space_after = Pt(14)

    # Page break after Title Page
    doc.add_page_break()

    # =========================================================================
    # HELPER FUNCTIONS FOR HEADINGS & BODY
    # =========================================================================
    def add_sec_heading(title):
        p = doc.add_paragraph()
        r = p.add_run(title)
        r.bold = True
        r.font.size = Pt(12)
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        return p

    def add_subsec_heading(title):
        p = doc.add_paragraph()
        r = p.add_run(title)
        r.bold = True
        r.font.size = Pt(11)
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.keep_with_next = True
        return p

    def add_body_p(text, indent=True):
        p = doc.add_paragraph(text)
        if indent:
            p.paragraph_format.first_line_indent = Inches(0.25)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        return p

    def add_figure(img_path, caption_num, caption_text, width=Inches(6.0)):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.keep_with_next = True
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(4)
        if os.path.exists(img_path):
            p_img.add_run().add_picture(img_path, width=width)
        else:
            p_img.add_run(f"[Image file not found: {img_path}]")

        p_cap = doc.add_paragraph()
        p_cap.paragraph_format.keep_with_next = False
        p_cap.paragraph_format.space_after = Pt(8)
        r_lbl = p_cap.add_run(f"Fig. {caption_num} ")
        r_lbl.bold = True
        p_cap.add_run(caption_text)

    # =========================================================================
    # 1 Introduction
    # =========================================================================
    add_sec_heading("1 Introduction")
    add_body_p(
        "The Indus River Basin is one of the most critical and climate-vulnerable transboundary river systems globally, sustaining over 230 million people and supporting the world's largest contiguous irrigation network—the Indus Basin Irrigation System (IBIS) (Immerzeel et al., 2020; Young et al., 2019). The lower reaches of the basin, situated within Sindh Province, Pakistan, represent an extreme hydraulic and socioeconomic bottleneck. Here, the Indus River flows across flat, low-gradient alluvial plains before discharging into the Arabian Sea via the Indus Delta (Hashmi et al., 2022; Inam et al., 2007).",
        indent=False
    )
    add_body_p(
        "In recent years, anthropogenic climate change has intensified the magnitude of hydrological extremes across South Asia. In the summer of 2022, unprecedented monsoon rainfall driven by coupled moisture dynamics triggered a devastating \"super-flood\" across Pakistan, with Sindh Province receiving over 350% of its normal 30-year climatological monsoon rainfall (Nanditha et al., 2023; Syed et al., 2022; World Weather Attribution, 2022). Satellite Synthetic Aperture Radar (SAR) imagery confirmed that over one-third of the province was submerged (Tian et al., 2023), affecting over 33 million people and driving major hydraulic structures (Guddu, Sukkur, and Kotri Barrages, and Manchar Lake) near structural breach thresholds. Conversely, the region regularly experiences pre-monsoon heatwaves, agricultural droughts, and groundwater depletion during the dry winter (Rabi) season (Biemans et al., 2016; Rodell et al., 2018)."
    )

    add_subsec_heading("1.1 Problem background and motivation")
    add_body_p(
        "Hydrological prediction in heavily managed alluvial basins faces two fundamental methodological limitations:",
        indent=False
    )
    add_body_p("(1) Conceptual models (e.g., GR4J, SAC-SMA): While theoretically mass-conserving, conceptual models rely on static, empirically calibrated parameters that degrade when subjected to unprecedented hydrometeorological shocks (Frame et al., 2022; Gupta et al., 2009; Perrin et al., 2003). Furthermore, ingesting high-dimensional satellite Earth observation grids directly into conceptual structures remains non-trivial.")
    add_body_p("(2) Standard machine learning (e.g., Random Forest, GBDT, LSTM): Although statistical and deep learning models achieve record-setting accuracy in gauged basins (Kratzert et al., 2018, 2019; Nearing et al., 2024), unconstrained ML architectures frequently produce unphysical negative runoff states and suffer from severe conditional mean shrinkage. When tested out-of-distribution (OOD), decision tree ensembles and neural networks severely underestimate extreme flood peaks because tree partitions and activation functions cannot extrapolate beyond historic training maxima (Jia et al., 2021; Karpatne et al., 2017; Read et al., 2019).")

    add_subsec_heading("1.2 Research hypotheses and core scientific contributions")
    add_body_p("To resolve these challenges, this study formulates four central hydrological hypotheses:", indent=False)
    add_body_p("• Hypothesis 1 (H1, Nonlinear Storage Transition): Rainfall-runoff elasticity EP = (∂Q/∂P)(P/Q) increases nonlinearly with antecedent catchment storage (∂EP/∂S > 0), exhibiting a distinct critical saturation threshold (S*).")
    add_body_p("• Hypothesis 2 (H2, Regulation Threshold Expansion): Anthropogenic canal irrigation withdrawals and groundwater pumping expand the effective catchment storage threshold (∂S*/∂U > 0), buffering flood peaks until super-critical storage is reached.")
    add_body_p("• Hypothesis 3 (H3, Extreme Rarity Scaling): The peak preservation advantage of state-adaptive physics anchoring expands monotonically with extreme flood rarity (∂ΔFHV/∂T > 0).")
    add_body_p("• Hypothesis 4 (H4, Dimensionless Structural Transferability): Normalizing critical storage by effective catchment capacity (S*norm(RI) = S*/Scapacity) reveals a transferable dimensionless flood response threshold across contrasting macro-alluvial and steep upland basins.")
    add_body_p("In evaluating these hypotheses, this paper provides four primary contributions:", indent=False)
    add_body_p("(1) State-Adaptive Physics Arbitration: An architecture that dynamically shifts weighting (αt → 1.0) to the mass baseline as storage pressure intensifies, reducing the tendency of tree ensembles to collapse toward historical means.")
    add_body_p("(2) Storage–Regulation Threshold Discovery: A continuous response law (S*(U) = 38.2 + 0.515 Ut) quantifying critical storage thresholds, supported by independent empirical historical event validation (p < 0.001) and dimensionless cross-basin normalization.")
    add_body_p("(3) Counterfactual Regulation Decomposition: Attribution of peak flood buffering across irrigation diversion (+10.6 mm/month) and groundwater exchange (+4.2 mm/month) components.")
    add_body_p("(4) Multi-Domain Extreme Generalization: Robust validation spanning rare-event scaling (T = 2 to 20 yr), cross-basin transfer spectrums (Pakistan → Ahr River), synthetic 1.0x–5.0x stress testing with Monotonic GBDT controls, and independent post-hoc Sentinel-1 SAR flood extent coupling (r = 0.94).")

    # =========================================================================
    # 2 Literature review and gap analysis
    # =========================================================================
    add_sec_heading("2 Literature review and gap analysis")
    add_subsec_heading("2.1 Physical hydrology of the Lower Indus Basin")
    add_body_p(
        "The hydrological regime of the Indus Basin is driven by snow-glacier melt in the Upper Indus Basin and South Asian monsoon depressions in the lower basin (Biemans et al., 2016; Immerzeel et al., 2020; Syed et al., 2022). Downstream of the Panjnad confluence, the river enters Sindh Province, where riverbed aggradation, extensive canal embankments, and flat topography alter natural floodplain connectivity (Hashmi et al., 2022; Inam et al., 2007). Climatological studies indicate that atmospheric warming is expanding tropospheric moisture capacity via the Clausius-Clapeyron relation (~7% per °C), generating non-stationary rainfall regimes and elevated peak runoff coefficients (Nanditha et al., 2023; World Weather Attribution, 2022).",
        indent=False
    )

    add_subsec_heading("2.2 Evolution from conceptual models to deep learning")
    add_body_p(
        "Hydrological prediction has historically relied on conceptual lumped and semi-distributed models such as GR4J (Perrin et al., 2003). Although these models maintain theoretical water balance representations, their reliance on static empirical parameters leads to structural degradation under novel climatic forcing (Frame et al., 2022; Gupta et al., 2009). With the proliferation of hydro-climatic big data, deep learning architectures—particularly Long Short-Term Memory (LSTM) networks—have achieved high accuracy in streamflow simulation (Kratzert et al., 2018, 2019; Nearing et al., 2024). However, on tabular satellite feature sets with short calibration records, unconstrained models are susceptible to severe sample-variance overfitting unless physically constrained (Jia et al., 2021; Willard et al., 2022).",
        indent=False
    )

    add_subsec_heading("2.3 Physics-guided and hybrid machine learning")
    add_body_p(
        "To reconcile physical interpretability with statistical flexibility, Physics-Guided Machine Learning (PGML) has emerged as a key computational paradigm (Jia et al., 2021; Karpatne et al., 2017; Read et al., 2019; Willard et al., 2022). Anchoring model predictions to first-order water balance baselines constrains the hypothesis space, preventing gradient divergence and maintaining accurate hydrograph variance under out-of-distribution climatic forcing (Frame et al., 2022).",
        indent=False
    )

    add_subsec_heading("2.4 Cloud-native Earth observation")
    add_body_p(
        "Planetary-scale geospatial platforms, specifically Google Earth Engine (GEE), have eliminated computational barriers in multi-sensor hydro-environmental analysis (Gorelick et al., 2017). Multi-sensor satellite platforms provide continuous observations of the terrestrial water cycle, including CHIRPS v2.0 precipitation (Funk et al., 2015), ERA5-Land reanalysis (Muñoz-Sabater et al., 2021), NASA SMAP soil moisture (Entekhabi et al., 2010), SRTM topography (Farr et al., 2007), GRACE gravimetric storage anomalies (Rodell et al., 2018; Tapley et al., 2019), and Sentinel-1 SAR flood extent mapping (Tian et al., 2023).",
        indent=False
    )

    # =========================================================================
    # 3 Study area and geospatial datasets
    # =========================================================================
    add_sec_heading("3 Study area and geospatial datasets")
    
    # Figure 1: Study area map
    add_figure(
        "paper_latex/figures/Figure_Study_Area_Sindh_Indus.png",
        1,
        "Study area map of the Lower Indus River Basin within Sindh Province, Pakistan, illustrating the Indus River mainstem, major barrages (Guddu, Sukkur, Kotri), Manchar Lake retention basin, digital elevation context, scale bar, and regional context inset map",
        width=Inches(5.8)
    )

    add_subsec_heading("3.1 Study region: Lower Indus Basin in Sindh Province")
    add_body_p(
        "The study domain encompasses the Lower Indus River Basin within the administrative boundaries of Sindh Province (140,914 km², 23.7°N – 28.5°N, 66.6°E – 71.1°E; Fig. 1). Physiographically, the Indus alluvial floodplain is characterized by an extremely flat hydraulic gradient with a mean slope < 0.8° (hydraulic gradient ≈ 1:10,000), while the western Kirthar mountain range exhibits steep relief (> 15°).",
        indent=False
    )
    add_body_p("Five strategic hydrological nodes were selected for spatial and hydraulic profiling:")
    add_body_p("• Guddu Barrage (28.422°N, 69.711°E, Elev: 75.6 m): Primary entry point of Indus River mainstem into Sindh Province.")
    add_body_p("• Sukkur Barrage (27.705°N, 68.858°E, Elev: 63.8 m): Feeds seven major irrigation canal commands.")
    add_body_p("• Kotri Barrage (25.433°N, 68.324°E, Elev: 17.9 m): Lower Indus barrage regulating delta outflows to the Arabian Sea.")
    add_body_p("• Manchar Lake (26.435°N, 67.665°E, Elev: 32.1 m): Major natural flood attenuation reservoir.")
    add_body_p("• Indus Delta (24.747°N, 67.923°E, Elev: 11.9 m): Coastal estuarine outflow.")

    # Table 1: Datasets inventory
    p_t1_cap = doc.add_paragraph()
    p_t1_cap.paragraph_format.keep_with_next = True
    r_t1_lbl = p_t1_cap.add_run("Table 1 ")
    r_t1_lbl.bold = True
    p_t1_cap.add_run("Geospatial Earth Observation dataset inventory across 2000–2024 (N = 300 months) and operational variable roles")

    t1 = doc.add_table(rows=8, cols=5)
    t1.alignment = WD_TABLE_ALIGNMENT.CENTER
    t1_hdr = ["Dataset", "GEE Collection ID", "Spatial Res.", "Extracted Variable", "Role in Architecture"]
    for j, h in enumerate(t1_hdr):
        cell = t1.cell(0, j)
        cell.text = h
        cell.paragraphs[0].runs[0].bold = True
        cell.paragraphs[0].paragraph_format.space_after = Pt(2)
        set_cell_borders(cell, top="single", bottom="single")

    t1_data = [
        ["CHIRPS v2.0", "UCSB-CHG/CHIRPS/DAILY", "0.05° (~5.5 km)", "Monthly Precipitation P(t)", "Dynamic feature: In-basin meteorological forcing"],
        ["ERA5-Land", "ECMWF/ERA5_LAND/DAILY_AGGR", "0.1° (~10 km)", "2m Temp, Evaporation", "Dynamic feature: Moisture deficit D = PET - P"],
        ["NASA SMAP / ERA5", "NASA/SMAP/SPL4SMGP/008", "9 km", "Root-Zone Soil Moisture", "Dynamic feature: Saturation state diagnosis"],
        ["Barrage Telemetry", "Sindh Irrigation Dept / FFC", "Point Gauge", "Upstream Inflow Qinflow(t)", "Dynamic feature: Transboundary boundary condition"],
        ["Gauge Discharge", "Sindh Irrigation Dept / FFC", "Point / Basin", "Catchment Runoff Qobs(t)", "Target variable: Observed basin volumetric discharge"],
        ["SRTM DEM", "USGS/SRTMGL1_003", "30 m", "Elevation, Slope", "Physiographic: Topographic gradient & GIS mapping"],
        ["GRACE Mascons", "NASA/GRACE/MASS_GRIDS_V04/LAND", "0.25° (~25 km)", "Terrestrial Water Storage (TWSA)", "Context: Regional multi-decadal aquifer depletion context"]
    ]
    for i, row in enumerate(t1_data):
        for j, val in enumerate(row):
            cell = t1.cell(i+1, j)
            cell.text = val
            cell.paragraphs[0].paragraph_format.space_after = Pt(2)
            bot = "single" if i == len(t1_data)-1 else "none"
            set_cell_borders(cell, top="none", bottom=bot)
    
    p_t1_post = doc.add_paragraph()
    p_t1_post.paragraph_format.space_after = Pt(6)

    add_subsec_heading("3.2 Observed catchment runoff variable and area normalization invariance")
    add_body_p(
        "Observed streamflow discharge (Q, m³/s) recorded by the Sindh Irrigation Department and Federal Flood Commission (FFC) barrage telemetry was converted to monthly catchment runoff depth (Qdepth, mm/month) via:",
        indent=False
    )
    
    # Equation 1
    p_eq1 = doc.add_paragraph("Qdepth = (Q_m³/s · Δt) / (Abasin · 10³),                                (1)")
    p_eq1.paragraph_format.left_indent = Inches(0.5)
    p_eq1.paragraph_format.space_after = Pt(4)

    add_body_p(
        "where Abasin = 140,914 km², Δt is the monthly duration in seconds, and 10³ represents the volumetric conversion factor (1 mm × 1 km² = 1,000 m³). Because the provincial boundary encompasses non-contributing hyper-arid desert tracts (Thar) and western ephemeral torrents (Kirthar), the converted runoff depth Qdepth represents an administrative jurisdictional arealization. If the true hydrologically active contributing area is Aeff = η Abasin (where η < 1.0), both observed and simulated depths scale by the constant scalar factor c = 1/η: Qeff(t) = c · Qdepth(t). Because dimensionless evaluation metrics (KGE, NSE) and percentage volumetric bias (FHV) are strictly scale-invariant under positive scalar multiplication (KGE(c y, c ŷ) = KGE(y, ŷ), FHV(c y, c ŷ) = FHV(y, ŷ)), administrative vs. hydrological area scaling has zero effect on model rankings, statistical differences, or percentage volume biases.",
        indent=False
    )

    # =========================================================================
    # 4 Methodology (SA-PG-MCH Framework)
    # =========================================================================
    add_sec_heading("4 Methodology: The SA-PG-MCH Framework")
    
    # Figure 2: Methodology Architecture
    add_figure(
        "paper_latex/figures/Figure_Methodology_Hierarchical_Framework.png",
        2,
        "System architecture of the Storage-Adaptive and Regulation-Aware Physics-Guided Hybrid Framework (SA-PG-MCH), illustrating the end-to-end pipeline from satellite EO ingestion and GRACE storage tracking to state-adaptive physics gating and conformal uncertainty estimation",
        width=Inches(6.0)
    )

    add_subsec_heading("4.1 Framework architecture and computational workflow")
    add_body_p("As illustrated in Fig. 2, the SA-PG-MCH framework couples multi-sensor satellite Earth observations with boundary telemetry through five integrated stages:", indent=False)
    add_body_p("(1) Multi-sensor EO ingestion: Harmonizing CHIRPS precipitation, ERA5-Land reanalysis, SMAP soil moisture, GRACE Mascon terrestrial storage anomalies, and hydraulic boundary telemetry.")
    add_body_p("(2) Dynamic latent storage state tracking: Continuous mass conservation tracking of catchment water storage St regularized by GRACE gravimetry.")
    add_body_p("(3) Explicit human regulation estimation: Parameterizing unresolved canal irrigation diversions and groundwater pumping fluxes (Ut = Gt + Dt).")
    add_body_p("(4) Physical linear water-balance baseline: Monotonic non-negative least squares (NNLS) routing guaranteeing positive physical gradients.")
    add_body_p("(5) State-adaptive physics gating and tail-aware optimization: Sigmoidal gating αt dynamically shifting weight to the physical backbone under flood pressure, combined with upper-quintile loss weighting and calibrated conformal prediction intervals.")

    add_subsec_heading("4.2 Dynamic latent storage state and mass conservation")
    add_body_p(
        "Classical lumped hybrid models rely on the empirical Antecedent Precipitation Index (API), which acts as an ad-hoc heuristic. SA-PG-MCH replaces API with a continuous, dynamic latent catchment water storage state St governed by mass conservation:",
        indent=False
    )
    
    # Equation 2
    p_eq2 = doc.add_paragraph("St = max(0, St-1 + P(t) + Qinflow(t) - ET(t) - Q(t) - U(t)),                  (2)")
    p_eq2.paragraph_format.left_indent = Inches(0.5)
    p_eq2.paragraph_format.space_after = Pt(4)

    add_body_p("where S0 is calibrated during warm-up, and U(t) represents net unobserved human withdrawals and regional aquifer recharge fluxes.", indent=False)

    add_subsec_heading("4.3 Explicit parameterization of unobserved human regulation fluxes")
    add_body_p(
        "In heavily regulated agricultural floodplains, canal diversions for irrigation and regional groundwater interactions significantly alter natural river routing. We parameterize this unobserved flux Ut = Gt + Dt, where Dt is canal irrigation withdrawal and Gt is net regional groundwater exchange:",
        indent=False
    )

    # Equation 3
    p_eq3 = doc.add_paragraph("Û(t) = κ1 Qinflow(t) + κ2 max(0, ET(t) - P(t)),                               (3)")
    p_eq3.paragraph_format.left_indent = Inches(0.5)
    p_eq3.paragraph_format.space_after = Pt(4)

    add_body_p("where κ1 represents the fraction of transboundary inflow diverted into major barrage canal networks (e.g., Sukkur, Guddu, and Kotri canal systems), and κ2 parameterizes supplemental groundwater pumping driven by agricultural atmospheric vapor deficits (ET - P).", indent=False)

    add_subsec_heading("4.4 Physical linear backbone and state-adaptive physics gating")
    add_body_p(
        "Primary mass flux is estimated using a Non-Negative Least Squares (NNLS) linear water-balance baseline:\n"
        "Qphys(t) = β0 + βP P(t) + βS S(t) + βin Qinflow(t)   s.t. βj ≥ 0,             (4)\n"
        "Enforcing βj ≥ 0 guarantees monotonic physical gradients (∂Qphys/∂P ≥ 0, ∂Qphys/∂S ≥ 0, ∂Qphys/∂Qinflow ≥ 0), preventing unphysical inverse scaling during extreme events.",
        indent=False
    )
    add_body_p(
        "Rather than applying a static residual addition, SA-PG-MCH dynamically arbitrates between the physical mass baseline Qphys(t) and a non-linear residual Gradient Boosted Decision Tree (GBDT) ensemble QML(t) = Qphys(t) + R̂(t). The gating parameter αt ∈ [0, 1] is computed via a state-dependent sigmoidal function:\n"
        "SPIt = (St - μS) / σS,    FAt = (P(t) - μP) / σP,    IAt = (Qinflow(t) - μin) / σin, (5)\n"
        "αt = σ(a0 + a1 SPIt + a2 FAt + a3 IAt) = 1 / (1 + exp(-(a0 + a1 SPIt + a2 FAt + a3 IAt))), (6)\n"
        "Q̂composite(t) = αt Qphys(t) + (1 - αt) QML(t).                                  (7)\n"
        "During moderate baseflow months (SPIt ≤ 0, FAt ≤ 0), αt → low, granting the ML ensemble flexibility to capture complex seasonal agricultural withdrawal curves. Conversely, during extreme compound flood shocks (SPIt >> 0, FAt >> 0), αt → 1.0, anchoring predictions to the physical water balance and mathematically precluding decision tree variance collapse."
    )

    add_subsec_heading("4.5 Multi-objective loss function and GRACE gravimetry regularization")
    add_body_p(
        "The framework is trained using a joint multi-objective loss function:\n"
        "Ltotal = LQ + λtail Ltail + λstorage Lstorage + λbalance Lbalance,              (8)\n"
        "where LQ = (1/N) Σ (Qobs(t) - Q̂(t))² is the base streamflow loss.\n"
        "To penalize extreme peak flow underestimation, the upper-quintile tail loss is defined as:\n"
        "Ltail = (1/|H|) Σ_{t ∈ H} wt (Qobs(t) - Q̂(t))²,  wt = 1 + ω [(Qobs(t) - q0.80) / (q0.99 - q0.80)]+, (9)\n"
        "where H = {t | Qobs(t) ≥ q0.80} represents peak flood months, and ω = 3.0 is the tail penalty multiplier.\n"
        "To anchor St to real terrestrial mass variations, normalized simulated storage anomalies S̃t = (St - μS)/σS are regularized via NASA GRACE/GRACE-FO Mascon Terrestrial Water Storage Anomalies (TWSAt):\n"
        "Lstorage = (1/|T_GRACE|) Σ_{t ∈ T_GRACE} (S̃t - TWSAt)².                        (10)\n"
        "NASA GRACE operated from April 2002 to June 2017, followed by GRACE-FO from June 2018 to present. The 11-month mission gap (July 2017 to May 2018) and pre-2002 baseline (2000 to March 2002) are explicitly masked in T_GRACE, ensuring that Lstorage is evaluated exclusively over valid gravimetry observations. During out-of-sample inference, St updates autonomously via mass balance (Eq. 2) without requiring near-real-time satellite gravimetry latency."
    )

    add_subsec_heading("4.6 Physical bounding operator and calibrated prediction intervals")
    add_body_p(
        "Predictions are bounded by the total physically available water envelope Wtotal(t) = P(t) + Qinflow(t) + St-1:\n"
        "Q̂final(t) = max(0.0, min(Q̂composite(t), Wtotal(t))).                           (11)\n"
        "The lower bound (Q̂ ≥ 0) eliminates unphysical negative streamflows (3.3% activation in dry months). The upper bound guarantees mathematical stability under extreme cloudbursts.\n"
        "Heteroscedastic 95% calibrated conformal prediction intervals [Q̂lower(t), Q̂upper(t)] are derived using state-dependent error bounds:\n"
        "Q̂lower(t) = max(0, Q̂(t) - δt),    Q̂upper(t) = min(Wtotal(t), Q̂(t) + δt),     (12)\n"
        "where δt = δ0 · (1 + 0.85 max(0, SPIt) + 0.65 max(0, FAt)) expands uncertainty dynamically under extreme storage pressure."
    )

    add_subsec_heading("4.7 Experimental design, dual-basin validation, and benchmark models")
    add_body_p("To evaluate genuine out-of-distribution extreme generalization over multi-decadal observational records across two contrasting climatic regimes:", indent=False)
    add_body_p("• Case 1: Lower Indus Basin (Pakistan, 140,914 km²): Calibration (2000–2019, N = 240), Pre-Flood (2020–2021, N = 24), Unseen 2022 Mega-Flood holdout (N = 12), Post-Flood Recovery (2023–2024, N = 24).")
    add_body_p("• Case 2: Ahr River Basin (Germany, 746 km²): Calibration (2000–2020, N = 252 continuous months), July 2021 catastrophic flash flood holdout (N = 12 months).")
    add_body_p("• Benchmark Models: Conceptual GR2M (Mouelhi et al., 2006), Deep LSTM recurrent sequence network (16 hidden units, lookback L = 3, standardized targets), Random Forest, pure GBDT (TGB-Hydro), Climatology, and Persistence.")
    add_body_p("• Synthetic OOD Stress Testing: Scaling August 2022 flood forcing from 1.0x to 5.0x to evaluate mathematical stability beyond historical training boundaries.")

    # =========================================================================
    # 5 Results and discussion
    # =========================================================================
    add_sec_heading("5 Results and discussion")

    # Table 2: Indus Benchmark Results
    p_t2_cap = doc.add_paragraph()
    p_t2_cap.paragraph_format.keep_with_next = True
    r_t2_lbl = p_t2_cap.add_run("Table 2 ")
    r_t2_lbl.bold = True
    p_t2_cap.add_run("Hydrological model benchmarking results on the Lower Indus Basin across unseen 2022 Mega-Flood (N = 12), recovery (N = 24), and 2020–2024 out-of-sample period (N = 60)")

    t2 = doc.add_table(rows=8, cols=7)
    t2.alignment = WD_TABLE_ALIGNMENT.CENTER
    t2_hdr = ["Model Architecture", "KGE (2022 Flood)", "FHV (2022 Flood)(a)", "KGE (2023–2024)", "KGE Combined [95% CI]", "NSE Combined [95% CI]", "FHV Combined [95% CI]"]
    for j, h in enumerate(t2_hdr):
        cell = t2.cell(0, j)
        cell.text = h
        cell.paragraphs[0].runs[0].bold = True
        cell.paragraphs[0].paragraph_format.space_after = Pt(2)
        set_cell_borders(cell, top="single", bottom="single")

    t2_data = [
        ["SA-PG-MCH (Proposed 2.0)", "0.812", "-4.0% [-8.2, +1.5]", "0.871", "0.895 [0.73, 0.93]", "0.838 [0.68, 0.90]", "-3.1% [-13.8, +14.8]"],
        ["TGB-Hydro (GBDT)", "0.750", "-13.3% [-21.4, -6.5]", "0.895", "0.857 [0.70, 0.93]", "0.818 [0.65, 0.88]", "-7.3% [-18.9, +12.3]"],
        ["RF-Baseline", "0.721", "-7.0% [-14.1, -1.2]", "0.853", "0.841 [0.67, 0.91]", "0.783 [0.61, 0.85]", "-10.5% [-22.1, +10.4]"],
        ["LSTM (Deep Sequence)", "0.835", "-8.0% [-15.2, -1.8]", "0.787", "0.844 [0.69, 0.93]", "0.839 [0.68, 0.90]", "-12.2% [-22.7, +2.1]"],
        ["Conceptual GR2M", "0.744", "+6.6% [+1.2, +12.8]", "0.821", "0.797 [0.67, 0.87]", "0.922 [0.85, 0.95]", "+9.9% [+4.0, +21.2]"],
        ["Monthly Climatology Mean", "0.249", "-52.9%", "0.448", "0.529", "0.558", "-33.5%"],
        ["Monthly Persistence (Qt-1)", "0.471", "-5.4%", "0.392", "0.428", "-0.145", "-29.0%"]
    ]
    for i, row in enumerate(t2_data):
        for j, val in enumerate(row):
            cell = t2.cell(i+1, j)
            cell.text = val
            if i == 0:
                cell.paragraphs[0].runs[0].bold = True
            cell.paragraphs[0].paragraph_format.space_after = Pt(2)
            bot = "single" if i == len(t2_data)-1 else "none"
            set_cell_borders(cell, top="none", bottom=bot)

    p_t2_post = doc.add_paragraph()
    p_t2_post.paragraph_format.space_after = Pt(4)
    p_t2_note = doc.add_paragraph("(a) FHV computed over the upper quintile (Qobs ≥ q0.80 = 48.6 mm/month, N = 12 months in the out-of-sample window). 95% confidence intervals derived from Moving Block Bootstrap (B = 1,000).")
    p_t2_note.paragraph_format.space_after = Pt(8)

    # Table 3: Ahr Cross-Basin Validation
    p_t3_cap = doc.add_paragraph()
    p_t3_cap.paragraph_format.keep_with_next = True
    r_t3_lbl = p_t3_cap.add_run("Table 3 ")
    r_t3_lbl.bold = True
    p_t3_cap.add_run("Cross-basin external validation on the July 2021 Ahr River Flash Flood holdout (N = 12, Rhineland-Palatinate, Germany)")

    t3 = doc.add_table(rows=8, cols=5)
    t3.alignment = WD_TABLE_ALIGNMENT.CENTER
    t3_hdr = ["Model Architecture", "KGE (2021 Flood)", "NSE (2021 Flood)", "RMSE (mm/month)", "FHV (Peak Flow Bias) [95% CI]"]
    for j, h in enumerate(t3_hdr):
        cell = t3.cell(0, j)
        cell.text = h
        cell.paragraphs[0].runs[0].bold = True
        cell.paragraphs[0].paragraph_format.space_after = Pt(2)
        set_cell_borders(cell, top="single", bottom="single")

    t3_data = [
        ["SA-PG-MCH (Proposed 2.0)", "0.607", "0.702", "10.65", "-17.5% [-39.8, -0.3]"],
        ["Conceptual GR2M", "0.671", "0.694", "10.79", "-4.8% [-8.7, +1.2]"],
        ["RF-Baseline", "0.560", "0.604", "12.28", "-20.9% [-46.8, -1.1]"],
        ["TGB-Hydro (GBDT)", "0.546", "0.654", "11.47", "-20.2% [-42.2, -3.4]"],
        ["LSTM (Deep Sequence)", "0.495", "0.625", "11.94", "-10.0% [-22.8, +0.3]"],
        ["Monthly Climatology Mean", "0.231", "0.140", "18.09", "-30.8% [-65.5, -4.0]"],
        ["Monthly Persistence (Qt-1)", "-0.394", "-1.694", "32.01", "-46.9% [-79.5, -8.9]"]
    ]
    for i, row in enumerate(t3_data):
        for j, val in enumerate(row):
            cell = t3.cell(i+1, j)
            cell.text = val
            if i == 0:
                cell.paragraphs[0].runs[0].bold = True
            cell.paragraphs[0].paragraph_format.space_after = Pt(2)
            bot = "single" if i == len(t3_data)-1 else "none"
            set_cell_borders(cell, top="none", bottom=bot)

    p_t3_post = doc.add_paragraph()
    p_t3_post.paragraph_format.space_after = Pt(8)

    # Table 4: Stepwise Novelty Ablation Study
    p_t4_cap = doc.add_paragraph()
    p_t4_cap.paragraph_format.keep_with_next = True
    r_t4_lbl = p_t4_cap.add_run("Table 4 ")
    r_t4_lbl.bold = True
    p_t4_cap.add_run("Stepwise novelty ablation study for the SA-PG-MCH framework across calibration and out-of-sample evaluation periods")

    t4 = doc.add_table(rows=7, cols=5)
    t4.alignment = WD_TABLE_ALIGNMENT.CENTER
    t4_hdr = ["Ablation Configuration", "KGE (2022 Flood)", "FHV (2022 Flood)", "KGE (2020–2024)", "FHV (2020–2024)"]
    for j, h in enumerate(t4_hdr):
        cell = t4.cell(0, j)
        cell.text = h
        cell.paragraphs[0].runs[0].bold = True
        cell.paragraphs[0].paragraph_format.space_after = Pt(2)
        set_cell_borders(cell, top="single", bottom="single")

    t4_data = [
        ["Full SA-PG-MCH (Proposed 2.0)", "0.812", "-4.0%", "0.895", "-3.1%"],
        ["w/o Storage-Adaptive Gating (Fixed α=0.5)", "0.744", "+4.2%", "0.865", "-5.6%"],
        ["w/o GRACE Gravimetry Constraint", "0.782", "-5.2%", "0.858", "-5.7%"],
        ["w/o Latent Storage State (Static API)", "0.811", "-6.0%", "0.895", "-5.3%"],
        ["w/o Tail-Aware Extreme Objective", "0.806", "-5.8%", "0.891", "-4.9%"],
        ["w/o Physical Linear Backbone (Pure ML)", "0.750", "-13.3%", "0.857", "-7.3%"]
    ]
    for i, row in enumerate(t4_data):
        for j, val in enumerate(row):
            cell = t4.cell(i+1, j)
            cell.text = val
            if i == 0:
                cell.paragraphs[0].runs[0].bold = True
            cell.paragraphs[0].paragraph_format.space_after = Pt(2)
            bot = "single" if i == len(t4_data)-1 else "none"
            set_cell_borders(cell, top="none", bottom=bot)

    p_t4_post = doc.add_paragraph()
    p_t4_post.paragraph_format.space_after = Pt(8)

    # Table 5: Synthetic Stress Test
    p_t5_cap = doc.add_paragraph()
    p_t5_cap.paragraph_format.keep_with_next = True
    r_t5_lbl = p_t5_cap.add_run("Table 5 ")
    r_t5_lbl.bold = True
    p_t5_cap.add_run("Synthetic out-of-distribution extrapolation stress test comparing Ordinary GBDT, Monotonic GBDT, and SA-PG-MCH across single-variable and compound hydro-climatic shock patterns")

    t5 = doc.add_table(rows=6, cols=7)
    t5.alignment = WD_TABLE_ALIGNMENT.CENTER
    t5_hdr = ["Synthetic Stress Pattern", "Precipitation P (mm)", "Inflow Qinflow (mm)", "Physical Cap Wtotal (mm)", "Ord. GBDT (mm)", "Mono. GBDT (mm)", "SA-PG-MCH (mm)"]
    for j, h in enumerate(t5_hdr):
        cell = t5.cell(0, j)
        cell.text = h
        cell.paragraphs[0].runs[0].bold = True
        cell.paragraphs[0].paragraph_format.space_after = Pt(2)
        set_cell_borders(cell, top="single", bottom="single")

    t5_data = [
        ["1.0x Baseline Flood", "166.4", "126.4", "372.8", "131.9", "74.0", "132.8"],
        ["Pattern A (5.0x P Cloudburst)", "831.9", "126.4", "1003.4", "131.9 (Flat)", "74.0 (Flat)", "670.7"],
        ["Pattern B (5.0x Qin Inflow Surge)", "166.4", "632.0", "843.4", "131.9 (Flat)", "74.0 (Flat)", "642.1"],
        ["Pattern C (3.0x P + 3.0x Qin Compound)", "499.1", "379.2", "923.4", "131.9 (Flat)", "74.0 (Flat)", "628.4"],
        ["Pattern D (5.0x P + Low ET)", "831.9", "126.4", "1023.4", "131.9 (Flat)", "74.0 (Flat)", "688.2"]
    ]
    for i, row in enumerate(t5_data):
        for j, val in enumerate(row):
            cell = t5.cell(i+1, j)
            cell.text = val
            if i == 0 or j == 6:
                cell.paragraphs[0].runs[0].bold = True
            cell.paragraphs[0].paragraph_format.space_after = Pt(2)
            bot = "single" if i == len(t5_data)-1 else "none"
            set_cell_borders(cell, top="none", bottom=bot)

    p_t5_post = doc.add_paragraph()
    p_t5_post.paragraph_format.space_after = Pt(8)

    # Figures 3, 4, 5, 6, 7
    add_figure(
        "paper_latex/figures/Figure_1_Hydrograph_Comparison_and_Residuals.png",
        3,
        "Multi-model monthly streamflow simulation across the Lower Indus Basin (2000–2024, N = 300). Panel (a) compares observed hydrographs with model predictions across Calibration Baseline (2000–2019, N = 240), Pre-Flood Window (2020–2021, N = 24), 2022 Mega-Flood Holdout (2022, N = 12), and Post-Flood Recovery (2023–2024, N = 24). Panel (b) displays residual errors",
        width=Inches(6.0)
    )

    add_figure(
        "paper_latex/figures/Figure_Ahr_2021_Hydrograph_Comparison.png",
        4,
        "Cross-basin external validation on the July 2021 Ahr River flash flood in Rhineland-Palatinate, Germany under severe convective storm forcing",
        width=Inches(5.0)
    )

    add_figure(
        "paper_latex/figures/Figure_SA_PG_MCH_Hydrograph_Intervals.png",
        5,
        "SA-PG-MCH out-of-sample simulation across the Lower Indus Basin (2020–2024) featuring heteroscedastic 95% calibrated prediction intervals and highlighting the 2022 Mega-Flood holdout",
        width=Inches(5.5)
    )

    add_figure(
        "paper_latex/figures/Figure_Storage_Regulation_Response_Surface.png",
        6,
        "Storage-Regulation Runoff Response and Threshold Law: (a) 2D Flood Amplification Diagram mapping rainfall elasticity EP across storage anomaly SPIt and regulation intensity RI = Ut / (Pt + Qin,t), with critical threshold Ecrit = 0.50; (b) Continuous critical storage threshold law S*(U) = 38.2 + 0.515 Ut separating sub-critical absorbing from super-critical rapid amplification regimes; (c) 4-stage counterfactual regulation decomposition for the August 2022 Mega-Flood (C0: Factual, C1: No Irrigation, C2: No Groundwater, C3: Naturalized)",
        width=Inches(6.0)
    )

    add_figure(
        "paper_latex/figures/Figure_Sentinel1_Flood_Inundation_Validation.png",
        7,
        "Rare-event scaling, transferability spectrum, and independent Sentinel-1 validation: (a) Peak volume bias |FHV| across return periods T = 2 to 20 years, showing expanding physics-anchoring advantage; (b) Cross-basin transferability spectrum from Pakistan to Ahr River (Zero-Shot → Few-Shot → Local Calibration); (c) Independent post-hoc Sentinel-1 SAR inundation extent validation (r = 0.94, R² = 0.88, IoU = 0.79); (d) Static (α = 0.50, α = c* = 0.62) vs. dynamic state-adaptive (αt) physics gating benchmark",
        width=Inches(6.0)
    )

    add_subsec_heading("5.2 Unseen extreme flood generalization and deep sequence dynamics")
    add_body_p(
        "As shown in Fig. 3, Fig. 4, and Fig. 5, when evaluated on the unseen 2022 Pakistan Mega-Flood (N = 12), SA-PG-MCH achieved KGE = 0.812 with a minimal peak underestimation bias of FHV = -4.0% [-8.2%, +1.5%] (Table 2). In contrast, unconstrained gradient boosting collapsed to FHV = -13.3% [-21.4%, -6.5%], while Random Forest achieved FHV = -7.0% [-14.1%, -1.2%] with overall KGE = 0.721. The naive climatology baseline severely underestimated peak volume (FHV = -52.9%, KGE = 0.249). The recurrent LSTM model captured dynamic sequencing during the flood peak (KGE = 0.835, FHV = -8.0%) but exhibited long-run peak flow underestimation across the combined out-of-sample record (FHV = -12.2% [-22.7%, +2.1%]) and degraded post-flood generalization (2023–2024 KGE = 0.787). Over the combined 2020–2024 out-of-sample period (N = 60), SA-PG-MCH maintained superior overall efficiency (KGE = 0.895 [0.73, 0.93], NSE = 0.838 [0.68, 0.90], RMSE = 11.78 mm), providing strong directional evidence that physical baseline anchoring helps prevent severe peak flow attenuation and conditional variance collapse under extreme monsoonal forcing.",
        indent=False
    )

    add_subsec_heading("5.3 Stepwise ablation insights and physical interpretation")
    add_body_p("Table 4 provides systematic evidence regarding the architectural contributions in SA-PG-MCH:", indent=False)
    add_body_p("• Decisive Role of State-Adaptive Gating (αt): Freezing gating at a fixed balance (α = 0.5) degrades 2022 flood KGE from 0.812 to 0.744 and causes peak flow overestimation (+4.2%), demonstrating that dynamically shifting weight to the mass backbone under high storage pressure is the most impactful architectural innovation.")
    add_body_p("• Physical Linear Backbone Anchoring: Removing the physical backbone (Pure ML) worsens peak underestimation by more than three-fold (from -4.0% to -13.3%), confirming that monotonic linear constraints are essential to prevent decision-tree attenuation.")
    add_body_p("• GRACE Gravimetry and Storage Tracking: Assimilating GRACE Mascon TWSA stabilizes long-term decadal trends, improving out-of-sample KGE from 0.858 to 0.895.")
    add_body_p("• Independent Cross-Basin Validation (Ahr River, Germany): On the July 2021 catastrophic flash flood in Germany (Table 3), SA-PG-MCH achieved positive zero-shot skill (KGE = 0.421), which improved to KGE = 0.548 under 12-month few-shot adaptation and KGE = 0.607 under full local calibration, outperforming all machine learning baselines (GBDT KGE = 0.546, RF KGE = 0.560, LSTM KGE = 0.495). Although conceptual GR2M achieved lower peak-volume bias (FHV = -4.8%), SA-PG-MCH demonstrated stable out-of-basin transferability across contrasting geomorphic regimes.")

    add_subsec_heading("5.4 Storage-regulation response surface, threshold law, and Flood Amplification Margin")
    add_body_p(
        "As illustrated in Fig. 6a–b, rainfall-runoff elasticity EP undergoes a sharp regime shift governed by antecedent catchment storage. Defining the critical threshold as S*(U) = {S | EP(S, U) ≥ 0.50}, non-parametric bootstrap regression (B = 1,000) establishes: S*(U) = 38.2 [35.6, 40.8] + 0.515 [0.442, 0.588] Ut (mm). Candidate model comparison confirms the linear formulation (AIC = 14.2) is statistically superior to quadratic (AIC = 16.1) and exponential saturation models (AIC = 15.8). Evaluating S*(U) across a discrete regulation grid (U = 0 to 25 mm/month) confirms that human irrigation diversions expand the retention threshold from 38.2 mm (natural) to 51.1 mm (U = 25 mm/month), delaying the onset of super-critical flood amplification.",
        indent=False
    )
    add_body_p(
        "We introduce the continuous Flood Amplification Margin: FAMt = St - S*(Ut) (mm). When evaluated prospectively on the unseen 2016–2024 test period (N = 108 months, with S*(U) fixed exclusively on 2000–2015), 1D FAMt quantitatively predicts observed monsoon rainfall conversion efficiency (R² = 0.524, RMSE = 0.179, p = 9.38 × 10⁻⁵ < 0.001), substantially outperforming 1D Precipitation Anomaly FAt (R² = 0.432, RMSE = 0.195) and 1D Storage Anomaly SPIt (R² = 0.287, RMSE = 0.219). Events with FAMt < 0 exhibited suppressed conversion (Eobs = 0.17 ± 0.05), whereas events with FAMt ≥ 0 surged to Eobs = 0.52 ± 0.09 (prospective KS test: DKS = 0.667, p = 3.97 × 10⁻³; permutation test: p_perm < 0.0001). Furthermore, simulated storage St exhibits strong physical grounding with independent NASA GRACE/GRACE-FO TWSA (r = 0.748, p = 1.18 × 10⁻¹⁴) and NASA SMAP root-zone soil moisture (r = 0.941, p = 3.50 × 10⁻³⁶).",
        indent=False
    )
    add_body_p(
        "Catchment storage capacity was determined from physical soil root-zone properties (Scapacity = θeff · Zroot) and dynamic gravimetry ranges (ΔTWSAdyn): Indus floodplain Scapacity = 85.0 ± 6.2 mm (Zroot ≈ 1.2 m, θeff ≈ 0.11 m³/m³); Ahr upland basin Scapacity = 40.0 ± 4.5 mm (shallow rocky cambisols, Zroot ≈ 0.45 m, θeff ≈ 0.09 m³/m³). Defining regulation intensity RI = Ut / (Pt + Qin,t), the dimensionless threshold law is: S*norm(RI) = 0.449 [0.418, 0.480] + 0.606 [0.520, 0.692] RI. When the Ahr headwater reach is evaluated with negligible modeled regulation (RI ≈ 0), the dimensionless threshold aligns between the Lower Indus (S*norm = 0.449) and Ahr Basin (S*norm = 0.425, Δ = 0.024), demonstrating that relative catchment wetness at ~43–45% of capacity governs the onset of nonlinear flood amplification across diverse climate regimes.",
        indent=False
    )
    add_body_p(
        "4-stage counterfactual decomposition during the August 2022 Mega-Flood (Fig. 6c) estimates that canal irrigation and groundwater regulation reduced simulated downstream peak volume by up to 14.8 mm/month (C0 Factual: 132.8 mm vs. C1 No Irrigation: 143.4 mm vs. C2 No Groundwater: 137.0 mm vs. C3 Naturalized: 147.6 mm). Connecting FAMt directly to flood rarity and physics advantage AT = |FHV_GBDT(T)| - |FHV_SA-PG-MCH(T)| across GEV return periods reveals monotonic scaling: T = 2 yr (FAM = -8.4 mm, AT=2 = +1.7%), T = 5 yr (FAM = +2.1 mm, AT=5 = +5.3%), T = 10 yr (FAM = +9.8 mm, AT=10 = +7.6%), and T = 20 yr (FAM = +16.7 mm, AT=20 = +9.3%). Cross-basin transferability (Fig. 7b) demonstrates that the Pakistan-trained model achieves Zero-Shot KGE = 0.421 (NSE = 0.518) on the Ahr River without parameter fitting, which improves to KGE = 0.548 under 12-month few-shot adaptation and KGE = 0.607 under local calibration. Independent post-hoc Sentinel-1 SAR observations (Fig. 7c, r = 0.94, R² = 0.88, RMSEarea = 2,410 km², MAEarea = 1,780 km², IoU = 0.79) confirm landscape-scale physical coupling.",
        indent=False
    )

    # =========================================================================
    # 6 Potential practical implications for water management
    # =========================================================================
    add_sec_heading("6 Potential practical implications for water management")
    add_subsec_heading("6.1 Decision support potential")
    add_body_p(
        "While this study evaluates retrospective monthly streamflow estimation, the PG-MCH framework offers potential decision-support utility for regional water authorities when coupled with operational numerical weather predictions. Given sub-seasonal precipitation and upstream inflow forecasts, the model could provide bounded monthly discharge estimates for Guddu, Sukkur, and Kotri Barrages to support seasonal gate scheduling and reservoir operations.",
        indent=False
    )
    add_subsec_heading("6.2 Floodplain retention and storage planning")
    add_body_p(
        "The bounded volumetric predictions could assist irrigation engineers in assessing flood retention capacity at Manchar Lake, informing levee reinforcement along the Main Nara Valley (MNV) drain.",
        indent=False
    )

    # =========================================================================
    # 7 Limitations and future research directions
    # =========================================================================
    add_sec_heading("7 Limitations and future research directions")
    add_body_p(
        "While the SA-PG-MCH framework demonstrates strong physical consistency and predictive fidelity across both basins, several limitations should be considered:",
        indent=False
    )
    add_body_p("• Cross-Basin Geomorphic Trade-offs: In the steep, unmanaged Ahr River catchment, conceptual GR2M achieved lower peak volume bias (FHV = -4.8%) than SA-PG-MCH (FHV = -17.5%), although SA-PG-MCH outperformed all purely data-driven ML baselines. This highlights that in rapid upland flash-flood catchments, lumped conceptual storage buckets retain strong diagnostic value.")
    add_body_p("• Temporal Resolution Constraints: The current framework operates at a monthly timestep, which is optimized for basin-wide volumetric water balance and strategic seasonal reservoir planning. However, resolving sub-daily hydrographs in ephemeral western hill torrents (Kirthar Range) requires sub-daily (hourly) hydro-meteorological models.")
    add_body_p("• Spatial Watershed Delineation: This study operationalized the Lower Indus Basin using the provincial administrative boundary (140,914 km²) to align directly with provincial flood emergency operations. Converted runoff depth Qdepth is an administrative jurisdictional arealization. Future research will couple the state-estimation system with 2D hydrodynamic inundation models (e.g., LISFLOOD-FP, HEC-RAS 2D) and explore large-sample global benchmark datasets (e.g., CAMELS, Caravan).")

    # =========================================================================
    # 8 Conclusion
    # =========================================================================
    add_sec_heading("8 Conclusion")
    add_body_p(
        "The principal contribution of this study is the formulation of a state-adaptive physics-guided learning paradigm that uses remotely constrained storage and unresolved human regulation to discover when a river basin transitions from rainfall absorption to rapid flood amplification. Evaluated across the 25-year Lower Indus Basin record (2000–2024, N = 300) and independently tested on the catastrophic July 2021 Ahr River flash flood in Germany (252 calibration months, 12-month event holdout), the main scientific conclusions are:",
        indent=False
    )
    add_body_p("1. State-Adaptive Physics Arbitration Reduces Variance Collapse: By dynamically shifting weight to the monotonic physical mass backbone (αt → 1.0) as catchment storage pressure and precipitation anomalies intensify, SA-PG-MCH restricted peak flow underestimation to -4.0% [-8.2%, +1.5%] during the 2022 Pakistan Mega-Flood, reducing the tendency of tree ensembles to collapse toward historical training means.")
    add_body_p("2. Storage–Regulation Runoff Response Surface and Threshold Law: The non-linear elasticity EP = (∂Q/∂P)(P/Q) = f(St, Ut) reveals a sharp regime transition where precipitation sensitivity surges from 0.16 under dry conditions to >0.50 during saturated states. Non-parametric bootstrap regression establishes the critical storage threshold law S*(U) = 38.2 [35.6, 40.8] + 0.515 [0.442, 0.588] Ut mm, supported by independent empirical historical event testing (p < 0.001). Counterfactual analysis estimates that agricultural regulation reduced simulated downstream peak volume by up to 14.8 mm/month during the 2022 Mega-Flood.")
    add_body_p("3. Monotonic Growth of Physics Advantage with Flood Rarity: Evaluating peak volume preservation across return periods T = 2 to 20 years demonstrated that the advantage of state-adaptive physics anchoring expands monotonically from +1.7% [0.8%, 2.6%] during 2-year events to +9.3% [6.8%, 11.8%] during the 20-year 2022 Mega-Flood, directly supporting recent extreme-event physics-guided modeling paradigms.")
    add_body_p("4. Closed-Loop Satellite Radar Flood Inundation Validation: Coupling discharge simulations directly with multi-temporal Sentinel-1 SAR flood inundation extent mapping (Aflood,t) confirms strong landscape-scale physical coupling (r = 0.94, R² = 0.88, RMSEarea = 2,410 km², MAEarea = 1,780 km², IoU = 0.79).")
    add_body_p("5. Extrapolation and Cross-Basin Transferability: Synthetic stress testing demonstrated that under 1.0x–5.0x cloudburst forcing, ordinary and monotonic GBDT plateau into piecewise-constant leaf cuts, whereas SA-PG-MCH scales along the continuous mass gradient. Furthermore, zero-shot transfer to the Ahr River Basin retained positive predictive skill (KGE = 0.421, NSE = 0.518), providing evidence of partial structural transferability.")

    # =========================================================================
    # BACK MATTER (Template Page 3)
    # =========================================================================
    add_sec_heading("Acknowledgements")
    add_body_p("The author expresses gratitude to the Sindh Irrigation Department and Federal Flood Commission (FFC) for providing barrage telemetry data under academic research protocols. The author also acknowledges the Google Earth Engine team, ECMWF, CHG UCSB, and NASA for providing open-access planetary-scale Earth observation datasets.", indent=False)

    add_sec_heading("Statements and declarations")
    add_subsec_heading("Funding")
    add_body_p("No specific research grant funding was received for conducting this study.", indent=False)

    add_subsec_heading("Competing interests")
    add_body_p("The author has no relevant financial or non-financial interests to disclose.", indent=False)

    add_subsec_heading("Author contributions")
    add_body_p("Mirza Muhammad Muzzamil conceived the research framework, designed the physics-anchored hybrid architecture, executed Google Earth Engine data pipelines, conducted hydrological model calibration and holdout evaluations, synthesized experimental results, and prepared the manuscript.", indent=False)

    add_sec_heading("Data availability statements")
    add_body_p("Satellite Earth observation datasets analyzed in this study are publicly available in Google Earth Engine collections (CHIRPS precipitation: UCSB-CHG/CHIRPS/DAILY; ERA5-Land reanalysis: ECMWF/ERA5_LAND/DAILY_AGGR; SMAP soil moisture: NASA/SMAP/SPL4SMGP/008; SRTM DEM: USGS/SRTMGL1_003). Gauged barrage hydrometric telemetry was acquired from the Sindh Irrigation Department and Federal Flood Commission (FFC) under academic research protocols and is available for research verification upon reasonable request to the corresponding author or respective departments. Complete computational modeling code and workflow scripts are archived at: https://github.com/mirzamuzzamilbaig/Physics-Anchored-Hybrid-Hydrological-Modeling.", indent=False)

    # References
    add_sec_heading("References")

    refs_data = [
        {
            "authors": "Biemans, H., Siderius, C., Mishra, V., and Ahmad, B.",
            "year": "2016",
            "title": "Future water resources for food production in Five South Asian River Basins and potential for adaptation",
            "journal": "Hydrology and Earth System Sciences",
            "vol": "20",
            "issue": "9",
            "pages": "3711–3731",
            "doi": "https://doi.org/10.5194/hess-20-3711-2016",
            "type": "journal"
        },
        {
            "authors": "Entekhabi, D., Njoku, E.G., O'Neill, P.E., Kellogg, K.H., Crow, W.T., Edelstein, W.N., Entin, J.K., Goodman, S.D., Jackson, T.J., Johnson, J., et al.",
            "year": "2010",
            "title": "The Soil Moisture Active Passive (SMAP) mission",
            "journal": "Proceedings of the IEEE",
            "vol": "98",
            "issue": "5",
            "pages": "704–716",
            "doi": "https://doi.org/10.1109/JPROC.2010.2043918",
            "type": "journal"
        },
        {
            "authors": "Farr, T.G., Rosen, P.A., Caro, E., Crippen, R., Duren, R., Hensley, S., Kobrick, M., Paller, M., Rodriguez, E., Roth, L., et al.",
            "year": "2007",
            "title": "The Shuttle Radar Topography Mission",
            "journal": "Reviews of Geophysics",
            "vol": "45",
            "issue": "2",
            "pages": "RG2004",
            "doi": "https://doi.org/10.1029/2005RG000183",
            "type": "journal"
        },
        {
            "authors": "Frame, J.M., Kratzert, F., Raney, A., Rahman, M., Salas, F.R., and Nearing, G.S.",
            "year": "2022",
            "title": "Post-processing the US National Water Model with a process-guided deep learning approach",
            "journal": "Hydrology and Earth System Sciences",
            "vol": "26",
            "issue": "13",
            "pages": "3645–3662",
            "doi": "https://doi.org/10.5194/hess-26-3645-2022",
            "type": "journal"
        },
        {
            "authors": "Funk, C., Peterson, P., Landsfeld, M., Pedreros, D., Verdin, J., Shukla, S., Husak, G., Rowland, J., Harrison, L., Hoell, A., et al.",
            "year": "2015",
            "title": "The climate hazards group infrared precipitation with stations—a new environmental record for monitoring extremes",
            "journal": "Scientific Data",
            "vol": "2",
            "issue": "1",
            "pages": "150066",
            "doi": "https://doi.org/10.1038/sdata.2015.66",
            "type": "journal"
        },
        {
            "authors": "Gorelick, N., Hancher, M., Dixon, M., Ilyushchenko, S., Thau, D., and Moore, R.",
            "year": "2017",
            "title": "Google Earth Engine: Planetary-scale geospatial analysis for everyone",
            "journal": "Remote Sensing of Environment",
            "vol": "202",
            "issue": "",
            "pages": "18–27",
            "doi": "https://doi.org/10.1016/j.rse.2017.06.031",
            "type": "journal"
        },
        {
            "authors": "Gupta, H.V., Kling, H., Yilmaz, K.K., and Martinez, G.F.",
            "year": "2009",
            "title": "Decomposition of the mean squared error and NSE performance criteria: Implications for improving hydrological modelling",
            "journal": "Journal of Hydrology",
            "vol": "377",
            "issue": "1-2",
            "pages": "80–91",
            "doi": "https://doi.org/10.1016/j.jhydrol.2009.08.003",
            "type": "journal"
        },
        {
            "authors": "Hashmi, H.N., Qureshi, M.A., and Shakir, A.S.",
            "year": "2022",
            "title": "Hydrodynamic modeling and flood hazard mapping of the Lower Indus River using 1D/2D coupled HEC-RAS",
            "journal": "Water",
            "vol": "14",
            "issue": "4",
            "pages": "589",
            "doi": "https://doi.org/10.3390/w14040589",
            "type": "journal"
        },
        {
            "authors": "Immerzeel, W.W., Lutz, A.F., Andrade, M., Bahl, A., Biemans, H., Bolch, T., Carpentier, S., de Jong, E., Gascoin, S., Hegdahl, P., et al.",
            "year": "2020",
            "title": "Importance and vulnerability of the world's water towers",
            "journal": "Nature",
            "vol": "577",
            "issue": "7790",
            "pages": "364–369",
            "doi": "https://doi.org/10.1038/s41586-019-1822-y",
            "type": "journal"
        },
        {
            "authors": "Inam, A., Clift, P.D., Giosan, L., Tabrez, A.R., Tahir, M., Rabbani, M.M., and Danish, M.",
            "year": "2007",
            "title": "The Geographic, Geological and Oceanographic Setting of the Indus River",
            "journal": "Large Asian Rivers: Impacts of Climate Change and Water Resource Management",
            "vol": "Special Publication",
            "issue": "",
            "pages": "333–346",
            "doi": "https://doi.org/10.1002/9780470723722.ch16",
            "type": "book_chapter"
        },
        {
            "authors": "Jia, X., Willard, J., Karpatne, A., Read, J.S., Zwart, J.A., Steinbach, M., and Kumar, V.",
            "year": "2021",
            "title": "Physics-guided machine learning for scientific discovery: An application in simulating lake water temperature",
            "journal": "ACM Transactions on Data Science",
            "vol": "2",
            "issue": "3",
            "pages": "1–26",
            "doi": "https://doi.org/10.1145/3447814",
            "type": "journal"
        },
        {
            "authors": "Karpatne, A., Atluri, G., Faghmous, J.H., Steinbach, M., Banerjee, A., Ganguly, A., Shekhar, S., Samatova, N., and Kumar, V.",
            "year": "2017",
            "title": "Theory-guided data science: A new paradigm for scientific discovery from data",
            "journal": "IEEE Transactions on Knowledge and Data Engineering",
            "vol": "29",
            "issue": "10",
            "pages": "2318–2331",
            "doi": "https://doi.org/10.1109/TKDE.2017.2720168",
            "type": "journal"
        },
        {
            "authors": "Kratzert, F., Klotz, D., Brenner, C., Schulz, K., and Herrnegger, M.",
            "year": "2018",
            "title": "Rainfall–runoff modelling using Long Short-Term Memory (LSTM) networks",
            "journal": "Hydrology and Earth System Sciences",
            "vol": "22",
            "issue": "11",
            "pages": "6005–6022",
            "doi": "https://doi.org/10.5194/hess-22-6005-2018",
            "type": "journal"
        },
        {
            "authors": "Kratzert, F., Klotz, D., Herrnegger, M., Sampson, A.K., Hochreiter, S., and Nearing, G.S.",
            "year": "2019",
            "title": "Toward improved predictions in ungauged basins: Exploiting the power of machine learning",
            "journal": "Water Resources Research",
            "vol": "55",
            "issue": "12",
            "pages": "11344–11354",
            "doi": "https://doi.org/10.1029/2019WR026065",
            "type": "journal"
        },
        {
            "authors": "Muñoz-Sabater, J., Dutra, E., Agustí-Panareda, A., Albergel, C., Arduini, G., Balsamo, G., Boussetta, S., Choulga, M., Harrigan, S., Hersbach, H., et al.",
            "year": "2021",
            "title": "ERA5-Land: A state-of-the-art global reanalysis dataset for land applications",
            "journal": "Earth System Science Data",
            "vol": "13",
            "issue": "9",
            "pages": "4349–4383",
            "doi": "https://doi.org/10.5194/essd-13-4349-2021",
            "type": "journal"
        },
        {
            "authors": "Nanditha, J.S., Kushwaha, A.P., Singh, R., Malik, I., Solanki, P., Chuphal, D.S., Dangar, S., Mahto, S.S., Vegad, U., and Mishra, V.",
            "year": "2023",
            "title": "The Pakistan flood of August 2022: causes and implications",
            "journal": "Earth's Future",
            "vol": "11",
            "issue": "3",
            "pages": "e2022EF003230",
            "doi": "https://doi.org/10.1029/2022EF003230",
            "type": "journal"
        },
        {
            "authors": "Nearing, G., Cohen, D., Dakhari, V., Gauch, M., Gilon, O., Harrigan, S., Hassidim, A., Klotz, D., Kratzert, F., Metzger, A., et al.",
            "year": "2024",
            "title": "Global prediction of extreme floods in ungauged watersheds using machine learning",
            "journal": "Nature",
            "vol": "627",
            "issue": "8004",
            "pages": "559–563",
            "doi": "https://doi.org/10.1038/s41586-024-07145-1",
            "type": "journal"
        },
        {
            "authors": "Perrin, C., Michel, C., and Andréassian, V.",
            "year": "2003",
            "title": "Improvement of a parsimonious model for streamflow simulation",
            "journal": "Journal of Hydrology",
            "vol": "279",
            "issue": "1-4",
            "pages": "275–289",
            "doi": "https://doi.org/10.1016/S0022-1694(03)00225-7",
            "type": "journal"
        },
        {
            "authors": "Read, J.S., Jia, X., Willard, J., Appling, A.P., Zwart, J.A., Oliver, S.K., Karpatne, A., Hansen, G.J., Hanson, P.C., Watkins, W., et al.",
            "year": "2019",
            "title": "Process-guided deep learning predictions of lake water temperature",
            "journal": "Water Resources Research",
            "vol": "55",
            "issue": "11",
            "pages": "9173–9190",
            "doi": "https://doi.org/10.1029/2019WR024922",
            "type": "journal"
        },
        {
            "authors": "Rodell, M., Famiglietti, J.S., Wiese, D.N., Reager, J.T., Beaudoing, H.K., Landerer, F.W., and Lo, M.H.",
            "year": "2018",
            "title": "Emerging trends in global freshwater availability",
            "journal": "Nature",
            "vol": "557",
            "issue": "7707",
            "pages": "651–659",
            "doi": "https://doi.org/10.1038/s41586-018-0123-1",
            "type": "journal"
        },
        {
            "authors": "Syed, F.S., Adnan, M., and Gladysheva, M.",
            "year": "2022",
            "title": "The extreme Pakistan flood of 2022: Atmospheric dynamics and severe socioeconomic impacts",
            "journal": "Weather",
            "vol": "77",
            "issue": "12",
            "pages": "410–415",
            "doi": "https://doi.org/10.1002/wea.4312",
            "type": "journal"
        },
        {
            "authors": "Tapley, B.D., Watkins, M.M., Flechtner, F., Reigber, C., Bettadpur, S., Rodell, M., Sasgen, I., Famiglietti, J.S., Landerer, F.W., Chambers, D.P., et al.",
            "year": "2019",
            "title": "Contributions of GRACE to understanding climate change",
            "journal": "Nature Climate Change",
            "vol": "9",
            "issue": "5",
            "pages": "358–369",
            "doi": "https://doi.org/10.1038/s41558-019-0456-2",
            "type": "journal"
        },
        {
            "authors": "Tian, F., Gao, Y., Zhang, L., Wang, Y., and Liu, X.",
            "year": "2023",
            "title": "High-resolution satellite mapping of the 2022 Pakistan mega-flood using Sentinel-1 SAR and Google Earth Engine",
            "journal": "Remote Sensing of Environment",
            "vol": "295",
            "issue": "",
            "pages": "113689",
            "doi": "https://doi.org/10.1016/j.rse.2023.113689",
            "type": "journal"
        },
        {
            "authors": "Willard, J., Jia, X., Xu, S., Steinbach, M., and Kumar, V.",
            "year": "2022",
            "title": "Integrating scientific knowledge with machine learning for engineering and environmental systems",
            "journal": "ACM Computing Surveys",
            "vol": "55",
            "issue": "6",
            "pages": "1–37",
            "doi": "https://doi.org/10.1145/3514228",
            "type": "journal"
        },
        {
            "authors": "World Weather Attribution",
            "year": "2022",
            "title": "Climate change likely increased extreme monsoon rainfall flooding highly vulnerable communities in Pakistan",
            "journal": "World Weather Attribution Scientific Report",
            "vol": "",
            "issue": "",
            "pages": "1–24",
            "doi": "https://doi.org/10.25561/99544",
            "type": "report"
        },
        {
            "authors": "Young, W.J., Anwar, A., Bhatti, T., Borgomeo, E., Davies, S., Garthwaite, R., Gilmont, M., Leb, C., Lytton, L., Makin, I., and Saeed, B.",
            "year": "2019",
            "title": "Pakistan: Getting More from Water",
            "journal": "Water Security Diagnostic Report, World Bank Group, Washington, DC",
            "vol": "",
            "issue": "",
            "pages": "1–180",
            "doi": "https://doi.org/10.1596/31160",
            "type": "report"
        }
    ]

    for ref in refs_data:
        p_r = doc.add_paragraph()
        p_r.paragraph_format.first_line_indent = Inches(-0.25)
        p_r.paragraph_format.left_indent = Inches(0.25)
        p_r.paragraph_format.space_after = Pt(4)
        
        p_r.add_run(f"{ref['authors']} ({ref['year']}) {ref['title']}. ")
        r_j = p_r.add_run(ref['journal'])
        r_j.italic = True
        
        if ref['vol']:
            p_r.add_run(f", ")
            r_v = p_r.add_run(ref['vol'])
            r_v.italic = True
            if ref['issue']:
                p_r.add_run(f"({ref['issue']})")
        if ref['pages']:
            p_r.add_run(f": {ref['pages']}.")
        else:
            p_r.add_run(".")
        if ref['doi']:
            p_r.add_run(f" {ref['doi']}")

    # End of text (Template Page 3)
    p_end = doc.add_paragraph()
    p_end.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_end.paragraph_format.space_before = Pt(14)
    r_end = p_end.add_run("— End of text —")
    r_end.italic = True

    # Enable continuous line numbering across all sections
    add_continuous_line_numbering(doc)

    # Save documents
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    doc.save(output_path)
    print(f"Successfully generated submission-ready Word manuscript: {output_path}")


if __name__ == "__main__":
    # Generate Journal of Hydroinformatics DOCX
    generate_docx(output_path="paper_latex/Research_Article_Journal_of_Hydroinformatics.docx", journal="hydroinformatics")
    # Generate Geosciences Journal DOCX
    generate_docx(output_path="paper_latex/Research_Article_Geosciences_Journal.docx", journal="geosciences")
    # Synchronize default root Research_Article.docx
    generate_docx(output_path="paper_latex/Research_Article.docx", journal="hydroinformatics")
