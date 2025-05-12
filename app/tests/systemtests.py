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
        # simulate a chrome tab (use self.driver.get(url) to go to url)
        options = webdriver.ChromeOptions()
        options.add_argument("--headless-new")
        self.driver = webdriver.Chrome(options=options)

    def tearDown(self):
        # get rid of the chrome tab to avoid memory leak
        self.driver.quit()

    # makes sure the server is up and Selenium WebDriver is operational
    def testHomepageLive(self):
        self.driver.get("http://localhost:5000")
        time.sleep(1)
        self.assertIn("Welcome to Wild Puzzles!", self.driver.page_source)
    
    def testValidLogin(self):
        # go to login page
        self.driver.get("http://localhost:5000")
        homePageLoginButton = self.driver.find_element(By.ID, "loginBtn")
        homePageLoginButton.click()
        time.sleep(1) # just in case, to allow the next page to load

        # sign in with username=1, password=1
        usernameInput = self.driver.find_element(By.NAME, "username")        
        passwordInput = self.driver.find_element(By.NAME, "password")
        usernameInput.send_keys("1")
        passwordInput.send_keys("1")
        loginButton = self.driver.find_element(By.ID, "loginBtn")
        loginButton.click()
        time.sleep(1) # just in case, to allow the next page to load
        self.assertIn("Hello, 1", self.driver.page_source)

        # logout and attempt to sign in with bad details
        logoutButton = self.driver.find_element(By.ID, "logoutBtn")
        logoutButton.click()
        usernameInput = self.driver.find_element(By.NAME, "username")        
        passwordInput = self.driver.find_element(By.NAME, "password")
        usernameInput.send_keys("1")
        passwordInput.send_keys("2")
        loginButton = self.driver.find_element(By.ID, "loginBtn")
        loginButton.click()
        time.sleep(0.3) # just in case, to allow the next page to load
        self.assertIn("Invalid username or password", self.driver.page_source)

