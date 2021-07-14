"""
Director namespace and api-model
"""

from flask_restplus import fields, Namespace



api = Namespace('directors', description='Movie director')


director_model = api.model(
    'Director',
    {
        'name': fields.String('blank'),
        'created': fields.String('blank')
    },
)
