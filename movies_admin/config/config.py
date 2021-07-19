import os

from dotenv import load_dotenv

load_dotenv()

dsl = {
    'dbname': os.getenv('POSTGRESQL_DB', 'movies'),
    'user': os.getenv('POSTGRESQL_USER', 'postgres'),
    'password': os.getenv('POSTGRESQL_PASSWORD', 'postgres'),
    'host': os.getenv('POSTGRESQL_HOST', 'localhost'),
    'port': os.getenv('POSTGRESQL_PORT', '5432'),
    'options': os.getenv('POSTGRESQL_OPTIONS', '-c search_path=content'),
}
