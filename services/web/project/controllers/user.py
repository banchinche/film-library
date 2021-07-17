"""
User namespace and api-model + CRUD requests
"""

from flask import request
from project.models import User
from flask_restplus import Resource, Namespace



user_namespace = Namespace('users', description='User that operates with movies')


@user_namespace.route('/get')
class GetUsers(Resource):
    """
    GET class resource (returns all users)
    """

    @staticmethod
    def get() -> tuple:
        """
        Get all users
        """

        users = User.query.all()
        if users:
            user_list = [
                {
                    'username': user.username,
                    'created': str(user.created)
                }
                for user in users
            ]
            return {'users': user_list}, 200
        return {'Error': 'No users'}, 404
