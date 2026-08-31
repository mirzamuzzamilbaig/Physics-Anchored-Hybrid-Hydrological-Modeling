# Physics-Anchored Hybrid Hydrological Modeling Using Satellite Earth Observation for Monthly Volumetric Flood Risk and Extreme Generalization in the Lower Indus Basin, Pakistan

[![Domain](https://img.shields.io/badge/Domain-Hydrology_%26_Remote_Sensing-green.svg)]()
[![Data](https://img.shields.io/badge/Data-Google_Earth_Engine-blue.svg)](https://earthengine.google.com/)
[![License](https://img.shields.io/badge/License-MIT-brightgreen.svg)](LICENSE)

Official repository for the research paper: **"Physics-Anchored Hybrid Hydrological Modeling Using Satellite Earth Observation for Monthly Volumetric Flood Risk and Extreme Generalization in the Lower Indus Basin, Pakistan"**.

---

## 📌 Author & Institutional Affiliation

**Mirza Muhammad Muzzamil**  
*Department of Computer and Information Systems Engineering (CISE)*  
*NED University of Engineering and Technology, Karachi 75270, Pakistan*  
*Corresponding Author Email:* `mirzamuzzamil@neduet.edu.pk`  
*ORCID iD:* [0000-0001-5258-8959](https://orcid.org/0000-0001-5258-8959)

---

## 📖 Executive Summary

Accurate monthly volumetric streamflow and flood runoff forecasting in heavily managed, low-gradient alluvial river basins remains challenging due to severe hydrometeorological non-stationarity, intensive canal diversions, transboundary upstream inflows, and observational data scarcity.

This repository provides a **Physics-Anchored Water-Balance Hybrid Framework (PG-MCH)** for the Lower Indus Basin within Sindh Province, Pakistan ($140,914 \text{ km}^2$). The model ingests a 25-year multi-decadal satellite Earth observation record from Google Earth Engine (GEE) spanning **2000–2024 ($N=300$ monthly observations)**:
* **CHIRPS v2.0** precipitation ($P$)
* **ERA5-Land** temperature ($T$) and total evaporation ($ET$)
* **NASA SMAP L4 & ERA5** volumetric root-zone soil moisture ($SM$)
* **SRTM 30m DEM** catchment elevation profiles
* **NASA GRACE/GRACE-FO** terrestrial water storage anomalies ($TWSA$)
* **Mainstem Upstream Telemetry** ($Q_{\text{inflow}}$ at Guddu Barrage)

To evaluate genuine out-of-distribution (OOD) extreme generalization over multi-decadal timelines:
* **Calibration Baseline:** 20-year multi-decadal record (**2000–2019**, $N=240$ months).
* **Extreme Holdout:** Unseen catastrophic **2022 Pakistan Mega-Flood** ($+350\%$ monsoon rainfall) and **2020–2022** holdout period.
* **Future Validation:** **2023–2024** non-stationary post-flood recovery.

---

## 📊 Key Experimental Findings

### Benchmark Evaluation (2000–2024, $N=300$)
| Model Architecture | KGE (2022 Mega-Flood) | FHV Peak Bias (2022 Flood) | KGE (2023–2024 Future) | KGE Combined [95% CI] | NSE Combined | RMSE Combined (mm) | FHV Combined |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **PG-MCH (Proposed Hybrid)** | **0.812** | **-4.0%** | **0.871** | **0.895 [0.73, 0.93]** | **0.838** | **11.78** | **-3.1%** |
| TGB-Hydro (GBDT) | 0.750 | -13.3% | 0.895 | 0.857 [0.70, 0.93] | 0.818 | 12.49 | -7.3% |
| RF-Baseline | 0.721 | -7.0% | 0.853 | 0.841 [0.67, 0.91] | 0.783 | 13.61 | -10.5% |
| Conceptual GR4J Baseline | 0.744 | +6.6% | 0.821 | 0.797 [0.67, 0.87] | 0.922 | 8.18 | +9.9% |

### Systematic Multi-Regime Ablation Study
| Ablation Configuration | KGE (2022 Mega-Flood) | FHV (2022 Mega-Flood) | KGE (2020–2024 Combined) | FHV (2020–2024 Combined) |
|---|:---:|:---:|:---:|:---:|
| **Full PG-MCH (Proposed Framework)** | **0.812** | **-4.0%** | **0.895** | **-3.1%** |
| w/o Physical Backbone (Pure ML) | 0.750 | -13.3% | 0.857 | -7.3% |
| w/o Upstream Inflow ($Q_{\text{inflow}}$ Telemetry) | 0.717 | -16.9% | 0.845 | -6.1% |
| w/o Antecedent Memory (No Lagged $API$) | 0.811 | -6.0% | 0.901 | -5.3% |
| w/o Thermal/Evaporative Forcing | 0.814 | -3.1% | 0.898 | -5.1% |

---

## ⚙️ Model Architecture (PG-MCH)

The framework combines physical water-balance constraints with residual non-linear learning across 5 integrated tiers:

$$\hat{Q}(t) = \min\left(P(t) + Q_{\mathrm{inflow}}(t) + API_t, \; \max\left(0, \; \boldsymbol{\beta}^T \mathbf{X}_{\mathrm{base}}(t) + \hat{\varepsilon}(\mathbf{X}(t))\right)\right)$$

1. **Tier 1 (EO Ingestion)**: Multi-decadal satellite grids extracted via Google Earth Engine (2000–2024).
2. **Tier 2 (Feature Engineering)**: Strictly lagged Antecedent Precipitation Index ($API_t = 0.60 P_{t-1} + 0.36 P_{t-2}$, eliminating current-step double-counting) and moisture deficit calculations.
3. **Tier 3A (Physical Linear Backbone)**: Non-Negative L2-Regularized Least Squares (NNLS, $\boldsymbol{\beta} \ge 0$, $\lambda = 2.0$) establishing monotonic water balance $Q_{\text{base}}$.
4. **Tier 3B (Residual ML Correction)**: Tree-depth-capped Gradient Boosted Decision Trees modeling non-linear residual errors $\hat{\varepsilon} = Q_{\text{obs}} - Q_{\text{base}}$.
5. **Tier 4 (Dual Mass-Bounding Operator)**: Strict physical bounding enforcing non-negativity and single-count mass envelope limits.
6. **Tier 5 (Uncertainty Quantification)**: 1,000 resamples using Moving Block Bootstrap (MBB, block size $b=3$ months) to compute non-parametric $95\%$ confidence intervals.

---

## 📁 Repository Structure

```text
.
├── paper_latex/                        # LaTeX manuscript, rebuttal, & 300 DPI figures
│   ├── main.tex                        # Primary LaTeX source
│   ├── Research_Article_Geosciences_Journal.tex # Synchronized journal LaTeX format
│   ├── Research_Article_Geosciences_Journal.docx # Synchronized Word manuscript format
│   ├── Research_Article.docx           # Synchronized root Word document
│   ├── Response_to_Editor_and_Reviewers.md # Comprehensive point-by-point rebuttal
│   ├── references.bib                  # Complete BibTeX bibliography database
│   └── figures/                        # 300 DPI publication figures (PNG)
├── paper_results/                      # Benchmark outputs & tables
│   ├── figures/                        # Generated hydrographs, scatter & ablation charts
│   └── tables/                         # CSV performance metric tables
├── extracted_sindh_data/               # Extracted 2000–2024 GEE EO & telemetry dataset
│   └── sindh_indus_basin_monthly_2000_2024.csv
├── run_rigorous_q1_experiments.py      # Main experimental pipeline & MBB bootstrap
├── run_true_2022_holdout_experiment.py # 2022 Pakistan Mega-Flood OOD holdout test
├── generate_methodology_chart.py       # Architecture diagram generator
├── generate_manuscript_docx.py         # Complete Word manuscript builder
├── plot_sindh_hydro_analytics.py       # Hydro-climatic visual analytics
├── LICENSE                             # MIT License
└── README.md                           # Documentation
```

---

## 🚀 Quickstart & Usage

### 1. Requirements & Dependencies
* Python 3.9+
* `numpy`, `pandas`, `scikit-learn`, `scipy`, `matplotlib`, `seaborn`, `python-docx`

Install dependencies via pip:
```bash
pip install numpy pandas scikit-learn scipy matplotlib seaborn python-docx
```

### 2. Run Multi-Decadal Benchmark Suite & Moving Block Bootstrap UQ
To run full model benchmarking, multi-regime ablation, and 1,000 MBB confidence intervals across 2000–2024:
```bash
python run_rigorous_q1_experiments.py
```

### 3. Run Out-of-Distribution 2022 Mega-Flood Holdout
To execute the zero-shot 2022 Pakistan Mega-Flood evaluation:
```bash
python run_true_2022_holdout_experiment.py
```

### 4. Build Submission-Ready Word Manuscript
To generate the updated, formatted `.docx` manuscript with continuous line numbering:
```bash
python generate_manuscript_docx.py
```

---

## 📜 Citation

If you use this codebase or model architecture in your research, please cite:

```bibtex
@article{muzzamil2026physics,
  title={Physics-Anchored Hybrid Hydrological Modeling Using Satellite Earth Observation for Monthly Volumetric Flood Risk and Extreme Generalization in the Lower Indus Basin, Pakistan},
  author={Muzzamil, Mirza Muhammad},
  journal={Geosciences Journal},
  year={2026},
  publisher={Springer Nature}
}
```

---

## ⚖️ License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
