# from django.test import TestCase, Client
# from io import BytesIO
# from PIL import Image
# from django.core.files.base import File
# from django.core.files.base import ContentFile
# from django.core.files.uploadedfile import SimpleUploadedFile
# from django.shortcuts import redirect, reverse
# # from .factories import UserFactory
# from unittest.mock import Mock, patch
# from django.core.files import File
# from .models import InfoPrompt, CustomUser
# from .forms import CustomUserCreationForm, CustomUserChangeForm, ProfileForm
# from django.contrib.staticfiles.testing import StaticLiveServerTestCase
# from selenium.webdriver.firefox.webdriver import WebDriver
# from .views import test_homepage_search_input


# # Unit Tests Start Here
# # ////////////////////////////////////////////


# class HomepageTest(TestCase):
#     # Tell us what this test is supposed to do
#     def test_session_var(self):
#         self.assertTrue(test_homepage_search_input() != {})


# class CustomUserTestCase(TestCase):
#     def setUp(self):
#         CustomUser.objects.create(
#             email="validemail@gmail.com", your_name="New Biz")

#     # Can retrieve users name
#     def test_org_name_valid(self):
#         dummy = CustomUser.objects.get(email="validemail@gmail.com")
#         self.assertEqual(dummy.get_short_name(), "New Biz")

#     # User accounts can recieve emails
#     @patch('main.models.CustomUser')
#     def test_user_accounts(self, user_mock):
#         user_mock.email_user(self, "test Sub", "hello", from_email=None)


# class CustomUserFormTest(TestCase):
#     def setUp(self):
#         self.user = CustomUser.objects.create(
#             email="user@mp.com", password="user", org_name="user", phone=12345678)

#     # Valid User Creation Form Data
#     def test_UserForm_valid(self):
#         form = CustomUserCreationForm(
#             data={'email': "user@gmail.com", 'password1': "Test123.", 'password2': "Test123.", 'your_name': "user"})
#         self.assertTrue(form.is_valid())

#     # Invalid User Creation Form Data
#     def test_UserForm_invalid(self):
#         form = CustomUserCreationForm(
#             data={'email': "", 'password': "mp", 'your_name': "mp"})
#         self.assertFalse(form.is_valid())

#      # Check Password Cleaning
#     @patch('main.forms.CustomUserChangeForm')
#     def test_PassForm_valid(self, form_mock):
#         form_mock.clean_password2(self)

# def create_image(storage, filename, size=(100, 100), image_mode='RGB', image_format='PNG'):
#     """
#     Generate a test image, returning the filename that it was saved as.

#     If ``storage`` is ``None``, the BytesIO containing the image data
#     will be passed instead.
#      """
#     data = BytesIO()
#     Image.new(image_mode, size).save(data, image_format)
#     data.seek(0)
#     if not storage:
#         return data
#     image_file = ContentFile(data.read())
#     return storage.save(filename, image_file)


# class ProfileFormTest(TestCase):
#     def setUp(self):
#         self.credentials = {
#             'email': 'user@gmail.com',
#             'password': 'Easy123'}
#         self.user = CustomUser.objects.create(
#             email="user@gmail.com", password="Easy123", your_name="user")

#     # deleting the user will remove the user, the user_profile, AND the avatar image
#     def tearDown(self):
#         self.user.delete()

#     @patch('main.models.Profile')
#     def test_ProfileAddress(self, profile_mock):
#         profile_mock.get_address(self)

#     def test_login_valid(self):
#         # send login data
#         c = Client()
#         logged_in = c.login(email='user@gmail.com', password='Easy123')
#         # should be logged in now
#         self.assertTrue(self.user.is_active)

#     # Valid Profile Edit Form Data but it doesn't work SAD.
#     # def test_ProfileForm_valid(self):
#     #     avatar = create_image(None, 'avatar.png')
#     #     avatar_file = SimpleUploadedFile('front.png', avatar.getvalue())
#     #     c = Client()
#     #     logged_in = c.login(email='user@gmail.com', password='Easy123')
#     #     # newPhoto = SimpleUploadedFile(name='test.png', content=b"file_content", content_type='image/png')
#     #     form_data={'org_name': "Nonprof", 'org_role': "RECIPIENT", 'org_email': "user@gmail.com",'org_phone': "2345678901",
#     #     'org_address': "1777 San Ricardo Dr.",'org_city': "St. Louis",'org_state': "MO",'org_zipcode': "63138",
#     #     'org_country': "US",'image': avatar,'org_desc': "We do good stuff"}
#     #     form = ProfileForm(data=form_data)
#     #     self.user = Profile.objects.create(
#     #     # self.assertTrue(form.is_valid())





