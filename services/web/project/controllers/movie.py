"""
Movie namespace and api-model
"""
from flask import request
from marshmallow import ValidationError
from datetime import datetime
from flask_restplus import fields, Namespace, Resource
from project.models import db, Movie, MovieGenre, Genre, Director, User
from marshmallow import ValidationError
from sqlalchemy import String, func
from sqlalchemy.dialects.postgresql import ARRAY
from project.pagination import get_paginated_list, pagination_arguments


movie_namespace = Namespace('movies', description='Movies from library')

movie_model = movie_namespace.model(
    'Movie',
    {
        'name': fields.String,
        'rate': fields.Integer,
        'year': fields.Integer,
        'genres': fields.List,
        'description': fields.String,
        'poster': fields.String,
        'director-name': fields.String,
        'username': fields.String,
        'created': fields.String
    },
)

@movie_namespace.route("/get/")
class GetMovies(Resource):
    """Method GET all movies"""

    @staticmethod
    @movie_namespace.expect(pagination_arguments)
    def get() -> tuple:
        """Get data about all movies
        Format: json
        """
        start = request.args['start']
        per_page = request.args['per_page']
        genre_agg = func.array_agg(Genre.name, type=ARRAY(String)).label(
            'genres'
        )
        movies = (
            db.session.query(Movie, Director, User.username, genre_agg)
                .select_from(Movie)
                .join(MovieGenre)
                .join(Genre)
                .join(User)
                .join(Director)
                .group_by(Movie.id, Director.id, User.username)
                .all()
        )
        if movies:
            result = [
                {
                    'name': movie[0].name,
                    'rate': movie[0].rate,
                    'year': movie[0].year,
                    'genres': movie.genres,
                    'description': movie[0].description,
                    'poster': movie[0].poster,
                    'director-name': movie[1].name,
                    'user': movie.username,
                    'created': str(movie[0].created)
                }
                for movie in movies
            ]
            return (
                get_paginated_list(
                    result,
                    "",
                    start=start,
                    limit=per_page
                ),
                200,
            )

        return {"Error": "Films was not found"}, 404