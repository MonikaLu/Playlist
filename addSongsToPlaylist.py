import pandas as pd
import requests
from requests.exceptions import RequestException
import os
from dotenv import load_dotenv
BASEDIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASEDIR, '.env.local'))

# Constants
access_token=os.getenv('AUTHORIZATION')
playlistId=os.getenv('PLAYLIST_ID')
base_url = 'https://api.spotify.com/v1/search'
headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
}

# Checks existing songs with pagination
def get_existing_tracks(playlist_id, headers):
    playlist_url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    existing_tracks = []
    while playlist_url:
        try:
            response = requests.get(playlist_url, headers=headers)
            response.raise_for_status()
            data = response.json()
            existing_tracks.extend(item['track']['id'] for item in data['items'])
            playlist_url = data.get('next')
        except RequestException as e:
            print(f"An error occurred: {e}")
            break
    return existing_tracks

def getSongIdsFromSpotify(songList):
    song_ids = []
    for song in songList:
        params = {
            'q': song,
            'type': 'track',
            'limit': 1
        }
        res = requests.get(base_url, headers=headers, params=params).json()
        tracks = res['tracks']['items']
        if tracks:
            song_ids.append(tracks[0]['id'])
    return song_ids

# Compare song_ids with existing_ids
def getFilteredList(songList, existing_ids):
    filtered_ids = []
    for songId in songList:
        if songId not in existing_ids:
            filtered_ids.append(songId)
    return filtered_ids

def add_songs_to_playlist(filtered_ids):
    songs_successfully_added = 0
    for id in filtered_ids:
        add_tracks_response = requests.post(
        f'https://api.spotify.com/v1/playlists/{playlistId}/tracks',
        headers=headers,
        json={'uris': [f'spotify:track:{id}']})
        if add_tracks_response.status_code == 201:
            songs_successfully_added += 1
            print(songs_successfully_added, "/", len(filtered_ids), end='\r')
        if songs_successfully_added == len(filtered_ids):
            print("Completed!")
        if songs_successfully_added == 0:
            print("No new songs are added!")

# Data
def main():
    chunk_size = 10  # Adjust based on your system's capabilities
    existing_ids = get_existing_tracks(playlistId, headers)
    for chunk in pd.read_csv('nesten_ferdig.csv', sep='|', chunksize=chunk_size):
        songNames = chunk['Songs:'].tolist()
        all_song_ids = getSongIdsFromSpotify(songNames)
        filtered_ids = getFilteredList(all_song_ids, existing_ids)
        add_songs_to_playlist(filtered_ids)
        
main()