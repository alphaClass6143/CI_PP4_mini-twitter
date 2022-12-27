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
                    num_likes=Sum(Case(When(vote_post__type=1, then=1), default=0)),
                    num_dislikes=Sum(Case(When(vote_post__type=0, then=1), default=0))
                )

    form = PostForm()

    for post in post_list:
        # Calculate Like/Dislike ratio
        if post.num_likes + post.num_dislikes > 0:
            post.vote_ratio = (post.num_likes / (post.num_likes + post.num_dislikes)) * 100
        else:
            post.vote_ratio = 0

        # Check if the request user has liked or disliked the post
        if request.user.is_authenticated and PostVote.objects.filter(post=post, user=request.user).exists():
            post.user_vote = 'like' if PostVote.objects.get(post=post, user=request.user).type == 1 else 'dislike'

    return render(request,
                  'home/index.html',
                  {'post_list': post_list, 'form': form})


def feed(request):
    '''
    Renders users feed (posts from followed accounts)
    '''
    if request.user.is_authenticated:
        followed_list = FollowRelation.objects.filter(user=request.user).values('followed_user')
        print(followed_list)

        post_list = (Post.objects.filter(user__in=followed_list)
                     .order_by('-created_at')
                     [:20])

        form = PostForm()
        print(post_list)
        return render(request,
                      'home/feed.html',
                      {'post_list': post_list, 'form': form})
    return redirect('home')


def load_feed_posts(request, offset):
    '''
    Loads more posts for the feed
    '''
    if request.user.is_authenticated:
        followed_list = FollowRelation.objects.filter(user=request.user).values('followed_user')

        limit = 20
        post_list = (Post.objects.filter(user__in=followed_list)
                     .order_by('-created_at')
                     [int(offset):int(offset)+limit])

        return HttpResponse(json.dumps([{
                'content': post.content,
                'username': post.user.username
                } for post in post_list]), content_type='application/json')

    return redirect('home')


def load_posts(request, offset):
    '''
    Loads additional posts
    '''
    print("load posts")
    limit = 20
    post_list = (Post.objects.all()
                 .order_by('-created_at')
                 [int(offset):int(offset)+limit])

    return HttpResponse(json.dumps([{
        'content': post.content,
        'username': post.user.username
        } for post in post_list]), content_type='application/json')


def search(request):
    '''
    Search posts
    '''
    form = SearchForm(request.GET)
    if form.is_valid():
        query = form.cleaned_data['query']

        post_list = Post.objects.filter(content__icontains=query)[:20]

        user_list = User.objects.filter(username__icontains=query)[:5]

        return render(request,
                      'home/search_result.html',
                      {'post_list': post_list,
                       'user_list': user_list,
                       'query': query})

    return redirect('home')


