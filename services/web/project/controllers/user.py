"""
User namespace and api-model + CRUD requests
"""

from flask import request
from project.models import db, User
from flask_restplus import fields, Resource, Namespace
from marshmallow import ValidationError
from datetime import datetime


user_namespace = Namespace('users', description='User that operates with movies')

user_model = user_namespace.model(
    'User',
    {
        'username': fields.String('blank'),
        'password': fields.String('blank'),
        'is_admin': fields.Boolean(False),
        'created': fields.String('blank')
    },
)


@user_namespace.route('/get')
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
                    'created': str(user.created)
                }
                for user in users
            ]
            return {'users': user_list}, 200
        return {'Error': 'No users'}, 404


@user_namespace.route('/get/<int:user_id>')
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
                'created': str(user.created)
            }, 200
        return {'Error': 'User was not found'}, 404


@user_namespace.route('/post')
class PostUser(Resource):
    """
    POST class resource (creates new user)
    """

    @staticmethod
    @user_namespace.expect(user_model)
    def post() -> tuple:
        """
        Creates new user
        """

        try:
            user = User(
                username=request.json['username'], password=request.json['password'],
                is_admin=request.json['is_admin'], created=datetime.fromisoformat(request.json['created'])
            )
            db.session.add(user)
            db.session.commit()
            return {'Notification': 'User created.'}, 201
        except ValidationError as err:
            return {'Error: ': str(err)}, 400


@user_namespace.route('/put/<int:user_id>')
class PutUser(Resource):
    """
    PUT class resource (updates user data)
    """

    @staticmethod
    @user_namespace.expect(user_model)
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


@user_namespace.route('/delete/<int:user_id>')
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
