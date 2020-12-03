from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from django.contrib.auth.hashers import make_password
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import LiveServerTestCase
from django.urls import reverse
from django.core import management 
import time
from .models import *
import urllib.request
import os


class UserCreationTest(StaticLiveServerTestCase):
    # fixtures = ['newspaper_data.json']
    # Setting up the test

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.chrome = webdriver.Chrome(
            ChromeDriverManager().install())
        cls.chrome.implicitly_wait(10)
        print("--Test Account--")

    @classmethod
    def tearDownClass(cls):
        cls.chrome.quit()
        super().tearDownClass()

    def setUp(self):
        management.call_command('flush', verbosity=0, interactive=False)
        self._load_test_data()
    # Test methods

    def test_logIn(self):
        # Go to login page
        self.chrome.get(self.live_server_url+"/login/")

        # Input username and password
        # Fail login
        user_field = self.chrome.find_element_by_name("username")
        password_field = self.chrome.find_element_by_name("password")
        user_field.send_keys("test_user1")
        password_field.send_keys("secret_password1")
        login_button = self.chrome.find_element_by_css_selector(
            "input[type='submit']")
        login_button.click()
        # Check if is in login_validation url
        current_url = self.chrome.current_url
        self.is_url(self.live_server_url +
                    "/login_validation/")

        # Clear fields
        user_field = self.chrome.find_element_by_name("username")
        password_field = self.chrome.find_element_by_name("password")
        user_field.clear()
        password_field.clear()

        # Success login
        user_field = self.chrome.find_element_by_name("username")
        password_field = self.chrome.find_element_by_name("password")
        user_field.send_keys("test_user")
        password_field.send_keys("secret_password")
        login_button = self.chrome.find_element_by_css_selector(
            "input[type='submit']")
        login_button.click()
        # Check if is in login_validation url
        current_url = self.chrome.current_url
        self.is_url(self.live_server_url + "/")

    def test_sucess_register(self):
        # Go to Registration page
        self.chrome.get(self.live_server_url+"/register/")
        # -------------------Input and submit value-----------------------
        username_field = self.chrome.find_element_by_name("username")
        password_field = self.chrome.find_element_by_name("password1")
        password2_field = self.chrome.find_element_by_name("password2")
        email_field = self.chrome.find_element_by_name("email")
        dob_field = self.chrome.find_element_by_name("dob")
        pref_cate_field = self.chrome.find_elements_by_name("pref_cate")
        profile_pic_field = self.chrome.find_element_by_id("id_profile_pic")

        username_field.send_keys("Duyyy")
        password_field.send_keys("Duy12345")
        password2_field.send_keys("Duy12345")
        email_field.send_keys("yuddayama@gmail.com")
        dob_field.clear()
        dob_field.send_keys("1944-10-10")

        for category in pref_cate_field:
            category.click()
        profile_pic_field.send_keys(
            os.path.abspath("newspaper_app/static/newspaper_app/image_test/doggo.png"))
        login_button = self.chrome.find_element_by_css_selector(
            "input[type='submit']")
        login_button.click()
        current_url = self.chrome.current_url
        self.is_url(self.live_server_url + "/profile/")

    def test_fail_register(self):
        # Go to Registration page
        self.chrome.get(self.live_server_url+"/register/")
        # -------------------Input missing username-----------------------
        username_field = self.chrome.find_element_by_name("username")
        password_field = self.chrome.find_element_by_name("password1")
        password2_field = self.chrome.find_element_by_name("password2")
        email_field = self.chrome.find_element_by_name("email")
        dob_field = self.chrome.find_element_by_name("dob")
        password_field = self.chrome.find_element_by_name("password1")
        password2_field = self.chrome.find_element_by_name("password2")

        password_field.send_keys("Duy12345")
        password2_field.send_keys("Duy12345")

        login_button = self.chrome.find_element_by_css_selector(
            "input[type='submit']")
        login_button.click()
        current_url = self.chrome.current_url
        self.is_url(self.live_server_url +
                    "/register/")
        # -------------------Input missing email-----------------------
        username_field.send_keys("Duyyy")
        # email_field.send_keys("yuddayama@gmail.com")
        dob_field.clear()
        dob_field.send_keys("1944-10-10")

        login_button = self.chrome.find_element_by_css_selector(
            "input[type='submit']")
        login_button.click()
        current_url = self.chrome.current_url
        self.is_url(self.live_server_url +
                    "/register/")

        # -------------------Input missing dob-----------------------
        email_field.send_keys("yuddayama@gmail.com")
        dob_field.clear()

        login_button = self.chrome.find_element_by_css_selector(
            "input[type='submit']")
        login_button.click()
        current_url = self.chrome.current_url
        self.is_url(self.live_server_url +
                    "/register/")
        # -------------------Input missing profile_pic and preferences-----------------------
        dob_field.send_keys("1944-10-10")

        login_button = self.chrome.find_element_by_css_selector(
            "input[type='submit']")
        login_button.click()
        current_url = self.chrome.current_url
        self.is_url(self.live_server_url +
                    "/profile/")

    def is_url(self, match_url):
        current_url = self.chrome.current_url
        self.assertEqual(current_url, match_url)

    def _load_test_data(self):
        test_category = Category.objects.create(name="Test Category")

        test_article = Article.objects.create(
            title="Test Article",
            content="Test content",
            author="Test Author",
            category=test_category
        )

        TEST_EMAIL = "toby@gmail.com"
        TEST_PASSWORD = "secret_password"

        test_user = User.objects.create(
            id=1,
            username='test_user',
            password=make_password(TEST_PASSWORD),
        )

        test_profile = Profile.objects.create(
            user=test_user,
            email=TEST_EMAIL,
        )
