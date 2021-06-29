from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from flask_migrate import Migrate


app = Flask(__name__)
app.config['DEBUG'] = True

db = SQLAlchemy(app)

api = Api(app)

migrate = Migrate(app, db)
