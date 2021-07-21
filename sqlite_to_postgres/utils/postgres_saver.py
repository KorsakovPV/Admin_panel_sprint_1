from datetime import datetime
from typing import List, Dict, Set, Any, Optional
from uuid import uuid4

from psycopg2 import extras
from psycopg2.extensions import connection as _connection


class PostgresSaver:
    def __init__(self, connection: _connection):
        self.conn = connection
        self.person_set: Set[str] = set()
        self.genres_set: Set[str] = set()

        self.film_work: List[dict] = []
        self.genre: Dict[str] = {}  # List[dict] = []
        self.genre_film_work: List[dict] = []
        self.person: List[dict] = []
        self.person_film_work: List[dict] = []

        self.schema = 'content'

    def append_film_work(self, row: Dict[str, Any]) -> str:
        film_id = str(uuid4())
        new_row = {
            'id': film_id,
            'title': row['title'],
            'description': row['description'] or '',
            'imdb_rating': row['imdb_rating'] or 0,
            'created': datetime.now().astimezone(),
            'modified': datetime.now().astimezone(),
            'type': ''
        }

        self.film_work.append(new_row)

        return film_id

    def add_person(self, id_: str, name: str):
        row = {
            'id': id_,
            'full_name': name,
            'birthdate': None,
        }
        self.person.append(row)

    def append_person(self, person_list: List[str]) -> Optional[List[str]]:
        if person_list is None:
            return []

        id_list = []
        for person_name in person_list:
            if person_name not in self.person_set:
                id_ = str(uuid4())
                self.add_person(id_, person_name)
                self.person_set.add(person_name)
            else:
                for p in self.person:
                    if p['full_name'] == person_name:
                        id_ = p['id']
                        break

            id_list.append(id_)

        return id_list

    def add_genre(self, id_: str, name: str):
        self.genre[name] = id_

    def append_genre(self, genre_list: List[str]) -> List[str]:
        if genre_list is None:
            return []

        id_list = []
        for genre in genre_list:
            if genre not in self.genres_set:
                id_ = str(uuid4())
                self.add_genre(id_, genre)
                self.genres_set.add(genre)
            else:
                id_ = self.genre.get(genre)

            id_list.append(id_)

        return id_list

    def append_person_film_work(self, film_id: str, person_id_list: List[str], role: str):
        for person_id in person_id_list:
            id_ = str(uuid4())
            row = {
                'id': id_,
                'film_work_id': film_id,
                'person_id': person_id,
                'role': role,
            }
            self.person_film_work.append(row)

    def append_genre_film_work(self, film_id: str, genre_id_list: List[str]):
        for genre_id in genre_id_list:
            id_ = str(uuid4())
            row = {
                'id': id_,
                'film_work_id': film_id,
                'genre_id': genre_id,
            }
            self.genre_film_work.append(row)

    def insert_film_work(self):
        with self.conn.cursor() as cursor:
            params_list = []
            for row in self.film_work:
                params_list.append((row.get('id'), row.get('title'), row.get('description'), row.get('imdb_rating'),
                                    row.get('created').strftime('%Y-%m-%d %H:%M:%S.%f%z'),
                                    row.get('modified').strftime('%Y-%m-%d %H:%M:%S.%f%z')))
            extras.execute_batch(cursor,
                                 '''INSERT INTO content.film_work (id, title, description, rating, created, modified) 
                                 VALUES (%s, %s, %s, %s, %s, %s)''',
                                 params_list)

    def insert_genre(self):
        with self.conn.cursor() as cursor:
            params_list = []
            for row in self.genre:
                params_list.append((row.get('id'), row.get('name')))
            extras.execute_batch(cursor, 'INSERT INTO content.genre (id, name) VALUES (%s, %s)', params_list)

    def insert_person(self):
        with self.conn.cursor() as cursor:
            params_list = []
            for row in self.person:
                params_list.append((row.get('id'), row.get('full_name'), row.get('birthdate')))
            extras.execute_batch(cursor,
                                 'INSERT INTO content.person (id, full_name, birth_date) VALUES (%s, %s, %s)',
                                 params_list)

    def insert_film_work_genre(self):
        with self.conn.cursor() as cursor:
            params_list = []
            for row in self.genre_film_work:
                params_list.append((row.get('id'), row.get('film_work_id'), row.get('genre_id')))
            extras.execute_batch(cursor,
                                 '''INSERT INTO content.film_work_genre (id, film_work_id, genre_id) VALUES 
                                 (%s, %s, %s)''',
                                 params_list)

    def insert_film_work_person(self):
        with self.conn.cursor() as cursor:
            params_list = []
            for row in self.person_film_work:
                params_list.append((row.get('id'), row.get('film_work_id'), row.get('person_id'), row.get('role')))
            extras.execute_batch(cursor,
                                 '''INSERT INTO content.film_work_person (id, film_work_id, person_id, role) VALUES 
                                 (%s, %s, %s, %s) ON CONFLICT (film_work_id, person_id, role) DO NOTHING''',
                                 params_list)

    def save_all_data(self, data: List[dict]):
        for row in data:
            film_id = self.append_film_work(row)

            actor_id_list = self.append_person(row['actors'])
            self.append_person_film_work(film_id, actor_id_list, 'actor')

            writer_id_list = self.append_person(row['writers'])
            self.append_person_film_work(film_id, writer_id_list, 'writer')

            director_id_list = self.append_person(row['director'])
            self.append_person_film_work(film_id, director_id_list, 'director')

            genre_id_list = self.append_genre(row['genre'])
            self.append_genre_film_work(film_id, genre_id_list)

        # self.insert_film_work()
        # self.insert_genre()
        # self.insert_person()
        # self.insert_film_work_person()
        # self.insert_film_work_genre()
