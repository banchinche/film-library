from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api, Resource
from flask_migrate import Migrate


app = Flask(__name__)

db = SQLAlchemy(app)

api = Api(app)

migrate = Migrate(app, db)


if __name__ == '__main__':
    app.run()
