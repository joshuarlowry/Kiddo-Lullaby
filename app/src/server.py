import os
import spotipy
import json
from airium import Airium
from flask import Flask, redirect, url_for, request
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
    returnString = ""
    try:
        track = now['item']['name']
        artists = now['item']['album']['artists'][0]
        returnString = ("{0} by {1}").format(track, artists['name'])
    except:
        returnString = "UNKNOWN"
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

def getTrack(sp, track_id):
    return sp.track(track_id)
def getPlaylist(sp, playlist_id):
    return sp.playlist(playlist_id)

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

def getAlbumArt(playingNow):
    '''
    return the medium album art url
    '''
    art = ""
    try:
        art = playingNow['item']['album']['images'][0]['url']
    except:
        art = ""
    
    return art
def getAlbumArtMedium(playingNow):
    '''
    return the medium album art url
    '''
    art = ""
    try:
        art = playingNow['album']['images'][1]['url']
    except:
        art = ""
    return art

def getAlbumArtSmall(playingNow):
    '''
    return the small album art url
    '''
    art = ""
    try:
        art = playingNow['album']['images'][2]['url']
    except:
        art = ""
    
    return art

def authenticationRoutine():
    '''
    Authenticates with Spotify using the stored auth (or attempts to authorize manually).
    Returns the auth manager
    '''
    scope = "user-read-private user-read-email user-read-playback-state user-modify-playback-state user-read-currently-playing app-remote-control streaming playlist-read-private playlist-read-collaborative user-library-read user-read-recently-played"
    return spotipy.oauth2.SpotifyOAuth(scope=scope, show_dialog=True, cache_path="./config")

def checkAuthentication():
    '''
    Make sure we have a valid cached token otherwise redirect back to /.
    Returns the authorized spotipy object
    '''
    auth_manager = authenticationRoutine()
    if not auth_manager.get_cached_token():
        return redirect('/')
    return spotipy.Spotify(auth_manager=auth_manager)

@server.route("/callback")
def callback():
    '''
    Spotify returns you to here for auth. 
    You must have /callback at the end of your SPOTIPY_REDIRECT_URI
    '''
    auth_manager = authenticationRoutine()
    auth_manager.get_access_token(code=request.args.get("code"),as_dict=False,check_cache=True)
    return redirect('/')

