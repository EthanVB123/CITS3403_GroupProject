from flask import render_template, request, redirect, url_for, jsonify
from . import app
import json
from . import db
from .models import Puzzle, Users
from flask_login import login_user, login_required, logout_user, current_user

@app.route("/")
def homePage():
    return render_template('homePage.html')

@app.route("/login", methods=['GET', 'POST'])
def loginPage():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = Users.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('homePage'))
        # if invalid credentials
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # 401 since this is an authentication error
            return jsonify({ 'error': 'Invalid username or password' }), 401
    
    return render_template('login.html')

@app.route("/logout")
@login_required
def logoutPage():
    logout_user()
    return redirect(url_for('loginPage'))

@app.route("/register", methods=['GET', 'POST'])
def registerPage():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # check if username already exists
        existing_user = Users.query.filter_by(username=username).first()
        if existing_user:
            # if username already exists
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                # 400 since this is a client error
                return jsonify({ 'error': 'Username already exists' }), 400
        
        user = Users(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('loginPage'))
    
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

@app.route('/puzzleselect/friends/<username>')
def puzzleSelectFromFriends(username):
    return render_template('friends_puzzles.html')

@app.route('/puzzleselect/toppuzzles')
def puzzleSelectFromTopPuzzles():
    return render_template('top_puzzles.html')

# Will not be the top_puzzles.html file, can make new files for each difficulty
@app.route('/puzzleselect/difficulty/<difficulty>')
def puzzleSelectFromDifficulty(difficulty):
    return render_template('top_puzzles.html') # adapt to make dynamic on difficulty

@app.route('/puzzle/<int:puzzleid>')
def solvePuzzle(puzzleid):
    puzzle = Puzzle.query.get(puzzleid)
    print(puzzle)
    #puzzleJSON = getPuzzleAsJSON(puzzleid)
    puzzleSize = [puzzle.num_rows, puzzle.num_columns]
    return render_template('solvePuzzle.html',
                           role="solver", 
                           puzzleSize = puzzleSize, 
                           rowClues = puzzle.row_clues, 
                           colClues = puzzle.column_clues,
                           puzzleName = puzzle.puzzle_name,
                           puzzleParTime = puzzle.par_time_seconds,
                           puzzleDifficulty = puzzle.difficulty,
                           puzzleid = puzzleid,
                           numSolved = puzzle.number_players_solved)

@app.route('/puzzle/new/<int:numRows>/<int:numCols>/<puzzleName>')
def puzzleEditor(numRows, numCols, puzzleName):
    startingRowClues = [[0] for i in range(numRows)]
    startingColClues = [[0] for i in range(numCols)]

    return render_template('solvePuzzle.html',
                           role="editor", 
                           puzzleSize = [numRows, numCols], 
                           rowClues = 0, 
                           colClues = 0,
                           puzzleName = puzzleName,
                           puzzleParTime = 0,
                           puzzleDifficulty = 0,
                           puzzleid = 0,
                           numSolved = 0)

@app.route('/submit-puzzle', methods=['POST'])
def submitPuzzle():
    data = request.get_json()
    puzzleSize = data.get('puzzleSize')
    rowClues = data.get('rowClues')
    colClues = data.get('colClues')
    # make a unique id
    #puzzleId = 0
    #for i in rowClues:
    #    for j in i:
    #        puzzleId += j
    #puzzleIdStr = str(puzzleId)+str(puzzleSize[0])+str(puzzleSize[1])
    puzzle = Puzzle(# id auto increments
                    num_rows = puzzleSize[0],
                    num_columns = puzzleSize[1],
                    row_clues = rowClues,
                    column_clues = colClues,
                    number_players_solved = 0,
                    puzzle_name = data.get('puzzleName'),
                    par_time_seconds = 60,
                    difficulty = 1)
    print(puzzle)
    db.session.add(puzzle)
    db.session.commit()
    return redirect(url_for('solvePuzzle', puzzleid = puzzle.puzzle_id), code=303)