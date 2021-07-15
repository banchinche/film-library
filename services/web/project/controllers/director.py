"""
Director namespace and api-model
"""

from flask_restplus import fields, Namespace



director_namespace = Namespace('directors', description='Movie director')


director_model = director_namespace.model(
    'Director',
    {
        'name': fields.String('blank'),
        'created': fields.String('blank')
    },
)
