import os
import dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth


dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

RECENTLY_ADDED = "3BZP1mB69SWnSNCy4nfxXX"

scope = """ugc-image-upload, 
user-read-recently-played, user-top-read, user-read-playback-position,
user-read-playback-state, user-modify-playback-state, user-read-currently-playing,
app-remote-control, streaming,
playlist-modify-public, playlist-modify-private,
playlist-read-private, playlist-read-collaborative,
user-follow-modify, user-follow-read,
user-library-modify, user-library-read,
user-read-email, user-read-private"""

# Finds the most recently added albums in a shitty loop since I don't know how to parse a larger album data set yet
def find_recently_saved_albums(amount, offset):
    recently_saved_albums = []
    for i in range(0,amount):
        new_album = sp.current_user_saved_albums(limit = 1, offset = offset + i, market = "from_token")
        recently_saved_albums.append(new_album)
    return recently_saved_albums

# Parses album data to get track uris
def get_track_uris_from_album(album):
    track_uris = []
    total = album['items'][0]['album']['total_tracks']
    
    for i in range(0,total):
        track = album['items'][0]['album']['tracks']['items'][i]['uri']
        track_uris.append(track)   

    return track_uris


# Parses album data to get total songs
def get_amount_of_songs_in_album(album):
    return album['items'][0]['album']['total_tracks']

# Adds the most recently saved albums to a playlist
def replace_recently_added_playlist(amount, offset):
    RECENTLY_ADDED = "3BZP1mB69SWnSNCy4nfxXX"
    recently_added_albums = find_recently_saved_albums(amount, offset)
    track_uris = []
    sp.playlist_replace_items(RECENTLY_ADDED, track_uris)
    for album in recently_added_albums:
        track_uris = track_uris + get_track_uris_from_album(album)
    
    size = len(track_uris)
    
    print(size)
    split_track_uris = split_list_below_100(track_uris, [])
    for tracks in split_track_uris:
        sp.playlist_add_items(RECENTLY_ADDED, tracks)

# Splits a larger list of tracks into a smaller lists with max size of 100
def split_list_below_100(tracks, storage):
    length = len(tracks)
    if(length <= 100):
        storage.append(tracks)
        return storage

    else:
        storage = split_list_below_100(tracks[:100], storage)
        storage = split_list_below_100(tracks[100:], storage)
        return storage

# Set environment to most recent album
def reset_most_recent():
    album = find_recently_saved_albums(1, 0)
    album_id = album[0]['items'][0]['album']['uri']
    os.environ['MOST_RECENT_ALBUM'] = album_id
    dotenv.set_key(dotenv_file, 'MOST_RECENT_ALBUM', os.environ['MOST_RECENT_ALBUM'])

# Check newest most recent album against stored most recent album. Returns True if there is a new album, false otherwise
def check_if_new_saved_album():
    album = find_recently_saved_albums(1, 0)
    album_id = album[0]['items'][0]['album']['uri']

    if (album_id != os.getenv["MOST_RECENT_ALBUM"]):
        return True
    else:
        return False

# Finds how many albums have been added since latest check
def count_new_albums():
    dotenv_file = dotenv.find_dotenv()
    dotenv.load_dotenv(dotenv_file)

    counter = 0;
    while (album != os.getenv["MOST_RECENT_ALBUM"]):
        album = find_recently_saved_albums(1, counter)
        counter += 1
    
    return counter

# Update everything playlist
def update_everything():
    EVERYTHING = "3ZqjihXebfS117lF9bi9FI"
    new_albums = find_recently_saved(count_new_albums(), 0)
    track_uris = []
    for album in new_albums:
        track_uris = track_uris + get_track_uris_from_album(album)
    
    split_track_uris = split_list_below_100(track_uris, [])
    for tracks in split_track_uris.reverse:
        sp.playlist_add_items(EVERYTHING, tracks)

# Checks if new albums have been added and updates playlists
def update():
    dotenv_file = dotenv.find_dotenv()
    dotenv.load_dotenv(dotenv_file)

    if check_if_new_saved_album():
        update_everything()
        replace_recently_added_playlist(50, 0)
        reset_most_recent()

# query all artist albums crosscheck against saved playlists to make new playlist. change name
# makeds most recently added album env variable
# checks every minute whether most recently added = above album and if not runs replace_recently_added and add to everything functionsz


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
# replace_recently_added_playlist(50, 0)