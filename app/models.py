from app import db

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
    # to implement later:
    # puzzle name!
    # parTimeSeconds INTEGER,
    # creatorID INTEGER REFERENCES users(userID),
    # difficulty REAL NOT NULL
