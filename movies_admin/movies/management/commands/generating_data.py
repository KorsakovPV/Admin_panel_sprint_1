import logging
import random

import pyprind
from django.core.management.base import BaseCommand

from movies_admin.movies.factories.film_work import FilmWorkFactory
from movies_admin.movies.factories.genre import GenreFactory, FilmWorkGenreFactory
from movies_admin.movies.factories.person import PersonFactory, FilmWorkPersonFactory
from movies_admin.movies.factories.user import UserFactory
from movies_admin.movies.models import User, Genre, FilmWork, Person, FilmWorkGenre, FilmWorkPerson


class Command(BaseCommand):
    help = 'Generating data.'

    USER = 100
    GENRE = 10000
    PERSON = 1000
    FILMWORK_FILM = 1000000
    FILMWORK_SERIES = 200000
    FILMWORK_MIN_GENRE = 0
    FILMWORK_MAX_GENRE = 5
    FILMWORK_MIN_PERSONS = 0
    FILMWORK_MAX_PERSONS = 5
    FILMWORK_GENRES_PERSONS = 7200000

    def handle(self, *args, **options):
        """
        python manage.py generating_data
        """

        # User.objects.exclude(is_superuser=True).delete()
        # Genre.objects.all().delete()
        # Person.objects.all().delete()
        # FilmWork.objects.all().delete()

        self.generating_users()
        logging.info('User=', User.objects.all().count())

        self.generating_genres()
        self.all_genre = Genre.objects.all()
        logging.info('Genre=', self.all_genre.count())

        self.generating_persons()
        self.all_person = Person.objects.all()
        logging.info('Person=', self.all_person.count())

        self.generating_film(type='series', counter=self.FILMWORK_SERIES)

        self.generating_film(type='film', counter=self.FILMWORK_FILM)

        self.films = FilmWork.objects.all()
        logging.info('FilmWork=', self.films.count())

        self.generating_relationship_film_to_genres_and_persons()
        logging.info('FilmWorkGenre=', FilmWorkGenre.objects.all().count())
        logging.info('FilmWorkPerson=', FilmWorkPerson.objects.all().count())

    def generating_relationship_film_to_genres_and_persons(self):
        genres_persons_count = self.FILMWORK_GENRES_PERSONS - FilmWorkGenre.objects.all().count() - FilmWorkPerson.objects.all().count()
        if genres_persons_count > 0:
            genres = []
            persons = []
            bar = pyprind.ProgBar(self.films.count(), title='Generating FilmWorkGenre and FilmWorkPerson.')
            for film in self.films:
                bar.update()
                film_genres = {random.choice(self.all_genre) for _ in
                               range(random.randint(self.FILMWORK_MIN_GENRE, self.FILMWORK_MAX_GENRE))}
                for film_genre in film_genres:
                    genres.append(FilmWorkGenreFactory.build(film_work=film, genre=film_genre))

                film_persons = {random.choice(self.all_person) for _ in
                                range(random.randint(self.FILMWORK_MIN_PERSONS, self.FILMWORK_MAX_PERSONS))}
                for film_person in film_persons:
                    persons.append(FilmWorkPersonFactory.build(film_work=film, person=film_person))

                if len(genres) > 50000:
                    FilmWorkGenre.objects.bulk_create(genres)
                    genres = []

                if len(persons) > 50000:
                    FilmWorkPerson.objects.bulk_create(persons)
                    persons = []

            FilmWorkGenre.objects.bulk_create(genres)
            FilmWorkPerson.objects.bulk_create(persons)

    def generating_film(self, type, counter):
        film_count = counter - FilmWork.objects.filter(type=type).count()
        if film_count > 0:
            films = []
            bar = pyprind.ProgBar(film_count, title=f'Generating FilmWork {type}.')
            for _ in range(film_count):
                bar.update()
                films.append(FilmWorkFactory.build(type=type))
                if len(films) > 50000:
                    FilmWork.objects.bulk_create(films)
                    films = []
            FilmWork.objects.bulk_create(films)

    def generating_persons(self):
        person_count = self.PERSON - Person.objects.all().count()
        if person_count > 0:
            persons = []
            bar = pyprind.ProgBar(person_count, title='Generating Person')
            for _ in range(person_count):
                bar.update()
                persons.append(PersonFactory.build())
            Person.objects.bulk_create(persons)

    def generating_users(self):
        user_count = self.USER - User.objects.all().count()
        if user_count > 0:
            user = []
            bar = pyprind.ProgBar(user_count, title='Generating User.')
            for _ in range(user_count):
                bar.update()
                user.append(UserFactory.build())
            User.objects.bulk_create(user)

    def generating_genres(self):
        genre_count = self.GENRE - Genre.objects.all().count()
        if genre_count > 0:
            genres = []
            bar = pyprind.ProgBar(genre_count, title='Generating Genre.')
            for _ in range(genre_count):
                bar.update()
                genres.append(GenreFactory.build())
            Genre.objects.bulk_create(genres)
