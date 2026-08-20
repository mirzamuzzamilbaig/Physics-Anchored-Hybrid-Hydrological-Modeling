# Physics-Anchored Hybrid Hydrological Modeling Using Satellite Earth Observation for Extreme Flood Generalization in the Lower Indus Basin, Pakistan

**Mirza Muhammad Muzammil**  
*Department of Environmental and Water Resources Engineering*  
*Indus Basin Hydro-Informatics & Earth Observation Research Initiative*  

---

## Abstract
Accurate streamflow and flood runoff forecasting in heavily managed, low-gradient river basins remains challenging due to severe hydrometeorological non-stationarity, intensive canal diversions, and observational data scarcity. While purely data-driven machine learning algorithms capture complex non-linear patterns, they frequently suffer from physical inconsistency, variance dampening, and severe peak flow underestimation when tested on unprecedented extreme floods. Conversely, traditional conceptual models struggle to ingest multi-source satellite Earth observation grids directly. In this study, we investigate how coupling a linear water-balance-informed baseline with non-linear residual machine learning mitigates peak flow attenuation while preserving generalization under extreme climate forcing. 

We develop a **Physics-Anchored Water-Balance Hybrid** framework for the Lower Indus Basin within Sindh Province, Pakistan ($140,914\text{ km}^2$), ingesting multi-sensor Google Earth Engine (GEE) streams across 2020–2024 (CHIRPS v2.0 precipitation, ERA5-Land reanalysis, NASA SMAP soil moisture, SRTM topography, and GRACE storage anomalies). To evaluate true out-of-distribution extreme-event generalization, the model was calibrated exclusively on baseline years (2020–2021) and stress-tested on the **completely unseen 2022 Pakistan Mega-Flood** as an independent extreme holdout, followed by a 2023–2024 future test period. Uncertainty was evaluated using **Moving Block Bootstrap (MBB, $b = 3\text{ months}$)** to respect time-series autocorrelation. 

Results demonstrate that during the unseen 2022 Mega-Flood, the proposed hybrid achieved a **Kling-Gupta Efficiency (KGE) of 0.872** and restricted peak underestimation bias ($FHV$) to **$-7.9\%$**, whereas unconstrained Random Forest collapsed to $\text{KGE} = 0.573$ with severe peak attenuation ($FHV = -27.6\%$) and conceptual models yielded $\text{KGE} = 0.477$ ($FHV = -40.6\%$). Over the entire out-of-sample period (2022–2024), the hybrid maintained **$\text{KGE} = 0.854\ [95\%\text{ CI: } 0.76, 0.90]$**. A multi-regime ablation study demonstrates that physical baseline anchoring provides the dominant contribution to extreme-flow robustness, offering a reproducible paradigm for flood risk assessment in data-sparse alluvial basins.

**Keywords:** Physics-Guided Machine Learning, Google Earth Engine, Indus River Basin, Sindh Province, Flood Generalization, CHIRPS, ERA5-Land, Water Balance, 2022 Pakistan Flood.

---

## 1. Introduction

### 1.1 Background and Problem Statement
The Indus River Basin is one of the most critical and climate-vulnerable transboundary river systems globally, sustaining over 230 million people and supporting the world's largest contiguous irrigation network—the Indus Basin Irrigation System (IBIS) (Immerzeel et al., 2020; Young et al., 2019). The lower reaches of the basin, situated within Sindh Province, Pakistan, represent an extreme hydraulic and socioeconomic bottleneck. Here, the Indus River flows across flat, low-gradient alluvial plains before discharging into the Arabian Sea via the Indus Delta (Inam et al., 2007).

In recent years, anthropogenic climate change has intensified the magnitude of hydrological extremes across the basin. In the summer of 2022, unprecedented monsoon rainfall driven by coupled moisture dynamics triggered a devastating "super-flood" across Pakistan, with Sindh Province receiving over $350\%$ of its normal 30-year climatological rainfall (World Weather Attribution, 2022; Nanditha et al., 2023). Over 33 million people were affected, vast agricultural belts were submerged, and major hydraulic structures (Guddu, Sukkur, and Kotri Barrages, and Manchar Lake) operated near failure thresholds. Conversely, the region regularly experiences pre-monsoon heatwaves, agricultural droughts, and groundwater depletion during the dry winter (*Rabi*) season (Biemans et al., 2016).

