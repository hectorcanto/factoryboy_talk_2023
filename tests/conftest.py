import os

import factory
import pytest
import sqlalchemy
from pytest_factoryboy import register
from sqlalchemy.exc import PendingRollbackError
from sqlalchemy_utils import create_database, database_exists

from examples.db_common import Base

from .common import TestSession
from .user_factories import (
    AdminFactory,
    DbProfileFactory,
    DbProfileFactory2,
    DbUserFactory,
    ProfileFactory,
)


@pytest.fixture(scope="session", name="db_session", autouse=True)
def create_tables():
    db_url = os.environ.get("DB_URL")
    engine = sqlalchemy.create_engine(db_url)

    if not database_exists(engine.url):
        create_database(engine.url)

    tables = reversed(Base.metadata.sorted_tables)
    Base.metadata.create_all(bind=engine, tables=tables, checkfirst=True)
    yield None
    Base.metadata.drop_all(bind=engine, tables=tables)


@pytest.mark.usefixtures("create_tables")
@pytest.fixture(scope="session", name="db_session", autouse=True)
def global_db_session():
    """SQLA session to be injected in tests, used also in test body

    Reset database once all tests are complete

    See https://factoryboy.readthedocs.io/en/stable/orms.html#sqlalchemy
    for more detail.
    """

    engine = sqlalchemy.create_engine(os.environ.get("DB_URL"))
    TestSession.configure(bind=engine)
    tables = reversed(Base.metadata.sorted_tables)
    Base.metadata.create_all(bind=engine, tables=tables, checkfirst=True)
    yield TestSession
    Base.metadata.drop_all(bind=engine, tables=tables)
    TestSession.close()


@pytest.fixture
def reset_db(db_session):
    """Reset all database table data in the test environment"""
    try:
        for table in reversed(Base.metadata.sorted_tables):
            db_session.execute(table.delete())
        db_session.commit()
    except PendingRollbackError:
        # Protection against open rollbacks in failed tests
        db_session.rollback()
        for table in reversed(Base.metadata.sorted_tables):
            db_session.execute(table.delete())
        db_session.commit()


register(AdminFactory, "admin")
register(DbUserFactory, "user1", email="user1@hello.es")
register(DbUserFactory, "user2", status=0)
register(DbProfileFactory2, "profile")


@register
class DummyFactory(factory.DictFactory):
    example = 1


def pytest_collection_modifyitems(items):
    """Adds marker to all tests in these submodules

    Usage:
        pytest -m unit
        pytest -m "not integration"

    To silence warnings, markers are registered with pytest_configure, below
    """
    for item in items:
        if "/integration/" in str(item.module):
            item.add_marker("integration")
        elif "/unit/" in str(item.module):
            item.add_marker("unit")
        elif "/smoke/" in str(item.module):
            item.add_marker("smoke")
        elif "/api/" in str(item.module):
            item.add_marker("api")


def pytest_configure(config):
    markers = [
        "smoke: basic tests",
        "unit: unitary tests",
        "integration: integration tests, needs docker",
        "api: tests from outside the API",
        "current: in development",
        "first: run first",  # pytest-ordering
        "last: run last",  # pytest-ordering
    ]
    for line in markers:
        config.addinivalue_line("markers", line)


# TODO mute SQLALCHEMY_SILENCE_UBER_WARNING=1
