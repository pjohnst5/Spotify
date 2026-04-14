import logging
import os
import azure.functions as func
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import random

app = func.FunctionApp()

@app.timer_trigger(schedule="0 0 7 * * *", arg_name="myTimer")
def Last20(myTimer: func.TimerRequest) -> None:
    logging.info('Starting to make last 20 liked songs playlist')
    if myTimer.past_due:
        logging.info('The timer is past due!')

    scope = "user-library-read playlist-modify-private"
    playlist_id = os.getenv("LAST_20_ID")
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    # Get latest 20 songs
    results = sp.current_user_saved_tracks()
    tracks = [item['track']['id'] for item in results['items']]

    # Replace latest 20 songs
    sp.playlist_replace_items(playlist_id=playlist_id, items=tracks)
    logging.info('Replaced latest 20 songs')
    for idx, item in enumerate(results['items']):
        track = item['track']
        print_str = str(idx) + " " + track['artists'][0]['name'] + " - " + track['name']
        logging.info(print_str)

@app.timer_trigger(schedule="0 0 7 * * *", arg_name="myTimer")
def Random20(myTimer: func.TimerRequest) -> None:
    logging.info('Starting to make random 20 songs playlist')
    if myTimer.past_due:
        logging.info('The timer is past due!')

    scope = "user-library-read playlist-modify-private"
    playlist_id_2 = os.getenv("RANDOM_20_ID")
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

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

    logging.info(f"Number of liked songs: {liked_songs_count}")

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

