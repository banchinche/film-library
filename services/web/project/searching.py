from flask import abort
from flask_restplus import reqparse

search_arguments = reqparse.RequestParser()

search_arguments.add_argument(
    'start', type=int, required=False,
    default=1, help='Start from movie number'
)
search_arguments.add_argument(
    'per_page', type=int, required=False,
    choices=[10, 20, 50], default=10,
    help='Movies per page'
)
search_arguments.add_argument(
    'sorting',  required=False,
    choices=['rate-ascending', 'rate-descending', 'year-ascending', 'year-descenging']
)
search_arguments.add_argument(
    'filter_genre', required=False,
    choices=['Action', 'Comedy', 'Drama', 'Fantasy', 'Horror', 'Mystery', 'Romance', 'Thriller']
)
search_arguments.add_argument(
    'filter_first_date', type=int, required=False,
    help='First range date parameter'
)
search_arguments.add_argument(
    'filter_second_date', type=int, required=False,
    help='Second range date parameter'
)
search_arguments.add_argument(
    'filter_director', required=False,
    help='Director of movie'
)
search_arguments.add_argument(
    'search_string', required=False,
    help='Word from or entire title of movie'
)



def get_paginated_list(results, url, start, limit):
    start = int(start)
    limit = int(limit)
    count = len(results)
    if count < start or limit < 0:
        abort(404)
    # make response
    obj = {'start': start, 'limit': limit, 'count': count}
    # make URLs
    # make previous url
    if start == 1:
        obj['previous'] = ''
    else:
        start_copy = max(1, start - limit)
        limit_copy = start - 1
        obj['previous'] = url + '?start=%d&limit=%d' % (start_copy, limit_copy)
    # make next url
    if start + limit > count:
        obj['next'] = ''
    else:
        start_copy = start + limit
        obj['next'] = url + '?start=%d&limit=%d' % (start_copy, limit)
    # finally extract result according to bounds
    obj['results'] = results[(start - 1):(start - 1 + limit)]
    return obj