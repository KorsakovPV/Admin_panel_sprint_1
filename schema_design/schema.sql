CREATE DATABASE movies;

\c movies

DROP SCHEMA IF EXISTS content CASCADE;

CREATE SCHEMA IF NOT EXISTS content;

CREATE TYPE content.film_team_role AS ENUM ('actor', 'director', 'writer');

CREATE TYPE content.film_work_types AS ENUM ('movie', 'series', 'tv_show');

CREATE TYPE content.film_mpaa_rating_type AS ENUM ('G', 'PG', 'PG_13', 'R', 'NC_17');

CREATE TABLE IF NOT EXISTS content.film_work (
    id UUID PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    creation_date DATE,
    certificate TEXT,
    file_path TEXT,
    rating NUMERIC(2,1),
    type content.film_work_types,
    created_at TIMESTAMP with time zone,
    updated_at TIMESTAMP with time zone
);

CREATE TABLE IF NOT EXISTS content.genre (
    id UUID PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP with time zone,
    updated_at TIMESTAMP with time zone
);

CREATE TABLE IF NOT EXISTS content.film_work_genre (
    id UUID PRIMARY KEY,
    film_work_id UUID REFERENCES content.film_work (id),
    genre_id UUID REFERENCES content.genre (id),
    created_at TIMESTAMP with time zone,
    UNIQUE (film_work_id, genre_id)
);

CREATE TABLE IF NOT EXISTS content.person (
    id uuid PRIMARY KEY,
    full_name TEXT NOT NULL,
    birth_date DATE,
    created_at TIMESTAMP with time zone,
    updated_at TIMESTAMP with time zone
);

CREATE TABLE IF NOT EXISTS content.film_work_person (
    id UUID PRIMARY KEY,
    film_work_id UUID REFERENCES content.film_work (id),
    person_id UUID REFERENCES content.person (id),
    role content.film_team_role,
    created_at TIMESTAMP with time zone,
    UNIQUE (film_work_id, person_id, role)
);
