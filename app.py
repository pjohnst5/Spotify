from dotenv import load_dotenv
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import random
import logging

# Won't need this in production
load_dotenv()

scope = "user-library-read playlist-modify-private"
client_id = os.getenv("SPOTIPY_CLIENT_ID")
client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
playlist_id = os.getenv("PLAYLIST_ID")
playlist_id_2 = os.getenv("PLAYLIST_ID_2")

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
user = sp.me()

# Get latest 20 songs
# results = sp.current_user_saved_tracks()
# tracks = [item['track']['id'] for item in results['items']]

# # Replace latest 20 songs
# sp.playlist_replace_items(playlist_id=playlist_id, items=tracks)

# Make random list of 20 liked songs
liked_songs_count = 0
offset = 0
limit = 50
k = 20

while True:
    results = sp.current_user_saved_tracks(offset=offset, limit=limit)
    liked_songs_count += len(results['items'])
    if results['next'] is None:
        break
    offset += limit

print(f"Number of liked songs: {liked_songs_count}")

population = range(0, liked_songs_count)
random_integers = random.sample(population, k)
tracks = []
track_ids = []

for rand_int in random_integers:
    result = sp.current_user_saved_tracks(offset=rand_int, limit=1)
    track = result['items'][0]['track']
    tracks.append(track)
    track_ids.append(track['id'])

sp.playlist_replace_items(playlist_id=playlist_id_2, items=track_ids)

logging.info('Updated random 20 songs')
for idx, track in enumerate(tracks):
    print_str = str(idx) + " " + track['artists'][0]['name'] + " - " + track['name']
    logging.info(print_str)
