import os

basedir = os.path.abspath(os.path.dirname(__file__))
default_db_location = 'sqlite:///' + os.path.join(basedir, 'puzzles.db')

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or default_db_location
    SECRET_KEY = "very_secret"