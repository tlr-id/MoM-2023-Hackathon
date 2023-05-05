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
st.write('# 📊 Statistics')
with open(f"data.json", "r") as outfile:
        artist_data = json.load(outfile)

#Get artist metadata
artist_metadata=artist_data.get('metadata')
#Get artist fan metrics
fan_metrics=artist_data.get("fan_metrics")
platforms = list(fan_metrics.keys())
st.write('# Fan Metrics')
for platform in platforms:
        st.write(f"### {platform}")
        for k,v in fan_metrics[platform].items():
                st.write(f"{k.replace('_',' ').capitalize()}: {int(v):,}")

st.write('# Instagram Audience Info')
instagram_audience_info=artist_data.get("instagram_audience_info")
df = pd.DataFrame(instagram_audience_info["audience_genders_per_age"])
df = df.reset_index(drop=True)
st.table(df)
st.write('Average likes per post:', instagram_audience_info['avg_likes_per_post'])
st.write('Average comments per post:', instagram_audience_info['avg_commments_per_post'])
st.write('Engagement rate:', instagram_audience_info['engagement_rate'])
#Tiktok
st.write('# TikTok Audience Info')
tiktok_audience_info=artist_data.get("tiktok_audience_info")

df = pd.DataFrame(tiktok_audience_info["audience_genders_per_age"])
df = df.reset_index(drop=True)
#rename columns

st.table(df)
st.write('Average likes per post:', tiktok_audience_info['avg_likes_per_post'])
st.write('Average comments per post:', tiktok_audience_info['avg_commments_per_post'])
st.write('Engagement rate:', tiktok_audience_info['engagement_rate'])
#st.write(fan_metrics)
#st.write(instagram_metrics)