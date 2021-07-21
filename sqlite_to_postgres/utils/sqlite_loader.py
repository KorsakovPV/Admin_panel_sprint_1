import json
import sqlite3
from typing import List


class SQLiteLoader:
    SQL = '''
    WITH movies_actors as (
        SELECT movies.id, group_concat(actors.id) as actors_ids, group_concat(actors.name) as actors_names
        FROM movies
                 LEFT JOIN movie_actors on movies.id = movie_actors.movie_id
                 LEFT JOIN actors on movie_actors.actor_id = actors.id
        GROUP BY movies.id
    )
    SELECT movies.id, genre, director, title, plot, imdb_rating, movies_actors.actors_ids, movies_actors.actors_names,
           CASE
            WHEN movies.writers = '' THEN '[{"id": "' || movies.writer || '"}]'
            ELSE movies.writers
           END AS writers
    FROM movies
    LEFT JOIN movies_actors ON movies.id = movies_actors.id
    '''

    def __init__(self, connection: sqlite3.Connection):
        self.conn = connection
        self.conn.row_factory = sqlite3.Row

    def load_writers_names(self) -> dict:
        writers = {}
        for writer in self.conn.execute('SELECT DISTINCT id, name FROM writers'):
            writers[writer['id']] = writer
        return writers

    def transform_row(self, row: dict, writers: dict) -> dict:
        movie_writers = []
        writers_set = set()
        for writer in json.loads(row['writers']):
            writer_id = writer['id']
            if writers[writer_id]['name'] != 'N/A' and writer_id not in writers_set:
                movie_writers.append(writers[writer_id])
                writers_set.add(writer_id)

        actors_names = []
        if row['actors_ids'] is not None and row['actors_names'] is not None:
            actors_names = [x for x in row['actors_names'].split(',') if x != 'N/A']

        new_row = {
            'id': row['id'],
            'genre': row['genre'].split(','),
            'actors': actors_names,
            'writers': [x['name'] for x in movie_writers],
            'imdb_rating': float(row['imdb_rating']) if row['imdb_rating'] != 'N/A' else None,
            'title': row['title'],
            'director': [
                x.strip() for x in row['director'].split(',')
            ] if row['director'] != 'N/A' else None,
            'description': row['plot'] if row['plot'] != 'N/A' else None
        }

        return new_row

    def load_movies(self) -> List[dict]:
        movies = []

        writers = self.load_writers_names()

        for row in self.conn.execute(self.SQL):
            transformed_row = self.transform_row(row, writers)
            movies.append(transformed_row)

        return movies
