
import json
import requests

response = requests.post('https://api.chartmetric.com/api/token', json={'refreshtoken': 'G9F02Aaw0qjFedlWjMjPhr54Ke8b2Wi8GWtafS2o37aEzqLAYc83FeGYKYZTaDE1'})

response_json = json.loads(response.text)
token = response_json['token']

headers = {'Authorization': 'Bearer ' + token}

params = {
    'sortBy': 'spotify_followers',
    'maxSpotifyFollowers': 1000000,
    'limit': 10
}
response = requests.get('https://api.chartmetric.com/api/artist/anr/by/social-index', headers=headers, params=params)

response_json = json.loads(response.text)
# Extracting names from the response
artist_names = [artist['name'] for artist in response_json['obj']]

print(artist_names)


# Set the access token in the headers
headers = {'Authorization': 'Bearer ' + token}

# Set the artist ID and platform type
artist_id = '6M2wZ9GZgrQXHCFfjv46we'  # Dua Lipa's Spotify artist ID
platform = 'spotify'

# Set the endpoint URL and parameters
endpoint_url = f'https://api.chartmetric.com/api/artist/{platform}/{artist_id}/get-ids'
params = {
    'aggregate': 'true'  # We only need one result with all of the IDs
}

# Send the GET request to the endpoint
response = requests.get(endpoint_url, headers=headers, params=params)

# Parse the JSON response
response_json = json.loads(response.text)

# Extract the Chartmetric ID from the response

chartmetric_id = response_json['obj'][0]['chartmetric_id']
print("The Chartmetric ID is:", chartmetric_id)
print(f"Dua Lipa's Chartmetric ID is {chartmetric_id}")
