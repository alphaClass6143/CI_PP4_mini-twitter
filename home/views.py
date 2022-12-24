from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, login, authenticate
from django.http import HttpResponseRedirect, HttpResponse
from .forms import LogInForm, PostForm, RegisterForm
import json

from .models import Post, User

# Create your views here.
# def signup(request):
#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             user = User.objects.create_user(
#                 form.cleaned_data['username'],
#                 form.cleaned_data['email'],
#                 form.cleaned_data['password']
#             )
#             return redirect('login')
#     else:
#         form = SignUpForm()
#     return render(request, 'signup.html', {'form': form})

def home(request):
    limit = 10
    offset = request.GET.get('offset', 0)
    post_list = Post.objects.all().order_by('-created_at')[int(offset):int(offset)+limit]
    form = PostForm()
    return render(request, 'index.html', {'post_list': post_list, 'form': form})

def load_posts(request, offset):
    print(offset)
    limit = 10
    post_list = Post.objects.all().order_by('-created_at')[int(offset):int(offset)+limit]
    return HttpResponse(json.dumps([{'content': post.content, 'username': post.user.username} for post in post_list]), content_type='application/json')


def new_post(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = PostForm(request.POST)
            if form.is_valid():
                Post.objects.create(
                    user = request.user,
                    content=form.cleaned_data['content'],
                    created_at= datetime.now()
                )
                return redirect('home')
        else:
            return render(request, '401.html', status=401)
    return redirect('home')

def view_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'post.html', {'post': post})

# def edit_post(request, tweet_id):
#     tweet = Tweet.objects.get(id=tweet_id)
#     if request.method == 'POST':
#         form = TweetForm(request.POST)
#         if form.is_valid():
#             tweet.text = form.cleaned_data['text']
#             tweet.save()
#             return redirect('home')
#     else:
#         form = TweetForm(initial={'text': tweet.text})
#     return render(request, 'edit_tweet.html', {'form': form})

# def delete_post(request, tweet_id):
#     tweet = Tweet.objects.get(id=tweet_id)
#     tweet.delete()
#     return redirect('home')

def logout_user(request):
    logout(request)
    return redirect('home')

def login_user(request):
    if request.method == 'POST':
            form = LogInForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('home')
                else:
                    print("user does not exist")
    else:
        form = LogInForm()
    return render(request, 'login.html', {'form': form})

def register_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                form.cleaned_data['username'],
                form.cleaned_data['email'],
                form.cleaned_data['password']
            )
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'signup.html', {'form': form})

# def profile(request, username):
#     # user = Profile.objects.get(user.username=username)
#     post_list = Post.objects.filter(user=user).order_by('-created_at')
#     form = TweetForm()
#     return render(request, 'profile.html', {'user': user, 'post': post, 'form': form})

# def follow(request, username):
#     user = User.objects.get(username=username)
#     Profile.objects.create(
#                 user=user
#     )
#     FollowRelation.objects.create(follower=request.user, following=user)
#     return redirect('profile', username=username)

# def unfollow(request, username):
#     user = User.objects.get(username=username)
#     Follow.objects.filter(follower=request.user, following=user).delete()
#     return redirect('profile', username=username)


def custom_401(request, exception):
    return render(request, '401.html', status=401)