@server.route("/")
def index():
    '''
    Try to authenticate, but if the cache is missing then provide sign-in link.
    Otherwise, load the whole interface :)
    '''
    dbug=""
    auth_manager = authenticationRoutine()
    if not auth_manager.get_cached_token():
        auth_url = auth_manager.get_authorize_url()
        a = Airium()
        a('<!DOCTYPE html>')
        with a.html(lang="pl"):
            with a.head():
                a.meta(charset="utf-8")
                a.link(href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta2/dist/css/bootstrap.min.css", rel="stylesheet", integrity="sha384-BmbxuPwQa2lc/FVzBcNJ7UAyJxM6wuqIj61tLrc4wSX0szH/Ev+nYRRuWlolflfl", crossorigin="anonymous")
                a.link(href="static/font-awesome-4.7.0/css/font-awesome.min.css", rel='stylesheet', type='text/css')
                a.link(href='static/home.css?q=33', rel='stylesheet', type='text/css')
                a.title(_t="Kiddo-Lullaby Home")
            with a.body():
                with a.a(href=auth_url, klass="btn btn-primary"):
                    a.h2(_t="Sign in")
        html = str(a)
        html += dbug
        return html
    
    '''
    The home page. html generated in here, could probably be more elegant and use Flask for real.
    '''
    playlist = {
        "spotify:track:2WOM5LEDprdaJ6V6gnFK0Z":"track",
        "spotify:track:3kd7YGbHbuDQzASBgtVt3h":"track",
        "spotify:track:3N6kzbnfpTPB5J9NAGc1rU":"track",
        "spotify:playlist:6jUXWvAQhTMFyPECJGJmoX":"playlist",
        "spotify:playlist:37i9dQZF1DX03b46zi3S82":"playlist",
        "spotify:playlist:37i9dQZF1E8U54MaF9DPlR":"playlist"
    }

    sp = spotipy.Spotify(auth_manager=auth_manager)
    deviceID = getActiveDevice(sp)
    playingNow = sp.current_playback()
    devices = sp.devices()
    activeDeviceName = getActiveDeviceName(sp)
    recentlyPlayed = sp.current_user_recently_played()

    a = Airium()
    a('<!DOCTYPE html>')
    with a.html(lang="pl"):
        with a.head():
            a.meta(charset="utf-8")
            a.link(href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta2/dist/css/bootstrap.min.css", rel="stylesheet", integrity="sha384-BmbxuPwQa2lc/FVzBcNJ7UAyJxM6wuqIj61tLrc4wSX0szH/Ev+nYRRuWlolflfl", crossorigin="anonymous")
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
                    a.img(src=getAlbumArt(playingNow), alt=nowPlaying(sp))
                    with a.p(id="idNowPlaying", klass='now-playing'):
                        a(("Playing {0}").format(nowPlaying(sp)))
                    with a.div():
                        if playingNow['is_playing']:
                            with a.a(href="/pause", klass="btn btn-dark"):
                                a.i(klass="fa fa-pause fa-4x")
                        else:
                            with a.a(href="/resume", klass="btn btn-dark"):
                                a.i(klass="fa fa-play fa-4x")
                        with a.a(href='/tooLoud', klass="btn btn-dark"):
                            a.i(klass="fa fa-volume-down fa-4x")
                        with a.a(href='/tooQuiet', klass="btn btn-dark"):
                            a.i(klass="fa fa-volume-up fa-4x")
            with a.div():
                with a.ul(klass="list-group"):
                    with a.li():
                        for (id, typ) in playlist.items():
                                    if typ == 'playlist':
                                        spData = getPlaylist(sp, id)
                                        albumArt = spData['images'][0]['url']
                                    elif typ == 'track':
                                        spData = getTrack(sp, id)
                                        albumArt = getAlbumArtMedium(spData)
                                    with a.a(href='/'+typ+'/'+spData['id'], klass="list-group-item list-group-item-action list-group-item-dark flex-column align-items-start"):
                                        with a.div(klass="row g-0"):
                                            with a.div(klass="col-md-3"):
                                                a.img(src=albumArt, alt=spData['name'], width="200px")
                                            with a.div(klass="col-md-8"):
                                                with a.div(klass="card-body"):
                                                    a.h2(_t=spData['name'], klass="card-title")
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
    html += dbug
    return html

@server.route("/playlist/<id>")
def playlist(id):
    '''
    Enables you to play a playlist directly using the spotify ID (enables ad-hoc playlists instead of hard routes of /chill /tiger etc.)
    localhost:5000/playlist/37i9dQZF1E8U54MaF9DPlR
    '''
    sp = checkAuthentication()
    deviceID = getActiveDevice(sp)
    play(sp, deviceID,'spotify:playlist:'+id)
    return redirect(url_for("index"))

@server.route("/track/<id>")
def track(id):
    '''
    Enables you to play a specific song directly using the spotify ID
    localhost:5000/track/2WOM5LEDprdaJ6V6gnFK0Z
    '''
    sp = checkAuthentication()
    deviceID = getActiveDevice(sp)
    playSong(sp, deviceID, ['spotify:track:'+id])
    return redirect(url_for("index"))

@server.route("/chill")
def chill():
    '''
    Play Low-Fi - Chill Lofi / Hip Hop Radio - Lo Fi Beats to Chill, Study, Sleep to, 3:30 a.m. Playlist
    '''
    sp = checkAuthentication()
    deviceID = getActiveDevice(sp)
    play(sp,deviceID,'spotify:playlist:6jUXWvAQhTMFyPECJGJmoX')
    return redirect(url_for("index"))

@server.route("/tiger")
def tiger():
    '''
    Play Hey Tiger! by Robbie Williams
    '''
    sp = checkAuthentication()
    deviceID = getActiveDevice(sp)
    playSong(sp,deviceID,["spotify:track:2WOM5LEDprdaJ6V6gnFK0Z"])
    return redirect(url_for("index"))

@server.route("/abc")
def abc():
    '''
    Play Abc Song by Wheels on the Bus
    '''
    sp = checkAuthentication()
    deviceID = getActiveDevice(sp)
    playSong(sp,deviceID,["spotify:track:3kd7YGbHbuDQzASBgtVt3h"])
    return redirect(url_for("index"))

@server.route("/sleepyPiano")
def sleepyPiano():
    '''
    Play Sleepy Piano Playlist
    '''
    sp = checkAuthentication()
    deviceID = getActiveDevice(sp)
    play(sp,deviceID,"spotify:playlist:37i9dQZF1DX03b46zi3S82")
    return redirect(url_for("index"))

@server.route("/twinkeTwinkle")
def twinkleTwinkle():
    '''
    Play Twinkle Twinkle Little Star by Super Simple Songs
    '''
    sp = checkAuthentication()
    deviceID = getActiveDevice(sp)
    playSong(sp,deviceID,["spotify:track:3N6kzbnfpTPB5J9NAGc1rU"])
    return redirect(url_for("index"))

@server.route("/tooLoud")
def tooLoud():
    '''
    Sets audio to 25. This is generally below the volume threshold for baby monitor.
    '''
    sp = checkAuthentication()
    deviceID = getActiveDevice(sp)    
    sp.volume(25, deviceID)
    return redirect(url_for("index"))

@server.route("/tooQuiet")
def tooQuiet():
    '''
    Sets audio to 50. This is above threshold for baby monitor, but is more immersive.
    '''
    sp = checkAuthentication()
    deviceID = getActiveDevice(sp)    
    sp.volume(50, deviceID)
    return redirect(url_for("index"))

@server.route("/pause")
def pause():
    '''
    Pause the active playing track.
    '''
    sp = checkAuthentication()
    deviceID = getActiveDevice(sp)    
    sp.pause_playback(deviceID)
    return redirect(url_for("index"))

@server.route("/resume")
def resume():
    '''
    Resume the track on the device retrieved from the nowPlaying().
    '''
    sp = checkAuthentication()
    deviceID = getActiveDevice(sp)    
    sp.start_playback()
    return redirect(url_for("index"))

if __name__ == "__main__":
   server.run(host='0.0.0.0', debug=True)
