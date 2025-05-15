from flask import render_template, request, redirect, url_for, jsonify, abort, Blueprint, render_template_string
import json
from . import db
from .models import Puzzle, Users, Friends
from flask_login import login_user, login_required, logout_user, current_user
from .models import Puzzle, Users, SolvedPuzzle
from .verifySolution import verifySolution
from .forms import LoginForm, RegisterForm
import math
import html


main = Blueprint('main', __name__)


@main.app_template_filter('unescape')
def unescape_filter(s):
    return html.unescape(s)

@main.context_processor
def inject_solved_ids():
    if current_user.is_authenticated:
        solved = (
            SolvedPuzzle.query
            .with_entities(SolvedPuzzle.puzzle_id, SolvedPuzzle.accuracy)
            .filter_by(user_id=current_user.id)
            .all()
        )
        solved_puzzle_info = {pid: acc for pid, acc in solved}
    else:
        solved_puzzle_info = {}
    return dict(solved_puzzle_info=solved_puzzle_info)


@main.route("/")
def homePage():
    return render_template('homePage.html')

@main.route("/login", methods=['GET', 'POST'])
def loginPage():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = Users.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('main.userProfile', userid = user.id))

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

@main.route("/logout")
@login_required
def logoutPage():
    logout_user()
    return redirect(url_for('main.loginPage'))

@main.route("/register", methods=['GET', 'POST'])
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
        return redirect(url_for('main.loginPage'))
    
    # If there are validation errors and this is an AJAX request
    if form.errors and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Get the first error message
        error_msg = next(iter(form.errors.values()))[0]
        return jsonify({'error': error_msg}), 400
        
    return render_template('register.html', form=form)

@main.route("/profile")
@main.route("/profile/<int:userid>")
@login_required
def userProfile(userid=None):
    if userid == None:
        userid = current_user.id
    # only allow people to view their own profile (or drop this check to let
    # users view each other’s pages)
    if userid != current_user.id:
        if not current_user.friends.filter_by(id=userid).first():
            return render_template_string("""
            <!doctype html>
            <html lang="en">
            <head>
                <meta charset="utf-8">
                <title>Redirecting…</title>
            </head>
            <body onload="
                alert('You do not have access to that profile. Redirecting to your own profile.');
                window.location.href='{{ url }}';
            ">
                <!-- If JS is disabled, show a link instead -->
                <noscript>
                    <p>You do not have access to that profile.
                    <a href="{{ url }}">Click here</a> to go to your own profile.
                    </p>
                </noscript>
            </body>
            </html>
        """, url=url_for('main.userProfile', userid=current_user.id))

    user = Users.query.get_or_404(userid)
    solved_count = SolvedPuzzle.query.filter_by(user_id=userid).count()
    friends = user.friends.all()
    total_friends = len(friends)
    if total_friends > 0:
        higher = sum(1 for f in friends if f.userScore > user.userScore)
        rank = higher + 1
        friend_ranking = f"#{rank} out of {total_friends + 1}"
    else:
        friend_ranking = "No friends yet"
    return render_template('personprofile.html',
        user=user,
        solved_count=solved_count,
        friend_ranking=friend_ranking)

@main.route('/newpuzzle')
def puzzleCreationLandingPage():
    return render_template('createPuzzle.html')

@main.route('/friends/<username>')
@login_required
def displayFriendsPage(username):
    friends = current_user.friends.all()
    return render_template("friends_page.html", friends=friends)


@main.route('/puzzleselect')
@login_required
def puzzleSelect():
    your_puzzles = Puzzle.query.filter_by(creator_id=current_user.id).limit(3).all()
    friend_ids = [friend.id for friend in current_user.friends.all()]
    friend_puzzles = Puzzle.query.filter(Puzzle.creator_id.in_(friend_ids)).limit(3).all()
    top_puzzles = Puzzle.query.order_by(Puzzle.number_players_solved.desc()).limit(3).all()
    return render_template('puzzle_select.html', your_puzzles=your_puzzles, friend_puzzles=friend_puzzles, top_puzzles=top_puzzles)

