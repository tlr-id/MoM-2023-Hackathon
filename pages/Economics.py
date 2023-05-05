import os.path
import random
import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import geopandas
import json
import numpy as np
#Import search_artist.py (in parent folder) functions
from search_artist import *
from fields import *
import folium
import pickle
from seatgeek_api import *


st.write('# Economy')


with open(f"data.json", "r") as outfile:
        artist_data = json.load(outfile)

artist_metadata=artist_data.get('metadata')
st.subheader("Current available information about "+ artist_metadata.get('name')+"'s concerts :")
st.write(get_seatgeek_data(artist_metadata.get('name')))
name=artist_metadata.get('name')
