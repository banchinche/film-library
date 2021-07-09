from app.app import db
from sqlalchemy.dialects.postgresql import INTEGER, VARCHAR, TIMESTAMP
from sqlalchemy.sql.schema import ForeignKeyConstraint


class MovieGenre(db.Model):
    __tablename__ = 'MovieGenre'

    id = db.Column(INTEGER, primary_key=True)
    movie_id = db.Column(VARCHAR, nullable=False)
    genre_id = db.Column(TIMESTAMP, nullable=False)
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
