from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from .models import CustomUser

class CustomUserTestCase(TestCase):
    def setUp(self):
        CustomUser.objects.create(email="user@example.com", password="password")
        CustomUser.objects.create(email="other@example.com", password="password")

    def test_users_have_emails(self):
        user1 = CustomUser.objects.get(email="user@example.com")
        user2 = CustomUser.objects.get(email="other@example.com")
        self.assertEqual(user1.email, "user@example.com")
        self.assertEqual(user2.email, "other@example.com")

    def test_password_hashing(self):
        user1 = CustomUser.objects.get(email="user@example.com")
        user2 = CustomUser.objects.get(email="other@example.com")
        self.assertNotEqual(user1.password, "password")
        self.assertNotEqual(user2.password, "password")
        self.assertTrue(user1.check_password("password"))
        self.assertTrue(user2.check_password("password"))

