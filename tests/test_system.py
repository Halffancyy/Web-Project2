import unittest
import subprocess
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from app import create_app, db
from config import TestConfig
from models import User
import os
import traceback

localHost = "http://localhost:5000/"

class TestSelenium(unittest.TestCase):

    def setUp(self):
        """
        Set up the test environment, including creating a test application,
        starting the Flask server, and initializing the Selenium WebDriver.
        """
        # Create test application
        self.testApp = create_app(TestConfig)
        self.app_context = self.testApp.app_context()
        self.app_context.push()
        db.create_all()
        self.add_test_data()

        # Print users in the database to confirm the user has been added
        users = User.query.all()
        print(f"Users in database: {[user.username for user in users]}")

        # Start Flask server
        flask_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../venv/bin/flask')
        self.server_process = subprocess.Popen([flask_path, "run"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, env={"FLASK_APP": "app.py", **os.environ})
        time.sleep(5)  # Wait for the server to start

        # Start Selenium WebDriver
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        options.binary_location = "/usr/bin/google-chrome"  # Specify the Chrome browser path
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        self.driver.get(localHost)

    def tearDown(self):
        """
        Clean up the test environment, including terminating the Flask server
        and the Selenium WebDriver.
        """
        # Terminate Flask server and Selenium WebDriver
        self.server_process.terminate()
        self.server_process.wait()
        self.driver.quit()
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def add_test_data(self):
        """
        Add test data to the database.
        """
        user = User(username='testuser', email='test@example.com')
        user.set_password('testpassword')
        db.session.add(user)
        db.session.commit()

    def test_user_login(self):
        """
        Test the user login functionality.
        """
        print("Navigating to login page...")
        self.driver.get(localHost + "auth/login")
        
        # Use explicit wait to ensure elements are loaded
        try:
            print("Waiting for username input...")
            username_input = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.NAME, 'username')))
            print("Username input found")
            
            print("Waiting for password input...")
            password_input = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.NAME, 'password')))
            print("Password input found")
            
            print("Waiting for login button...")
            login_button = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, '//button[text()="Login"]')))
            print("Login button found")
            
            username_input.send_keys('testuser')
            password_input.send_keys('testpassword')
            login_button.click()
            
            print("Login button clicked")
            
            # Add a short delay to ensure the page has time to process the request
            time.sleep(5)  # Wait for the page to load
            
            # Print the current URL and page source
            current_url = self.driver.current_url
            print(f"Current URL: {current_url}")
            with open("page_source_after_login.html", "w", encoding="utf-8") as f:
                f.write(self.driver.page_source)  # Save page source
            
            print("Waiting for index page to load...")
            WebDriverWait(self.driver, 20).until(EC.url_changes(localHost + "auth/login"))
            print("Index page loaded")
            
            print("Checking for username display on the index page...")
            username_display = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, f'//*[contains(text(), "testuser")]')))
            print("Username display found on index page")
            
            self.assertIsNotNone(username_display, "Login failed, 'testuser' not found on the index page.")
        except Exception as e:
            print("Error during test execution:")
            traceback.print_exc()  # Print detailed exception stack trace
            self.driver.save_screenshot('screenshot.png')  # Take and save a screenshot
            with open("page_source.html", "w", encoding="utf-8") as f:
                f.write(self.driver.page_source)  # Save page source
            self.fail(f"Test failed due to exception: {str(e)}")

if __name__ == '__main__':
    unittest.main()