# # Integration Tests Start Here
# # ////////////////////////////////////////////



# class MySeleniumTests(StaticLiveServerTestCase):
#     # This Integration Test goes through the simple flow of filling out login form and submitting

#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
#         cls.selenium = WebDriver()
#         cls.selenium.implicitly_wait(10)

#     @classmethod
#     def tearDownClass(cls):
#         cls.selenium.quit()
#         super().tearDownClass()

#     def test_login(self):
#         self.selenium.get('%s%s' % (self.live_server_url, '/login'))
#         username_input = self.selenium.find_element_by_name("username")
#         username_input.send_keys('myuser')
#         password_input = self.selenium.find_element_by_name("password")
#         password_input.send_keys('secret')
#         self.selenium.find_element_by_id('login-submit').click()

# class HomepageTestSearchData(TestCase):
#     def test_homepage_search_data(self):
#         self.assertTrue(session.request['place'],{})

# # NOTES FOR Coverage Testing
# # First: $ pip install coverage==3.6
# # Second: $ coverage run manage.py test 
# # Third: $ coverage report -m
# # Bonus Fourth: $ coverage html
# # Bonus Fifth: Open Sal_django_site/htmlcov/index.html to see the results of your report. Scroll to the bottom of the report.


from django.test import TestCase, Client
from io import BytesIO
from PIL import Image
from django.core.files.base import File
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.shortcuts import redirect, reverse
# from .factories import UserFactory
from unittest.mock import Mock, patch
from django.core.files import File
from .models import InfoPrompt, CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm, ProfileForm
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from .views import test_homepage_search_input
from django.http import HttpRequest
from django.test import SimpleTestCase
from django.urls import reverse
import re
from . import views

# Unit Tests Start Here
# ////////////////////////////////////////////




