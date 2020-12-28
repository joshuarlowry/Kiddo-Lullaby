import spotipy
#import pprint

from flask import Flask
server = Flask(__name__)
#from airium import Airium
#https://stackoverflow.com/questions/6748559/generating-html-documents-in-python
from spotipy.oauth2 import SpotifyOAuth

scope = "user-read-private user-read-email user-read-playback-state user-modify-playback-state user-read-currently-playing app-remote-control streaming playlist-read-private playlist-read-collaborative user-library-read"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

@server.route("/")
def hello():
    return "Hello World!"

@server.route("/kiddo")
def kiddo():
    devices = sp.devices()
    for idx, device in enumerate(devices['devices']):
        print(("{0}, {1} - {2}").format(device['id'],device['name'],device['is_active']))

    now = sp.current_playback()
    print(("Playing on {0}").format(now['device']['name']))
    track = now['item']['name']
    artists = now['item']['album']['artists'][0]
    return(("Playing {0} by {1}").format(track, artists['name']))

if __name__ == "__main__":
   server.run(host='localhost') 
#pp = pprint.PrettyPrinter(indent=4)
#pp.pprint(now)


#sp.start_playback('ab8f217d556c0295562f7767177cf9d58e41bc67',"spotify:playlist:37i9dQZF1DX03b46zi3S82")
#sp.volume(45)

# results = sp.current_user_saved_tracks()
# for idx, item in enumerate(results['items']):
#     track = item['track']
#     print(idx, track['artists'][0]['name'], " – ", track['name'])