from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, login, authenticate
from django.http import HttpResponseRedirect, HttpResponse
from .forms import LogInForm, PostForm, RegisterForm, CommentForm
import json
from django.contrib import messages

from .models import Post, User, PostComment, FollowRelation, PostVote

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

    # Calculate Like/Dislike ratio
    like_votes = PostVote.objects.filter(post=post, type=0).count()
    dislike_votes = PostVote.objects.filter(post=post, type=1).count()
    if like_votes + dislike_votes > 0:
        vote_ratio = (like_votes / (like_votes + dislike_votes)) * 100
    else:
        vote_ratio = 0

    return render(request, 'post.html', {'post': post, 'comment_list': comment_list, 'vote_ratio': vote_ratio, 'form': form})

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
            return redirect('view_post', post_id=post_id)
        else:
            return render(request, 'edit_post.html', {'form': form, 'error_message': 'Invalid input'})
    else:
        form = PostForm(initial={'content': post.content})
        return render(request, 'edit_post.html', {'form': form})

def delete_post(request, post_id):
    post = Post.objects.get(id=post_id)
    if post.user == request.user:
        post.delete()
        return redirect('home')
    else:
        return redirect('view_post')

def vote_post(request, post_id, type):
    post = Post.objects.get(id=post_id)

    if PostVote.objects.filter(post=post, user=request.user).exists:
        vote = PostVote.objects.filter(post=post, user=request.user)
    else:
        PostComment.objects.create(
            type = type,
            post = post,
            user = request.user
        )
    
    return redirect('view_post', post_id=post_id)

def logout_user(request):
    logout(request)
    return redirect('home')

def login_user(request):
    '''
    Displays login page and logs the user in
    '''
    if request.method == 'POST':
            form = LogInForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data.get('email')
                password = form.cleaned_data.get('password')
                user = authenticate(request, email=email, password=password)
                print(user)
                if user is not None:
                    login(request, user)
                    return redirect('home')
                else:
                    return render(request, 'login.html', {'error_message': "Invalid login credentials"})
    else:
        form = LogInForm()
    return render(request, 'login.html', {'form': form})


def register_user(request):
    '''
    Displays register page and registers user
    '''
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            password_confirm = request.POST['password_confirm']

            if password != password_confirm:
                return render(request, 'register.html', {'error_message': "Passwords do not match"})

            if User.objects.filter(username=username).exists():
                return render(request, 'register.html', {'error_message': "Username is already taken"})

            if User.objects.filter(email=email).exists():
                return render(request, 'register.html', {'error_message': "Email address is already taken"})
            
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'register.html', {'error_message': "Invalid input"})
    else:
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})

def profile(request, username):
    user = get_object_or_404(User, username=username)
    post_list = Post.objects.filter(user=user).order_by('-created_at')

    if request.user.is_authenticated and request.user != user:
        is_following = FollowRelation.objects.filter(user=request.user, followed_user=user).exists()
        return render(request, 'profile.html', {'user': user, 'is_following': is_following, 'post_list': post_list})

    return render(request, 'profile.html', {'user': {'username':user.username, 'profile_picture':user.user_picture}, 'post_list': post_list})

def profile_following(request, username):
    user = get_object_or_404(User, username=username)

    # follow_list = FollowRelation.objects.filter(user=user).only('followed_user')
    follow_list = [{'username':follow_relation.followed_user.username, 'user_picture':follow_relation.followed_user.user_picture} for follow_relation in FollowRelation.objects.filter(user=user)]

    return render(request, 'profile_follow_list.html', {'user': user, 'type':'Following', 'follow_list': follow_list})


def profile_follower(request, username):
    user = get_object_or_404(User, username=username)

    follow_list = [{'username':follow_relation.followed_user.username, 'user_picture':follow_relation.followed_user.user_picture} for follow_relation in FollowRelation.objects.filter(followed_user=user)]
    return render(request, 'profile_follow_list.html', {'user': user, 'type':'Follower', 'follow_list': follow_list})


def follow(request, username):
    user = User.objects.get(username=username)

    FollowRelation.objects.create(
        user=request.user,
        followed_user=user,
        followed_at=datetime.now()
    )
    return redirect('profile', username=username)

def unfollow(request, username):
    user = User.objects.get(username=username)
    FollowRelation.objects.filter(
        user=request.user,
        followed_user=user).delete()
    return redirect('profile', username=username)


def custom_401(request, exception):
    return render(request, '401.html', status=401)