from django.test import TestCase
from unittest.mock import Mock, patch
from .models import InfoPrompt, CustomUser

# Create your tests here.
class CustomUserTestCase(TestCase):
    def setUp(self):
        CustomUser.objects.create(email="validemail@gmail.com", org_name="New Biz")
        # CustomUser.objects.create(name="cat", sound="meow")

    @patch('CustomUser.email_user')
    def test_user_accounts(self, mock_email_user):
        """Custom User Accounts can recieve emails and display proper account info"""
        user1 = CustomUser.objects.get(org_name="New Biz")
        user1.email_user(self, "test Sub", "hello", from_email=None)
        self.assertTrue(mock_email_user.called)


        # """Animals that can speak are correctly identified"""
        # lion = Animal.objects.get(name="lion")
        # cat = Animal.objects.get(name="cat")
        # self.assertEqual(lion.speak(), 'The lion says "roar"')
        # self.assertEqual(cat.speak(), 'The cat says "meow"')