### 1.2 Research Question and Core Contributions
Existing hydrological modeling approaches face two fundamental limitations:
1. **Conceptual Models (e.g., GR4J, SAC-SMA):** While theoretically mass-conserving, their reliance on static, empirically calibrated parameters leads to structural degradation when subjected to unprecedented hydrometeorological shocks (Gupta et al., 2009; Frame et al., 2022).
2. **Standard Machine Learning (e.g., Random Forest, GBDT, LSTM):** Although capable of non-linear pattern recognition, unconstrained models frequently produce unphysical states and suffer from severe conditional mean shrinkage, severely underestimating extreme flood peaks when tested out-of-distribution (Kratzert et al., 2018; Jia et al., 2021).

To address these limitations, this paper provides three primary contributions:
1. **Physics-Anchored Hybrid Architecture:** We formulate a hybrid framework that couples a linear water-balance-informed runoff baseline with non-linear residual machine learning.
2. **Unseen Extreme-Event Evaluation Protocol:** We enforce a strict chronological holdout design where the historic 2022 Pakistan Super-Flood is completely withheld from model calibration to evaluate genuine out-of-distribution extreme generalization.
3. **Multi-Regime Ablation and Trade-off Analysis:** We provide a systematic ablation study evaluating model components across both extreme flood and post-flood recovery regimes.

---

## 2. Literature Review and Gap Analysis

### 2.1 Physical Hydrology of the Indus Basin
The hydrological regime of the Indus Basin is governed by snow-glacier melt in the Upper Indus Basin and intense South Asian monsoon depressions in the lower basin (Immerzeel et al., 2020; Biemans et al., 2016). Downstream of the Panjnad confluence, the river enters Sindh Province, where riverbed aggradation, extensive canal embankments, and flat topography have altered natural floodplain connectivity (Inam et al., 2007). Climatological studies indicate that atmospheric warming is expanding moisture capacity via the Clausius-Clapeyron relation ($\sim 7\%\text{ per }^\circ\text{C}$), generating non-stationary rainfall regimes and elevated peak runoff coefficients (World Weather Attribution, 2022; Nanditha et al., 2023).

### 2.2 Evolution from Conceptual Models to Machine Learning
Hydrological prediction has historically relied on conceptual lumped and semi-distributed models (Gupta et al., 2009). Although these models maintain theoretical water balance representations, their reliance on static empirical parameters leads to structural degradation under novel climatic forcing (Frame et al., 2022; Kratzert et al., 2018). With the proliferation of hydro-climatic big data, deep learning models have achieved record-setting accuracy in streamflow simulation (Kratzert et al., 2018; Nearing et al., 2024; Kratzert et al., 2019). However, purely statistical models frequently fail to conserve mass and suffer from peak flow underestimation (Read et al., 2019; Jia et al., 2021).

### 2.3 Physics-Guided and Hybrid Machine Learning
To reconcile physical interpretability with machine learning flexibility, Physics-Guided Machine Learning (PGML) has emerged as a major focus in computational hydrology (Read et al., 2019; Jia et al., 2021). Anchoring model predictions to first-order water balance baselines constrains the hypothesis space, preventing gradient divergence and maintaining accurate hydrograph variance (Frame et al., 2022).

### 2.4 Cloud-Native Earth Observation (GEE)
Planetary-scale geospatial platforms, specifically Google Earth Engine (GEE), have eliminated computational barriers in multi-sensor hydro-environmental analysis (Gorelick et al., 2017). Multi-sensor satellite platforms provide continuous observations of the terrestrial water cycle, including CHIRPS v2.0 precipitation (Funk et al., 2015), ERA5-Land reanalysis (Muñoz-Sabater et al., 2021), NASA SMAP soil moisture (Entekhabi et al., 2010), SRTM topography (Farr et al., 2007), and GRACE gravimetric storage anomalies (Tapley et al., 2019).

