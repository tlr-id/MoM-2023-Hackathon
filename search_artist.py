import requests
import json

from fields import *

API_URL = 'https://api.chartmetric.com/api/'
ARTIST_URL = API_URL+"artist/{}/" # artist id
REFRESH_KEY = 'G9F02Aaw0qjFedlWjMjPhr54Ke8b2Wi8GWtafS2o37aEzqLAYc83FeGYKYZTaDE1'

# Load the header once at the sartup
response = requests.post(API_URL+"token", 
                        json={'refreshtoken': REFRESH_KEY})
response_json = json.loads(response.text)
HEADERS = {'Authorization': 'Bearer '+response_json['token']}

def find_artist(artist_name, verbose=False):
    response = requests.get(API_URL+"search", 
                            params={"q": artist_name,
                                    "limit": 10,
                                    "offset": 0,
                                    }, 
                            headers=HEADERS
                            )
    if response.status_code == 200:
        response_json = response.json()
        first_artist = response_json['obj']['artists'][0]
        artist_dict = {"Name": first_artist['name'],
                    "id": first_artist['id'],
                    #"Spotify_followers": first_artist['sp_followers'],
                    "image_url": first_artist['image_url']
                    }
        if verbose:
            print(json.dumps(artist_dict, indent=4))
    else:
        print("Error occurred. Status code: ", response.status_code)
        artist_dict = {}
    return artist_dict

def get_artist_metadata(id, verbose=False):
    response = requests.get(ARTIST_URL.format(id),
                            headers=HEADERS,
                            #params={"geoOnly": True},
                            )
    if response.status_code == 200:
        data = response.json()['obj']
        if verbose:
            print(json.dumps(data, indent=4))
        return {field: data[field] for field in METADATA_FIELDS}
    else:
        print(f"Error {response.status_code}: {response.reason}")
        return {}

def get_fan_data(id, verbose=False):
    dct = {}
    for fan_metric in FAN_METRICS:
        platform = list(fan_metric.keys())[0]
        fields = list(fan_metric.values())[0]
        url = ARTIST_URL.format(id)+'stat/{}'.format(platform)
        response = requests.get(url,
                        headers=HEADERS, 
                        params={'latest': True,
                                'interpolated': True,
                                },
                        )
        if response.status_code == 200:
            data = response.json()['obj']
            # Only get the value, discard time change data (for now!)
            # each has only one so idx 0 holds
            dct[platform] = {field: data[field][0]["value"] for field in fields}
            if verbose:
                print(json.dumps(data, indent=4))
        else:
            print(f"Error on {platform} {response.status_code}: {response.reason}")
            continue
    return dct

################################################################

def get_instagram_audience_stats(id, verbose=False):
    url = ARTIST_URL+"instagram-audience-stats"
    response = requests.get(url.format(id), 
                            headers=HEADERS,
                            )
    dct = {}
    if response.status_code == 200:
        data = response.json()["obj"]
        if verbose:
            print(json.dumps(data, indent=4))
        for field in INSTAGRAM_FIELDS:
            dct[field] = data[field]
    else:
        print(f"Error {response.status_code}: {response.reason}")
    return dct

def get_instagram_country_info(insta_info, country_name):
    for country_dict in insta_info["top_countries"]:
        if country_dict["name"] == country_name:
            return country_dict
    print(f"Could not find the Instagram Country info for: {country_name}")
    return {}

################################################################
def get_youtube_audience_stats(id, verbose=False):
    url = ARTIST_URL+"youtube-audience-stats"
    response = requests.get(url.format(id), 
                            headers=HEADERS,
                            params={"geoOnly": True}
                            )
    dct = {}
    if response.status_code == 200:
        data = response.json()["obj"]
        if verbose:
            print(json.dumps(data, indent=4))
        for field in YOUTUBE_FIELDS:
            dct[field] = data[field]
    else:
        print(f"Error {response.status_code}: {response.reason}")
    return dct

def get_youtube_country_info(youtube, country_name):
    for country_dict in youtube["top_countries"]:
        if country_dict["name"] == country_name:
            return country_dict
    print(f"Could not find the Youtube Country info for: {country_name}")
    return {}

################################################################

def get_tiktok_audience_stats(id, verbose=False):
    url = ARTIST_URL+"tiktok-audience-stats"
    response = requests.get(url.format(id), 
                            headers=HEADERS,
                            )
    dct = {}
    if response.status_code == 200:
        data = response.json()["obj"]
        if verbose:
            print(json.dumps(data, indent=4))
        for field in TIKTOK_FIELDS:
            dct[field] = data[field]
    else:
        print(f"Error {response.status_code}: {response.reason}")
    return dct

def get_tiktok_country_info(tiktok, country_name):
    for country_dict in tiktok["top_countries"]:
        if country_dict["name"] == country_name:
            return country_dict
    print(f"Could not find the Tiktok Country info for: {country_name}")
    return {}

################################################################

def get_spotify_where_info(id, verbose=False):
    url = ARTIST_URL+"where-people-listen"
    response = requests.get(url.format(id), 
                            headers=HEADERS,
                            params={'latest': True,
                                    'limit': 50})
    if response.status_code == 200:
        response_json = response.json()
        if verbose:
            json.dumps(response_json['obj'], indent=4)
        return response_json['obj']
    else:
        print("Error occurred. Status code: ", response.status_code)
        return {}, {}

def get_spotify_country_info(id, country_name):
    spotify_where_info = get_spotify_where_info(id)
    spotify_country_info = spotify_where_info["countries"].get(country_name, None)
    if spotify_country_info:
        return spotify_country_info[0]
    else:
        print(f"Could not find the Spotify Country info for: {country_name}")

################################################################

def main(artist_name, country_name):
    artist_data = find_artist(artist_name)
    id = artist_data["id"]

    spotify_where_info = get_spotify_where_info(id)
    spotify_top_country_info = spotify_where_info["countries"].get(country_name, None)
        
    insta_info = get_instagram_audience_stats(id)
    insta_top_country_info = get_instagram_country_info(insta_info, country_name)

    youtube_info = get_youtube_audience_stats(id)
    youtube_top_country_info = get_youtube_country_info(youtube_info, country_name)

    tiktok_info = get_tiktok_audience_stats(id)
    tiktok_top_country_info = get_tiktok_country_info(tiktok_info, country_name)

    return {
            "metadata": {**{"name": artist_data["Name"]}, **get_artist_metadata(id)},
            "fan_metrics": get_fan_data(id),
            "instagram_audience_info": insta_info,
            "instagram_top_country_info": insta_top_country_info,
            "youtube_audience_info": youtube_info,
            "youtube_top_country_info": youtube_top_country_info,
            "tiktok_audience_info": tiktok_info,
            "tiktok_top_country_info": tiktok_top_country_info,
            "spotify_city_info": get_spotify_where_info(id)["cities"],
            "spotify_top_country_info": spotify_top_country_info,
            }

if __name__=="__main__":
    x = "Dua Lipa"
    y = "Germany"
    data = main(x, y)
    # Export as json
    with open(f"{x}-{y}.json", "w") as outfile:
        json.dump(data, outfile, indent=4)
    print("Done!")
