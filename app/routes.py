from flask import render_template
from . import app
from .puzzlesdb import getPuzzleAsJSON
@app.route("/")
def homePage():
    return render_template('test.html', argument="This should be the home page.")

@app.route("/login")
def loginPage():
    return render_template('test.html', argument="This should be the login page.")

@app.route("/profile/<username>") # <username> is a dynamic element.
def userProfile(username):
    return render_template('test.html', argument=f"This should display the profile of user {username}.")

@app.route('/newpuzzle')
def puzzleCreationLandingPage():
    return render_template('test.html', argument="This should display the createPuzzle screen.")

@app.route('/friends/<username>')
def displayFriendsPage(username):
    return render_template('test.html', argument=f"This should display the friends list of user {username}.")

@app.route('/puzzleselect')
def puzzleSelect():
    return render_template('test.html', argument="This should be the landing page for Puzzle Select.")

@app.route('/puzzleselect/<username>')
def puzzleSelectFromUser(username):
    return render_template('test.html', argument=f"This should display puzzles from user {username}.")

@app.route('/puzzleselect/difficulty/<difficulty>')
def puzzleSelectFromDifficulty(difficulty):
    return render_template('test.html', argument=f"This should display puzzles with difficulty {difficulty}.")

@app.route('/puzzle/<int:puzzleid>')
def solvePuzzle(puzzleid):
    puzzleJSON = getPuzzleAsJSON(puzzleid)
    return render_template('solvePuzzle.html', puzzleJSON=puzzleJSON)

@app.route('/puzzle/new')
def puzzleEditor():
    return render_template('createPuzzle.html')
