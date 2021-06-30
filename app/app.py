from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from flask_migrate import Migrate


app = Flask(__name__)
app.config['DEBUG'] = True

db = SQLAlchemy(app)

api = Api(app)

migrate = Migrate(app, db)


@app.route('/home')
def home():
    return 'Welcome home.'

@app.route('/nothome')
def not_home():
    return 'There is not your home.'