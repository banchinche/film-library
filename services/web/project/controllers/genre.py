"""
Genres namespace and api-model
"""


from flask_restplus import fields,Namespace



api = Namespace('genres', description='Movie genres')


genre_model = api.model(
    'Genre',
    {
        'name': fields.String('blank'),
        'created': fields.String('blank')
    },
)
