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
        设置测试环境，包括创建测试应用、启动 Flask 服务器和 Selenium WebDriver。
        """
        # 创建测试应用
        self.testApp = create_app(TestConfig)
        self.app_context = self.testApp.app_context()
        self.app_context.push()
        db.create_all()
        self.add_test_data()

        # 打印数据库中的用户信息以确认用户是否已被添加
        users = User.query.all()
        print(f"Users in database: {[user.username for user in users]}")

        # 启动 Flask 服务器
        flask_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../venv/bin/flask')
        self.server_process = subprocess.Popen([flask_path, "run"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, env={"FLASK_APP": "app.py", **os.environ})
        time.sleep(5)  # 等待服务器启动

        # 启动 Selenium WebDriver
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        options.binary_location = "/usr/bin/google-chrome"  # 添加这一行，指定 Chrome 浏览器路径
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
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
        print("Navigating to login page...")
        self.driver.get(localHost + "auth/login")
        
        # 使用显式等待确保元素加载完成
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
            
            # 增加短暂延迟以确保页面有时间处理请求
            time.sleep(5)  # 等待页面加载
            
            # 打印当前页面的URL和源代码
            current_url = self.driver.current_url
            print(f"Current URL: {current_url}")
            with open("page_source_after_login.html", "w", encoding="utf-8") as f:
                f.write(self.driver.page_source)  # 保存页面源代码
            
            print("Waiting for index page to load...")
            WebDriverWait(self.driver, 20).until(EC.url_changes(localHost + "auth/login"))
            print("Index page loaded")
            
            print("Checking for username display on the index page...")
            username_display = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, f'//*[contains(text(), "testuser")]')))
            print("Username display found on index page")
            
            self.assertIsNotNone(username_display, "Login failed, 'testuser' not found on the index page.")
        except Exception as e:
            print("Error during test execution:")
            traceback.print_exc()  # 打印详细的异常堆栈信息
            self.driver.save_screenshot('screenshot.png')  # 截取页面截图并保存
            with open("page_source.html", "w", encoding="utf-8") as f:
                f.write(self.driver.page_source)  # 保存页面源代码
            self.fail(f"Test failed due to exception: {str(e)}")

if __name__ == '__main__':
    unittest.main()
