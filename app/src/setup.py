# This will run through initial authentication and populate the .cache file with your token. 

import spotipy
from spotipy.oauth2 import SpotifyOAuth

scope = "user-read-private user-read-email user-read-playback-state user-modify-playback-state user-read-currently-playing app-remote-control streaming playlist-read-private playlist-read-collaborative user-library-read"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
sp.current_user()