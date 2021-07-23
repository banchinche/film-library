import pytest
import requests
from flask import json


def test_search():
    url_request = 'http://0.0.0.0:5000/api/v1/movies/get?search_string=Animator'
    response = requests.get(url_request)
    text = json.loads(response.text)
    assert text['count'] >= 0

def test_pagination():
    url_request = 'http://0.0.0.0:5000/api/v1/movies/get?start=1&per_page=10'
    response = requests.get(url_request)
    text = json.loads(response.text)
    assert len(text['results']) == 10

def test_genre_filter():
    url_request = 'http://0.0.0.0:5000/api/v1/movies/get?filter_genre=Action'
    response = requests.get(url_request)
    text = json.loads(response.text)
    assert text['results'][0]['genres'] == ['Action']

def test_year_range_filter():
    url_request = 'http://0.0.0.0:5000/api/v1/movies/get?filter_first_date=1800&filter_second_date=1900'
    response = requests.get(url_request)
    text = json.loads(response.text)
    assert all([text['results'][i]['year'] in range(1800, 1901) for i in range(len(text['results']))])

# won't work with new randomly generated directors !
def test_director_filter():
    url_request = 'http://0.0.0.0:5000/api/v1/movies/get?filter_director=Jeffrey%20Porter'
    response = requests.get(url_request)
    text = json.loads(response.text)
    assert all([text['results'][i]['director-name'] == 'Jeffrey Porter' for i in range(len(text['results']))])

def test_sort_year_ascending():
    url_request = 'http://0.0.0.0:5000/api/v1/movies/get?sorting=year-ascending'
    response = requests.get(url_request)
    text = json.loads(response.text)
    assert all([text['results'][i]['year'] <= text['results'][i+1]['year'] for i in range(len(text['results']) - 1)])

def test_sort_year_descending():
    url_request = 'http://0.0.0.0:5000/api/v1/movies/get?sorting=year-descending'
    response = requests.get(url_request)
    text = json.loads(response.text)
    assert all([text['results'][i]['year'] >= text['results'][i+1]['year'] for i in range(len(text['results']) - 1)])

def test_sort_rate_ascending():
    url_request = 'http://0.0.0.0:5000/api/v1/movies/get?sorting=rate-ascending'
    response = requests.get(url_request)
    text = json.loads(response.text)
    assert all([text['results'][i]['rate'] <= text['results'][i+1]['rate'] for i in range(len(text['results']) - 1)])

def test_sort_rate_descending():
    url_request = 'http://0.0.0.0:5000/api/v1/movies/get?sorting=rate-descending'
    response = requests.get(url_request)
    text = json.loads(response.text)
    assert all([text['results'][i]['rate'] >= text['results'][i+1]['rate'] for i in range(len(text['results']) - 1)])
