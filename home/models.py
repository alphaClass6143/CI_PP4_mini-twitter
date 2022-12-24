from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class User(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        profile_picture = models.ImageField(
            upload_to='profile_pictures', 
            blank=True)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class FollowRelation(models.Model):
    date_followed = models.DateTimeField()

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    user_followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")


class Post(models.Model):
    content = models.TextField(
        max_length=500
    )
    created_on = models.DateTimeField()

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")

class Comment(models.Model):
    content = models.TextField(
        max_length = 500
    )
    
    created_on = models.DateTimeField()

    post = models.ForeignKey(
        Post, 
        on_delete=models.CASCADE, 
        related_name="comments"
    )

    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="user"
    )