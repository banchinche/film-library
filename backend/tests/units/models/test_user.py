from datetime import datetime
from project.app import app
from project.models.user import User
from faker import Faker
from werkzeug.security import check_password_hash
import pytest


fake = Faker()


@pytest.mark.parametrize('username, password',
                            [
                                ('username1',  'user1-pass'),
                                ('user2', 'great_pass123')
                            ]
)
def test_user_init(username, password):
    with app.app_context():
        user = User(username=username, password=password)
        assert user.username == username
        assert check_password_hash(user.password, password)
        assert user.created != datetime.utcnow()

@pytest.mark.parametrize('username',
                            [
                                ('user123'),
                                ('not_admin777'),
                                ('qwerty321')
                            ]
)
def test_user_insert(username):
    with app.app_context():
        if not User.exists(username):
            fake_pass = fake.password()
            fake_date = fake.date()
            user = User(username, fake_pass, False, fake_date)
            user.save()
            assert User.exists(username)
