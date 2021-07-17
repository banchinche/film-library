from . import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import VARCHAR, INTEGER, TIMESTAMP


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
        return Genre.query.get

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()    
    @classmethod
    def exists(cls, name):
        return Genre.query.filter(Genre.name == name).first()