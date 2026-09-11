"""
Rigorous Hydrological Benchmark & Ablation Framework for Ahr River Basin, Germany
Multi-Decadal Satellite/Gridded Earth Observation & Gauge Telemetry (2000-2021, N=264 Months)
- DWD HYRAS v6.0 Monthly Precipitation P(t)
- ERA5-Land Temperature & Evaporation ET(t)
- ERA5-Land Volumetric Soil Moisture SM(t)
- Real Gauged Ahr Telemetry: Müsch Upstream Inflow Q_inflow(t) & Altenahr Outflow Q_obs(t)
- Multi-Decadal Calibration (2000-2020, N=252 Months)
- Out-of-Distribution Extreme Holdout: 2021 (Featuring the July 2021 Catastrophic Flash Flood)
- Comprehensive Baseline Suite: PG-MCH, GBDT, Random Forest, LSTM, GR2M, Naive Climatology, Persistence
- Moving Block Bootstrap Uncertainty Quantification (1,000 resamples for 95% CIs)
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
from scipy import stats
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import Ridge
from sklearn.metrics import r2_score
import torch
import torch.nn as nn
import torch.optim as optim

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
# 1. Performance Metrics
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

def calc_fhv(obs, sim, q_thresh=0.80):
    obs, sim = np.array(obs), np.array(sim)
    threshold = np.quantile(obs, q_thresh)
    high_idx = np.where(obs >= threshold)[0]
    if len(high_idx) == 0:
        return np.nan
    obs_high = obs[high_idx]
    sim_high = sim[high_idx]
    fhv = ((np.sum(sim_high) - np.sum(obs_high)) / np.sum(obs_high)) * 100.0
    return fhv

def calc_rmse(obs, sim):
    obs, sim = np.array(obs), np.array(sim)
    return np.sqrt(np.mean((obs - sim)**2))

# -------------------------------------------------------------
# 2. Moving Block Bootstrap
# -------------------------------------------------------------
def block_bootstrap_ci(obs, sim, metric_func, block_size=4, n_boot=1000, ci=95):
    n = len(obs)
    if n < block_size:
        return np.nan, np.nan
    n_blocks = int(np.ceil(n / block_size))
    boot_stats = []
    np.random.seed(42)
    for _ in range(n_boot):
        start_indices = np.random.randint(0, n - block_size + 1, size=n_blocks)
        boot_idx = np.concatenate([np.arange(idx, idx + block_size) for idx in start_indices])[:n]
        val = metric_func(obs[boot_idx], sim[boot_idx])
        if isinstance(val, tuple): val = val[0]
        if not np.isnan(val): boot_stats.append(val)
    if len(boot_stats) == 0: return np.nan, np.nan
    lower = np.percentile(boot_stats, (100 - ci) / 2.0)
    upper = np.percentile(boot_stats, 100 - (100 - ci) / 2.0)
    return lower, upper

# -------------------------------------------------------------
# 3. Model Architecture Implementations
# -------------------------------------------------------------
class PGMCH_Ahr:
    def __init__(self, gamma=0.6, alpha_ridge=2.0):
        self.gamma = gamma
        self.alpha_ridge = alpha_ridge
        self.ridge = Ridge(alpha=alpha_ridge, positive=True, fit_intercept=True)
        self.gbr = GradientBoostingRegressor(
            n_estimators=80,
            max_depth=2,
            learning_rate=0.04,
            subsample=0.80,
            random_state=42
        )
        
    def fit(self, X_base, X_resid, y):
        self.ridge.fit(X_base, y)
        base_pred = self.ridge.predict(X_base)
        residuals = y - base_pred
        self.gbr.fit(X_resid, residuals)
        return self
        
    def predict(self, X_base, X_resid, P, Q_inflow, API):
        base_pred = self.ridge.predict(X_base)
        resid_pred = self.gbr.predict(X_resid)
        raw_pred = base_pred + resid_pred
        
        # Dual mass bounds: 0 <= Q <= P + Q_inflow + API
        W_total = P + Q_inflow + API
        bounded_pred = np.maximum(0.0, np.minimum(raw_pred, W_total))
        return bounded_pred, base_pred, resid_pred

# GR2M Conceptual Model
class GR2M_Model:
    def __init__(self):
        self.x1 = 250.0  # Production store capacity (mm)
        self.x2 = 0.85   # Groundwater exchange coefficient
        
    def fit(self, P, ET, Q_obs):
        best_kge = -999
        best_params = (250.0, 0.85)
        for x1 in np.linspace(50.0, 800.0, 30):
            for x2 in np.linspace(0.2, 1.8, 30):
                sim = self._simulate(P, ET, x1, x2)
                kge, _, _, _ = calc_kge(Q_obs, sim)
                if kge > best_kge:
                    best_kge = kge
                    best_params = (x1, x2)
        self.x1, self.x2 = best_params
        return self
        
    def _simulate(self, P, ET, x1, x2):
        S = 0.5 * x1
        Q_sim = []
        for p, et in zip(P, ET):
            # Production store update
            phi = np.tanh(p / x1)
            psi = np.tanh(et / x1)
            S1 = (S + x1 * phi) / (1.0 + phi * S / x1)
            P1 = p - (S1 - S)
            S2 = S1 * (1.0 - psi) / (1.0 + psi * (1.0 - S1 / x1))
            S = S2 / (1.0 + (S2 / x1)**3)**(1/3)
            
            # Routing and exchange
            R = P1 + (S2 - S)
            Q = x2 * R
            Q_sim.append(max(0.0, Q))
        return np.array(Q_sim)
        
    def predict(self, P, ET):
        return self._simulate(P, ET, self.x1, self.x2)

# LSTM Sequence Model
class LSTM_Model(nn.Module):
    def __init__(self, input_dim=6, hidden_dim=16, num_layers=1):
        super(LSTM_Model, self).__init__()
        self.lstm = nn.LSTM(input_dim, hidden_dim, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_dim, 1)
        self.relu = nn.ReLU()
        
    def forward(self, x):
        out, _ = self.lstm(x)
        out = self.fc(out[:, -1, :])
        return self.relu(out)

def train_lstm(X_train, y_train, seq_len=3, epochs=200, lr=0.01):
    torch.manual_seed(42)
    # Prepare sequence batches
    X_seq, y_seq = [], []
    for i in range(len(X_train) - seq_len + 1):
        X_seq.append(X_train[i:i+seq_len])
        y_seq.append(y_train[i+seq_len-1])
    X_seq = torch.tensor(np.array(X_seq), dtype=torch.float32)
    y_seq = torch.tensor(np.array(y_seq), dtype=torch.float32).unsqueeze(1)
    
    # Normalization
    mean_X, std_X = torch.mean(X_seq, dim=(0, 1), keepdim=True), torch.std(X_seq, dim=(0, 1), keepdim=True) + 1e-5
    mean_y, std_y = torch.mean(y_seq), torch.std(y_seq) + 1e-5
    X_norm = (X_seq - mean_X) / std_X
    y_norm = (y_seq - mean_y) / std_y
    
    model = LSTM_Model(input_dim=X_train.shape[1], hidden_dim=16)
    optimizer = optim.Adam(model.parameters(), lr=lr, weight_decay=1e-4)
    criterion = nn.MSELoss()
    
    model.train()
    for ep in range(epochs):
        optimizer.zero_grad()
        pred = model(X_norm)
        loss = criterion(pred, y_norm)
        loss.backward()
        optimizer.step()
        
    return model, (mean_X, std_X, mean_y, std_y)

def predict_lstm(model, norm_params, X_all, seq_len=3):
    mean_X, std_X, mean_y, std_y = norm_params
    X_seq = []
    for i in range(len(X_all) - seq_len + 1):
        X_seq.append(X_all[i:i+seq_len])
    X_seq = torch.tensor(np.array(X_seq), dtype=torch.float32)
    X_norm = (X_seq - mean_X) / std_X
    
    model.eval()
    with torch.no_grad():
        pred_norm = model(X_norm)
        pred = pred_norm * std_y + mean_y
    
    # Pad first seq_len-1 entries with mean
    preds_full = np.zeros(len(X_all))
    preds_full[:seq_len-1] = float(mean_y)
    preds_full[seq_len-1:] = pred.numpy().flatten()
    return np.maximum(0.0, preds_full)

# -------------------------------------------------------------
# 4. Main Execution & Evaluation
# -------------------------------------------------------------
def run_ahr_experiments():
    data_path = "extracted_ahr_data/ahr_basin_monthly_2000_2021.csv"
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Dataset not found: {data_path}")
        
    df = pd.read_csv(data_path)
    print(f"Loaded Ahr dataset: {len(df)} monthly observations (2000-2021)")
    
    # Feature engineering: Lagged-only API (gamma = 0.6)
    gamma = 0.6
    P = df['precip_total_mm'].values
    API = np.zeros(len(P))
    for t in range(len(P)):
        if t == 1:
            API[t] = gamma * P[t-1]
        elif t >= 2:
            API[t] = gamma * P[t-1] + (gamma**2) * P[t-2]
    df['API_lagged'] = API
    df['Deficit'] = np.maximum(0.0, df['evaporation_total_mm'].values - P)
    
    # Base features: P, API, Q_inflow (Müsch)
    X_base = df[['precip_total_mm', 'API_lagged', 'q_inflow_muesch_mm']].values
    # Residual features: P, ET, Temp, SM, Q_inflow, Deficit, Month
    X_resid = df[['precip_total_mm', 'evaporation_total_mm', 'temp_celsius_mean', 
                  'soil_moisture_m3m3', 'q_inflow_muesch_mm', 'Deficit', 'month']].values
    y = df['obs_runoff_altenahr_mm'].values
    
    # Train / Test Split: Calibration (2000-2020, N=252), Holdout (2021, N=12)
    train_mask = (df['year'] <= 2020).values
    test_mask = (df['year'] == 2021).values
    
    y_train, y_test = y[train_mask], y[test_mask]
    P_test = P[test_mask]
    Qin_test = df['q_inflow_muesch_mm'].values[test_mask]
    API_test = API[test_mask]
    
    # 1. Fit PG-MCH
    pg_mch = PGMCH_Ahr(gamma=0.6, alpha_ridge=2.0)
    pg_mch.fit(X_base[train_mask], X_resid[train_mask], y_train)
    sim_pg_mch_test, base_test, _ = pg_mch.predict(X_base[test_mask], X_resid[test_mask], P_test, Qin_test, API_test)
    
    # 2. Pure GBDT
    gbdt = GradientBoostingRegressor(n_estimators=80, max_depth=2, learning_rate=0.04, subsample=0.80, random_state=42)
    gbdt.fit(X_resid[train_mask], y_train)
    sim_gbdt_test = np.maximum(0.0, gbdt.predict(X_resid[test_mask]))
    
    # 3. Random Forest
    rf = RandomForestRegressor(n_estimators=100, max_depth=4, random_state=42)
    rf.fit(X_resid[train_mask], y_train)
    sim_rf_test = np.maximum(0.0, rf.predict(X_resid[test_mask]))
    
    # 4. GR2M Conceptual Model
    gr2m = GR2M_Model()
    gr2m.fit(P[train_mask], df['evaporation_total_mm'].values[train_mask], y_train)
    sim_gr2m_test = gr2m.predict(P_test, df['evaporation_total_mm'].values[test_mask])
    
    # 5. LSTM Sequence Model
    lstm_model, norm_params = train_lstm(X_resid[train_mask], y_train)
    sim_lstm_all = predict_lstm(lstm_model, norm_params, X_resid)
    sim_lstm_test = sim_lstm_all[test_mask]
    
    # 6. Naive Climatology Mean
    clim_mean = df[train_mask].groupby('month')['obs_runoff_altenahr_mm'].mean().to_dict()
    sim_clim_test = np.array([clim_mean[m] for m in df.loc[test_mask, 'month']])
    
    # 7. Naive Persistence (Q_t = Q_{t-1})
    sim_pers_test = np.zeros(len(y_test))
    sim_pers_test[0] = y_train[-1]
    sim_pers_test[1:] = y_test[:-1]
    
    # Evaluate Models on 2021 Extreme Holdout
    models = {
        "PG-MCH (Proposed)": sim_pg_mch_test,
        "TGB-Hydro (GBDT)": sim_gbdt_test,
        "RF-Baseline": sim_rf_test,
        "LSTM (Deep Sequence)": sim_lstm_test,
        "Conceptual GR2M": sim_gr2m_test,
        "Monthly Climatology Mean": sim_clim_test,
        "Monthly Persistence": sim_pers_test
    }
    
    results = []
    print("\n" + "="*80)
    print("AHR RIVER BASIN (GERMANY) - 2021 EXTREME HOLDOUT BENCHMARK (N=12)")
    print("="*80)
    print(f"{'Model':<25} | {'KGE':<7} | {'NSE':<7} | {'RMSE':<7} | {'FHV (Peak)':<12}")
    print("-"*80)
    
    for name, sim in models.items():
        kge, r, alpha, beta = calc_kge(y_test, sim)
        nse = calc_nse(y_test, sim)
        rmse = calc_rmse(y_test, sim)
        fhv = calc_fhv(y_test, sim, q_thresh=0.80)
        
        # Bootstrap CI for FHV
        fhv_low, fhv_high = block_bootstrap_ci(y_test, sim, lambda o, s: calc_fhv(o, s, 0.80), block_size=3)
        ci_str = f"[{fhv_low:+.1f}%, {fhv_high:+.1f}%]" if not np.isnan(fhv_low) else "N/A"
        
        results.append({
            "Model": name,
            "KGE": round(kge, 3),
            "NSE": round(nse, 3),
            "RMSE": round(rmse, 2),
            "FHV": round(fhv, 1),
            "FHV_CI": ci_str
        })
        print(f"{name:<25} | {kge:<7.3f} | {nse:<7.3f} | {rmse:<7.2f} | {fhv:>+6.1f}% {ci_str}")
        
    df_results = pd.DataFrame(results)
    df_results.to_csv("paper_results/tables/ahr_2021_benchmark_results.csv", index=False)
    
    # -------------------------------------------------------------
    # 5. Systematic Within-Model Ablations on Ahr
    # -------------------------------------------------------------
    print("\n" + "="*80)
    print("AHR RIVER BASIN (GERMANY) - SYSTEMATIC ABLATION STUDY (2021)")
    print("="*80)
    
    ablations = {}
    # Full Model
    ablations["Full PG-MCH (Proposed)"] = sim_pg_mch_test
    # w/o Physical Backbone (Pure ML)
    ablations["w/o Physical Backbone (Pure ML)"] = sim_gbdt_test
    # w/o Inflow (No Müsch)
    pg_no_inflow = PGMCH_Ahr()
    X_base_no_in = df[['precip_total_mm', 'API_lagged']].values
    X_resid_no_in = df[['precip_total_mm', 'evaporation_total_mm', 'temp_celsius_mean', 
                        'soil_moisture_m3m3', 'Deficit', 'month']].values
    pg_no_inflow.fit(X_base_no_in[train_mask], X_resid_no_in[train_mask], y_train)
    sim_no_in, _, _ = pg_no_inflow.predict(X_base_no_in[test_mask], X_resid_no_in[test_mask], P_test, 0.0, API_test)
    ablations["w/o Upstream Inflow (No Müsch)"] = sim_no_in
    
    # w/o Antecedent Memory (No API)
    pg_no_api = PGMCH_Ahr()
    X_base_no_api = df[['precip_total_mm', 'q_inflow_muesch_mm']].values
    pg_no_api.fit(X_base_no_api[train_mask], X_resid[train_mask], y_train)
    sim_no_api, _, _ = pg_no_api.predict(X_base_no_api[test_mask], X_resid[test_mask], P_test, Qin_test, 0.0)
    ablations["w/o Antecedent Memory (No API)"] = sim_no_api
    
    # w/o ET
    pg_no_et = PGMCH_Ahr()
    X_resid_no_et = df[['precip_total_mm', 'temp_celsius_mean', 'soil_moisture_m3m3', 'q_inflow_muesch_mm', 'month']].values
    pg_no_et.fit(X_base[train_mask], X_resid_no_et[train_mask], y_train)
    sim_no_et, _, _ = pg_no_et.predict(X_base[test_mask], X_resid_no_et[test_mask], P_test, Qin_test, API_test)
    ablations["w/o Evaporative Demand (No ET)"] = sim_no_et
    
    # w/o Coupled Land-Atmosphere
    pg_no_atm = PGMCH_Ahr()
    X_resid_no_atm = df[['precip_total_mm', 'q_inflow_muesch_mm', 'month']].values
    pg_no_atm.fit(X_base[train_mask], X_resid_no_atm[train_mask], y_train)
    sim_no_atm, _, _ = pg_no_atm.predict(X_base[test_mask], X_resid_no_atm[test_mask], P_test, Qin_test, API_test)
    ablations["w/o Coupled Land-Atmosphere (No ET/Temp/SM)"] = sim_no_atm
    
    ablation_results = []
    for name, sim in ablations.items():
        kge, _, _, _ = calc_kge(y_test, sim)
        fhv = calc_fhv(y_test, sim, q_thresh=0.80)
        ablation_results.append({
            "Ablation Configuration": name,
            "KGE (2021 Flood)": round(kge, 3),
            "FHV (2021 Flood)": f"{fhv:>+6.1f}%"
        })
        print(f"{name:<45} | KGE: {kge:<6.3f} | FHV: {fhv:>+6.1f}%")
        
    df_abl = pd.DataFrame(ablation_results)
    df_abl.to_csv("paper_results/tables/ahr_2021_ablation_results.csv", index=False)
    
    # -------------------------------------------------------------
    # 6. Comparative Visualizations
    # -------------------------------------------------------------
    plt.figure(figsize=(10, 5), dpi=300)
    test_dates = df.loc[test_mask, 'date'].values
    x_axis = np.arange(len(test_dates))
    
    plt.plot(x_axis, y_test, 'k-', lw=2.5, label='Observed (Altenahr Gauge)', zorder=5)
    plt.plot(x_axis, sim_pg_mch_test, 'b-o', lw=2.0, ms=5, label='PG-MCH (Proposed)', zorder=4)
    plt.plot(x_axis, sim_gbdt_test, 'g--', lw=1.8, label='Pure GBDT (No Backbone)', zorder=3)
    plt.plot(x_axis, sim_lstm_test, 'm-.', lw=1.8, label='LSTM Sequence', zorder=2)
    plt.plot(x_axis, sim_gr2m_test, 'r:', lw=1.8, label='Conceptual GR2M', zorder=1)
    
    plt.axvline(x=6, color='gray', linestyle='--', alpha=0.7) # July 2021 flood peak (month index 6)
    plt.text(6.1, 80, 'July 2021 Cloudburst\nPeak Flood ($Q_{obs} = 88.6$ mm)', fontsize=9, color='darkred', weight='bold')
    
    plt.xticks(x_axis, test_dates, rotation=45)
    plt.xlabel('Date (Monthly)')
    plt.ylabel('Discharge Depth (mm/month)')
    plt.title('Ahr River Basin (Germany) 2021 Extreme Holdout Evaluation\n(Pre-saturated convective flash flood)', weight='bold')
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend(frameon=True, loc='upper left')
    plt.tight_layout()
    
    plt.savefig('paper_latex/figures/Figure_Ahr_2021_Hydrograph_Comparison.png')
    plt.savefig('paper_results/figures/Figure_Ahr_2021_Hydrograph_Comparison.png')
    plt.close()
    print("\nSaved plot: paper_latex/figures/Figure_Ahr_2021_Hydrograph_Comparison.png")

if __name__ == "__main__":
    run_ahr_experiments()
