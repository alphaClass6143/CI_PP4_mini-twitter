from django.db import models

# Create your models here.
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # profile_picture = models.ImageField(upload_to='profile_pictures', blank=True)
    profile_text = models.TextField()

    def __str__(self):
        return self.user.username



class FollowRelation(models.Model):
    date_followed = models.DateTimeField()

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following_user")
    user_followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followed_user")

    class Meta:
        ordering = ['-date_followed']


class Post(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField()

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="post_user")

class PostComment(models.Model):
    content = models.TextField()
    
    created_at = models.DateTimeField()

    post = models.ForeignKey(
        Post, 
        on_delete=models.CASCADE, 
        related_name="post"
    )

    profile = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="comment_user"
    )