import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SECRET_KEY = "very_secret" # not secure! in final codebase, should not make this public.
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_BINDS = {
        'users': 'sqlite:///' + os.path.join(basedir, 'users.db'),
        'friends': 'sqlite:///' + os.path.join(basedir, 'friends.db')
    }    