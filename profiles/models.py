from django.db import models

from accounts.models import User



# Create your models here.
class FollowRelation(models.Model):
    followed_at = models.DateTimeField()

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following_user")
    followed_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followed_user")

    class Meta:
        ordering = ['-followed_at']