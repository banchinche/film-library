from . import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import VARCHAR, INTEGER, TIMESTAMP


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
    
    @classmethod
    def exists(cls, name):
        return Director.query.filter(Director.name == name).first()