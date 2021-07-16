"""
Authorization user module
"""
from datetime import datetime
from flask import request
from flask_login import login_user, logout_user, login_required
from flask_restplus import fields, Resource, Namespace
from project.models import User


auth_namespace = Namespace('auth', description='Authorization')


auth_model = auth_namespace.model(
    'Log in',
    {
        'username': fields.String,
        'password': fields.String,
    }
)

@auth_namespace.route('/signup', methods=['POST'])
class SignUp(Resource):
    """
    Creating new User
    """

    @staticmethod
    @auth_namespace.expect(auth_model)
    def post() -> tuple:
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
                        return {'Error': 'Username already exists.'}, 
                    new_user = User(
                        username=username, 
                        password=password, 
                        is_admin=False, 
                        created=str(datetime.utcnow())
                    )
                    new_user.save()

                    return {
                        'Notification': 'Registration finished succesfully.'
                    }, 200
                except KeyError:
                    pass
            return {'Error': 'Wrong data format. Use JSON format'}, 401


@auth_namespace.route('/login', methods=['POST'])
class LogIn(Resource):
    """
    Logining User in to system
    """

    @staticmethod
    @auth_namespace.expect(auth_model)
    def post() -> tuple:
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
                        return {'Error': 'Wrong login data.'}, 404

                    login_user(user)

                    return {'Notification': 'Succesfully logined.'}, 202
                except KeyError:
                    return {'Error': 'Wrong data format. Use JSON format'}
            
            return {'Error': 'Wrong data format. Use JSON format'}, 401


@auth_namespace.route('/logout', methods=['GET'])
class LogOut(Resource):
    """
    User log out from system
    """

    @staticmethod
    @login_required
    def get() -> tuple:
        """
        User logout
        """
        try:
            logout_user()
            return {'Notification': 'You logged out.'}, 202
        except:
            return {'Error': 'You was not logined.'}, 400
