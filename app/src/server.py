import spotipy
from spotipy.oauth2 import SpotifyOAuth
from airium import Airium
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
    playingNow = sp.current_playback()
    devices = sp.devices()
    a = Airium()
    a('<!DOCTYPE html>')
    with a.html(lang="pl"):
        with a.head():
            a.meta(charset="utf-8")
            a.title(_t="Kiddo-Lullaby Home")
        with a.body():
            if playingNow is not None:
                with a.h3(id="id23409231", klass='main_header'):
                    a("Now Playing")
                with a.div():
                    a.img(src=playingNow['item']['album']['images'][1]['url'], alt=nowPlaying(sp))
                with a.p(id="idNowPlaying", klass='now_playing'):
                    a(nowPlaying(sp))
            with a.div():
                with a.ul():
                    with a.li():
                        with a.a(href='/tiger'):
                            a("Play Hey Tiger! by Robbie Williams")
                    with a.li():
                        with a.a(href='/abc'):
                            a("Play Abc Song by Wheels on the Bus")
                    with a.li():
                        with a.a(href="/twinkeTwinkle"):
                            a("Play Twinkle Twinkle Little Star by Super Simple Songs")
                    with a.li():
                        with a.a(href="/sleepyPiano"):
                            a("Play Sleepy Piano Playlist")
                    with a.li():
                        with a.a('a', href='/chill'):
                            a("Play Chill Music Playlist")
            with a.div():
                with a.ul():
                    for idx, device in enumerate(devices['devices']):
                        with a.li():
                            a(("{0}, {1} - {2}").format(device['id'],device['name'],device['is_active']))
            
    html = str(a)
    return html

@server.route("/chill")
def chill():
    sp, deviceID = authenticationRoutine()
    # Play my low-fi-chill lofi/hiphop radio
    play(sp,deviceID,'spotify:playlist:6jUXWvAQhTMFyPECJGJmoX')
    return redirect(url_for("index"))

@server.route("/tiger")
def tiger():
    sp, deviceID = authenticationRoutine()
    #Play Hey Tiger! by Robbie Williams
    playSong(sp,deviceID,["spotify:track:2WOM5LEDprdaJ6V6gnFK0Z"])
    return redirect(url_for("index"))

@server.route("/abc")
def abc():
    sp, deviceID = authenticationRoutine()
    #Play Abc Song by Wheels on the Bus
    playSong(sp,deviceID,["spotify:track:3kd7YGbHbuDQzASBgtVt3h"])
    return redirect(url_for("index"))

@server.route("/sleepyPiano")
def sleepyPiano():
    sp, deviceID = authenticationRoutine()
    #Play Sleepy Piano Playlist
    play(sp,deviceID,"spotify:playlist:37i9dQZF1DX03b46zi3S82")
    return redirect(url_for("index"))

@server.route("/twinkeTwinkle")
def twinkleTwinkle():
    sp, deviceID = authenticationRoutine()
    #Play Twinkle Twinkle Little Star by Super Simple Songs
    playSong(sp,deviceID,["spotify:album:2T9jkpdjKDjzoOqPfaCAMu"])
    return redirect(url_for("index"))

if __name__ == "__main__":
   server.run(host='0.0.0.0')
