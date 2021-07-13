"""
Module with ORM models
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.dialects.postgresql import INTEGER, SMALLINT, VARCHAR, TEXT, BOOLEAN
from sqlalchemy.sql.schema import ForeignKeyConstraint

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'User'

    id = db.Column(INTEGER, primary_key=True)
    username = db.Column(VARCHAR, nullable=False, unique=True)
    password = db.Column(VARCHAR, nullable=False)
    is_admin = db.Column(BOOLEAN, nullable=False)
    created = db.Column(VARCHAR, nullable=False, default=str(datetime.utcnow().date()))

    def __init__(self, username, password, is_admin=False, created=str(datetime.utcnow())):
        self.username = username
        self.set_password(password)
        self.is_admin = is_admin
        self.created = created

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'User: {self.username} created: {self.created} admin:{self.is_admin}'


class Director(db.Model):
    __tablename__ = 'Director'

    id = db.Column(INTEGER, primary_key=True)
    name = db.Column(VARCHAR, nullable=False)
    created = db.Column(VARCHAR, nullable=False, default=str(datetime.utcnow()))

    def __init__(self, name, date):
        self.name = name
        self.created = date

    def __repr__(self):
        return f'Director {self.name}'


class Genre(db.Model):
    __tablename__ = 'Genre'

    id = db.Column(INTEGER, primary_key=True)
    name = db.Column(VARCHAR, nullable=False, unique=True)
    created = db.Column(VARCHAR, nullable=False, default=str(datetime.utcnow()))

    def __init__(self, name, date):
        self.name = name
        self.created = date

    def __repr__(self):
        return f'Genre {self.name}'


class Movie(db.Model):
    __tablename__ = 'Movie'

    id = db.Column(INTEGER, primary_key=True)
    name = db.Column(VARCHAR(255), nullable=False)
    rate = db.Column(SMALLINT, nullable=False)
    year = db.Column(SMALLINT, nullable=False)
    description = db.Column(TEXT)
    poster = db.Column(VARCHAR(255), nullable=False)
    director_id = db.Column(INTEGER, nullable=False)
    user_id = db.Column(INTEGER, nullable=False)
    ForeignKeyConstraint(
        ['director_id', 'user_id'],
        ['Director.id', 'User.id'],
        onupdate="CASCADE"
    )
    created = db.Column(VARCHAR, nullable=False, default=str(datetime.utcnow()))

    def __init__(self, name, rate, year, description, image_link, d_id, u_id, date):
        self.name = name
        self.rate = rate
        self.year = year
        self.description = description
        self.poster = image_link
        self.director_id = d_id
        self.user_id = u_id
        self.created = date

    def __repr__(self):
        return f'Movie {self.name} {self.year} {self.rate}/10'


class MovieGenre(db.Model):
    __tablename__ = 'MovieGenre'

    id = db.Column(INTEGER, primary_key=True)
    movie_id = db.Column(INTEGER, nullable=False)
    genre_id = db.Column(INTEGER, nullable=False)
    ForeignKeyConstraint(
        ['movie_id', 'genre_id'],
        ['Movie.id', 'Genre.id'],
        onupdate='CASCADE', ondelete='CASCADE'
    )

    def __init__(self, m_id, g_id):
        self.movie_id = m_id
        self.genre_id = g_id

    def __repr__(self):
        return f'{self.movie_id} : {self.genre_id}'
