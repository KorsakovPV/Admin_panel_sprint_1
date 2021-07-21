DROP DATABASE IF EXISTS movies;

CREATE DATABASE movies;

\c movies

DROP SCHEMA IF EXISTS content CASCADE;

CREATE SCHEMA IF NOT EXISTS content;

-- CREATE TYPE content.film_team_role AS ENUM ('actor', 'director', 'writer');

-- CREATE TYPE content.film_work_types AS ENUM ('movie', 'series', 'tv_show');

-- CREATE TYPE content.film_mpaa_rating_type AS ENUM ('G', 'PG', 'PG_13', 'R', 'NC_17');

CREATE TABLE IF NOT EXISTS content.film_work (
    id UUID PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    creation_date DATE,
    certificate TEXT,
    file_path TEXT,
    rating FLOAT,
    type CHAR(20),
    mpaa_rating CHAR(20),
    created TIMESTAMP with time zone,
    updated TIMESTAMP with time zone
);

CREATE TABLE IF NOT EXISTS content.genre (
    id UUID PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    created TIMESTAMP with time zone,
    updated TIMESTAMP with time zone
);

CREATE TABLE IF NOT EXISTS content.film_work_genre (
    id UUID PRIMARY KEY,
    film_work_id UUID REFERENCES content.film_work (id),
    genre_id UUID REFERENCES content.genre (id),
    created TIMESTAMP with time zone,
    updated TIMESTAMP with time zone,
);

CREATE UNIQUE INDEX film_work_genre ON content.film_work_genre (film_work_id, genre_id);

CREATE TABLE IF NOT EXISTS content.person (
    id uuid PRIMARY KEY,
    full_name TEXT NOT NULL,
    birth_date DATE,
    created TIMESTAMP with time zone,
    updated TIMESTAMP with time zone
);

CREATE TABLE IF NOT EXISTS content.film_work_person (
    id UUID PRIMARY KEY,
    film_work_id UUID REFERENCES content.film_work (id),
    person_id UUID REFERENCES content.person (id),
    role CHAR(20),
    created TIMESTAMP with time zone,
    updated TIMESTAMP with time zone,
);

CREATE UNIQUE INDEX film_work_person_role ON content.film_work_person (film_work_id, person_id, role);