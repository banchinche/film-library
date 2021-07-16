"""
Module with ORM models
"""
from random import randint, sample
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
from sqlalchemy.sql.sqltypes import INT
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.dialects.postgresql import INTEGER, SMALLINT, VARCHAR, TEXT, BOOLEAN, TIMESTAMP, ARRAY
# from sqlalchemy.sql.schema import ForeignKeyConstraint
from sqlalchemy import func, String

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'User'

    id = db.Column(INTEGER, primary_key=True)
    username = db.Column(VARCHAR, nullable=False, unique=True)
    password = db.Column(VARCHAR, nullable=False)
    is_admin = db.Column(BOOLEAN, nullable=False)
    created = db.Column(TIMESTAMP, nullable=False, default=datetime.utcnow)
    movies = db.relationship('Movie', backref='Movie')

    def __init__(self, username, password, is_admin=False, created=datetime.utcnow):
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
    
    @classmethod
    def seed(cls, fake):
        user = User(
            username = fake.name(),
            password = generate_password_hash(fake.password()),
            is_admin = False,
            created = fake.date_between(start_date='-5y')
        )
        user.save()

    def save(self):
        db.session.add(self)
        db.session.commit()

class Director(db.Model):
    __tablename__ = 'Director'

    id = db.Column(INTEGER, primary_key=True)
    name = db.Column(VARCHAR, nullable=False)
    created = db.Column(TIMESTAMP, nullable=False, default=datetime.utcnow)
    directed_movie = db.relationship('Movie', backref='directed_movie')

    def __init__(self, name, created):
        self.name = name
        self.created = created

    def __repr__(self):
        return f'Director {self.name}'

    @classmethod
    def seed(cls, fake):
        director = Director(
            name = fake.name(),
            created = fake.date_between(start_date='-5y')
        )
        director.save()
    
    @classmethod
    def add_unknown(cls, fake):
        director = Director(
            name = 'unknown',
            created=fake.date()
        )
        director.save()

    def save(self):
        db.session.add(self)
        db.session.commit()


class Genre(db.Model):
    __tablename__ = 'Genre'

    id = db.Column(INTEGER, primary_key=True)
    name = db.Column(VARCHAR, nullable=False, unique=True)
    created = db.Column(TIMESTAMP, nullable=False, default=datetime.utcnow)

    def __init__(self, name, created):
        self.name = name
        self.created = created

    def __repr__(self):
        return f'Genre {self.name}'
    
    @classmethod
    def seed(cls, genre_name, fake):
        genre = Genre(
                name = genre_name,
                created = fake.date_between(start_date='-5y')
                )
        genre.save()

    @classmethod
    def all_genres(cls):
        pass

    def save(self):
        db.session.add(self)
        db.session.commit()


class Movie(db.Model):
    __tablename__ = 'Movie'

    id = db.Column(INTEGER, primary_key=True)
    name = db.Column(VARCHAR(255), nullable=False)
    rate = db.Column(SMALLINT, nullable=False)
    year = db.Column(SMALLINT, nullable=False)
    description = db.Column(TEXT)
    poster = db.Column(VARCHAR(255), nullable=False)
    director_id = db.Column(
        INTEGER,
        db.ForeignKey('Director.id', ondelete='SET null'),
        nullable=True
    )
    user_id = db.Column(INTEGER, db.ForeignKey('User.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    created = db.Column(TIMESTAMP, nullable=False, default=datetime.utcnow)
    genres = db.relationship('Genre', secondary='MovieGenre')

    def __init__(self, name, rate, year, description, image_link, d_id, u_id, created):
        self.name = name
        self.rate = rate
        self.year = year
        self.description = description
        self.poster = image_link
        self.director_id = d_id
        self.user_id = u_id
        self.created = created

    def __repr__(self):
        return f'Movie {self.name} {self.year} {self.rate}/10'
    
    @classmethod
    def seed(cls, directors, users, fake):
        movie = Movie(
            name = fake.job(),
            rate = randint(1, 10),
            year = randint(1820, 2019),
            description = fake.paragraph(nb_sentences=4, variable_nb_sentences=False),
            image_link = fake.image_url(),
            d_id = randint(1, directors),
            u_id = randint(1, users),
            created = fake.date_between(start_date='-1y')
        )
        movie.save()

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def all_movies(cls) -> tuple:
        genres_array = func.array_agg(Genre.name, type=ARRAY(String)).label('genres')
        return (
            db.session.query(Movie, Director, User.username, genres_array)
            .select_from(Movie)
            .join(MovieGenre)
            .join(Genre)
            .join(Director)
            .join(User)
            .group_by(Movie.id, Director.id, User.username)
        )

    @classmethod
    def from_id(cls, movie_id) -> tuple:
        all_movies = cls.all_movies()
        return all_movies.filter(movie_id)


class MovieGenre(db.Model):
    __tablename__ = 'MovieGenre'

    id = db.Column(INTEGER, primary_key=True)
    movie_id = db.Column(INTEGER, db.ForeignKey('Movie.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    genre_id = db.Column(INTEGER, db.ForeignKey('Genre.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    
    def __init__(self, m_id, g_id):
        self.movie_id = m_id
        self.genre_id = g_id

    def __repr__(self):
        return f'{self.movie_id} : {self.genre_id}'

    @classmethod
    def seed(cls, movie_id, genres):
        m_genres = tuple(set(sample(range(1, genres + 1), randint(1, 3))))
        for g in m_genres:
            movie_genre = MovieGenre(
                m_id = movie_id,
                g_id = g
            )
            movie_genre.save()

    def save(self):
        db.session.add(self)
        db.session.commit()