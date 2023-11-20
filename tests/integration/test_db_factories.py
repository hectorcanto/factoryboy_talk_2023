import factory
import pytest

from examples.db_models import Profile, User
from tests.user_factories import (
    DbProfileFactory,
    DbUserFactory,
    DeletedUserFactory,
    ProfileFactory,
    UserFactory,
)

pytestmark = pytest.mark.usefixtures("reset_db")


def test_user_factory(db_session):
    user = UserFactory()
    db_session.add(user)
    db_session.commit()

    assert db_session.query(User).count() == 1
    assert db_session.query(Profile).count() == 0


def test_related_factory(db_session):
    profile = ProfileFactory()
    db_session.add(profile)
    db_session.commit()

    assert db_session.query(User).count() == 1
    assert db_session.query(Profile).count() == 1

    user = db_session.query(User).first()

    assert user.username.startswith(f"{profile.firstname}_{profile.lastname}")


def test_batch_factory(db_session):
    users = UserFactory.create_batch(size=5)
    db_session.add_all(users)
    db_session.commit()

    assert db_session.query(User).count() == 5


def test_batch_related_factory(db_session):
    """Creating a batch of 5 profiles also creates"""
    profiles = DbProfileFactory.create_batch(size=5)

    assert db_session.query(Profile).count() == 5
    assert db_session.query(User).count() == 5


def test_batch_with_iterator(db_session):
    """We can use iterators in batche"""
    names = ["Adrian", "Braulio", "Carlos", "Daniel", "Ernesto"]
    DbProfileFactory.create_batch(size=10, firstname=factory.Iterator(names))
    assert db_session.query(Profile).filter(Profile.firstname == "Adrian").count() == 2


def test_stub_factory(db_session):
    """stubs are not flushed or committed"""
    user = DbUserFactory.stub()
    print(user.__dict__)
    assert db_session.query(User).count() == 0


def test_registered_factories(admin, user1, user2):
    assert admin.email.startswith("admin")
    assert user1.email.startswith("user1")
    assert user2.status == 0


def test_nested_factory_parameter(db_session):
    DbProfileFactory(user__email="test_nested@hello.com")
    assert db_session.query(User).first().email == "test_nested@hello.com"


@pytest.mark.parametrize("profile__lastname", ("Garcia", "Rodriguez"))
def test_parametrized_factory(profile):
    assert profile.lastname in ["Garcia", "Rodriguez"]
