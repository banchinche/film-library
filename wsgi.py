# from backend.app.app import app, db
# from backend.app.models.user import User
# from backend.app.models.director import Director
# from backend.app.models.genre import Genre
# from backend.app.models.movie import Movie
# from backend.app.models.movie_genre import MovieGenre
# from flask import Blueprint, request
# @app.route('/home')
# def home():
#     return 'Home'

# user_bp = Blueprint('user_bp', __name__, url_prefix='/user')
# @user_bp.route('', methods=['GET'])
# def index():
#     data = request.args
#     u_id = data.get('id')
#     user = User.query.get(u_id)
#     if user:
#         return {**{'name': user.name, 'passwd': user.password}, **data, }
#     return {'ERROR': 'There is no such user!'}, 404


