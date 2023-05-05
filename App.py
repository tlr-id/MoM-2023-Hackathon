import os.path
import random
import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import geopandas
import json
import numpy as np
import folium
import pickle

from search_artist import *
from fields import *

def draw_image(data):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(' ')
    with col2:
          st.image(data.get('image_url'), width=300, use_column_width=False)
    with col3:
        st.write(' ')

#Main

if __name__=="__main__":

    st.write('# Fan Turnout')
    st.write('### Select an Artist and a Country to Get Information')
    selected_artist= st.text_input("Search ([Artist]-[Country])", "")

    if st.button("Search 👀"):
        artist,country_name=selected_artist.split('-')
        country_name=country_name.capitalize()

        artist_data = find_artist(artist)
        id = artist_data["id"]
        fan_data =  get_fan_data(id)
        artist_metadata = get_artist_metadata(id)
        spotify_where_info = get_spotify_where_info(id)
        insta_info = get_instagram_audience_stats(id)
        youtube_info = get_youtube_audience_stats(id)
        tiktok_info = get_tiktok_audience_stats(id)

        spotify_top_country_info = spotify_where_info["countries"].get(country_name, None)
        if spotify_top_country_info is None:
            st.write(f"### Artist data could not be found for {country_name}.")
            st.write('### '+" - ".join(list(spotify_where_info["countries"].keys())))
            st.write("### Please try again.")

        insta_top_country_info = get_instagram_country_info(insta_info, country_name)
        youtube_top_country_info = get_youtube_country_info(youtube_info, country_name)
        tiktok_top_country_info = get_tiktok_country_info(tiktok_info, country_name)

        data =  {
                "metadata": {**{"name": artist_data["Name"]}, **artist_metadata},
                "fan_metrics": fan_data,
                "instagram_audience_info": insta_info,
                "instagram_top_country_info": insta_top_country_info,
                "youtube_audience_info": youtube_info,
                "youtube_top_country_info": youtube_top_country_info,
                "tiktok_audience_info": tiktok_info,
                "tiktok_top_country_info": tiktok_top_country_info,
                "spotify_city_info": spotify_where_info["cities"],
                "spotify_top_country_info": spotify_top_country_info,
                }

        with open(f"data.json", "w") as outfile:
            json.dump(data, outfile, indent=4)

        st.write('### '+data["metadata"]["name"]) #artist_metadata.get('name')
        draw_image(artist_metadata)

        st.write(f"##### Career Stage: {artist_metadata.get('career_status').get('stage').capitalize()}")

        st.subheader(f'{country_name} Information: ')
        if insta_top_country_info:
            st.write(f'##### Instagram Followers: {insta_top_country_info["followers"]:,}')
        if youtube_top_country_info:
            st.write(f'##### Youtube Subscribers: {youtube_top_country_info["subscribers"]:,}')
        if tiktok_top_country_info:
            st.write(f'##### Tiktok Followers: {tiktok_top_country_info["followers"]:,}')

        st.write(f'##### Spotify Listeners: {spotify_top_country_info[0]["listeners"]:,}')

        st.subheader('Global Information (Streaming): ')
        influence_data=artist_metadata.get('cm_statistics')
        st.write(f'##### Spotify Monthly Listeners: {influence_data.get("sp_monthly_listeners"):,}')
        st.write(f'##### Spotify Followers: {influence_data.get("sp_followers"):,}')
        st.write(f'##### Deezer Followers: {influence_data.get("deezer_fans"):,}')

        st.subheader('Global Information (Social Media): ')
        st.write(f'##### Instagram Followers: {influence_data.get("ins_followers"):,}')
        st.write(f'##### Tiktok Followers: {influence_data.get("tiktok_followers"):,}')
        #st.write('Your data is ready, you can now access the other pages!')