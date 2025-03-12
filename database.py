import psycopg2
from psycopg2 import sql
from config import DB_CONFIG

class Database:
    def __init__(self):
        self.conn = psycopg2.connect(**DB_CONFIG)

    def search_artists(self, name):
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT artist_id, name FROM artists WHERE name ILIKE %s;",
                (f'%{name}%',)
            )
            return cur.fetchall()

    def get_albums_by_artist(self, artist_id):
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT album_id, title FROM albums WHERE artist_id = %s;",
                (artist_id,)
            )
            return cur.fetchall()

    def get_tracks_by_album(self, album_id):
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT track_id, title FROM tracks WHERE album_id = %s;",
                (album_id,)
            )
            return cur.fetchall()

    def get_track_info(self, track_id):
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT t.title,
                       ar.name,
                       al.title,
                       al.release_year,
                       g.name,
                       l.name,
                       t.track_number
                FROM tracks t
                JOIN albums al ON t.album_id = al.album_id
                JOIN artists ar ON al.artist_id = ar.artist_id
                JOIN genres g ON al.genre_id = g.genre_id
                JOIN labels l ON al.label_id = l.label_id
                WHERE t.track_id = %s;
            """, (track_id,))
            return cur.fetchone()

    def close(self):
        self.conn.close()
