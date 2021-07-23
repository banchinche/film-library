from . import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.dialects.postgresql import VARCHAR, INTEGER, BOOLEAN, TIMESTAMP


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
            password = fake.password(),
            is_admin = False,
            created = fake.date_between(start_date='-5y')
        )
        user.save()

    def save(self):
        db.session.add(self)
        db.session.commit()
    


    @classmethod
    def exists(cls, username):
        return User.query.filter(User.username == username).first()
