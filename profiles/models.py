'''
Profile models
'''
from django.db import models

from accounts.models import User


class FollowRelation(models.Model):
    '''
    Follow relation model
    '''
    followed_at = models.DateTimeField()

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following_user"
    )

    followed_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="followed_user"
    )

    class Meta:
        '''
        Order
        '''
        ordering = ['-followed_at']
