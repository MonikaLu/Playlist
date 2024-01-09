import pandas as pd
import requests
import os
from dotenv import load_dotenv
BASEDIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASEDIR, '.env.local'))

# Constants
access_token=os.getenv('AUTHORIZATION')
playlistId=os.getenv('PLAYLIST_ID')
base_url = 'https://api.spotify.com/v1/search'

# Data
songNamesFromFile = pd.read_csv('songNames.csv')
songNames = songNamesFromFile['Songs:'].tolist()

headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
}

# Checks existing songs
def get_playlist_tracks(playlist_id, headers):
    playlist_url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    response = requests.get(playlist_url, headers=headers)
    track_data = response.json()
    existing_track_ids = [item['track']['id'] for item in track_data['items']]
    return existing_track_ids

existing_ids = get_playlist_tracks(playlistId, headers)

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
        
# Compare song_ids with existing_ids
filtered_ids = []
for songId in song_ids:
    if songId not in existing_ids:
        filtered_ids.append(songId)
        

add_tracks_response = requests.post(
    f'https://api.spotify.com/v1/playlists/{playlistId}/tracks',
    headers=headers,
    json={'uris': [f'spotify:track:{id}' for id in filtered_ids]})

# Add counter 5/10 songs completed