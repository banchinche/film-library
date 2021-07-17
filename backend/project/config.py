"""Configuration of app"""
import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """
    Main config class with env variables
    """
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://")
    STATIC_FOLDER = f"{os.getenv('APP_FOLDER')}/project/static/"

