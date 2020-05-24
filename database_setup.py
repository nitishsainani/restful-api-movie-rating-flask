import sys

# for creating the mapper code
from sqlalchemy import Column, ForeignKey, Integer, String

# for configuration and class code
from sqlalchemy.ext.declarative import declarative_base

# for creating foreign key relationship between the tables
from sqlalchemy.orm import relationship

# for configuration
from sqlalchemy import create_engine

# create declarative_base instance
Base = declarative_base()


# We will add classes here
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    password = Column(String(250), nullable=False)
    children = relationship("Movie")

    @property
    def serialize(self):
        return {
            'name': self.name,
            'email': self.email,
            'id': self.id
        }


class Movie(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String(250), nullable=False)
    created_by = Column(Integer, ForeignKey('users.id'))

    @property
    def serialize(self):
        return {
            'title': self.title,
            'created_by': self.created_by,
            'id': self.id
        }


class Rating(Base):
    __tablename__ = 'ratings'

    id = Column(Integer, primary_key=True)
    value = Column(Integer, nullable=False)
    movie_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)

    @property
    def serialize(self):
        return {
            'value': self.value,
            'user_id': self.user_id,
            'movie_id': self.movie_id,
            'id': self.id
        }


# creates a create_engine instance at the bottom of the file
engine = create_engine('sqlite:///movies-collection.db')
Base.metadata.create_all(engine)
