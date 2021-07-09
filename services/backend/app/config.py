from os import path, getenv


basedir = path.abspath(path.dirname(__file__))


class Config:
    """
    Main class of application configuration
    """
    POSTGRES_USER = getenv('POSTGRES_USER')
    POSTGRES_PASSWORD = getenv('POSTGRES_PASSWORD')
    POSTGRES_DB = getenv('POSTGRES_DB')
    SQL_HOST = getenv('SQL_HOST')
    SQL_PORT = getenv('SQL_PORT')
    SQLALCHEMY_DATABASE_URI = (
            f'postgresql://'
            f'{POSTGRES_USER}:{POSTGRES_PASSWORD}'
            f'@{SQL_HOST}:{SQL_PORT}/{POSTGRES_DB}'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    RESTPLUS_VALIDATE = True
    RESTPLUS_MASK_SWAGGER = False
    RESTPLUS_ERROR_404_HELP = False
    RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'

