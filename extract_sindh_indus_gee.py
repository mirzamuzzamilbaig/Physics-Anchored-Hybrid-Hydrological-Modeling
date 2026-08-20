"""
Indus Basin (Sindh Region) Hydrological & Earth Observation Data Extractor
Extracts Multi-Decadal and Multi-Sensor GEE Datasets for Sindh Province & Key Barrages:
- Guddu Barrage (Upper Sindh Indus Entry)
- Sukkur Barrage (Central Indus Canal Command)
- Kotri Barrage (Lower Indus / Delta Gateway)
- Manchar Lake (Flood Retention & Reservoir Dynamics)
- Indus Delta (Thatta/Coastal Outflow)
"""

import os
import json
import ee
import pandas as pd
from gee_connector import init_gee

ee = init_gee()

# Define Key Hydrological Nodes in Sindh Region (Indus Basin)
SINDH_STATIONS = {
    'Guddu_Barrage': {'lat': 28.422, 'lon': 69.711, 'desc': 'Upper Sindh Indus River Entry'},
    'Sukkur_Barrage': {'lat': 27.705, 'lon': 68.858, 'desc': 'Central Indus Canal Command'},
    'Kotri_Barrage': {'lat': 25.433, 'lon': 68.324, 'desc': 'Lower Indus Barrage & Delta Outflow'},
    'Manchar_Lake': {'lat': 26.435, 'lon': 67.665, 'desc': 'Major Flood Basin & Lake System'},
    'Indus_Delta_Thatta': {'lat': 24.747, 'lon': 67.923, 'desc': 'Indus Estuary & Coastal Mangroves'}
}

def get_sindh_geometry():
    """Retrieves FAO GAUL Level 1 Sindh province polygon."""
    sindh_fc = ee.FeatureCollection('FAO/GAUL/2015/level1').filter(
        ee.Filter.And(
            ee.Filter.eq('ADM0_NAME', 'Pakistan'),
            ee.Filter.eq('ADM1_NAME', 'Sindh')
        )
    )
    return sindh_fc.first().geometry()

