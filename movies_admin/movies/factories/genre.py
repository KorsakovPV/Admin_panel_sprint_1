import datetime

from factory import Faker, fuzzy
from factory.django import DjangoModelFactory
from pytz import UTC

from movies.models import Genre, FilmWorkGenre


class GenreFactory(DjangoModelFactory):
    name = Faker('company')
    description = Faker('sentence', nb_words=128, variable_nb_words=True)
    created_at = fuzzy.FuzzyDateTime(start_dt=datetime.datetime(1940, 1, 1, tzinfo=UTC))

    class Meta:
        model = Genre


class FilmWorkGenreFactory(DjangoModelFactory):
    created_at = fuzzy.FuzzyDateTime(start_dt=datetime.datetime(1940, 1, 1, tzinfo=UTC))

    class Meta:
        model = FilmWorkGenre