@main.route('/puzzleselect/<int:userid>')
@login_required
def puzzleSelectFromUser(userid):
    if userid != current_user.id:
        return render_template_string("""
        <!doctype html>
        <html lang="en">
        <head>
            <meta charset="utf-8">
            <title>Redirecting…</title>
        </head>
        <body onload="
            alert('Access denied. Redirecting you to your puzzles...');
            window.location.href='{{ url }}';
        ">
            <!-- If JS is disabled, show a link instead -->
            <noscript>
                <p>Access denied. Redirecting you to your puzzles...
                If you are not redirected, <a href="{{ url }}">click here</a>.
                </p>
            </noscript>
        </body>
        </html>
    """, url=url_for('main.puzzleSelectFromUser', userid=current_user.id))
    your_puzzles = Puzzle.query.filter_by(creator_id=userid).all()
    return render_template('puzzle_select_subset.html', puzzles=your_puzzles, status="you")

@main.route('/puzzleselect/<int:user_id>/friends/')
@login_required
def puzzleSelectFromFriends(user_id):
    if user_id != current_user.id:
        return render_template_string("""
        <!doctype html>
        <html lang="en">
        <head>
            <meta charset="utf-8">
            <title>Redirecting…</title>
        </head>
        <body onload="
            alert('Access denied. Redirecting you to your friends puzzles...');
            window.location.href='{{ url }}';
        ">
            <!-- If JS is disabled, show a link instead -->
            <noscript>
                <p>Access denied. Redirecting you to your friends puzzles...
                If you are not redirected, <a href="{{ url }}">click here</a>.
                </p>
            </noscript>
        </body>
        </html>
    """, url=url_for('puzzleSelectFromFriends', user_id=current_user.id))
    friends_ids = [friend.id for friend in current_user.friends.all()]
    friend_puzzles = Puzzle.query.filter(Puzzle.creator_id.in_(friends_ids)).all()
    return render_template('puzzle_select_subset.html', puzzles=friend_puzzles, status="friends")

@main.route('/puzzleselect/toppuzzles')
def puzzleSelectFromTopPuzzles():
    top_puzzles = Puzzle.query.order_by(Puzzle.number_players_solved.desc()).limit(10).all()
    return render_template('puzzle_select_subset.html', puzzles=top_puzzles, status="top")

@main.route('/puzzle/<int:puzzleid>')
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
                           numSolved = puzzle.number_players_solved,
                           creatorUsername = Puzzle.query.get(puzzleid).creator.username)

@main.route('/puzzle/new/<int:numRows>/<int:numCols>/')
@main.route('/puzzle/new/<int:numRows>/<int:numCols>/<puzzleName>')
def puzzleEditor(numRows, numCols, puzzleName='Untitled'):
    numRows = max(1, numRows) # at least 1 row
    numRows = min(10, numRows) #at most 10 rows
    numCols = max(1, numCols) # at least 1 col
    numCols = min(10, numCols) # at most 10 col
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
                           numSolved = 0,
                           creatorUsername = current_user.username)

def is_array_of_two_integers(value):
    return (
        isinstance(value, (list, tuple)) and
        len(value) == 2 and
        all(isinstance(x, int) for x in value)
    )

@main.route('/submit-puzzle', methods=['POST'])
@login_required
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
    if ((not is_array_of_two_integers(puzzleSize)) or puzzleSize[0] > 10 or puzzleSize[1] > 10 or puzzleSize[0] < 1 or puzzleSize[1] < 1):
        # they didn't make the puzzle legitimately
        # there is no way to accidentally reach this, unless a serious error occurred
        # redirect to homepage
        return redirect(url_for('main.homePage'), code=400)
    puzzle = Puzzle(# id auto increments
                    num_rows = puzzleSize[0],
                    num_columns = puzzleSize[1],
                    row_clues = rowClues,
                    column_clues = colClues,
                    number_players_solved = 0,
                    puzzle_name = data.get('puzzleName'),
                    par_time_seconds = 60,
                    difficulty = math.ceil(len(rowClues)*len(colClues) / 10),
                    creator_id = current_user.id)
    print(puzzle)
    db.session.add(puzzle)
    db.session.commit()
    return redirect(url_for('main.solvePuzzle', puzzleid = puzzle.puzzle_id), code=303)

