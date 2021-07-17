"""
Movie namespace and api-model
"""
from datetime import datetime

from flask import request
from flask_login import login_required, current_user
from flask_restplus import fields, Namespace, Resource
from project.models import Movie, Genre, Director, MovieGenre
from project.searching import get_paginated_list, search_arguments
from marshmallow import ValidationError



movie_namespace = Namespace('movies', description='Movies from library')

movie_model = movie_namespace.model(
    'Movie',
    {
        'name': fields.String,
        'rate': fields.Integer,
        'year': fields.Integer,
        'genres': fields.List(fields.String),
        'description': fields.String,
        'poster': fields.String,
        'director-name': fields.String,
    },
)


@movie_namespace.route('/get/<string:movie_name>')
class GetMovieId(Resource):
    """
    Get movie id from it name
    """

    @staticmethod
    def get(movie_name: str) -> tuple:
        movie = Movie.exists(movie_name)
        if movie:
            return {
                'id': movie.id,
                'name': f'{movie_name}'
            }, 200
        return {'Error': 'No such movie'}, 404


@movie_namespace.route('/get')
class GetMovies(Resource):
    """
    Method GET all movies
    """

    @staticmethod
    def apply_search(
        movies, sort, genre, f_from, f_to, director, s_string
        ):
        """
        Applies settings of search to movies
        """
        # search string and filters
        if s_string:
            movies = movies.filter(Movie.name.ilike(f'%{s_string}%'))
        if director:
            movies = movies.filter(Director.name == director)
        # bug (finds just direct entry i.e Action doesnt find Action + Horror)
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
        """
        Get data about all movies
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
                    'id': movie[0].id,
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

        return {'Error': 'Movies were not found.'}, 404


@movie_namespace.route('/post')
class PostMovie(Resource):
    """
    Posts new movie
    """
    @staticmethod
    @login_required
    @movie_namespace.expect(movie_model)
    def post() -> tuple:
        """
        Creates new movie
        """
        args = request.json
        name = args.get('name', None)
        rate = args.get('rate', None)
        year = args.get('year', None)
        genres = args.get('genres', None)
        description = args.get('description', None)
        poster = args.get('poster', None)
        director_name = args.get('director-name', 'unknown')
        if Movie.exists(name):
            return {'Error': 'Movie already exists.'}, 409
        try:
            if current_user.id:
                director = Director.exists(director_name)
                if not director:
                    new_director = Director(director_name, datetime.utcnow())
                    new_director.save()
                    director = new_director
                
                movie = Movie(
                    name = name,
                    rate = rate,
                    year = year,
                    description = description,
                    image_link = poster,
                    d_id = director.id,
                    u_id = current_user.id,
                    created = datetime.utcnow()

                )
                movie.save()
                for g in genres:
                    genre = Genre.exists(g)
                    if not genre:
                        genre = Genre(
                            name = g,
                            created = datetime.utcnow()
                        )
                        genre.save()
                    movie_genre = MovieGenre(
                        m_id = movie.id,
                        g_id = genre.id
                    )
                    movie_genre.save()
                return {'Notification': 'Movie added to library.'}, 201
            return {'Error': 'You can not use this resource unauthorized.'}, 403
        except ValidationError as error:
            return {'Error': str(error)}, 400


@movie_namespace.route('/put/<int:movie_id>')
class PutMovie(Resource):
    """
    Puts into movie new data
    """

    @staticmethod
    @login_required
    @movie_namespace.expect(movie_model)
    def put(movie_id: int) -> tuple:
        """
        Updates data about certain movie in library
        movie_id: int
        returns: tuple
        """
        try:
            args = request.json
            print(args)
            movie = Movie.query.filter(Movie.id == movie_id).first()
            if not movie:
                return {'Error': 'No such movie.'}, 404
            name = args.get('name', None)
            rate = args.get('rate', None)
            year = args.get('year', None)
            genres = args.get('genres', None)
            description = args.get('description', None)
            poster = args.get('poster', None)
            director_name = args.get('director-name', 'unknown')

            if current_user.id:
                if name and isinstance(name, str):
                    movie.name = name
                if rate and isinstance(rate, int):
                    movie.rate = rate
                if year and isinstance(year, int):
                    movie.year = year
                if description and isinstance(description, str):
                    movie.description = description
                if poster and isinstance(poster, str):
                    movie.poster = poster
                director = Director.exists(director_name)
                if not director:
                    director = Director(
                        name = director_name,
                        created = datetime.utcnow()
                    )
                    director.save()
                movie.director_id = director.id
                movie.user_id = current_user.id
                movie.save()
                if genres:
                    for g in genres:
                        genre = Genre.exists(g)
                        if not genre:
                            genre = Genre(
                                name = g,
                                created = datetime.utcnow()
                            )
                            genre.save()
                        movie_genre = MovieGenre(
                            m_id = movie.id,
                            g_id = genre.id
                        )
                        movie_genre.save()
                return {'Notification': 'Movie data updated succesfully.'}, 201
            return {'Error': 'You can not use this resource unauthorized.'}, 403

        except ValidationError as error:
            return {'Error': str(error)}, 400


@movie_namespace.route('/delete/<int:movie_id>')
class DeleteMovie(Resource):
    """
    Deletes movie
    """
    
    @staticmethod
    @login_required
    def delete(movie_id: int) -> tuple:
        """
        Deletes movie from the library
        movie_id: int
        returns: tuple
        """
        try:
            movie = Movie.query.get(movie_id)
            if not movie:
                return {'Error': 'No such movie'}, 404
            if current_user and current_user.id == movie.user_id:
                movie.delete()
                return {'Notification': 'Movie deleted succesfully.'}, 201
            return {'Error': 'You can not use this resource unauthorized.'}, 403
        except ValidationError as error:
            return {'Error': str(error)}, 400
