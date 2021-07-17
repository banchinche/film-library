from . import db
from sqlalchemy.dialects.postgresql import INTEGER
from random import sample, randint


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