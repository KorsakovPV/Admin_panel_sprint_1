import logging
import random

import pyprind
from django.core.management.base import BaseCommand

from movies.factories.film_work import FilmWorkFactory
from movies.factories.genre import GenreFactory, FilmWorkGenreFactory
from movies.factories.person import PersonFactory, FilmWorkPersonFactory
from movies.factories.user import UserFactory
from movies.models import User, Genre, FilmWork, Person, FilmWorkGenre, FilmWorkPerson


class Command(BaseCommand):
    help = 'Generating data.'

    USER = 100
    GENRE = 10000
    PERSON = 100000
    FILMWORK_FILM = 1000000
    FILMWORK_SERIES = 200000
    FILMWORK_MIN_GENRE = 0
    FILMWORK_MAX_GENRE = 5
    FILMWORK_MIN_PERSONS = 0
    FILMWORK_MAX_PERSONS = 5
    FILMWORK_GENRES_PERSONS = 7200000
    PADGE = 10000

    def handle(self, *args, **options):
        """
        python manage.py generating_data
        """

        logging.basicConfig(filename="sample.log", level=logging.INFO)

        User.objects.exclude(is_superuser=True).delete()
        Genre.objects.all().delete()
        Person.objects.all().delete()
        FilmWork.objects.all().delete()

        self.generating_users()
        logging.info('User=', User.objects.all().count())

        self.generating_genres()
        self.all_genre = Genre.objects.all()
        logging.info('Genre=', len(self.all_genre))

        self.generating_persons()
        self.all_person = Person.objects.all()
        logging.info('Person=', len(self.all_person))

        self.generating_film(type='series', counter=self.FILMWORK_SERIES)

        self.generating_film(type='film', counter=self.FILMWORK_FILM)

    def generating_film(self, type, counter):
        film_count = counter - FilmWork.objects.filter(type=type).count()
        if film_count > 0:
            films = []
            genres = []
            persons = []
            bar = pyprind.ProgBar(film_count, title=f'Generating FilmWork {type}.')
            for _ in range(film_count):
                bar.update()
                film = FilmWorkFactory.build(type=type)

                film_genres = {random.choice(self.all_genre) for _ in
                               range(random.randint(self.FILMWORK_MIN_GENRE, self.FILMWORK_MAX_GENRE))}
                for film_genre in film_genres:
                    genres.append(FilmWorkGenreFactory.build(film_work=film, genre=film_genre))

                film_persons = {random.choice(self.all_person) for _ in
                                range(random.randint(self.FILMWORK_MIN_PERSONS, self.FILMWORK_MAX_PERSONS))}
                for film_person in film_persons:
                    persons.append(FilmWorkPersonFactory.build(film_work=film, person=film_person))

                films.append(film)
                if len(films) > self.PADGE:
                    FilmWork.objects.bulk_create(films)
                    films = []
                    FilmWorkGenre.objects.bulk_create(genres)
                    genres = []
                    FilmWorkPerson.objects.bulk_create(persons)
                    persons = []
            FilmWork.objects.bulk_create(films)
            FilmWorkGenre.objects.bulk_create(genres)
            FilmWorkPerson.objects.bulk_create(persons)

    def generating_persons(self):
        person_count = self.PERSON - Person.objects.all().count()
        if person_count > 0:
            persons = PersonFactory.build_batch(person_count)
            Person.objects.bulk_create(persons)

    def generating_genres(self):
        genre_count = self.GENRE - Genre.objects.all().count()
        if genre_count > 0:
            genres = GenreFactory.build_batch(genre_count)
            Genre.objects.bulk_create(genres)

    def generating_users(self):
        user_count = self.USER - User.objects.all().count()
        if user_count > 0:
            user = UserFactory.build_batch(user_count)
            User.objects.bulk_create(user)
