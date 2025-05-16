import os
 

 
class Config:
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY") # not secure! in final codebase, should not make this public.

class DeploymentConfig(Config):
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, os.environ.get("FLASK_DATABASE_FILENAME"))

class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    TESTING = True