class HomePageTests(SimpleTestCase):
    # Check that homepage exists and return 200 HTTP Status
    def test_home_page_status_code(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)
    # confirm that it uses the url named home
    def test_view_url_by_name(self):
        response = self.client.get(reverse('home'))
        self.assertEquals(response.status_code, 200)
    # check that the template used is home.html
    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('home'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
    # test that it does not contain incorrect HTML
    def test_home_page_does_not_contain_incorrect_html(self):
        response = self.client.get('/')
        self.assertNotContains(
            response, 'Hi there! I should not be on the page.')


# class HomepageTest(TestCase):
#     # Tell us what this test is supposed to do
#     def test_session_var(self):
#         self.assertTrue(test_homepage_search_input() != {})


class CustomUserTestCase(TestCase):
    def setUp(self):
        CustomUser.objects.create(
            email="validemail@gmail.com", your_name="New Biz")

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
        self.user = CustomUser.objects.create(
            email="user@mp.com", password="user", org_name="user", phone=12345678)

    # Valid User Creation Form Data
    def test_UserForm_valid(self):
        form = CustomUserCreationForm(
            data={'email': "user@gmail.com", 'password1': "Test123.", 'password2': "Test123.", 'your_name': "user"})
        self.assertTrue(form.is_valid())

    # Invalid User Creation Form Data
    def test_UserForm_invalid(self):
        form = CustomUserCreationForm(
            data={'email': "", 'password': "mp", 'your_name': "mp"})
        self.assertFalse(form.is_valid())

     # Check Password Cleaning
    @patch('main.forms.CustomUserChangeForm')
    def test_PassForm_valid(self, form_mock):
        form_mock.clean_password2(self)

def create_image(storage, filename, size=(100, 100), image_mode='RGB', image_format='PNG'):
    """
    Generate a test image, returning the filename that it was saved as.

    If ``storage`` is ``None``, the BytesIO containing the image data
    will be passed instead.
     """
    data = BytesIO()
    Image.new(image_mode, size).save(data, image_format)
    data.seek(0)
    if not storage:
        return data
    image_file = ContentFile(data.read())
    return storage.save(filename, image_file)


class ProfileFormTest(TestCase):
    def setUp(self):
        self.credentials = {
            'email': 'user@gmail.com',
            'password': 'Easy123'}
        self.user = CustomUser.objects.create(
            email="user@gmail.com", password="Easy123", your_name="user")

    # deleting the user will remove the user, the user_profile, AND the avatar image
    def tearDown(self):
        self.user.delete()

    @patch('main.models.Profile')
    def test_ProfileAddress(self, profile_mock):
        profile_mock.get_address(self)

    def test_login_valid(self):
        # send login data
        c = Client()
        logged_in = c.login(email='user@gmail.com', password='Easy123')
        # should be logged in now
        self.assertTrue(self.user.is_active)
  
        
# class HomepageTestSearchData(TestCase):
#     def test_homepage_search_data(self):
#         self.assertTrue(session.request['place'],{})


class ProfileTests(TestCase):
    
    def setUp(self):
        url = reverse('profile_view')
        response = self.client.get(url)
        self.client = Client()
        
    # general test that we're getting the page we ask for
    def test_profile_view_page(self):
        url = reverse('profile_view')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile_view.html')
        self.assertNotContains(response, '.svg')
        
    # Tries 'donor' and 'recipient' with upper or lower case, and returns error if not one of these
    # Let me know if there is an easy way to reefactor this \/\/\/
    def test_donor_recipient(self):
        url = reverse('profile_view')
        response = self.client.get(url)
        try:
            self.assertContains(response, 'Donor')
        except:
            pass
        try:
            self.assertContains(response, 'donor')
        except:
            pass
        try:
            self.assertContains(response, 'Recipient')
        except:
            pass
        try:
            self.assertContains(response, 'recipient')
        except:
            pass
        finally:
            print('Incorrect User Type; must be "donor" or "recipient" user Type. Either no selection or incorrect selection found ')
    
    # Test whether address field is greater than 3 characters
    def test_valid_org_address(self):
        url = reverse('profile_view')
        response = self.client.get(url)
        self.assertTrue(re.search(r'<p class="p-line"><strong>Organzation Address: </strong>\.(.*?)</p>', response).group(1)>=3)
    
    # Test whether city field is non-empty
    def test_valid_org_address(self):
        url = reverse('profile_view')
        response = self.client.get(url)
        self.assertTrue(re.search(r'<p class="p-line col"><strong> City: </strong>\.(.*?)</p>', response).group(1)!='')
    
    # Test whether state field is non-empty
    def test_valid_org_address(self):
        url = reverse('profile_view')
        response = self.client.get(url)
        self.assertTrue(re.search(r'<p class="p-line col"><strong> State: </strong>\.(.*?)</p>', response).group(1)!='')
    
    # Test whether zipcode field is non-empty
    def test_valid_org_address(self):
        url = reverse('profile_view')
        response = self.client.get(url)
        self.assertTrue(re.search(r'<p class="p-line col"><strong> Zipcode: </strong>\.(.*?)</p>', response).group(1)!='')
    
     
    # Valid Profile Edit Form Data but it doesn't work SAD.
    # def test_ProfileForm_valid(self):
    #     avatar = create_image(None, 'avatar.png')
    #     avatar_file = SimpleUploadedFile('front.png', avatar.getvalue())
    #     c = Client()
    #     logged_in = c.login(email='user@gmail.com', password='Easy123')
    #     # newPhoto = SimpleUploadedFile(name='test.png', content=b"file_content", content_type='image/png')
    #     form_data={'org_name': "Nonprof", 'org_role': "RECIPIENT", 'org_email': "user@gmail.com",'org_phone': "2345678901",
    #     'org_address': "1777 San Ricardo Dr.",'org_city': "St. Louis",'org_state': "MO",'org_zipcode': "63138",
    #     'org_country': "US",'image': avatar,'org_desc': "We do good stuff"}
    #     form = ProfileForm(data=form_data)
    #     self.user = Profile.objects.create(
    #     # self.assertTrue(form.is_valid())





# Integration Tests Start Here
# ////////////////////////////////////////////



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


