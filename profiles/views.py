from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, update_session_auth_hash

from accounts.models import User
from .forms import SettingsForm, PasswordChangeForm
from .models import FollowRelation
from post.models import Post


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

    return render(request,
                  'profile/profile.html',
                  {
                    'user': {
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

    return render(request,
                  'profile/profile_follow_list.html',
                  {
                    'user': user,
                    'type': 'Following',
                    'follow_list': follow_list
                  })


def profile_follower(request, username):
    '''
    Lists the follower of the profile
    '''
    user = get_object_or_404(User, username=username)

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
                    'user': user,
                    'type': 'Follower',
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
