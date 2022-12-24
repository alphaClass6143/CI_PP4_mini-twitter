from django.db import models

# Create your models here.
from django.contrib.auth.models import User


from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.TextField(max_length=50)
    user_picture = models.ImageField(upload_to='profile_pictures', blank=True)
    user_text = models.TextField(blank=True)
    joined_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    def switch_active(self):
        self.is_active = not self.is_active
        self.save()

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'



class FollowRelation(models.Model):
    date_followed = models.DateTimeField()

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following_user")
    user_followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followed_user")

    class Meta:
        ordering = ['-date_followed']


class Post(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField()

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post_user")

class PostComment(models.Model):
    content = models.TextField()
    
    created_at = models.DateTimeField()

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