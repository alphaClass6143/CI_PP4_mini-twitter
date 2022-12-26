'''
Home views
'''
import json

from django.shortcuts import render, redirect
from django.http import HttpResponse

from accounts.models import User
from post.models import Post

from home.forms import SearchForm
from post.forms import PostForm


def home(request):
    '''
    Loads the home page
    '''
    limit = 10
    offset = request.GET.get('offset', 0)
    post_list = (Post.objects.all()
                 .order_by('-created_at')
                 [int(offset):int(offset)+limit])

    form = PostForm()
    return render(request,
                  'home/index.html',
                  {'post_list': post_list, 'form': form})


def load_posts(request, offset):
    '''
    Loads additional posts
    '''
    limit = 10
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
