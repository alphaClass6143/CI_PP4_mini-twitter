from django.shortcuts import render
from .forms import PostForm

from .models import Post

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
    posts = Post.objects.all().order_by('-created_at')
    form = PostForm()
    return render(request, 'index.html', {'posts': posts, 'form': form})
