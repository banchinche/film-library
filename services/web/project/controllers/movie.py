"""
Movie namespace and api-model
"""
from flask import request
from flask_restplus import fields, Namespace, Resource
from project.models import db, Movie, Genre, Director
from project.searching import get_paginated_list, search_arguments


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
    def apply_search(
        movies, sort, genre, f_from, f_to, director, s_string
        ):
        # search string and filters
        if s_string:
            movies = movies.filter(Movie.name.ilike(f'%{s_string}%'))
        if director:
            movies = movies.filter(Director.name == director)
        if genre:
            movies = movies.filter(Genre.name.contains(genre))
        # year between
        if f_from and f_to:
            movies = movies.filter(Movie.year.between(f_from, f_to))
        # sort by rate and by year 
        if sort:
            if sort == 'rate-ascending':
                movies = movies.order_by(Movie.rate.asc())
            elif sort == 'rate-descending':
                movies = movies.order_by(Movie.rate.desc())
            elif sort == 'year-ascending':
                movies = movies.order_by(Movie.year.asc())
            else:
                movies = movies.order_by(Movie.year.desc())
        return movies


    @staticmethod
    @movie_namespace.expect(search_arguments, validate=True)
    def get() -> tuple:
        """Get data about all movies
        Format: json
        """

        args = request.args
        start = args.get('start', 1)
        per_page = args.get('per_page', 10)
        sorting = args.get('sorting', None)
        filtered_genre = args.get('filter_genre', None)
        filtered_from = args.get('filter_first_date', None)
        filtered_to = args.get('filter_second_date', None)
        filtered_director = args.get('filter_director', None)
        search_string = args.get('search_string', None)
        
        movies = Movie.all_movies()
        movies = GetMovies.apply_search(
            movies, 
            sorting, 
            filtered_genre, 
            filtered_from,
            filtered_to,
            filtered_director,
            search_string
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
                    'username': movie.username,
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

        return {'Error': 'Movies were not found'}, 404



