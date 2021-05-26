import spotipy
from spotipy.oauth2 import SpotifyOAuth

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

def find_recently_saved_albums(amount, offset):
    recently_saved_albums = []
    for i in range(offset,amount + offset):
        new_album = sp.current_user_saved_albums(limit = 1, offset = i, market = "from_token")
        recently_saved_albums.append(new_album)
    return recently_saved_albums

def get_track_uris_from_album(album):
    track_uris = []
    total = album['items'][0]['album']['total_tracks']
    
    for i in range(0,total):
        track = album['items'][0]['album']['tracks']['items'][i]['uri']
        track_uris.append(track)   

    return track_uris

def get_amount_of_songs_in_album(album):
    return album['items'][0]['album']['total_tracks']

def replace_recently_added_playlist(playlist_id, amount, offset):
    recently_added_albums = find_recently_saved_albums(amount, offset)
    track_uris = []
    sp.playlist_replace_items(playlist_id, track_uris)
    for album in recently_added_albums:
        track_uris = get_track_uris_from_album(album) + track_uris
        
    for track in reversed(track_uris):
        sp.playlist_add_items(playlist_id, [track])


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

replace_recently_added_playlist(RECENTLY_ADDED, 50, 0)
