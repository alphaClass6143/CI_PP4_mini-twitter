from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate
from django.http import HttpResponseRedirect
from .forms import LogInForm, PostForm, RegisterForm

from .models import Post, Profile, User

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
    post_list = Post.objects.all().order_by('-created_at')
    form = PostForm()
    return render(request, 'index.html', {'post_list': post_list, 'form': form})


def new_post(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = PostForm(request.POST)
            print(form["content"].value())
            if form.is_valid():
                print("VALID")
                profile_request = Profile.objects.get(user=request.user)
                Post.objects.create(
                    profile = profile_request,
                    content=form.cleaned_data['content'],
                    created_at= datetime.now()
                )
                return redirect('home')
        else:
            return render(request, '401.html', status=401)
    return redirect('home')

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
            Profile.objects.create(
                user=user
            )
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'signup.html', {'form': form})

def custom_401(request, exception):
    return render(request, '401.html', status=401)