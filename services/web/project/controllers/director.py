"""
Director namespace and api-model
"""

from flask_restplus import fields, Namespace, Resource
from project.models import Director



director_namespace = Namespace('directors', description='Movie director')


director_model = director_namespace.model(
    'Director',
    {
        'name': fields.String('blank'),
        'created': fields.String('blank')
    },
)

@director_namespace.route('/get')
class GetDirectors(Resource):
    """
    GET class resource (returns all directors)
    """

    @staticmethod
    def get() -> tuple:
        """
        Get all directors
        Format: JSON
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
  