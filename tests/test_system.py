import unittest
import subprocess
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from app import create_app, db
from config import TestConfig
from models import User

localHost = "http://localhost:5000/"

class TestSelenium(unittest.TestCase):

    def setUp(self):
        """
        设置测试环境，包括创建测试应用、启动 Flask 服务器和 Selenium WebDriver。
        """
        # 创建测试应用
        self.testApp = create_app(TestConfig)
        self.app_context = self.testApp.app_context()
        self.app_context.push()
        db.create_all()
        self.add_test_data()

        # 启动 Flask 服务器
        self.server_process = subprocess.Popen(["python", "app.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(5)  # 等待服务器启动

        # 启动 Selenium WebDriver
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        executable_path = ChromeDriverManager().install()
        self.driver = webdriver.Chrome(executable_path=executable_path, options=options)
        self.driver.get(localHost)

    def tearDown(self):
        """
        清理测试环境，包括终止 Flask 服务器和 Selenium WebDriver。
        """
        # 终止 Flask 服务器和 Selenium WebDriver
        self.server_process.terminate()
        self.server_process.wait()
        self.driver.quit()
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def add_test_data(self):
        """
        添加测试数据到数据库中。
        """
        user = User(username='testuser', email='test@example.com')
        user.set_password('testpassword')
        db.session.add(user)
        db.session.commit()

    def test_user_login(self):
        """
        测试用户登录功能。
        """
        self.driver.get(localHost + "auth/login")
        
        username_input = self.driver.find_element(By.NAME, 'username')
        password_input = self.driver.find_element(By.NAME, 'password')
        submit_button = self.driver.find_element(By.NAME, 'submit')
        
        username_input.send_keys('testuser')
        password_input.send_keys('testpassword')
        submit_button.click()
        
        welcome_message = self.driver.find_element(By.XPATH, '//*[contains(text(), "Welcome")]')
        self.assertIsNotNone(welcome_message, "Login failed, 'Welcome' message not found.")

if __name__ == '__main__':
    unittest.main()
