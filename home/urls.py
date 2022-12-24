
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
    path('login/', views.login_user, name='login'),
    # path('logout/', auth_views.LogoutView.as_view(next_page=''), name='logout'),
    # path('<str:username>/', views.profile, name='profile'),
]