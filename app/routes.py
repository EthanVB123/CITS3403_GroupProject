from flask import render_template
from . import app
from .puzzlesdb import getPuzzleAsJSON
import json
from . import db
from .models import Puzzle

@app.route("/")
def homePage():
    return render_template('homePage.html')

@app.route("/login")
def loginPage():
    return render_template('login.html')

@app.route("/register")
def registerPage():
    return render_template('register.html')

@app.route("/profile/<username>") # <username> is a dynamic element.
def userProfile(username):
    return render_template('personprofile.html') # adapt to make dynamic on username

@app.route('/newpuzzle')
def puzzleCreationLandingPage():
    return render_template('createPuzzle.html')

@app.route('/friends/<username>')
def displayFriendsPage(username):
    return render_template("friends_page.html")

@app.route('/puzzleselect')
def puzzleSelect():
    return render_template('puzzle_select.html')

@app.route('/puzzleselect/<username>')
def puzzleSelectFromUser(username):
    return render_template('your_puzzles.html') # adapt to make dynamic on username

@app.route('/puzzleselect/difficulty/<difficulty>')
def puzzleSelectFromDifficulty(difficulty):
    return render_template('top_puzzles.html') # adapt to make dynamic on difficulty

@app.route('/puzzle/<int:puzzleid>')
def solvePuzzle(puzzleid):
    puzzles = Puzzle.query.get(puzzleid)
    print(puzzles)
    puzzleJSON = getPuzzleAsJSON(puzzleid)
    return render_template('solvePuzzle.html', puzzleJSON=puzzleJSON)

@app.route('/puzzle/new/<int:numRows>/<int:numCols>')
def puzzleEditor(numRows, numCols):
    startingRowClues = [[0] for i in range(numRows)]
    startingColClues = [[0] for i in range(numCols)]
    puzzle = Puzzle(puzzle_id = int(str(numRows)+str(numCols)),
                    num_rows = numRows,
                    num_columns = numCols,
                    row_clues = startingRowClues,
                    column_clues = startingColClues,
                    number_players_solved = 0)
    db.session.add(puzzle)
    db.session.commit()
    return render_template('solvePuzzle.html', puzzleJSON=json.dumps({"role": "editor", "numRows": numRows, "numCols": numCols}))
