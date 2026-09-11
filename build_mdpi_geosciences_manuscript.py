#!/usr/bin/env python3
"""
build_mdpi_geosciences_manuscript.py

Transforms the complete manuscript into the official MDPI Geosciences template (water-template.dot),
strictly adhering to MDPI Guidelines for Authors:
- Exact MDPI styles, typography, headers, line numbering
- Concise 250-word abstract within the 200-300 word requirement
- Consecutive in-text citations for all 7 figures (Figure 1 to 7) and 5 tables (Table 1 to 5)
- Strict sequential in-text numerical ordering of all 36 references ([1] to [36])
- Complete MDPI Back Matter: Supplementary Materials, Author Contributions (CRediT),
  Funding, Institutional Review Board Statement, Informed Consent Statement,
  Data Availability Statement, Acknowledgments, and Conflicts of Interest.
"""

import os
import zipfile
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def prepare_template_docx(dot_path="water-template.dot", template_docx="mdpi_template.docx"):
    """Convert .dot/.dotx template to .docx readable by python-docx by patching [Content_Types].xml."""
    with zipfile.ZipFile(dot_path, 'r') as zin:
        with zipfile.ZipFile(template_docx, 'w') as zout:
            for item in zin.infolist():
                buffer = zin.read(item.filename)
                if item.filename == '[Content_Types].xml':
                    buffer = buffer.replace(b'template.main+xml', b'document.main+xml')
                zout.writestr(item, buffer)
    print(f"Prepared template {template_docx} from {dot_path}")

def set_cell_borders(cell, top="single", bottom="single", left="none", right="none", sz="4", color="auto"):
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:top w:val="{top}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:left w:val="{left}" w:sz="0" w:space="0" w:color="auto"/>'
        f'<w:bottom w:val="{bottom}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:right w:val="{right}" w:sz="0" w:space="0" w:color="auto"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(tcBorders)

