from app import db

class Puzzle(db.Model):
    puzzle_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    num_rows = db.Column(db.Integer, nullable=False)
    num_columns = db.Column(db.Integer, nullable=False)
    row_clues = db.Column(db.PickleType, nullable=False)
    column_clues = db.Column(db.PickleType, nullable=False)
    number_players_solved = db.Column(db.Integer, nullable=False)
    # to implement later:
    # puzzle name!
    # parTimeSeconds INTEGER,
    # creatorID INTEGER REFERENCES users(userID),
    # difficulty REAL NOT NULL