---

## 3. Study Area and Geospatial Datasets

### 3.1 Study Region: Lower Indus Basin in Sindh Province
The study domain encompasses the Lower Indus River Basin within the administrative boundaries of Sindh Province ($140,914\text{ km}^2$, $23.7^\circ\text{N} - 28.5^\circ\text{N}$, $66.6^\circ\text{E} - 71.1^\circ\text{E}$; Fig. 1). Physiographically, the Indus alluvial floodplain is characterized by an extremely flat hydraulic gradient with a mean slope $< 0.8^\circ$ (hydraulic gradient $\approx 1:10,000$), while the western Kirthar mountain range exhibits steep relief ($> 15^\circ$).

Five strategic hydrological nodes were selected for spatial and hydraulic profiling:
* **Guddu Barrage ($28.422^\circ\text{N}, 69.711^\circ\text{E}$, Elev: $75.6\text{ m}$):** Primary entry point of Indus River into Sindh.
* **Sukkur Barrage ($27.705^\circ\text{N}, 68.858^\circ\text{E}$, Elev: $63.8\text{ m}$):** Feeds seven major irrigation canal commands.
* **Kotri Barrage ($25.433^\circ\text{N}, 68.324^\circ\text{E}$, Elev: $17.9\text{ m}$):** Lower Indus barrage regulating delta outflows.
* **Manchar Lake ($26.435^\circ\text{N}, 67.665^\circ\text{E}$, Elev: $32.1\text{ m}$):** Major natural flood attenuation reservoir.
* **Indus Delta ($24.747^\circ\text{N}, 67.923^\circ\text{E}$, Elev: $11.9\text{ m}$):** Coastal estuarine outflow to Arabian Sea.

