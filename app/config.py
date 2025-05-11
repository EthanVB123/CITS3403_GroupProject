import os
 
basedir = os.path.abspath(os.path.dirname(__file__))
default_db_location = 'sqlite:///' + os.path.join(basedir, os.environ.get("FLASK_DATABASE_FILENAME",'puzzles.db'))
 
class Config:
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY") # not secure! in final codebase, should not make this public.

class DeploymentConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or default_db_location

class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory"
    TESTING = True