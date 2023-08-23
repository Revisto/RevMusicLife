import requests
import dotenv
import os
from spotipy.oauth2 import SpotifyOAuth
import datetime
from random import randint

dotenv.load_dotenv()



class Spotify:

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Spotify, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.base_url = "https://api.spotify.com/"
        self.AUTH_CODE = os.getenv('AUTH_CODE')
        self.CLIENT_ID = os.getenv('CLIENT_ID')
        self.CLIENT_SECRET = os.getenv('CLIENT_SECRET')
        self.sp_oauth = SpotifyOAuth(client_id=self.CLIENT_ID, client_secret=self.CLIENT_SECRET, redirect_uri=' ')
        self.refresh_access_token()

    def token_expired_decorator(func):
        def wrapper(self, *args, **kwargs):
            if self.is_access_token_expired():
                self.refresh_access_token()
            return func(self, *args, **kwargs)
        return wrapper


    def get_token_info(self):
        token_info = self.sp_oauth.get_access_token(self.AUTH_CODE)
        return token_info


    def refresh_access_token(self):
        self.token_info = self.get_token_info()
        self.ACCESS_TOKEN = self.token_info["access_token"]

    def is_access_token_expired(self):
        expires_at = self.token_info['expires_at']

        if expires_at:
            expires_at = datetime.datetime.fromtimestamp(float(expires_at))
            return expires_at <= datetime.datetime.now()

        return True

    @token_expired_decorator
    def make_request(self, endpoint, method='GET', params=None, headers=None, data=None):
        url = self.base_url + endpoint
        headers = headers or {}
        headers['Authorization'] = f'Bearer {self.ACCESS_TOKEN}'

        response = requests.request(method, url, params=params, headers=headers, json=data)
        return response.json()



    def currently_playing(self):
        response = self.make_request("v1/me/player/currently-playing")
        track_id = response['item']['id']
        track_name = response['item']['name']
        artists = [artist for artist in response['item']['artists']]
        link = response['item']['external_urls']['spotify']
        artist_names = ', '.join([artist['name'] for artist in artists])
        cover_url = response['item']['album']['images'][0]['url']
        duration_ms = response['item']['duration_ms']
        progress_ms = response['progress_ms']

        current_track_info = {
            "id": track_id,
            "track_name": track_name,
            "artists": artist_names,
            "link": link,
            "cover_url": cover_url,
            "duration_ms": duration_ms,
            "progress_ms": progress_ms
        }

        return current_track_info