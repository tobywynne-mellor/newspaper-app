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
from django.core.management import call_command
from django.test.utils import override_settings
import time

from .models import User, Profile, Category, Article, Like, Comment

class CommentTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.chrome = webdriver.Chrome(ChromeDriverManager().install())
        cls.chrome.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.chrome.quit()
        super().tearDownClass()

    def setUp(self):
        self._load_test_data() 

    # the comment input should not display when logged out
    @override_settings(DEBUG=True)
    def test_not_able_to_comment_when_logged_out(self):
        self._navigate_to_home()
        self._click_first_article()
        comment_input_selector = "#comments-container div.textarea"
        comment_input_visible = self._is_visible_by_css_selector(comment_input_selector)
        assert comment_input_visible is False

    @override_settings(DEBUG=True)
    def test_post_comment(self):
        # login
        self._login()

        # go to first article
        self._click_first_article()

        comment_input_selector = "#comments-container div.textarea"
        # comment input is displayed
        comment_input_visible = self._is_visible_by_css_selector(comment_input_selector)
        assert comment_input_visible is True

        # assert no comments present
        comment_in_list_selector = "#comment-list > li"
        comment_in_list = self._is_visible_by_css_selector(comment_in_list_selector)
        assert comment_in_list is False

        # add text to input
        comment_input = self.chrome.find_element_by_css_selector(comment_input_selector)
        comment_input.click() # to show send button
        comment_input.send_keys("TEST")

        # send comment
        comment_send_selector = "#comments-container .send"
        comment_send = self.chrome.find_element_by_css_selector(comment_send_selector)
        comment_send.click()

        # check comments if it now exists
        comment_in_list = self._is_visible_by_css_selector(comment_in_list_selector)
        assert comment_in_list is True
        
        # check database that it exists
        comment_object = Comment.objects.get(content="TEST")
        assert comment_object is not None

        # remove comment 
        comment_object.delete()


    @override_settings(DEBUG=True)
    def test_delete_comment(self):
        comment = Comment.objects.create(
                    article=Article.objects.get(content="Test content"),
                    user=Profile.objects.get(user=User.objects.get(username="test_user")),
                    content="TEST COMMENT"
        )
        
        assert comment is not None

        self._login()
        self._navigate_to_home()
        self._click_first_article()

        # check a comment is present
        comment_in_list_selector = "#comment-list .comment-wrapper"
        comment_in_list = self._is_visible_by_css_selector(comment_in_list_selector)
        assert comment_in_list is True

        # check comment contains test
        comment_content_selector = "#comment-list div.content"
        comment_content = self.chrome.find_element_by_css_selector(comment_content_selector)
        comment_content_text = comment_content.get_attribute('innerText')
        assert comment_content_text == "TEST COMMENT"

        # click edit 
        edit_btn_selector = "#comment-list button.edit"
        edit_btn_visible = self._is_visible_by_css_selector(edit_btn_selector)
        edit_btn = self.chrome.find_element_by_css_selector(edit_btn_selector)
        edit_btn.click()

        # click delete
        delete_btn_selector = "#comment-list span.delete.enabled"
        delete_btn = self.chrome.find_element_by_css_selector(delete_btn_selector)
        delete_btn.click()

        # check comments if it does not exist
        comment_in_list = self.chrome.find_element_by_css_selector("#comment-list .comment-wrapper")
        assert comment_in_list is not None 

        # check database that it does not exist
        comment_object = Comment.objects.filter(content="TEST")
        assert comment_object.exists() is False 

    def _navigate_to_home(self):
        self.chrome.get(self.live_server_url)
        index_path = reverse("newspaper_app:index")
        WebDriverWait(self.chrome, 2).until(lambda _: index_path in self.chrome.current_url) 

    def _click_first_article(self):
        selector = ".card"
        article_displayed = self._is_visible_by_css_selector(selector)
        if article_displayed:
            article_card = self.chrome.find_element_by_css_selector(selector)
            article_id = article_card.get_attribute('data-article_id')
            article_card.click()
            assert "{}{}{}/".format(self.live_server_url, "/article/", article_id) == self.chrome.current_url

    def _assert_url_equals(self, url):
        current_url = self.chrome.getCurrentUrl()
        assert url == current_url

    def _is_visible_by_css_selector(self, selector):
        element = None
        try:
            element = self.chrome.find_element_by_css_selector(selector)
        except (NoSuchElementException, StaleElementReferenceException) as e:
            return False
        return element.is_displayed()

    def _load_test_data(self):
        test_category = Category.objects.create(name="Test Category")

        test_article = Article.objects.create(
                    title="Test Article",
                    content="Test content",
                    author="Test Author",
                    category=test_category
                )

        TEST_EMAIL="toby@gmail.com"
        TEST_PASSWORD="secret_password"

        test_user = User.objects.create(
                id=1,
                username='test_user',
                password=make_password(TEST_PASSWORD),
        )

        test_profile = Profile.objects.create(
                user=test_user,
                email=TEST_EMAIL,
        )

    def _login(self):
        try:
            self.chrome.get(self.live_server_url+"/login/")

            user_field = self.chrome.find_element_by_name("username")
            password_field = self.chrome.find_element_by_name("password")

            user_field.send_keys("test_user")
            password_field.send_keys("secret_password")
            login_button = self.chrome.find_element_by_css_selector("input[type='submit']")
            login_button.click()
        except NoSuchElementException as e:
            pass


