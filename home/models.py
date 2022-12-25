from django.db import models

# Create your models here.
from django.contrib.auth.models import User


from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

VOTE = ((0, "Dislike"), (1, "Like"))

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        """
        Create and save a user with the given email, password, and username.
        """
        if not email:
            raise ValueError('The Email field must be set')
        if not password:
            raise ValueError('The Password field must be set')
        if not username:
            raise ValueError('The Username field must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        unique=True
    )

    username = models.TextField(
        max_length=50,
        unique=True
    )

    user_picture = models.ImageField(
        upload_to='profile_pictures',
        blank=True
    )

    user_text = models.TextField(
        blank=True
    )

    joined_at = models.DateTimeField(
        auto_now_add=True
    )

    is_active = models.BooleanField(
        default=True
    )

    is_staff = models.BooleanField(
        default=False
    )

    def switch_active(self):
        self.is_active = not self.is_active
        self.save()

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'password']



class FollowRelation(models.Model):
    followed_at = models.DateTimeField()

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following_user")
    followed_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followed_user")

    class Meta:
        ordering = ['-followed_at']


class Post(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField()

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post_user")


class PostComment(models.Model):
    '''
    Model for the comment on a post
    '''
    content = models.TextField()
    
    created_at = models.DateTimeField()

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comment_post"
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comment_user"
    )


class PostVote(models.Model):
    '''
    Model to vote on a post
    '''
    status = models.IntegerField(choices=VOTE)

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="vote_post"
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="vote_user"
    )