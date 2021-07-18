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

    def handle(self, *args, **options):
        """
        python manage.py generating_data
        """
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

        # User.objects.exclude(is_superuser=True).delete()
        # Genre.objects.all().delete()
        # Person.objects.all().delete()
        # FilmWork.objects.all().delete()

        # UserFactory
        user_count = USER - User.objects.all().count()
        if user_count > 0:
            user = []
            bar = pyprind.ProgBar(user_count, title='Generating User.')
            for _ in range(user_count):
                bar.update()
                user.append(UserFactory.build())
            User.objects.bulk_create(user)
        print('User=', User.objects.all().count())

        # GenreFactory#
        genre_count = GENRE - Genre.objects.all().count()
        if genre_count > 0:
            genres = []
            bar = pyprind.ProgBar(genre_count, title='Generating Genre.')
            for _ in range(genre_count):
                bar.update()
                genres.append(GenreFactory.build())
            Genre.objects.bulk_create(genres)
        all_genre = Genre.objects.all()
        print('Genre=', Genre.objects.all().count())

        # PersonFactory
        person_count = PERSON - Person.objects.all().count()
        if person_count > 0:
            persons = []
            bar = pyprind.ProgBar(person_count, title='Generating Person')
            for _ in range(person_count):
                bar.update()
                persons.append(PersonFactory.build())
            Person.objects.bulk_create(persons)
        all_person = Person.objects.all()
        print('Person=', Person.objects.all().count())

        # FilmWorkFactory series
        film_count = FILMWORK_SERIES - FilmWork.objects.filter(type='series').count()
        if film_count > 0:
            films = []
            bar = pyprind.ProgBar(film_count, title='Generating FilmWork series.')
            for _ in range(film_count):
                bar.update()
                films.append(FilmWorkFactory.build(type='series'))
                if len(films) > 50000:
                    FilmWork.objects.bulk_create(films)
                    films = []
            FilmWork.objects.bulk_create(films)

        # FilmWorkFactory film
        film_count = FILMWORK_FILM - FilmWork.objects.filter(type='film').count()
        if film_count > 0:
            films = []
            bar = pyprind.ProgBar(film_count, title='Generating FilmWork film.')
            for _ in range(film_count):
                bar.update()
                films.append(FilmWorkFactory.build(type='film'))
                if len(films) > 50000:
                    FilmWork.objects.bulk_create(films)
                    films = []
            FilmWork.objects.bulk_create(films)
        films = FilmWork.objects.all()
        print('FilmWork=', FilmWork.objects.all().count())

        # FilmWork_Genre FILMWORKS_GENRES_PERSONS
        genres_persons_count = FILMWORK_GENRES_PERSONS - FilmWorkGenre.objects.all().count() - FilmWorkPerson.objects.all().count()
        if genres_persons_count > 0:
            genres = []
            persons = []
            bar = pyprind.ProgBar(films.count(), title='Generating FilmWorkGenre and FilmWorkPerson.')
            for film in films:
                bar.update()
                film_genres = {random.choice(all_genre) for _ in
                               range(random.randint(FILMWORK_MIN_GENRE, FILMWORK_MAX_GENRE))}
                for film_genre in film_genres:
                    genres.append(FilmWorkGenreFactory.build(film_work=film, genre=film_genre))

                film_persons = {random.choice(all_person) for _ in
                                range(random.randint(FILMWORK_MIN_PERSONS, FILMWORK_MAX_PERSONS))}
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
        print('FilmWorkGenre=', FilmWorkGenre.objects.all().count())
        print('FilmWorkPerson=', FilmWorkPerson.objects.all().count())
