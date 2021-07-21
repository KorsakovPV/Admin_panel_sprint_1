import os
import sqlite3

import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

from utils.postgres_saver import PostgresSaver
from utils.sqlite_loader import SQLiteLoader

dsl = {
    'dbname': os.getenv('POSTGRESQL_DB', 'movies'),
    'user': os.getenv('POSTGRESQL_USER', 'postgres'),
    'password': os.getenv('POSTGRESQL_PASSWORD', 'postgres'),
    'host': os.getenv('POSTGRESQL_HOST', 'localhost'),
    'port': os.getenv('POSTGRESQL_PORT', '5432'),
    'options': os.getenv('POSTGRESQL_OPTIONS', '-c search_path=content'),
}


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""
    postgres_saver = PostgresSaver(pg_conn)
    sqlite_loader = SQLiteLoader(connection)

    data = sqlite_loader.load_movies()
    postgres_saver.save_all_data(data)


if __name__ == '__main__':
    with sqlite3.connect('db.sqlite') as sqlite_conn, psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)
