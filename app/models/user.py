from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from sqlalchemy.dialects.postgresql import INTEGER, VARCHAR, TIMESTAMP, BOOLEAN
from app.app import db


class User(db.Model, UserMixin):
    __tablename__ = 'User'

    id = db.Column(INTEGER, primary_key=True)
    name = db.Column(VARCHAR, nullable=False, unique=True)
    password = db.Column(VARCHAR, nullable=False)
    is_admin = db.Column(BOOLEAN, nullable=False)
    created = db.Column(TIMESTAMP, nullable=False, default=datetime.utcnow())

    def __init__(self, name, password, is_admin, date):
        self.name = name
        self.password = password
        self.is_admin = is_admin
        self.created = date

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'User: {self.name} created: {self.created} admin:{self.is_admin}'
