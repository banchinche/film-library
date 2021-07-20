from datetime import datetime
from project.app import app
from project.models.director import Director
from faker import Faker
import pytest


fake = Faker()


@pytest.mark.parametrize('name',
                            [
                                ('Genius Director'),
                                ('New Director')
                            ]
)
def test_director_init(name):
    with app.app_context():
        director = Director(name)
        assert director.name == name
        assert director.created != datetime.utcnow()

@pytest.mark.parametrize('name',
                            [
                                ('Test Director Name')
                            ]
)
def test_director_insert(name):
    with app.app_context():
        if not Director.exists(name):
            director = Director(
                name,
                created=fake.date()
            )
            director.save()
            assert Director.exists(name)
