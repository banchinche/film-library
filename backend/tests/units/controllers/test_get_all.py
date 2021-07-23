import pytest
import requests


def test_users_get():
    url_request = "http://0.0.0.0:5000/api/v1/users/get"
    response = requests.get(url_request)
    assert response.status_code == 200

def test_directors_get():
    url_request = "http://0.0.0.0:5000/api/v1/directors/get"
    response = requests.get(url_request)
    assert response.status_code == 200

def test_genres_get():
    url_request = "http://0.0.0.0:5000/api/v1/genres/get"
    response = requests.get(url_request)
    assert response.status_code == 200

def test_movies_get():
    url_request = "http://0.0.0.0:5000/api/v1/movies/get"
    response = requests.get(url_request)
    assert response.status_code == 200
