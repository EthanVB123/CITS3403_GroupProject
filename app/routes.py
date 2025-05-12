from flask import render_template, request, redirect, url_for, jsonify, abort
from . import app
import json
from . import db
from .models import Puzzle, Users
from flask_login import login_user, login_required, logout_user, current_user
from .models import Puzzle, Users, SolvedPuzzle
from .verifySolution import verifySolution
from .forms import LoginForm, RegisterForm

@app.route("/")
def homePage():
    return render_template('homePage.html')

@app.route("/login", methods=['GET', 'POST'])
def loginPage():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = Users.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('userProfile', userid=user.id))
        
        # if invalid credentials
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # 401 since this is an authentication error
            return jsonify({ 'error': 'Invalid username or password' }), 401
        # used as a fallback
        return render_template('login.html', form=form, error='Invalid username or password')
    
    # If there are validation errors and this is an AJAX request
    if form.errors and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Get the first error message
        error_msg = next(iter(form.errors.values()))[0]
        return jsonify({'error': error_msg}), 400
        
    return render_template('login.html', form=form)

@app.route("/logout")
@login_required
def logoutPage():
    logout_user()
    return redirect(url_for('loginPage'))

@app.route("/register", methods=['GET', 'POST'])
def registerPage():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        # Create new user
        user = Users(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('loginPage'))
    
    # If there are validation errors and this is an AJAX request
    if form.errors and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Get the first error message
        error_msg = next(iter(form.errors.values()))[0]
        return jsonify({'error': error_msg}), 400
        
    return render_template('register.html', form=form)

@app.route("/profile/<int:userid>")
@login_required
def userProfile(userid):
    # only allow people to view their own profile (or drop this check to let
    # users view each other’s pages)
    if userid != current_user.id:
        return abort(403)

    user = Users.query.get_or_404(userid)
    solved_count = SolvedPuzzle.query.filter_by(user_id=userid).count()
    return render_template('personprofile.html',
        user=user,
        solved_count=solved_count)

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

@app.route('/puzzle/new/<int:numRows>/<int:numCols>/')
@app.route('/puzzle/new/<int:numRows>/<int:numCols>/<puzzleName>')
def puzzleEditor(numRows, numCols, puzzleName='Untitled'):
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

@app.route('/register-solved-puzzle', methods=['POST'])
def registerSolvedPuzzle():
    data = request.get_json()
    puzzleId = data.get('puzzleId')
    userId = data.get('userId')
    new_accuracy = data.get('accuracy')
    shadedCells = data.get('shadedCells')
    puzzleObj = Puzzle.query.get(puzzleId)
    userObj = Users.query.get(userId)
    rowClues = puzzleObj.row_clues
    colClues = puzzleObj.column_clues
    if (puzzleObj is not None and userObj is not None and verifySolution(rowClues, colClues, shadedCells)):
        print('Solution accepted!')
        # note that score is  accuracy (out of 100) * difficulty (a small integer)
        previousBestAttempt = SolvedPuzzle.query.get((userId, puzzleId))
        if (previousBestAttempt is not None): # if user already solved this one
            if (new_accuracy > previousBestAttempt.accuracy): # if user did better than last time
                userObj.userScore += (new_accuracy - previousBestAttempt.accuracy) * puzzleObj.difficulty # update their score - if they got 300 pts last time, and 320 this time, they get 20 extra points on their record (not 320)
                previousBestAttempt.accuracy = new_accuracy
                db.session.commit()
            # if user didn't do as well, nothing is updated.
        else: # if this is the user's first solve
            savedAttempt = SolvedPuzzle(
                user_id = userId,
                puzzle_id = puzzleId,
                accuracy = new_accuracy
            )
            db.session.add(savedAttempt)
            userObj.userScore += puzzleObj.difficulty * new_accuracy
            db.session.commit()
        
        print(url_for('userProfile', userid = userId))
        return jsonify({"redirect_url": url_for('userProfile', userid = userId)}), 200
    else:
        return jsonify({"error": "Failed to solve."}), 400 # maybe make this more detailed