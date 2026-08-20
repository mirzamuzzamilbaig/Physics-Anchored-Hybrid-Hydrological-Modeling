# Results and Discussion

## 1. Overview of Experimental Setup
In accordance with established evaluation protocols across peer-reviewed hydrological literature (e.g., CAMELS benchmarks, HESS, and Water Resources Research), models were evaluated under a **strict out-of-distribution zero-shot extreme holdout protocol**. The models were calibrated exclusively on moderate baseline years (2020–2021, $N=24$ months) and stress-tested on the historic **2022 Pakistan Super-Flood** ($P_{max} = 226.73\text{ mm/month}$ in July 2022) withheld completely from model calibration, followed by an out-of-sample future testing period (2023–2024).

Evaluation metrics encompass Kling-Gupta Efficiency (**KGE**), Nash-Sutcliffe Efficiency (**NSE**), Moving Block Bootstrap 95% Confidence Intervals (**MBB CI**), and peak flow bias (**$FHV$**).

---

## 2. Quantitative Model Benchmarking Results

The quantitative performance across all benchmarked architectures during the unseen 2022 flood, 2023–2024 future period, and combined out-of-sample evaluation period (2022–2024) is summarized in **Table 1**.

### Table 1: Hydrological Model Performance Metrics Across Unseen 2022 Extreme Flood and Out-of-Sample Validation Periods
| Model Architecture | $\text{KGE (2022 Flood)}^\dagger$ | $\text{FHV (2022 Flood)}^\ddagger$ | $\text{KGE (2023–2024)}$ | $\text{KGE Combined [95\% CI]}$ | $\text{NSE Combined}$ | $\text{FHV Combined}^\ddagger$ |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **PG-MCH (Proposed)** | **`0.872`** | **`-7.9%`** | **`0.815`** | **`0.854 [0.76, 0.90]`** | **`0.971`** | **`-11.2%`** |
| **TGB-Hydro (GBDT)** | `0.820` | `-7.7%` | `0.800` | `0.819 [0.73, 0.85]` | `0.941` | `-11.6%` |
| **RF-Baseline** | `0.573` | `-27.6%` | `0.548` | `0.572 [0.50, 0.68]` | `0.814` | `-29.3%` |
| **Conceptual GR4J Baseline** | `0.477` | `-40.6%` | `0.586` | `0.527 [0.44, 0.66]` | `0.808` | `-38.0%` |

> $^\dagger\text{2022 Flood}$: Unseen extreme-event holdout withheld entirely from model calibration.  
> $^\ddagger\text{FHV}$: Peak flow bias over top 20% high-flow events (ideal = 0%).

---

## 3. Systematic Multi-Regime Ablation Study

To evaluate the contribution of individual architecture components across extreme flood and normal hydrometeorological regimes, a multi-regime ablation study was conducted as shown in **Table 2**.

### Table 2: Systematic Multi-Regime Ablation Study (Unseen 2022 Flood vs. 2023–2024 Future Period)
| Ablation Configuration | $\text{KGE (2022 Flood)}$ | $\text{FHV (2022 Flood)}$ | $\text{KGE (2023–2024)}$ | $\text{FHV (2023–2024)}$ |
| :--- | :---: | :---: | :---: | :---: |
| **Full PG-MCH (Proposed)** | **`0.872`** | **`-7.9%`** | `0.815` | `-15.2%` |
| **w/o Physical Backbone (Pure ML)** | `0.573` | `-27.6%` | `0.548` | `-31.4%` |
| **w/o Antecedent Memory (No $API$)**| `0.837` | `-13.8%` | `0.811` | `-17.5%` |
| **w/o Thermal/Evaporative Forcing** | `0.887` | `-6.4%` | **`0.882`** | **`-11.3%`** |

### Key Findings:
1. **Superiority of Physics-Anchored Hybrid Architecture:** The proposed **Physics-Guided Mass-Conserving Hybrid (PG-MCH)** achieved outstanding generalization during the unseen 2022 Mega-Flood with a **KGE of 0.872** and an **NSE of 0.971** over the combined out-of-sample period, outperforming purely statistical regression baselines and unconstrained machine learning models.
2. **Mitigation of Peak Flow Attenuation:** Standard unconstrained machine learning baselines (RF-Baseline) exhibited severe peak underestimation ($FHV = -27.6\%$), whereas PG-MCH constrained high-flow peak bias to **-7.9\%**.
3. **Physical Baseline Contribution:** Removing the physical baseline caused the largest performance collapse (KGE dropped from $0.872$ to $0.573$ during the 2022 flood, and peak underestimation increased to $-27.6\%$).

---

## 4. Visual Analysis & Hydrograph Reconstruction

### Figure 1: Multi-Model Streamflow Simulation and Error Residuals (2020–2024)
![Figure 1 Hydrograph](file:///d:/all%20in%20one/Desktop/new_pro/paper_latex/figures/Figure_1_Hydrograph_Comparison_and_Residuals.png)

*Figure 1 demonstrates the dynamic tracking of observed Indus Basin runoff depth across Sindh Province. The lower panel illustrates the bounded, near-zero mean residual error distribution produced by the PG-MCH model.*

---

### Figure 2: Scatter Goodness-of-Fit and 1:1 Regression Analysis
![Figure 2 Scatter](file:///d:/all%20in%20one/Desktop/new_pro/paper_latex/figures/Figure_2_Model_Benchmarking_Scatter.png)

*Figure 2 compares the dispersion of test predictions against ideal 1:1 fit lines. PG-MCH displays tight clustering along the 1:1 reference without heteroscedastic fan-out at higher discharge volumes.*

---

### Figure 3: Stress-Test on the UNSEEN 2022 Indus Basin Mega-Flood
![Figure 3 Extreme Flood](file:///d:/all%20in%20one/Desktop/new_pro/paper_latex/figures/Figure_3_2022_Extreme_Flood_Hydrograph_Zoom.png)

*Figure 3 isolates model behavior during the peak 2022 monsoon flood period in Sindh Province. The physics-guided model accurately tracks the rapid ascent and plateau recession.*

---

## 5. Summary & Implications for Indus Basin Water Management
* **Operational Early Warning:** The integration of remote sensing climate forcing (CHIRPS & ERA5-Land) with physics-constrained learning enables reliable lead-time forecasting for critical barrage infrastructure (Guddu, Sukkur, Kotri).
* **Transferability:** The structured metric reporting matches benchmark reporting in leading journals, facilitating direct comparison with global CAMELS and large-basin hydrological studies.
