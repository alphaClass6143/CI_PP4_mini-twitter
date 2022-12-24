from django.db import models

# Create your models here.
from django.contrib.auth.models import User

# class User(BaseUserManager):
#     """
#     Custom user model 
#     """
#     def create_user(self, email, password, **extra_fields):
#         if not email:
#             raise ValueError('The Email field must be set')

#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         profile_picture = models.ImageField(
#             upload_to='profile_pictures', 
#             blank=True)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, password, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         return self.create_user(email, password, **extra_fields)

# class CustomUser(AbstractUser):
#     username = None
#     email = models.EmailField(_('email address'), unique=True)

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []

#     objects = CustomUserManager()

#     def __str__(self):
#         return self.email

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # profile_picture = models.ImageField(upload_to='profile_pictures', blank=True)
    profile_text = models.TextField()


class FollowRelation(models.Model):
    date_followed = models.DateTimeField()

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following_user")
    user_followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followed_user")

    class Meta:
        ordering = ['-date_followed']


class Post(models.Model):
    content = models.TextField()
    created_on = models.DateTimeField()

    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="post_user")

class PostComment(models.Model):
    content = models.TextField()
    
    created_on = models.DateTimeField()

    post = models.ForeignKey(
        Post, 
        on_delete=models.CASCADE, 
        related_name="post"
    )

    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="comment_user"
    )