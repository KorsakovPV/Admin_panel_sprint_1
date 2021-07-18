import datetime

from factory import Faker, fuzzy
from factory.django import DjangoModelFactory
from pytz import UTC

from movies.models import Person, FilmWorkPerson, RoleType


class PersonFactory(DjangoModelFactory):
    full_name = Faker('name')
    birth_date = Faker('date')
    created_at = fuzzy.FuzzyDateTime(start_dt=datetime.datetime(1940, 1, 1, tzinfo=UTC))

    class Meta:
        model = Person


class FilmWorkPersonFactory(DjangoModelFactory):
    role = fuzzy.FuzzyChoice(RoleType)
    created_at = fuzzy.FuzzyDateTime(start_dt=datetime.datetime(1940, 1, 1, tzinfo=UTC))

    class Meta:
        model = FilmWorkPerson
