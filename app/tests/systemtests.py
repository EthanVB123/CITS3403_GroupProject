import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from app.models import Users
from selenium.common.exceptions import NoAlertPresentException
import threading # instead of multiprocessing, which works differently on windows
from app import create_app, db
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
# When running system tests, ensure there is a user present
# with a username of '1' and a password of '1'.

class SystemTests(unittest.TestCase):
    def setUp(self):

        self.app = create_app('app.config.TestingConfig')  # Load the TestingConfig
        self.client = self.app.test_client()  # Flask test client
        self.app_context = self.app.app_context()
        self.app_context.push()  # Push app context to simulate running within Flask

        db.create_all()  # Create tables using the testing database

        user = Users(username='1')
        user.set_password('1')  # assumes a set_password method (like from Flask-Login or Werkzeug)
        db.session.add(user)
        db.session.commit()

        self.server_thread = threading.Thread(target=lambda: self.app.run(use_reloader=False))
        self.server_thread.daemon = True
        self.server_thread.start()
        time.sleep(0.5) # to allow the server time to start

        # simulate a chrome tab (use self.driver.get(url) to go to url)
        options = webdriver.ChromeOptions()
        # use both of these arguments to allow all versions of ChromeDriver to run in headless mode
        options.add_argument("--headless-new")
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=options)

    def tearDown(self):
        # get rid of the chrome tab to avoid memory leak
        self.driver.quit()

    # makes sure the server is up and Selenium WebDriver is operational
    def testHomepageLive(self):
        self.driver.get("http://127.0.0.1:5000")
        WebDriverWait(self.driver, 5).until(
            expected_conditions.presence_of_element_located((By.TAG_NAME, "body"))
        )
        self.assertIn("Welcome to Wild Puzzles", self.driver.page_source)
    
    def testValidLogin(self):
        # go to login page
        self.driver.get("http://127.0.0.1:5000")
        homePageLoginButton = self.driver.find_element(By.ID, "loginBtn")
        homePageLoginButton.click()
        WebDriverWait(self.driver, 5).until(
            expected_conditions.presence_of_element_located((By.ID, "loginPage"))
        ) # just in case, to allow the next page to load

        # sign in with username=1, password=1
        usernameInput = self.driver.find_element(By.NAME, "username")        
        passwordInput = self.driver.find_element(By.NAME, "password")
        usernameInput.send_keys("1")
        passwordInput.send_keys("1")
        loginButton = self.driver.find_element(By.ID, "loginBtn")
        loginButton.click()
        WebDriverWait(self.driver, 5).until(
            expected_conditions.presence_of_element_located((By.ID, "homePage"))
        ) # just in case, to allow the next page to load
        self.assertIn("1's Profile", self.driver.page_source)

        # logout and attempt to sign in with bad details
        logoutButton = self.driver.find_element(By.ID, "logoutBtn")
        logoutButton.click()
        usernameInput = self.driver.find_element(By.NAME, "username")        
        passwordInput = self.driver.find_element(By.NAME, "password")
        usernameInput.send_keys("1")
        passwordInput.send_keys("2")
        loginButton = self.driver.find_element(By.ID, "loginBtn")
        loginButton.click()
        time.sleep(1) # if the error takes >1s to appear, this is also a problem, so leave this time.sleep call in
        self.assertIn("Invalid username or password", self.driver.page_source)
    
    def testAuthorisedToUseProfile(self):
        # go to login page
        self.driver.get("http://127.0.0.1:5000")
        homePageLoginButton = self.driver.find_element(By.ID, "loginBtn")
        homePageLoginButton.click()
        WebDriverWait(self.driver, 5).until(
            expected_conditions.presence_of_element_located((By.ID, "loginPage"))
        ) # just in case, to allow the next page to load

        # sign in with username=1, password=1
        usernameInput = self.driver.find_element(By.NAME, "username")        
        passwordInput = self.driver.find_element(By.NAME, "password")
        usernameInput.send_keys("1")
        passwordInput.send_keys("1")
        loginButton = self.driver.find_element(By.ID, "loginBtn")
        loginButton.click()
        WebDriverWait(self.driver, 5).until(
            expected_conditions.presence_of_element_located((By.ID, "homePage"))
        ) # just in case, to allow the next page to load
        self.assertIn("1's Profile", self.driver.page_source)

        self.driver.find_element(By.ID, "profileBtn").click()
        WebDriverWait(self.driver, 5).until(
            expected_conditions.presence_of_element_located((By.ID, "profilePage"))
        )
        self.assertTrue(self.driver.current_url.startswith("http://127.0.0.1:5000/profile/"))

    def testUnauthorisedToUseProfile(self):
        # go to login page
        self.driver.get("http://127.0.0.1:5000")
        homePageLoginButton = self.driver.find_element(By.ID, "loginBtn")
        homePageLoginButton.click()
        WebDriverWait(self.driver, 5).until(
            expected_conditions.presence_of_element_located((By.ID, "loginPage"))
        ) # just in case, to allow the next page to load

        # sign in with username=1, password=1
        usernameInput = self.driver.find_element(By.NAME, "username")        
        passwordInput = self.driver.find_element(By.NAME, "password")
        usernameInput.send_keys("1")
        passwordInput.send_keys("1")
        loginButton = self.driver.find_element(By.ID, "loginBtn")
        loginButton.click()
        WebDriverWait(self.driver, 5).until(
            expected_conditions.presence_of_element_located((By.ID, "homePage"))
        ) # just in case, to allow the next page to load
        self.assertIn("1's Profile", self.driver.page_source)

        self.driver.find_element(By.ID, "profileBtn").click()
        WebDriverWait(self.driver, 5).until(
            expected_conditions.presence_of_element_located((By.ID, "profilePage"))
        )
        self.assertTrue(self.driver.current_url.startswith("http://127.0.0.1:5000/profile/"))
        profile = self.driver.current_url
        # redirect to an obvious nonexistent profile (or a profile that user isn't friends of)
        self.driver.get(self.driver.current_url + "000000000000") # we won't have trillions of users, if we did we probably shouldn't use flask anyway
        WebDriverWait(self.driver, 5).until(
            expected_conditions.alert_is_present()
        )
        # this should alert and redirect us
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
        
        WebDriverWait(self.driver, 5).until(
            expected_conditions.presence_of_element_located((By.ID, "profilePage"))
        )
        # confirm redirect
        self.assertEqual(self.driver.current_url, profile)

    def testCreatePuzzleForm(self):
        # go to login page
        self.driver.get("http://127.0.0.1:5000")
        homePageLoginButton = self.driver.find_element(By.ID, "loginBtn")
        homePageLoginButton.click()
        WebDriverWait(self.driver, 5).until(
            expected_conditions.presence_of_element_located((By.ID, "loginPage"))
        ) # just in case, to allow the next page to load

        # sign in with username=1, password=1
        usernameInput = self.driver.find_element(By.NAME, "username")        
        passwordInput = self.driver.find_element(By.NAME, "password")
        usernameInput.send_keys("1")
        passwordInput.send_keys("1")
        loginButton = self.driver.find_element(By.ID, "loginBtn")
        loginButton.click()
        WebDriverWait(self.driver, 5).until(
            expected_conditions.presence_of_element_located((By.ID, "homePage"))
        ) # just in case, to allow the next page to load
        self.assertIn("1's Profile", self.driver.page_source)

        # navigate to profile page
        self.driver.get("http://127.0.0.1:5000/profile") # replace this with /profile/
        WebDriverWait(self.driver, 5).until(
            expected_conditions.presence_of_element_located((By.ID, "profilePage"))
        )
        createPuzzleBtn = self.driver.find_element(By.ID, "createBtn")
        createPuzzleBtn.click()
        WebDriverWait(self.driver, 5).until(
            expected_conditions.presence_of_element_located((By.ID, "rows"))
        )

        # create a 2x2 puzzle and make sure it redirects to the correct puzzle editor screen
        rowsInput = self.driver.find_element(By.ID, "rows")
        colsInput = self.driver.find_element(By.ID, "columns")
        nameInput = self.driver.find_element(By.ID, "name")
        submitBtn = self.driver.find_element(By.ID, "submitBtn")
        rowsInput.send_keys("2")
        colsInput.send_keys("2")
        nameInput.send_keys("Test Puzzle")
        submitBtn.click()
        WebDriverWait(self.driver, 5).until(
            expected_conditions.presence_of_element_located((By.ID, "timer"))
        )
        self.assertEqual("http://127.0.0.1:5000/puzzle/new/2/2/Test%20Puzzle", self.driver.current_url)

    def testPuzzleEditorUI(self):
        # go to login page
        self.driver.get("http://127.0.0.1:5000")
        homePageLoginButton = self.driver.find_element(By.ID, "loginBtn")
        homePageLoginButton.click()
        WebDriverWait(self.driver, 5).until(
            expected_conditions.presence_of_element_located((By.ID, "loginPage"))
        ) # just in case, to allow the next page to load

        # sign in with username=1, password=1
        usernameInput = self.driver.find_element(By.NAME, "username")        
        passwordInput = self.driver.find_element(By.NAME, "password")
        usernameInput.send_keys("1")
        passwordInput.send_keys("1")
        loginButton = self.driver.find_element(By.ID, "loginBtn")
        loginButton.click()
        WebDriverWait(self.driver, 5).until(
            expected_conditions.presence_of_element_located((By.ID, "homePage"))
        ) # just in case, to allow the next page to load
        self.assertIn("1's Profile", self.driver.page_source)

        # navigate to profile page
        self.driver.get("http://127.0.0.1:5000/profile") # replace this with /profile/
        WebDriverWait(self.driver, 5).until(
            expected_conditions.presence_of_element_located((By.ID, "profilePage"))
        )
        createPuzzleBtn = self.driver.find_element(By.ID, "createBtn")
        createPuzzleBtn.click()
        WebDriverWait(self.driver, 5).until(
            expected_conditions.presence_of_element_located((By.ID, "rows"))
        )

        # create a 2x2 puzzle and make sure it redirects to the correct puzzle editor screen
        rowsInput = self.driver.find_element(By.ID, "rows")
        colsInput = self.driver.find_element(By.ID, "columns")
        nameInput = self.driver.find_element(By.ID, "name")
        submitBtn = self.driver.find_element(By.ID, "submitBtn")
        rowsInput.send_keys("2")
        colsInput.send_keys("2")
        nameInput.send_keys("Test Puzzle")
        submitBtn.click()
        WebDriverWait(self.driver, 5).until(
            expected_conditions.presence_of_element_located((By.ID, "timer"))
        )
        self.assertEqual("http://127.0.0.1:5000/puzzle/new/2/2/Test%20Puzzle", self.driver.current_url)

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

        WebDriverWait(self.driver, 5).until(
            lambda d: d.current_url.startswith("http://127.0.0.1:5000/puzzle/")
        )
        # confirm redirected
        self.assertTrue(self.driver.current_url.startswith("http://127.0.0.1:5000/puzzle/"))

    def testCreatePuzzleAndSolveIt(self):
        # go to login page
        self.driver.get("http://127.0.0.1:5000")
        homePageLoginButton = self.driver.find_element(By.ID, "loginBtn")
        homePageLoginButton.click()
        WebDriverWait(self.driver, 5).until(
            expected_conditions.presence_of_element_located((By.ID, "loginPage"))
        ) # just in case, to allow the next page to load

        # sign in with username=1, password=1
        usernameInput = self.driver.find_element(By.NAME, "username")        
        passwordInput = self.driver.find_element(By.NAME, "password")
        usernameInput.send_keys("1")
        passwordInput.send_keys("1")
        loginButton = self.driver.find_element(By.ID, "loginBtn")
        loginButton.click()
        WebDriverWait(self.driver, 5).until(
            expected_conditions.presence_of_element_located((By.ID, "homePage"))
        ) # just in case, to allow the next page to load
        self.assertIn("1's Profile", self.driver.page_source)

        # navigate to profile page
        self.driver.get("http://127.0.0.1:5000/profile") # replace this with /profile/
        WebDriverWait(self.driver, 5).until(
            expected_conditions.presence_of_element_located((By.ID, "profilePage"))
        )
        createPuzzleBtn = self.driver.find_element(By.ID, "createBtn")
        createPuzzleBtn.click()
        WebDriverWait(self.driver, 5).until(
            expected_conditions.presence_of_element_located((By.ID, "rows"))
        )

        # create a 2x2 puzzle and make sure it redirects to the correct puzzle editor screen
        rowsInput = self.driver.find_element(By.ID, "rows")
        colsInput = self.driver.find_element(By.ID, "columns")
        nameInput = self.driver.find_element(By.ID, "name")
        submitBtn = self.driver.find_element(By.ID, "submitBtn")
        rowsInput.send_keys("2")
        colsInput.send_keys("2")
        nameInput.send_keys("Test Puzzle")
        submitBtn.click()
        WebDriverWait(self.driver, 5).until(
            expected_conditions.presence_of_element_located((By.ID, "timer"))
        )
        self.assertEqual("http://127.0.0.1:5000/puzzle/new/2/2/Test%20Puzzle", self.driver.current_url)

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
        # time.sleep(1) intentional here, should fail if too slow as well, this should not take long and will be noticed
        self.assertTrue(self.driver.current_url.startswith("http://127.0.0.1:5000/puzzle/"))
        # attempt an incorrect solution
        self.driver.find_element(By.ID, "cell0").click()
        self.driver.find_element(By.ID, "cell1").click()
        self.driver.find_element(By.ID, "submit").click()
        WebDriverWait(self.driver, 5).until(
            expected_conditions.alert_is_present()
        )
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
        WebDriverWait(self.driver, 5).until(
            expected_conditions.presence_of_element_located((By.ID, "profilePage"))
        )
        # confirm redirect
        self.assertTrue(self.driver.current_url.startswith("http://127.0.0.1:5000/profile/"))




