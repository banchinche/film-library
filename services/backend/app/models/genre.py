from app.app import db
from sqlalchemy.dialects.postgresql import INTEGER, VARCHAR, TIMESTAMP
from datetime import datetime


class Genre(db.Model):
    __tablename__ = 'Genre'

    id = db.Column(INTEGER, primary_key=True)
    name = db.Column(VARCHAR, nullable=False, unique=True)
    created = db.Column(TIMESTAMP, nullable=False, default=datetime.utcnow())

    def __init__(self, name, date):
        self.name = name
        self.created = date

    def __repr__(self):
        return f'Genre {self.name}'
