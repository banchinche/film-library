from app.app import db
from sqlalchemy.dialects.postgresql import INTEGER, VARCHAR, TIMESTAMP
from datetime import datetime


class Poster(db.Model):
    __tablename__ = 'Poster'

    id = db.Column(INTEGER, primary_key=True)
    link = db.Column(VARCHAR, unique=True)
    created = db.Column(TIMESTAMP, nullable=False)

    def __init__(self, link):
        self.link = link
        self.created = datetime.utcnow()

    def __repr__(self):
        return f'Poster {self.link}'
