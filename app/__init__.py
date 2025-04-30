from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from app.config import Config

app = Flask(__name__)
app.config.from_object(Config) # gets the config variables as defined in config.py
db = SQLAlchemy(app)
migrate = Migrate(app, db)
from . import routes, models # this is the same thing as from app import routes, but we are in app so that is redundant
if __name__ == '__main__':
    app.run()