def build_geosciences_manuscript():
    prepare_template_docx()
    doc = docx.Document("mdpi_template.docx")

    # Update Header for Geosciences
    for s in doc.sections:
        for p in s.header.paragraphs:
            if "Water" in p.text:
                for r in p.runs:
                    if "Water" in r.text:
                        r.text = r.text.replace("Water", "Geosciences")
                    if "2025" in r.text:
                        r.text = r.text.replace("2025", "2026")
                    if "17" in r.text:
                        r.text = r.text.replace("17", "16")

    # Clear body paragraphs and tables while preserving sectPr
    body = doc._body._element
    to_remove = [child for child in body if child.tag.endswith(('p', 'tbl'))]
    for child in to_remove:
        body.remove(child)

    # 1. Article Type
    doc.add_paragraph("Article", style="MDPI_1.1_article_type")

    # 2. Title
    doc.add_paragraph("Storage- and Regulation-Aware Physics-Guided Learning Reveals Nonlinear Flood Response Thresholds in Regulated River Basins", style="MDPI_1.2_title")

    # 3. Authors
    doc.add_paragraph("Mirza Muhammad Muzzamil *", style="MDPI_1.3_authornames")

    # 4. Affiliations & Correspondence
    doc.add_paragraph("Department of Computer and Information Systems Engineering (CISE), NED University of Engineering and Technology, University Road, Karachi 75270, Sindh, Pakistan; mirzamuzzamil@neduet.edu.pk", style="MDPI_1.6_affiliation")
    doc.add_paragraph("* Correspondence: mirzamuzzamil@neduet.edu.pk; Tel.: +92-21-99261261; ORCID: 0000-0001-5258-8959", style="MDPI_1.6_affiliation")

    # 5. Abstract (Strictly 200-300 words target)
    p_abs = doc.add_paragraph(style="MDPI_1.7_abstract")
    r_abs_lbl = p_abs.add_run("Abstract: ")
    r_abs_lbl.bold = True
    p_abs.add_run(
        "Accurate streamflow simulation and extreme flood risk estimation in heavily regulated alluvial basins are hindered by hydro-climatic non-stationarity, hydraulic diversions, and observational scarcity. While machine learning (ML) architectures capture non-linear hydrological interactions, unconstrained algorithms suffer from severe peak-flow attenuation when exposed to out-of-distribution extremes. In this study, we propose the Storage-Adaptive and Regulation-Aware Physics-Guided Multi-Sensor Catchment Hydrology framework (SA-PG-MCH). SA-PG-MCH tracks a continuous latent catchment water storage state (St) regularized by satellite Earth observations (CHIRPS precipitation, ERA5-Land reanalysis, NASA SMAP soil moisture, NASA GRACE/GRACE-FO gravimetry) and upstream barrage telemetry, while explicitly decoupling anthropogenic canal irrigation and recharge fluxes (Ut). A state-dependent sigmoidal gating mechanism (αt) dynamically shifts weight to a monotonic mass-conservation backbone as catchment storage pressure intensifies. Calibrated on a 20-year baseline (2000–2019, N = 240) and evaluated on an unseen holdout across the catastrophic 2022 Pakistan Mega-Flood (N = 12), SA-PG-MCH achieved KGE = 0.812 and restricted peak underestimation bias (FHV) to -4.0%, whereas unconstrained GBDT collapsed (FHV = -13.3%). Independent cross-climatic validation on the July 2021 Ahr River flash flood in Germany confirmed structural transferability (zero-shot KGE = 0.421; local calibration KGE = 0.607). Response surface analysis reveals that runoff sensitivity surges nonlinearly from 0.12 under dry baseflows to >0.50 during saturated states, while hydraulic regulation expands the critical storage threshold S*(U) = 38.2 + 0.515 Ut mm, providing up to +14.8 mm/month of modeled peak flood buffering. The Flood Amplification Margin (FAMt = St - S*(Ut)) prospectively predicts runoff conversion elasticity (R² = 0.52, p < 0.001), and closed-loop validation against Sentinel-1 SAR flood inundation extent confirms strong temporal agreement (r = 0.94, IoU = 0.79)."
    )

    # 6. Keywords
    p_kw = doc.add_paragraph(style="MDPI_1.8_keywords")
    r_kw_lbl = p_kw.add_run("Keywords: ")
    r_kw_lbl.bold = True
    p_kw.add_run("physics-guided machine learning; storage-adaptive gating; GRACE terrestrial water storage; anthropogenic regulation; response surface; Indus Basin; Sentinel-1 SAR; out-of-distribution extremes")

    # Formatting helpers
    def h1(title):
        return doc.add_paragraph(title, style="MDPI_2.1_heading1")

    def h2(title):
        return doc.add_paragraph(title, style="MDPI_2.2_heading2")

    def h3(title):
        return doc.add_paragraph(title, style="MDPI_2.3_heading3")

    def text(t, indent=True):
        style = "MDPI_3.1_text" if indent else "MDPI_3.2_text_no_indent"
        return doc.add_paragraph(t, style=style)

    def bullet(t):
        return doc.add_paragraph(t, style="MDPI_3.8_bullet")

    def equation(t):
        return doc.add_paragraph(t, style="MDPI_3.9_equation")

    def add_fig(img_path, num, caption_text, width=Inches(6.4)):
        p_img = doc.add_paragraph(style="MDPI_5.2_figure")
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        if os.path.exists(img_path):
            p_img.add_run().add_picture(img_path, width=width)
        else:
            p_img.add_run(f"[Image file not found: {img_path}]")
        
        p_cap = doc.add_paragraph(style="MDPI_5.1_figure_caption")
        r_num = p_cap.add_run(f"Figure {num}. ")
        r_num.bold = True
        p_cap.add_run(caption_text)

    # -------------------------------------------------------------------------
    # 1. Introduction
    # -------------------------------------------------------------------------
    h1("1. Introduction")
    text("The Indus River Basin is one of the most critical and climate-vulnerable transboundary river systems globally, sustaining over 230 million people and supporting the world's largest contiguous irrigation network—the Indus Basin Irrigation System (IBIS) [1,2]. The lower reaches of the basin, situated within Sindh Province, Pakistan, represent an extreme hydraulic and socioeconomic bottleneck. Here, the Indus River flows across flat, low-gradient alluvial plains before discharging into the Arabian Sea via the Indus Delta [3,4].", indent=False)
    text("In recent years, anthropogenic climate change has intensified the magnitude of hydrological extremes across South Asia. In the summer of 2022, unprecedented monsoon rainfall driven by coupled moisture dynamics triggered a devastating \"super-flood\" across Pakistan, with Sindh Province receiving over 350% of its normal 30-year climatological monsoon rainfall [5–7]. Satellite Synthetic Aperture Radar (SAR) imagery confirmed that over one-third of the province was submerged [8], affecting over 33 million people and driving major hydraulic structures (Guddu, Sukkur, and Kotri Barrages, and Manchar Lake) near structural breach thresholds. Conversely, the region regularly experiences pre-monsoon heatwaves, agricultural droughts, and groundwater depletion during the dry winter (Rabi) season [1,9].")

    h2("1.1. Problem Background and Motivation")
    text("Hydrological prediction in heavily managed alluvial basins faces two fundamental methodological limitations:", indent=False)
    bullet("(1) Conceptual models (e.g., GR4J, SAC-SMA): While theoretically mass-conserving, conceptual models rely on static, empirically calibrated parameters that degrade when subjected to unprecedented hydrometeorological shocks [10–12]. Furthermore, ingesting high-dimensional satellite Earth observation grids directly into conceptual structures remains non-trivial.")
    bullet("(2) Standard machine learning (e.g., Random Forest, GBDT, LSTM): Although statistical and deep learning models achieve record-setting accuracy in gauged basins [13–15], unconstrained ML architectures frequently produce unphysical negative runoff states and suffer from severe conditional mean shrinkage. When tested out-of-distribution (OOD), decision tree ensembles and neural networks severely underestimate extreme flood peaks because tree partitions and activation functions cannot extrapolate beyond historic training maxima [16–18]. Surveying physics-informed architectures reveals that embedding explicit mass balance constraints is essential for robust out-of-distribution extrapolation [19].")

    h2("1.2. Research Hypotheses and Core Scientific Contributions")
    text("To resolve these challenges, this study formulates four central hydrological hypotheses:", indent=False)
    bullet("• Hypothesis 1 (H1, Nonlinear Storage Transition): Rainfall-runoff elasticity EP = (∂Q/∂P)(P/Q) increases nonlinearly with antecedent catchment storage (∂EP/∂S > 0), exhibiting a distinct critical saturation threshold (S*).")
    bullet("• Hypothesis 2 (H2, Regulation Threshold Expansion): Anthropogenic canal irrigation withdrawals and groundwater pumping expand the effective catchment storage threshold (∂S*/∂U > 0), buffering flood peaks until super-critical storage is reached.")
    bullet("• Hypothesis 3 (H3, Extreme Rarity Scaling): The peak preservation advantage of state-adaptive physics anchoring expands monotonically with extreme flood rarity (∂ΔFHV/∂T > 0).")
    bullet("• Hypothesis 4 (H4, Dimensionless Structural Transferability): Normalizing critical storage by effective catchment capacity (S*norm(RI) = S*/Scapacity) reveals a transferable dimensionless flood response threshold across contrasting macro-alluvial and steep upland basins.")
    text("In evaluating these hypotheses, this paper provides four primary contributions:", indent=False)
    bullet("(1) State-Adaptive Physics Arbitration: An architecture that dynamically shifts weighting (αt → 1.0) to the mass baseline as storage pressure intensifies, reducing the tendency of tree ensembles to collapse toward historical means.")
    bullet("(2) Storage–Regulation Threshold Discovery: A continuous response law (S*(U) = 38.2 + 0.515 Ut) quantifying critical storage thresholds, supported by independent empirical historical event validation (p < 0.001) and dimensionless cross-basin normalization.")
    bullet("(3) Counterfactual Regulation Decomposition: Attribution of peak flood buffering across irrigation diversion (+10.6 mm/month) and groundwater exchange (+4.2 mm/month) components.")
    bullet("(4) Multi-Domain Extreme Generalization: Robust validation spanning rare-event scaling (T = 2 to 20 yr), cross-basin transfer spectrums (Pakistan → Ahr River), synthetic 1.0x–5.0x stress testing with Monotonic GBDT controls, and independent post-hoc Sentinel-1 SAR flood extent coupling (r = 0.94).")

    # -------------------------------------------------------------------------
    # 2. Materials and Methods
    # -------------------------------------------------------------------------
    h1("2. Materials and Methods")
    
    h2("2.1. Study Area: Lower Indus River Basin (Sindh, Pakistan)")
    text("The Lower Indus Basin within Sindh Province encompasses approximately 140,914 km², bounded by the Kirthar Mountains to the west and the Thar Desert to the east (Figure 1). The hydraulic backbone comprises three major barrage structures: Guddu Barrage (upstream entry), Sukkur Barrage (central diversion hub commanding 3.12 million hectares), and Kotri Barrage (downstream terminal). Runoff generation is governed by upstream snowmelt from the Asian water towers [20], monsoonal depressions, and complex canal abstractions. High-resolution topographic elevation was parameterized using the Shuttle Radar Topography Mission (SRTM 30 m DEM) [21].", indent=False)

    add_fig(
        "paper_latex/figures/Figure_Study_Area_Sindh_Indus.png",
        1,
        "Geographic and hydro-climatic characterization of the Lower Indus River Basin within Sindh Province, Pakistan: (a) Regional administrative boundary, river network, and major barrages (Guddu, Sukkur, Kotri); (b) Topographic elevation from SRTM 30 m DEM; (c) Land use and irrigation distribution; (d) Spatial climatology of mean monsoon precipitation (CHIRPS v2.0)."
    )

    h2("2.2. Multi-Sensor Satellite and Telemetry Datasets")
    text("To reconstruct basin hydrology without relying on unconstrained parameters, we compiled a multi-source Earth observation dataset spanning 2000–2024 at monthly resolution (Table 1). Meteorological precipitation forcing was derived from the Climate Hazards Group InfraRed Precipitation with Stations (CHIRPS v2.0 at 0.05°) [22]. Atmospheric evaporative demand and potential evapotranspiration were acquired from ERA5-Land reanalysis (0.10°) [23]. Surface and root-zone soil moisture (0–100 cm) were extracted from the NASA Soil Moisture Active Passive (SMAP L4) mission [24]. Column-integrated terrestrial water storage anomalies (TWSA) were obtained from NASA GRACE and GRACE Follow-On JPL Mascon RL06 [25]. Surface water inundation extent was mapped from Copernicus Sentinel-1 Synthetic Aperture Radar (SAR C-band) imagery [26]. Observed boundary inflows and discharge telemetry were obtained from the Sindh Irrigation Department.", indent=False)

    # Table 1
    p_t1_cap = doc.add_paragraph(style="MDPI_4.1_table_caption")
    r_t1_num = p_t1_cap.add_run("Table 1. ")
    r_t1_num.bold = True
    p_t1_cap.add_run("Multi-sensor satellite Earth observation and in-situ hydrometric datasets compiled across the Lower Indus Basin (2000–2024).")

    t1 = doc.add_table(rows=7, cols=5)
    t1.alignment = WD_TABLE_ALIGNMENT.CENTER
    t1_hdr = ["Variable / Sensor", "Platform / Source", "Spatial Resolution", "Temporal Coverage", "Hydrological Role"]
    for j, h in enumerate(t1_hdr):
        cell = t1.cell(0, j)
        cell.text = h
        cell.paragraphs[0].style = "MDPI_4.2_table_body"
        cell.paragraphs[0].runs[0].bold = True
        set_cell_borders(cell, top="single", bottom="single", sz="6")

    t1_data = [
        ["Precipitation (P)", "CHIRPS v2.0 (UCSB/CHG)", "0.05° (~5 km)", "2000–2024 (Monthly)", "Meteorological water input forcing"],
        ["Evapotranspiration (ET)", "ERA5-Land (ECMWF)", "0.10° (~10 km)", "2000–2024 (Monthly)", "Atmospheric evaporative demand"],
        ["Root-Zone Soil Moisture (SM)", "NASA SMAP L4 (SPL4SMGP)", "9 km EASE-Grid", "2015–2024 (Extended)", "Infiltration and vadose zone saturation"],
        ["Terrestrial Water Storage (TWSA)", "NASA GRACE/GRACE-FO JPL", "0.50° Mascon RL06", "2002–2024 (Monthly)", "Total column catchment mass constraint"],
        ["Streamflow Telemetry (Qin, Qout)", "Sindh Irrigation Department", "Gauged Barrages", "2000–2024 (Daily/Monthly)", "Boundary inflow and basin discharge"],
        ["Inundation Extent (Aflood)", "Copernicus Sentinel-1 SAR", "10 m (GRD, C-Band)", "2020–2024 (Bi-weekly)", "Post-hoc radar flood extent validation"]
    ]
    for i, row in enumerate(t1_data):
        for j, val in enumerate(row):
            cell = t1.cell(i+1, j)
            cell.text = val
            cell.paragraphs[0].style = "MDPI_4.2_table_body"
            bot = "single" if i == len(t1_data)-1 else "none"
            set_cell_borders(cell, top="none", bottom=bot, sz="6" if bot=="single" else "0")

    h2("2.3. Model Architecture: SA-PG-MCH Framework")
    text("The Storage-Adaptive and Regulation-Aware Physics-Guided Multi-Sensor Catchment Hydrology (SA-PG-MCH) architecture integrates machine learning estimators, such as gradient boosting [27], with a mass-conserving physical backbone through three coupled components:", indent=False)
    bullet("(1) Physical Mass-Conservation Baseline (Qphys,t): Represents dynamic catchment water balance: Qphys,t = max(0, Qin,t + Pt - ETt - ΔSt - Ut), where St is latent storage and Ut represents anthropogenic irrigation diversion and aquifer exchange.")
    bullet("(2) Latent Storage Tracking: State variable St is updated iteratively via: St = St-1 + Pt + Qin,t - ETt - Qobs,t-1 - Ut, constrained by NASA GRACE gravimetry anomalies and SMAP vadose soil moisture.")
    bullet("(3) State-Adaptive Sigmoidal Gating (αt): To eliminate unconstrained tree-leaf shrinkage during rare extremes, αt dynamically shifts weight between physical mass conservation and machine learning: αt = σ(k1 · SPIt + k2 · FAt - k3 · RIt), where SPIt is catchment storage anomaly, FAt is rainfall anomaly, and RIt is regulation intensity.")
    text("The composite streamflow prediction is given by:")
    equation("Qsim,t = αt · Qphys,t + (1 - αt) · QML,t(Xt)")

    # -------------------------------------------------------------------------
    # 3. Results
    # -------------------------------------------------------------------------
    h1("3. Results")
    
    h2("3.1. Benchmark Evaluation and Flood Peak Preservation")
    text("Model performance was evaluated across a 20-year calibration baseline (2000–2019, N = 240) and an unseen out-of-sample holdout (2020–2024, N = 60), benchmarking against Random Forest [28], Deep LSTM networks [29], and conceptual GR2M [30]. Hydrograph accuracy was quantified using the Nash–Sutcliffe Efficiency (NSE) [31], Kling–Gupta Efficiency (KGE) [32], and peak volume bias (FHV) [33]. Statistical differences among models were confirmed via algorithm comparison tests [34] and rank-sum tests [35]. As detailed in Table 2 and illustrated in the scatter comparisons of Figure 2, SA-PG-MCH achieved superior out-of-sample performance (KGE = 0.895, NSE = 0.838).", indent=False)

    add_fig(
        "paper_latex/figures/Figure_2_Model_Benchmarking_Scatter.png",
        2,
        "Scatter plots and 1:1 line comparisons of simulated vs. observed monthly streamflow across competing hydrological models on the Lower Indus Basin benchmark (2020–2024): (a) SA-PG-MCH; (b) Ordinary GBDT; (c) Conceptual GR2M; (d) Deep LSTM Recurrent Network."
    )

    # Table 2
    p_t2_cap = doc.add_paragraph(style="MDPI_4.1_table_caption")
    r_t2_num = p_t2_cap.add_run("Table 2. ")
    r_t2_num.bold = True
    p_t2_cap.add_run("Quantitative performance metrics across the Lower Indus Basin out-of-sample test period (2020–2024, N = 60) and the 2022 Mega-Flood holdout (N = 12).")

    t2 = doc.add_table(rows=6, cols=5)
    t2.alignment = WD_TABLE_ALIGNMENT.CENTER
    t2_hdr = ["Model Architecture", "KGE (2020–2024)", "NSE (2020–2024)", "RMSE (mm)", "FHV (%) [2022 Peak Bias]"]
    for j, h in enumerate(t2_hdr):
        cell = t2.cell(0, j)
        cell.text = h
        cell.paragraphs[0].style = "MDPI_4.2_table_body"
        cell.paragraphs[0].runs[0].bold = True
        set_cell_borders(cell, top="single", bottom="single", sz="6")

    t2_data = [
        ["SA-PG-MCH (Proposed)", "0.895 [0.73, 0.93]", "0.838 [0.68, 0.90]", "11.78", "-4.0% [-8.2, +1.5]"],
        ["Ordinary GBDT", "0.857 [0.66, 0.90]", "0.784 [0.61, 0.86]", "13.61", "-13.3% [-21.4, -6.5]"],
        ["Random Forest", "0.841 [0.63, 0.89]", "0.760 [0.57, 0.84]", "14.34", "-7.0% [-14.1, -1.2]"],
        ["Conceptual GR2M", "0.748 [0.51, 0.82]", "0.682 [0.46, 0.77]", "16.51", "-11.9% [-19.5, -4.2]"],
        ["Deep Sequence LSTM", "0.835 [0.62, 0.88]", "0.751 [0.55, 0.83]", "14.62", "-8.0% [-15.8, -2.1]"]
    ]
    for i, row in enumerate(t2_data):
        for j, val in enumerate(row):
            cell = t2.cell(i+1, j)
            cell.text = val
            cell.paragraphs[0].style = "MDPI_4.2_table_body"
            if i == 0:
                cell.paragraphs[0].runs[0].bold = True
            bot = "single" if i == len(t2_data)-1 else "none"
            set_cell_borders(cell, top="none", bottom=bot, sz="6" if bot=="single" else "0")

    text("The simulated monthly hydrographs and residual time-series across the full 2000–2024 record are depicted in Figure 3. SA-PG-MCH reliably tracks both low baseflows and monsoon flood surges without producing negative flow anomalies or peak attenuation.")

    add_fig(
        "paper_latex/figures/Figure_1_Hydrograph_Comparison_and_Residuals.png",
        3,
        "Multi-model monthly streamflow simulation across the Lower Indus Basin (2000–2024, N = 300). Panel (a) compares observed hydrographs with model predictions across Calibration Baseline (2000–2019, N = 240), Pre-Flood Window (2020–2021, N = 24), 2022 Mega-Flood Holdout (2022, N = 12), and Post-Flood Recovery (2023–2024, N = 24). Panel (b) displays residual errors."
    )

    h2("3.2. Cross-Basin Validation on the Ahr River Flash Flood (Germany)")
    text("To rigorously evaluate cross-climatic transferability under contrasting steep topography and convective flash-flood forcing, the architecture was deployed on the July 2021 catastrophic Ahr River flood in Germany (Table 3 and Figure 4). Under zero-shot direct transfer, SA-PG-MCH achieved KGE = 0.421 and NSE = 0.518, which increased to KGE = 0.607 and NSE = 0.702 under local calibration.", indent=False)

    # Table 3
    p_t3_cap = doc.add_paragraph(style="MDPI_4.1_table_caption")
    r_t3_num = p_t3_cap.add_run("Table 3. ")
    r_t3_num.bold = True
    p_t3_cap.add_run("Cross-basin transferability evaluation on the July 2021 catastrophic Ahr River flash flood in Rhineland-Palatinate, Germany.")

    t3 = doc.add_table(rows=7, cols=5)
    t3.alignment = WD_TABLE_ALIGNMENT.CENTER
    t3_hdr = ["Model Architecture / Strategy", "KGE", "NSE", "RMSE (mm)", "FHV (%) [2021 Peak Bias]"]
    for j, h in enumerate(t3_hdr):
        cell = t3.cell(0, j)
        cell.text = h
        cell.paragraphs[0].style = "MDPI_4.2_table_body"
        cell.paragraphs[0].runs[0].bold = True
        set_cell_borders(cell, top="single", bottom="single", sz="6")

    t3_data = [
        ["SA-PG-MCH (Local Calibration)", "0.607", "0.702", "10.64", "-17.5% [-28.2, -6.0]"],
        ["SA-PG-MCH (12-Mo Few-Shot Adaptation)", "0.548", "0.635", "11.78", "-19.4% [-31.0, -7.5]"],
        ["SA-PG-MCH (Zero-Shot Direct Transfer)", "0.421", "0.518", "13.52", "-24.8% [-38.5, -11.0]"],
        ["Conceptual GR2M (Local Calibration)", "0.582", "0.680", "11.02", "-4.8% [-12.5, +3.2]"],
        ["Ordinary GBDT (Local Calibration)", "0.546", "0.655", "11.45", "-26.2% [-39.0, -13.5]"],
        ["Deep LSTM Network (Local Calibration)", "0.495", "0.625", "11.94", "-10.0% [-22.8, +0.3]"]
    ]
    for i, row in enumerate(t3_data):
        for j, val in enumerate(row):
            cell = t3.cell(i+1, j)
            cell.text = val
            cell.paragraphs[0].style = "MDPI_4.2_table_body"
            if i == 0:
                cell.paragraphs[0].runs[0].bold = True
            bot = "single" if i == len(t3_data)-1 else "none"
            set_cell_borders(cell, top="none", bottom=bot, sz="6" if bot=="single" else "0")

    add_fig(
        "paper_latex/figures/Figure_Ahr_2021_Hydrograph_Comparison.png",
        4,
        "Cross-basin external validation on the July 2021 Ahr River flash flood in Rhineland-Palatinate, Germany under severe convective storm forcing, comparing Zero-Shot, Few-Shot, and Local Calibration trajectories."
    )

    text("Calibrated uncertainty estimates for the Indus Basin simulation are illustrated in Figure 5, displaying heteroscedastic 95% confidence intervals that widen realistically during the 2022 Mega-Flood peak.")

    add_fig(
        "paper_latex/figures/Figure_SA_PG_MCH_Hydrograph_Intervals.png",
        5,
        "SA-PG-MCH out-of-sample simulation across the Lower Indus Basin (2020–2024) featuring heteroscedastic 95% calibrated prediction intervals and highlighting the 2022 Mega-Flood holdout."
    )

    h2("3.3. Stepwise Ablation Insights")
    text("Systematic ablation experiments demonstrate the quantitative necessity of each architectural component in SA-PG-MCH (Table 4). Freezing gating at a static balance (α = 0.5) degrades 2022 flood KGE to 0.744 and causes peak overestimation (+4.2%), while removing the physical backbone worsens peak underestimation to -13.3%.", indent=False)

    # Table 4
    p_t4_cap = doc.add_paragraph(style="MDPI_4.1_table_caption")
    r_t4_num = p_t4_cap.add_run("Table 4. ")
    r_t4_num.bold = True
    p_t4_cap.add_run("Stepwise novelty ablation study for the SA-PG-MCH framework across calibration and out-of-sample evaluation periods.")

    t4 = doc.add_table(rows=7, cols=5)
    t4.alignment = WD_TABLE_ALIGNMENT.CENTER
    t4_hdr = ["Ablation Configuration", "KGE (2022 Flood)", "FHV (2022 Flood)", "KGE (2020–2024)", "FHV (2020–2024)"]
    for j, h in enumerate(t4_hdr):
        cell = t4.cell(0, j)
        cell.text = h
        cell.paragraphs[0].style = "MDPI_4.2_table_body"
        cell.paragraphs[0].runs[0].bold = True
        set_cell_borders(cell, top="single", bottom="single", sz="6")

    t4_data = [
        ["Full SA-PG-MCH (Proposed)", "0.812", "-4.0%", "0.895", "-3.1%"],
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
            cell.paragraphs[0].style = "MDPI_4.2_table_body"
            if i == 0:
                cell.paragraphs[0].runs[0].bold = True
            bot = "single" if i == len(t4_data)-1 else "none"
            set_cell_borders(cell, top="none", bottom=bot, sz="6" if bot=="single" else "0")

    h2("3.4. Storage-Regulation Response Surface and Critical Threshold Law S*(U)")
    text("Response surface mapping confirms that runoff sensitivity surges nonlinearly from 0.12 under dry baseflows to >0.50 during saturated states (Figure 6). Defining the critical threshold as S*(U) = {S | EP(S, U) ≥ 0.50}, non-parametric bootstrap regression [36] establishes: S*(U) = 38.2 [35.6, 40.8] + 0.515 [0.442, 0.588] Ut (mm). Human regulation expands retention capacity from 38.2 mm to 51.1 mm (U = 25 mm/month), providing up to +14.8 mm/month of flood buffering during the August 2022 Mega-Flood.", indent=False)

    add_fig(
        "paper_latex/figures/Figure_Storage_Regulation_Response_Surface.png",
        6,
        "Storage-Regulation Runoff Response and Threshold Law: (a) 2D Flood Amplification Diagram mapping rainfall elasticity EP across storage anomaly SPIt and regulation intensity RI = Ut / (Pt + Qin,t), with critical threshold Ecrit = 0.50; (b) Continuous critical storage threshold law S*(U) = 38.2 + 0.515 Ut separating sub-critical absorbing from super-critical rapid amplification regimes; (c) 4-stage counterfactual regulation decomposition for the August 2022 Mega-Flood (C0: Factual, C1: No Irrigation, C2: No Groundwater, C3: Naturalized)."
    )

    text("Synthetic out-of-distribution stress tests under single-variable and compound hydro-climatic shock patterns are reported in Table 5, demonstrating that standard GBDT collapses to flat horizontal predictions, whereas SA-PG-MCH preserves physically consistent volumetric scaling.")

    # Table 5
    p_t5_cap = doc.add_paragraph(style="MDPI_4.1_table_caption")
    r_t5_num = p_t5_cap.add_run("Table 5. ")
    r_t5_num.bold = True
    p_t5_cap.add_run("Synthetic out-of-distribution extrapolation stress test comparing Ordinary GBDT, Monotonic GBDT, and SA-PG-MCH across single-variable and compound hydro-climatic shock patterns.")

    t5 = doc.add_table(rows=6, cols=7)
    t5.alignment = WD_TABLE_ALIGNMENT.CENTER
    t5_hdr = ["Synthetic Stress Pattern", "P (mm)", "Qin (mm)", "Cap W (mm)", "Ord. GBDT", "Mono. GBDT", "SA-PG-MCH"]
    for j, h in enumerate(t5_hdr):
        cell = t5.cell(0, j)
        cell.text = h
        cell.paragraphs[0].style = "MDPI_4.2_table_body"
        cell.paragraphs[0].runs[0].bold = True
        set_cell_borders(cell, top="single", bottom="single", sz="6")

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
            cell.paragraphs[0].style = "MDPI_4.2_table_body"
            if i == 0 or j == 6:
                cell.paragraphs[0].runs[0].bold = True
            bot = "single" if i == len(t5_data)-1 else "none"
            set_cell_borders(cell, top="none", bottom=bot, sz="6" if bot=="single" else "0")

    text("Figure 7 synthesizes extreme rarity scaling, cross-basin transferability, and closed-loop validation against Sentinel-1 SAR flood extent observations (r = 0.94, R² = 0.88, IoU = 0.79).")

    add_fig(
        "paper_latex/figures/Figure_Sentinel1_Flood_Inundation_Validation.png",
        7,
        "Rare-event scaling, transferability spectrum, and independent Sentinel-1 validation: (a) Peak volume bias |FHV| across return periods T = 2 to 20 years, showing expanding physics-anchoring advantage; (b) Cross-basin transferability spectrum from Pakistan to Ahr River (Zero-Shot → Few-Shot → Local Calibration); (c) Independent post-hoc Sentinel-1 SAR inundation extent validation (r = 0.94, R² = 0.88, IoU = 0.79); (d) Static (α = 0.50, α = c* = 0.62) vs. dynamic state-adaptive (αt) physics gating benchmark."
    )

    # -------------------------------------------------------------------------
    # 4. Discussion
    # -------------------------------------------------------------------------
    h1("4. Discussion")
    
    h2("4.1. Physical Interpretation of Dynamic Gating")
    text("The central innovation of SA-PG-MCH is state-adaptive arbitration (αt). During normal baseflow and moderate monsoon seasons, data-driven gradient boosting accounts for intricate localized interactions, agricultural demands, and non-linear evapotranspiration losses. However, during unprecedented monsoonal deluges, catchment storage reaches saturation (FAMt ≥ 0), and αt asymptotically shifts weighting toward the physical mass backbone (αt → 1.0). This prevents decision-tree leaf cuts from artificially flattening out-of-distribution extremes, resolving the severe peak flow attenuation characteristic of standard machine learning.", indent=False)

    h2("4.2. Role of Multi-Sensor Satellite Earth Observations")
    text("Incorporating NASA GRACE/GRACE-FO TWSA provides an essential decadal mass anchor that prevents cumulative storage drift in long-term simulations. NASA SMAP root-zone soil moisture captures high-frequency antecedent infiltration dynamics, ensuring that dry-to-wet seasonal transitions are accurately resolved prior to peak monsoon arrivals. Coupling simulated discharge with Copernicus Sentinel-1 SAR flood inundation extent (r = 0.94, R² = 0.88, IoU = 0.79) independently confirms that the modeled streamflow dynamics translate into real terrestrial flood extents across the Sindh floodplain.")

    h2("4.3. Limitations and Future Work")
    text("Several operational limitations must be noted: (1) The monthly timestep is tailored for strategic regional water allocation and seasonal reservoir operations, but hourly models are required for sub-daily flash flood forecasting in ephemeral western hill torrents (Kirthar Range); (2) Catchment arealization was defined using provincial administrative boundaries to directly interface with flood emergency agencies. Future work will couple SA-PG-MCH directly with 2D hydrodynamic inundation engines (e.g., LISFLOOD-FP, HEC-RAS 2D) and global benchmark catchments (CAMELS).")

    # -------------------------------------------------------------------------
    # 5. Conclusions
    # -------------------------------------------------------------------------
    h1("5. Conclusions")
    text("This study introduced the Storage-Adaptive and Regulation-Aware Physics-Guided Multi-Sensor Catchment Hydrology (SA-PG-MCH) framework, designed for flood modeling in heavily managed, data-scarce alluvial river basins. Evaluated across a 25-year record (2000–2024) in the Lower Indus Basin and externally validated on the 2021 Ahr River flash flood in Germany, the principal findings are:", indent=False)
    bullet("1. Elimination of Extreme Peak Underestimation: By dynamically shifting weight to the physical mass baseline during saturated states, SA-PG-MCH restricted peak flow underestimation to -4.0% during the 2022 Pakistan Mega-Flood, compared to -13.3% for unconstrained GBDT and -11.9% for conceptual GR2M.")
    bullet("2. Storage–Regulation Threshold Discovery: Non-parametric bootstrap regression derived the continuous threshold law S*(U) = 38.2 + 0.515 Ut mm. Anthropogenic irrigation diversions expand this threshold by up to +12.9 mm, providing up to 14.8 mm/month of flood buffering.")
    bullet("3. Flood Amplification Margin Diagnostic: FAMt = St - S*(Ut) provides a continuous indicator that prospectively predicts observed monsoon runoff elasticity (R² = 0.52, p < 0.001).")
    bullet("4. Satellite Radar Coupling: Closed-loop validation against Sentinel-1 SAR flood extents achieved strong temporal agreement (r = 0.94, IoU = 0.79).")

    # -------------------------------------------------------------------------
    # Back Matter (Mandatory MDPI Headings)
    # -------------------------------------------------------------------------
    p_sup = doc.add_paragraph(style="MDPI_6.2_back_matter")
    r_sup_lbl = p_sup.add_run("Supplementary Materials: ")
    r_sup_lbl.bold = True
    p_sup.add_run("The following supporting information can be downloaded from the project code repository: Table S1: GBDT hyperparameters and tuning grids; Table S2: Cross-basin soil hydraulic parameters; Code S1: Python implementation of the SA-PG-MCH architecture.")

    p_ac = doc.add_paragraph(style="MDPI_6.2_back_matter")
    r_ac_lbl = p_ac.add_run("Author Contributions: ")
    r_ac_lbl.bold = True
    p_ac.add_run("Conceptualization, M.M.M.; methodology, M.M.M.; software, M.M.M.; validation, M.M.M.; formal analysis, M.M.M.; investigation, M.M.M.; resources, M.M.M.; data curation, M.M.M.; writing—original draft preparation, M.M.M.; writing—review and editing, M.M.M.; visualization, M.M.M.; project administration, M.M.M. The author has read and agreed to the published version of the manuscript.")

    p_fund = doc.add_paragraph(style="MDPI_6.2_back_matter")
    r_fund_lbl = p_fund.add_run("Funding: ")
    r_fund_lbl.bold = True
    p_fund.add_run("This research received no external funding.")

    p_irb = doc.add_paragraph(style="MDPI_6.2_back_matter")
    r_irb_lbl = p_irb.add_run("Institutional Review Board Statement: ")
    r_irb_lbl.bold = True
    p_irb.add_run("Not applicable.")

    p_ic = doc.add_paragraph(style="MDPI_6.2_back_matter")
    r_ic_lbl = p_ic.add_run("Informed Consent Statement: ")
    r_ic_lbl.bold = True
    p_ic.add_run("Not applicable.")

    p_da = doc.add_paragraph(style="MDPI_6.2_back_matter")
    r_da_lbl = p_da.add_run("Data Availability Statement: ")
    r_da_lbl.bold = True
    p_da.add_run("Publicly available hydrometeorological and satellite Earth observation datasets analyzed in this study are available from their respective repositories: NASA GRACE/GRACE-FO TWSA from JPL Mascon RL06 (https://grace.jpl.nasa.gov/), NASA SMAP L3/L4 from NSIDC (https://nsidc.org/data/smap), CHIRPS v2.0 from UCSB CHC (https://www.chc.ucsb.edu/data/chirps), ERA5-Land reanalysis from ECMWF/Copernicus Climate Data Store (https://cds.climate.copernicus.eu/), and Copernicus Sentinel-1 SAR imagery from the Copernicus Data Space Ecosystem (https://dataspace.copernicus.eu/). Hydrometric Indus Basin discharge and canal diversion records were obtained from the Sindh Irrigation Department and Pakistan Indus River System Authority (IRSA). All processing scripts and trained model checkpoints are available at https://github.com/mirzamuzzamilbaig/Physics-Anchored-Hybrid-Hydrological-Modeling.")

    p_ack = doc.add_paragraph(style="MDPI_6.2_back_matter")
    r_ack_lbl = p_ack.add_run("Acknowledgments: ")
    r_ack_lbl.bold = True
    p_ack.add_run("The author expresses gratitude to the Sindh Irrigation Department and Federal Flood Commission (FFC) for providing barrage telemetry data under academic research protocols. The author also acknowledges the Google Earth Engine team, ECMWF, CHG UCSB, and NASA for providing open-access planetary-scale Earth observation datasets.")

    p_coi = doc.add_paragraph(style="MDPI_6.2_back_matter")
    r_coi_lbl = p_coi.add_run("Conflicts of Interest: ")
    r_coi_lbl.bold = True
    p_coi.add_run("The author declares no conflicts of interest.")

    # -------------------------------------------------------------------------
    # References (Strictly in order of appearance in text: [1] to [36])
    # -------------------------------------------------------------------------
    h1("References")

    refs = [
        "Biemans, H.; Siderius, C.; Mishra, V.; Ahmad, B. Future water resources for food production in Five South Asian River Basins and potential for adaptation. Hydrol. Earth Syst. Sci. 2016, 20, 3711–3731. https://doi.org/10.5194/hess-20-3711-2016.",
        "Young, W.J.; Anwar, A.H.M.F.; Bhatti, T.; Borgomeo, E.; Davies, S.; Garthwaite, W.R.; Gilmont, M.; Leb, C.; Lytton, L.; Makin, I.; et al. Pakistan: Getting More from Water; World Bank: Washington, DC, USA, 2019; pp. 1–180. https://doi.org/10.1596/31160.",
        "Hashmi, H.N.; Shakir, A.S.; Tariq, M.A.U.R. Water management issues in the Indus Basin of Pakistan. Water Policy 2022, 24, 185–204.",
        "Inam, A.; Clift, P.D.; Giosan, L.; Tabrez, A.R.; Tahir, M.; Rabbani, M.M.; Danish, M. The geographic, geological and oceanographic setting of the Indus River. In Large Asian Rivers; Gupta, A., Ed.; John Wiley & Sons: Hoboken, NJ, USA, 2007; pp. 333–345.",
        "Syed, F.S.; Adnan, M.; Dilshad, M.H.; Rasul, G. The extraordinary 2022 monsoon flood in Pakistan: Hydro-meteorological perspective. Atmosphere 2022, 13, 1759.",
        "Nanditha, J.S.; Kushwaha, A.P.; Singh, R.; Malik, I.; Solanki, V.; Chuphal, D.S.; Dangar, S.; Mahto, S.S.; Vegad, U.; Mishra, V. The 2022 Pakistan flood: Articulating the role of climate change, heatwaves, and antecedent soil moisture. Earth's Future 2023, 11, e2022EF003019.",
        "World Weather Attribution. Climate Change Likely Increased Extreme Monsoon Rainfall Flooding Highly Vulnerable Communities in Pakistan; Imperial College London: London, UK, 2022.",
        "Tian, F.; Liu, L.; Zhang, K.; Lu, Y.; Hou, X. Satellite-based monitoring and damage assessment of the 2022 severe flood in Pakistan using multi-source remote sensing data. Remote Sens. 2023, 15, 1420.",
        "Rodell, M.; Famiglietti, J.S.; Wiese, D.N.; Reager, J.T.; Beaudoing, H.K.; Landerer, F.W.; Lo, M.H. Emerging trends in global freshwater availability. Nature 2018, 557, 651–659.",
        "Perrin, C.; Michel, C.; Andréassian, V. Improvement of a parsimonious model for streamflow simulation. J. Hydrol. 2003, 279, 275–289.",
        "Gupta, H.V.; Kling, H.; Yilmaz, K.K.; Martinez, G.F. Decomposition of the mean squared error and NSE performance criteria: Implications for improving hydrological modelling. J. Hydrol. 2009, 377, 80–91.",
        "Frame, J.M.; Kratzert, F.; Raney, A.; Rahman, M.; Salas, F.R.; Nearing, G.S. Post-processing the US National Water Model with a Long Short-Term Memory network. J. Am. Water Resour. Assoc. 2022, 58, 775–788.",
        "Kratzert, F.; Klotz, D.; Brenner, C.; Schulz, K.; Herrnegger, M. Rainfall–runoff modelling using Long Short-Term Memory (LSTM) networks. Hydrol. Earth Syst. Sci. 2018, 22, 6005–6022.",
        "Kratzert, F.; Klotz, D.; Shalev, G.; Klambauer, G.; Hochreiter, S.; Nearing, G. Towards learning universal, regional, and local hydrological behaviors via machine learning applied to large-sample datasets. Hydrol. Earth Syst. Sci. 2019, 23, 5083–5097.",
        "Nearing, G.; Cohen, D.; Dakhari, V.; Gauch, M.; Gilon, O.; Harrigan, S.; Hassidim, A.; Klotz, D.; Kratzert, F.; Metzger, A.; et al. Global prediction of extreme floods in ungauged watersheds. Nature 2024, 627, 559–563.",
        "Karpatne, A.; Atluri, G.; Faghmous, J.H.; Steinbach, M.; Banerjee, A.; Ganguly, A.; Shekhar, S.; Samatova, N.; Kumar, V. Theory-guided data science: A new paradigm for scientific discovery from data. IEEE Trans. Knowl. Data Eng. 2017, 29, 2318–2331.",
        "Read, J.S.; Jia, X.; Willard, J.; Manson, A.P.; Zwart, J.A.; Best, C.D.; Anderson, S.; Ward, N.K.; Hamilton, D.P.; Kumar, V. Process-guided deep learning predictions of lake water temperature. Water Resour. Res. 2019, 55, 9173–9190.",
        "Jia, X.; Willard, J.; Karpatne, A.; Read, J.S.; Zwart, J.A.; Steinbach, M.; Kumar, V. Physics-guided machine learning for scientific discovery: An application in simulating lake water temperature. ACM Trans. Data Sci. 2021, 2, 1–26.",
        "Willard, J.; Jia, X.; Xu, S.; Steinbach, M.; Kumar, V. Integrating physics-based modeling with machine learning: A survey on physics-informed machine learning. ACM Comput. Surv. 2022, 55, 1–37.",
        "Immerzeel, W.W.; Lutz, A.F.; Andrade, M.; Bahl, A.; Biemans, H.; Bolch, T.; Carpentier, S.; de Kok, E.; Hazemi, S.; Immerzeel, P.J.; et al. Importance and vulnerability of the world's water towers. Nature 2020, 577, 364–369.",
        "Farr, T.G.; Rosen, P.A.; Caro, E.; Crippen, R.; Duren, R.; Hensley, S.; Kobrick, M.; Paller, M.; Rodriguez, E.; Roth, L.; et al. The Shuttle Radar Topography Mission. Rev. Geophys. 2007, 45, RG2004.",
        "Funk, C.; Peterson, P.; Landsfeld, M.; Pedreros, D.; Verdin, J.; Shukla, S.; Husak, G.; Rowland, J.; Harrison, L.; Hoell, A.; et al. The climate hazards group infrared precipitation with stations—a new environmental record for monitoring extremes. Sci. Data 2015, 2, 150066.",
        "Muñoz-Sabater, J.; Dutra, E.; Agustí-Panareda, A.; Albergel, C.; Arduini, G.; Balsamo, G.; Boussetta, S.; Choulga, M.; Harrigan, S.; Hersbach, H.; et al. ERA5-Land: A state-of-the-art global reanalysis dataset for land applications. Earth Syst. Sci. Data 2021, 13, 4349–4383.",
        "Entekhabi, D.; Njoku, E.G.; O'Neill, P.E.; Kellogg, K.H.; Crow, W.T.; Edelstein, W.N.; Entin, J.K.; Goodman, S.D.; Jackson, T.J.; Johnson, J.; et al. The Soil Moisture Active Passive (SMAP) mission. Proc. IEEE 2010, 98, 704–716.",
        "Landerer, F.W.; Flechtner, F.M.; Save, H.; Webb, F.H.; Bandikova, T.; Bertiger, W.I.; Bettadpur, S.V.; Byun, S.H.; Dahle, C.; Dobslaw, H.; et al. Extending the global mass change data record: GRACE Follow-On instrument and science data performance. Geophys. Res. Lett. 2020, 47, e2020GL088306.",
        "Torres, R.; Snoeij, P.; Geudtner, D.; Bibby, D.; Davidson, M.; Attema, E.; Potin, P.; Rommen, B.; Floury, N.; Brown, M.; et al. GMES Sentinel-1 mission. Remote Sens. Environ. 2012, 120, 9–24.",
        "Friedman, J.H. Greedy function approximation: A gradient boosting machine. Ann. Stat. 2001, 29, 1189–1232.",
        "Breiman, L. Random forests. Mach. Learn. 2001, 45, 5–32.",
        "Hochreiter, S.; Schmidhuber, J. Long short-term memory. Neural Comput. 1997, 9, 1735–1780.",
        "Mouelhi, S.; Michel, C.; Perrin, C.; Andréassian, V. Stepwise development of a two-parameter monthly water balance model. J. Hydrol. 2006, 318, 200–214.",
        "Nash, J.E.; Sutcliffe, J.V. River flow forecasting through conceptual models part I—A discussion of principles. J. Hydrol. 1970, 10, 282–290.",
        "Kling, H.; Fuchs, M.; Paulin, M. Runoff conditions in the upper Danube basin under an ensemble of climate change scenarios. J. Hydrol. 2012, 424, 264–277.",
        "Yilmaz, K.K.; Gupta, H.V.; Wagener, T. A process-based diagnostic approach to model evaluation: Application to the NWS distributed hydrologic model. Water Resour. Res. 2008, 44, W09417.",
        "Dietterich, T.G. Approximate statistical tests for comparing supervised classification learning algorithms. Neural Comput. 1998, 10, 1895–1923.",
        "Kruskal, W.H.; Wallis, W.A. Use of ranks in one-criterion variance analysis. J. Am. Stat. Assoc. 1952, 47, 583–621.",
        "Efron, B.; Tibshirani, R.J. An Introduction to the Bootstrap; Chapman and Hall/CRC: New York, NY, USA, 1994."
    ]

    for i, ref in enumerate(refs):
        p_ref = doc.add_paragraph(style="MDPI_8.1_references")
        r_num = p_ref.add_run(f"{i+1}. ")
        p_ref.add_run(ref)

    # Save output manuscripts
    out_paths = [
        "paper_latex/Research_Article_Geosciences_Journal.docx",
        "Research_Article_MDPI_Geosciences.docx"
    ]
    for p in out_paths:
        os.makedirs(os.path.dirname(p) if os.path.dirname(p) else ".", exist_ok=True)
        doc.save(p)
        print(f"Successfully generated official MDPI Geosciences manuscript: {p}")

if __name__ == "__main__":
    build_geosciences_manuscript()
