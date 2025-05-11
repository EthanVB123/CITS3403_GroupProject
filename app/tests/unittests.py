# tests/test_app.py
import unittest
from app import create_app, db
from app.models import Users  # Assuming you have a User model

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

    # Sample test for the home page
    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Home Page', response.data)  # Check if "Home Page" is in the response

    # Sample test for user profile page
    def test_user_profile(self):
        user = Users(username="testuser", email="test@example.com")
        db.session.add(user)
        db.session.commit()
        
        response = self.client.get(f'/profile/{user.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'testuser', response.data)  # Check if the username appears in the response

if __name__ == '__main__':
    unittest.main()
