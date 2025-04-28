CREATE TABLE users (
    userID INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    passwordHash TEXT NOT NULL,
    userScore INTEGER NOT NULL
);

CREATE TABLE friendships ( -- must be a separate table to resolve m:n relationship
-- also note this doesn't resolve symmetry, that can be resolved by inserting both a:b and b:a at the same time (or just ensure a<b)
    userID_1 INTEGER REFERENCES users(userID),
    userID_2 INTEGER REFERENCES users(userID),
    PRIMARY KEY (userID_1, userID_2)
);

CREATE TABLE puzzles (
    puzzleID INTEGER PRIMARY KEY,
    puzzleName TEXT,
    numRows INTEGER NOT NULL,
    numCols INTEGER NOT NULL,
    rowClues TEXT, -- this is JSON
    colClues TEXT, -- this is JSON
    parTimeSeconds INTEGER,
    creatorID INTEGER REFERENCES users(userID),
    numberPlayersSolved INTEGER NOT NULL,
    difficulty REAL NOT NULL
);