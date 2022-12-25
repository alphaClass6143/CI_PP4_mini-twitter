from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, login, authenticate
from django.http import HttpResponseRedirect, HttpResponse
from .forms import LogInForm, PostForm, RegisterForm, CommentForm
import json

from .models import Post, User, PostComment

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
    '''
    Allows to view the post
    '''
    # Query for the post
    post = get_object_or_404(Post, pk=post_id)

    # Add a new comment
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                PostComment.objects.create(
                    user = request.user,
                    post = post,
                    content=form.cleaned_data['content'],
                    created_at= datetime.now()
                )
                return redirect('view_post', post_id=post.id)
        else:
            return render(request, '401.html', status=401)
    else:
        form = CommentForm()

    # Get list of comments
    comment_list = PostComment.objects.filter(post=post)

    return render(request, 'post.html', {'post': post, 'comment_list': comment_list, 'form': form})

def edit_post(request, post_id):
    '''
    Edit post route
    '''
    post = Post.objects.get(id=post_id)

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():

            post.content = form.cleaned_data['content']
            post.save()
            return redirect('home')
    else:
        form = PostForm(initial={'content': post.content})
    return render(request, 'edit_post.html', {'form': form})

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

def profile(request, username):
    user = User.objects.get(username=username)
    post_list = Post.objects.filter(user=user).order_by('-created_at')

    return render(request, 'profile.html', {'user': user, 'post_list': post_list})

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