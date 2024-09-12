# Playlist and Song Management API

This project provides a RESTful API for managing playlists and songs. Users can create songs, create playlists, add songs to playlists, retrieve songs, and delete songs from playlists. The API is built using Flask and stores data in Python dictionaries (in-memory).

## Features

- **CRUD Operations** for songs (Create, Read, Update, Delete)
- **CRUD Operations** for playlists (Create, Read, Delete)
- **Add songs to playlists**
- **Remove songs from playlists**
- **Retrieve all songs in a playlist with optional sorting (by title, artist, or genre)**

## Requirements

- Python 3.x
- Flask
- (Optional) **Postman** for testing API endpoints

## Installation

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd playlist-api
   ```

2. **Set up a virtual environment (optional but recommended)**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install the required packages**:
   ```bash
   pip install Flask
   ```

4. **Run the application**:
   ```bash
   python app.py
   ```

5. **Access the API**:
   Once the server is running, the API will be available at `http://127.0.0.1:5000`.

## API Endpoints

### Song Management

#### 1. **Create a Song**

- **Endpoint**: `POST /create_song`
- **Description**: Creates a new song in the system.
- **Request Body**:
  ```json
  {
      "song_id": 1,
      "song_title": "Church Clap",
      "artist": "KB",
      "genre": "Hip-Hop"
  }
  ```
- **Response**:
  ```json
  {
      "message": "Song 'Church Clap' added successfully!"
  }
  ```

#### 2. **Get All Songs**

- **Endpoint**: `GET /songs`
- **Description**: Retrieves all songs in the system.
- **Response**:
  ```json
  [
      {
          "song_id": 1,
          "song_title": "Church Clap",
          "artist": "KB",
          "genre": "Hip-Hop"
      },
      {
          "song_id": 2,
          "song_title": "Graves to Gardens",
          "artist": "Elevation Worship",
          "genre": "Worship"
      },
      {
          "song_id": 3,
          "song_title": "Home",
          "artist": "Chris Tomlin",
          "genre": "Christian"
      }
  ]
  ```

#### 3. **Get a Song by ID**

- **Endpoint**: `GET /songs/<song_id>`
- **Description**: Retrieves a specific song by its `song_id`.
- **Response**:
  ```json
  {
      "song_id": 1,
      "song_title": "Church Clap",
      "artist": "KB",
      "genre": "Hip-Hop"
  }
  ```

#### 4. **Update a Song**

- **Endpoint**: `PUT /songs/<song_id>`
- **Description**: Updates a specific song by its `song_id`.
- **Request Body**:
  ```json
  {
      "song_title": "Church Clap",
      "artist": "KB",
      "genre": "Rap"
  }
  ```
- **Response**:
  ```json
  {
      "message": "Song updated"
  }
  ```

#### 5. **Delete a Song**

- **Endpoint**: `DELETE /songs/<song_id>`
- **Description**: Deletes a specific song by its `song_id`.
- **Response**:
  ```json
  {
      "message": "Song deleted"
  }
  ```

### Playlist Management

#### 1. **Create a Playlist**

- **Endpoint**: `POST /create_playlist`
- **Description**: Creates a new playlist.
- **Request Body**:
  ```json
  {
      "playlist_id": 1,
      "playlist_name": "My Worship Playlist",
      "user_id": 101
  }
  ```
- **Response**:
  ```json
  {
      "message": "Playlist 'My Worship Playlist' created successfully!"
  }
  ```

#### 2. **Add a Song to a Playlist**

- **Endpoint**: `POST /playlists/<playlist_id>/songs`
- **Description**: Adds a song to a playlist by `playlist_id` and `song_id`.
- **Request Body**:
  ```json
  {
      "song_id": 1
  }
  ```
- **Response**:
  ```json
  {
      "message": "Song 'Church Clap' added to playlist 'My Worship Playlist'"
  }
  ```

#### 3. **Get All Songs in a Playlist (with Sorting)**

- **Endpoint**: `GET /playlists/<playlist_id>/songs`
- **Description**: Retrieves all songs in a playlist, with optional sorting by `title`, `artist`, or `genre`.
- **Query Parameter**: `sort_by` (optional, valid values: `title`, `artist`, `genre`)
- **Example**: `GET /playlists/1/songs?sort_by=artist`
- **Response**:
  ```json
  [
      {
          "song_id": 2,
          "song_title": "Graves to Gardens",
          "artist": "Elevation Worship",
          "genre": "Worship"
      },
      {
          "song_id": 3,
          "song_title": "Home",
          "artist": "Chris Tomlin",
          "genre": "Christian"
      },
      {
          "song_id": 1,
          "song_title": "Church Clap",
          "artist": "KB",
          "genre": "Hip-Hop"
      }
  ]
  ```

#### 4. **Remove a Song from a Playlist**

- **Endpoint**: `DELETE /playlists/<playlist_id>/songs/<song_id>`
- **Description**: Removes a specific song from a playlist.
- **Response**:
  ```json
  {
      "message": "Song 'Church Clap' removed from playlist 'My Worship Playlist'"
  }
  ```

### Error Handling

If an invalid request is made or a resource is not found, the API will return a descriptive error message. For example:

- **Playlist Not Found**:
  ```json
  {
      "error": "Playlist not found"
  }
  ```

- **Song Not Found**:
  ```json
  {
      "error": "Song not found"
  }
  ```
