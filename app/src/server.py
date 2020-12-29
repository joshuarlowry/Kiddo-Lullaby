import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, redirect, url_for
server = Flask(__name__)

def play(sp, deviceID, contextUri):
    print(("About to start playing {0} on device {1}.").format(contextUri,deviceID))
    sp.start_playback(device_id=deviceID,context_uri=contextUri)

def playSong(sp, deviceID, uris):
    print(("About to start playing {0} on device {1}.").format(uris,deviceID))
    sp.start_playback(device_id=deviceID,uris=uris)
    sp.repeat('context',deviceID)

def nowPlaying(sp):
    now = sp.current_playback()
    print(("Playing on {0}").format(now['device']['name']))
    track = now['item']['name']
    artists = now['item']['album']['artists'][0]
    returnString = ("Playing {0} by {1}").format(track, artists['name'])
    print(returnString)
    return returnString

def getActiveDevice(sp):
    devices = sp.devices()
    activeDevice = devices['devices'][0]['id']
    # note, idx is used to store the index of the returned tuple. 
    for idx, device in enumerate(devices['devices']):
        print(("{0}, {1} - {2}").format(device['id'],device['name'],device['is_active']))
        if(device['is_active']):
            activeDevice = device['id']
            print("Assigning active device.")
    return activeDevice

def authenticationRoutine():
    scope = "user-read-private user-read-email user-read-playback-state user-modify-playback-state user-read-currently-playing app-remote-control streaming playlist-read-private playlist-read-collaborative user-library-read"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    deviceID = getActiveDevice(sp)
    return sp, deviceID

@server.route("/")
def index():
    sp, deviceID = authenticationRoutine()
    return nowPlaying(sp)

@server.route("/chill")
def chill():
    sp, deviceID = authenticationRoutine()
    # Play my low-fi-chill lofi/hiphop radio
    play(sp,deviceID,'spotify:playlist:6jUXWvAQhTMFyPECJGJmoX')
    return redirect(url_for("index"))

@server.route("/tiger")
def tiger():
    sp, deviceID = authenticationRoutine()
    #Play Hey Tiger!
    playSong(sp,deviceID,["spotify:track:2WOM5LEDprdaJ6V6gnFK0Z"])
    return redirect(url_for("index"))

if __name__ == "__main__":
   server.run(host='0.0.0.0')

#Authentication
# scope = "user-read-private user-read-email user-read-playback-state user-modify-playback-state user-read-currently-playing app-remote-control streaming playlist-read-private playlist-read-collaborative user-library-read"
# sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
# deviceID = getActiveDevice()
heyTiger = ['spotify:track:2WOM5LEDprdaJ6V6gnFK0Z']
marching = 'spotify:playlist:0ibeKGFzDV4bbqENRNrcf8'
# nowPlaying()

# playSong(heyTiger)

# play(marching)



