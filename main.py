import os
from datetime import datetime as dt
from spotify_time_machine import SpotifyTimeMachine
from spotipy_object import SpotipyObject

SPOTIFY_CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.environ.get("REDIRECT_URI")

TODAYS_DATE = dt.today()
URL = "https://www.billboard.com/charts/hot-100/"

time_machine = SpotifyTimeMachine(url=URL,todays_date=TODAYS_DATE)
spotipy = SpotipyObject(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET, redirect_uri=REDIRECT_URI)

time_machine.get_input()
time_machine.get_rankings_info()


playlist_description_date = f"{time_machine.y_m_d_list[0]}/{time_machine.y_m_d_list[1]}/{time_machine.y_m_d_list[2]}"

playlist_name = time_machine.get_new_playlist_name()

spotipy.create_playlist(playlist_name=playlist_name, description_date=playlist_description_date)

song_id_list = spotipy.get_song_id_list(songs_list=time_machine.get_songs_list())

spotipy.add_songs_to_playlist(id_list=song_id_list)

