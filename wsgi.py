from app.app import app, db
from app.models.user import User
from app.models.director import Director
from app.models.genre import Genre
from app.models.movie import Movie
from app.models.movie_genre import MovieGenre

@app.route('/home')
def home():
    return 'Home'

if __name__ == '__main__':
    # app.config['DEBUG'] = True
    db.create_all(User, Director, Genre, Movie, MovieGenre)
    app.run()
