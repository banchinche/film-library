from flask import Flask
from flask_migrate import Migrate
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://arima:arima@localhost:5432/practice'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
engine = create_engine(
    'postgresql://arima:arima@localhost:5432/practice',
    echo=True
)
db = SQLAlchemy(app)

api = Api(app)

migrate = Migrate(app, db)
