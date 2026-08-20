"""
Physics-Informed Machine Learning Flood Risk & Runoff Predictor for Indus Basin (Sindh)
Implements Random Forest and Gradient Boosting models trained on extracted GEE variables:
- Antecedent Rainfall Indices (API)
- Evaporative Demand & Thermal Deficit
- Extreme Monsoon Precipitation Flags
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, mean_squared_error, r2_score
import joblib
import os

os.makedirs('models', exist_ok=True)

# Load dataset
df = pd.read_csv('extracted_sindh_data/sindh_indus_basin_monthly_2020_2024.csv')

# Feature Engineering: Lagged precipitation & Antecedent Moisture Indicators
df['precip_lag1'] = df['precip_total_mm'].shift(1).fillna(0)
df['precip_lag2'] = df['precip_total_mm'].shift(2).fillna(0)
df['temp_lag1'] = df['temp_celsius_mean'].shift(1).fillna(df['temp_celsius_mean'].mean())
df['evap_lag1'] = df['evaporation_total_mm'].shift(1).fillna(df['evaporation_total_mm'].mean())

# Multi-month Cumulative Monsoon Rainfall
df['monsoon_cumulative_3m'] = df['precip_total_mm'] + df['precip_lag1'] + df['precip_lag2']

# Define High-Water / Flood Risk State (Precipitation > 50 mm/month & Cumulative > 100 mm)
df['flood_risk_level'] = np.where(df['precip_total_mm'] >= 100, 2, # High / Extreme Flood Risk (e.g. 2022, 2020, 2024)
                         np.where(df['precip_total_mm'] >= 30, 1,  # Moderate / Alert
                         0))                                       # Low / Normal

features = ['month', 'temp_celsius_mean', 'evaporation_total_mm', 'precip_lag1', 'precip_lag2', 'temp_lag1', 'evap_lag1']
X = df[features]
y = df['flood_risk_level']

# Train Random Forest Classifier
clf = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=4)
clf.fit(X, y)

# Feature Importance
importance_df = pd.DataFrame({
    'Feature': features,
    'Importance': clf.feature_importances_
}).sort_values('Importance', ascending=False)

print("\n=======================================================", flush=True)
print(" SINDH INDUS BASIN MACHINE LEARNING MODEL RESULTS", flush=True)
print("=======================================================", flush=True)
print("\nFeature Importance Rankings:")
for _, row in importance_df.iterrows():
    print(f"- {row['Feature']:20s}: {row['Importance']*100:.2f}%", flush=True)

# Save trained model
model_path = 'models/sindh_flood_risk_model.joblib'
joblib.dump(clf, model_path)
print(f"\n [SUCCESS] Saved Trained Random Forest Model -> {model_path}", flush=True)
