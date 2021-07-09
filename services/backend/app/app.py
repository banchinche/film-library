from flask import Flask
from flask_migrate import Migrate
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

app = Flask(__name__)
app.config.from_object('app.config.Config')


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://arima:arima@db:5432/practice'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
engine = create_engine(
    'postgresql://arima:arima@db:5432/practice',
    echo=True
)
db = SQLAlchemy()

#  init app

# init db
migrate = Migrate(app, db)
db.init_app(app)

# # init blueprint /auth
# app.register_blueprint(auth.auth, url_prefix='/auth')

# init restplus
api = Api(
    version='1.0',
    title='Movie library REST API',
    description='',
    prefix='/api/v1',
)
api.init_app(app)
# api.add_namespace(user_namespace)
# api.add_namespace(genre_namespace)
# api.add_namespace(film_namespace)
# api.add_namespace(director_namespace)

# init flask_login
# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = "auth.login"


# @login_manager.user_loader
# def load_user(user_id):
#     """Reloading the user object from the user ID stored in the session"""

#     return models.UserModel.query.get(int(user_id))


if __name__ == '__main__':
    app.debug = True
    app.run()