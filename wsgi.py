from app.app import app, db
from app.models.user import User
from app.models.director import Director
from app.models.genre import Genre
from app.models.movie import Movie
from app.models.movie_genre import MovieGenre
from flask import Blueprint, request
@app.route('/home')
def home():
    return 'Home'

user_bp = Blueprint('user_bp', __name__, url_prefix='/user')
@user_bp.route('', methods=['GET'])
def index():
    data = request.args
    u_id = data.get('id')
    user = User.query.get(u_id)
    if user:
        return {**{'name': user.name, 'passwd': user.password}, **data, }
    return {'ERROR': 'There is no such user!'}, 404


if __name__ == '__main__':
    # app.config['DEBUG'] = True
    db.create_all(User, Director, Genre, Movie, MovieGenre)
    db.session.add(User(name='name', password='pass', is_admin=True, date='2021-08-08'))
    db.session.commit()
    app.run()
