import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from airium import Airium
from flask import Flask, redirect, url_for
server = Flask(__name__)

def play(sp, deviceID, contextUri):
    '''
    Plays a playlist or an album. contextUri is a single string.
    '''
    #print(("About to start playing {0} on device {1}.").format(contextUri,deviceID))
    sp.start_playback(device_id=deviceID,context_uri=contextUri)

def playSong(sp, deviceID, uris):
    '''
    Plays a song. uri must be passed as a list. Repeat is always on. 
    '''
    #print(("About to start playing {0} on device {1}.").format(uris,deviceID))
    sp.start_playback(device_id=deviceID,uris=uris)
    sp.repeat('context',deviceID)

def nowPlaying(sp):
    '''
    This returns the "<track> by <artist name>" string for the active track.
    '''
    now = sp.current_playback()
    #print(("Playing on {0}").format(now['device']['name']))
    track = now['item']['name']
    artists = now['item']['album']['artists'][0]
    returnString = ("{0} by {1}").format(track, artists['name'])
    #print(returnString)
    return returnString

def getActiveDevice(sp):
    '''
    This returns the ID of the active device if there is one.
    If there isn't, it returns the ID of the first device.
    '''
    devices = sp.devices()
    activeDevice = devices['devices'][0]['id']
    # note, idx is used to store the index of the returned tuple. 
    for idx, device in enumerate(devices['devices']):
        #print(("{0}, {1} - {2}").format(device['id'],device['name'],device['is_active']))
        if(device['is_active']):
            activeDevice = device['id']
            #print("Assigning active device.")
    return activeDevice

def getActiveDeviceName(sp):
    '''
    This returns the name of the active device is there is one.
    If there isn't, it returns an empty string.
    '''
    devices = sp.devices()
    # note, idx is used to store the index of the returned tuple. 
    for idx, device in enumerate(devices['devices']):
        #print(("{0}, {1} - {2}").format(device['id'],device['name'],device['is_active']))
        if(device['is_active']):
            return device['name']
    return ""

def authenticationRoutine():
    '''
    Authenticates with Spotify using the stored auth (or attempts to authorize manually).
    Must have a browser and user interaction to start new authentication.
    Returns the spotipy spotify object.
    '''
    scope = "user-read-private user-read-email user-read-playback-state user-modify-playback-state user-read-currently-playing app-remote-control streaming playlist-read-private playlist-read-collaborative user-library-read"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, cache_path=os.environ['CACHE_PATH']))
    deviceID = getActiveDevice(sp)
    return sp, deviceID

@server.route("/")
def index():
    '''
    The home page. html generated in here, could probably be more elegant and use Flask for real.
    '''
    sp, deviceID = authenticationRoutine()
    playingNow = sp.current_playback()
    devices = sp.devices()
    activeDeviceName = getActiveDeviceName(sp)
    a = Airium()
    a('<!DOCTYPE html>')
    with a.html(lang="pl"):
        with a.head():
            a.meta(charset="utf-8")
            a.link(href="https://www.w3schools.com/w3css/4/w3.css", rel='stylesheet', type='text/css')
            a.link(href="static/font-awesome-4.7.0/css/font-awesome.min.css", rel='stylesheet', type='text/css')
            a.link(href='static/home.css?q=33', rel='stylesheet', type='text/css')
            a.title(_t="Kiddo-Lullaby Home")
        with a.body():
            with a.h1(id="title", klass='title_header'):
                if activeDeviceName == "":
                    a(("Kiddo Lullaby"))
                else:
                    a(("Kiddo Lullaby on {0}").format(activeDeviceName))
            #This means that there is not an active device ready to play.
            if playingNow is not None:
                with a.div(klass="now-playing-card"):
                    with a.h3(id="id23409231", klass='main-header'):
                        a("Now Playing")
                    a.img(src=playingNow['item']['album']['images'][1]['url'], alt=nowPlaying(sp))
                    with a.p(id="idNowPlaying", klass='now-playing'):
                        a(("Playing {0}").format(nowPlaying(sp)))
                    with a.div():
                        if playingNow['is_playing']:
                            with a.a(href="/pause", klass="w3-btn"):
                                a.i(klass="fa fa-pause fa-4x")
                        else:
                            with a.a(href="/resume", klass="w3-btn"):
                                a.i(klass="fa fa-play fa-4x")
                        with a.a(href='/tooLoud', klass="w3-btn"):
                            a.i(klass="fa fa-volume-down fa-4x")
                        with a.a(href='/tooQuiet', klass="w3-btn"):
                            a.i(klass="fa fa-volume-up fa-4x")
            with a.div(klass="button-box"):
                with a.ul(klass="linked-list"):
                    with a.li():
                        with a.a(href='/tiger', klass="w3-btn w3-block w3-indigo button-link"):
                            a("Hey Tiger! by Robbie Williams")
                    with a.li():
                        with a.a(href='/abc', klass="w3-btn w3-block w3-indigo button-link"):
                            a("Abc Song by Wheels on the Bus")
                    with a.li():
                        with a.a(href="/twinkeTwinkle", klass="w3-btn w3-block w3-indigo button-link"):
                            a("Twinkle Twinkle Little Star by Super Simple Songs")
                    with a.li():
                        with a.a(href="/sleepyPiano", klass="w3-btn w3-block w3-indigo button-link"):
                            a("Sleepy Piano Playlist")
                    with a.li():
                        with a.a('a', href='/chill', klass="w3-btn w3-block w3-indigo button-link"):
                            a("Chill Music Playlist")
            # This is for debugging devices.
            #
            #  if devices is not None:
            #     with a.div():
            #         with a.ul():
            #             for idx, device in enumerate(devices['devices']):
            #                 with a.li():
            #                     a(("{0}, {1} - {2}").format(device['id'],device['name'],device['is_active']))

            # This is for debugging Now PLaying.
            #
            # with a.div():
            #     a(("is_playing: {0}").format(playingNow['is_playing']))
            
    html = str(a)
    return html

