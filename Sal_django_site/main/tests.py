from django.test import TestCase
from unittest.mock import Mock, patch
from .models import InfoPrompt, CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from .views import test_homepage_search_input 


#Unit Tests Start Here
#////////////////////////////////////////////


class HomepageTest(TestCase):
    # Tell us what this test is supposed to do
    def test_session_var(self):
        self.assertTrue(test_homepage_search_input()!={})
    

class CustomUserTestCase(TestCase):
    def setUp(self):
        CustomUser.objects.create(email="validemail@gmail.com", org_name="New Biz")

    # Can retrieve users name
    def test_org_name_valid(self):
        dummy = CustomUser.objects.get(email="validemail@gmail.com")
        self.assertEqual(dummy.get_short_name(), "New Biz")
    
    # User accounts can recieve emails
    @patch('main.models.CustomUser')
    def test_user_accounts(self, user_mock):
        user_mock.email_user(self, "test Sub", "hello", from_email=None)



class CustomUserFormTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(email="user@mp.com", password="user", org_name="user", phone=12345678)

    # Valid User Creation Form Data
    def test_UserForm_valid(self):
        form = CustomUserCreationForm(data={'email': "user@gmail.com", 'password1': "Test123.", 'password2': "Test123.",'org_name': "user"})
        self.assertTrue(form.is_valid())

    # Invalid User Creation Form Data
    def test_UserForm_invalid(self):
        form = CustomUserCreationForm(data={'email': "", 'password': "mp", 'org_name': "mp"})
        self.assertFalse(form.is_valid())
        
     # Check Password Cleaning
    @patch('main.forms.CustomUserChangeForm')
    def test_PassForm_valid(self, form_mock):
        form_mock.clean_password2(self)

#Integration Tests Start Here
#////////////////////////////////////////////



class MySeleniumTests(StaticLiveServerTestCase):
    # This Integration Test goes through the simple flow of filling out login form and submitting

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_login(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/login'))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('myuser')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('secret')
        self.selenium.find_element_by_id('login-submit').click()


# NOTES FOR Coverage Testing
# First: $ pip install coverage==3.6
# Second: $ coverage run manage.py test 
# Third: $ coverage report -m
# Bonus Fourth: $ coverage html
# Bonus Fifth: Open Sal_django_site/htmlcov/index.html to see the results of your report. Scroll to the bottom of the report.


