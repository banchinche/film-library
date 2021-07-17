"""
Setting up application
"""

import re
from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_restplus import Api
from project import models

from project.config import Config
from project.controllers.director import director_namespace
from project.controllers.genre import genre_namespace
from project.controllers.movie import movie_namespace
from project.controllers.user import user_namespace
from project.auth import auth_namespace


def create_app():
    app = Flask(__name__)
    app.secret_key = 'SECRET_KEY'
    app.config.from_object(Config)
    return app

def init_migrate(app):
    migrate = Migrate(app, models.db)
    models.db.init_app(app)
    migrate.init_app(app, models.db)
    return migrate

def create_api(app):
    api = Api(
    version='1.0',
    title='REST-API services',
    description='API service for managing the film library',
    prefix='/api/v1',
)
    api.init_app(app)
    return api

app = create_app()
migrate = init_migrate(app=app)
api = create_api(app=app)


# namespaces
api.add_namespace(director_namespace)
api.add_namespace(genre_namespace)
api.add_namespace(movie_namespace)
api.add_namespace(user_namespace)
api.add_namespace(auth_namespace)

# login manager initialization

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth_log_in'
login_manager.logout_view = 'auth_log_out'


@login_manager.user_loader
def load_user(user_id):
    """
    Reloading the user object from the user ID stored in the session
    """

    return models.User.query.get(int(user_id))

if __name__ == '__main__':
    app.debug = True
    app.run()