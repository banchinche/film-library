"""
Authorization user module
"""
from datetime import datetime
from flask import Blueprint, request
from flask_login import login_user, logout_user, login_required
from project.models import db, User


auth = Blueprint('auth', __name__)


@auth.route("/login", methods=['POST'])
def login():
    """
    User logining method
    """

    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            try:
                username, password = data['username'], data['password']
                user = User.query.filter_by(username=username).first()

                if not user and not user.check_password(password):
                    return {'Error': 'Wrong login data.'}

                login_user(user)

                return {'Notification': 'Succesfully logined.'}
            except KeyError:
                return {'Error': 'Wrong data format. Use JSON format'}
        
        return {'Error': 'Wrong data format. Use JSON format'}


@auth.route('/signup', methods=['POST'])
def signup():
    """
    User signing up method
    """

    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            try:
                username, password = data['username'], data['password']
                user = User.query.filter_by(username=username).first()
                if user:
                    return {'Error': 'Username already exists.'}
                new_user = User(
                    username=username, 
                    password=password, 
                    is_admin=False, 
                    created=str(datetime.utcnow())
                )

                db.session.add(new_user)
                db.session.commit()

                return {
                    'Notification': 'Registration finished succesfully.'
                }
            except KeyError:
                pass
        return {'Error': 'Wrong data format. Use JSON format'}


@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    """
    User logout
    """

    logout_user()
    return {'Notification': 'You logged out.'}
