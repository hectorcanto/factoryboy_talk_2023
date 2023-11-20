from faker import Faker as FakeIt
from sqlalchemy import orm

FAKE = FakeIt()

TestSession = orm.scoped_session(orm.sessionmaker())
"""Global scoped session (thread-safe) for tests"""
# From https://factoryboy.readthedocs.io/en/stable/orms.html#managing-sessions
