import logging
import os
import azure.functions as func
import spotipy
from spotipy.oauth2 import SpotifyOAuth

app = func.FunctionApp()

@app.timer_trigger(schedule="0 0 3 * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False)
def Appifier(myTimer: func.TimerRequest) -> None:
    logging.info('Python timer trigger function executed.')
    if myTimer.past_due:
        logging.info('The timer is past due!')

    scope = "user-library-read playlist-modify-private"
    playlist_id = os.getenv("PLAYLIST_ID")
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    # Get latest 20 songs
    results = sp.current_user_saved_tracks()
    tracks = [item['track']['id'] for item in results['items']]

    # Replace latest 20 songs
    sp.playlist_replace_items(playlist_id=playlist_id, items=tracks)
    logging.info('Replaced latest 20 songs')
    for idx, item in enumerate(results['items']):
        track = item['track']
        print_str = str(idx) + track['artists'][0]['name'] + " - " + track['name']
        logging.info(print_str)
