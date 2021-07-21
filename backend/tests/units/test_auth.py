import pytest
import requests
from flask import json
from flask_login import current_user
from faker import Faker

fake = Faker()
username = fake.name()

def test_signup():
    headers = {
        'Content-Type': 'application/json', 
        'Accept': 'application/json'
    }
    
    signup_settings = {
        'username': username, 'password': username, 
        }
    url_request = 'http://0.0.0.0:5000/api/v1/auth/signup'
    response = requests.post(
        url=url_request, 
        data=json.dumps(signup_settings), 
        headers=headers
    )
    notification, code = json.loads(response.text), response.status_code
    assert notification == {'Notification': 'Registration finished succesfully.'}
    assert code == 200

def test_login():
    headers = {
        'Content-Type': 'application/json', 
        'Accept': 'application/json'
    }
    
    login_settings = {
        'username': username, 'password': username, 
        }
    url_request = 'http://0.0.0.0:5000/api/v1/auth/login'
    response = requests.post(
        url=url_request, 
        data=json.dumps(login_settings), 
        headers=headers
    )
    notification, code = json.loads(response.text), response.status_code
    assert notification == {'Notification': 'Succesfully logined.'}
    assert code == 202

def test_logout():
    url_request = 'http://0.0.0.0:5000/api/v1/auth/logout'
    response = requests.get(url_request)
    notification, code = json.loads(response.text), response.status_code

    if current_user:
        assert notification == {'Notification': 'You logged out.'}
        assert code == 202
    else:
        assert notification == {'message': 'The method is not allowed for the requested URL.'}
        assert code == 405
