import requests
import dotenv
import os
from spotipy.oauth2 import SpotifyOAuth
import datetime
import schedule
import time
import threading


dotenv.load_dotenv()

class Spotify:

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Spotify, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.base_url = "https://api.spotify.com/"
        self.CLIENT_ID = os.getenv('CLIENT_ID')
        self.CLIENT_SECRET = os.getenv('CLIENT_SECRET')
        self.SCOPE = "ugc-image-upload user-read-playback-state user-modify-playback-state user-read-currently-playing app-remote-control streaming playlist-read-private playlist-read-collaborative playlist-modify-private playlist-modify-public user-follow-modify user-follow-read user-read-playback-position user-top-read user-read-recently-played user-library-modify user-library-read user-read-email user-read-private"
        # self.CACHE_PATH = "spotify_cache.txt" # if testing and debugging spotify.py file
        self.CACHE_PATH = "listening_to/api/spotify_cache.txt"
        self.sp_oauth = SpotifyOAuth(client_id=self.CLIENT_ID, client_secret=self.CLIENT_SECRET, redirect_uri='http://localhost:8080', cache_path=self.CACHE_PATH)
        self.set_token_info()
        # Run Spotify Access Code Refresher Cronjob In Background
        self.spotify_refresher_thread = threading.Thread(target=self.run_access_code_refresher)
        self.spotify_refresher_thread.daemon = True  # Set the thread as daemon to exit when the main thread exits
        self.spotify_refresher_thread.start()  # Start the cron job thread


    def is_access_token_about_to_expire_decorator(func):
        def wrapper(self, *args, **kwargs):
            if self.is_access_token_about_to_expire():
                self.refresh_access_token()
            return func(self, *args, **kwargs)
        return wrapper


    def run_access_code_refresher(self):
        schedule.every(50).minutes.do(self.refresh_access_token)

        while True:
            schedule.run_pending()
            time.sleep(1)

    def get_token_info(self):
        token_info = self.sp_oauth.get_cached_token()
        return token_info
    
    def set_token_info(self):
        token_info = self.get_token_info()
        self.TOKEN_INFO = token_info["refresh_token"]
        self.EXPIRES_AT = token_info["expires_at"]
        self.ACCESS_TOKEN = token_info["access_token"]
        self.REFRESH_TOKEN = token_info["refresh_token"]
        return True

    def refresh_access_token(self):
        self.sp_oauth.refresh_access_token(self.REFRESH_TOKEN)
        self.set_token_info()

    def is_access_token_about_to_expire(self):
        expires_at = self.EXPIRES_AT

        if expires_at:
            expires_at -= 60
            expires_at = datetime.datetime.fromtimestamp(float(expires_at))
            return expires_at <= datetime.datetime.now()

        return True

    @is_access_token_about_to_expire_decorator
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