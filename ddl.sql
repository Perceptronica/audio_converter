CREATE TABLE IF NOT EXISTS artists (
    artist_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    country VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS labels (
    label_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS genres (
    genre_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS albums (
    album_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    artist_id INTEGER REFERENCES artists (artist_id),
    release_year INTEGER,
    label_id INTEGER REFERENCES labels (label_id),
    genre_id INTEGER REFERENCES genres (genre_id)
);

CREATE TABLE IF NOT EXISTS tracks (
    track_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    duration INTEGER,
    track_number INTEGER,
    album_id INTEGER REFERENCES albums (album_id)
);

CREATE TABLE IF NOT EXISTS artist_track (
    artist_id INTEGER REFERENCES artists (artist_id),
    track_id INTEGER REFERENCES tracks (track_id),
    role VARCHAR(100),
    PRIMARY KEY (artist_id, track_id)
);

CREATE TABLE IF NOT EXISTS track_tags (
    track_id INTEGER PRIMARY KEY REFERENCES tracks (track_id),
    file_path VARCHAR(255),
    bitrate INTEGER
);