@main.route('/register-solved-puzzle', methods=['POST'])
@login_required
def registerSolvedPuzzle():
    data = request.get_json()
    puzzleId = data.get('puzzleId')
    userId = current_user.id
    new_accuracy = data.get('accuracy')
    shadedCells = data.get('shadedCells')
    puzzleObj = Puzzle.query.get(puzzleId)
    rowClues = puzzleObj.row_clues
    colClues = puzzleObj.column_clues
    if (puzzleObj is not None and current_user is not None and verifySolution(rowClues, colClues, shadedCells)):
        difficulty = puzzleObj.difficulty if userId != puzzleObj.creator_id else 0 # difficulty is 0 for solving your own puzzle!
        # note that score is  accuracy (out of 100) * difficulty (a small integer)
        previousBestAttempt = SolvedPuzzle.query.get((userId, puzzleId))
        if (previousBestAttempt is not None): # if user already solved this one
            if (new_accuracy > previousBestAttempt.accuracy): # if user did better than last time
                current_user.userScore += (new_accuracy - previousBestAttempt.accuracy) * difficulty # update their score - if they got 300 pts last time, and 320 this time, they get 20 extra points on their record (not 320)
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
            puzzleObj.number_players_solved += 1
            current_user.userScore += difficulty * new_accuracy
            db.session.commit()
        
        print(url_for('main.userProfile', userid = userId))
        return jsonify({"redirect_url": url_for('main.userProfile', userid = userId)}), 200
    else:
        return jsonify({"error": "Failed to solve."}), 400 # maybe make this more detailed

@main.route('/add-friend', methods=['POST'])
@login_required
def add_friend():
    data = request.get_json()
    friend_username = data.get('username')
    if not friend_username or friend_username == current_user.username:
        return jsonify({'error': 'Invalid username'}), 400

    friend = Users.query.filter_by(username=friend_username).first()
    if not friend:
        return jsonify({'error': 'User not found'}), 404

    # Check if already friends (one-way)
    already_friend = Friends.query.filter_by(user_id=current_user.id, friend_id=friend.id).first()
    if already_friend:
        return jsonify({'error': 'Already friends'}), 400

    new_friend = Friends(user_id=current_user.id, friend_id=friend.id)
    db.session.add(new_friend)
    db.session.commit()
    return jsonify({'success': True, 'username': friend.username, 'userScore': friend.userScore}), 200

@main.route('/search-users')
@login_required
def search_users():
    query = request.args.get('q', '')
    if not query:
        return jsonify([])

    # Exclude current user and already-friends
    already_friends_ids = [f.id for f in current_user.friends]
    users = Users.query.filter(
        Users.username.ilike(f"%{query}%"),
        Users.id != current_user.id,
        ~Users.id.in_(already_friends_ids)
    ).limit(10).all()
    return jsonify([u.username for u in users])

@main.route('/remove-friend', methods=['POST'])
@login_required
def remove_friend():
    data = request.get_json()
    friend_username = data.get('username')
    friend = Users.query.filter_by(username=friend_username).first()
    if not friend:
        return jsonify({'error': 'User not found'}), 404

    link = Friends.query.filter_by(user_id=current_user.id, friend_id=friend.id).first()
    if not link:
        return jsonify({'error': 'Not friends'}), 400

    db.session.delete(link)
    db.session.commit()
    return jsonify({'success': True}), 200