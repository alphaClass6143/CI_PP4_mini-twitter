'''
TestCases for profiles app
'''
import datetime

from django.test import TestCase

from accounts.models import User
from profiles.models import FollowRelation

from profiles.forms import SettingsForm, PasswordChangeForm

# Create your tests here.
# Forms
class SettingsFormTests(TestCase):
    '''
    SettingsForm
    '''
    def test_form_optional_valid(self):
        '''
        Tests if the optional fields can be empty
        '''
        form = SettingsForm({
            'username': 'testuser',
            'user_picture': '',
            'user_text': ''
        })
        self.assertTrue(form.is_valid())

    def test_form_valid_with_all_required_fields(self):
        '''
        Test full form validity
        '''
        form = SettingsForm({
            'username': 'testuser',
            'user_picture': 'https://example.com/picture.jpg',
            'user_text': 'Test text'
        })
        self.assertTrue(form.is_valid())

    def test_form_invalid_when_required_fields_are_missing(self):
        '''
        Test for missing username
        '''
        form = SettingsForm({
            'username': '',
            'user_picture': 'https://example.com/picture.jpg',
            'user_text': 'Test text'
        })
        self.assertFalse(form.is_valid())

    def test_form_invalid_when_username_contains_special_characters(self):
        '''
        Test for invalid username
        '''
        form = SettingsForm({
            'username': 'testuser!',
            'user_picture': 'https://example.com/picture.jpg',
            'user_text': 'Test text'
        })
        self.assertFalse(form.is_valid())


class PasswordChangeFormTests(TestCase):
    '''
    PasswordChangeForm
    '''
    def test_form_valid_data(self):
        '''
        Test form valid
        '''
        form = PasswordChangeForm(data={
            'password': 'testpassword',
            'password_confirm': 'testpassword'
        })
        self.assertTrue(form.is_valid())


# Models
class FollowRelationModelTests(TestCase):
    '''
    FollowRelation
    '''
    def setUp(self):
        # Create two users to use in the tests
        self.user1 = User.objects.create_user(
            email='user1@example.com',
            username='user1',
            password='password'
        )
        self.user2 = User.objects.create_user(
            email='user2@example.com',
            username='user2',
            password='password'
        )

    def test_follow_relation_creation(self):
        '''
        Test successful creation
        '''
        follow_relation = FollowRelation.objects.create(
            followed_at=datetime.datetime.now(),
            user=self.user1,
            followed_user=self.user2
        )
        self.assertIsInstance(follow_relation, FollowRelation)
        self.assertEqual(follow_relation.user, self.user1)
        self.assertEqual(follow_relation.followed_user, self.user2)
