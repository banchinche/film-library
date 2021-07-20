"""Configuration of app"""
import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """
    Main config class with env variables
    """
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
    SECRET_KEY = os.getenv('SECRET_KEY')
    LOG_FILE = os.getenv('LOG_FILE')
    RESTPLUS_VALIDATE = os.getenv('RESTPLUS_VALIDATE')
    RESTPLUS_MASK_SWAGGER = os.getenv('RESTPLUS_MASK_SWAGGER')
    RESTPLUS_ERROR_404_HELP = os.getenv('RESTPLUS_ERROR_404_HELP')
    RESTPLUS_SWAGGER_UI_DOC_EXPANSION = os.getenv('RESTPLUS_SWAGGER_UI_DOC_EXPANSION')
