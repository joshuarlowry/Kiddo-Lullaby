import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time

def play(contextUri):
    print(("About to start playing {0} on device {1}.").format(contextUri,deviceID))
    sp.start_playback(device_id=deviceID,context_uri=contextUri)

def playSong(uris):
    print(("About to start playing {0} on device {1}.").format(uris,deviceID))
    sp.start_playback(device_id=deviceID,uris=uris)
    sp.repeat('context',deviceID)

def nowPlaying():
    now = sp.current_playback()
    print(("Playing on {0}").format(now['device']['name']))
    track = now['item']['name']
    artists = now['item']['album']['artists'][0]
    print(("Playing {0} by {1}").format(track, artists['name']))

def getActiveDevice():
    devices = sp.devices()
    activeDevice = devices['devices'][0]['id']
    # note, idx is used to store the index of the returned tuple. 
    for idx, device in enumerate(devices['devices']):
        print(("{0}, {1} - {2}").format(device['id'],device['name'],device['is_active']))
        if(device['is_active']):
            activeDevice = device['id']
            print("Assigning active device.")
    return activeDevice


#Authentication
scope = "user-read-private user-read-email user-read-playback-state user-modify-playback-state user-read-currently-playing app-remote-control streaming playlist-read-private playlist-read-collaborative user-library-read"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
deviceID = getActiveDevice()
heyTiger = ['spotify:track:2WOM5LEDprdaJ6V6gnFK0Z']
marching = 'spotify:playlist:0ibeKGFzDV4bbqENRNrcf8'
nowPlaying()
# playSong(heyTiger)
# nowPlaying()
# time.sleep(30)
# play(marching)
# nowPlaying()

