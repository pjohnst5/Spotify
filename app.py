from dotenv import load_dotenv
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import logging

# Won't need this in production
load_dotenv()

scope = "user-library-read playlist-modify-private"
client_id = os.getenv("SPOTIPY_CLIENT_ID")
client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
playlist_id = os.getenv("PLAYLIST_ID")

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

hey = sp.me()

# Get latest 20 songs
results = sp.current_user_saved_tracks()
tracks = [item['track']['id'] for item in results['items']]

# Replace latest 20 songs
sp.playlist_replace_items(playlist_id=playlist_id, items=tracks)

print('Replaced latest 20 songs')
for idx, item in enumerate(results['items']):
    track = item['track']
    print_str = str(idx) + track['artists'][0]['name'] + " - " + track['name']
    print(print_str)

