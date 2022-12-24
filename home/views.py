from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .forms import PostForm

from .models import Post, Profile

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
    return redirect('home')

def logout_user(request):
    logout(request)
    return redirect('home')