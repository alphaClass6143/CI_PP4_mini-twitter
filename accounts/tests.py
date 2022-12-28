'''
Tests for the accounts app
'''
from django.test import TestCase
from django.db import IntegrityError

from accounts.models import User

from accounts.forms import RegisterForm, LogInForm


# Create your tests here.
# Forms
class RegisterFormTestCase(TestCase):
    '''
    RegisterForm test cases
    '''
    def test_form_valid(self):
        '''
        Test for a valid form
        '''
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass',
            'password_confirm': 'testpass',
        }
        form = RegisterForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_username(self):
        '''
        Test for invalid username
        '''
        form_data = {
            'username': 'test%&user!',
            'email': 'test@example.com',
            'password': 'testpass',
            'password_confirm': 'testpass',
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'username': ['Only alphabetic and numeric characters are allowed.']
        })

    def test_form_invalid_email(self):
        '''
        Test for invalid email
        '''
        form_data = {
            'username': 'testuser',
            'email': 'invalidemail',
            'password': 'testpass',
            'password_confirm': 'testpass',
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'email': ['Enter a valid email address.']
        })


class LogInFormTests(TestCase):
    '''
    RegisterForm test cases
    '''
    def test_form_validation(self):
        '''
        Test form validation
        '''
        form = LogInForm(data={'email': '', 'password': 'testpass'})
        self.assertFalse(form.is_valid())
        self.assertFormError(form, 'email', 'This field is required.')

        form = LogInForm(data={'email': 'test@example.com', 'password': ''})
        self.assertFalse(form.is_valid())
        self.assertFormError(form, 'password', 'This field is required.')

        form = LogInForm(data={'email': 'test@example.com', 'password': 'testpass'})
        self.assertTrue(form.is_valid())


# Models
class TestUserModel(TestCase):
    '''
    Test user model
    '''
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass'
        )

    def test_create_user(self):
        '''
        Test create user
        '''
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.username, 'testuser')
        self.assertTrue(self.user.check_password('testpass'))

    def test_email_is_unique(self):
        '''
        Test for unique email
        '''
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                email='test@example.com',
                username='anothertestuser',
                password='anothertestpass'
            )

    def test_username_is_unique(self):
        '''
        Test for unique email
        '''
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                email='anothertest@example.com',
                username='testuser',
                password='anothertestpass'
            )

    def test_user_defaults(self):
        '''
        Test the user default flags
        '''
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)

    def test_switch_active(self):
        '''
        Test if the switch_active method works
        '''
        self.user.switch_active()
        self.assertFalse(self.user.is_active)
        self.user.switch_active()
        self.assertTrue(self.user.is_active)
