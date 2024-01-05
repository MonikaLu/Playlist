import pandas as pd
import requests
import os
from dotenv import load_dotenv
BASEDIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASEDIR, '.env.local'))

# Constants
access_token=os.getenv('SPOTIFY_ACCESS_TOKEN')
playlistId=os.getenv('PLAYLIST_ID')
base_url = 'https://api.spotify.com/v1/search'

# Data
songNamesFromFile = pd.read_csv('songNames.csv')
songNames = songNamesFromFile['Songs:'].tolist()

headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
}

# q and type are defined by Spotify and required.
song_ids = []
for song in songNames:
    params = {
        'q': song,
        'type': 'track',
        'limit': 1
    }
    res = requests.get(base_url, headers=headers, params=params).json()
    tracks = res['tracks']['items']
    if tracks:
        song_ids.append(tracks[0]['id'])
        
add_tracks_response = requests.post(
    f'https://api.spotify.com/v1/playlists/{playlistId}/tracks',
    headers=headers,
    json={'uris': [f'spotify:track:{id}' for id in song_ids]}
)