![Figure 1: Study Area](file:///d:/all%20in%20one/Desktop/new_pro/paper_latex/figures/Figure_Study_Area_Sindh_Indus.png)

### 3.2 Geospatial Earth Observation Inventory
Multi-sensor Earth observation datasets were retrieved via Google Earth Engine API across 2020–2024:

#### **Table 1: Geospatial Earth Observation Dataset Inventory and Operational Variable Roles**
| Dataset | GEE Collection ID | Spatial Res. | Extracted Variable | Role in Proposed Architecture |
| :--- | :--- | :---: | :--- | :--- |
| **CHIRPS v2.0** | `UCSB-CHG/CHIRPS/DAILY` | $0.05^\circ$ ($\sim 5.5\text{ km}$) | Daily Precipitation $P(t)$ | Active input to $Q_{\text{base}}$ baseline and $\hat{\varepsilon}$ ensemble |
| **ERA5-Land** | `ECMWF/ERA5_LAND/DAILY_AGGR` | $0.1^\circ$ ($\sim 10\text{ km}$) | 2m Temperature, Evaporation | Moisture deficit $D = PET - P$ in $\hat{\varepsilon}$ ensemble |
| **NASA SMAP L4**| `NASA/SMAP/SPL4SMGP/008` | $9\text{ km}$ | Root-Zone Soil Moisture | Regional catchment saturation state diagnosis |
| **SRTM DEM** | `USGS/SRTMGL1_003` | $30\text{ m}$ | Topographic Elevation, Slope | Floodplain delineation and hydraulic node profiling |
| **GRACE Mascons**| `NASA/GRACE/MASS_GRIDS_V04/LAND` | $0.5^\circ$ ($\sim 50\text{ km}$) | Terrestrial Storage ($TWSA$) | Regional macro-scale storage boundary state diagnosis |
| **Barrage Telemetry** | `Sindh Irrigation Dept / FFC` | Gauged Nodes | Upstream Inflow $Q_{\text{inflow}}(t)$ | Boundary condition input to $Q_{\text{base}}$ physical baseline |

### 3.3 Observed Catchment Runoff Variable
Observed streamflow discharge ($Q_{\text{m}^3/\text{s}}$) recorded by the Sindh Irrigation Department and Federal Flood Commission (FFC) barrage telemetry was converted to catchment runoff depth ($Q_{\text{depth}}$, mm/month) via:

$$Q_{\text{depth}} = \frac{Q_{\text{m}^3/\text{s}} \cdot \Delta t}{A_{\text{basin}} \cdot 10^3}$$

where $A_{\text{basin}} = 140,914\text{ km}^2$, $\Delta t$ is the monthly duration in seconds, and $10^3$ represents the volumetric conversion factor ($1\text{ mm} \times 1\text{ km}^2 = 1,000\text{ m}^3$).

---

## 4. Methodology & System Architecture

### 4.1 Hierarchical Architecture Framework

![Figure 2: Hierarchical Methodology](file:///d:/all%20in%20one/Desktop/new_pro/paper_latex/figures/Figure_Methodology_Hierarchical_Framework.png)

* **Tier 1 (Data Ingestion):** Cloud-native GEE pipeline extracting multi-sensor grids (Table 1).
* **Tier 2 (Harmonization & Feature Engineering):** Spatial boundary masking, monthly aggregation, Antecedent Precipitation Index ($API$) derivation, and atmospheric moisture deficit modeling ($D = PET - P$).
* **Tier 3 (Physics-Anchored Core):** Dual-stage coupling of water-balance-informed linear baseline with non-linear residual tree ensembles.
* **Tier 4 (Multi-Criteria Evaluation):** Benchmark evaluation across KGE, NSE, RMSE, and peak flow bias ($FHV$).
* **Tier 5 (Decision Support Applications):** Monthly flood risk and inflow volume estimation for Sindh barrages and Manchar Lake.

### 4.2 Mathematical Water Balance Formulation
The regional catchment water balance in the managed Lower Indus is governed by:

$$\frac{dS(t)}{dt} = P(t) - ET(t) - Q(t) - G(t) - D(t)$$

where $P(t)$ is precipitation, $ET(t)$ is evapotranspiration, $Q(t)$ is discharge, $G(t)$ is net groundwater exchange, and $D(t)$ represents major canal irrigation diversions. Antecedent soil moisture memory is modeled using the Antecedent Precipitation Index ($API_t$):

$$API_t = \sum_{k=0}^{K} \gamma^k P_{t-k} = P_t + \gamma P_{t-1} + \gamma^2 P_{t-2}$$

where the memory decay factor is set to $\gamma = 0.60$ based on grid-search calibration on the 2020–2021 training record.

### 4.3 Physics-Anchored Hybrid Architecture
The framework operates in two coupled stages:
1. **Physics-Anchored Runoff Baseline:**
   $$Q_{\text{base}}(t) = \beta_0 + \beta_1 P(t) + \beta_2 API(t)$$
   where coefficients $\beta_1, \beta_2$ are estimated using non-negative least squares with L2 regularization ($\lambda = 2.0$) on the 2020–2021 training set to enforce positive scaling ($\beta_1 \ge 0, \beta_2 \ge 0$).
2. **Non-Linear Residual Tree Ensemble:**
   $$\varepsilon(t) = Q_{\text{obs}}(t) - Q_{\text{base}}(t)$$
   $$\hat{\varepsilon}(t) = \mathcal{F}_{\text{trees}}\big(P(t), ET(t), T_{2m}(t), D_{\text{deficit}}(t), P_{t-1}, P_{t-2}, API(t), \text{Month}\big)$$
3. **Composite Output:**
   $$\hat{Q}(t) = \max\left(0, Q_{\text{base}}(t) + \hat{\varepsilon}(t)\right)$$

### 4.4 Experimental Design and True Extreme Holdout Protocol
* **Model Calibration (2020–2021):** 24 months of moderate baseline hydrometeorology.
* **Unseen Extreme-Event Holdout (2022):** 12 months containing the historic 2022 Pakistan Super-Flood ($+350\%$ precipitation), withheld completely from calibration.
* **Future Generalization Period (2023–2024):** 24 months of non-stationary post-flood recovery.
* **Moving Block Bootstrap (MBB):** 1,000 resamplings with block size $b = 3\text{ months}$ (selected to represent seasonal persistence) to evaluate confidence intervals while respecting time-series autocorrelation.
* **Hyperparameter Integrity:** All model hyperparameters (tree depth $= 3$, estimators $= 100$, learning rate $= 0.08$), feature transformations ($API$ decay $\gamma = 0.60$), and regularization penalties ($\lambda = 2.0$) were estimated exclusively using 5-fold cross-validation on the 2020–2021 calibration period; no information from 2022–2024 was utilized during model selection or tuning.

---

## 5. Results and Discussion

### 5.1 Quantitative Benchmarking Results

#### **Table 2: Quantitative Hydrological Model Benchmark Results Across Unseen 2022 Extreme Flood and Future Validation Periods**
| Model Architecture | $\text{KGE (2022 Flood)}^\dagger$ | $\text{FHV (2022 Flood)}^\ddagger$ | $\text{KGE (2023–2024)}$ | $\text{KGE Combined [95\% CI]}$ | $\text{NSE Combined}$ | $\text{FHV Combined}^\ddagger$ |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **PG-MCH (Proposed)** | **`0.872`** | **`-7.9%`** | **`0.815`** | **`0.854 [0.76, 0.90]`** | **`0.971`** | **`-11.2%`** |
| **TGB-Hydro (GBDT)** | `0.820` | `-7.7%` | `0.800` | `0.819 [0.73, 0.85]` | `0.941` | `-11.6%` |
| **RF-Baseline** | `0.573` | `-27.6%` | `0.548` | `0.572 [0.50, 0.68]` | `0.814` | `-29.3%` |
| **Conceptual GR4J Baseline** | `0.477` | `-40.6%` | `0.586` | `0.527 [0.44, 0.66]` | `0.808` | `-38.0%` |

> $^\dagger\text{2022 Flood}$: Unseen extreme-event holdout withheld entirely from calibration.  
> $^\ddagger\text{FHV}$: Peak flow bias over top 20% high-flow events (ideal = 0%).

#### **Table 3: Systematic Multi-Regime Ablation Study (Unseen 2022 Flood vs. 2023–2024 Future Period)**
| Ablation Configuration | $\text{KGE (2022 Flood)}$ | $\text{FHV (2022 Flood)}$ | $\text{KGE (2023–2024)}$ | $\text{FHV (2023–2024)}$ |
| :--- | :---: | :---: | :---: | :---: |
| **Full PG-MCH (Proposed)** | **`0.872`** | **`-7.9%`** | `0.815` | `-15.2%` |
| **w/o Physical Backbone (Pure ML)** | `0.573` | `-27.6%` | `0.548` | `-31.4%` |
| **w/o Antecedent Memory (No $API$)**| `0.837` | `-13.8%` | `0.811` | `-17.5%` |
| **w/o Thermal/Evaporative Forcing** | `0.887` | `-6.4%` | **`0.882`** | **`-11.3%`** |

---

### 5.2 Comparative Analysis & Multi-Regime Findings

**Unseen 2022 Indus Mega-Flood Reconstruction**
Figure 6 presents the reconstruction of the **unseen 2022 Indus Mega-Flood** in Sindh Province under extreme monsoon forcing. The PG-MCH model was calibrated exclusively using the **2020–2021 baseline period**, with the entire 2022 period withheld from model calibration. The figure compares observed runoff depth with predictions from PG-MCH, TGB-Hydro (GBDT), and the Conceptual Rainfall–Runoff Baseline during the extreme event.

* **Unseen Flood Generalization:** As detailed in Table 2 and Figure 6, during the unseen 2022 Super-Flood, PG-MCH achieved $\text{KGE} = 0.872$ with $FHV = -7.9\%$, whereas unconstrained Random Forest collapsed to $\text{KGE} = 0.573$ and $FHV = -27.6\%$, and the conceptual baseline produced $\text{KGE} = 0.477$ ($FHV = -40.6\%$).
* **GBDT vs. PG-MCH Comparison:** PG-MCH achieved higher overall efficiency across both out-of-sample evaluation periods ($\text{KGE} = 0.872$ vs. $0.820$ in 2022; $\text{KGE} = 0.815$ vs. $0.800$ in 2023–2024; Combined $\text{KGE} = 0.854$ vs. $0.819$), while GBDT achieved a marginally smaller peak-flow bias during the 2022 event ($FHV = -7.7\%$ vs. $-7.9\%$).
* **Physical Baseline Contribution:** Removing the physical baseline caused the largest performance degradation in the ablation experiments (KGE dropped from $0.872$ to $0.573$ during the 2022 flood, and peak underestimation increased from $-7.9\%$ to $-27.6\%$).
* **Thermal Forcing Trade-off:** Interestingly, removing thermal/evaporative forcing improved both KGE ($0.887$ vs. $0.872$) and peak-flow bias ($-6.4\%$ vs. $-7.9\%$) during the 2022 holdout, suggesting that temperature and potential evaporation provide limited incremental predictive information at the monthly basin scale and may contain redundant information relative to precipitation. Their inclusion in the full architecture is therefore maintained as a physically motivated feature group representing the evaporative demand of the catchment water balance rather than as an unconstrained performance maximizer.

---

### 5.3 Visual Demonstrations

#### **Figure 3: Hydrograph Tracking and Residual Errors (2020–2024)**
![Figure 3: Hydrograph](file:///d:/all%20in%20one/Desktop/new_pro/paper_latex/figures/Figure_1_Hydrograph_Comparison_and_Residuals.png)

#### **Figure 4: 1:1 Scatter Regressions Across Out-of-Sample Period (2022–2024)**
![Figure 4: Scatter Plot](file:///d:/all%20in%20one/Desktop/new_pro/paper_latex/figures/Figure_2_Model_Benchmarking_Scatter.png)

#### **Figure 5: Multi-Regime Ablation Bar Chart (2022 Flood KGE vs. $|FHV|$)**
![Figure 5: Ablation](file:///d:/all%20in%20one/Desktop/new_pro/paper_latex/figures/Figure_4_Ablation_Study_Comparison.png)

#### **Figure 6: UNSEEN 2022 Indus Mega-Flood Reconstruction**
![Figure 6: Unseen 2022 Flood Zoom](file:///d:/all%20in%20one/Desktop/new_pro/paper_latex/figures/Figure_3_2022_Extreme_Flood_Hydrograph_Zoom.png)

---

## 6. Physical Hydrological Interpretation
1. **Mitigation of Conditional Mean Shrinkage:** Standard tree ensembles partition feature space and predict leaf node averages, inherently failing to extrapolate beyond historical training maxima. The physical linear baseline scales proportionally with unprecedented precipitation, anchoring the baseline.
2. **Antecedent Catchment Memory:** Multi-month $API$ parameters capture progressive soil saturation build-up prior to catastrophic monsoon peaks.

---

## 7. Practical Implications for Water Management
* **Flood Risk Assessment:** Provides monthly volumetric inflow projections for Guddu, Sukkur, and Kotri Barrages during monsoon onset.
* **Flood Retention Planning:** Volumetric forecasts assist water managers in assessing storage pressure at Manchar Lake.
* **Data-Sparse Basin Modeling:** Demonstrates the feasibility of cloud-native satellite data harmonization where ground gauge networks are sparse.

---

## 8. Limitations and Future Work
* **Temporal Resolution:** The monthly time-step does not resolve sub-daily flash flood hydrographs in Kirthar hill torrents.
* **Spatial Scale:** $0.05^\circ$ CHIRPS and $0.1^\circ$ ERA5-Land grids do not resolve micro-embankments or localized urban drainage.
* **Future Work:** Coupling with daily hydraulic models (e.g., HEC-RAS 2D) and ingesting operational barrage gate telemetry.

---

## 9. Conclusion
This study demonstrated that anchoring residual machine learning to a linear water-balance-informed baseline substantially improves extreme flood generalization in the Lower Indus Basin. When tested on the unseen 2022 Super-Flood, the proposed hybrid preserved peak flows ($FHV = -7.9\%$) while unconstrained machine learning suffered severe peak dampening ($FHV = -27.6\%$). The cloud-native workflow provides a reproducible foundation for basin-scale flood risk modeling.

---

## References

1. **Biemans, H., Siderius, C., Mishra, V., & Ahmad, B. (2016).** Future water resources for food production in Five South Asian River Basins and potential for adaptation. *Hydrology and Earth System Sciences*, 20(9), 3711-3731.
2. **Entekhabi, D., Njoku, E. G., O'Neill, P. E., et al. (2010).** The Soil Moisture Active Passive (SMAP) mission. *Proceedings of the IEEE*, 98(5), 704-716.
3. **Farr, T. G., Rosen, P. A., Caro, E., et al. (2007).** The Shuttle Radar Topography Mission. *Reviews of Geophysics*, 45(2), RG2004.
4. **Frame, J. M., Kratzert, F., Raney, A., et al. (2022).** Post-processing hydrological models with deep learning: Exploring the continuum between physics and data-driven methods. *Hydrological Processes*, 36(9), e14674.
5. **Funk, C., Peterson, P., Landsfeld, M., et al. (2015).** The climate hazards infrared precipitation with stations—a new environmental record for monitoring extremes. *Scientific Data*, 2, 150066.
6. **Gorelick, N., Hancher, M., Dixon, M., Ilyushchenko, I., Thau, D., & Moore, R. (2017).** Google Earth Engine: Planetary-scale geospatial analysis for everyone. *Remote Sensing of Environment*, 202, 18-27.
7. **Gupta, H. V., Kling, H., Yilmaz, K. K., & Martinez, G. F. (2009).** Decomposition of the mean squared error and NSE performance criteria: Implications for improving hydrological modelling. *Journal of Hydrology*, 377(1-2), 80-91.
8. **Immerzeel, W. W., Lutz, A. F., Andrade, M., et al. (2020).** Importance and vulnerability of the world's water towers. *Nature*, 577(7790), 364-369.
9. **Inam, A., Clift, P. D., Giosan, L., et al. (2007).** The geographic and geological context of the Indus River. *Large Rivers: Geomorphology and Management*, 263-274.
10. **Jia, X., Willard, J., Karpatne, A., et al. (2021).** Physics-guided machine learning for scientific discovery: An application in simulating lake water temperature. *ACM Transactions on Data Science*, 2(3), 1-26.
11. **Kratzert, F., Klotz, D., Brenner, C., Schulz, K., & Herrnegger, M. (2018).** Rainfall–runoff modelling using Long Short-Term Memory (LSTM) networks. *Hydrology and Earth System Sciences*, 22(11), 6005-6022.
12. **Kratzert, F., Klotz, D., Herrnegger, M., et al. (2019).** Towards learning universal, regionalized rainfall-runoff representations. *Hydrology and Earth System Sciences*, 23(12), 5089-5110.
13. **Muñoz-Sabater, J., Dutra, E., Agustí-Panareda, A., et al. (2021).** ERA5-Land: a state-of-the-art global reanalysis dataset for land applications. *Earth System Science Data*, 13(9), 4349-4383.
14. **Nanditha, J. S., Kushwaha, A., Singh, R., Malik, I., & Mishra, V. (2023).** The 2022 Pakistan floods: Was it a compound disaster? *Environmental Research Letters*, 18(4), 044005.
15. **Nearing, G., Cohen, D., Doidge, V., et al. (2024).** Global prediction of extreme floods in ungauged watersheds. *Nature*, 627(8004), 559-563.
16. **Read, J. S., Jia, X., Willard, J., et al. (2019).** Process-guided deep learning predictions of lake water temperature. *Water Resources Research*, 55(11), 9173-9190.
17. **Tapley, B. D., Watkins, M. M., Flechtner, F., et al. (2019).** Contributions of GRACE to understanding climate change. *Nature Climate Change*, 9(5), 358-369.
18. **World Weather Attribution. (2022).** Climate Change Increased Extreme Monsoon Rainfall, Resulting in Devastating Floods in Pakistan. *WWA Scientific Rapid Assessment Report*.
19. **Young, W. J., Anwar, A., Bhatti, T., et al. (2019).** *Pakistan: Getting More from Water*. World Bank Group, Washington, DC.
