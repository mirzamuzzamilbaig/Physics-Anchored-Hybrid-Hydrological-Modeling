"""
Interactive Leaflet/Folium Geospatial Map for Indus Basin (Sindh Region)
Displays Barrage Infrastructure, River Elevation Profile, and Station Stats.
"""

import folium
from folium import plugins
import pandas as pd
import os

os.makedirs('visualizations', exist_ok=True)
stations = pd.read_csv('extracted_sindh_data/sindh_indus_barrages_stations.csv')

# Create base map centered over Sindh
m = folium.Map(location=[26.5, 68.5], zoom_start=7, tiles='CartoDB positron')

# Add Satellite and OpenStreetMap Layers
folium.TileLayer('OpenStreetMap', name='OpenStreetMap').add_to(m)
folium.TileLayer(
    tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    attr='Esri World Imagery',
    name='Satellite View'
).add_to(m)

# Add Indus River Mainstem Approximate Path
river_coords = [
    [28.422, 69.711], # Guddu
    [27.705, 68.858], # Sukkur
    [26.850, 68.100], # Dadu / Central
    [26.435, 67.665], # Manchar Lake connection
    [25.433, 68.324], # Kotri
    [24.747, 67.923], # Thatta / Delta
    [24.150, 67.500]  # Arabian Sea Outflow
]

folium.PolyLine(
    river_coords,
    color='#0066cc',
    weight=5,
    opacity=0.8,
    tooltip='Indus River Mainstem Corridor (Sindh)'
).add_to(m)

# Add Barrages & Water Nodes with Rich Popups
for _, row in stations.iterrows():
    popup_html = f"""
    <div style="font-family: Arial, sans-serif; width: 230px; padding: 4px;">
        <h4 style="color: #0d47a1; margin-bottom: 4px;">{row['station_name'].replace('_', ' ')}</h4>
        <p style="margin: 2px 0; font-size: 12px;"><b>Role:</b> {row['description']}</p>
        <p style="margin: 2px 0; font-size: 12px;"><b>Elevation:</b> {row['elevation_m']:.1f} meters a.s.l.</p>
        <p style="margin: 2px 0; font-size: 12px;"><b>Coordinates:</b> {row['latitude']:.3f}° N, {row['longitude']:.3f}° E</p>
    </div>
    """
    
    icon_color = 'red' if 'Lake' in row['station_name'] else ('green' if 'Delta' in row['station_name'] else 'blue')
    icon_symbol = 'water' if 'Barrage' in row['station_name'] else 'info-sign'
    
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=folium.Popup(popup_html, max_width=280),
        tooltip=f"{row['station_name'].replace('_', ' ')} ({row['elevation_m']:.1f} m)",
        icon=folium.Icon(color=icon_color, icon=icon_symbol, prefix='glyphicon')
    ).add_to(m)

# Add Layer Control and MiniMap
folium.LayerControl().add_to(m)
plugins.MiniMap(toggle_display=True).add_to(m)

map_html = 'visualizations/sindh_indus_basin_interactive_map.html'
m.save(map_html)
print(f" [SUCCESS] Generated Interactive Geospatial Map -> {map_html}", flush=True)
