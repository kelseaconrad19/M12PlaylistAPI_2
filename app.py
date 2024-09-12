from flask import Flask, request, jsonify
from connect_to_db import get_db_connection
from data_organization import *
import requests
app = Flask(__name__)
playlist_manager = PlaylistManager()

@app.route('/')
def index():
    return "Welcome to the Playlist API!"

@app.route('/create_song', methods=['POST'])
def create_song():
    print("Request received!")  # Log when the request is received
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data received"}), 400

    print(f"Data received: {data}")  # Log the received data

    song_id = data.get("song_id")
    song_title = data.get("song_title")
    artist = data.get("artist")
    genre = data.get("genre")

    # Create a new Song object
    new_song = Song(song_id, song_title, artist, genre)

    # Add the song to the playlist manager
    playlist_manager.add_song(new_song)

    print(f"Song '{song_title}' added!")  # Log the successful addition

    # Return a success message
    return jsonify({"message": f"Song '{song_title}' added successfully!"}), 201

@app.route('/songs', methods=['GET'])
def get_songs():
    songs = playlist_manager.songs.values()
    songs_list = []

    for song in songs:
        song_dict = {
            "song_id": song.song_id,
            "song_title": song.song_title,
            "artist": song.artist,
            "genre": song.genre
        }
        songs_list.append(song_dict)
    return jsonify(songs_list), 200

@app.route('/songs/<int:song_id>', methods=['GET'])
def get_song(song_id):
    song = playlist_manager.get_song(song_id)
    if song:
        song_dict = {
            "song_id": song.song_id,
            "song_title": song.song_title,
            "artist": song.artist,
            "genre": song.genre
        }
        return jsonify(song_dict), 200
    else:
        return jsonify({"error": "Song not found"}), 404

@app.route('/songs/<int:song_id>', methods=['DELETE'])
def delete_song(song_id):
    playlist_manager.remove_song(song_id)
    return jsonify({"message": "Song deleted"}), 200

@app.route('/songs/<int:song_id>', methods=['PUT'])
def update_song(song_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data received"}), 400

    song = playlist_manager.get_song(song_id)
    if song:
        # Ensure the required fields are present
        song_title = data.get("song_title")
        artist = data.get("artist")
        genre = data.get("genre")

        if not all([song_title, artist, genre]):
            return jsonify({"error": "Missing fields: song_title, artist, and genre are required"}), 400

        song.song_title = song_title
        song.artist = artist
        song.genre = genre
        return jsonify({"message": "Song updated"}), 200
    else:
        return jsonify({"error": "Song not found"}), 404


@app.route("/create_playlist", methods=["POST"])
def create_playlist():
    data = request.get_json()

    # Get playlist details from the request body
    playlist_id = data.get("playlist_id")
    playlist_name = data.get("playlist_name")
    user_id = data.get("user_id")  # Optional user_id

    if not playlist_id or not playlist_name:
        return jsonify({"error": "Playlist ID and name are required"}), 400

    # Create a new playlist with optional user_id
    playlist_manager.create_playlist(playlist_id, playlist_name, user_id)

    # Return a success message
    return jsonify({"message": f"Playlist '{playlist_name}' created successfully!"}), 201



@app.route('/playlists/<int:playlist_id>/songs', methods=['POST'])
def add_song_to_playlist(playlist_id):
    data = request.get_json()

    # Get the song_id from the request body
    song_id = data.get("song_id")

    if not song_id:
        return jsonify({"error": "Song ID is required"}), 400

    # Attempt to add the song to the playlist
    result = playlist_manager.add_song_to_playlist(playlist_id, song_id)

    # Check if the operation was successful or if there was an error
    if "error" in result:
        return jsonify(result), 404
    else:
        return jsonify(result), 200

@app.route('/playlists/<int:playlist_id>/songs', methods=['GET'])
def get_songs_in_playlist(playlist_id):
    # Check if the playlist exists
    playlist = playlist_manager.playlists.get(playlist_id)
    if not playlist:
        return jsonify({"error": "Playlist not found"}), 404

    # Retrieve the sorting parameter from the query string (default is 'title')
    sort_by = request.args.get('sort_by', 'title')

    # Convert playlist songs dictionary to a list of songs
    songs_list = list(playlist.songs.values())

    # Sort songs based on the provided sort_by parameter
    if sort_by == 'title':
        songs_list.sort(key=lambda song: song.song_title.lower())
    elif sort_by == 'artist':
        songs_list.sort(key=lambda song: song.artist.lower())
    elif sort_by == 'genre':
        songs_list.sort(key=lambda song: song.genre.lower())
    else:
        return jsonify({"error": f"Invalid sort_by parameter: '{sort_by}'. Use 'title', 'artist', or 'genre'."}), 400

    # Create the response list
    songs_response = [
        {
            "song_id": song.song_id,
            "song_title": song.song_title,
            "artist": song.artist,
            "genre": song.genre
        }
        for song in songs_list
    ]

    # Return the sorted list of songs
    return jsonify(songs_response), 200

@app.route('/playlists/<int:playlist_id>/songs/<int:song_id>', methods=['DELETE'])
def remove_song_from_playlist(playlist_id, song_id):
    # Check if the playlist exists
    playlist = playlist_manager.playlists.get(playlist_id)
    if not playlist:
        return jsonify({"error": "Playlist not found"}), 404

    # Check if the song exists in the playlist
    if song_id not in playlist.songs:
        return jsonify({"error": "Song not found in the playlist"}), 404

    # Remove the song from the playlist
    removed_song = playlist.songs.pop(song_id)
    return jsonify({"message": f"Song '{removed_song.song_title}' removed from playlist '{playlist.playlist_name}'"}), 200




if __name__ == '__main__':
    app.run(debug=True)
