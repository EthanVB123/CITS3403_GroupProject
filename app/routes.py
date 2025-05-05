from flask import render_template, request, redirect, url_for, jsonify
from . import app
import json
from . import db
from .models import Puzzle, Users, SolvedPuzzle
from .verifySolution import verifySolution

@app.route("/")
def homePage():
    return render_template('homePage.html')

@app.route("/login")
def loginPage():
    return render_template('login.html')

@app.route("/register")
def registerPage():
    return render_template('register.html')

@app.route("/profile/<int:userid>") # <username> is a dynamic element.
def userProfile(userid):
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