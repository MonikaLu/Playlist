# If songs in new attempt are in correct song, remove from new attempts.

# Get song ids from playlist ID

# Check overlap, if overlap, put in the overlap_list

# Go in New Attempt and remove these song ids

import requests
import os
from requests.exceptions import RequestException
from dotenv import load_dotenv
BASEDIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASEDIR, '.env.local'))
access_token=os.getenv('AUTHORIZATION')
headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
}

correct_songs_playlist = os.getenv('CORRECT_SONGS_PLAYLIST_ID')
new_attempt_songs_playlist = os.getenv('NEW_ATTEMPT_SONGS_PLAYLIST_ID')


def getSongIds(playlist_id):
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

def comparePlaylists(list1, list2):
    overlaps = []
    for song in list1:
        if song in list2:
            overlaps.append(song)
    return overlaps

def removeSongsFromPlaylist(listOfSongs, playlist):
    batch_size = 100
    for i in range(0, len(listOfSongs), batch_size):
        batch = listOfSongs[i:i + batch_size]

        # Prepare the payload for the batch
        tracks = [{"uri": f"spotify:track:{song}"} for song in batch]

        # Send the DELETE request for the batch
        remove_tracks_response = requests.delete(
            f'https://api.spotify.com/v1/playlists/{playlist}/tracks',
            headers=headers,
            json={"tracks": tracks}
        )

        # Check the response
        if remove_tracks_response.status_code == 200:
            print(f"Batch {i//batch_size + 1} successfully removed.")
        else:
            print(f"Error occurred in batch {i//batch_size + 1}:",
                  remove_tracks_response.status_code, remove_tracks_response.text)

def main():
    correct_songs = getSongIds(correct_songs_playlist)
    new_songs = getSongIds(new_attempt_songs_playlist)
    overlapped_songs = comparePlaylists(new_songs, correct_songs)
    removeSongsFromPlaylist(overlapped_songs, new_songs)

main()