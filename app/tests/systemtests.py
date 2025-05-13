import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from app.models import Users
from selenium.common.exceptions import NoAlertPresentException
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
        time.sleep(1) # just in case, to allow the next page to load
        self.assertIn("Invalid username or password", self.driver.page_source)
    
    def testAuthorisedToUseProfile(self):
        pass

    def testViewFriends(self):
        pass

    def testAddFriend(self):
        pass
    def testCreatePuzzleAndSolveIt(self):
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

        # navigate to profile page
        self.driver.get("http://localhost:5000/profile/5") # replace this with /profile/
        time.sleep(1)
        createPuzzleBtn = self.driver.find_element(By.ID, "createBtn")
        createPuzzleBtn.click()
        time.sleep(1)

        # create a 2x2 puzzle and make sure it redirects to the correct puzzle editor screen
        rowsInput = self.driver.find_element(By.ID, "rows")
        colsInput = self.driver.find_element(By.ID, "columns")
        nameInput = self.driver.find_element(By.ID, "name")
        submitBtn = self.driver.find_element(By.ID, "submitBtn")
        rowsInput.send_keys("2")
        colsInput.send_keys("2")
        nameInput.send_keys("Test Puzzle")
        submitBtn.click()
        time.sleep(1)
        self.assertEqual("http://localhost:5000/puzzle/new/2/2/Test%20Puzzle", self.driver.current_url)

        # create a sample puzzle
        # the puzzle created in this case:
        # \21
        # 2xx
        # 1x.
        # where x is a filled square and . is an empty one

        self.driver.find_element(By.ID, "cell0").click()
        self.driver.find_element(By.ID, "cell1").click()
        self.driver.find_element(By.ID, "cell2").click()
        self.driver.find_element(By.ID, "export").click()

        time.sleep(1)
        # confirm redirected
        self.assertTrue(self.driver.current_url.startswith("http://localhost:5000/puzzle/"))
        # attempt an incorrect solution
        self.driver.find_element(By.ID, "cell0").click()
        self.driver.find_element(By.ID, "cell1").click()
        self.driver.find_element(By.ID, "submit").click()
        # an alert should appear (try-except block adapted from GenAI)
        try:
            alert = self.driver.switch_to.alert
            alert_text = alert.text
            print("Alert appeared:", alert_text)

            # Assert that an alert appeared
            self.assertTrue(True)

            # Dismiss (or use alert.accept() if needed)
            alert.dismiss()
        except NoAlertPresentException:
            self.assertTrue(False, "No alert was present when expected.")
        self.driver.find_element(By.ID, "cell2").click()
        self.driver.find_element(By.ID, "submit").click()
        time.sleep(1)
        # confirm redirect
        self.assertTrue(self.driver.current_url.startswith("http://localhost:5000/profile/"))




