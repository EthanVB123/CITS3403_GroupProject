import unittest
from flask_login import login_user
from app import create_app, db
from app.models import Users, Friends, Puzzle, SolvedPuzzle  # Assuming you have a User model
from app import verifySolution
class FlaskAppTestCase(unittest.TestCase):
    
    # Set up the app for testing
    def setUp(self):
        self.app = create_app('app.config.TestingConfig')  # Load the TestingConfig
        self.client = self.app.test_client()  # Flask test client
        self.app_context = self.app.app_context()
        self.app_context.push()  # Push app context to simulate running within Flask

        db.create_all()  # Create tables using the testing database

    # Tear down after each test
    def tearDown(self):
        db.session.remove()  # Remove the session
        db.drop_all()  # Drop tables after tests
        self.app_context.pop()  # Pop app context

    def login_as_user_n(self, n):
        with self.app.test_request_context():
            user = Users.query.get(n)
            login_user(user)

    # Test that creation of users and setting of passwords has no issues
    def test_create_user(self):
        # add two users
        user1 = Users(username="First")
        user2 = Users(username="2nd")
        user1.set_password("1234")
        user2.set_password("password")
        db.session.add_all([user1, user2])
        db.session.commit()

        self.assertTrue(user1.check_password("1234"))
        self.assertTrue(user2.check_password('password'))
        self.assertFalse(user1.check_password('wrongpassword'))
        self.assertFalse(user2.check_password('1234'))
        self.assertFalse(user1.check_password('password'))
        self.assertFalse(user1.check_password(''))

    # Following 2 tests check the backend puzzle solution verifier found in app/verifySolution.py
    # Checks verifySolution.py gets the correct clues from a row/col of shadedCells (to then correctly verify the solution with)
    def test_generate_clues(self):
        # Check behaviour with empty lines
        self.assertListEqual([0],verifySolution.generateClues([0]))
        self.assertListEqual([0],verifySolution.generateClues([0,0,0,0,0]))
        # Check behaviour with typical lines in a puzzle
        self.assertListEqual([1,1], verifySolution.generateClues([1,0,0,1,0]))
        self.assertListEqual([3,1,2],verifySolution.generateClues([0,0,1,1,1,0,0,0,1,0,0,1,1,0]))
        # Check behaviour with lines of all 1's
        self.assertListEqual([1],verifySolution.generateClues([1]))
        self.assertListEqual([6], verifySolution.generateClues([1,1,1,1,1,1]))
    # Checks the overall verifySolution function
    def test_verify_solution(self):
        # Check all possible 1x1 puzzles
        self.assertTrue(verifySolution.verifySolution([[0]],[[0]],[[0]]))
        self.assertTrue(verifySolution.verifySolution([[1]],[[1]],[[1]]))
        self.assertFalse(verifySolution.verifySolution([[0]],[[0]],[[1]]))
        self.assertFalse(verifySolution.verifySolution([[1]],[[1]],[[0]]))
        # Check non-square (1x3 in this case) puzzles with more than 1 clue in some rows/cols
        self.assertTrue(verifySolution.verifySolution([[1,1]],[[1],[0],[1]],[[1,0,1]]))
        self.assertFalse(verifySolution.verifySolution([[1,1]],[[1],[0],[1]],[[0,0,1]])) 
        # Check larger puzzles       
        self.assertTrue(verifySolution.verifySolution([[2],[1]],[[1],[2]],[[1,1],[0,1]]))
        self.assertTrue(verifySolution.verifySolution([[4],[1,1],[2,1],[0]],[[3],[1,1],[1],[3]],[[1,1,1,1],[1,0,0,1],[1,1,0,1],[0,0,0,0]]))
        self.assertFalse(verifySolution.verifySolution([[4],[1,1],[2,1],[0]],[[3],[1,1],[1],[3]],[[1,1,1,1],[1,0,0,1],[1,1,0,1],[0,0,1,0]]))
    
    #Tests that users can solve puzzle and the userScore attribute updates at the right time 
    def test_register_solved_puzzle(self):
        # Create 2 new users (default score zero, id=1 and 2)
        user1 = Users(username="First")
        user2 = Users(username="2nd")
        user1.set_password("1234")
        user2.set_password("password")
        db.session.add_all([user1, user2])
        db.session.commit()
        self.login_as_user_n(1)
        # Create two sample puzzles
        puzzle1 = Puzzle(
            num_rows = 2,
            num_columns = 2,
            row_clues = [[1],[1]],
            column_clues = [[1],[1]],
            number_players_solved = 0,
            puzzle_name = "Test Puzzle 1",
            par_time_seconds = 60,
            difficulty = 1,
            creator_id = 1
        )
        
        puzzle2 = Puzzle(
            num_rows = 3,
            num_columns = 4,
            row_clues = [[1],[1],[1]],
            column_clues = [[1],[1],[1],[0]],
            number_players_solved = 0,
            puzzle_name = "Test Puzzle 2",
            par_time_seconds = 120,
            difficulty = 2,
            creator_id = 1
        )
        db.session.add_all([puzzle1, puzzle2])
        db.session.commit()

        # check user starts with zero points
        self.assertEqual(0, Users.query.get(1).userScore)
        self.assertEqual(0, Users.query.get(2).userScore)

        # user 1 attempts to solve puzzle 1 correctly, obtaining 50% accuracy score
        # this should not award any points as user 1 created the puzzle
        response = self.client.post("/register-solved-puzzle", 
                                 json={'puzzleId':1,
                                       'accuracy':50,
                                       'shadedCells':[[1,0],[0,1]]})
        self.assertEqual(200, response.status_code)
        self.assertEqual(0, Users.query.get(1).userScore)
        # user 1 attempts to solve puzzle 1 correctly, obtaining 50% accuracy score
        # this should award 50 points (50 accuracy * 1 difficulty)
        self.login_as_user_n(2)
        response = self.client.post("/register-solved-puzzle", 
                                 json={'puzzleId':1,
                                       'accuracy':50,
                                       'shadedCells':[[1,0],[0,1]]})
        self.assertEqual(200, response.status_code)
        self.assertEqual(50, Users.query.get(2).userScore)

        # user 1 attempts to solve puzzle 1 incorrectly, then puzzle 2 incorrectly
        # these should award no points each, meaning user 1 still has 50 points
        response = self.client.post("/register-solved-puzzle", 
                                 json={'puzzleId':1,
                                       'accuracy':50,
                                       'shadedCells':[[1,1],[0,1]]})
        self.assertEqual(400, response.status_code)
        self.assertEqual(50, Users.query.get(2).userScore)
        response = self.client.post("/register-solved-puzzle", 
                                 json={'puzzleId':2,
                                       'accuracy':50,
                                       'shadedCells':[[1,1],[0,1]]})
        self.assertEqual(400, response.status_code)
        self.assertEqual(50, Users.query.get(2).userScore)

        # user 1 correctly solves puzzle 2, with 100% accuracy score
        # this should award 200 points (100 acc * 2 difficulty), so current score=250
        response = self.client.post("/register-solved-puzzle", 
                                 json={'puzzleId':2,
                                       'accuracy':100,
                                       'shadedCells':[[1,0,0,0],[0,1,0,0],[0,0,1,0]]})
        self.assertEqual(200, response.status_code)
        self.assertEqual(250, Users.query.get(2).userScore)

        # user 1 correctly solves puzzle 2, with a lower accuracy score
        # this shouldn't award any points (should still have 250)
        response = self.client.post("/register-solved-puzzle", 
                                 json={'puzzleId':2,
                                       'accuracy':50,
                                       'shadedCells':[[1,0,0,0],[0,1,0,0],[0,0,1,0]]})
        self.assertEqual(200, response.status_code)
        self.assertEqual(250, Users.query.get(2).userScore)

        # user 1 correctly solves puzzle 1, with a higher accuracy score of 75
        # this should award 25 points (accuracy += 25 * 1 difficulty)
        response = self.client.post("/register-solved-puzzle", 
                                 json={'puzzleId':1,
                                       'accuracy':75,
                                       'shadedCells':[[1,0],[0,1]]})
        self.assertEqual(200, response.status_code)
        self.assertEqual(275, Users.query.get(2).userScore)


    #Tests that the login-required condition activates
    def test_login_required(self):
        # add two users
        user1 = Users(username="First")
        user2 = Users(username="2nd")
        user1.set_password("1234")
        user2.set_password("password")
        db.session.add_all([user1, user2])
        db.session.commit()
        response = self.client.get("/profile/1")
        self.assertNotEqual(200, response.status_code)
        self.login_as_user_n(1)
        response = self.client.get("/profile/1")
        self.assertEqual(200, response.status_code)
    #Tests that users can create puzzles correctly (with validation)
    def test_submit_puzzle(self):
        # add two users
        user1 = Users(username="First")
        user2 = Users(username="2nd")
        user1.set_password("1234")
        user2.set_password("password")
        db.session.add_all([user1, user2])
        db.session.commit()

        self.login_as_user_n(1)
        # test user 1 making a valid puzzle
        response = self.client.post("/submit-puzzle",
                                    json={'puzzleSize': [2,2],
                                          'rowClues': [[1],[2]],
                                          'colClues': [[2],[1]]})
        self.assertEqual(303, response.status_code)

        # test user 1 making a puzzle with too large dimensions
        # this will fail at the moment, as validation isn't yet implemented here
        response = self.client.post("/submit-puzzle",
                                    json={'puzzleSize': [2,12],
                                          'rowClues': [[1],[2]],
                                          'colClues': [[2],[1]]})
        self.assertEqual(400, response.status_code)

        # test user 1 making a puzzle with zero-length dimensions
        # this will fail at the moment, as validation isn't yet implemented here
        response = self.client.post("/submit-puzzle",
                                    json={'puzzleSize': [2,0],
                                          'rowClues': [[1],[2]],
                                          'colClues': [[2],[1]]})
        self.assertEqual(400, response.status_code)


if __name__ == '__main__':
    unittest.main()
