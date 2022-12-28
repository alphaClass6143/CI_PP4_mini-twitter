'''
URL patterns for the profiles app
'''
from django.urls import path

from profiles import views

urlpatterns = [
    path('profile/<str:username>/following',
         views.profile_following,
         name='profile_following'),
    path('profile/<str:username>/follower',
         views.profile_follower,
         name='profile_follower'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('profile/<str:username>/load_profile_posts/<int:offset>',
         views.load_profile_posts,
         name='load_profile_posts'),
    path('profile/<str:username>/follow/', views.follow, name='follow'),
    path('profile/<str:username>/unfollow/',
         views.unfollow,
         name='unfollow'),
    path('settings/', views.settings, name='settings'),
    path('settings/change_password',
         views.change_password,
         name='change_password'),
]
