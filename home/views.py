'''
Home views
'''
import json

from django.shortcuts import render
from django.http import HttpResponse

from accounts.models import User
from post.models import Post

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
    return render(request, 'home/index.html', {'post_list': post_list, 'form': form})


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
