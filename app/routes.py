from flask import render_template
from . import app

@app.route("/")
def test():
    return render_template('test.html', argument="Hello World!")