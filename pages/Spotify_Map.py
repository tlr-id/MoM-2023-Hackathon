import os.path
import random
import streamlit as st
import folium
from streamlit_folium import st_folium
import geopandas
import json
import numpy as np
# Import search_artist.py (in parent folder) functions
import folium
import pickle
from folium.plugins import HeatMap
import pandas as pd

st.write('## 🔍 Spotify  Top Cities Statistics')
# Create pandas dataframe with lat and lon


def make_marker(location, popup, tooltip, icon, map):
    return folium.Marker(location=location, popup=popup, tooltip=tooltip, icon=icon).add_to(map)


def make_circle_marker(location, radius, color, fill_color, map, tooltip, popup, fill=True):
    return folium.CircleMarker(location=location, tooltip=tooltip, popup=popup, radius=radius, color=color, fill_color=fill_color, fill=fill).add_to(map)


heat_m = folium.Map(location=[41.3787519, 2.132281],
                    zoom_start=8, tiles="Stamen Terrain", width="%100",
                    height="%100")

json_file = "/Users/recep_oguz_araz/Projects/measure_of_music-MTG_best/data.json"


# Load the JSON file
with open(json_file, 'r') as f:
    json_data = json.load(f)

name = json_data['metadata'].get('name')
# Extract the 'spotify_city_info' key from the JSON data
spotify_city_info = json_data['spotify_city_info']

# Loop through the list of cities and extract the 'lat' and 'lng' values
for city in spotify_city_info:
    lat = spotify_city_info.get(city)[0]["lat"]
    lng = spotify_city_info.get(city)[0]["lng"]
    location = [lat, lng]
    artist_city_rank = spotify_city_info.get(city)[0]["artist_city_rank"]
    listeners = spotify_city_info.get(city)[0]["listeners"]
    population = spotify_city_info.get(city)[0]["population"]
    popup = f"<strong>{name}</strong><br> City rank: {artist_city_rank}</br><br> Spotify listeners: {listeners}</br><br> City Population: {population}</br>"

    make_circle_marker(location=location, radius=15, color='blue',
                       fill_color='red', map=heat_m, tooltip=city, popup=popup, fill=True)

folium.plugins.MiniMap(tile_layer=None, position='bottomright', width=150, height=150, collapsed_width=25, collapsed_height=25, zoom_level_offset=- 5,
                       zoom_level_fixed=None, center_fixed=False, zoom_animation=True, toggle_display=True, auto_toggle_display=False, minimized=False).add_to(heat_m)


st_data = st_folium(heat_m, width=700)
