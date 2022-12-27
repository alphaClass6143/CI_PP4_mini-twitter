'''
Home views
'''
import json

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Count, Sum, Case, When

from accounts.models import User
from post.models import Post, PostVote
from profiles.models import FollowRelation

from home.forms import SearchForm
from post.forms import PostForm


def home(request):
    '''
    Loads the home page
    '''
    post_list = (Post.objects.all()
                 .order_by('-created_at')
                 [:20]).annotate(
                    comment_count=Count('comment_post'),
                    num_likes=Sum(Case(
                        When(vote_post__type=1, then=1), default=0)),
                    num_dislikes=Sum(Case(
                        When(vote_post__type=0, then=1), default=0))
                )

    form = PostForm()

    for post in post_list:
        # Calculate Like/Dislike ratio
        if post.num_likes + post.num_dislikes > 0:
            post.vote_ratio = (post.num_likes / (post.num_likes + post.num_dislikes)) * 100

        else:
            post.vote_ratio = 0

        # Check if the request user has liked or disliked the post
        if (
            request.user.is_authenticated
            and PostVote.objects.filter(post=post,
                                        user=request.user).exists()
        ):
            post.user_vote = (
                'like'
                if PostVote.objects.get(post=post, user=request.user).type == 1 else
                'dislike'
            )

    return render(request,
                  'home/index.html',
                  {'post_list': post_list, 'form': form})


def load_posts(request, offset):
    '''
    Loads additional posts
    '''
    print("load posts")
    limit = 2
    post_list = (Post.objects.all()
                 .order_by('-created_at')
                 [int(offset):int(offset)+limit]).annotate(
                    comment_count=Count('comment_post'),
                    num_likes=Sum(Case(
                              When(vote_post__type=1, then=1), default=0)),
                    num_dislikes=Sum(Case(
                              When(vote_post__type=0, then=1), default=0))
                )

    new_post_list = []
    for post in post_list:

        # Calculate Like/Dislike ratio
        if post.num_likes + post.num_dislikes > 0:
            post.vote_ratio = (
                (post.num_likes / (post.num_likes + post.num_dislikes))
                * 100
            )
        else:
            post.vote_ratio = 0

        new_post = {
                'id': post.id,
                'user': {
                    'username': post.user.username,
                    'user_picture': post.user.user_picture
                },
                'comment_count': post.comment_count,
                'content': post.content,
                'created_at': post.created_at.strftime('%b. %d, %Y, %I:%M %p'),
                'vote_ratio': post.vote_ratio,
        }

        # Check if the request user has liked or disliked the post
        if (
            request.user.is_authenticated
            and PostVote.objects.filter(post=post,
                                        user=request.user).exists()
        ):
            post.user_vote = (
                'like'
                if PostVote.objects.get(post=post, user=request.user).type == 1 else
                'dislike'
            )

        new_post_list.append(new_post)

    return HttpResponse(json.dumps(list(new_post_list)),
                        content_type='application/json')


def feed(request):
    '''
    Renders users feed (posts from followed accounts)
    '''
    if request.user.is_authenticated:
        followed_list = (FollowRelation.objects
                         .filter(user=request.user).values('followed_user'))

        post_list = (Post.objects.filter(user__in=followed_list)
                     .order_by('-created_at')
                     [:20]).annotate(
                        comment_count=Count('comment_post'),
                        num_likes=Sum(Case(
                                  When(vote_post__type=1, then=1), default=0)),
                        num_dislikes=Sum(Case(
                                     When(vote_post__type=0, then=1), default=0))
                )

        form = PostForm()
        for post in post_list:
            # Calculate Like/Dislike ratio
            if post.num_likes + post.num_dislikes > 0:
                post.vote_ratio = (
                    (post.num_likes / (post.num_likes + post.num_dislikes))
                    * 100
                )
            else:
                post.vote_ratio = 0

            # Check if the request user has liked or disliked the post
            if (
                request.user.is_authenticated
                and PostVote.objects.filter(post=post,
                                            user=request.user).exists()
            ):
                post.user_vote = (
                    'like'
                    if PostVote.objects.get(post=post, user=request.user).type == 1 else
                    'dislike'
                )

        return render(request,
                      'home/feed.html',
                      {'post_list': post_list, 'form': form})
    return redirect('home')


def load_feed_posts(request, offset):
    '''
    Loads more posts for the feed
    '''
    if request.user.is_authenticated:
        followed_list = (FollowRelation.objects
                         .filter(user=request.user).values('followed_user'))

        # Get post list with likes/dislikes and comment count
        query_post_list = (Post.objects.filter(user__in=followed_list)
                           .order_by('-created_at')
                           [int(offset):int(offset)+20]).annotate(
                        comment_count=Count('comment_post'),
                        num_likes=Sum(Case(
                                  When(vote_post__type=1, then=1), default=0)),
                        num_dislikes=Sum(Case(
                                     When(vote_post__type=0, then=1), default=0))
                    )

        post_list = []
        for post in query_post_list:
            
            # Calculate Like/Dislike ratio
            if post.num_likes + post.num_dislikes > 0:
                post.vote_ratio = (
                    (post.num_likes / (post.num_likes + post.num_dislikes))
                    * 100
                )
            else:
                post.vote_ratio = 0

            new_post = {
                    'id': post.id,
                    'user': {
                        'username': post.user.username,
                        'user_picture': post.user.user_picture
                    },
                    'comment_count': post.comment_count,
                    'content': post.content,
                    'created_at': post.created_at.strftime('%b. %d, %Y, %I:%M %p'),
                    'vote_ratio': post.vote_ratio,
            }

            # Check if the request user has liked or disliked the post
            if (
                request.user.is_authenticated
                and PostVote.objects.filter(post=post,
                                            user=request.user).exists()
            ):
                post.user_vote = (
                    'like'
                    if PostVote.objects.get(post=post, user=request.user).type == 1 else
                    'dislike'
                )

            post_list.append(new_post)

        return HttpResponse(json.dumps(list(post_list)),
                            content_type='application/json')


def search(request):
    '''
    Search posts
    '''
    form = SearchForm(request.GET)
    if form.is_valid():
        query = form.cleaned_data['query']

        post_list = (Post.objects.all()
                     .filter(content__icontains=query)[:20].annotate(
                    comment_count=Count('comment_post'),
                    num_likes=Sum(Case(
                              When(vote_post__type=1, then=1), default=0)),
                    num_dislikes=Sum(Case(
                              When(vote_post__type=0, then=1), default=0))
                ))

        for post in post_list:
            # Calculate Like/Dislike ratio
            if post.num_likes + post.num_dislikes > 0:
                post.vote_ratio = (
                    (post.num_likes / (post.num_likes + post.num_dislikes))
                    * 100
                )
            else:
                post.vote_ratio = 0

            # Check if the request user has liked or disliked the post
            if (
                request.user.is_authenticated
                and PostVote.objects.filter(post=post,
                                            user=request.user).exists()
            ):
                post.user_vote = (
                    'like'
                    if PostVote.objects.get(post=post, user=request.user).type == 1 else
                    'dislike'
                )

        user_list = User.objects.filter(username__icontains=query)[:5]

        return render(request,
                      'home/search_result.html',
                      {'post_list': post_list,
                       'user_list': user_list,
                       'query': query})

    return redirect('home')
