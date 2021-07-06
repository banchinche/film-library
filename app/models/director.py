from app.app import db
from sqlalchemy.dialects.postgresql import INTEGER, VARCHAR, TIMESTAMP
from datetime import datetime


class Director(db.Model):
    __tablename__ = 'Director'

    id = db.Column(INTEGER, primary_key=True)
    name = db.Column(VARCHAR, nullable=False)
    created = db.Column(TIMESTAMP, nullable=False, default=datetime.utcnow())

    def __init__(self, name, date):
        self.name = name
        self.created = date

    def __repr__(self):
        return f'Director {self.name}'
