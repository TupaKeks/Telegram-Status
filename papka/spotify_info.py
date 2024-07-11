import urllib

import requests
import json

from pprint import pprint
from get_token import token

SPOTIFY_GET_CURRENT_TRACK_URL = 'https://api.spotify.com/v1/me/player/currently-playing'
token_data, user_data = token()
ACCESS_TOKEN = token_data['access_token']


def main_access_token():
    return ACCESS_TOKEN


def get_refresh():
    token_url = "https://accounts.spotify.com/api/token"

    token_params = {
        "grant_type": "refresh_token",
        "refresh_token": token_data['refresh_token'],
        "client_id": user_data[0],
        "client_secret": user_data[1],
    }
    response = requests.post(token_url, data=token_params)
    return response.json()['access_token']


def get_current_track(access_token):
    response = requests.get(
        SPOTIFY_GET_CURRENT_TRACK_URL,
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )
    json_resp = response.json()

    track_id = json_resp['item']['id']
    track_name = json_resp['item']['name']
    artists = [artist for artist in json_resp['item']['artists']]
    status = json_resp['is_playing']

    link = json_resp['item']['external_urls']['spotify']

    artist_names = ', '.join([artist['name'] for artist in artists])

    current_track_info = {
        "id": track_id,
        "track_name": track_name,
        "artists": artist_names,
        "link": link,
        "is_playing": status
    }

    return current_track_info


def main(access_token, current_track_id):
    current_track_info = get_current_track(access_token)

    if current_track_info['id'] != current_track_id:
        pprint(current_track_info, indent=4)
        return current_track_info
    return access_token


if __name__ == '__main__':
    main(access_token=ACCESS_TOKEN, current_track_id=None)
