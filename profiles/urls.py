from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views

# handler401 = views.custom_401

urlpatterns = [
    path('profile/<str:username>/following', views.profile_following, name='profile_following'),
    path('profile/<str:username>/follower', views.profile_follower, name='profile_follower'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('profile/<str:username>/follow/', views.follow, name='follow'),
    path('profile/<str:username>/unfollow/', views.unfollow, name='unfollow'),
    path('settings/', views.settings, name='settings'),
    path('settings/change_password', views.change_password, name='change_password'),
]