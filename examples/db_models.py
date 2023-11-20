"""Postgres SQL models"""
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, text
from sqlalchemy.orm import backref, relationship

from .db_common import Base


class User(Base):
    """Basic user definition, no personal data"""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    password = Column(String(128), nullable=False)
    email = Column(String(128))
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    deleted_date = Column(DateTime, default=None)
    status = Column(Integer, nullable=False, index=True, server_default=text("'1'"))


class Profile(Base):
    """Personal data of a User"""

    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True)
    firstname = Column(String(50), index=True)
    lastname = Column(String(50), index=True)
    language = Column(String(3), nullable=False, server_default=text("'en'"))
    address = Column(String(250))
    telephone = Column(String(20))
    timezone = Column(String(30), nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", backref=backref("profiles", uselist=False))
