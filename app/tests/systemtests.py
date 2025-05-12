import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from app.models import Users
# When running system tests, ensure there is a user present
# with a username of '1' and a password of '1'.

class SystemTests(unittest.TestCase):
    def setUp(self):
        # simulate a chrome tab
        self.driver = webdriver.Chrome()

    def tearDown(self):
        # get rid of the chrome tab to avoid memory leak
        self.driver.quit()

    # makes sure the server is up and Selenium WebDriver is operational
    def testHomepageLive(self):
        self.driver.get("http://localhost:5000")
        self.assertIn("Welcome to Wild Puzzles!", self.driver.page_source)
    
    