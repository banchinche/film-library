from datetime import datetime
from project.app import app
from project.models.genre import Genre
from faker import Faker
import pytest


fake = Faker()


@pytest.mark.parametrize('name',
                            [
                                ('New Genre'),
                            ]
)
def test_genre_init(name):
    with app.app_context():
        genre = Genre(name)
        assert genre.name == name
        assert genre.created != datetime.utcnow()

@pytest.mark.parametrize('name',
                            [
                                ('Test Genre Name')
                            ]
)
def test_genre_insert(name):
    with app.app_context():
        if not Genre.exists(name):
            genre = Genre(
                name,
                created=fake.date()
            )
            genre.save()
            assert Genre.exists(name)
