# Current Status
The app runs in a docker container, visiting / will show you the current song and a premade list of potential things to play (focused on my need for now). 

Lots of styling enhancements.
There are now icon buttons for play/pause and only one is shown based on the context of the music. 
There are buttons for the tracks now.

Current Screenshot of the app.

<img src="https://github.com/joshuarlowry/Kiddo-Lullaby/blob/main/images/Screenshot1.png" width="250px" alt="Screenshot showing the album art, Play/Pause button, Volume Low and High, as well as a list of playlists as buttons."/>

Note, Strange things happen if the device is suddenly unavailable. Will need to think about that. 

# Kiddo-Lullaby
This app will help parents (and grandparents) manage music in the kid's rooms specifically targeted at nap/bed time. This includes triggering specific playlists or songs and changing the volume. There may be other uses. 

*I feel like I should tell you that this is probably something you want to run on a local server and not out on the web. If it is discovered, someone could wreak havoc on you by changing your music and stuff.*

There is a complexity around the Spotify/Amazon/Echo setup that makes control complicated, especially when you want to play separate songs in different areas of the home at the same time. The Echo can only be linked to a single Amazon account and the Amazon account to a single Spotify account. A single spotify account has only one play "seat". This means that you may require multiple Spotify and Amazon accounts. This will also prevent you from controlling echo devices in different areas of your home. The Spotify account doesn't allow you to easily switch between these accounts to control music. 

So, if for example, you want to have one set of lullabies playing in room A and another set playing in room B you will need two Amazon Accounts, two (or more) Echos, and two Spotify Accounts. We will call each combination of Amazon Account, Echo, and Spotify Account linked a "zone". This app will hopefully allow you to configure a "page" for these zones for you to control. 

## Assumptions
For the core purpose of this app, you must have a Spotify account.

The Amazon account, and an Echo are optional and there is no code to access them directly in here as Spotify manages that. They must be linked and the code assumes you want to play on the first device in the list. I created a dedicated Amazon/Spotify account and linked the Echo. This means that that spotify account only sees one device. 

For each Spotify account, I plan to run a separate docker container and Spotify app api key, unless I find some way to have multiple linked accounts to a single app. 

## Setup
Create an environment file called kiddoDev.env containing the following variables. It is referenced by the docker-compose-dev.yml.

* SPOTIPY_CLIENT_ID
* SPOTIPY_CLIENT_SECRET
* SPOTIPY_REDIRECT_URI = http://localhost:5000/callback

> SPOTIPY_REDIRECT_URI must end in /callback for this server to work.
> 
> Don't forget to set up the callback url in your Spotify account. 

The first time you open the server in the browser it will prompt you to log in. At this moment that is not saved between docker sessions (so reboots are a little painful if you have multiples running).

Build
```
docker-compose -f docker-compose-dev.yml --verbose build
```

Turn it on
```
docker-compose -f docker-compose-dev.yml up -d
```

Create other yml files and env files for each environment. 


# Dev Notes

Everything up to this point is incorporated above. 

# Attributions and dependencies
This project is built on top of Spotipy. https://github.com/plamere/spotipy
It is also using Flask. https://flask.palletsprojects.com/en/1.1.x/
We are now using FontAwesome. https://fontawesome.com
Some styling help on buttons from w3Schools. https://www.w3schools.com/w3css/w3css_buttons.asp 
