
'''
Home url patterns
'''
from django.urls import path

from home import views

urlpatterns = [
    path('', views.home, name='home'),
    path('load_posts/<int:offset>/', views.load_posts, name='load_posts'),
    path('feed', views.feed, name='feed'),
    path('load_feed_posts/<int:offset>/', views.load_posts, name='load_posts'),
    path('search/', views.search, name='search'),
]
