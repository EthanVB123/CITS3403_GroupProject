# Note - this file has been refactored from handmade code to an app factory by ChatGPT.
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from sqlalchemy import event
from .config import Config, DeploymentConfig

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'main.loginPage'

def create_app(config_class=DeploymentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Enable SQLite foreign keys
    with app.app_context():
        @event.listens_for(db.engine, 'connect')
        def enable_sqlite_fk(connection, _):
            connection.execute("PRAGMA foreign_keys=ON")

    # Import models for migration
    from . import models
    from .models import Users

    # User loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.get(int(user_id))

    # Register routes (or Blueprints if used)
    from .routes import main
    app.register_blueprint(main)

    return app