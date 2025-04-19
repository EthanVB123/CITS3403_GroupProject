from flask import Flask
app = Flask(__name__)
from . import routes # this is the same thing as from app import routes, but we are in app so that is redundant
if __name__ == '__main__':
    app.run()