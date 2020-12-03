from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from webdriver_manager.chrome import ChromeDriverManager
from django.contrib.auth.hashers import make_password
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import LiveServerTestCase
from django.urls import reverse
from django.core import management
from django.test.utils import override_settings
import time
from .models import *
import django.core.management.commands

# a1. like article ...DONE!
# a2. check like exists in database ...DONE!
# b1. unlike article ...DONE!
# b2. check like removed from database ...DONE!
# c1. check likes not visible when logged out ...DONE!
# c2. check likes visible when logged in ...DONE!

class LikesTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.chrome = webdriver.Chrome(ChromeDriverManager().install())
        cls.chrome.implicitly_wait(5)
        print("--Test Likes--")

    @classmethod
    def tearDownClass(cls):
        cls.chrome.quit()
        super().tearDownClass()

    def setUp(self):
        management.call_command('flush', verbosity=0, interactive=False)
        self._load_test_data()
    

    @override_settings(DEBUG=True)
    def test_like_logged_out(self):
        self.chrome.get(self.live_server_url)
        self.chrome.find_element_by_css_selector(".card").click()

        # c1. check likes not visible when logged out
        try:
            like_container_visible = self.chrome.find_element_by_css_selector(".like-container")
            status = True
        except (NoSuchElementException, StaleElementReferenceException) as e:
            status = False
        assert status is False


    @override_settings(DEBUG=True)
    def test_like_logged_in(self):
        self.chrome.get(self.live_server_url)

        self.chrome.get(self.live_server_url+"/login/")
        self.chrome.find_element_by_name("username").send_keys("doge")
        self.chrome.find_element_by_name("password").send_keys("hackerman")
        self.chrome.find_element_by_css_selector("input[type='submit']").click()

        self.chrome.get(self.live_server_url)

        # article_obj_id below used for database check later
        article_obj_id = self.chrome.find_element_by_css_selector(".card").get_attribute('data-article_id')
        self.chrome.find_element_by_css_selector(".card").click()
        
        # c2. check likes visible when logged in
        assert self.chrome.find_element_by_css_selector(".far.fa-heart") is not None

        # a1. like article
        self.chrome.find_element_by_css_selector(".far.fa-heart").click()
        # check if fa icon changed to liked version
        assert self.chrome.find_element_by_css_selector(".fas.fa-heart") is not None
        # a2. check like exists in database
        time.sleep(1)
        like_object = Like.objects.filter(article_id=article_obj_id, user_id=1)
        assert like_object.exists() is True

        # b1. unlike article
        self.chrome.find_element_by_css_selector(".fas.fa-heart").click()
        # check if fa icon changed to unliked version
        assert self.chrome.find_element_by_css_selector(".far.fa-heart") is not None
        # b2. check like removed from database
        time.sleep(1)
        like_object = Like.objects.filter(article_id=article_obj_id, user_id=1)
        assert like_object.exists() is False 


    def _assert_url_equals(self, url):
        current_url = self.chrome.getCurrentUrl()
        assert url == current_url

    def _load_test_data(self):
        test_category = Category.objects.create(name="Test Category")
        test_article = Article.objects.create(title="Test Article", content="Test content", author="Test Author", category=test_category)
        test_user = User.objects.create(id=1, username='doge', password=make_password("hackerman"))
        test_profile = Profile.objects.create(user=test_user, email="doge@doge.com")