@server.route("/chill")
def chill():
    '''
    Play Low-Fi - Chill Lofi / Hip Hop Radio - Lo Fi Beats to Chill, Study, Sleep to, 3:30 a.m. Playlist
    '''
    sp, deviceID = authenticationRoutine()
    play(sp,deviceID,'spotify:playlist:6jUXWvAQhTMFyPECJGJmoX')
    return redirect(url_for("index"))

@server.route("/tiger")
def tiger():
    '''
    Play Hey Tiger! by Robbie Williams
    '''
    sp, deviceID = authenticationRoutine()
    playSong(sp,deviceID,["spotify:track:2WOM5LEDprdaJ6V6gnFK0Z"])
    return redirect(url_for("index"))

@server.route("/abc")
def abc():
    '''
    Play Abc Song by Wheels on the Bus
    '''
    sp, deviceID = authenticationRoutine()
    playSong(sp,deviceID,["spotify:track:3kd7YGbHbuDQzASBgtVt3h"])
    return redirect(url_for("index"))

@server.route("/sleepyPiano")
def sleepyPiano():
    '''
    Play Sleepy Piano Playlist
    '''
    sp, deviceID = authenticationRoutine()
    play(sp,deviceID,"spotify:playlist:37i9dQZF1DX03b46zi3S82")
    return redirect(url_for("index"))

@server.route("/twinkeTwinkle")
def twinkleTwinkle():
    '''
    Play Twinkle Twinkle Little Star by Super Simple Songs
    '''
    sp, deviceID = authenticationRoutine()
    playSong(sp,deviceID,["spotify:track:3N6kzbnfpTPB5J9NAGc1rU"])
    return redirect(url_for("index"))

@server.route("/tooLoud")
def tooLoud():
    '''
    Sets audio to 25. This is generally below the volume threshold for baby monitor.
    '''
    sp, deviceID = authenticationRoutine()
    sp.volume(25, deviceID)
    return redirect(url_for("index"))

@server.route("/tooQuiet")
def tooQuiet():
    '''
    Sets audio to 50. This is above threshold for baby monitor, but is more immersive.
    '''
    sp, deviceID = authenticationRoutine()
    sp.volume(50, deviceID)
    return redirect(url_for("index"))

@server.route("/pause")
def pause():
    '''
    Pause the active playing track.
    '''
    sp, deviceID = authenticationRoutine()
    sp.pause_playback(deviceID)
    return redirect(url_for("index"))

@server.route("/resume")
def resume():
    '''
    Resume the track on the device retrieved from the nowPlaying().
    '''
    sp, deviceID = authenticationRoutine()
    sp.start_playback()
    return redirect(url_for("index"))

if __name__ == "__main__":
   server.run(host='0.0.0.0', debug=True)
