import spotipy
import pprint
import itertools

from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth


class SpotipyObject:
    def __init__(self, client_id, client_secret, redirect_uri):

        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.playlist_id = ""
        self.spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=self.client_id,
                                                                 client_secret=self.client_secret,
                                                                 redirect_uri=self.redirect_uri,
                                                                 scope="playlist-modify-public playlist-modify-private user-read-currently-playing"))
        self.pp = pprint.PrettyPrinter(indent=4)

    # When user want's to create a playlist, this will automatically check if the playlist exists
    def create_playlist(self, playlist_name, description_date):
        user_id = self.get_user_id()
        if self.check_playlists(playlist_name):
            print("Playlist already exists A")
        else:
            new_playlist = self.spotify.user_playlist_create(user=user_id, name=playlist_name, public=True,
                                                             collaborative=False,
                                                             description=f"Billboard Top 100 Songs on {description_date} ")
            print("Playlist has been created")

            self.set_playlist_id(playlist_data=new_playlist, playlist_name=playlist_name)

    # Returns True or False depending if the provided playlist name is in users spotify playlist
    def check_playlists(self, playlist_name):
        users_playlists_data = self.spotify.current_user_playlists(limit=50)

        playlists_names = [item['name'] for item in users_playlists_data['items']]
        if playlist_name in playlists_names:
            # Get playlist id of existing playlist
            self.set_playlist_id(playlist_data=users_playlists_data, playlist_name=playlist_name)

            return True
        else:
            # print("playlist doesn't exists.")
            return False

    def get_user_id(self):
        return self.spotify.current_user()["id"]

    def get_song_id_list(self, songs_list):
        track_id_list = []

        for x in range(0, len(songs_list)):
            try:
                container = self.spotify.search(q=' track:' + songs_list[x], type='track', limit=2)
                track_id_list.append(container['tracks']['items'][0]['id'])
            except IndexError:
                print(f"{x} IndexError")
            except KeyError:
                print(f'{x} KeyError')
            else:
                continue

        return track_id_list

    def add_songs_to_playlist(self, id_list):
        self.spotify.playlist_replace_items(items=id_list, playlist_id=self.playlist_id)

    def set_playlist_id(self, playlist_data, playlist_name):
        try:
            self.playlist_id = playlist_data['id']
        except KeyError:
            for item in playlist_data['items']:
                if item["name"] == playlist_name:
                    print(playlist_name + " has been found")
                    self.playlist_id = item["id"]
                    break
                else:
                    print("Error, can't find id in dict playlist_data")
