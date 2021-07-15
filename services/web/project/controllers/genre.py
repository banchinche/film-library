"""
Genres namespace and api-model
"""

from flask_restplus import fields, Namespace, Resource
from project.models import Genre


genre_namespace = Namespace('genres', description='Movie genres')


genre_model = genre_namespace.model(
    'Genre',
    {
        'name': fields.String('blank'),
        'created': fields.String('blank')
    },
)

@genre_namespace.route('/get')
class GetGenres(Resource):
    """
    GET class resource (returns all genres)
    """

    @staticmethod
    def get() -> tuple:
        """
        Get all genres
        Format: JSON
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
  