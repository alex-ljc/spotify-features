#!/usr/bin/env python3

import os
import dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time

RECENTLY_ADDED = "3BZP1mB69SWnSNCy4nfxXX"
QUEUE_OF_SHIT = '7kSoTKPlSLr0BKkFfOLhY2'

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
def find_recently_saved_albums(amount, off):
    recently_saved_albums = []
    for i in range(0,amount):
        new_album = sp.current_user_saved_albums(limit = 1, offset = (off + i), market = "from_token")
        recently_saved_albums.append(new_album)

    return recently_saved_albums

# Finds the most recently saved songs
def find_recently_saved_songs(amount, off):
    recently_saved_songs = []
    for i in range(0, amount):
        new_songs = sp.current_user_saved_tracks(limit = 1, offset = (off + i), market = "from_token")
        recently_saved_songs.append(new_songs)

    return recently_saved_songs

# Parses album data to get track uris
def get_track_uris_from_albums(album):
    track_uris = []
    total = album['items'][0]['album']['total_tracks']
    
    for i in range(0,total):
        track = album['items'][0]['album']['tracks']['items'][i]['uri']
        track_uris.append(track)   

    return track_uris


# Parses album data to get total songs
def get_amount_of_songs_in_albums(album):
    return album['items'][0]['album']['total_tracks']


# Adds the most recently saved albums to a playlist
def replace_recently_added_playlist(amount, offset):
    RECENTLY_ADDED = "3BZP1mB69SWnSNCy4nfxXX"
    recently_added_albums = find_recently_saved_albums(amount, offset)
    track_uris = []
    sp.playlist_replace_items(RECENTLY_ADDED, track_uris)
    for album in recently_added_albums:
        track_uris = track_uris + get_track_uris_from_albums(album)
    
    size = len(track_uris)
    
    split_track_uris = split_list_below_100(track_uris, [])
    for tracks in split_track_uris:
        sp.playlist_add_items(RECENTLY_ADDED, tracks)
    
    print(f"Recently played has {size} songs")

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
def reset_most_recent_album():
    album = find_recently_saved_albums(1, 0)
    album_id = album[0]['items'][0]['album']['uri']
    os.environ['MOST_RECENT_ALBUM'] = album_id
    dotenv.set_key(dotenv_file, 'MOST_RECENT_ALBUM', os.environ['MOST_RECENT_ALBUM'])


# Check newest most recent album against stored most recent album. Returns True if there is a new album, false otherwise
def check_if_new_saved_album():
    album = find_recently_saved_albums(1, 0)
    album_id = album[0]['items'][0]['album']['uri']
    if (album_id != os.environ['MOST_RECENT_ALBUM']):
        return True
    else:
        return False


# Finds how many albums have been added since latest check
def count_new_albums():
    counter = 0;
    album_id = 0;
    while (album_id != os.environ['MOST_RECENT_ALBUM']):
        album = find_recently_saved_albums(1, counter)
        album_id = album[0]['items'][0]['album']['uri']
        counter += 1
    
    return counter - 1


# Update everything playlist
def update_everything():
    EVERYTHING = "3ZqjihXebfS117lF9bi9FI"
    new_albums = find_recently_saved_albums(count_new_albums(), 0)
    track_uris = []
    for album in new_albums:
        track_uris = track_uris + get_track_uris_from_albums(album)
    
    split_track_uris = split_list_below_100(track_uris, [])
    for tracks in split_track_uris:
        sp.playlist_add_items(EVERYTHING, tracks)
    print(f"Updated everything with {len(track_uris)} songs")


def check_if_new_saved_song():
    song = find_recently_saved_songs(1, 0)
    song_id = song[0]['items'][0]['track']['uri']
    if (song_id != os.environ['MOST_RECENT_SONG']):
        return True
    else:
        return False


def reset_most_recent_song():
    song = find_recently_saved_songs(1, 0)
    song_id = song[0]['items'][0]['track']['uri']
    os.environ['MOST_RECENT_SONG'] = song_id
    dotenv.set_key(dotenv_file, 'MOST_RECENT_SONG', os.environ['MOST_RECENT_SONG'])

def count_new_songs():
    counter = 0
    song_id = 0
    while (song_id != os.environ['MOST_RECENT_SONG']):
        song = find_recently_saved_songs(1, counter)
        song_id = song[0]['items'][0]['track']['uri']
        counter += 1

    return counter - 1

# Checks if new albums have been added and updates playlists
def update():
    dotenv_file = dotenv.find_dotenv()
    dotenv.load_dotenv(dotenv_file)
    if check_if_new_saved_album():
        update_everything()
        replace_recently_added_playlist(45, 0)
        reset_most_recent_album()
    
    if check_if_new_saved_song():
        update_liked()
        reset_most_recent_song()

def update_liked():
    LIKED = "1Eb6PKpnm0iz68zmNkT5rY"
    new_songs = find_recently_saved_songs(count_new_songs(), 0)
    tracks = []
    for song in new_songs:
        uri = song['items'][0]['track']['uri']
        tracks.append(uri)

    split_track_uris = split_list_below_100(tracks, [])
    for tracks in split_track_uris:
        sp.playlist_add_items(LIKED, tracks)

    print(f"Updated liked with {len(tracks)} songs")

def loop_current_album(x):
    currently_playing_song = sp.current_user_playing_track()
    if currently_playing_song == None:
        currently_playing_song = sp.current_user_recently_played(limit=1)
        album_id = currently_playing_song['items'][0]['track']['album']['uri']
    else:
        album_id = currently_playing_song['item']['album']['id']
    album = sp.album(album_id)
    i = 0
    album_length = get_duration_of_album(album)
    found_last_song = False
    sleep_time = album['tracks']['items'][album['total_tracks'] - 1]['duration_ms'] / (3 * 1000) 
    while i < x:
        if sp.current_user_playing_track()['item']['track_number'] == album['total_tracks'] and not found_last_song:
            found_last_song = True
            sleep_attempts = 0
            add_album_to_queue(album)
            i += 1
            if sleep_attempts > album_length / (sleep_time * 1000 * album['total_tracks'] * 2):
                raise "Last song in album was never played"
            
            time.sleep(sleep_time)
            sleep_attempts += 1    
        elif found_last_song and sp.current_user_playing_track()['item']['track_number'] == 0:
            found_last_song = False
        

def add_album_to_queue(album):
    for song in album['tracks']['items']:
        sp.add_to_queue(song['uri'])
    
def get_duration_of_album(album):
    length = 0
    for i in range(0, album['total_tracks']):
        length += int(album['tracks']['items'][i]['duration_ms'])
    
    return length / 1000
        
def clear_playlist(playlist_id):
    playlist_tracks = sp.playlist_items(playlist_id)   
    song_ids = [track['track']['id'] for track in playlist_tracks['items']]
    sp.playlist_remove_all_occurrences_of_items(playlist_id, song_ids)

def get_album_info(album_id):
    album_data = sp.album(album_id)
    print(f"{album_data['artists'][0]['name']}\n  '{album_data['name']}'")
    
def get_track_info(track_id):
    track_data = sp.track(track_id)
    print(f"{track_data['artists'][0]['name']}\n  '{track_data['name']}'")

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, open_browser=False))
