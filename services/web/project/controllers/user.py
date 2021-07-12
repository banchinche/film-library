"""
User testing default requests (GET, POST, PUT, DELETE)
"""

from flask import request
from project.models import db, User
from flask_restplus import fields, Resource, Namespace
from marshmallow import ValidationError


api = Namespace('users', description='User default methods')

user_model = api.model(
    'User',
    {
        'username': fields.String('blank'),
        'password': fields.String('blank'),
        'is_admin': fields.Boolean('blank'),
        'created': fields.String('blank')
    },
)


@api.route('/get')
class GetUsers(Resource):
    """
    GET class resource (returns all users)
    """

    @staticmethod
    def get() -> tuple:
        """
        Get all users
        Format: JSON
        """

        users = User.query.all()
        if users:
            user_list = [
                {
                    'user_id': user.id,
                    'username': user.username,
                    'password': user.password,
                    'is_admin': user.is_admin,
                    'created': user.created
                }
                for user in users
            ]
            return {'users': user_list}, 200
        return {'Error': 'No users'}, 404


@api.route('/get/<int:user_id>')
class GetOneUser(Resource):
    """
    GET class resource (returns user with certain id)
    """
    @staticmethod
    def get(user_id: int) -> tuple:
        """
        Get certain user
        Format: JSON
        """

        user = (
            db.session.query(User).filter_by(id=user_id).first()
        )
        if user:
            return {
                'User': user.id,
                'username': user.username,
                'password': user.password,
                'is_admin': user.is_admin,
                'created': user.created
            }, 200
        return {'Error': 'User was not found'}, 404


@api.route('/post')
class PostUser(Resource):
    """
    POST class resource (creates new user)
    """

    @staticmethod
    @api.expect(user_model)
    def post() -> tuple:
        """
        Creates new user
        """

        try:
            user = User(
                username=request.json['username'], password=request.json['password'],
                is_admin=request.json['is_admin'], created=request.json['created']
            )
            db.session.add(user)
            db.session.commit()
            return {'Notification': 'User created.'}, 201
        except ValidationError as err:
            return {'Error: ': str(err)}, 400


@api.route('/put/<int:user_id>')
class PutUser(Resource):
    """
    PUT class resource (updates user data)
    """

    @staticmethod
    @api.expect(user_model)
    def put(user_id):
        """
        Updates info about user
        """
        try:
            user = User.query.get(user_id)
            user.username = request.json['username']
            user.password = request.json['password']
            db.session.commit()
            return {'Notification': 'User updated.'}, 201
        except ValidationError as err:
            return {'Error: ': str(err)}, 400


@api.route('/delete/<int:user_id>')
class DeleteUser(Resource):
    """
    DELETE class resource (deletes user from database)
    """

    @staticmethod
    def delete(user_id) -> tuple:
        """
        Removes certain user by given id
        """

        user = User.query.get(user_id)
        db.session.delete(user)
        db.session.commit()
        return {'Notification': 'User deleted successfully'}, 201
