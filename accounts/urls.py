'''
Url paths for accounts app
'''
from django.urls import path

from accounts import views

urlpatterns = [
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
]
