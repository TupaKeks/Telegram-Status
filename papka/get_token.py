import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
import os

CLIENT_ID = "id"
CLIENT_SECRET = "sec"

birdy_uri = 'spotify:artist:2WX2uTcsvV5OnS0inACecP'
spotify = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                                                  client_secret=CLIENT_SECRET,
                                                                  redirect_uri="https://localhost:8888/callback",
                                                                  scope='user-read-currently-playing'))


def token():
    results = spotify.artist_albums(birdy_uri, album_type='album')

    with open('.cache', 'r', encoding='utf-8') as file:
        data = json.load(file)

    print(f"{data}")

    return data, [[CLIENT_ID], [CLIENT_SECRET]]


if __name__ == '__main__':
    token()
