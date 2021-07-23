"""
Genres namespace and api-model
"""

from flask_restplus import Namespace, Resource
from project.models.genre import Genre


genre_namespace = Namespace('genres', description='Movie genres')


@genre_namespace.route('/get')
class GetGenres(Resource):
    """
    GET class resource (returns all genres)
    """

    @staticmethod
    def get() -> tuple:
        """
        Get all genres
        """

        genres = Genre.query.all()
        if genres:
            genre_list = [
                {
                    'name': genre.name,
                    'created': str(genre.created)
                }
                for genre in genres
            ]
            return {'genres': genre_list}, 200

        return {'Error': 'No genres'}, 404
  