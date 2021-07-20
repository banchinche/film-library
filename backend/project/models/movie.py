from . import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import VARCHAR, INTEGER, SMALLINT, TEXT, TIMESTAMP
from sqlalchemy import func, String, ARRAY
from random import randint
from .user import User
from .director import Director
from .genre import Genre
from .movie_genre import MovieGenre



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

    def __init__(self, name, rate, year, description, image_link, d_id, u_id, created=datetime.utcnow):
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
    
    def delete(self):
        db.session.delete(self)
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
    def exists(cls, name):
        return Movie.query.filter(Movie.name == name).first()
