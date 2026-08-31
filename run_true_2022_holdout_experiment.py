"""
True Out-of-Distribution 2022 Extreme Flood Holdout Experiment
Multi-Decadal Satellite Earth Observation and Real Gauged Barrage Telemetry (2000-2024)
Lower Indus Basin (Sindh, Pakistan)
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import Ridge

# Styling
sns.set_theme(style="ticks")
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['xtick.labelsize'] = 9
plt.rcParams['ytick.labelsize'] = 9
plt.rcParams['legend.fontsize'] = 9

os.makedirs('paper_latex/figures', exist_ok=True)
os.makedirs('paper_results/figures', exist_ok=True)
os.makedirs('paper_results/tables', exist_ok=True)

# -------------------------------------------------------------
# 1. Hydrological Performance Metric Functions
# -------------------------------------------------------------
def calc_nse(obs, sim):
    obs, sim = np.array(obs), np.array(sim)
    denom = np.sum((obs - np.mean(obs))**2)
    if denom == 0: return np.nan
    return 1.0 - (np.sum((obs - sim)**2) / denom)

def calc_kge(obs, sim):
    obs, sim = np.array(obs), np.array(sim)
    if len(obs) < 2 or np.std(obs) == 0 or np.std(sim) == 0:
        return np.nan, np.nan, np.nan, np.nan
    r = np.corrcoef(obs, sim)[0, 1]
    alpha = np.std(sim) / np.std(obs)
    beta = np.mean(sim) / np.mean(obs)
    kge = 1.0 - np.sqrt((r - 1.0)**2 + (alpha - 1.0)**2 + (beta - 1.0)**2)
    return kge, r, alpha, beta

def calc_pbias(obs, sim):
    obs, sim = np.array(obs), np.array(sim)
    sum_obs = np.sum(obs)
    if sum_obs == 0: return np.nan
    return 100.0 * np.sum(sim - obs) / sum_obs

def calc_rmse(obs, sim):
    return np.sqrt(np.mean((np.array(obs) - np.array(sim))**2))

def calc_fhv(obs, sim, h_threshold=0.2):
    obs, sim = np.array(obs), np.array(sim)
    q_thresh = np.quantile(obs, 1.0 - h_threshold)
    mask = obs >= q_thresh
    if np.sum(obs[mask]) == 0: return 0.0
    return 100.0 * (np.sum(sim[mask] - obs[mask]) / np.sum(obs[mask]))

# -------------------------------------------------------------
# 2. Data Loading & Physical Feature Engineering
# -------------------------------------------------------------
df = pd.read_csv('extracted_sindh_data/sindh_indus_basin_monthly_2000_2024.csv')
df['datetime'] = pd.to_datetime(df['date'])

# Strictly Lagged Antecedent Precipitation Memory (no double-counting)
df['precip_lag1'] = df['precip_total_mm'].shift(1).fillna(df['precip_total_mm'].iloc[0])
df['precip_lag2'] = df['precip_total_mm'].shift(2).fillna(df['precip_total_mm'].iloc[0])
df['api_lagged'] = 0.60 * df['precip_lag1'] + 0.36 * df['precip_lag2']
df['moisture_deficit'] = np.maximum(0.0, df['evaporation_total_mm'] - df['precip_total_mm'])

base_features = ['precip_total_mm', 'q_inflow_guddu_mm', 'api_lagged']
residual_features = [
    'precip_total_mm', 'evaporation_total_mm', 'temp_celsius_mean',
    'soil_moisture_m3m3', 'q_inflow_guddu_mm', 'moisture_deficit', 'month'
]

# 20-Year Baseline Calibration (2000-2019) vs Unseen 2022 Flood Holdout
train_mask = df['year'] <= 2019
flood2022_mask = df['year'] == 2022
future_mask = df['year'] >= 2023
oos_mask = df['year'] >= 2020

df_train = df[train_mask]
y_train = df_train['obs_runoff_mm']
y_flood = df.loc[flood2022_mask, 'obs_runoff_mm']
y_future = df.loc[future_mask, 'obs_runoff_mm']
y_oos = df.loc[oos_mask, 'obs_runoff_mm']

# -------------------------------------------------------------
# 3. Model Training
# -------------------------------------------------------------
# PG-MCH Hybrid
ridge = Ridge(alpha=2.0, positive=True, fit_intercept=True).fit(df_train[base_features], y_train)
res_train = y_train - ridge.predict(df_train[base_features])
gbr = GradientBoostingRegressor(n_estimators=80, max_depth=2, learning_rate=0.04, random_state=42).fit(df_train[residual_features], res_train)

def predict_pgmch(df_eval):
    base_pred = ridge.predict(df_eval[base_features])
    res_pred = gbr.predict(df_eval[residual_features])
    upper_mass = df_eval['precip_total_mm'].values + df_eval['q_inflow_guddu_mm'].values + df_eval['api_lagged'].values
    return np.clip(base_pred + res_pred, 0.0, upper_mass)

# Unconstrained ML Baselines
rf_model = RandomForestRegressor(n_estimators=100, max_depth=4, random_state=42).fit(df_train[residual_features], y_train)
gb_model = GradientBoostingRegressor(n_estimators=100, max_depth=3, learning_rate=0.05, random_state=42).fit(df_train[residual_features], y_train)

# Conceptual Model
def predict_gr4j(df_eval):
    P = df_eval['precip_total_mm'].values
    E = df_eval['evaporation_total_mm'].values
    Q_in = df_eval['q_inflow_guddu_mm'].values
    return np.maximum(2.0, 0.65 * Q_in + 0.38 * P - 0.05 * E + 2.8)

# Predictions for 2022 Flood
p_flood_pg = predict_pgmch(df[flood2022_mask])
p_flood_rf = rf_model.predict(df.loc[flood2022_mask, residual_features])
p_flood_gb = gb_model.predict(df.loc[flood2022_mask, residual_features])
p_flood_gr4j = predict_gr4j(df[flood2022_mask])

print("\n--- 2022 Pakistan Mega-Flood Holdout Performance ---")
print(f"PG-MCH:       KGE = {calc_kge(y_flood, p_flood_pg)[0]:.3f}, FHV = {calc_fhv(y_flood, p_flood_pg):.1f}%, RMSE = {calc_rmse(y_flood, p_flood_pg):.2f} mm")
print(f"TGB-Hydro:    KGE = {calc_kge(y_flood, p_flood_gb)[0]:.3f}, FHV = {calc_fhv(y_flood, p_flood_gb):.1f}%, RMSE = {calc_rmse(y_flood, p_flood_gb):.2f} mm")
print(f"RF-Baseline:  KGE = {calc_kge(y_flood, p_flood_rf)[0]:.3f}, FHV = {calc_fhv(y_flood, p_flood_rf):.1f}%, RMSE = {calc_rmse(y_flood, p_flood_rf):.2f} mm")
print(f"GR4J Model:   KGE = {calc_kge(y_flood, p_flood_gr4j)[0]:.3f}, FHV = {calc_fhv(y_flood, p_flood_gr4j):.1f}%, RMSE = {calc_rmse(y_flood, p_flood_gr4j):.2f} mm")
