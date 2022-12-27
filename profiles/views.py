'''
Profile views
'''
import json

from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.db.models import Count, Sum, Case, When
from django.http import HttpResponse

from profiles.models import FollowRelation
from post.models import Post, PostVote
from accounts.models import User

from profiles.forms import SettingsForm, PasswordChangeForm


# Create your views here.
def settings(request):
    '''
    Settings route
    '''
    if request.user.is_authenticated:
        user = request.user

        if request.method == 'POST':
            form = SettingsForm(request.POST)
            if form.is_valid():

                if not User.objects.filter(username=form.cleaned_data.get('username')).exists() or form.cleaned_data.get('username') == user.username:
                    user.username = form.cleaned_data.get('username')
                else:
                    return render(request,
                                  'profile/settings.html',
                                  {
                                    'form': form,
                                    'error_message': 'Username is already taken'
                                })

                user.user_text = form.cleaned_data.get('user_text')
                user.user_picture = form.cleaned_data.get('user_picture')

                user.save(update_fields=['username',
                                         'user_text',
                                         'user_picture'])

                return render(request,
                              'profile/settings.html',
                              {
                               'form': form,
                               'success_message': "You have successfully changed your profile settings"
                              })

            return render(request,
                          'profile/settings.html',
                          {'form': form, 'error_message': 'Invalid input'})

        return render(request,
                      'profile/settings.html',
                      {'user': {
                        'username': user.username,
                        'user_text': user.user_text,
                        'user_picture': user.user_picture
                    }})

    return render(request, 
                  'home/index.html',
                  {'error_message': 'You cannot access this area!'})


def change_password(request):
    '''
    Change password
    '''
    if request.user.is_authenticated:
        user = request.user

        if request.method == 'POST':
            form = PasswordChangeForm(request.POST)
            if form.is_valid():
                    
                if form.cleaned_data.get('password') == form.cleaned_data.get('password_confirm'):
                    user.set_password(form.cleaned_data.get('password'))
                    user.save()

                    updated_user = authenticate(request, email=user.email, password=form.cleaned_data.get('password'))
                    login(request, updated_user)
                    return render(request, 'profile/settings.html', {'user': {'username': user.username, 'user_text':user.user_text, 'user_picture':user.user_picture}, 'success_message':'You have successfully changed your password'})

                return render(request, 'profile/settings.html', {'form': form, 'error_message': 'Passwords do not match'})

            return render(request, 'profile/settings.html', {'form': form, 'error_message': 'Invalid input'})
        else:
            return render(request, 'profile/settings.html', {'user': {'username': user.username, 'user_text':user.user_text, 'user_picture':user.user_picture}})
    else:
        return render(request, 'home/index.html', {'error_message': 'You cannot access this area!'})


def profile(request, username):
    '''
    Shows the profile
    '''
    user = get_object_or_404(User, username=username)

    post_list = Post.objects.filter(user=user).order_by('-created_at')

    if request.user.is_authenticated and request.user != user:
        is_following = FollowRelation.objects.filter(user=request.user, followed_user=user).exists()
    else:
        is_following = False

    following_count = FollowRelation.objects.filter(user=user).count()
    follower_count = FollowRelation.objects.filter(followed_user=user).count()

    post_list = (Post.objects.filter(user=user)
                .order_by('-created_at')
                [:2]).annotate(
                comment_count=Count('comment_post'),
                num_likes=Sum(Case(When(vote_post__type=1, then=1), default=0)),
                num_dislikes=Sum(Case(When(vote_post__type=0, then=1), default=0))
        )


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
                  'profile/profile.html',
                  {
                    'profile': {
                        'username': user.username,
                        'user_text': user.user_text,
                        'user_picture': user.user_picture
                    },
                    'post_count': len(post_list),
                    'is_following': is_following,
                    'following_count': following_count,
                    'follower_count': follower_count,
                    'post_list': post_list
                    })

def load_profile_posts(request, username, offset):
    '''
    Loads additional posts
    '''
    user = get_object_or_404(User, username=username)
    limit = 2

    post_list = (Post.objects.filter(user=user)
                .order_by('-created_at')
                [int(offset):int(offset)+limit]).annotate(
                comment_count=Count('comment_post'),
                num_likes=Sum(Case(When(vote_post__type=1, then=1), default=0)),
                num_dislikes=Sum(Case(When(vote_post__type=0, then=1), default=0))
                )
    
    new_post_list = []
    for post in post_list:
        
        # Calculate Like/Dislike ratio
        if post.num_likes + post.num_dislikes > 0:
            post.vote_ratio = (post.num_likes / (post.num_likes + post.num_dislikes)) * 100
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
        if request.user.is_authenticated and PostVote.objects.filter(post=post, user=request.user).exists():
            new_post['user_vote'] = 'like' if PostVote.objects.get(post=post, user=request.user).type == 1 else 'dislike'

        new_post_list.append(new_post)

    return HttpResponse(json.dumps(list(new_post_list)), content_type='application/json')

def profile_following(request, username):
    '''
    Lists the follows of the profile
    '''
    user = get_object_or_404(User, username=username)

    follow_list = [
        {
            'username': follow_relation.followed_user.username,
            'user_picture': follow_relation.followed_user.user_picture
        }
        for follow_relation
        in FollowRelation.objects.filter(user=user)]

    if request.user.is_authenticated and request.user != user:
        is_following = FollowRelation.objects.filter(user=request.user, followed_user=user).exists()
    else:
        is_following = False

    following_count = FollowRelation.objects.filter(user=user).count()
    follower_count = FollowRelation.objects.filter(followed_user=user).count()

    return render(request,
                  'profile/profile_follow_list.html',
                  {
                    'profile': {
                        'username': user.username,
                        'user_text': user.user_text,
                        'user_picture': user.user_picture
                    },
                    'type': 'Following',
                    'is_following': is_following,
                    'following_count': following_count,
                    'follower_count': follower_count,
                    'follow_list': follow_list
                  })


def profile_follower(request, username):
    '''
    Lists the follower of the profile
    '''
    user = get_object_or_404(User, username=username)

    if request.user.is_authenticated and request.user != user:
        is_following = FollowRelation.objects.filter(user=request.user, followed_user=user).exists()
    else:
        is_following = False

    following_count = FollowRelation.objects.filter(user=user).count()
    follower_count = FollowRelation.objects.filter(followed_user=user).count()

    follow_list = [
        {
            'username': follow_relation.followed_user.username,
            'user_picture': follow_relation.followed_user.user_picture
        }
        for follow_relation
        in FollowRelation.objects.filter(followed_user=user)]

    return render(request,
                  'profile/profile_follow_list.html',
                  {
                    'profile': {
                        'username': user.username,
                        'user_text': user.user_text,
                        'user_picture': user.user_picture
                    },
                    'type': 'Follower',
                    'is_following': is_following,
                    'following_count': following_count,
                    'follower_count': follower_count,
                    'follow_list': follow_list
                  })


def follow(request, username):
    '''
    Follows a user
    '''
    if request.user.is_authenticated:
        user = User.objects.get(username=username)

        FollowRelation.objects.create(
            user=request.user,
            followed_user=user,
            followed_at=datetime.now()
        )
    return redirect('profile', username=username)


def unfollow(request, username):
    '''
    Unfollows the user
    '''
    if request.user.is_authenticated:
        user = User.objects.get(username=username)
        FollowRelation.objects.filter(
            user=request.user,
            followed_user=user
        ).delete()

    return redirect('profile', username=username)
