'''
Tests for post app
'''
from django.test import TestCase
from django.utils import timezone

from accounts.models import User
from .models import Post, PostComment, PostVote

from post.forms import PostForm, CommentForm


# Create your tests here.
# Forms
class PostFormTests(TestCase):
    '''
    PostForm tests
    '''
    def test_form_validation(self):
        '''
        Test validity of form
        '''
        # Test that the form is valid with valid data
        form_data = {'content': 'Test post'}
        form = PostForm(data=form_data)
        self.assertTrue(form.is_valid())

        # Test that the form is invalid with empty content
        form_data = {'content': ''}
        form = PostForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['content'], ['This field is required.'])


class CommentFormTests(TestCase):
    '''
    CommentForm tests
    '''
    def test_form_validation(self):
        '''
        Test validity of form
        '''
        # Test that the form is valid with valid data
        form_data = {'content': 'Test comment'}
        form = CommentForm(data=form_data)
        self.assertTrue(form.is_valid())

        # Test that the form is invalid with empty content
        form_data = {'content': ''}
        form = CommentForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['content'], ['This field is required.'])


# Models
class PostModelTests(TestCase):
    '''
    Post model tests
    '''
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(
            email='Test@email.com',
            username='testuser',
            password='testpass'
        )

    def test_create_post(self):
        '''
        Test model tests
        '''
        # Test that a post can be created
        post = Post.objects.create(
            content='Test post',
            created_at=timezone.now(),
            user=self.user
        )
        self.assertEqual(post.content, 'Test post')
        self.assertEqual(post.user, self.user)

    def test_str_method(self):
        '''
        Tests the str method
        '''
        post = Post.objects.create(
            content='Test post',
            created_at=timezone.now(),
            user=self.user
        )
        self.assertEqual(str(post), 'Test post')

    def test_get_username(self):
        '''
        Test get username method
        '''
        post = Post.objects.create(
            content='Test post',
            created_at=timezone.now(),
            user=self.user
        )
        self.assertEqual(post.get_username(), 'testuser')


class PostCommentModelTests(TestCase):
    '''
    PostComment model tests
    '''
    def setUp(self):
        # Create a user and post for testing
        self.user = User.objects.create_user(
            email='Test@email.com',
            username='testuser',
            password='testpass'
        )
        self.post = Post.objects.create(
            content='Test post',
            created_at=timezone.now(),
            user=self.user
        )

    def test_create_comment(self):
        '''
        Create comment test
        '''
        comment = PostComment.objects.create(
            content='Test comment',
            created_at=timezone.now(),
            post=self.post,
            user=self.user
        )
        self.assertEqual(comment.content, 'Test comment')
        self.assertEqual(comment.post, self.post)
        self.assertEqual(comment.user, self.user)


class PostVoteModelTests(TestCase):
    '''
    PostVote model tests
    '''
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(
            email='Test@email.com',
            username='testuser',
            password='testpass'
        )
        self.post = Post.objects.create(
            content='This is a test post',
            created_at='2022-12-24 12:34:56',
            user=self.user
        )

    def test_create_post_vote(self):
        '''
        Create post vote
        '''
        vote = PostVote.objects.create(
            type=1,
            post=self.post,
            user=self.user
        )
        self.assertEqual(vote.type, 1)
        self.assertEqual(vote.post, self.post)
        self.assertEqual(vote.user, self.user)
