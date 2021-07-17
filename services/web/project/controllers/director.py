"""
Director namespace and api-model
"""

from flask_restplus import Namespace, Resource
from project.models import Director



director_namespace = Namespace('directors', description='Movie director')


@director_namespace.route('/get')
class GetDirectors(Resource):
    """
    GET class resource (returns all directors)
    """

    @staticmethod
    def get() -> tuple:
        """
        Get all directors
        """

        directors = Director.query.all()
        if directors:
            director_list = [
                {
                    'name': director.name,
                    'created': str(director.created)
                }
                for director in directors
            ]
            return {'directors': director_list}, 200
        return {'Error': 'No genres'}, 404
  