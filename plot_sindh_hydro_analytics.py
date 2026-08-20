"""
Hydrological & Climate Analytics Visualizer for Indus Basin (Sindh Region)
Generates high-resolution publication charts and interactive HTML dashboards.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns

# Set style
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'

os.makedirs('visualizations', exist_ok=True)

# Load data
df = pd.read_csv('extracted_sindh_data/sindh_indus_basin_monthly_2020_2024.csv')
df['datetime'] = pd.to_datetime(df['date'])
stations = pd.read_csv('extracted_sindh_data/sindh_indus_barrages_stations.csv')

# -------------------------------------------------------------
# 1. Multi-Panel Comprehensive Hydro-Climatic Timeseries (2020-2024)
# -------------------------------------------------------------
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(14, 11), sharex=True)
fig.suptitle('Indus Basin (Sindh Region) Hydro-Meteorological Dynamics (2020–2024)\nEarth Observation Analysis via CHIRPS, ERA5-Land & SRTM', 
             fontsize=15, fontweight='bold', y=0.98)

# Panel 1: Precipitation & Flood Anomalies
bars = ax1.bar(df['datetime'], df['precip_total_mm'], width=20, color='#1f77b4', edgecolor='#0d47a1', alpha=0.85, label='CHIRPS Monthly Rainfall (mm)')
ax1.set_ylabel('Rainfall (mm)', fontsize=11, fontweight='bold')
ax1.set_title('A. Monthly Precipitation & Monsoon Extremes (2022 Super Flood Highlighted)', fontsize=12, loc='left', fontweight='bold')
ax1.axhline(y=df['precip_total_mm'].mean(), color='red', linestyle='--', alpha=0.7, label=f'5-Year Mean: {df["precip_total_mm"].mean():.1f} mm')

# Annotate 2022 Flood Peak
flood_2022 = df[df['date'] == '2022-07'].iloc[0]
ax1.annotate('2022 Historic Flood Peak\n(226.7 mm in July)', 
             xy=(pd.to_datetime('2022-07-01'), flood_2022['precip_total_mm']),
             xytext=(pd.to_datetime('2021-08-01'), 210),
             arrowprops=dict(facecolor='crimson', shrink=0.08, width=2, headwidth=8),
             fontsize=10, fontweight='bold', color='crimson',
             bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="crimson", lw=1.5))
ax1.legend(loc='upper right', frameon=True)

# Panel 2: Temperature & Heatwaves
ax2.plot(df['datetime'], df['temp_celsius_mean'], color='#d62728', lw=2.2, marker='o', markersize=4, label='ERA5-Land 2m Mean Temp (°C)')
ax2.fill_between(df['datetime'], df['temp_celsius_mean'], color='#ff9999', alpha=0.3)
ax2.set_ylabel('Temperature (°C)', fontsize=11, fontweight='bold')
ax2.set_title('B. Mean Monthly Ambient Temperature & Pre-Monsoon Heat Peaks', fontsize=12, loc='left', fontweight='bold')
ax2.legend(loc='upper right', frameon=True)

# Panel 3: Total Evaporation
ax3.plot(df['datetime'], df['evaporation_total_mm'], color='#2ca02c', lw=2.2, marker='s', markersize=4, label='ERA5-Land Total Evaporation (mm)')
ax3.fill_between(df['datetime'], df['evaporation_total_mm'], color='#98df8a', alpha=0.3)
ax3.set_ylabel('Evaporation (mm)', fontsize=11, fontweight='bold')
ax3.set_xlabel('Year / Month', fontsize=11, fontweight='bold')
ax3.set_title('C. Total Surface & Lake Evaporation Dynamics', fontsize=12, loc='left', fontweight='bold')
ax3.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
ax3.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
plt.xticks(rotation=45)
ax3.legend(loc='upper right', frameon=True)

plt.tight_layout()
timeseries_png = 'visualizations/sindh_indus_hydro_timeseries_2020_2024.png'
plt.savefig(timeseries_png, dpi=300, bbox_inches='tight')
plt.close()
print(f" [SUCCESS] Saved Hydro-Climatic Timeseries Plot -> {timeseries_png}", flush=True)

# -------------------------------------------------------------
# 2. Indus River Elevation & Hydraulic Profile (Sindh Barrages)
# -------------------------------------------------------------
plt.figure(figsize=(10, 6))
plt.plot(stations['station_name'], stations['elevation_m'], marker='o', markersize=10, color='#1f77b4', lw=2.5, linestyle='-')

for i, row in stations.iterrows():
    plt.annotate(f"{row['station_name'].replace('_', ' ')}\n({row['elevation_m']:.1f} m)\n{row['description']}", 
                 (i, row['elevation_m']),
                 textcoords="offset points", 
                 xytext=(0, 15 if i % 2 == 0 else -35), 
                 ha='center', fontsize=9, fontweight='bold',
                 bbox=dict(boxstyle="round,pad=0.3", fc="#f0f8ff", ec="#1f77b4", lw=1))

plt.title('Indus River Hydraulic Elevation Profile in Sindh Province\nFrom Upper Sindh Entry (Guddu) to Indus Delta', fontsize=13, fontweight='bold')
plt.ylabel('Elevation above sea level (meters)', fontsize=11, fontweight='bold')
plt.xlabel('Hydrological Stations & Barrages (Downstream Flow Direction ->)', fontsize=11, fontweight='bold')
plt.ylim(0, 95)
plt.grid(True, linestyle='--', alpha=0.6)

profile_png = 'visualizations/sindh_indus_river_elevation_profile.png'
plt.savefig(profile_png, dpi=300, bbox_inches='tight')
plt.close()
print(f" [SUCCESS] Saved Indus River Elevation Profile -> {profile_png}", flush=True)
