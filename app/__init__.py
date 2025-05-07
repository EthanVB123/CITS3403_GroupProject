from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from app.config import Config
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config) # gets the config variables as defined in config.py
db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'loginPage' # name of function in routes.py

from .models import Users

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))
# Enable foreign key enforcement for SQLite (chatgpt code)
with app.app_context():
    @event.listens_for(db.engine, 'connect')
    def enable_sqlite_fk(connection, _):
        connection.execute("PRAGMA foreign_keys=ON")

from . import routes, models # this is the same thing as from app import routes, but we are in app so that is redundant
if __name__ == '__main__':
    app.run()
