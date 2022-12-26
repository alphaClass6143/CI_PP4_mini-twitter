from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views

urlpatterns = [
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
 
]