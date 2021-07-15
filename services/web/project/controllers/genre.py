"""
Genres namespace and api-model
"""


from flask_restplus import fields, Namespace



genre_namespace = Namespace('genres', description='Movie genres')


genre_model = genre_namespace.model(
    'Genre',
    {
        'name': fields.String('blank'),
        'created': fields.String('blank')
    },
)
