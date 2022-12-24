
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views

handler401 = views.custom_401

urlpatterns = [
    path('', views.home, name='home'),
    path('new_post/', views.new_post, name='new_post'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('load_posts/<int:offset>/', views.load_posts, name='load_posts'),
    path('login/', views.login_user, name='login'),
    # path('profile/<str:username>/', views.profile, name='profile'),
    path('post/<int:post_id>', views.view_post, name='view_post'),
    path('post/<int:post_id>/edit/', views.edit_post, name='edit_post'),
    # path('post/<int:post_id>/delete/', views.delete_tweet, name='delete_post'),
    # path('<str:username>/follow/', views.follow, name='follow'),
    # path('<str:username>/unfollow/', views.unfollow, name='unfollow'),
    # path('post/<int:post_id>/like/', views.like, name='like'),
    # path('post/<int:post_id>/unlike/', views.unlike, name='unlike'),
    # path('logout/', auth_views.LogoutView.as_view(next_page=''), name='logout'),
    # path('<str:username>/', views.profile, name='profile'),
]