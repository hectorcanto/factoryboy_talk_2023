import factory
from faker import Faker
from sqlalchemy import orm

TestSession = orm.scoped_session(orm.sessionmaker())
"""Global scoped session (thread-safe) for tests"""
# From https://factoryboy.readthedocs.io/en/stable/orms.html#managing-sessions

FAKE = Faker()


class BaseFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        abstract = True
        sqlalchemy_session = TestSession
