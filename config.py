import os



from dotenv import load_dotenv

load_dotenv()

dsl = {
    'dbname': os.getenv('POSTGRESQL_DB'),
    'user': os.getenv('POSTGRESQL_USER'),
    'password': os.getenv('POSTGRESQL_PASSWORD'),
    'host': os.getenv('POSTGRESQL_HOST'),
    'port': os.getenv('POSTGRESQL_PORT'),
    'options': os.getenv('POSTGRESQL_OPTIONS'),
}
