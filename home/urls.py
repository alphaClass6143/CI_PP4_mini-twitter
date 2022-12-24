
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('new_post/', views.new_post, name='new_post'),
    path('logout/', views.logout_user, name='logout'),
    # path('logout/', auth_views.LogoutView.as_view(next_page=''), name='logout'),
    # path('<str:username>/', views.profile, name='profile'),
]