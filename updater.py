#!/usr/bin/env python

from spotify import *
import sys

scope = """ugc-image-upload, 
user-read-recently-played, user-top-read, user-read-playback-position,
user-read-playback-state, user-modify-playback-state, user-read-currently-playing,
app-remote-control, streaming,
playlist-modify-public, playlist-modify-private,
playlist-read-private, playlist-read-collaborative,
user-follow-modify, user-follow-read,
user-library-modify, user-library-read,
user-read-email, user-read-private"""

if __name__ == "__main__":
    if len(sys.argv) < 1 or len(sys.argv) > 3:
        print("Usage: python3 updater.py <command>")
        exit()
    elif len(sys.argv) == 2 and sys.argv[1] == "update":
        update()
    elif len(sys.argv) == 3 and sys.argv[1] == "loop_album" and isinstance(int(sys.argv[2]), int):
        loop_current_album(int(sys.argv[2]))
    elif len(sys.argv) == 3 and sys.argv[1] == "loop_current_album" and isinstance(int(sys.argv[2]), int):
        loop_currently_playing_album(int(sys.argv[2]))
    elif len(sys.argv) == 2 and sys.argv[1] == 'clearrecent':
        clear_playlist(QUEUE_OF_SHIT)
    elif len(sys.argv) == 3 and sys.argv[1] == 'changevolume':
        change_volume(sys.argv[2])
    elif len(sys.argv) == 2 and sys.argv[1] == 'savecurrent':
        add_current_track_to_saved()
    else:
        print("Usage: python3 updater.py <command>")
        exit()
