import dotenv
import os
from spotipy.oauth2 import SpotifyOAuth


custom_cache_path = 'spotify_cache.txt'
dotenv.load_dotenv()

# Create a new SpotifyOAuth object
sp_oauth = SpotifyOAuth(
    client_id=os.getenv('CLIENT_ID'),
    client_secret=os.getenv('CLIENT_SECRET'),
    redirect_uri='http://localhost:8080',
    scope='ugc-image-upload user-read-playback-state user-modify-playback-state user-read-currently-playing app-remote-control streaming playlist-read-private playlist-read-collaborative playlist-modify-private playlist-modify-public user-follow-modify user-follow-read user-read-playback-position user-top-read user-read-recently-played user-library-modify user-library-read user-read-email user-read-private',
    cache_path=custom_cache_path
)


# Obtain the authorization URL
auth_url = sp_oauth.get_authorize_url()

# Prompt the user to authorize the application and retrieve the authorization code
print(f"Please authorize the application by clicking the following link:\n{auth_url}")
auth_code = input("Enter the authorization code: ")

# Exchange the authorization code for an access token
token_info = sp_oauth.get_access_token(auth_code)

# write spotify cache
sp_oauth.refresh_access_token(token_info['refresh_token'])
