import sqlite3

import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

from config import dsl

from sqlite_to_postgres.utils.postgres_saver import PostgresSaver
from sqlite_to_postgres.utils.sqlite_loader import SQLiteLoader

def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""
    # создаем экземпляр класа для постгреса
    postgres_saver = PostgresSaver(pg_conn)
    # сождаем экземпляр класса для sqlite
    sqlite_loader = SQLiteLoader(connection)

    # загружаем даные из sqlite фильмы
    data = sqlite_loader.load_movies()
    # загружаем даные в postgres
    postgres_saver.save_all_data(data)


if __name__ == '__main__':
    #через менеджер контекста обращаемся к базе
    with sqlite3.connect('db.sqlite') as sqlite_conn, psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
        #Вызываем функцию
        load_from_sqlite(sqlite_conn, pg_conn)
