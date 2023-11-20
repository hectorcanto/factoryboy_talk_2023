from datetime import date, datetime, timedelta
from random import randint

from factory import Faker, LazyAttribute, LazyFunction, SelfAttribute, SubFactory
from factory.fuzzy import FuzzyChoice, FuzzyInteger, FuzzyText

from examples.db_models import Profile, User

from .common import FAKE, BaseFactory

LANG_CODES = ["en", "es", "gal", "pt", "fr"]


class UserFactory(BaseFactory):
    """Factory for creating mock User objects"""

    class Meta:
        model = User
        sqlalchemy_session_persistence = None
        # could be `commit`, `flush` or None

    class Params:  # NOTE aux fields in params, won't be rendered
        """Extra params for the factory"""

        first = Faker("first_name_female", locale="es")
        last = Faker("last_name", locale="es")
        # TODO Traits and Maybe

    id = FuzzyInteger(100, 10000)
    username = LazyAttribute(lambda obj: f"{obj.first}_{obj.last}_{randint(1, 1000)}")
    password = FuzzyText(length=16)
    email = LazyAttribute(lambda obj: f"{obj.first}.{obj.last}@{FAKE.domain_name()}")
    created_at = Faker("date_time_between", start_date=date(2015, 1, 1), end_date="-1y")
    # Other fakers: date_this_year, date_this_decade,
    updated_at = LazyFunction(datetime.now)
    status = 1


class DbUserFactory(UserFactory):
    class Meta:
        sqlalchemy_session_persistence = "commit"


class ProfileFactory(BaseFactory):
    class Meta:
        model = Profile
        sqlalchemy_session_persistence = None
        # could be `commit`, `flush` or None

    id = FuzzyInteger(100, 10000)
    firstname = Faker("first_name_female", locale="en")
    lastname = Faker("last_name", locale="en")
    language = FuzzyChoice(LANG_CODES)
    address = Faker("address")
    telephone = Faker("phone_number", locale="es")
    timezone = "Europe/Madrid"
    # NOTE multi-level references
    user = SubFactory(  # NOTE that we set user not user_id
        UserFactory,
        first=SelfAttribute("..firstname"),
        last=SelfAttribute("..lastname"),
    )


class DbProfileFactory(ProfileFactory):
    class Meta:
        sqlalchemy_session_persistence = "commit"


class DbProfileFactory2(DbProfileFactory):
    user = None


class DeletedUserFactory(BaseFactory):
    """A factory for a soft-deleted user"""

    deleted_at = LazyAttribute(
        lambda self: datetime.fromtimestamp(self.created_at) + timedelta(days=370)
    )
    updated_at = SelfAttribute("deleted_at")
    status = 0


class AdminFactory(DbUserFactory):
    email = "admin@example.net"
