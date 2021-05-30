import json
import youtube_dl
import requests
import os

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="b523045ad2864a499929f5f271e8ab44",
                                                           client_secret="b6b26357a43a483ab3ecc67bff25ee88"))
# https://open.spotify.com/playlist/3WOcIUMI1fRw6f1ONlro2n?si=9dd37a52e9e14a61
# Spotify
playlist_id = 'spotify:playlist:3WOcIUMI1fRw6f1ONlro2n'
results = sp.playlist(playlist_id)
# Playlist directory
playlist_dir = os.path.dirname(os.path.realpath(__file__)) + "/" + results['name']
# playlist_dir = '/media/raminduw/Entertainment' + results['name']
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
params = {'key': 'AIzaSyDPVRYosEjLyNN7VOuBW9Cihnh8ztoq5rk',
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

# results = sp.search(q='Somebody to Love', limit=20)
# for idx, track in enumerate(results['tracks']['items']):
#     print(idx, track['name'])
