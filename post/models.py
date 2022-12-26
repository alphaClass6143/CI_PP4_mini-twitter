'''
Post models
'''
from django.db import models

from accounts.models import User

VOTE = ((0, "Dislike"), (1, "Like"))


# Create your models here.
class Post(models.Model):
    '''
    Model for the post
    '''
    content = models.TextField()
    created_at = models.DateTimeField()

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="post_user"
    )


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
    type = models.IntegerField(choices=VOTE)

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
