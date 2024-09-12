class PlaylistManager:
    def __init__(self):
        self.songs = {}      # Stores songs by song_id
        self.playlists = {}  # Stores playlists by playlist_id

    def add_song(self, song):
        """Adds a song to the hash table using song_id as the key."""
        if song.song_id in self.songs:
            print(f"Song with ID {song.song_id} already exists.")
        else:
            self.songs[song.song_id] = song
            print(f"Song '{song.song_title}' added to the playlist.")

    def create_playlist(self, playlist_id, playlist_name, user_id=None):
        """Creates a new playlist."""
        if playlist_id in self.playlists:
            print(f"Playlist with ID {playlist_id} already exists.")
        else:
            new_playlist = Playlist(playlist_id, playlist_name, user_id)
            self.playlists[playlist_id] = new_playlist
            print(f"Playlist '{playlist_name}' created successfully.")

    def add_song_to_playlist(self, playlist_id, song_id):
        """Adds an existing song to a playlist."""
        # Convert song_id to an integer to match the stored type
        song_id = int(song_id)

        # Check if the playlist exists
        if playlist_id not in self.playlists:
            return {"error": "Playlist not found"}

        # Check if the song exists in the central collection
        if song_id not in self.songs:
            return {"error": "Song not found"}

        playlist = self.playlists[playlist_id]
        song = self.songs[song_id]

        # Check if the song is already in the playlist
        if song_id in playlist.songs:
            return {"error": "Song is already in the playlist"}

        # Add the song to the playlist
        playlist.songs[song_id] = song
        return {"message": f"Song '{song.song_title}' added to playlist '{playlist.playlist_name}'"}

    def get_song(self, song_id):
        """Retrieves a song by its song_id from the hash table."""
        if song_id in self.songs:
            return self.songs[song_id]
        else:
            print(f"Song with ID {song_id} not found.")
            return None

    def remove_song(self, song_id):
        """Removes a song from the hash table using song_id."""
        if song_id in self.songs:
            removed_song = self.songs.pop(song_id)
            print(f"Song '{removed_song.song_title}' removed from the system.")
        else:
            print(f"Song with ID {song_id} not found.")


class Song:
    def __init__(self, song_id, song_title, artist, genre):
        self.song_id = song_id
        self.song_title = song_title
        self.artist = artist
        self.genre = genre

    def __str__(self):
        return f"{self.song_title} by {self.artist} ({self.genre})"

class Playlist:
    def __init__(self, playlist_id, playlist_name, user_id=None):
        self.playlist_id = playlist_id
        self.playlist_name = playlist_name
        self.user_id = user_id  # Optional user_id
        self.songs = {}  # Dictionary to store songs by song_id


#
# playlist_manager = PlaylistManager()
#
# # Create some song objects
# song1 = Song(1, "Shape of You", "Ed Sheeran", "Pop")
# song2 = Song(2, "Someone Like You", "Adele", "Pop")
# song3 = Song(3, "Bohemian Rhapsody", "Queen", "Rock")
#
# # Add songs to the hash table
# playlist_manager.add_song(song1)
# playlist_manager.add_song(song2)
# playlist_manager.add_song(song3)
#
# # Retrieve a song by song_id
# retrieved_song = playlist_manager.get_song(2)
# if retrieved_song:
#     print(f"Retrieved: {retrieved_song}")
#
# # Attempt to retrieve a song that does not exist
# playlist_manager.get_song(4)
#
# # Remove a song by song_id
# playlist_manager.remove_song(2)
#
# # Try removing the same song again (should not be found)
# playlist_manager.remove_song(2)
#
# # Check if the song was actually removed by trying to retrieve it again
# playlist_manager.get_song(2)