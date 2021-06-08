import json
import youtube_dl
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

SP_CLIENT_ID = os.environ.get("SP_CLIENT_ID")
SP_CLIENT_SECRET = os.environ.get("SP_CLIENT_SECRET")
YT_KEY = os.environ.get("YT_KEY")

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=SP_CLIENT_ID,
                                                           client_secret=SP_CLIENT_SECRET))

# Spotify
playlist_URL = input("Spotify Playlist URL: ")
playlist_id = 'spotify:playlist:{ID}'.format(ID=playlist_URL.rsplit('/', 1)[1])
results = sp.playlist(playlist_id)

# Playlist directory
playlist_dir = dirname(os.path.realpath(__file__)) + "/" + results['name']
if not os.path.exists(playlist_dir):
    os.makedirs(playlist_dir)

# YT - Download
ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': playlist_dir + '/%(title)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        # 'preferredquality': '192',
    }],
}

# YT API
URL = "https://youtube.googleapis.com/youtube/v3/search"
params = {'key': YT_KEY,
          'part': 'snippet',
          'maxResults': 1,
          'q': 'song'}

results = results['tracks']
for idx, item in enumerate(results['items']):
    track = item['track']
    song = track['artists'][0]['name'] + " – " + track['name']

    # YT - API
    params.update({'q': song + ' lyrics'})
    response = requests.get(URL, params=params)
    videoId = response.json()['items'][0]['id']['videoId']

    # YT - Download
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(['https://www.youtube.com/watch?v=' + videoId])

