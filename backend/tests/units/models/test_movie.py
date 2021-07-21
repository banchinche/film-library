from datetime import datetime
from random import randint
from project.app import app
from project.models.movie import Movie
from faker import Faker
import pytest


fake = Faker()


@pytest.mark.parametrize('name',
                            [
                                ('Great Movie 1'),
                                ('New Marvel Movie')
                            ]
)
def test_movie_init(name):
    with app.app_context():
        movie = Movie(
            name, 
            rate=9, 
            year=2045, 
            description='movie',
            image_link=fake.image_url(),
            d_id=randint(1, 20),
            u_id=randint(1, 20),
            created=fake.date_between(start_date='-5y')
        )
        assert movie.name == name
        assert movie.rate == 9
        assert movie.year == 2045
        assert movie.created != datetime.utcnow()

@pytest.mark.parametrize('name',
                            [
                                ('Test Movie Name')
                            ]
)
def test_movie_insert(name):
    with app.app_context():
        if not Movie.exists(name):
            movie = Movie(
                name, 
                rate=9, 
                year=2045, 
                description='movie',
                image_link=fake.image_url(),
                d_id=randint(1, 20),
                u_id=randint(1, 20),
                created=fake.date_between(start_date='-5y')
            )
            movie.save()
            assert Movie.exists(name)


            name = fake.job(),
            rate = randint(1, 10),
            year = randint(1820, 2019),
