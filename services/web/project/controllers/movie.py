"""
Movie namespace and api-model
"""

from flask_restplus import fields, Namespace


movie_namespace = Namespace('movies', description='Movies from library')

movie_model = movie_namespace.model(
    'Movie',
    {
        'name': fields.String('blank'),
        'rate': fields.Integer('blank'),
        'year': fields.String('blank'),
        'description': fields.String('blank'),
        'poster': fields.String('blank'),
        'director_id': fields.Integer('blank'),
        'user_id': fields.Integer('blank'),
        'created': fields.String('blank')
    },
)
