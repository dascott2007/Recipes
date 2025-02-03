from decouple import config
import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

# General Configuration for the authentication application
class Config:
    # Generated secret key and added to .env file
    SECRET_KEY=config('SECRET_KEY')
    # For testing turning this off. set to false in .env file
    SQLALCHEMY_TRACK_MODIFICATIONS=config('SQLALCHEMY_TRACK_MODIFICATIONS',cast=bool) 


class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI="sqlite:///"+os.path.join(BASE_DIR, 'dev.db')
    DEBUG=True
    SQLALCHEMY_ECHO=True

class ProdConfig(Config):
    pass

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI='sqlite:///test.db'
    SQLALCHEMY_ECHO=False # so you don't get SQL generated
    TESTING=True # for error cataching
