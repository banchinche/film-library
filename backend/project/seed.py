from faker import Faker
from project.models.user import User
from project.models.director import Director
from project.models.genre import Genre
from project.models.movie import Movie
from project.models.movie_genre import MovieGenre


def seed(users, directors, movies):
    fake = Faker()
    genres = ('Action', 'Comedy', 'Drama', 'Fantasy', 'Horror', 'Mystery', 'Romance', 'Thriller')

    # does not guarantee unique usernames !!! (possible to fail seeding)
    for _ in range(users):
        User.seed(fake)

    Director.add_unknown(fake)
    for _ in range(directors):
        Director.seed(fake)


    for g in genres:
        Genre.seed(g, fake)

    for _ in range(movies):
        Movie.seed(directors, users, fake)

    for movie_id in range(1, movies + 1):
        MovieGenre.seed(movie_id, len(genres))
