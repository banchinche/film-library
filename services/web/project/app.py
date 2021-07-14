"""
Setting up application
"""

from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_restplus import Api
from project import models, auth

from project.controllers.user import api as user_namespace
from project.controllers.genre import api as genre_namespace
from project.controllers.film import api as film_namespace
from project.controllers.director import api as director_namespace

#  init app
app = Flask(__name__)
app.secret_key = 'SECRET_KEY'
app.config.from_object('project.config.Config')

# init db
migrate = Migrate(app, models.db)
models.db.init_app(app)
migrate.init_app(app, models.db)

# init blueprint /auth
app.register_blueprint(auth.auth, url_prefix='/auth')

# init restplus
api = Api(
    version='1.0',
    title='REST-API service',
    description='API service for managing the film library',
    prefix='/api/v1',
)
api.init_app(app)
api.add_namespace(user_namespace)
api.add_namespace(genre_namespace)
api.add_namespace(film_namespace)
api.add_namespace(director_namespace)

# init flask_login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'


@login_manager.user_loader
def load_user(user_id):
    """
    Reloading the user object from the user ID stored in the session
    """

    return models.User.query.get(int(user_id))


if __name__ == '__main__':
    app.debug = True
    app.run()
