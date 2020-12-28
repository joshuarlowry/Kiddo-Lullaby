import spotipy
from spotipy.oauth2 import SpotifyOAuth

scope = "user-read-private user-read-email user-read-playback-state user-modify-playback-state user-read-currently-playing app-remote-control streaming playlist-read-private playlist-read-collaborative user-library-read"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

devices = sp.devices()
for idx, device in enumerate(devices['devices']):
    print(("{0}, {1} - {2}").format(device['id'],device['name'],device['is_active']))

now = sp.current_playback()
print(("Playing on {0}").format(now['device']['name']))
track = now['item']['name']
artists = now['item']['album']['artists'][0]
print(("Playing {0} by {1}").format(track, artists['name']))