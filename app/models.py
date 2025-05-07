from app import db
from sqlalchemy import CheckConstraint

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False)
    passwordHash = db.Column(db.String(256), nullable=False)
    userScore = db.Column(db.Integer, nullable=False, default=0)


class Friends(db.Model):
    __tablename__ = 'friends'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    friend_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)


class Puzzle(db.Model):
    puzzle_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    num_rows = db.Column(db.Integer, nullable=False)
    num_columns = db.Column(db.Integer, nullable=False)
    row_clues = db.Column(db.PickleType, nullable=False)
    column_clues = db.Column(db.PickleType, nullable=False)
    number_players_solved = db.Column(db.Integer, nullable=False)
    puzzle_name = db.Column(db.String(100))
    par_time_seconds = db.Column(db.Integer)
    difficulty = db.Column(db.Integer)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    creator = db.relationship('Users', backref=db.backref('puzzles'))
    __table_args__ = (
        CheckConstraint('num_columns > 0 AND num_columns <= 20 AND num_rows > 0 AND num_rows <= 20', name='puzzle_size_check'), # trailing comma means this is treated as a tuple
    )

class SolvedPuzzle(db.Model):
    __tablename__ = 'solvedpuzzle'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    puzzle_id = db.Column(db.Integer, db.ForeignKey('puzzle.puzzle_id'), primary_key=True)
    accuracy = db.Column(db.Integer)
    __table_args__ = (
        CheckConstraint('accuracy > 0 AND accuracy <= 100', name='accuracy_checker'), # trailing comma means this is treated as a tuple
    )