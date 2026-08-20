"""
Google Earth Engine (GEE) Authentication and Connection Module
Using Service Account Credentials from ee-muzzamil12.json
"""

import os
import json
import ee

CREDENTIALS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ee-muzzamil12.json')

def init_gee(credentials_path=None):
    """
    Initializes Earth Engine using the service account credentials.
    """
    if credentials_path is None:
        credentials_path = CREDENTIALS_FILE
        
    if not os.path.exists(credentials_path):
        raise FileNotFoundError(f"Earth Engine credentials file not found at: {credentials_path}")
        
    with open(credentials_path, 'r', encoding='utf-8') as f:
        key_data = json.load(f)
        
    client_email = key_data.get('client_email')
    project_id = key_data.get('project_id')
    
    credentials = ee.ServiceAccountCredentials(client_email, credentials_path)
    ee.Initialize(credentials)
    print(f" Earth Engine connected successfully! (Project: {project_id}, Account: {client_email})", flush=True)
    return ee

if __name__ == '__main__':
    print("Testing Earth Engine connection...", flush=True)
    ee_instance = init_gee()
    
    # Simple query test
    dem = ee_instance.Image('USGS/SRTMGL1_003')
    band_names = dem.bandNames().getInfo()
    print(f"Verification Successful: SRTM DEM bands available -> {band_names}", flush=True)
