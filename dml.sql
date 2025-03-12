INSERT INTO
    artists (name, country)
VALUES
    ('The Beatles', 'UK'),
    ('Queen', 'UK'),
    ('Michael Jackson', 'USA');

INSERT INTO
    labels (name)
VALUES
    ('Apple Records'),
    ('EMI'),
    ('Epic Records');

INSERT INTO
    genres (name)
VALUES
    ('Rock'),
    ('Pop'),
    ('Disco');

INSERT INTO
    albums (
        title,
        artist_id,
        release_year,
        label_id,
        genre_id
    )
VALUES
    ('Abbey Road', 1, 1969, 1, 1),
    ('A Night at the Opera', 2, 1975, 2, 1),
    ('Thriller', 3, 1982, 3, 2);

INSERT INTO
    tracks (title, duration, track_number, album_id)
VALUES
    ('Come Together', 259, 1, 1),
    ('Something', 182, 2, 1),
    ('Bohemian Rhapsody', 354, 1, 2),
    ('Love of My Life', 216, 2, 2),
    ('Beat It', 258, 3, 3),
    ('Billie Jean', 294, 4, 3);

INSERT INTO
    artist_track (artist_id, track_id, role)
VALUES
    (1, 1, 'Main'),
    (1, 2, 'Main'),
    (2, 3, 'Main'),
    (2, 4, 'Main'),
    (3, 5, 'Main'),
    (3, 6, 'Main');

INSERT INTO
    track_tags (track_id, file_path, bitrate)
VALUES
    (1, '/music/beatles/come_together.mp3', 320),
    (3, '/music/queen/bohemian.flac', 1411),
    (5, '/music/mj/beat_it.mp3', 256),
    (6, '/music/mj/billie_jean.flac', 1411);
