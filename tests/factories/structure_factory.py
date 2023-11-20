from datetime import datetime, timedelta, timezone
from enum import Enum
from random import randint
from typing import NamedTuple

import arrow
from factory import Factory, Faker, LazyAttribute, LazyFunction, SubFactory
from factory.fuzzy import FuzzyChoice, FuzzyDateTime, FuzzyFloat, FuzzyText
from faker import Faker as FakeIt
from pydantic import BaseModel

from .dict_generator import generate_dict_factory

fake_it = FakeIt()  # Another way to use Faker
YEAR_IN_DAYS = 365


class Category(str, Enum):
    backend = "BackEnd"
    frontend = "FrontEnd"
    qa = "QA"


class Inner(NamedTuple):
    inner_value: float


class InnerFactory(Factory):
    inner = FuzzyFloat(1, 99.9)


class Structure(BaseModel):
    # Could be Dataclass, Pydantic model or Marshmallow class
    # Could also a SQLAlchemy, Django or pyMongo model

    id: str  # UUID
    active: bool
    value: int
    salary: float
    text: str
    category: str
    ip: str

    first_name: str
    last_name: str
    full_name: str
    username: str
    email: str
    password: str

    created_at: datetime
    updated_at: int
    last_login: datetime

    nested: Inner


class StructureFactory(Factory):
    class Meta:
        model = Structure

    nested = SubFactory(InnerFactory)

    id = Faker("uuid4")
    active: bool = True
    value: int = LazyFunction(lambda: randint(1, 1000))
    salary: float = FuzzyFloat(20_000, 50_000, 2)
    text = Faker("sentence", nb_words=5)
    category = FuzzyChoice(Category.__members__)
    ip = Faker("ipv4")

    first_name = Faker("first_name")
    last_name = Faker("last_name")
    full_name = LazyAttribute(lambda self: self.first_name + " " + self.last_name)
    username = LazyAttribute(lambda self: self.full_name.replace(" ", "_"))
    email = LazyAttribute(lambda o: f"{o.username}@{fake_it.domain_name()}")
    password = FuzzyText(length=16)

    created_at = FuzzyDateTime(
        datetime.now(tz=timezone.utc) - timedelta(5 * YEAR_IN_DAYS),
        datetime.now(tz=timezone.utc) - timedelta(1 * YEAR_IN_DAYS),
    )
    updated_at = Faker(
        "unix_time",
        start_datetime=arrow.utcnow().shift(weeks=-3).datetime,
        end_datetime=datetime.utcnow(),
    )
    # arrow  is a good human-friendly tool to handle datetimes
    last_login = LazyFunction(lambda: fake_it.date_time_between("-1m", "-1w"))
    # we can call faker lazyly instead of the introspected version


StructureDictFactory = generate_dict_factory(StructureFactory)
