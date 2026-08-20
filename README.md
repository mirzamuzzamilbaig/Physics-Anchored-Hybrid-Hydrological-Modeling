# Physics-Anchored Hybrid Hydrological Modeling Using Satellite Earth Observation for Monthly Volumetric Flood Risk and Extreme Generalization in the Lower Indus Basin, Pakistan

[![Journal](https://img.shields.io/badge/Journal-Journal_of_Hydroinformatics-003366.svg)](https://iwaponline.com/jh/)
[![Domain](https://img.shields.io/badge/Domain-Hydrology_%26_Remote_Sensing-green.svg)]()
[![Data](https://img.shields.io/badge/Data-Google_Earth_Engine-blue.svg)](https://earthengine.google.com/)
[![License](https://img.shields.io/badge/License-MIT-brightgreen.svg)](LICENSE)

Official repository for the research paper: **"Physics-Anchored Hybrid Hydrological Modeling Using Satellite Earth Observation for Monthly Volumetric Flood Risk and Extreme Generalization in the Lower Indus Basin, Pakistan"**.

---

## 📌 Author & Institutional Affiliation

**Mirza Muhammad Muzzamil**  
*National Center in Big Data and Cloud Computing*  
*Department of Computer and Information Systems Engineering (CISE)*  
*NED University of Engineering and Technology, Karachi 75270, Pakistan*  
*Corresponding Author Email:* `mirzamuzzamil@neduet.edu.pk`

---

## 📖 Executive Summary

Accurate monthly volumetric streamflow and flood runoff forecasting in heavily managed, low-gradient alluvial river basins remains challenging due to severe hydrometeorological non-stationarity, intensive canal diversions, transboundary upstream inflows, and observational data scarcity.

This repository provides a **Physics-Anchored Water-Balance Hybrid Framework (PG-MCH)** for the Lower Indus Basin within Sindh Province, Pakistan ($140,914 \text{ km}^2$). The model ingests multi-sensor satellite Earth observation streams from Google Earth Engine (GEE) across 2020–2024:
* **CHIRPS v2.0** high-resolution precipitation ($P$)
* **ERA5-Land** temperature ($T$) and total evaporation ($ET$)
* **NASA SMAP L4** volumetric soil moisture
* **SRTM 30m DEM** catchment elevation profiles
* **NASA GRACE/GRACE-FO** terrestrial water storage anomalies
* **Mainstem Upstream Telemetry** ($Q_{\text{inflow}}$ at Guddu Barrage)

To evaluate true zero-shot out-of-distribution (OOD) extreme generalization, the model was calibrated exclusively on baseline years (**2020–2021**, $N=24$ months) and stress-tested on the unseen catastrophic **2022 Pakistan Mega-Flood** ($+350\%$ monsoon rainfall) followed by a **2023–2024** non-stationary future test period.

---

## 📊 Key Experimental Findings

| Model Architecture | KGE (2022 Flood Holdout) | FHV Peak Bias (2022 Flood) | KGE (2023–2024 Future) | KGE Combined [95% CI] | NSE Combined |
|---|:---:|:---:|:---:|:---:|:---:|
| **PG-MCH (Proposed Hybrid)** | **0.879** | **-9.4%** | **0.938** | **0.902 [0.86, 0.95]** | **0.990** |
| Conceptual GR4J Baseline | 0.836 | -12.1% | 0.804 | 0.820 [0.70, 0.88] | 0.972 |
| TGB-Hydro (GBDT) | 0.589 | -29.1% | 0.935 | 0.725 [0.56, 0.96] | 0.883 |
| RF Baseline | 0.532 | -30.9% | 0.832 | 0.646 [0.52, 0.88] | 0.834 |

---

## ⚙️ Model Architecture (PG-MCH)

The framework combines physical water-balance constraints with residual non-linear learning across 5 integrated layers:

$$\hat{Q}(t) = \min\left(P_t + Q_{\mathrm{inflow},t} + API_t, \; \max\left(0, \; \boldsymbol{\beta}^T \mathbf{X}_{\mathrm{phys}}(t) + \hat{\varepsilon}(\mathbf{X}(t))\right)\right)$$

1. **Layer 1 (EO Ingestion)**: Multi-sensor satellite grids extracted via Google Earth Engine.
2. **Layer 2 (Feature Engineering)**: Antecedent Precipitation Index ($API_t = P_t + 0.60 P_{t-1} + 0.36 P_{t-2}$) and moisture deficit calculations.
3. **Layer 3A (Physical Linear Backbone)**: Non-Negative L2-Regularized Least Squares (NNLS, $\boldsymbol{\beta} \ge 0$, $\lambda = 2.0$) establishing monotonic water balance $Q_{\text{base}}$.
4. **Layer 3B (Residual ML Correction)**: Tree-depth-capped Gradient Boosted Decision Trees modeling non-linear residual errors $\hat{\varepsilon} = Q_{\text{obs}} - Q_{\text{base}}$.
5. **Layer 4 (Dual Mass-Bounding Operator)**: Strict physical bounding enforcing non-negativity and maximum water input volume limits.
6. **Layer 5 (Uncertainty Quantification)**: 1,000 resamples using Moving Block Bootstrap (MBB, block size $b=3$ months) to compute non-parametric $95\%$ confidence intervals.

---

## 📁 Repository Structure

```text
.
├── paper_latex/                        # Complete LaTeX manuscript & 300 DPI figures
│   ├── main.tex                        # Journal of Hydroinformatics LaTeX source
│   ├── references.bib                  # Complete BibTeX bibliography database
│   └── figures/                        # High-resolution manuscript figures (PNG)
├── paper_results/                      # Benchmark outputs & tables
│   ├── figures/                        # Generated hydrographs, scatter & ablation charts
│   └── tables/                         # CSV performance metric tables (Tables I & II)
├── extracted_sindh_data/               # Extracted GEE EO & telemetry dataset (2020–2024)
│   └── sindh_indus_basin_monthly_2020_2024.csv
├── run_rigorous_q1_experiments.py      # Main experimental pipeline & MBB bootstrap
├── run_true_2022_holdout_experiment.py # 2022 Pakistan Mega-Flood OOD holdout test
├── generate_methodology_chart.py       # Architecture diagram generator (Matplotlib)
├── plot_sindh_hydro_analytics.py       # Hydro-climatic visual analytics
├── LICENSE                             # MIT License
└── README.md                           # Documentation
```

---

## 🚀 Quickstart & Usage

### 1. Requirements & Dependencies
* Python 3.9+
* `numpy`, `pandas`, `scikit-learn`, `scipy`, `matplotlib`, `seaborn`

Install dependencies via pip:
```bash
pip install numpy pandas scikit-learn scipy matplotlib seaborn
```

### 2. Run Out-of-Distribution 2022 Holdout Experiment
To execute the zero-shot 2022 Pakistan Mega-Flood evaluation and regenerate hydrographs:
```bash
python run_true_2022_holdout_experiment.py
```

### 3. Run Benchmark Suite & Moving Block Bootstrap UQ
To run full model benchmarking, multi-regime ablation, and 1,000 MBB confidence intervals:
```bash
python run_rigorous_q1_experiments.py
```

### 4. Compile Manuscript PDF
To compile the LaTeX manuscript locally using Tectonic or PDFLaTeX:
```bash
tectonic paper_latex/main.tex
```

---

## 📜 Citation

If you use this codebase or model architecture in your research, please cite:

```bibtex
@article{muzzamil2026physics,
  title={Physics-Anchored Hybrid Hydrological Modeling Using Satellite Earth Observation for Monthly Volumetric Flood Risk and Extreme Generalization in the Lower Indus Basin, Pakistan},
  author={Muzzamil, Mirza Muhammad},
  journal={Journal of Hydroinformatics},
  year={2026},
  publisher={IWA Publishing / Oxford University Press}
}
```

---

## ⚖️ License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
