# Current Status
The app runs in a docker container, visiting / will show you the current song. 
Visiting /chill will play a Low-Fi-Chill playlist and redirect you to /. 

# Kiddo-Lullaby
This app will help parents (and grandparents) manage music in the kid's rooms specifically targeted at nap/bed time. This includes triggering specific playlists or songs and changing the volume. There may be other uses. 

*I feel like I should tell you that this is probably something you want to run on a local server and not out on the web. If it is discovered, someone could wreak havoc on you by changing your music and stuff.*

There is a complexity around the Spotify/Amazon/Echo setup that makes control complicated, especially when you want to play separate songs in different areas of the home at the same time. The Echo can only be linked to a single Amazon account and the Amazon account to a single Spotify account. A single spotify account has only one play "seat". This means that you may require multiple Spotify and Amazon accounts. This will also prevent you from controlling echo devices in different areas of your home. The Spotify account doesn't allow you to easily switch between these accounts to control music. 

So, if for example, you want to have one set of lullabies playing in room A and another set playing in room B you will need two Amazon Accounts, two (or more) Echos, and two Spotify Accounts. We will call each combination of Amazon Account, Echo, and Spotify Account linked a "zone". This app will hopefully allow you to configure a "page" for these zones for you to control. 

## Assumptions
You must have a Spotify account, Amazon account, and an Echo. They must be linked.

## Setup
First, setup your local environment variables on your machine. They will be passed during the docker run command. 
SPOTIPY_CLIENT_ID
SPOTIPY_CLIENT_SECRET
SPOTIPY_REDIRECT_URI = http://localhost:5000

__Don't forget to set up the callback url in your Spotify account.__

Authentication setup should be run using the following command:
```
python setup.py
```
If you have not authenticated before your browser will open to authenticate
Once authentication is completed, the .cache file will contain your key.
Build your docker container, the .cache file will be copied
```
docker build -t kiddolullaby .
```

Run your docker container
```
docker run -e SPOTIPY_CLIENT_ID -e SPOTIPY_CLIENT_SECRET -e SPOTIPY_REDIRECT_URI -p 5000:5000 kiddolullaby
```


# Dev Notes
During dev, I'm running this string of commands between changes. Contact me if you know of a better way.
```
docker stop kiddoDev; docker build -t kiddolullaby .; docker rm kiddoDev;  docker run -e SPOTIPY_CLIENT_ID -e SPOTIPY_CLIENT_SECRET -e SPOTIPY_REDIRECT_URI -p 5000:5000 --name kiddoDev kiddolullaby
kiddoDev
```

# Attributions
This project is built on top of Spotipy. https://github.com/plamere/spotipy