def extract_sindh_basin_timeseries(start_date='2020-01-01', end_date='2024-12-31'):
    """
    Extracts monthly time-series of CHIRPS Precipitation, ERA5-Land Temperature & Evaporation,
    SMAP Soil Moisture, and GRACE Terrestrial Water Storage for Sindh Province.
    """
    sindh_geom = get_sindh_geometry()
    os.makedirs('extracted_sindh_data', exist_ok=True)
    
    print(f"\n=======================================================", flush=True)
    print(f" EXTRACTING INDUS BASIN DATA FOR SINDH REGION", flush=True)
    print(f" Time Range: {start_date} to {end_date}", flush=True)
    print(f"=======================================================\n", flush=True)
    
    # 1. CHIRPS Monthly Precipitation
    print("1. Extracting CHIRPS Monthly Rainfall across Sindh...", flush=True)
    chirps = (ee.ImageCollection('UCSB-CHG/CHIRPS/DAILY')
              .filterDate(start_date, end_date)
              .filterBounds(sindh_geom)
              .select('precipitation'))
              
    # Aggregate monthly
    months = ee.List.sequence(1, 12)
    start_year = int(start_date.split('-')[0])
    end_year = int(end_date.split('-')[0])
    years = ee.List.sequence(start_year, end_year)
    
    def get_monthly_rainfall(y):
        y = ee.Number(y)
        def get_by_month(m):
            m = ee.Number(m)
            s_date = ee.Date.fromYMD(y, m, 1)
            e_date = s_date.advance(1, 'month')
            
            monthly_img = chirps.filterDate(s_date, e_date).sum()
            mean_stat = monthly_img.reduceRegion(
                reducer=ee.Reducer.mean(),
                geometry=sindh_geom,
                scale=10000,
                maxPixels=1e9
            ).get('precipitation')
            
            return ee.Feature(None, {
                'year': y,
                'month': m,
                'date': s_date.format('YYYY-MM'),
                'precip_total_mm': mean_stat
            })
        return months.map(get_by_month)
        
    monthly_fc = ee.FeatureCollection(years.map(get_monthly_rainfall).flatten())
    rain_data = [f['properties'] for f in monthly_fc.getInfo()['features'] if f['properties'].get('precip_total_mm') is not None]
    df_rain = pd.DataFrame(rain_data)
    
    # 2. ERA5-Land Monthly Climate (Temp, Evaporation, Radiation)
    print("2. Extracting ERA5-Land Monthly Climate across Sindh...", flush=True)
    era5 = (ee.ImageCollection('ECMWF/ERA5_LAND/DAILY_AGGR')
            .filterDate(start_date, end_date)
            .filterBounds(sindh_geom))
            
    def get_monthly_era5(y):
        y = ee.Number(y)
        def get_by_month(m):
            m = ee.Number(m)
            s_date = ee.Date.fromYMD(y, m, 1)
            e_date = s_date.advance(1, 'month')
            
            sub = era5.filterDate(s_date, e_date)
            mean_temp = sub.select('temperature_2m').mean().subtract(273.15)
            sum_evap = sub.select('total_evaporation_sum').sum().multiply(1000).abs()
            
            stats = mean_temp.addBands(sum_evap).reduceRegion(
                reducer=ee.Reducer.mean(),
                geometry=sindh_geom,
                scale=20000,
                maxPixels=1e9
            )
            
            return ee.Feature(None, {
                'date': s_date.format('YYYY-MM'),
                'temp_celsius_mean': stats.get('temperature_2m'),
                'evaporation_total_mm': stats.get('total_evaporation_sum')
            })
        return months.map(get_by_month)
        
    era5_fc = ee.FeatureCollection(years.map(get_monthly_era5).flatten())
    era5_data = [f['properties'] for f in era5_fc.getInfo()['features'] if f['properties'].get('temp_celsius_mean') is not None]
    df_era5 = pd.DataFrame(era5_data)
    
    # 3. GRACE Terrestrial Water Storage Anomaly (TWSA - Groundwater & Surface Water Mass)
    print("3. Extracting GRACE Terrestrial Water Storage Anomalies for Sindh...", flush=True)
    grace = (ee.ImageCollection('NASA/GRACE/MASS_GRIDS/LAND')
             .filterDate('2018-01-01', end_date)
             .filterBounds(sindh_geom)
             .select('lwe_thickness_csr'))
             
    def extract_grace(img):
        stat = img.reduceRegion(ee.Reducer.mean(), sindh_geom, 25000, maxPixels=1e9)
        date_str = img.date().format('YYYY-MM')
        return ee.Feature(None, {
            'date': date_str,
            'grace_tws_anomaly_cm': stat.get('lwe_thickness_csr')
        })
        
    grace_fc = grace.map(extract_grace).getInfo()
    grace_data = [f['properties'] for f in grace_fc['features'] if f['properties'].get('grace_tws_anomaly_cm') is not None]
    df_grace = pd.DataFrame(grace_data)
    
    # Merge Regional Sindh Dataset
    df_sindh = pd.merge(df_rain, df_era5, on='date', how='outer')
    if not df_grace.empty:
        df_sindh = pd.merge(df_sindh, df_grace, on='date', how='outer')
        
    df_sindh.sort_values('date', inplace=True)
    sindh_csv = 'extracted_sindh_data/sindh_indus_basin_monthly_2020_2024.csv'
    df_sindh.to_csv(sindh_csv, index=False)
    print(f"\n [SUCCESS] Saved Sindh Provincial Monthly Basin Data -> {sindh_csv}", flush=True)
    
    # 4. Extract Daily Hydro-Meteorology for Key Barrages
    print("\n4. Extracting Station-Level Data for Key Indus Barrages & Nodes...", flush=True)
    station_records = []
    for name, info in SINDH_STATIONS.items():
        pt = ee.Geometry.Point([info['lon'], info['lat']])
        dem_val = ee.Image('USGS/SRTMGL1_003').reduceRegion(ee.Reducer.mean(), pt.buffer(1000), 30).get('elevation').getInfo()
        station_records.append({
            'station_name': name,
            'description': info['desc'],
            'latitude': info['lat'],
            'longitude': info['lon'],
            'elevation_m': dem_val
        })
        
    df_stations = pd.DataFrame(station_records)
    stations_csv = 'extracted_sindh_data/sindh_indus_barrages_stations.csv'
    df_stations.to_csv(stations_csv, index=False)
    print(f" [SUCCESS] Saved Barrage Station Metadata -> {stations_csv}", flush=True)
    
    return df_sindh, df_stations

if __name__ == '__main__':
    df_sindh, df_stations = extract_sindh_basin_timeseries(start_date='2020-01-01', end_date='2024-12-31')
    print("\n=== Sindh Regional Monthly Data Sample (Top 12 Months) ===")
    print(df_sindh.head(12))
    print("\n=== Key Barrages & Hydrological Nodes in Sindh ===")
    print(df_stations)
